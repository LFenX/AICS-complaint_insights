"""Freeze one closed day from the local replica when its watermarks already cover day end.

Does not connect to production, does not change global status, and does not advance watermarks.
"""
from __future__ import annotations

import argparse
from collections import deque
from datetime import datetime, time, timedelta, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from insights.config import Settings
from insights.daily_generation import conversation_graph, require_closed_source, write_json
from insights.db import target_connection
from insights.time_rules import SHANGHAI


def instant(value):
    result = value if isinstance(value, datetime) else datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise RuntimeError('NAIVE_SOURCE_WATERMARK')
    return result


def freeze(business_date: str):
    day = datetime.fromisoformat(business_date).date()
    if day >= datetime.now(SHANGHAI).date():
        raise SystemExit('BUSINESS_DAY_NOT_FINISHED')
    work = ROOT / '.runtime' / 'daily-work' / business_date
    source_path = work / 'source.json'
    published = ROOT / '.runtime' / 'daily-reports' / business_date / 'report.json'
    if published.exists():
        print(json.dumps({'status': 'already_published', 'business_date': business_date}, ensure_ascii=False))
        return
    policy_path = ROOT / 'scripts' / 'daily-report-unattended-policy.json'
    fresh_mode = ''
    if policy_path.is_file():
        fresh_mode = (json.loads(policy_path.read_text(encoding='utf-8')).get('fresh_data') or {}).get('mode') or ''
    if fresh_mode == 'always_production_closed_day':
        raise SystemExit('LOCAL_FREEZE_DISABLED')
    if source_path.exists():
        print(json.dumps({'status': 'already_frozen', 'business_date': business_date}, ensure_ascii=False))
        return
    settings = Settings.load(ROOT / '.secrets' / 'production.json')
    if settings.allow_production_read:
        raise SystemExit('PERSISTENT_ISOLATION_REQUIRED')
    end = datetime.combine(day + timedelta(days=1), time(), SHANGHAI)
    with target_connection(settings, reader=True) as conn:
        state = conn.execute(
            'SELECT source_id,data_version,status,source_snapshot_at,last_sync_at,last_aux_at,last_reconcile_at '
            'FROM analysis.v_sync_status WHERE source_id=%s', (settings.source_id,)).fetchone()
        if state is None:
            raise SystemExit('LOCAL_SOURCE_NOT_FOUND')
        for key in ('source_snapshot_at', 'last_aux_at'):
            if not state.get(key) or instant(state[key]) < end:
                raise SystemExit('SOURCE_BEFORE_DAY_END:' + key)
        day_state = dict(state)
        day_state.update({
            'status': 'READY',
            'scope': 'closed_business_day',
            'business_date': business_date,
            'global_stream_caught_up': state['status'] == 'READY',
            'completeness_evidence': 'local watermarks already cover this day end',
        })
        packet = {
            'format': 'complaint-daily-source/v1', 'business_date': business_date,
            'timezone': 'Asia/Shanghai', 'direction': 'RECEIVED', 'source_id': settings.source_id,
            'captured_at': datetime.now(timezone.utc), 'status': day_state,
            'global_sync_status': dict(state), 'production_read': False,
            'completeness_note': 'This closed day is frozen from the local replica because its stored watermarks already cover day end. Global status and watermarks are not changed.',
        }
        require_closed_source(packet)
        cursor = conn.execute(
            "SELECT * FROM analysis.v_mail_details WHERE source_id=%s AND business_date=%s AND direction='RECEIVED' ORDER BY mail_pk",
            (settings.source_id, day))
        mails = []
        while batch := cursor.fetchmany(100):
            mails.extend(batch)
        expected = conn.execute(
            "SELECT count(*) AS n FROM analysis.mail_fact WHERE source_id=%s AND business_date=%s AND direction='RECEIVED'",
            (settings.source_id, day)).fetchone()['n']
        if len(mails) != expected:
            raise SystemExit('RAW_MAIL_JOIN_COVERAGE_MISMATCH')
        for mail in mails:
            mail['mail_pk'] = str(mail['mail_pk'])
        keys = [row['mail_pk'] for row in mails]
        attachments = conn.execute(
            "SELECT mail_pk,payload FROM analysis.v_attachments WHERE source_id=%s AND mail_pk=ANY(%s::text[]) ORDER BY mail_pk,payload->>'id'",
            (settings.source_id, keys)).fetchall() if keys else []
        taxonomy = {row['category_id']: row['name'] for row in conn.execute(
            'SELECT category_id,name FROM analysis.taxonomy WHERE source_id=%s', (settings.source_id,))}
        totals = conn.execute(
            "SELECT business_date,sum(mail_count)::bigint AS count FROM analysis.daily_category "
            "WHERE source_id=%s AND scope='primary' AND category_depth=1 AND direction='RECEIVED' "
            "AND business_date>=%s AND business_date<=%s GROUP BY business_date",
            (settings.source_id, day - timedelta(days=14), day)).fetchall()
        first = conn.execute(
            "SELECT min(business_date) AS first FROM analysis.mail_fact WHERE source_id=%s AND direction='RECEIVED'",
            (settings.source_id,)).fetchone()['first']
        by_day = {str(row['business_date']): int(row['count']) for row in totals}
        daily = [{'business_date': str(day - timedelta(days=i)), 'count': by_day.get(str(day - timedelta(days=i)), 0)}
                 for i in range(14, -1, -1) if first is not None and day - timedelta(days=i) >= first]
        headers = conn.execute(
            'SELECT mail_pk,mailbox,from_address,recipients,cc,smtp_message_id,in_reply_to,references_json '
            'FROM analysis.v_mail_details WHERE source_id=%s AND received_at<%s ORDER BY mail_pk',
            (settings.source_id, end)).fetchall()
        graph = conversation_graph(headers)
        needed, queue = set(keys), deque(keys)
        while queue:
            for neighbor in graph.get(queue.popleft(), ()):
                if neighbor not in needed:
                    needed.add(neighbor)
                    queue.append(neighbor)
        context_keys = sorted(needed - set(keys), key=int)
        context = conn.execute(
            'SELECT * FROM analysis.v_mail_details WHERE source_id=%s AND mail_pk=ANY(%s::bigint[]) ORDER BY mail_pk',
            (settings.source_id, context_keys)).fetchall() if context_keys else []
        for row in context:
            row['mail_pk'] = str(row['mail_pk'])
        packet.update(mails=mails, attachments=attachments, daily=daily, taxonomy=taxonomy,
                      conversation_context=context, local_mail_count=int(expected))
    work.mkdir(parents=True, exist_ok=True)
    write_json(source_path, packet)
    print(json.dumps({
        'status': 'frozen_from_local_replica', 'business_date': business_date,
        'mail_count': len(packet['mails']), 'attachment_count': len(packet['attachments']),
        'context_count': len(packet['conversation_context']), 'global_status': state['status'],
        'production_read': False,
    }, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', required=True)
    freeze(parser.parse_args().date)
