"""Download only a frozen mail manifest via read-only IMAP; never touches a DB."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from email import message_from_bytes
from hashlib import sha1, sha256
import imaplib
import json
from pathlib import Path
import re
import ssl
import threading
import time

from .config import ROOT

MAX_MESSAGE_BYTES = 100 * 1024 * 1024
LOCK = threading.Lock()


def atomic_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    staging = path.with_suffix('.tmp')
    staging.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    staging.replace(path)


def import_service_parameters(source: Path, destination: Path):
    """Explicit user-authorized one-time import; never echoes account secrets."""
    text = source.read_text(encoding='utf-8-sig')
    host, port, accounts, pending = 'imap.feishu.cn', 993, {}, None
    for line in map(str.strip, text.splitlines()):
        if not line:
            continue
        if re.fullmatch(r'[^@\s]+@[^@\s]+\.[A-Za-z0-9.-]+', line):
            pending = line.lower()
        elif '：' in line or ':' in line:
            key, value = re.split('[：:]', line, maxsplit=1)
            if 'IMAP' in key and '地址' in key and value.strip():
                host = value.strip()
            elif 'IMAP' in key and '端口' in key:
                port = int(re.sub(r'\D', '', value))
            pending = None
        elif pending:
            accounts[pending] = line
            pending = None
    if not accounts or port != 993 or host != 'imap.feishu.cn':
        raise ValueError('mail service must be the confirmed TLS IMAP endpoint')
    atomic_json(destination, {'host': host, 'port': port, 'accounts': accounts,
                             'imported_from_sha256': sha256(source.read_bytes()).hexdigest()})
    return len(accounts)


def mime_attachments(raw: bytes, uid: int, expected: list[dict], expected_message_id: str = '') -> dict[str, bytes]:
    message = message_from_bytes(raw)
    actual_id = str(message.get('Message-ID') or '').strip()
    if expected_message_id and actual_id != expected_message_id.strip():
        raise ValueError('MESSAGE_ID_MISMATCH')
    wanted = {str(row['attachment_id']): row for row in expected}
    found = {}
    # Identical walk ordinals and content digests to AICS app/imap_parse.py.
    for index, part in enumerate(message.walk()):
        if part.is_multipart():
            continue
        data = part.get_payload(decode=True) or b''
        digest = sha1(data).hexdigest()[:16] if data else f'empty{index}'
        key = f'imap-{uid}-{index}-{digest}'
        if key in wanted:
            expected_size = int(wanted[key].get('size_bytes') or 0)
            if expected_size and expected_size != len(data):
                raise ValueError('ATTACHMENT_SIZE_MISMATCH')
            found[str(wanted[key]['id'])] = data
    return found


def download(snapshot_path: Path, service_path: Path, output: Path, *, workers=2):
    snapshot = json.loads(snapshot_path.read_text(encoding='utf-8'))
    config = json.loads(service_path.read_text(encoding='utf-8'))
    if config['host'] != 'imap.feishu.cn' or config['port'] != 993:
        raise ValueError('unexpected mail endpoint')
    output = output.resolve()
    output.relative_to((ROOT / '.runtime').resolve())
    output.mkdir(parents=True, exist_ok=True)
    manifest_path = output / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {
        'source_snapshot_sha256': sha256(snapshot_path.read_bytes()).hexdigest(),
        'source_id': snapshot['source_id'], 'business_date': snapshot['business_date'],
        'transport': 'IMAPS EXAMINE + BODY.PEEK[]', 'files': {}}
    if manifest['source_snapshot_sha256'] != sha256(snapshot_path.read_bytes()).hexdigest():
        raise ValueError('manifest belongs to another source snapshot')
    expected_by_mail = {}
    for entry in snapshot['attachments']:
        item = entry['payload']
        if not re.fullmatch(r'\d+', str(item['id'])):
            raise ValueError('unexpected local attachment key')
        expected_by_mail.setdefault(str(item['message_pk']), []).append(item)
    jobs = {}
    for mail in snapshot['mails']:
        if str(mail['mail_pk']) in expected_by_mail:
            jobs.setdefault(mail['mailbox'].lower(), []).append(mail)

    def persist():
        manifest['updated_at'] = datetime.now(timezone.utc).isoformat()
        atomic_json(manifest_path, manifest)

    def record(item, **values):
        with LOCK:
            previous = manifest['files'].get(str(item['id']), {})
            manifest['files'][str(item['id'])] = {
                **previous, 'id': str(item['id']), 'mail_pk': str(item['message_pk']),
                'filename': item.get('filename') or 'attachment',
                'content_type': item.get('content_type') or 'application/octet-stream',
                'expected_size': int(item.get('size_bytes') or 0), **values}
            persist()

    def cached(item):
        saved = manifest['files'].get(str(item['id']), {})
        p = output / (str(item['id']) + '.bin')
        return saved.get('status') == 'ready' and p.is_file() and sha256(p.read_bytes()).hexdigest() == saved.get('sha256')

    def work(mailbox, mails):
        password = config['accounts'].get(mailbox)
        box = None
        selected = None
        selected_validity = None
        for mail in mails:
            items = [item for item in expected_by_mail[str(mail['mail_pk'])] if not cached(item)]
            if not items:
                continue
            if not password:
                for item in items:
                    record(item, status='failed', error='MAILBOX_CREDENTIAL_NOT_CONFIGURED')
                continue
            source = mail['raw_payload']
            uid = int(source.get('imap_uid') or 0)
            validity = int(source.get('imap_uidvalidity') or 0)
            folder = source.get('imap_folder') or 'INBOX'
            if not uid or not validity or any(c in folder for c in '\r\n'):
                for item in items:
                    record(item, status='failed', error='MISSING_IMAP_IDENTITY')
                continue
            for attempt in range(1, 4):
                try:
                    if box is None:
                        box = imaplib.IMAP4_SSL(config['host'], config['port'], ssl_context=ssl.create_default_context(), timeout=40)
                        if box.login(mailbox, password)[0] != 'OK':
                            raise RuntimeError('LOGIN_FAILED')
                        selected = None
                        selected_validity = None
                    if selected != folder:
                        quoted = '"' + folder.replace('\\', '\\\\').replace('"', '\\"') + '"'
                        if box.select(quoted, readonly=True)[0] != 'OK':
                            raise RuntimeError('EXAMINE_FAILED')
                        current = box.response('UIDVALIDITY')[1]
                        selected_validity = int(current[0]) if current and current[0] else None
                        selected = folder
                    # The selected namespace belongs to this connection, while
                    # every frozen message can carry a different source epoch.
                    if selected_validity != validity:
                        raise ValueError('UIDVALIDITY_MISMATCH')
                    kind, size_data = box.uid('FETCH', str(uid), '(UID RFC822.SIZE)')
                    sizes = re.findall(rb'RFC822\.SIZE (\d+)', b' '.join(v for v in size_data or [] if isinstance(v, bytes)))
                    # Some servers return OK with no SIZE. That is not proof the
                    # message exceeds the cap; the fetched bytes are checked below.
                    if kind == 'OK' and sizes and int(sizes[0]) > MAX_MESSAGE_BYTES:
                        raise ValueError('MESSAGE_SIZE_UNAVAILABLE_OR_LIMITED')
                    kind, parts = box.uid('FETCH', str(uid), '(UID BODY.PEEK[])')
                    raw = next((p[1] for p in parts or [] if isinstance(p, tuple) and isinstance(p[1], bytes) and re.search(rb'\bUID ' + str(uid).encode() + rb'\b', p[0])), None)
                    if kind != 'OK' or raw is None:
                        raise RuntimeError('FETCH_FAILED')
                    if len(raw) > MAX_MESSAGE_BYTES:
                        raise ValueError('MESSAGE_SIZE_UNAVAILABLE_OR_LIMITED')
                    found = mime_attachments(raw, uid, items, mail.get('smtp_message_id') or '')
                    for item in items:
                        key = str(item['id'])
                        if key not in found:
                            record(item, status='failed', error='PART_DIGEST_NOT_MATCHED', attempt=attempt)
                            continue
                        content = found[key]
                        dest = output / (key + '.bin')
                        staging = dest.with_suffix('.part')
                        staging.write_bytes(content)
                        staging.replace(dest)
                        record(item, status='ready', path=dest.name, size=len(content), sha256=sha256(content).hexdigest(),
                               downloaded_at=datetime.now(timezone.utc).isoformat(), uid=uid, uidvalidity=validity,
                               identity_verified=True, error=None, attempt=attempt)
                    del raw
                    break
                except (OSError, imaplib.IMAP4.error, ValueError, RuntimeError) as exc:
                    if box is not None:
                        try:
                            box.logout()
                        except Exception:
                            pass
                    box, selected, selected_validity = None, None, None
                    if attempt == 3 or isinstance(exc, ValueError):
                        safe_error = str(exc) if isinstance(exc, ValueError) else type(exc).__name__
                        for item in items:
                            record(item, status='failed', error=safe_error, attempt=attempt)
                        break
                    time.sleep(attempt)
            time.sleep(.15)
        if box is not None:
            try:
                box.logout()
            except Exception:
                pass

    with ThreadPoolExecutor(max_workers=max(1, min(workers, 2))) as pool:
        futures = [pool.submit(work, mailbox, mails) for mailbox, mails in jobs.items()]
        for future in futures:
            future.result()
    with LOCK:
        persist()
    summary = {'expected': len(snapshot['attachments']), 'ready': sum(v.get('status') == 'ready' for v in manifest['files'].values()),
               'failed': sum(v.get('status') == 'failed' for v in manifest['files'].values())}
    print(json.dumps(summary), flush=True)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path, default=ROOT / '.runtime/cursor-verification-20261030/frozen-source.json')
    parser.add_argument('--service', type=Path, default=ROOT / '.secrets/mail-service.json')
    parser.add_argument('--output', type=Path, default=ROOT / '.runtime/daily-reports/2026-10-29/attachments')
    parser.add_argument('--import-parameters', type=Path)
    args = parser.parse_args()
    if args.import_parameters:
        print(json.dumps({'imported_accounts': import_service_parameters(args.import_parameters, args.service)}))
    result = download(args.snapshot, args.service, args.output)
    raise SystemExit(0 if result['ready'] == result['expected'] else 1)


if __name__ == '__main__':
    main()
