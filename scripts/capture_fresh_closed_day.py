"""Capture one closed day from production, then store that day locally.

The nightly job must not freeze the stale local replica. This reads production
once, read-only, repeatable-read, for the requested date only, then disconnects.
The persistent allow_production_read switch stays false. Global watermarks and
status are not advanced. A published report is left untouched and production
is not contacted.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys

import psycopg
from psycopg import sql
from psycopg.types.json import Jsonb

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from insights.catalog import load_static
from insights.config import Settings, connection_identity, loopback
from insights.daily_generation import conversation_graph, require_closed_source, write_json
from insights.db import source_connection, target_connection
from insights.model import folder_track
from insights.projection import publish_catalog, rebuild_projection, verify_projection
from insights.source import BY_NAME, TABLES, check_contract, source_rows
from insights.syncer import local_related_keys, mirror_relation, related_keys
from insights.time_rules import SHANGHAI, detect_fallback_skew, received_at

POLICY = ROOT / 'scripts' / 'daily-report-unattended-policy.json'
FRESH_RESPONSE = '不从本机冻结，每次都要从生产库获取新鲜数据'
PRESERVED = ('status', 'source_snapshot_at', 'last_sync_at', 'last_aux_at', 'last_reconcile_at', 'last_error_code', 'identity_hash')


def fail(reason):
    raise SystemExit(reason)


def require(condition, reason):
    if not condition:
        fail(reason)


def load_policy():
    policy = json.loads(POLICY.read_text(encoding='utf-8'))
    fresh = policy.get('fresh_data') or {}
    require(fresh.get('response') == FRESH_RESPONSE, 'FRESH_DATA_AUTHORIZATION_MISSING')
    require(fresh.get('mode') == 'always_production_closed_day', 'FRESH_DATA_MODE_MISMATCH')
    require(fresh.get('decided_by') == 'user', 'FRESH_DATA_DECIDER_MISSING')
    return policy


def load_settings():
    config_path = ROOT / '.secrets' / 'production.json'
    before = sha256(config_path.read_bytes()).hexdigest()
    settings = Settings.load(config_path)
    require(settings.allow_production_read is False, 'PERSISTENT_ISOLATION_REQUIRED')
    identity = connection_identity(settings.source_url)
    require(identity['host'] == '10.8.45.155' and identity['port'] == '5432', 'SOURCE_IDENTITY_MISMATCH')
    require(identity['dbname'] == 'ai_complaint_mail', 'SOURCE_DATABASE_MISMATCH')
    return config_path, before, settings


def assert_config_unchanged(config_path, before):
    require(sha256(config_path.read_bytes()).hexdigest() == before, 'PERSISTENT_CONFIG_CHANGED')
    require(Settings.load(config_path).allow_production_read is False, 'PERSISTENT_ISOLATION_CHANGED')


def parse_day(value):
    try:
        day = date.fromisoformat(value)
    except ValueError:
        fail('INVALID_BUSINESS_DATE')
    if day >= datetime.now(SHANGHAI).date():
        fail('BUSINESS_DAY_NOT_FINISHED')
    return day


def fetch_related(conn, settings, name, field, values):
    keys = set()
    ordered = sorted(values)
    for offset in range(0, len(ordered), 500):
        keys.update(related_keys(conn, settings, BY_NAME[name], field, ordered[offset:offset + 500]))
    return keys


def capture_day(settings, day):
    capture = {
        'format': 'complaint-closed-days-capture/v1',
        'business_dates': [day.isoformat()],
        'source_id': settings.source_id,
        'purpose': 'unattended fresh closed-day capture',
        'started_at': datetime.now(timezone.utc),
        'persistent_production_read_allowed': False,
        'source_read_only': True,
        'target_written': False,
        'tables': {},
        'day_scopes': {},
    }
    with source_connection(settings) as conn:
        contract = check_contract(conn, settings)
        require(conn.execute('SHOW transaction_read_only').fetchone()['transaction_read_only'] == 'on', 'SOURCE_NOT_READ_ONLY')
        require(conn.execute('SHOW transaction_isolation').fetchone()['transaction_isolation'] == 'repeatable read', 'SOURCE_NOT_REPEATABLE_READ')
        snapshot = conn.execute('SELECT transaction_timestamp() AS t').fetchone()['t']
        require(snapshot.astimezone(SHANGHAI).date() > day, 'DAY_NOT_CLOSED')
        capture['source_snapshot_at'] = snapshot
        print(json.dumps({'source_snapshot_at': snapshot.isoformat(), 'read_only': True}, default=str), flush=True)

        def fetch(name, keys=None):
            rows = [{**row, 'payload': json.loads(row['payload'])}
                    for row in source_rows(conn, settings, BY_NAME[name], keys=None if keys is None else sorted(keys))]
            capture['tables'][name] = rows
            print(json.dumps({'table': name, 'rows': len(rows)}), flush=True)
            return rows

        boxes = fetch('mailboxes')
        fetch('folders')
        mailboxes = {str(row['payload']['id']): row['payload']['email'] for row in boxes}
        relation = sql.SQL('{}.messages').format(sql.Identifier(settings.source_schema))
        query = sql.SQL('SELECT id,mailbox_id,folder_id,from_address,to_json,cc_json,'
                        'smtp_message_id,in_reply_to,references_json,internal_date,'
                        'date_header,first_seen_at FROM {} WHERE id>%s ORDER BY id LIMIT %s').format(relation)
        metadata, last = [], 0
        while True:
            page = conn.execute(query, (last, 500)).fetchall()
            metadata.extend(page)
            if not page or len(page) < 500:
                break
            last = int(page[-1]['id'])
            if len(metadata) % 5000 == 0:
                print(json.dumps({'metadata_rows': len(metadata), 'last_id': last}), flush=True)
        print(json.dumps({'metadata_rows': len(metadata), 'last_id': last}), flush=True)
        skew = detect_fallback_skew(metadata[-300:])
        normalized, undated_ids = [], []
        for row in metadata:
            instant, _ = received_at(row, skew)
            if instant is not None:
                normalized.append((row, instant.astimezone(SHANGHAI).date()))
            elif folder_track(row['folder_id']) not in ('SENT', 'DRAFT', 'TRASH'):
                undated_ids.append(str(row['id']))
        capture['undated_received_mail_ids'] = undated_ids
        require(not undated_ids, 'UNDETERMINED_RECEIVED_BUSINESS_DATE')
        day_ids, headers, totals = set(), [], Counter()
        for row, mail_day in normalized:
            received = folder_track(row['folder_id']) not in ('SENT', 'DRAFT', 'TRASH')
            if received and 0 <= (day - mail_day).days <= 14:
                totals[str(mail_day)] += 1
            if received and mail_day == day:
                day_ids.add(str(row['id']))
            if mail_day <= day:
                headers.append({
                    'mail_pk': str(row['id']), 'mailbox': mailboxes[str(row['mailbox_id'])],
                    'from_address': row['from_address'], 'recipients': row['to_json'] or [],
                    'cc': row['cc_json'] or [], 'smtp_message_id': row['smtp_message_id'],
                    'in_reply_to': row['in_reply_to'], 'references_json': row['references_json'],
                })
        graph = conversation_graph(headers)
        needed, pending = set(day_ids), deque(day_ids)
        while pending:
            for neighbor in graph.get(pending.popleft(), ()):
                if neighbor not in needed:
                    needed.add(neighbor)
                    pending.append(neighbor)
        closed_graph = conversation_graph([row for row in headers if row['mail_pk'] in needed])
        require(all(closed_graph[key] == graph[key] for key in needed), 'RFC_CLOSURE_LOSES_AMBIGUITY_WITNESS')
        require(totals[day.isoformat()] == len(day_ids), 'DAY_COUNT_MISMATCH')
        capture['day_scopes'][day.isoformat()] = {
            'business_date': day.isoformat(), 'day_mail_ids': sorted(day_ids, key=int),
            'context_mail_ids': sorted(needed - day_ids, key=int),
            'day_mail_count': len(day_ids), 'headers': headers,
            'daily': [{'business_date': str(day - timedelta(days=offset)),
                       'count': totals[str(day - timedelta(days=offset))]}
                      for offset in range(14, -1, -1)],
        }
        print(json.dumps({'day': day.isoformat(), 'mails': len(day_ids), 'context': len(needed - day_ids)}, ensure_ascii=False), flush=True)
        messages = fetch('messages', needed)
        require({row['record_key'] for row in messages} == needed, 'MESSAGE_COVERAGE_MISMATCH')
        attachment_ids = fetch_related(conn, settings, 'attachments', 'message_pk', day_ids)
        fetch('attachments', attachment_ids)
        inbound_ids = fetch_related(conn, settings, 'InboundMail', 'sourcePk', needed)
        fetch('InboundMail', inbound_ids)
        artifact_ids = fetch_related(conn, settings, 'MailAiArtifact', 'inboundMailId', inbound_ids)
        fetch('MailAiArtifact', artifact_ids)
        binding_ids = fetch_related(conn, settings, 'MailIssueBinding', 'mailAiArtifactId', artifact_ids)
        fetch('MailIssueBinding', binding_ids)
        fetch('imap_reconcile_archive', needed)
        for table in TABLES:
            if table.name not in capture['tables']:
                fetch(table.name)
        capture.update(source_contract=contract['tables'], fallback_skew_hours=skew,
                       metadata_rows_scanned=len(metadata),
                       transaction_read_only=conn.execute('SHOW transaction_read_only').fetchone()['transaction_read_only'],
                       transaction_isolation=conn.execute('SHOW transaction_isolation').fetchone()['transaction_isolation'])
    capture.update(status='complete_consistent_source_capture', ended_at=datetime.now(timezone.utc))
    return capture


def import_capture(settings, capture, capture_path, digest):
    day = capture['business_dates'][0]
    scope = capture['day_scopes'][day]
    needed = {row['record_key'] for row in capture['tables']['messages']}
    day_ids = set(scope['day_mail_ids'])
    require(capture['source_read_only'] is True and capture['transaction_read_only'] == 'on', 'CAPTURE_NOT_READ_ONLY')
    require(capture['transaction_isolation'] == 'repeatable read', 'CAPTURE_NOT_REPEATABLE_READ')
    require(not capture['undated_received_mail_ids'], 'UNDETERMINED_RECEIVED_BUSINESS_DATE')
    require(set(capture['tables']) == {table.name for table in TABLES}, 'CAPTURE_TABLE_SET_MISMATCH')
    writer = connection_identity(settings.target_writer_url)
    require(loopback(writer['host']) and writer['port'] == '15433', 'LOCAL_TARGET_MISMATCH')
    static, files, _ = load_static(settings.catalog_path)
    work = ROOT / '.runtime' / 'daily-work' / day
    work.mkdir(parents=True, exist_ok=True)
    with target_connection(settings) as conn:
        conn.isolation_level = psycopg.IsolationLevel.REPEATABLE_READ
        require(conn.execute("SELECT pg_try_advisory_xact_lock(hashtext('complaint-insights:'||%s)) AS ok", (settings.source_id,)).fetchone()['ok'], 'LOCAL_LOCK_UNAVAILABLE')
        before_state = conn.execute('SELECT * FROM sync.sources WHERE source_id=%s FOR UPDATE', (settings.source_id,)).fetchone()
        require(before_state['status'] == 'DEGRADED', 'GLOBAL_STATUS_NOT_DEGRADED')
        current = {str(row['mail_pk']) for row in conn.execute("SELECT mail_pk FROM analysis.mail_fact WHERE source_id=%s AND business_date=%s AND direction='RECEIVED'", (settings.source_id, day))}
        require(current <= day_ids, 'LOCAL_DAY_HAS_ROWS_ABSENT_FROM_PRODUCTION')
        wanted = {}
        for table in TABLES:
            if table.name in ('messages', 'imap_reconcile_archive'):
                wanted[table.name] = set(needed)
            elif table.name == 'attachments':
                wanted[table.name] = {row['record_key'] for row in capture['tables'][table.name]} | local_related_keys(conn, settings.source_id, table, 'message_pk', day_ids)
            elif table.name == 'InboundMail':
                wanted[table.name] = {row['record_key'] for row in capture['tables'][table.name]} | local_related_keys(conn, settings.source_id, table, 'sourcePk', needed)
            elif table.name == 'MailAiArtifact':
                wanted[table.name] = {row['record_key'] for row in capture['tables'][table.name]} | local_related_keys(conn, settings.source_id, table, 'inboundMailId', wanted['InboundMail'])
            elif table.name == 'MailIssueBinding':
                wanted[table.name] = {row['record_key'] for row in capture['tables'][table.name]} | local_related_keys(conn, settings.source_id, table, 'mailAiArtifactId', wanted['MailAiArtifact'])
            else:
                wanted[table.name] = None
        old_by_table = {}
        for table in TABLES:
            query = sql.SQL('SELECT * FROM {} WHERE source_id=%s').format(mirror_relation(table))
            params = [settings.source_id]
            if wanted[table.name] is not None:
                query += sql.SQL(' AND record_key=ANY(%s::text[])')
                params.append(sorted(wanted[table.name]))
            rows = conn.execute(query, params).fetchall()
            old_by_table[table.name] = {row['record_key']: row for row in rows}
        conn.execute('CREATE TEMP TABLE scoped_capture_stage(source_id text,record_key text,payload jsonb,content_hash text) ON COMMIT DROP')
        metrics = {}
        for table in TABLES:
            incoming = {row['record_key']: row for row in capture['tables'][table.name]}
            old = old_by_table[table.name]
            changed = [row for key, row in incoming.items() if key not in old or old[key]['deleted_at'] is not None or old[key]['content_hash'] != row['content_hash']]
            removed = {key for key, row in old.items() if row['deleted_at'] is None and key not in incoming}
            if changed:
                conn.execute('TRUNCATE scoped_capture_stage')
                with conn.cursor().copy('COPY scoped_capture_stage(source_id,record_key,payload,content_hash) FROM STDIN') as stream:
                    for row in changed:
                        stream.write_row((settings.source_id, row['record_key'], Jsonb(row['payload']), row['content_hash']))
                conn.execute(sql.SQL('''INSERT INTO {}(source_id,record_key,payload,content_hash)
                    SELECT source_id,record_key,payload,content_hash FROM scoped_capture_stage
                    ON CONFLICT(source_id,record_key) DO UPDATE SET payload=excluded.payload,content_hash=excluded.content_hash,synced_at=now(),deleted_at=NULL''').format(mirror_relation(table)))
            if removed:
                conn.execute(sql.SQL('UPDATE {} SET deleted_at=now(),synced_at=now() WHERE source_id=%s AND record_key=ANY(%s::text[]) AND deleted_at IS NULL').format(mirror_relation(table)), (settings.source_id, sorted(removed)))
            expression = sql.SQL("md5((payload-'last_fetched_at')::text)") if table.name == 'messages' else sql.SQL('md5(payload::text)')
            actual = conn.execute(sql.SQL('SELECT record_key,content_hash,{} AS actual_hash FROM {} WHERE source_id=%s AND record_key=ANY(%s::text[]) AND deleted_at IS NULL').format(expression, mirror_relation(table)), (settings.source_id, sorted(incoming))).fetchall() if incoming else []
            require({row['record_key']: row['actual_hash'] for row in actual} == {key: row['content_hash'] for key, row in incoming.items()}, 'IMPORT_HASH_MISMATCH:' + table.name)
            metrics[table.name] = {'captured': len(incoming), 'changed': len(changed), 'deleted': len(removed)}
            print(json.dumps({'imported': table.name, **metrics[table.name]}, ensure_ascii=False), flush=True)
        catalog = publish_catalog(conn, settings.source_id, static, files)
        projection = rebuild_projection(conn, settings, catalog, pks=needed)
        require(projection['skew_hours'] == capture['fallback_skew_hours'], 'PROJECTION_SKEW_MISMATCH')
        parity = verify_projection(conn, settings.source_id)
        actual_ids = {str(row['mail_pk']) for row in conn.execute("SELECT mail_pk FROM analysis.mail_fact WHERE source_id=%s AND business_date=%s AND direction='RECEIVED'", (settings.source_id, day))}
        require(actual_ids == day_ids, 'IMPORTED_DAY_SET_MISMATCH')
        attachments = conn.execute('SELECT payload FROM analysis.v_attachments WHERE source_id=%s AND mail_pk=ANY(%s::text[])', (settings.source_id, scope['day_mail_ids'])).fetchall()
        expected = {row['record_key']: row['payload'] for row in capture['tables']['attachments'] if str(row['payload']['message_pk']) in day_ids}
        require({str(row['payload']['id']): row['payload'] for row in attachments} == expected, 'IMPORTED_ATTACHMENT_MISMATCH')
        version = int(before_state['data_version']) + 1
        conn.execute('UPDATE sync.sources SET data_version=%s WHERE source_id=%s', (version, settings.source_id))
        after_state = conn.execute('SELECT * FROM sync.sources WHERE source_id=%s', (settings.source_id,)).fetchone()
        require({key: before_state[key] for key in PRESERVED} == {key: after_state[key] for key in PRESERVED}, 'GLOBAL_CHECKPOINT_CHANGED')
        require(after_state['status'] == 'DEGRADED' and after_state['data_version'] == version, 'GLOBAL_VERSION_MISMATCH')
        proof = {
            'format': 'complaint-closed-day-proof/v1', 'status': 'READY', 'scope': 'closed_business_day',
            'business_date': day, 'source_id': settings.source_id, 'data_version': version,
            'source_snapshot_at': capture['source_snapshot_at'], 'local_import_verified_at': datetime.now(timezone.utc),
            'capture_sha256': digest, 'capture_file': str(capture_path.relative_to(ROOT)),
            'mail_count': len(day_ids), 'attachment_count': len(expected),
            'mail_ids_sha256': sha256('\n'.join(sorted(day_ids, key=int)).encode()).hexdigest(),
            'source_read_only': True, 'persistent_production_read_allowed': False,
            'global_sync_status': after_state, 'global_checkpoints_advanced': False,
            'tables': metrics, 'projection': projection, 'parity': parity,
        }
        changes = sum(item['changed'] + item['deleted'] for item in metrics.values())
        inserted = conn.execute("INSERT INTO sync.runs(source_id,finished_at,status,mode,changed_rows,metrics) VALUES(%s,clock_timestamp(),'SUCCEEDED','SCOPED_DAY_CAPTURE',%s,%s) RETURNING id", (settings.source_id, changes, Jsonb(json.loads(json.dumps(proof, default=str))))).fetchone()
        proof['sync_run_id'] = inserted['id']
    proof['committed_at'] = datetime.now(timezone.utc)
    write_json(work / 'local-import-result.json', proof)
    return proof


def write_source(settings, capture, digest, proof):
    day = capture['business_dates'][0]
    scope = capture['day_scopes'][day]
    work = ROOT / '.runtime' / 'daily-work' / day
    with target_connection(settings, reader=True) as conn:
        require(conn.execute('SHOW transaction_read_only').fetchone()['transaction_read_only'] == 'on', 'LOCAL_READER_NOT_READ_ONLY')
        state = conn.execute('SELECT source_id,data_version,status,source_snapshot_at,last_sync_at,last_aux_at,last_reconcile_at FROM analysis.v_sync_status WHERE source_id=%s', (settings.source_id,)).fetchone()
        require(state['status'] == 'DEGRADED', 'GLOBAL_STATUS_NOT_DEGRADED')
        for name, rows in capture['tables'].items():
            keys = [row['record_key'] for row in rows]
            expression = "md5((payload-'last_fetched_at')::text)" if name == 'messages' else 'md5(payload::text)'
            actual = conn.execute('SELECT record_key,' + expression + ' AS h FROM analysis.v_source_records WHERE source_id=%s AND source_table=%s AND record_key=ANY(%s::text[]) AND deleted_at IS NULL', (settings.source_id, name, keys)).fetchall() if keys else []
            require({row['record_key']: row['h'] for row in actual} == {row['record_key']: row['content_hash'] for row in rows}, 'LOCAL_CAPTURE_HASH_MISMATCH:' + name)
        taxonomy = {row['category_id']: row['name'] for row in conn.execute('SELECT category_id,name FROM analysis.taxonomy WHERE source_id=%s', (settings.source_id,))}
        day_ids = scope['day_mail_ids']
        context_ids = scope['context_mail_ids']
        mails = conn.execute("SELECT * FROM analysis.v_mail_details WHERE source_id=%s AND business_date=%s AND direction='RECEIVED' ORDER BY mail_pk", (settings.source_id, day)).fetchall()
        require({str(row['mail_pk']) for row in mails} == set(day_ids), 'LOCAL_DAY_SET_MISMATCH')
        context = conn.execute('SELECT * FROM analysis.v_mail_details WHERE source_id=%s AND mail_pk=ANY(%s::bigint[]) ORDER BY mail_pk', (settings.source_id, context_ids)).fetchall() if context_ids else []
        require({str(row['mail_pk']) for row in context} == set(context_ids), 'LOCAL_CONTEXT_SET_MISMATCH')
        for row in mails + context:
            row['mail_pk'] = str(row['mail_pk'])
        full_graph, graph = conversation_graph(scope['headers']), conversation_graph(mails + context)
        require(all(graph[key] == full_graph[key] for key in graph), 'LOCAL_CONVERSATION_GRAPH_MISMATCH')
        attachments = conn.execute("SELECT mail_pk,payload FROM analysis.v_attachments WHERE source_id=%s AND mail_pk=ANY(%s::text[]) ORDER BY mail_pk,payload->>'id'", (settings.source_id, day_ids)).fetchall()
        expected = {row['record_key']: row['payload'] for row in capture['tables']['attachments'] if str(row['payload']['message_pk']) in set(day_ids)}
        require({str(row['payload']['id']): row['payload'] for row in attachments} == expected, 'LOCAL_ATTACHMENT_MISMATCH')
    imported = proof['committed_at']
    if not isinstance(imported, datetime):
        imported = datetime.fromisoformat(str(imported).replace('Z', '+00:00'))
    global_state = {key: state[key] for key in state}
    day_state = {
        'source_id': settings.source_id, 'data_version': proof['data_version'], 'status': 'READY',
        'scope': 'closed_business_day', 'business_date': day,
        'source_snapshot_at': capture['source_snapshot_at'], 'last_sync_at': imported,
        'last_aux_at': imported, 'last_reconcile_at': imported,
        'completeness_evidence': 'local-import-result.json', 'global_stream_caught_up': False,
    }
    packet = {
        'format': 'complaint-daily-source/v1', 'business_date': day,
        'timezone': 'Asia/Shanghai', 'direction': 'RECEIVED', 'source_id': settings.source_id,
        'captured_at': datetime.now(timezone.utc), 'status': day_state,
        'global_sync_status': global_state, 'source_capture_sha256': digest,
        'closed_day_proof_sha256': sha256((work / 'local-import-result.json').read_bytes()).hexdigest(),
        'production_read': False, 'origin': 'production_closed_day_capture',
        'mails': mails, 'attachments': attachments, 'conversation_context': context,
        'daily': scope['daily'], 'taxonomy': taxonomy, 'local_mail_count': len(mails),
        'completeness_note': 'This closed day was read from production in one repeatable-read, read-only transaction and then stored locally. READY applies only to this day. Global status and watermarks were not advanced.',
    }
    require_closed_source(packet)
    source_path = work / 'source.json'
    if source_path.exists():
        replaced = work / ('source.json.replaced-' + datetime.now(SHANGHAI).strftime('%Y%m%dT%H%M%S'))
        source_path.replace(replaced)
    write_json(source_path, packet)
    write_json(work / 'state.json', {
        'status': 'awaiting_agent_review', 'business_date': day,
        'source_snapshot_sha256': sha256(source_path.read_bytes()).hexdigest(),
        'mail_count': len(mails), 'attachment_count': len(attachments),
        'context_count': len(context), 'production_capture': True,
        'global_checkpoints_advanced': False,
    })
    return {
        'status': 'fresh_production_capture', 'business_date': day,
        'mails': len(mails), 'attachments': len(attachments), 'context': len(context),
        'data_version': proof['data_version'], 'global_status': state['status'],
        'global_checkpoints_advanced': False, 'persistent_production_read_allowed': False,
        'source_snapshot_sha256': sha256(source_path.read_bytes()).hexdigest(),
    }


def connect_check(settings):
    with source_connection(settings) as conn:
        snapshot = conn.execute('SELECT transaction_timestamp() AS t').fetchone()['t']
        read_only = conn.execute('SHOW transaction_read_only').fetchone()['transaction_read_only']
        isolation = conn.execute('SHOW transaction_isolation').fetchone()['transaction_isolation']
    require(read_only == 'on' and isolation == 'repeatable read', 'SOURCE_SESSION_NOT_READ_ONLY')
    print(json.dumps({'status': 'production_connect_check', 'source_snapshot_at': snapshot.isoformat(), 'read_only': True, 'rows_read': 0}, default=str))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', required=True)
    parser.add_argument('--connect-check', action='store_true')
    args = parser.parse_args()
    load_policy()
    published = ROOT / '.runtime' / 'daily-reports' / args.date / 'report.json'
    if published.is_file() and not args.connect_check:
        print(json.dumps({'status': 'already_published', 'business_date': args.date}, ensure_ascii=False))
        return
    day = parse_day(args.date)
    config_path, before, settings = load_settings()
    runtime = replace(settings, allow_production_read=True)
    try:
        if args.connect_check:
            connect_check(runtime)
            return
        capture = capture_day(runtime, day)
        capture_dir = ROOT / '.runtime' / 'daily-work' / day.isoformat() / 'production-capture'
        capture_dir.mkdir(parents=True, exist_ok=True)
        capture_path = capture_dir / 'source-capture.json'
        write_json(capture_path, capture)
        digest = sha256(capture_path.read_bytes()).hexdigest()
        proof = import_capture(settings, json.loads(capture_path.read_text(encoding='utf-8')), capture_path, digest)
        result = write_source(settings, json.loads(capture_path.read_text(encoding='utf-8')), digest, proof)
        print(json.dumps(result, ensure_ascii=False))
    finally:
        assert_config_unchanged(config_path, before)


if __name__ == '__main__':
    main()
