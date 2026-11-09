"""Precompute source-bound subissue log archives; HTTP never performs compression."""
from __future__ import annotations

from collections import defaultdict
from datetime import date
from hashlib import file_digest, sha256
import json
from pathlib import Path
import re
import tempfile
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED


def safe_name(value: str, limit=120):
    value = re.sub(r'[\\/:*?"<>|\x00-\x1f\x7f\u202a-\u202e\u2066-\u2069]', '_', value)
    return value.strip(' .')[:limit].rstrip(' .') or 'log'


def prepare_log_archives(directory: Path, attachments: Path, records: list[dict], subthemes: list[dict],
                         *, business_date: str, source_sha256: str):
    by_sub = defaultdict(list)
    for record in records:
        for item in record['files']:
            if item['kind'] == 'log':
                by_sub[record['subtheme_id']].append((record['id'], item))
    directory.mkdir(parents=True, exist_ok=True)
    day = date.fromisoformat(business_date)
    stamp = (max(1980, day.year), day.month, day.day, 0, 0, 0)
    archives = {}
    for sub in subthemes:
        members = sorted(by_sub.get(sub['id'], []), key=lambda pair: (pair[0], pair[1]['id']))
        sub['log_archive'] = None
        if not members:
            continue
        count = len(members)
        mail_count = len({key for key, _ in members})
        if any(not item['ready'] for _, item in members):
            sub['log_archive'] = {'status': 'unavailable', 'file_count': count, 'mail_count': mail_count,
                                  'disabled_reason': '该子组存在尚未校验的日志，暂不提供不完整压缩包'}
            continue
        entries = []
        for key, item in members:
            if not str(key).isdigit() or not str(item['id']).isdigit():
                raise ValueError('archive source IDs must be numeric')
            entries.append({'mail_pk': key, 'attachment_id': item['id'], 'filename': item['name'],
                            'size': item['size'], 'sha256': item['sha256'],
                            'entry': f'mail_{key}/attachment_{item["id"]}_{safe_name(item["name"])}'})
        manifest = {'format': 'subissue-original-logs/v1', 'business_date': business_date,
                    'source_snapshot_sha256': source_sha256, 'subtheme_id': sub['id'],
                    'subtheme_name': sub['name'], 'file_count': count, 'mail_count': mail_count, 'files': entries}
        payload = json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
        archive_id = sha256(payload).hexdigest()
        destination = directory / (archive_id + '.zip')
        with tempfile.NamedTemporaryFile(dir=directory, prefix=archive_id + '.', suffix='.tmp', delete=False) as temp:
            temporary = Path(temp.name)
        try:
            with ZipFile(temporary, 'w', compression=ZIP_DEFLATED, compresslevel=6, allowZip64=True) as archive:
                def info(name):
                    item = ZipInfo(name, date_time=stamp)
                    item.compress_type = ZIP_DEFLATED
                    item.create_system = 3
                    item.external_attr = 0o100600 << 16
                    return item
                archive.writestr(info('_manifest.json'), payload)
                for entry in entries:
                    digest, size = sha256(), 0
                    original = attachments / (entry['attachment_id'] + '.bin')
                    with original.open('rb') as source, archive.open(info(entry['entry']), 'w') as target:
                        while chunk := source.read(256_000):
                            digest.update(chunk)
                            size += len(chunk)
                            target.write(chunk)
                    if digest.hexdigest() != entry['sha256'] or size != entry['size']:
                        raise ValueError('archive original log integrity mismatch')
            temporary.replace(destination)
        finally:
            temporary.unlink(missing_ok=True)
        with destination.open('rb') as stream:
            digest = file_digest(stream, 'sha256').hexdigest()
        meta = {'id': archive_id, 'status': 'ready', 'subtheme_id': sub['id'], 'file_count': count,
                'mail_count': mail_count, 'filename': f'{business_date}_{safe_name(sub["name"], 65)}_日志_{count}份.zip',
                'size': destination.stat().st_size, 'sha256': digest}
        sub['log_archive'] = meta
        archives[archive_id] = meta
    return archives
