"""Deterministic daily read model built from a frozen replica and per-mail review."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re

from .attachment_fetcher import atomic_json
from .attachment_preview import prepare_files
from .log_archive import prepare_log_archives
from .config import ROOT

RUNTIME = ROOT / '.runtime/cursor-verification-20261030'
CST = timezone(timedelta(hours=8))
DOMAIN_COLORS = {'进入游戏与更新': '#c8321a', '付费与账号': '#7a4fc9',
                 '玩法与活动': '#1f7f78', '建议与其他': '#8793a1', '信息不足': '#bcc3cd'}


def paragraphs(value):
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return '\n\n'.join(paragraphs(part) for part in value if paragraphs(part))
    if isinstance(value, dict):
        for key in ('text', 'content', 'paragraphs', 'body'):
            if key in value:
                return paragraphs(value[key])
    return ''


class TextHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style'}:
            self.skip += 1
        if tag in {'br', 'p', 'div', 'li', 'tr'}:
            self.output.append('\n')

    def handle_endtag(self, tag):
        if tag in {'script', 'style'}:
            self.skip = max(0, self.skip - 1)

    def handle_data(self, data):
        if not self.skip:
            self.output.append(data)


def original_body(mail):
    text = (mail.get('body_plain_text') or '').strip()
    if not text and mail.get('body_html'):
        parser = TextHTML()
        parser.feed(mail['body_html'])
        text = ''.join(parser.output).strip()
    return text or paragraphs(mail.get('ai_body_original'))


def uid_evidence(review, mail):
    states = {'message_text_supported': 'verified_mail', 'conversation_text_supported': 'verified_thread',
              'multiple_accounts_or_conflict': 'conflict', 'unverified_candidate': 'unverified', 'not_found': 'not_found'}
    if review['state'] not in states:
        raise ValueError('unrecognized UID review state')
    if review['from_address'] != mail['from_address'] or review['delivery_mailbox'] != mail['mailbox']:
        raise ValueError('UID evidence mail identity mismatch')
    state = states[review['state']]
    value = review.get('value') or ''
    # An extraction is evidence of text, never proof of game account ownership.
    # Ambiguous roles and historical conflicts MUST remain unresolved.
    if state in {'conflict', 'unverified', 'not_found'}:
        value = ''
    if value and not review.get('verified'):
        raise ValueError('UID selected without source text support')
    return {'value': value, 'state': state, 'evidence': review.get('evidence') or [],
            'fields': review.get('fields') or [], 'candidates': review.get('candidates') or [],
            'role': review.get('role'), 'history_conflict': review.get('history_conflict'),
            'conversation_links': review.get('conversation_links') or [],
            'verification_meaning': review.get('verification_meaning'), 'provenance': review.get('provenance'),
            'uid_roles': review.get('uid_roles') or [], 'direct_values': review.get('direct_values') or [],
            'conversation_values': review.get('conversation_values') or []}


def received_hour(mail, business_date):
    value = datetime.fromisoformat(str(mail['received_at']).replace('Z', '+00:00'))
    if value.tzinfo is None or value.astimezone(CST).date().isoformat() != business_date:
        raise ValueError('mail timestamp does not belong to the timezone-bound reporting date')
    return value.astimezone(CST).hour


def statistics(daily, business_date):
    by_day = {str(row['business_date']): int(row['count']) for row in daily}
    day = datetime.fromisoformat(business_date).date()
    total = by_day.get(business_date, 0)
    previous = by_day.get(str(day - timedelta(days=1)))
    preceding = [by_day.get(str(day - timedelta(days=i))) for i in range(1, 8)]
    average = sum(preceding) / 7 if all(v is not None for v in preceding) else None
    def growth(baseline):
        return (total - baseline) / baseline * 100 if baseline else None
    return {'total': total, 'previous': previous, 'previous_seven_average': average,
            'growth_previous': growth(previous), 'growth_seven': growth(average), 'daily': by_day}


def group_read_model(records, child_definitions):
    """Apply reviewed semantic definitions; source taxonomy never enters the key."""
    parents, children, domains = {}, {}, {}
    for record in records:
        leaf_id = record['theme_id']
        definition = child_definitions.get(leaf_id)
        if definition is None:
            raise ValueError(f'unreviewed classification leaf: {leaf_id}')
        if not isinstance(definition.get('concrete'), bool):
            raise ValueError('each semantic definition must distinguish concrete and unspecified issues')
        parent_id = record['scope'] + ':' + definition['parent_id']
        domain_name, domain_id = definition['domain_name'], definition['domain_id']
        if domain_name not in DOMAIN_COLORS:
            raise ValueError('unrecognized reviewed business domain')
        candidate = {'id': parent_id, 'name': definition['parent_name'], 'scope': record['scope'],
                     'domain_id': domain_id, 'domain_name': domain_name,
                     'definition': definition['definition'], 'concrete': definition['concrete']}
        parent = parents.setdefault(parent_id, {**candidate, 'count': 0, 'mail_ids': []})
        if any(parent[k] != candidate[k] for k in candidate):
            raise ValueError(f'inconsistent parent grouping definition: {parent_id}')
        parent['count'] += 1
        parent['mail_ids'].append(record['id'])
        child = children.setdefault(leaf_id, {'id': leaf_id, 'name': record['theme_name'],
                                             'parent_id': parent_id, 'scope': record['scope'],
                                             'count': 0, 'mail_ids': []})
        if child['parent_id'] != parent_id:
            raise ValueError('a semantic child cannot map to two parents')
        child['count'] += 1
        child['mail_ids'].append(record['id'])
        domain = domains.setdefault(domain_id, {'id': domain_id, 'name': domain_name,
                                                'color': DOMAIN_COLORS[domain_name], 'count': 0})
        if domain['name'] != domain_name:
            raise ValueError('business domain identity collision')
        domain['count'] += 1
        record.update(subtheme_id=leaf_id, subtheme_name=record['theme_name'], theme_id=parent_id,
                      theme_name=parent['name'], domain_id=domain_id, domain_name=domain_name,
                      concrete=definition['concrete'])
        record['search_text'] = '\n'.join(str(record.get(k) or '') for k in (
            'id', 'from', 'mailbox', 'subject', 'subject_zh', 'summary', 'body', 'body_zh',
            'theme_name', 'subtheme_name')) + '\n' + json.dumps(record['uid'], ensure_ascii=False)
    total = len(records)
    for collection in (parents, children, domains):
        if sum(row['count'] for row in collection.values()) != total:
            raise ValueError('semantic grouping counts do not reconcile')
        for row in collection.values():
            row['share'] = row['count'] / total * 100 if total else 0
    return (sorted(parents.values(), key=lambda row: (-row['count'], row['id'])),
            sorted(children.values(), key=lambda row: (-row['count'], row['id'])),
            sorted(domains.values(), key=lambda row: list(DOMAIN_COLORS).index(row['name'])))


def apply_mail_refinements(records, refinements, *, review_sha256):
    """Apply explicit per-mail decisions, retaining the superseded reasoning."""
    by_id = {row['id']: row for row in records}
    for decision in refinements:
        key = str(decision['mail_pk'])
        record = by_id[key]
        if not decision.get('reviewed') or not decision.get('summary_zh') or not decision.get('basis'):
            raise ValueError('per-mail refinement needs reviewed summary and evidence basis')
        previous = {field: record.get(field) for field in ('summary', 'basis', 'scope', 'theme_id',
                                                          'theme_name', 'subtheme_id', 'subtheme_name')}
        record['metadata']['final_reclassification'] = {'review_sha256': review_sha256,
                                                        'previous': previous, 'decision': decision}
        record['summary'], record['basis'] = decision['summary_zh'], decision['basis']
        if 'body_zh' in decision:
            record['body_zh'] = paragraphs(decision['body_zh'])
            record['body_zh_preview'] = record['body_zh'][:200]
            origin = decision.get('translation_origin') or 'review-agent'
            if origin == 'review-agent-html':
                origin = 'review-agent'
            if origin not in {'source-ai', 'review-agent', 'unavailable'}:
                raise ValueError('unrecognized translation provenance')
            record['translation_origin'] = origin if record['body_zh'] else 'unavailable'
        if decision.get('subject_zh'):
            record['subject_zh'] = decision['subject_zh']
            record['subject_translation_origin'] = 'review-agent'
        if 'secondary_themes' in decision:
            record['secondary_themes'] = decision['secondary_themes'] + decision.get('additional_secondary_suggestions', [])
        if 'main_id' in decision:
            if decision['scope'] not in {'complaint', 'non_complaint', 'unclear'}:
                raise ValueError('unrecognized mail scope in refinement')
            if not isinstance(decision.get('identified'), bool):
                raise ValueError('refinement must explicitly distinguish identified and unidentified')
            if decision['identified'] == (decision['main_id'] == 'unknown'):
                raise ValueError('identification state contradicts the assigned main group')
            record.update(main_id=decision['main_id'], scope=decision['scope'],
                          mail_status=decision['mail_status'], identified=decision['identified'],
                          subtheme_id=decision['specific_issue_id'], subtheme_name=decision['specific_issue_name'],
                          identification_basis=decision.get('issue_identification_basis'),
                          identification_evidence=decision.get('evidence_refs') or [])


def main_read_model(records, main_groups, child_to_main):
    """Summarize operational issue types while retaining each diagnostic subissue."""
    definitions = {row['id']: row for row in main_groups}
    if len(definitions) != len(main_groups):
        raise ValueError('duplicate operational issue group')
    groups, children, domains = {}, {}, {}
    total = len(records)
    for record in records:
        previous_child = record['subtheme_id']
        key = record.get('main_id') or child_to_main.get(previous_child)
        if key not in definitions:
            raise ValueError(f'unreviewed operational issue assignment: {record["id"]}')
        definition = definitions[key]
        domain_id, domain_name = definition['domain_id'], definition['domain_name']
        if domain_name not in DOMAIN_COLORS or not isinstance(definition['eligible_top10'], bool):
            raise ValueError('invalid operational issue definition')
        group_id = 'main:' + key
        group = groups.setdefault(group_id, {'id': group_id, 'name': definition['name'],
            'definition': definition['definition'], 'domain_id': domain_id, 'domain_name': domain_name,
            **({'brief': definition['brief'].strip()} if isinstance(definition.get('brief'), str) and definition['brief'].strip() else {}),
            'scope': 'complaint' if definition['eligible_top10'] else 'unclear' if key == 'unknown' else 'non_complaint',
            'eligible_top10': definition['eligible_top10'], 'concrete': definition['eligible_top10'],
            'count': 0, 'complaint_count': 0, 'mail_ids': [], 'scope_counts': {}})
        group['count'] += 1
        group['complaint_count'] += record['scope'] == 'complaint'
        group['mail_ids'].append(record['id'])
        group['scope_counts'][record['scope']] = group['scope_counts'].get(record['scope'], 0) + 1
        child_id = group_id + ':' + previous_child
        child = children.setdefault(child_id, {'id': child_id, 'name': record['subtheme_name'],
            'parent_id': group_id, 'source_child_id': previous_child,
            'count': 0, 'complaint_count': 0, 'mail_ids': [], 'scope_counts': {}})
        child['count'] += 1
        child['complaint_count'] += record['scope'] == 'complaint'
        child['mail_ids'].append(record['id'])
        child['scope_counts'][record['scope']] = child['scope_counts'].get(record['scope'], 0) + 1
        domain = domains.setdefault(domain_id, {'id': domain_id, 'name': domain_name,
                                                'color': DOMAIN_COLORS[domain_name], 'count': 0})
        domain['count'] += 1
        record['metadata']['diagnostic_group'] = {'id': record['theme_id'], 'name': record['theme_name'],
                                                  'source_child_id': previous_child}
        record.update(main_id=key, theme_id=group_id, theme_name=definition['name'],
                      subtheme_id=child_id, domain_id=domain_id, domain_name=domain_name,
                      identified=key != 'unknown', concrete=definition['eligible_top10'])
        default_status = {'unknown': 'unidentified', 'resolved-followup': 'resolved',
                          'consultation-request': 'inquiry', 'business-notice': 'notice'}.get(key)
        record.setdefault('mail_status', default_status or ('feedback' if record['scope'] == 'complaint' else 'suggestion'))
        record['search_text'] = '\n'.join(str(record.get(k) or '') for k in (
            'id', 'from', 'mailbox', 'subject', 'subject_zh', 'summary', 'body', 'body_zh',
            'theme_name', 'subtheme_name')) + '\n' + json.dumps(record['uid'], ensure_ascii=False)
    for collection in (groups, children, domains):
        if sum(row['count'] for row in collection.values()) != total:
            raise ValueError('operational issue counts do not reconcile')
        for row in collection.values():
            row['share'] = row['count'] / total * 100 if total else 0
    for group in groups.values():
        group['rank_count'] = group['complaint_count'] if group['eligible_top10'] else 0
        group['rank_share'] = group['rank_count'] / total * 100 if total else 0
    return (sorted(groups.values(), key=lambda row: (-row['count'], row['id'])),
            sorted(children.values(), key=lambda row: (-row['count'], row['id'])),
            sorted(domains.values(), key=lambda row: list(DOMAIN_COLORS).index(row['name'])))


def operational_reviews(folder, snapshot_sha256, expected):
    """Load source-bound, independently reviewed decisions before aggregation."""
    main_path = folder / 'main-groups-review.json'
    main_blob = main_path.read_bytes()
    main = json.loads(main_blob)
    baseline_blob = (folder / 'report-before-coarse.json').read_bytes()
    baseline_sha = sha256(baseline_blob).hexdigest()
    baseline = json.loads(baseline_blob)
    if (main['frozen_source_sha256'] != snapshot_sha256 or
            main['source_report_sha256'] != baseline_sha or
            baseline['source_snapshot_sha256'] != snapshot_sha256 or
            {r['id'] for r in baseline['records']} != expected):
        raise ValueError('operational review source identity mismatch')
    assignments = {r['child_id']: r['main_id'] for r in main['records']}
    if len(assignments) != len(main['records']) or set(assignments) != {r['id'] for r in baseline['subthemes']}:
        raise ValueError('operational review does not cover the diagnostic subissues')
    decision_blob = (folder / 'classification-decisions.json').read_bytes()
    decisions = json.loads(decision_blob)
    if (decisions['source_snapshot_sha256'] != snapshot_sha256 or
            decisions['source_report_sha256'] != baseline_sha):
        raise ValueError('per-mail reclassification source identity mismatch')
    for filename, digest in decisions['input_reviews'].items():
        # Review artifacts are fixed local filenames, never customer-supplied paths.
        if Path(filename).name != filename or sha256((folder / filename).read_bytes()).hexdigest() != digest:
            raise ValueError('per-mail reclassification evidence digest mismatch')
    if decisions['input_reviews'].get(main_path.name) != sha256(main_blob).hexdigest():
        raise ValueError('operational mapping is not bound to the per-mail decisions')
    rows = decisions['records']
    keys = [str(r['mail_pk']) for r in rows]
    targeted = {r['id'] for r in baseline['records'] if r['domain_id'] == 'insufficient-info'}
    if len(keys) != len(set(keys)) or set(keys) != targeted:
        raise ValueError('reclassification does not cover the former unclassified population')
    extra = decisions.get('global_corrections') or []
    extra_keys = [str(r['mail_pk']) for r in extra]
    if len(extra_keys) != len(set(extra_keys)) or not set(extra_keys).issubset(expected - targeted):
        raise ValueError('global correction identity mismatch')
    return main, assignments, decisions, sha256(decision_blob).hexdigest()


def build(snapshot_path: Path, review_paths: list[Path], output: Path):
    blob = snapshot_path.read_bytes()
    digest = sha256(blob).hexdigest()
    snapshot = json.loads(blob)
    reviews = {}
    review_sources = []
    for path in review_paths:
        doc = json.loads(path.read_text(encoding='utf-8'))
        bound = doc.get('source_sha256') or doc.get('source_snapshot_sha256')
        if bound != digest:
            raise ValueError(f'review source mismatch: {path.name}')
        review_sources.append({'file': path.name, 'sha256': sha256(path.read_bytes()).hexdigest(), 'reviewer': doc.get('reviewer')})
        for review in doc['records']:
            key = str(review['mail_pk'])
            if key in reviews or review.get('reviewed') is not True or not review.get('summary_zh', '').strip():
                raise ValueError(f'duplicate, incomplete or missing summary: {key}')
            reviews[key] = {**review, 'reviewer': doc.get('reviewer')}
    expected = {str(mail['mail_pk']) for mail in snapshot['mails']}
    if set(reviews) != expected:
        raise ValueError('per-mail review coverage differs from frozen source')
    uid_path = snapshot_path.parent / 'uid-review.json'
    uid_blob = uid_path.read_bytes()
    uid_sha = sha256(uid_blob).hexdigest()
    uid_review = json.loads(uid_blob)
    if uid_review['source_sha256'] != digest:
        raise ValueError('UID evidence belongs to another snapshot')
    context_path = snapshot_path.parent / 'uid-full-context.json'
    if sha256(context_path.read_bytes()).hexdigest() != uid_review['conversation_context_sha256']:
        raise ValueError('UID conversation context digest mismatch')
    if uid_review['data_version'] != snapshot['status']['data_version']:
        raise ValueError('UID evidence data version mismatch')
    supplement = uid_review['supplement']
    if sha256((snapshot_path.parent / 'uid-conversation-text.json').read_bytes()).hexdigest() != supplement['sha256']:
        raise ValueError('UID historical text digest mismatch')
    uid_map = {str(row['mail_pk']): row for row in uid_review['mapping']}
    if set(uid_map) != expected or len(uid_review['mapping']) != len(expected):
        raise ValueError('UID review coverage mismatch')
    overrides_path = snapshot_path.parent / 'theme-review-overrides.json'
    overrides = json.loads(overrides_path.read_text(encoding='utf-8')) if overrides_path.exists() else {}
    if overrides and overrides.get('source_sha256') != digest:
        raise ValueError('theme review belongs to another snapshot')
    for name, bound in overrides.get('input_review_sha256', {}).items():
        if sha256((snapshot_path.parent / f'mail-review-{name}.json').read_bytes()).hexdigest() != bound:
            raise ValueError('refined classification input review digest mismatch')
    override_map = {str(row['mail_pk']): row for row in overrides.get('records', [])}
    if len(override_map) != len(overrides.get('records', [])) or not set(override_map).issubset(expected):
        raise ValueError('duplicate or unknown theme override mail')
    if any(row.get('reviewed') is not True for row in override_map.values()):
        raise ValueError('theme override was not reviewed')
    taxonomy_path = snapshot_path.parent / 'taxonomy.json'
    taxonomy = json.loads(taxonomy_path.read_text(encoding='utf-8')) if taxonomy_path.exists() else {}
    aliases_path = ROOT / 'config/daily-theme-aliases.json'
    aliases = json.loads(aliases_path.read_text(encoding='utf-8')) if aliases_path.exists() else {}
    hierarchy_path = snapshot_path.parent / 'theme-hierarchy-review.json'
    hierarchy_blob = hierarchy_path.read_bytes()
    hierarchy_sha = sha256(hierarchy_blob).hexdigest()
    hierarchy = json.loads(hierarchy_blob)
    if hierarchy['source_sha256'] != digest:
        raise ValueError('semantic hierarchy belongs to another frozen snapshot')
    baseline_path = snapshot_path.parent / 'report-before-hierarchy.json'
    baseline_blob = baseline_path.read_bytes()
    if sha256(baseline_blob).hexdigest() != hierarchy['source_report_sha256']:
        raise ValueError('semantic review input report digest mismatch')
    baseline = json.loads(baseline_blob)
    if baseline['source_snapshot_sha256'] != digest:
        raise ValueError('semantic review input has a different source snapshot')
    baseline_map = {row['id']: row for row in baseline['records']}
    original_definitions = {row['child_id']: row for row in hierarchy['records']}
    if len(original_definitions) != len(hierarchy['records']) or set(original_definitions) != {r['theme_id'] for r in baseline['records']}:
        raise ValueError('semantic review did not cover every original working group')
    definitions = dict(original_definitions)
    for row in hierarchy['additional_children']:
        if row['child_id'] in definitions:
            raise ValueError('duplicate supplemental semantic child')
        definitions[row['child_id']] = row
    final_overrides = {str(row['mail_pk']): row for row in hierarchy['mail_overrides']}
    if len(final_overrides) != len(hierarchy['mail_overrides']) or not set(final_overrides).issubset(expected):
        raise ValueError('duplicate or unknown semantic correction')
    if any(row.get('reviewed') is not True for row in final_overrides.values()):
        raise ValueError('semantic correction lacks per-mail review')
    files = prepare_files(output.parent / 'attachments', snapshot['attachments'], snapshot_sha256=digest)
    files_by_mail = defaultdict(list)
    for entry in files:
        files_by_mail[entry['mail_pk']].append(entry)
    records = []
    for mail in snapshot['mails']:
        key = str(mail['mail_pk'])
        initial_review = reviews[key]
        review = {**initial_review, **override_map.get(key, {})}
        theme_id, theme_name = review['theme_id'], review['theme_name']
        alias = aliases.get(theme_id)
        if alias:
            theme_id, theme_name = alias['id'], alias['name']
        scope = review['scope']
        baseline_group = scope + ':' + theme_id
        previous = baseline_map.get(key)
        if previous is None or previous['theme_id'] != baseline_group or previous['theme_name'] != theme_name:
            raise ValueError(f'original review grouping drift: {key}')
        intermediate_review = review
        final_override = final_overrides.get(key)
        if final_override:
            if final_override['original_child_id'] != baseline_group:
                raise ValueError('semantic correction original mail group mismatch')
            # Corrections follow legacy normalization. Never normalize the new
            # child again: doing so would reintroduce the level/account collision.
            review = {**review, **final_override}
            theme_id, theme_name, scope = review['theme_id'], review['theme_name'], review['scope']
        if scope not in {'complaint', 'non_complaint', 'unclear'}:
            raise ValueError(f'unknown scope: {key}')
        group_id = scope + ':' + theme_id
        source_ai = mail.get('ai_record') or {}
        translated = paragraphs(review.get('body_zh')) or paragraphs(mail.get('body_translated'))
        original = original_body(mail)
        recipient = mail.get('recipients') or []
        to_addresses = [r.get('mail_address') or r.get('address') or '' for r in recipient if isinstance(r, dict)]
        r = {'id': key, 'from': mail['from_address'], 'mailbox': mail['mailbox'], 'to': to_addresses,
             'recipients_original': recipient,
             'cc': mail.get('cc') or [], 'at': mail['received_at'], 'hour': received_hour(mail, snapshot['business_date']),
             'subject': mail.get('subject') or '',
             'subject_zh': review.get('subject_zh') or source_ai.get('subjectZh') or '',
             'subject_translation_origin': 'review-agent' if review.get('subject_zh') else 'source-ai',
             'body': original, 'body_zh': translated, 'body_preview': original[:200], 'body_zh_preview': translated[:200],
             'translation_origin': 'review-agent' if review.get('body_zh') else 'source-ai' if translated else 'unavailable',
             'summary': review['summary_zh'], 'scope': scope, 'theme_id': group_id,
             'theme_name': theme_name, 'basis': review['basis'], 'review_notes': review.get('review_notes') or '',
             'secondary_themes': review.get('secondary_themes') or [], 'uid': uid_evidence(uid_map[key], mail),
             'source_summary': mail.get('summary_zh') or '', 'analysis_state': mail['analysis_state'],
             'original_classification': {'level_one': mail.get('level_one'), 'level_two': mail.get('level_two'),
                 'issue_type_id': mail.get('issue_type_id'), 'category_ai': mail.get('category_ai'),
                 'issue_type_name': taxonomy.get(mail.get('issue_type_id'), ''),
                 'ai_issues': mail.get('ai_issues') or []},
             'metadata': {'source_id': snapshot['source_id'], 'data_version': snapshot['status']['data_version'],
                 'source_mail_pk': key, 'source_body_sha256': sha256(original.encode()).hexdigest(),
                 'reviewer': review.get('reviewer'), 'source_snapshot_sha256': digest,
                 'analysis_version': mail.get('analysis_version'), 'reply_group_key': mail.get('reply_group_key'),
                 'thread_id': mail.get('thread_id'), 'review_theme': {'id': initial_review['theme_id'], 'name': initial_review['theme_name'], 'basis': initial_review['basis']},
                 'refined_theme': {'id': intermediate_review['theme_id'], 'name': intermediate_review['theme_name'], 'basis': intermediate_review['basis']},
                 'final_semantic_theme': {'id': group_id, 'name': theme_name, 'basis': review['basis']},
                 'semantic_hierarchy_sha256': hierarchy_sha, 'semantic_reviewer': hierarchy['reviewer'],
                 'uid_review_sha256': uid_sha,
                 'refined_by': overrides.get('reviewer') if key in override_map else None}, 'files': files_by_mail[key]}
        records.append(r)
    stats = statistics(snapshot['daily'], snapshot['business_date'])
    if stats['total'] != len(records):
        raise ValueError('daily volume does not reconcile with mail population')
    stats['hours'] = [sum(r['hour'] == hour for r in records) for hour in range(24)]
    all_themes, subthemes, domains = group_read_model(records, definitions)
    proposed_counts = Counter(row['scope'] for row in records)
    if dict(proposed_counts) != hierarchy['statistics']['proposed_scope_mail_counts']:
        raise ValueError('applied semantic corrections differ from the reviewed scope counts')
    if {row['id']: row['count'] for row in domains} != hierarchy['statistics']['proposed_domain_mail_counts']:
        raise ValueError('applied semantic corrections differ from the reviewed domain counts')
    main_review, child_to_main, decisions, decisions_sha = operational_reviews(snapshot_path.parent, digest, expected)
    apply_mail_refinements(records, decisions['records'] + decisions.get('global_corrections', []),
                           review_sha256=decisions_sha)
    all_themes, subthemes, domains = main_read_model(records, main_review['main_groups'], child_to_main)
    ranked = sorted((t for t in all_themes if t['rank_count'] > 0), key=lambda t: (-t['rank_count'], t['id']))
    for row in records:
        row['evidence_presence'] = {
            'uid': bool(row['uid']['value']) or row['uid']['state'] == 'conflict' and any(v.get('value') for v in row['uid']['uid_roles']),
            **{kind: any(f['kind'] == kind for f in row['files']) for kind in ('log', 'image', 'document')}}
    log_archives = prepare_log_archives(output.parent / 'archives', output.parent / 'attachments', records, subthemes,
                                        business_date=snapshot['business_date'], source_sha256=digest)
    report = {'business_date': snapshot['business_date'], 'timezone': 'Asia/Shanghai', 'source_id': snapshot['source_id'],
        'data_version': snapshot['status']['data_version'], 'source_snapshot_at': snapshot['status']['source_snapshot_at'],
        'generated_at': datetime.now(timezone.utc).isoformat(), 'production_isolated': True, 'statistics': stats,
        'coverage': {'expected': len(expected), 'reviewed': len(records), 'nonempty_summaries': len(records),
            'body_translations': sum(bool(r['body_zh']) for r in records), 'source_empty_summaries': sum(not r['source_summary'] for r in records),
            'scope_counts': dict(Counter(r['scope'] for r in records)), 'uid_states': dict(Counter(r['uid']['state'] for r in records)),
            'attachments_expected': len(files), 'attachments_ready': sum(f['ready'] for f in files),
            'identified_count': sum(r['identified'] for r in records),
            'unidentified_count': sum(not r['identified'] for r in records),
            'previous_unclassified_count': len(decisions['records']),
            'recovered_count': sum(r['identified'] for r in decisions['records']),
            'mail_status_counts': dict(Counter(r['mail_status'] for r in records))},
        'method': {'count_unit': '邮件封数；同一玩家多封来信分别保留，不代表独立玩家或独立故障',
            'grouping': '根据逐封摘要、正文、真实RFC会话与附件证据归纳业务问题类型；主层按处理能力合并，具体故障和不同阶段保留子类，原系统三级分类只供复查。一封一主类、一次计数。Top10按各主类的客诉相关来信封数排序，含能定位原问题的跟进和补件；纯咨询、已解决、商务及无法定位的残余不入榜。封数不代表新事故或玩家数，不以未确认根因作为无法分类的理由。',
            'translation': '系统译文与本次补译分开标注；部分系统译文仅含新正文，引用内容以原文核验',
            'uid': '结构化UID结合原文核对，缺失时按同采集邮箱的Message-ID / References / In-Reply-To链补充；业务问题组和同发件人本身都不构成会话。多账号角色与历史UID冲突不自动选值，仅证明原文支持，不验证游戏后端账号或持有人身份。',
            'limitation': '此报告仅覆盖生产隔离前的本地快照，当前线上完整性及一小时采集时效未重新核验'},
        'uid_review': {'context_mails': uid_review['context_count'], 'sha256': uid_sha,
                       'rules': uid_review.get('rules') or [], 'limits': uid_review.get('limits') or []},
        'grouping_review': {'sha256': hierarchy_sha, 'reviewer': hierarchy['reviewer'],
                           'method': hierarchy['review_method'], 'limitations': hierarchy['limitations'],
                           'corrected_mails': len(final_overrides), 'operational_review': main_review['reviewer'],
                           'operational_review_sha256': decisions['input_reviews']['main-groups-review.json'],
                           'classification_decisions_sha256': decisions_sha,
                           'input_reviews': decisions['input_reviews'],
                           'reclassification_count': len(decisions['records']),
                           'decision_method': decisions['method']},
        'review_sources': review_sources, 'source_snapshot_sha256': digest, 'themes': all_themes,
        'subthemes': subthemes, 'domains': domains, 'log_archives': log_archives,
        'top_ten': [t['id'] for t in ranked[:10]], 'records': records}
    atomic_json(output, report)
    print(json.dumps({'records': len(records), 'themes': len(all_themes), 'coverage': report['coverage']}, ensure_ascii=True))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path, default=RUNTIME / 'frozen-source.json')
    parser.add_argument('--output', type=Path, default=ROOT / '.runtime/daily-reports/2026-10-29/report.json')
    args = parser.parse_args()
    build(args.snapshot, [args.snapshot.parent / f'mail-review-{part}.json' for part in 'abc'], args.output)


if __name__ == '__main__':
    main()
