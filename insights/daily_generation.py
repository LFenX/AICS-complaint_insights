"""Freeze local data, assemble agent reviews and publish dated read models.

No production connection, LLM call or keyword classification occurs here.
Semantic decisions must be authored against the complete frozen packet.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from datetime import date, datetime, time, timedelta, timezone
from hashlib import file_digest, sha256
import json
import logging
import os
from pathlib import Path
import re
import shutil
import tempfile
from zipfile import ZipFile
import psycopg

from .attachment_fetcher import atomic_json
from .attachment_preview import detected_type, file_kind, prepare_files
from .config import ROOT, Settings
from .daily_report import (CST, main_read_model, original_body, paragraphs,
                           received_hour, statistics, uid_evidence)
from .db import target_connection
from .log_archive import prepare_log_archives, safe_name

REPORTS = ROOT / '.runtime/daily-reports'
WORK = ROOT / '.runtime/daily-work'
# The accepted immutable baseline predates canonical subgroup labels. Its rows
# retain per-mail label aliases; only these exact published bytes get that
# compatibility exception. New or changed reports must use consistent labels.
LEGACY_SUBGROUP_ALIASES_SHA256 = 'b2658daf25058d0ce07ee620d60266039998b5c767ddd0d81721698b3de93760'
# Explicitly reviewed revisions use the original curated-report format and
# preserve every preceding version in report-history. A date or self-declared lineage never grants this
# compatibility; all later generated reports use the normal evidence contract.
CURATED_LEGACY_REPORT_SHA256S = frozenset({
    LEGACY_SUBGROUP_ALIASES_SHA256,
    '7d64a5390f87b8bc374351147918ecbd60b29068a1b08b8a698b43a677cb7a2c',
    '829de9dbfcbf5b68ec88da5dac91b0481a4a8fdbd802b9aa72dd845835314a07',
    'c5150286ccbb1220ffdcc782965b44e656a45d0e9460152ff6d7d06e9d0a086d',
})
LOG = logging.getLogger('insights.daily_generation')
SCOPES = {'complaint', 'non_complaint', 'unclear'}
STATUSES = {'new_issue', 'follow_up', 'materials', 'resolved', 'inquiry', 'unidentified',
            'feedback', 'suggestion', 'notice', 'support_copy'}
NON_COMPLAINT_STATUSES = {'resolved', 'inquiry', 'notice', 'suggestion'}


class GenerationBlocked(ValueError):
    """The packet cannot yet support a complete daily report."""


def require_scope_status(scope, status):
    if scope not in SCOPES or status not in STATUSES:
        raise GenerationBlocked('INVALID_SCOPE_OR_STATUS')
    if status in NON_COMPLAINT_STATUSES and scope != 'non_complaint':
        raise GenerationBlocked('NON_COMPLAINT_STATUS_SCOPE_CONFLICT')


def prepared_preview_name(item):
    if item.get('preview_type') == 'text':
        return item['id'] + '.txt'
    if item.get('preview_type') == 'image':
        return item['id'] + '.jpg'
    if item.get('preview_type') == 'pdf' and item.get('preview_image'):
        return item['id'] + '.pdf.jpg'
    return None


def day_value(value):
    if not isinstance(value, str) or re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', value) is None:
        raise GenerationBlocked('INVALID_BUSINESS_DATE')
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise GenerationBlocked('INVALID_BUSINESS_DATE') from None


def instant(value):
    result = value if isinstance(value, datetime) else datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise GenerationBlocked('NAIVE_SOURCE_WATERMARK')
    return result


def require_closed_source(snapshot):
    day = day_value(snapshot['business_date'])
    if day >= datetime.now(CST).date():
        raise GenerationBlocked('BUSINESS_DAY_NOT_FINISHED')
    end = datetime.combine(day + timedelta(days=1), time(), CST)
    state = snapshot['status']
    if state.get('status') != 'READY' or int(state.get('data_version') or 0) < 1:
        raise GenerationBlocked('LOCAL_REPLICA_NOT_READY')
    # Both the message stream and auxiliary metadata must cover the day end.
    for key in ('source_snapshot_at', 'last_aux_at'):
        if not state.get(key) or instant(state[key]) < end:
            raise GenerationBlocked('SOURCE_BEFORE_DAY_END:' + key)
    if snapshot.get('direction', 'RECEIVED') != 'RECEIVED':
        raise GenerationBlocked('INCORRECT_DIRECTION')


def generation_availability(state, business_date=None):
    """Describe local generation readiness; never grants an HTTP/MCP action."""
    if os.environ.get('INSIGHTS_DAILY_GENERATION_ENABLED', '1') != '1':
        return {'enabled': False, 'disabled_reason': 'DAILY_GENERATION_DISABLED', 'invocation': 'local_os_operator_only'}
    day = business_date or (datetime.now(CST).date() - timedelta(days=1)).isoformat()
    try:
        require_closed_source({'business_date': day, 'status': state or {}, 'direction': 'RECEIVED'})
    except GenerationBlocked as error:
        return {'enabled': False, 'disabled_reason': str(error), 'invocation': 'local_os_operator_only'}
    return {'enabled': True, 'disabled_reason': None, 'invocation': 'local_os_operator_only'}


def json_value(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    raise TypeError(type(value).__name__)


def write_json(path, value):
    # Normalize database temporal values without ever serializing credentials.
    atomic_json(path, json.loads(json.dumps(value, default=json_value, ensure_ascii=False)))


def addresses(row, mailboxes):
    result = {str(row.get('from_address') or '').strip().lower()}
    for value in (row.get('recipients') or []) + (row.get('cc') or []):
        result.add((value if isinstance(value, str) else value.get('mail_address') or value.get('address') or '').strip().lower())
    return result - mailboxes - {''}


def message_ids(value):
    if isinstance(value, list):
        return [key for part in value for key in message_ids(part)]
    return re.findall(r'<[^<>\s]+@[^<>\s]+>', str(value or ''))


def conversation_graph(headers):
    """Only unique Message-ID references, same collection mailbox and participants."""
    rows = {str(row['mail_pk']): row for row in headers}
    if len(rows) != len(headers):
        raise GenerationBlocked('DUPLICATE_CONTEXT_MAIL')
    mailboxes = {str(row['mailbox']).lower() for row in headers}
    lookup = defaultdict(list)
    for key, row in rows.items():
        for mid in set(message_ids(row.get('smtp_message_id'))):
            lookup[(row['mailbox'].lower(), mid)].append(key)
    graph = {key: set() for key in rows}
    for key, row in rows.items():
        refs = message_ids(row.get('in_reply_to')) + message_ids(row.get('references_json'))
        for ref in set(refs):
            candidates = lookup.get((row['mailbox'].lower(), ref), [])
            if len(candidates) == 1:
                parent = candidates[0]
                if parent != key and addresses(row, mailboxes) & addresses(rows[parent], mailboxes):
                    graph[key].add(parent)
                    graph[parent].add(key)
    return graph


def linked_path(graph, start, end):
    queue, seen = deque([(start, [start])]), {start}
    while queue:
        key, path = queue.popleft()
        if key == end:
            return path
        for target in sorted(graph.get(key, ())):
            if target not in seen:
                seen.add(target)
                queue.append((target, path + [target]))
    return []


def export_snapshot(settings, business_date, work):
    """One read-only repeatable-read transaction against the local 15433 reader."""
    day = day_value(business_date)
    if day >= datetime.now(CST).date():
        raise GenerationBlocked('BUSINESS_DAY_NOT_FINISHED')
    with target_connection(settings, reader=True) as conn:
        state = conn.execute('SELECT source_id,data_version,status,source_snapshot_at,last_sync_at,last_aux_at,last_reconcile_at FROM analysis.v_sync_status WHERE source_id=%s', (settings.source_id,)).fetchone()
        if state is None:
            raise GenerationBlocked('LOCAL_SOURCE_NOT_FOUND')
        packet = {'format': 'complaint-daily-source/v1', 'business_date': business_date,
                  'timezone': 'Asia/Shanghai', 'direction': 'RECEIVED', 'source_id': settings.source_id,
                  'captured_at': datetime.now(timezone.utc), 'status': state}
        require_closed_source(packet)
        cursor = conn.execute("SELECT * FROM analysis.v_mail_details WHERE source_id=%s AND business_date=%s AND direction='RECEIVED' ORDER BY mail_pk", (settings.source_id, day))
        mails = []
        while batch := cursor.fetchmany(100):
            mails.extend(batch)
        expected = conn.execute("SELECT count(*) AS n FROM analysis.mail_fact WHERE source_id=%s AND business_date=%s AND direction='RECEIVED'", (settings.source_id, day)).fetchone()['n']
        if len(mails) != expected:
            raise GenerationBlocked('RAW_MAIL_JOIN_COVERAGE_MISMATCH')
        for mail in mails:
            mail['mail_pk'] = str(mail['mail_pk'])
        keys = [row['mail_pk'] for row in mails]
        attachments = conn.execute('SELECT mail_pk,payload FROM analysis.v_attachments WHERE source_id=%s AND mail_pk=ANY(%s::text[]) ORDER BY mail_pk,payload->>\'id\'', (settings.source_id, keys)).fetchall()
        taxonomy = {row['category_id']: row['name'] for row in conn.execute('SELECT category_id,name FROM analysis.taxonomy WHERE source_id=%s', (settings.source_id,))}
        totals = conn.execute("SELECT business_date,sum(mail_count)::bigint AS count FROM analysis.daily_category WHERE source_id=%s AND scope='primary' AND category_depth=1 AND direction='RECEIVED' AND business_date>=%s AND business_date<=%s GROUP BY business_date", (settings.source_id, day-timedelta(days=14), day)).fetchall()
        first = conn.execute("SELECT min(business_date) AS first FROM analysis.mail_fact WHERE source_id=%s AND direction='RECEIVED'", (settings.source_id,)).fetchone()['first']
        by_day = {str(row['business_date']): int(row['count']) for row in totals}
        daily = [{'business_date': str(day-timedelta(days=i)), 'count': by_day.get(str(day-timedelta(days=i)), 0)} for i in range(14, -1, -1) if first is not None and day-timedelta(days=i) >= first]
        if not any(row['business_date'] == business_date for row in daily):
            daily.append({'business_date': business_date, 'count': 0})
        headers = conn.execute('SELECT mail_pk,mailbox,from_address,recipients,cc,smtp_message_id,in_reply_to,references_json FROM analysis.v_mail_details WHERE source_id=%s AND received_at<%s ORDER BY mail_pk', (settings.source_id, datetime.combine(day+timedelta(days=1), time(), CST))).fetchall()
        graph = conversation_graph(headers)
        needed, queue = set(keys), deque(keys)
        while queue:
            for neighbor in graph.get(queue.popleft(), ()):
                if neighbor not in needed:
                    needed.add(neighbor)
                    queue.append(neighbor)
        context_keys = sorted(needed-set(keys), key=int)
        context = conn.execute('SELECT * FROM analysis.v_mail_details WHERE source_id=%s AND mail_pk=ANY(%s::bigint[]) ORDER BY mail_pk', (settings.source_id, context_keys)).fetchall() if context_keys else []
        for row in context:
            row['mail_pk'] = str(row['mail_pk'])
        packet.update(mails=mails, attachments=attachments, daily=daily, taxonomy=taxonomy,
                      conversation_context=context, local_mail_count=expected)
    work.mkdir(parents=True, exist_ok=True)
    source = work / 'source.json'
    if source.exists():
        raise GenerationBlocked('WORKSPACE_ALREADY_FROZEN:use-a-new-work-directory')
    write_json(source, packet)
    digest = sha256(source.read_bytes()).hexdigest()
    write_json(work / 'state.json', {'status': 'awaiting_agent_review', 'business_date': business_date,
        'source_snapshot_sha256': digest, 'mail_count': len(mails), 'attachment_count': len(attachments),
        'context_count': len(context), 'production_read': False})
    return {'status': 'awaiting_agent_review', 'business_date': business_date, 'work': str(work),
            'mail_count': len(mails), 'attachment_count': len(attachments), 'source_snapshot_sha256': digest}


def evidence_text(mail, field):
    if field == 'body':
        return original_body(mail)
    if field == 'subject':
        return mail.get('subject') or ''
    raise GenerationBlocked('UNSUPPORTED_EVIDENCE_FIELD')


def validate_quote(item, sources):
    key = str(item.get('mail_pk') or '')
    if key not in sources:
        raise GenerationBlocked('EVIDENCE_MAIL_NOT_IN_PACKET')
    quote = item.get('quote')
    if not isinstance(quote, str) or not quote.strip() or quote not in evidence_text(sources[key], item.get('field')):
        raise GenerationBlocked('EVIDENCE_QUOTE_NOT_IN_SOURCE')
    return key


def reviewed_uid(review, mail, sources, graph):
    value = review.get('value') or ''
    evidence = review.get('evidence') or []
    current = str(mail['mail_pk'])
    values, paths = set(), []
    for item in evidence:
        key = validate_quote(item, sources)
        candidate = str(item.get('value') or '')
        if not candidate or candidate not in item['quote']:
            raise GenerationBlocked('UID_NOT_IN_QUOTED_TEXT')
        path = linked_path(graph, current, key)
        if not path:
            raise GenerationBlocked('UID_HAS_NO_REAL_CONVERSATION_PATH')
        values.add(candidate)
        if key != current:
            paths.append({'mail_pk': key, 'path': path, 'basis': 'same mailbox + unique RFC references + shared external participant'})
    if review.get('state') in {'message_text_supported', 'conversation_text_supported'}:
        if not value or values != {value} or review.get('verified') is not True:
            raise GenerationBlocked('UID_SINGLE_VALUE_NOT_SUPPORTED')
        direct = any(str(item['mail_pk']) == current for item in evidence)
        if review['state'] == 'message_text_supported' and not direct:
            raise GenerationBlocked('UID_DIRECT_EVIDENCE_MISSING')
        if review['state'] == 'conversation_text_supported' and not paths:
            raise GenerationBlocked('UID_CONVERSATION_EVIDENCE_MISSING')
    elif value:
        raise GenerationBlocked('AMBIGUOUS_UID_MUST_NOT_SELECT_VALUE')
    for role in review.get('uid_roles') or []:
        if str(role.get('value') or '') not in values:
            raise GenerationBlocked('UID_ROLE_NOT_SUPPORTED')
    return uid_evidence({**review, 'conversation_links': paths}, mail)


def attachment_unavailability(directory, binding, snapshot, source_sha256):
    """Validate a local operator's exact, source-bound user decision; never infer one."""
    if binding is None:
        return {}
    if not isinstance(binding, dict) or set(binding) != {'file', 'sha256'} or binding['file'] != 'attachment-exceptions.json':
        raise GenerationBlocked('INVALID_ATTACHMENT_EXCEPTION_BINDING')
    raw = (directory / binding['file']).read_bytes()
    if sha256(raw).hexdigest() != binding['sha256']:
        raise GenerationBlocked('ATTACHMENT_EXCEPTION_DIGEST_MISMATCH')
    authorization = json.loads(raw)
    if (authorization.get('format') != 'complaint-daily-attachment-exceptions/v1'
            or authorization.get('source_snapshot_sha256') != source_sha256
            or authorization.get('business_date') != snapshot['business_date']):
        raise GenerationBlocked('ATTACHMENT_EXCEPTION_SOURCE_MISMATCH')
    decision = authorization.get('decision') or {}
    if (decision.get('outcome') != 'Approved' or decision.get('decided_by') != 'user'
            or any(not isinstance(decision.get(k), str) or not decision[k].strip()
                   for k in ('presented', 'response', 'decided_at', 'source_ref'))):
        raise GenerationBlocked('ATTACHMENT_EXCEPTION_USER_DECISION_MISSING')
    when = datetime.fromisoformat(decision['decided_at'].replace('Z', '+00:00'))
    if when.tzinfo is None or when > datetime.now(timezone.utc):
        raise GenerationBlocked('ATTACHMENT_EXCEPTION_DECISION_TIME_INVALID')
    expected = {str(x['payload']['id']): x['payload'] for x in snapshot['attachments']}
    rows = authorization.get('files')
    if not isinstance(rows, list) or not rows:
        raise GenerationBlocked('ATTACHMENT_EXCEPTION_FILES_MISSING')
    result = {}
    for row in rows:
        key = str(row.get('attachment_id') or '')
        if key not in expected or key in result:
            raise GenerationBlocked('ATTACHMENT_EXCEPTION_ID_MISMATCH')
        original = expected[key]
        identity = {'mail_pk': str(original['message_pk']), 'filename': original.get('filename') or 'attachment',
                    'expected_size': int(original.get('size_bytes') or 0),
                    'source_attachment_id': original.get('attachment_id') or ''}
        if (any(row.get(k) != v for k, v in identity.items())
                or not isinstance(row.get('reason'), str) or not row['reason'].strip()):
            raise GenerationBlocked('ATTACHMENT_EXCEPTION_IDENTITY_MISMATCH')
        result[key] = {'authorization_sha256': binding['sha256'], 'reason': row['reason']}
    return result


def check_attachment_availability(directory, files, allowed, *, annotate=False):
    missing = []
    for item in files:
        if item.get('ready') is True and item.get('status') == 'ready':
            if item.get('availability_exception'):
                raise GenerationBlocked('READY_ATTACHMENT_CANNOT_DECLARE_UNAVAILABLE')
            continue
        failure = 'ATTACHMENTS_NOT_COMPLETE' if annotate else 'REPORT_ATTACHMENTS_NOT_COMPLETE'
        if item.get('ready') is not False or item.get('status') == 'ready':
            raise GenerationBlocked(failure)
        key = item['id']
        if key not in allowed:
            raise GenerationBlocked(failure)
        # An unavailable original is different from existing bytes failing identity/hash checks.
        if (directory / 'attachments' / (key + '.bin')).exists() or item.get('status') == 'ready':
            raise GenerationBlocked('ATTACHMENT_EXCEPTION_CANNOT_MASK_PRESENT_FILE')
        if annotate:
            item['availability_exception'] = allowed[key]
        elif item.get('availability_exception') != allowed[key]:
            raise GenerationBlocked('ATTACHMENT_EXCEPTION_RECORD_MISMATCH')
        missing.append(key)
    return sorted(missing, key=int)


def reviewed_log_packages(directory, review, files):
    """An inspected archive containing logs stays byte-identical and joins log bundles."""
    by_id = {item['id']: item for item in files}
    result = {}
    for row in review.get('log_packages') or []:
        key = str(row.get('attachment_id') or '')
        item = by_id.get(key)
        names = row.get('member_names')
        if (item is None or key in result or item.get('ready') is not True
                or row.get('mail_pk') != item['mail_pk'] or row.get('source_sha256') != item['sha256']
                or Path(item['name']).suffix.lower() not in {'.rar', '.zip', '.7z'}
                or not isinstance(names, list) or not names or any(not isinstance(name, str) or not name for name in names)
                or not any(Path(name).suffix.lower() in {'.log', '.txt', '.clog', '.zst'} for name in names)
                or not isinstance(row.get('basis'), str) or not row['basis'].strip()):
            raise GenerationBlocked('INVALID_LOG_PACKAGE_REVIEW')
        with (directory / 'attachments' / (key + '.bin')).open('rb') as stream:
            signature = stream.read(8)
        signatures = {'.rar': b'Rar!\x1a\x07', '.zip': b'PK\x03\x04', '.7z': b'7z\xbc\xaf\x27\x1c'}
        if not signature.startswith(signatures[Path(item['name']).suffix.lower()]):
            raise GenerationBlocked('LOG_PACKAGE_FORMAT_MISMATCH')
        result[key] = {'source_sha256': row['source_sha256'], 'member_names': names, 'basis': row['basis']}
    return result


def assemble(work):
    source_path, review_path = work / 'source.json', work / 'review.json'
    blob, review_blob = source_path.read_bytes(), review_path.read_bytes()
    snapshot, review = json.loads(blob), json.loads(review_blob)
    digest, review_digest = sha256(blob).hexdigest(), sha256(review_blob).hexdigest()
    require_closed_source(snapshot)
    if review.get('source_snapshot_sha256') != digest or not review.get('reviewer'):
        raise GenerationBlocked('REVIEW_NOT_BOUND_TO_SOURCE')
    mails = snapshot['mails']
    expected = {str(mail['mail_pk']) for mail in mails}
    decisions = {str(row['mail_pk']): row for row in review['records']}
    if len(expected) != len(mails) or len(decisions) != len(review['records']) or set(decisions) != expected:
        raise GenerationBlocked('PER_MAIL_REVIEW_COVERAGE_MISMATCH')
    sources = {str(row['mail_pk']): row for row in mails+snapshot.get('conversation_context', [])}
    graph = conversation_graph(list(sources.values()))
    groups = review['main_groups']
    definitions = {row['id']: row for row in groups}
    if len(definitions) != len(groups):
        raise GenerationBlocked('DUPLICATE_MAIN_GROUP')
    domain_names = {}
    for group in groups:
        if any(not isinstance(group.get(field), str) or not group[field].strip() for field in ('id', 'name', 'definition', 'domain_id', 'domain_name')) or not isinstance(group.get('eligible_top10'), bool):
            raise GenerationBlocked('INVALID_MAIN_GROUP_DEFINITION')
        domain_id, domain_name = group['domain_id'], group['domain_name']
        if domain_id in domain_names and domain_names[domain_id] != domain_name:
            raise GenerationBlocked('DOMAIN_IDENTITY_CONFLICT:' + domain_id)
        domain_names[domain_id] = domain_name
    attachments = work / 'attachments'
    if any(re.fullmatch(r'[0-9]+', str(entry['payload'].get('id', ''))) is None or str(entry['payload'].get('message_pk', '')) not in expected for entry in snapshot['attachments']):
        raise GenerationBlocked('INVALID_ATTACHMENT_SOURCE_ID')
    if not snapshot['attachments'] and not (attachments / 'manifest.json').exists():
        write_json(attachments / 'manifest.json', {'source_snapshot_sha256': digest, 'files': {}})
    files = prepare_files(attachments, snapshot['attachments'], snapshot_sha256=digest,
                          rebuild_previews=True)
    exception_binding = review.get('attachment_exception_authorization')
    allowed = attachment_unavailability(work, exception_binding, snapshot, digest)
    unavailable_ids = check_attachment_availability(work, files, allowed, annotate=True)
    packages = reviewed_log_packages(work, review, files)
    for item in files:
        if item['id'] in packages:
            item.update(kind='log', original_kind='document', log_package=True, kind_review=packages[item['id']])
    for item in files:
        preview = prepared_preview_name(item)
        if preview:
            with (attachments / preview).open('rb') as stream:
                item['preview_sha256'] = file_digest(stream, 'sha256').hexdigest()
    by_mail = defaultdict(list)
    for item in files:
        by_mail[item['mail_pk']].append(item)
    if set(by_mail)-expected or len({item['id'] for item in files}) != len(files):
        raise GenerationBlocked('ATTACHMENT_IDENTITY_MISMATCH')
    records, sub_names = [], {}
    for mail in mails:
        key = str(mail['mail_pk'])
        row = decisions[key]
        if row.get('reviewed') is not True or any(not isinstance(row.get(k), str) or not row[k].strip() for k in ('summary_zh', 'basis', 'sub_id', 'sub_name')):
            raise GenerationBlocked('MISSING_PER_MAIL_SUMMARY_OR_BASIS:' + key)
        if row.get('scope') not in SCOPES or row.get('mail_status') not in STATUSES or row.get('main_id') not in definitions:
            raise GenerationBlocked('INVALID_PER_MAIL_DECISION:' + key)
        require_scope_status(row['scope'], row['mail_status'])
        sub_key = (row['main_id'], row['sub_id'])
        if sub_key in sub_names and sub_names[sub_key] != row['sub_name']:
            raise GenerationBlocked('SUBGROUP_IDENTITY_CONFLICT:' + key)
        sub_names[sub_key] = row['sub_name']
        if row.get('identified') is not (row['main_id'] != 'unknown'):
            raise GenerationBlocked('IDENTIFICATION_CONTRADICTION:' + key)
        if (row['scope'] == 'unclear') != (row['main_id'] == 'unknown'):
            raise GenerationBlocked('UNKNOWN_SCOPE_CONTRADICTION:' + key)
        if row['scope'] == 'complaint' and not definitions[row['main_id']]['eligible_top10']:
            raise GenerationBlocked('NON_ISSUE_CANNOT_ENTER_COMPLAINT_RANK')
        refs = row.get('evidence_refs') or []
        if not refs and row['main_id'] != 'unknown':
            raise GenerationBlocked('MISSING_CLASSIFICATION_EVIDENCE:' + key)
        for ref in refs:
            cited = validate_quote(ref, sources)
            if not linked_path(graph, key, cited):
                raise GenerationBlocked('CLASSIFICATION_EVIDENCE_HAS_NO_REAL_LINK')
        body = original_body(mail)
        translated = paragraphs(row.get('body_zh')) or paragraphs(mail.get('body_translated'))
        subject_zh = row.get('subject_zh') or (mail.get('ai_record') or {}).get('subjectZh') or ''
        record = {'id': key, 'from': mail['from_address'], 'mailbox': mail['mailbox'],
            'to': mail.get('recipients') or [], 'recipients_original': mail.get('recipients') or [], 'cc': mail.get('cc') or [],
            'at': mail['received_at'], 'hour': received_hour(mail, snapshot['business_date']),
            'subject': mail.get('subject') or '', 'subject_zh': subject_zh,
            'subject_translation_origin': 'review-agent' if row.get('subject_zh') else 'source-ai' if subject_zh else 'unavailable',
            'body': body, 'body_zh': translated, 'body_preview': body[:200], 'body_zh_preview': translated[:200],
            'translation_origin': 'review-agent' if row.get('body_zh') else 'source-ai' if translated else 'unavailable',
            'summary': row['summary_zh'], 'basis': row['basis'], 'scope': row['scope'], 'mail_status': row['mail_status'],
            'main_id': row['main_id'], 'identified': row['identified'], 'theme_id': row['sub_id'], 'theme_name': row['sub_name'],
            'subtheme_id': row['sub_id'], 'subtheme_name': row['sub_name'], 'secondary_themes': row.get('secondary_themes') or [],
            'review_notes': row.get('review_notes') or '', 'uid': reviewed_uid(row['uid'], mail, sources, graph),
            'source_summary': mail.get('summary_zh') or '', 'analysis_state': mail.get('analysis_state'),
            'original_classification': {**{k: mail.get(k) for k in ('level_one', 'level_two', 'issue_type_id', 'category_ai', 'ai_issues')}, 'issue_type_name': snapshot.get('taxonomy', {}).get(mail.get('issue_type_id'), '')},
            'metadata': {'source_id': snapshot['source_id'], 'data_version': snapshot['status']['data_version'],
                'source_mail_pk': key, 'source_body_sha256': sha256(body.encode()).hexdigest(), 'source_snapshot_sha256': digest,
                'reviewer': review['reviewer'], 'review_sha256': review_digest, 'evidence_refs': refs, 'decision': row},
            'files': by_mail[key]}
        records.append(record)
    quality = review['quality_review']
    checked = quality.get('reviewed_mail_ids') or []
    if len(checked) != len(expected) or set(checked) != expected:
        raise GenerationBlocked('SEMANTIC_REVIEW_NOT_COMPLETE')
    rechecks = quality.get('unknown_rechecks') or []
    unknown = {row['id'] for row in records if not row['identified']}
    if len(rechecks) != len(unknown) or {str(r['mail_pk']) for r in rechecks} != unknown:
        raise GenerationBlocked('UNKNOWN_MAILS_NOT_RECHECKED')
    for row in rechecks:
        if not row.get('reason') or any(row.get('checked', {}).get(k) is not True for k in ('subject', 'plain_and_html', 'attachments', 'real_conversation')):
            raise GenerationBlocked('UNKNOWN_RECHECK_INCOMPLETE')
    used = {row['main_id'] for row in records}
    checks = quality.get('group_reviews') or []
    if len(checks) != len(used) or {row['main_id'] for row in checks} != used:
        raise GenerationBlocked('GROUP_REVIEW_NOT_COMPLETE')
    for row in checks:
        members = {r['id'] for r in records if r['main_id'] == row['main_id']}
        if len(row.get('mail_ids', [])) != len(members) or set(row['mail_ids']) != members or not row.get('basis') or any(row.get(k) is not True for k in ('coarse_grain_checked', 'same_issue_merged', 'different_issues_separated')):
            raise GenerationBlocked('GROUP_GRANULARITY_NOT_CHECKED')
    editorial = review['editorial']
    if not all(isinstance(editorial.get(k), str) and editorial[k].strip() for k in ('summary', 'attention')) or (records and not editorial.get('evidence_mail_ids')) or not set(editorial.get('evidence_mail_ids', [])).issubset(expected):
        raise GenerationBlocked('EDITORIAL_HAS_NO_EVIDENCE')
    themes, subthemes, domains = main_read_model(records, groups, {})
    stats = statistics(snapshot['daily'], snapshot['business_date'])
    if stats['total'] != len(records):
        raise GenerationBlocked('DAILY_COUNT_MISMATCH')
    day = day_value(snapshot['business_date'])
    stats['daily'] = {str(day-timedelta(days=i)): stats['daily'].get(str(day-timedelta(days=i))) for i in range(14, -1, -1)}
    stats['hours'] = [sum(r['hour'] == hour for r in records) for hour in range(24)]
    for row in records:
        row['evidence_presence'] = {'uid': bool(row['uid']['value']) or row['uid']['state'] == 'conflict' and bool(row['uid']['uid_roles']),
            **{kind: any(f['kind'] == kind for f in row['files']) for kind in ('log', 'image', 'document')}}
    archives = prepare_log_archives(work / 'archives', attachments, records, subthemes, business_date=snapshot['business_date'], source_sha256=digest)
    ranked = sorted((t for t in themes if t['rank_count'] > 0), key=lambda t: (-t['rank_count'], t['id']))
    report = {'business_date': snapshot['business_date'], 'timezone': 'Asia/Shanghai', 'source_id': snapshot['source_id'],
        'data_version': snapshot['status']['data_version'], 'source_snapshot_at': snapshot['status']['source_snapshot_at'],
        'generated_at': datetime.now(timezone.utc).isoformat(), 'production_isolated': True, 'statistics': stats,
        'coverage': {'expected': len(expected), 'reviewed': len(records), 'nonempty_summaries': len(records),
            'body_translations': sum(bool(r['body_zh']) for r in records), 'source_empty_summaries': sum(not r['source_summary'] for r in records),
            'scope_counts': dict(Counter(r['scope'] for r in records)), 'uid_states': dict(Counter(r['uid']['state'] for r in records)),
            'attachments_expected': len(files), 'attachments_ready': sum(f['ready'] for f in files),
            'attachments_unavailable_authorized': len(unavailable_ids),
            'identified_count': len(records)-len(unknown), 'unidentified_count': len(unknown), 'previous_unclassified_count': 0, 'recovered_count': 0,
            'mail_status_counts': dict(Counter(r['mail_status'] for r in records))},
        'method': {'count_unit': '邮件封数；不代表独立玩家或新增事故', 'grouping': '逐封摘要和原文归纳业务主问题，具体差异保留子类；原系统三级分类只作参考。一封一主类；客诉与可定位跟进入榜，咨询、已解决、商务及真正无问题线索另列。',
            'translation': '系统译文与本次补译分别保留来源；HTML-only正文同等参与分析，缺译文明示。',
            'uid': '只接受本封文本或同实际采集邮箱、唯一RFC引用链和参与者交集支持的UID；多账号冲突不选单值，不验证账号持有人。',
            'limitation': '读取保持生产隔离的本地副本，日终水位与全部逐封覆盖已经校验；不宣称当前线上实时一致。'},
        'uid_review': {'context_mails': len(sources), 'sha256': review_digest, 'limits': ['文本证据不代表游戏后台身份验证', '缺少真实引用链时不借用同发件人或同UID历史邮件']},
        'grouping_review': {'reviewer': review['reviewer'], 'sha256': review_digest, 'quality_review': quality},
        'review_sources': [{'file': 'review.json', 'sha256': review_digest, 'reviewer': review['reviewer']}],
        'source_snapshot_sha256': digest, 'editorial': editorial, 'themes': themes, 'subthemes': subthemes,
        'domains': domains, 'log_archives': archives, 'top_ten': [row['id'] for row in ranked[:10]], 'records': records}
    if exception_binding:
        report['attachment_exception_authorization'] = exception_binding
        report['unavailable_attachment_ids'] = unavailable_ids
        report['method']['limitation'] += f' 本次有{len(unavailable_ids)}件原件按明确用户决定保留未取得状态；不提供涉及缺失日志的不完整ZIP。'
    if packages:
        report['log_packages'] = review['log_packages']
    write_json(work / 'report.json', report)
    result = audit_report(work / 'report.json', source_path)
    write_json(work / 'quality.json', {**result, 'review_sha256': review_digest, 'semantic_review': 'agent-authored; not a human approval'})
    return result


def audit_report(path, snapshot_path=None):
    blob = path.read_bytes()
    report_digest = sha256(blob).hexdigest()
    report = json.loads(blob)
    review_path = path.parent / 'review.json'
    if report_digest not in CURATED_LEGACY_REPORT_SHA256S and review_path.is_file():
        review_blob = review_path.read_bytes()
        review = json.loads(review_blob)
        review_digest = sha256(review_blob).hexdigest()
        if (review.get('source_snapshot_sha256') != report['source_snapshot_sha256']
                or review.get('attachment_exception_authorization') != report.get('attachment_exception_authorization')
                or review.get('log_packages', []) != report.get('log_packages', [])
                or report['grouping_review']['sha256'] != review_digest
                or report['uid_review']['sha256'] != review_digest
                or report.get('review_sources') != [{'file': 'review.json', 'sha256': review_digest, 'reviewer': review.get('reviewer')}]
                or any(row.get('metadata', {}).get('review_sha256') != review_digest for row in report['records'])):
            raise GenerationBlocked('REPORT_REVIEW_SOURCE_BINDING_MISMATCH')
    records, coverage, stats = report['records'], report['coverage'], report['statistics']
    for row in records:
        require_scope_status(row['scope'], row['mail_status'])
    keys = {r['id'] for r in records}
    n = len(records)
    if len(keys) != n or coverage['expected'] != n or coverage['reviewed'] != n or coverage['nonempty_summaries'] != n or stats['total'] != n:
        raise GenerationBlocked('REPORT_COVERAGE_MISMATCH')
    if any(not r['summary'].strip() or not r['basis'].strip() or received_hour({'received_at': r['at']}, report['business_date']) != r['hour'] for r in records):
        raise GenerationBlocked('REPORT_PER_MAIL_EVIDENCE_MISSING')
    if stats['hours'] != [sum(r['hour'] == h for r in records) for h in range(24)]:
        raise GenerationBlocked('REPORT_HOURLY_COUNTS_MISMATCH')
    for field, record_field in [('scope_counts', 'scope'), ('uid_states', None), ('mail_status_counts', 'mail_status')]:
        expected_counts = dict(Counter(r[record_field] if record_field else r['uid']['state'] for r in records))
        if coverage[field] != expected_counts:
            raise GenerationBlocked('REPORT_COVERAGE_BREAKDOWN_MISMATCH')
    if coverage['identified_count'] != sum(r['identified'] for r in records) or coverage['unidentified_count'] != sum(not r['identified'] for r in records):
        raise GenerationBlocked('REPORT_IDENTIFIED_COUNTS_MISMATCH')
    for name, field in [('themes', 'theme_id'), ('subthemes', 'subtheme_id'), ('domains', 'domain_id')]:
        rows = report[name]
        if len({row['id'] for row in rows}) != len(rows) or {row['id'] for row in rows} != {r[field] for r in records}:
            raise GenerationBlocked('REPORT_GROUP_IDS_MISMATCH')
        for row in rows:
            members = [r for r in records if r[field] == row['id']]
            label_field = {'themes': 'theme_name', 'subthemes': 'subtheme_name', 'domains': 'domain_name'}[name]
            legacy_aliases = name == 'subthemes' and report_digest in CURATED_LEGACY_REPORT_SHA256S
            if not legacy_aliases and any(member[label_field] != row['name'] for member in members):
                raise GenerationBlocked('REPORT_GROUP_NAME_MISMATCH')
            if name == 'subthemes' and any(member['theme_id'] != row['parent_id'] for member in members):
                raise GenerationBlocked('REPORT_SUBGROUP_PARENT_MISMATCH')
            if name == 'themes' and any(member['domain_id'] != row['domain_id'] or member['domain_name'] != row['domain_name'] for member in members):
                raise GenerationBlocked('REPORT_THEME_DOMAIN_MISMATCH')
            if row['count'] != len(members) or abs(row['share'] - (len(members)/n*100 if n else 0)) > 1e-7:
                raise GenerationBlocked('REPORT_GROUP_COUNTS_MISMATCH')
            if 'mail_ids' in row and (len(row['mail_ids']) != len(members) or set(row['mail_ids']) != {r['id'] for r in members}):
                raise GenerationBlocked('REPORT_GROUP_MEMBERS_MISMATCH')
            if 'complaint_count' in row and row['complaint_count'] != sum(r['scope'] == 'complaint' for r in members):
                raise GenerationBlocked('REPORT_COMPLAINT_COUNT_MISMATCH')
    ranked = sorted((t for t in report['themes'] if t.get('rank_count', 0) > 0), key=lambda t: (-t['rank_count'], t['id']))
    if report['top_ten'] != [row['id'] for row in ranked[:10]]:
        raise GenerationBlocked('REPORT_TOP_TEN_MISMATCH')
    for row in report['themes']:
        rank = row['complaint_count'] if row['eligible_top10'] else 0
        if row['rank_count'] != rank or abs(row['rank_share']-(rank/n*100 if n else 0)) > 1e-7:
            raise GenerationBlocked('REPORT_RANK_DENOMINATOR_MISMATCH')
    files = [f for r in records for f in r['files']]
    if len({f['id'] for f in files}) != len(files) or coverage['attachments_expected'] != len(files) or coverage['attachments_ready'] != sum(f['ready'] for f in files):
        raise GenerationBlocked('REPORT_ATTACHMENT_COVERAGE_MISMATCH')
    exception_binding = report.get('attachment_exception_authorization')
    allowed = {}
    if exception_binding is not None:
        snapshot_path = snapshot_path or path.parent / 'source.json'
        source_raw = snapshot_path.read_bytes()
        source = json.loads(source_raw)
        if sha256(source_raw).hexdigest() != report['source_snapshot_sha256'] or source['business_date'] != report['business_date']:
            raise GenerationBlocked('ATTACHMENT_EXCEPTION_SOURCE_MISMATCH')
        allowed = attachment_unavailability(path.parent, exception_binding, source, report['source_snapshot_sha256'])
    unavailable_ids = check_attachment_availability(path.parent, files, allowed)
    if (coverage.get('attachments_unavailable_authorized', 0) != len(unavailable_ids)
            or report.get('unavailable_attachment_ids', []) != unavailable_ids):
        raise GenerationBlocked('REPORT_UNAVAILABLE_ATTACHMENT_COVERAGE_MISMATCH')
    if report.get('log_packages') and not review_path.is_file():
        raise GenerationBlocked('LOG_PACKAGE_REVIEW_SOURCE_MISSING')
    packages = reviewed_log_packages(path.parent, report, files)
    for item in files:
        if item['id'] in packages:
            if (item['kind'] != 'log' or item.get('original_kind') != 'document'
                    or item.get('log_package') is not True or item.get('kind_review') != packages[item['id']]):
                raise GenerationBlocked('REPORT_LOG_PACKAGE_REVIEW_MISMATCH')
        elif item.get('log_package') or item.get('kind_review'):
            raise GenerationBlocked('REPORT_UNREVIEWED_LOG_PACKAGE')
    for item in files:
        if item['ready']:
            with (path.parent / 'attachments' / (item['id']+'.bin')).open('rb') as stream:
                if file_digest(stream, 'sha256').hexdigest() != item['sha256']:
                    raise GenerationBlocked('REPORT_ATTACHMENT_DIGEST_MISMATCH')
            preview = prepared_preview_name(item)
            if preview:
                preview_path = path.parent / 'attachments' / preview
                if not preview_path.is_file():
                    raise GenerationBlocked('REPORT_PREVIEW_MISSING')
                if report_digest != LEGACY_SUBGROUP_ALIASES_SHA256:
                    with preview_path.open('rb') as stream:
                        if file_digest(stream, 'sha256').hexdigest() != item.get('preview_sha256'):
                            raise GenerationBlocked('REPORT_PREVIEW_DIGEST_MISMATCH')
    for key, item in report['log_archives'].items():
        archive = path.parent / 'archives' / (key+'.zip')
        with archive.open('rb') as stream:
            if file_digest(stream, 'sha256').hexdigest() != item['sha256']:
                raise GenerationBlocked('REPORT_ARCHIVE_DIGEST_MISMATCH')
        with ZipFile(archive) as zipped:
            members = sorted(((r['id'], f) for r in records if r['subtheme_id'] == item['subtheme_id']
                              for f in r['files'] if f['kind'] == 'log'), key=lambda pair: (pair[0], pair[1]['id']))
            sub = next((row for row in report['subthemes'] if row['id'] == item['subtheme_id']), None)
            if sub is None or any(not f['ready'] for _, f in members):
                raise GenerationBlocked('REPORT_ARCHIVE_MEMBERS_MISMATCH')
            entries = [{'mail_pk': owner, 'attachment_id': f['id'], 'filename': f['name'],
                        'size': f['size'], 'sha256': f['sha256'],
                        'entry': f'mail_{owner}/attachment_{f["id"]}_{safe_name(f["name"])}'} for owner, f in members]
            manifest = {'format': 'subissue-original-logs/v1', 'business_date': report['business_date'],
                        'source_snapshot_sha256': report['source_snapshot_sha256'], 'subtheme_id': sub['id'],
                        'subtheme_name': sub['name'], 'file_count': len(entries),
                        'mail_count': len({owner for owner, _ in members}), 'files': entries}
            canonical = json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
            if (zipped.read('_manifest.json') != canonical or sha256(canonical).hexdigest() != key
                    or item.get('id') != key or item.get('file_count') != len(entries)
                    or item.get('mail_count') != manifest['mail_count']
                    or len(zipped.namelist()) != len(entries)+1
                    or set(zipped.namelist()) != {'_manifest.json', *(entry['entry'] for entry in entries)}):
                raise GenerationBlocked('REPORT_ARCHIVE_SOURCE_BINDING_MISMATCH')
            for entry in entries:
                if zipped.getinfo(entry['entry']).file_size != entry['size']:
                    raise GenerationBlocked('REPORT_ARCHIVE_MEMBER_SIZE_MISMATCH')
                if sha256(zipped.read(entry['entry'])).hexdigest() != entry['sha256']:
                    raise GenerationBlocked('REPORT_ARCHIVE_MEMBER_DIGEST_MISMATCH')
    log_readiness = defaultdict(list)
    for row in records:
        for item in row['files']:
            if item['kind'] == 'log':
                log_readiness[row['subtheme_id']].append((row['id'], item['ready']))
    ready_groups = {group for group, flags in log_readiness.items() if all(ready for _, ready in flags)}
    if ready_groups != {item['subtheme_id'] for item in report['log_archives'].values()}:
        raise GenerationBlocked('REPORT_ARCHIVE_GROUP_COVERAGE_MISMATCH')
    archive_by_sub = {item['subtheme_id']: item for item in report['log_archives'].values()}
    if len(archive_by_sub) != len(report['log_archives']):
        raise GenerationBlocked('REPORT_ARCHIVE_GROUP_DUPLICATED')
    for sub in report['subthemes']:
        members = log_readiness.get(sub['id'], [])
        shown = sub.get('log_archive')
        if sub['id'] in ready_groups:
            if shown != archive_by_sub[sub['id']]:
                raise GenerationBlocked('REPORT_SUBGROUP_ARCHIVE_BINDING_MISMATCH')
        elif members:
            if (not isinstance(shown, dict) or shown.get('status') != 'unavailable'
                    or shown.get('file_count') != len(members)
                    or shown.get('mail_count') != len({owner for owner, _ in members})
                    or not shown.get('disabled_reason')):
                raise GenerationBlocked('REPORT_SUBGROUP_UNAVAILABLE_ARCHIVE_MISMATCH')
        elif shown is not None:
            raise GenerationBlocked('REPORT_SUBGROUP_ARCHIVE_WITHOUT_LOGS')
    if snapshot_path:
        raw = snapshot_path.read_bytes()
        snapshot = json.loads(raw)
        sources = {str(row['mail_pk']): row for row in snapshot['mails']}
        if sha256(raw).hexdigest() != report['source_snapshot_sha256'] or set(sources) != keys or snapshot['business_date'] != report['business_date']:
            raise GenerationBlocked('REPORT_SOURCE_BINDING_MISMATCH')
        for row in records:
            if row['body'] != original_body(sources[row['id']]) or row['from'] != sources[row['id']]['from_address'] or row['mailbox'] != sources[row['id']]['mailbox']:
                raise GenerationBlocked('REPORT_SOURCE_TEXT_OR_MAILBOX_MISMATCH')
            original = sources[row['id']]
            if row['subject'] != (original.get('subject') or '') or row.get('recipients_original') != (original.get('recipients') or []) or row.get('cc') != (original.get('cc') or []) or row['at'] != original['received_at']:
                raise GenerationBlocked('REPORT_SOURCE_HEADER_MISMATCH')
        expected_files = {str(item['payload']['id']): str(item['payload']['message_pk']) for item in snapshot['attachments']}
        actual_files = {f['id']: row['id'] for row in records for f in row['files']}
        if len(expected_files) != len(snapshot['attachments']) or expected_files != actual_files:
            raise GenerationBlocked('REPORT_SOURCE_ATTACHMENT_POPULATION_MISMATCH')
        payloads = {str(item['payload']['id']): item['payload'] for item in snapshot['attachments']}
        for item in files:
            original = payloads[item['id']]
            detected = None
            if item['ready']:
                with (path.parent / 'attachments' / (item['id'] + '.bin')).open('rb') as stream:
                    detected = detected_type(stream.read(32))
            kind = 'log' if item['id'] in packages else file_kind(original.get('filename') or '', detected or original.get('content_type') or '')
            if (item['name'] != (original.get('filename') or 'attachment')
                    or item['content_type'] != (original.get('content_type') or 'application/octet-stream')
                    or item['kind'] != kind
                    or int(original.get('size_bytes') or 0) > 0 and item['size'] != int(original['size_bytes'])):
                raise GenerationBlocked('REPORT_SOURCE_ATTACHMENT_METADATA_MISMATCH')
        expected_stats = statistics(snapshot['daily'], report['business_date'])
        for key in ('total', 'previous', 'previous_seven_average', 'growth_previous', 'growth_seven'):
            if stats[key] != expected_stats[key]:
                raise GenerationBlocked('REPORT_SOURCE_STATISTICS_MISMATCH')
    return {'status': 'validated', 'business_date': report['business_date'], 'report_sha256': sha256(blob).hexdigest(),
            'mail_count': n, 'attachment_count': len(files), 'archive_count': len(report['log_archives']),
            'attachments_unavailable_authorized': len(unavailable_ids),
            'semantic_review': 'requires source-bound agent review; structural validation alone is insufficient'}


def audit_published_report(directory):
    """Verify complete evidence before first visibility and publication reuse."""
    try:
        report_path = directory / 'report.json'
        if sha256(report_path.read_bytes()).hexdigest() in CURATED_LEGACY_REPORT_SHA256S:
            return audit_report(report_path)
        for name in ('source.json', 'review.json', 'quality.json', 'attachments/manifest.json'):
            if not (directory / name).is_file():
                raise GenerationBlocked('PUBLISHED_EVIDENCE_MISSING:' + name)
        require_closed_source(json.loads((directory / 'source.json').read_bytes()))
        result = audit_report(report_path, directory / 'source.json')
        report = json.loads(report_path.read_bytes())
        review_digest = sha256((directory / 'review.json').read_bytes()).hexdigest()
        review = json.loads((directory / 'review.json').read_bytes())
        if (review.get('source_snapshot_sha256') != report['source_snapshot_sha256']
                or review.get('attachment_exception_authorization') != report.get('attachment_exception_authorization')):
            raise GenerationBlocked('PUBLISHED_REVIEW_SOURCE_BINDING_MISMATCH')
        quality = json.loads((directory / 'quality.json').read_bytes())
        if quality.get('report_sha256') != result['report_sha256'] or quality.get('review_sha256') != review_digest or report.get('review_sources') != [{'file': 'review.json', 'sha256': review_digest, 'reviewer': report['grouping_review']['reviewer']}]:
            raise GenerationBlocked('PUBLISHED_QUALITY_BINDING_MISMATCH')
        manifest = json.loads((directory / 'attachments/manifest.json').read_bytes())
        files = {item['id']: item for row in report['records'] for item in row['files']}
        if manifest.get('source_snapshot_sha256') != report['source_snapshot_sha256'] or set(manifest.get('files', {})) != set(files):
            raise GenerationBlocked('PUBLISHED_ATTACHMENT_MANIFEST_MISMATCH')
        for key, item in files.items():
            saved = manifest['files'][key]
            if item['ready']:
                if saved.get('status') != 'ready' or saved.get('identity_verified') is not True or saved.get('sha256') != item['sha256']:
                    raise GenerationBlocked('PUBLISHED_ATTACHMENT_MANIFEST_MISMATCH')
            elif saved.get('status') != item['status'] or saved.get('sha256') or saved.get('identity_verified'):
                raise GenerationBlocked('PUBLISHED_UNAVAILABLE_ATTACHMENT_MANIFEST_MISMATCH')
        return result
    except (OSError, KeyError, TypeError, ValueError) as error:
        reason = str(error) if isinstance(error, GenerationBlocked) else type(error).__name__
        raise GenerationBlocked('PUBLISHED_REPORT_NOT_INTACT:' + reason) from None


def publish(work, reports_root=REPORTS):
    source, review = work / 'source.json', work / 'review.json'
    result = audit_published_report(work)
    report = json.loads((work / 'report.json').read_text('utf-8'))
    require_closed_source(json.loads(source.read_text('utf-8')))
    quality = json.loads((work / 'quality.json').read_text('utf-8'))
    if quality.get('report_sha256') != result['report_sha256'] or quality.get('review_sha256') != sha256(review.read_bytes()).hexdigest() or report['review_sources'][0]['sha256'] != quality['review_sha256']:
        raise GenerationBlocked('PUBLICATION_QUALITY_BINDING_MISMATCH')
    day = day_value(report['business_date']).isoformat()
    destination = reports_root / day
    if destination.exists():
        old = destination / 'report.json'
        if old.is_file() and old.read_bytes() == (work / 'report.json').read_bytes():
            return {**audit_published_report(destination), 'status': 'already_published'}
        raise GenerationBlocked('PUBLISHED_DATE_ALREADY_EXISTS:preserve-history')
    reports_root.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.publishing-'+day+'-', dir=reports_root))
    try:
        for name in ('report.json', 'source.json', 'review.json', 'quality.json'):
            shutil.copy2(work / name, staging / name)
        if report.get('attachment_exception_authorization'):
            shutil.copy2(work / 'attachment-exceptions.json', staging / 'attachment-exceptions.json')
        for name in ('attachments', 'archives'):
            if (work / name).is_dir():
                shutil.copytree(work / name, staging / name)
        staged = audit_published_report(staging)
        if staged['report_sha256'] != quality['report_sha256'] or sha256((staging / 'review.json').read_bytes()).hexdigest() != quality['review_sha256']:
            raise GenerationBlocked('PUBLICATION_COPY_DRIFT')
        staging.rename(destination)
    finally:
        # Only the exact private temporary directory created above can be removed.
        if staging.is_dir() and staging.parent.resolve() == reports_root.resolve() and staging.name.startswith('.publishing-'+day+'-'):
            shutil.rmtree(staging)
    write_json(work / 'state.json', {**result, 'status': 'published'})
    return {**result, 'status': 'published'}


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    prepare = sub.add_parser('prepare')
    prepare.add_argument('--date', default='yesterday')
    prepare.add_argument('--config', type=Path, default=ROOT / '.secrets/production.json')
    prepare.add_argument('--work', type=Path)
    for name in ('build', 'publish'):
        sub.add_parser(name).add_argument('--work', type=Path, required=True)
    check = sub.add_parser('check')
    check.add_argument('--report', type=Path, required=True)
    check.add_argument('--snapshot', type=Path)
    args = parser.parse_args()
    work = None
    try:
        if os.environ.get('INSIGHTS_DAILY_GENERATION_ENABLED', '1') != '1':
            raise GenerationBlocked('DAILY_GENERATION_DISABLED')
        if args.command == 'check':
            result = audit_report(args.report, args.snapshot)
        else:
            if args.command == 'prepare':
                day = (datetime.now(CST).date()-timedelta(days=1)).isoformat() if args.date == 'yesterday' else day_value(args.date).isoformat()
                existing = REPORTS / day / 'report.json'
                if existing.is_file():
                    result = {**audit_published_report(existing.parent), 'status': 'already_published'}
                    print(json.dumps(result, ensure_ascii=False)); return
                candidate = (args.work or WORK / day).resolve()
            else:
                candidate = args.work.resolve()
            candidate.relative_to((ROOT / '.runtime').resolve())
            if candidate == (ROOT / '.runtime').resolve() or candidate.is_relative_to(REPORTS.resolve()):
                raise GenerationBlocked('WORK_MUST_NOT_BE_A_PUBLISHED_DIRECTORY')
            work = candidate
            if args.command == 'prepare':
                settings = Settings.load(args.config)
                if (work / 'source.json').is_file():
                    frozen = json.loads((work / 'source.json').read_text('utf-8'))
                    require_closed_source(frozen)
                    if frozen['business_date'] != day or frozen['source_id'] != settings.source_id:
                        raise GenerationBlocked('FROZEN_WORKSPACE_IDENTITY_MISMATCH')
                    policy_path = ROOT / 'scripts' / 'daily-report-unattended-policy.json'
                    fresh_mode = ''
                    if policy_path.is_file():
                        fresh_mode = (json.loads(policy_path.read_text(encoding='utf-8')).get('fresh_data') or {}).get('mode') or ''
                    if fresh_mode == 'always_production_closed_day' and frozen.get('origin') != 'production_closed_day_capture':
                        raise GenerationBlocked('LOCAL_FREEZE_DISABLED')
                    result = {'status': 'awaiting_agent_review', 'business_date': day, 'work': str(work),
                        'mail_count': len(frozen['mails']), 'source_snapshot_sha256': sha256((work / 'source.json').read_bytes()).hexdigest(), 'resumed': True}
                else:
                    policy_path = ROOT / 'scripts' / 'daily-report-unattended-policy.json'
                    fresh_mode = ''
                    if policy_path.is_file():
                        fresh_mode = (json.loads(policy_path.read_text(encoding='utf-8')).get('fresh_data') or {}).get('mode') or ''
                    if fresh_mode == 'always_production_closed_day':
                        raise GenerationBlocked('LOCAL_FREEZE_DISABLED')
                    result = export_snapshot(settings, day, work)
            elif args.command == 'build':
                result = assemble(work)
            else:
                result = publish(work)
        LOG.info(json.dumps({'action': 'daily-report.'+args.command, 'business_date': result['business_date'], 'status': result['status']}))
        print(json.dumps(result, ensure_ascii=False))
    except (GenerationBlocked, OSError, KeyError, TypeError, ValueError, psycopg.Error) as error:
        reason = str(error) if isinstance(error, GenerationBlocked) else type(error).__name__
        if work is not None:
            # No secret, mail text or database exception string in the run status.
            write_json(work / 'last-failure.json', {'status': 'blocked', 'reason': reason, 'at': datetime.now(timezone.utc).isoformat()})
        print(json.dumps({'status': 'blocked', 'reason': reason}, ensure_ascii=False))
        raise SystemExit(2) from None


if __name__ == '__main__':
    main()
