"""Actual synthetic packets exercise evidence, completeness and atomic publication."""
from copy import deepcopy
from datetime import datetime, timedelta
from hashlib import sha256
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from contextlib import redirect_stdout
from io import BytesIO, StringIO
from PIL import Image

from insights.daily_generation import (GenerationBlocked, assemble, audit_report,
                                      conversation_graph, linked_path, publish, require_closed_source, write_json)


class DailyGenerationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name) / 'work'
        self.work.mkdir()
        self.source = {'business_date': '2026-10-28', 'source_id': 'synthetic-only', 'direction': 'RECEIVED',
            'status': {'status': 'READY', 'data_version': 1, 'source_snapshot_at': '2026-10-29T00:20:00+08:00', 'last_aux_at': '2026-10-29T00:20:00+08:00'},
            'daily': [{'business_date': f'2026-10-{day:02}', 'count': 2} for day in range(14, 29)],
            'mails': [{'mail_pk': '1', 'from_address': 'player@example.test', 'mailbox': 'support@example.test',
                'recipients': [{'address': 'support@example.test'}], 'cc': [], 'received_at': '2026-10-28T15:20:00+08:00',
                'subject': 'Game does not start', 'body_plain_text': 'UID 12345678. Black screen after update.', 'smtp_message_id': '<one@example.test>'},
                {'mail_pk': '2', 'from_address': 'player@example.test', 'mailbox': 'support@example.test',
                'recipients': [], 'cc': [], 'received_at': '2026-10-28T18:10:00+08:00', 'subject': 'Re: Game does not start',
                'body_plain_text': '', 'body_html': '<p>Still a black screen.</p>', 'smtp_message_id': '<two@example.test>', 'in_reply_to': '<one@example.test>'}],
            'attachments': [], 'conversation_context': [], 'taxonomy': {}}
        group = {'id': 'update-launch', 'name': '更新安装与启动阻断', 'definition': '客户端进入前阻断，保留具体阶段', 'domain_id': 'entry-update', 'domain_name': '进入游戏与更新', 'eligible_top10': True}
        records = []
        for key, state in [('1', 'message_text_supported'), ('2', 'conversation_text_supported')]:
            records.append({'mail_pk': key, 'reviewed': True, 'summary_zh': '更新后启动黑屏，无法进入游戏' if key == '1' else '跟进启动黑屏仍未恢复',
                'basis': '原文明确描述进入前黑屏', 'scope': 'complaint', 'mail_status': 'new_issue' if key == '1' else 'follow_up',
                'main_id': 'update-launch', 'sub_id': 'entry-black-screen', 'sub_name': '启动黑屏', 'identified': True,
                'evidence_refs': [{'mail_pk': key, 'field': 'body', 'quote': 'Black screen after update.' if key == '1' else 'Still a black screen.'}],
                'uid': {'state': state, 'value': '12345678', 'verified': True, 'from_address': 'player@example.test', 'delivery_mailbox': 'support@example.test',
                    'evidence': [{'mail_pk': '1', 'field': 'body', 'quote': 'UID 12345678.', 'value': '12345678'}]}})
        self.review = {'reviewer': 'synthetic-fixture', 'main_groups': [group], 'records': records,
            'quality_review': {'reviewed_mail_ids': ['1', '2'], 'unknown_rechecks': [], 'group_reviews': [{'main_id': group['id'], 'mail_ids': ['1', '2'],
                'coarse_grain_checked': True, 'same_issue_merged': True, 'different_issues_separated': True, 'basis': '两封都是启动前黑屏，第二封是可定位跟进'}]},
            'editorial': {'summary': '两封来信聚焦更新后的启动黑屏，其中一封为未解决跟进。', 'attention': '按更新版本与启动阶段核对复现，不据此认定根因。', 'evidence_mail_ids': ['1', '2']}}
        self.save()

    def save(self):
        write_json(self.work / 'source.json', self.source)
        self.review['source_snapshot_sha256'] = sha256((self.work / 'source.json').read_bytes()).hexdigest()
        write_json(self.work / 'review.json', self.review)

    def test_complete_review_builds_same_template_and_publishes_idempotently(self):
        result = assemble(self.work)
        self.assertEqual(result['mail_count'], 2)
        report = json.loads((self.work / 'report.json').read_text('utf-8'))
        self.assertEqual(report['statistics']['hours'][15], 1)
        self.assertEqual(report['records'][1]['uid']['state'], 'verified_thread')
        self.assertEqual(report['records'][1]['body'], 'Still a black screen.')
        self.assertEqual(report['themes'][0]['rank_count'], 2)
        self.assertEqual(report['top_ten'], ['main:update-launch'])
        root = Path(self.temp.name) / 'published'
        self.assertEqual(publish(self.work, root)['status'], 'published')
        self.assertEqual(publish(self.work, root)['status'], 'already_published')
        old = (root / '2026-10-28/report.json').read_bytes()
        report['editorial']['attention'] = 'changed'
        write_json(self.work / 'report.json', report)
        with self.assertRaises(GenerationBlocked):
            publish(self.work, root)
        self.assertEqual((root / '2026-10-28/report.json').read_bytes(), old)

    def test_old_watermark_or_auxiliary_state_blocks_full_day(self):
        for key in ['source_snapshot_at', 'last_aux_at']:
            snapshot = deepcopy(self.source)
            snapshot['status'][key] = '2026-10-28T23:59:59+08:00'
            with self.subTest(key=key), self.assertRaises(GenerationBlocked):
                require_closed_source(snapshot)

    def test_missing_duplicate_unreviewed_or_empty_summary_cannot_build(self):
        for mutation in ['missing', 'duplicate', 'unreviewed', 'summary', 'basis', 'source_binding']:
            draft = deepcopy(self.review)
            if mutation == 'missing': draft['records'].pop()
            if mutation == 'duplicate': draft['records'].append(draft['records'][0])
            if mutation == 'unreviewed': draft['records'][0]['reviewed'] = False
            if mutation in {'summary', 'basis'}: draft['records'][0]['summary_zh' if mutation == 'summary' else 'basis'] = ''
            if mutation == 'source_binding': draft['source_snapshot_sha256'] = 'wrong'
            write_json(self.work / 'review.json', draft)
            with self.subTest(mutation=mutation), self.assertRaises(GenerationBlocked):
                assemble(self.work)

    def test_same_sender_thread_id_or_uid_cannot_replace_rfc_evidence(self):
        self.source['mails'][1].pop('in_reply_to')
        for row in self.source['mails']: row['thread_id'] = 'same-old-business-group'
        self.save()
        graph = conversation_graph(self.source['mails'])
        self.assertEqual(linked_path(graph, '1', '2'), [])
        with self.assertRaisesRegex(GenerationBlocked, 'UID_HAS_NO_REAL_CONVERSATION_PATH'):
            assemble(self.work)

    def test_wrong_participant_or_mailbox_cannot_share_uid(self):
        for field in ['mailbox', 'from_address']:
            source = deepcopy(self.source)
            source['mails'][1][field] = 'unrelated@example.test'
            self.assertEqual(linked_path(conversation_graph(source['mails']), '1', '2'), [])

    def test_uid_quote_and_multivalue_decisions_are_not_trusted(self):
        for mode in ['invented_quote', 'conflict_selection']:
            draft = deepcopy(self.review)
            if mode == 'invented_quote': draft['records'][0]['uid']['evidence'][0]['quote'] = 'UID 99999999'
            else: draft['records'][0]['uid']['state'] = 'multiple_accounts_or_conflict'
            write_json(self.work / 'review.json', draft)
            with self.subTest(mode=mode), self.assertRaises(GenerationBlocked):
                assemble(self.work)

    def test_quality_review_must_cover_every_mail_and_group(self):
        for mode in ['mail', 'group', 'granularity', 'editorial']:
            draft = deepcopy(self.review)
            if mode == 'mail': draft['quality_review']['reviewed_mail_ids'] = ['1']
            if mode == 'group': draft['quality_review']['group_reviews'] = []
            if mode == 'granularity': draft['quality_review']['group_reviews'][0]['same_issue_merged'] = False
            if mode == 'editorial': draft['editorial']['evidence_mail_ids'] = ['not-in-packet']
            write_json(self.work / 'review.json', draft)
            with self.subTest(mode=mode), self.assertRaises(GenerationBlocked):
                assemble(self.work)

    def test_report_rank_and_evidence_tampering_are_detected(self):
        assemble(self.work)
        value = json.loads((self.work / 'report.json').read_text('utf-8'))
        value['themes'][0]['rank_count'] = 20
        write_json(self.work / 'report.json', value)
        with self.assertRaises(GenerationBlocked):
            audit_report(self.work / 'report.json', self.work / 'source.json')

    def test_subgroup_identity_conflicts_block_instead_of_merging_different_labels(self):
        self.review['records'][1]['sub_name'] = '登录授权错误'
        self.save()
        with self.assertRaisesRegex(GenerationBlocked, 'SUBGROUP_IDENTITY_CONFLICT'):
            assemble(self.work)
        self.review['records'][1]['sub_id'] = 'login-authorization'
        self.save()
        assemble(self.work)
        report = json.loads((self.work / 'report.json').read_text('utf-8'))
        self.assertEqual(len(report['subthemes']), 2)
        self.assertEqual({row['name'] for row in report['subthemes']}, {'启动黑屏', '登录授权错误'})
        self.assertEqual(publish(self.work, self.work.parent/'isolated-published')['status'], 'published')

    def test_domain_identity_conflicts_block_and_distinct_domains_remain_navigable(self):
        group = deepcopy(self.review['main_groups'][0])
        group.update(id='account-login', name='账号登录授权', domain_name='付费与账号')
        self.review['main_groups'].append(group)
        self.review['records'][1]['main_id'] = group['id']
        check = deepcopy(self.review['quality_review']['group_reviews'][0])
        self.review['quality_review']['group_reviews'][0]['mail_ids'] = ['1']
        check.update(main_id=group['id'], mail_ids=['2'])
        self.review['quality_review']['group_reviews'].append(check)
        self.save()
        with self.assertRaisesRegex(GenerationBlocked, 'DOMAIN_IDENTITY_CONFLICT'):
            assemble(self.work)
        group['domain_id'] = 'payment-account'
        self.save()
        assemble(self.work)
        report = json.loads((self.work / 'report.json').read_text('utf-8'))
        self.assertEqual({row['name'] for row in report['domains']}, {'进入游戏与更新', '付费与账号'})
        self.assertEqual(publish(self.work, self.work.parent/'isolated-published')['status'], 'published')

    def test_report_navigation_label_and_parent_tampering_are_detected(self):
        assemble(self.work)
        original = json.loads((self.work / 'report.json').read_text('utf-8'))
        for collection in ['themes', 'subthemes', 'domains']:
            value = deepcopy(original)
            value[collection][0]['name'] = '无关的显示名称'
            write_json(self.work / 'report.json', value)
            with self.subTest(collection=collection), self.assertRaisesRegex(GenerationBlocked, 'REPORT_GROUP_NAME_MISMATCH'):
                audit_report(self.work / 'report.json', self.work / 'source.json')
        value = deepcopy(original)
        value['subthemes'][0]['parent_id'] = 'wrong-parent'
        write_json(self.work / 'report.json', value)
        with self.assertRaisesRegex(GenerationBlocked, 'REPORT_SUBGROUP_PARENT_MISMATCH'):
            audit_report(self.work / 'report.json', self.work / 'source.json')

    def test_zero_mail_day_is_valid_only_with_closed_source_and_complete_empty_review(self):
        self.source['mails'] = []
        self.source['daily'][-1]['count'] = 0
        self.review.update(records=[], main_groups=[])
        self.review['quality_review'].update(reviewed_mail_ids=[], group_reviews=[])
        self.review['editorial'].update(evidence_mail_ids=[], summary='当日完整副本未收到来信。', attention='无当日问题需要定位。')
        self.save()
        self.assertEqual(assemble(self.work)['mail_count'], 0)

    def test_capability_reports_actual_generation_flag_and_closed_local_day(self):
        from insights.api import create_app
        from insights.config import Settings
        from insights.daily_report import CST
        today = datetime.now(CST).date()
        state = {'status': 'READY', 'data_version': 1, 'source_snapshot_at': today.isoformat()+'T00:10:00+08:00', 'last_aux_at': today.isoformat()+'T00:10:00+08:00'}
        settings = Settings(source_id='synthetic-only', source_url='postgresql://reader:fake@127.0.0.1:55432/source', target_owner_url='postgresql://owner:fake@127.0.0.1:15433/complaint_insights_test', target_writer_url='postgresql://writer:fake@127.0.0.1:15433/complaint_insights_test', target_reader_url='postgresql://reader:fake@127.0.0.1:15433/complaint_insights_test', api_token='synthetic-token-that-is-long-enough-only')
        app = create_app(settings)
        endpoint = next(route.endpoint for route in app.routes if route.path == '/v1/capabilities')
        conn = MagicMock()
        conn.execute.return_value.fetchone.return_value = state
        with patch.dict('os.environ', {'INSIGHTS_DAILY_GENERATION_ENABLED': '0'}):
            result = endpoint(conn)['capabilities']['daily_generation']
            self.assertFalse(result['enabled'])
            self.assertEqual(result['disabled_reason'], 'DAILY_GENERATION_DISABLED')
        with patch.dict('os.environ', {'INSIGHTS_DAILY_GENERATION_ENABLED': '1'}):
            self.assertTrue(endpoint(conn)['capabilities']['daily_generation']['enabled'])
            self.assertEqual(endpoint(conn)['capabilities']['daily_generation']['invocation'], 'local_os_operator_only')
            state['status'] = 'DEGRADED'
            self.assertEqual(endpoint(conn)['capabilities']['daily_generation']['disabled_reason'], 'LOCAL_REPLICA_NOT_READY')
            state['status'] = 'READY'
            state['last_aux_at'] = (today-timedelta(days=1)).isoformat()+'T23:59:59+08:00'
            self.assertEqual(endpoint(conn)['capabilities']['daily_generation']['disabled_reason'], 'SOURCE_BEFORE_DAY_END:last_aux_at')
        self.assertFalse(any('POST' in (getattr(route, 'methods', set()) or set()) and 'generation' in route.path for route in app.routes))

    def test_explicit_non_complaint_statuses_cannot_be_counted_as_complaints(self):
        for status in ['resolved', 'inquiry', 'notice', 'suggestion']:
            for row in self.review['records']:
                row.update(mail_status=status, scope='complaint')
            self.save()
            with self.subTest(status=status), self.assertRaisesRegex(GenerationBlocked, 'NON_COMPLAINT_STATUS_SCOPE_CONFLICT'):
                assemble(self.work)
            for row in self.review['records']:
                row['scope'] = 'non_complaint'
            self.save()
            assemble(self.work)
            report = json.loads((self.work/'report.json').read_text('utf-8'))
            self.assertEqual(report['top_ten'], [])
            self.assertEqual(sum(t['rank_count'] for t in report['themes']), 0)

    def test_audit_rejects_status_scope_conflict_before_aggregate_checks(self):
        assemble(self.work)
        report = json.loads((self.work/'report.json').read_text('utf-8'))
        report['records'][0]['mail_status'] = 'resolved'
        write_json(self.work/'report.json', report)
        with self.assertRaisesRegex(GenerationBlocked, 'NON_COMPLAINT_STATUS_SCOPE_CONFLICT'):
            audit_report(self.work/'report.json', self.work/'source.json')

    def test_source_subject_original_recipients_cc_and_time_must_match(self):
        assemble(self.work)
        original = json.loads((self.work/'report.json').read_text('utf-8'))
        changes = {'subject': 'Subject from a different mail', 'recipients_original': [{'address': 'wrong@example.test'}], 'cc': [{'address': 'wrong-copy@example.test'}], 'at': '2026-10-28T15:40:00+08:00'}
        for field, value in changes.items():
            report = deepcopy(original)
            report['records'][0][field] = value
            write_json(self.work/'report.json', report)
            with self.subTest(field=field), self.assertRaisesRegex(GenerationBlocked, 'REPORT_SOURCE_HEADER_MISMATCH'):
                audit_report(self.work/'report.json', self.work/'source.json')
        projected = deepcopy(original)
        projected['records'][0]['to'] = ['support@example.test']
        write_json(self.work/'report.json', projected)
        self.assertEqual(audit_report(self.work/'report.json', self.work/'source.json')['status'], 'validated')

    def test_build_recreates_wrong_and_interrupted_previews_from_verified_originals(self):
        image = BytesIO()
        Image.new('RGB', (12, 12), 'red').save(image, 'PNG')
        payloads = {'9': b'True original log evidence.\n', '10': image.getvalue()}
        self.source['attachments'] = [{'mail_pk': '1', 'payload': {'id': key, 'message_pk': '1', 'filename': name, 'content_type': mime, 'size_bytes': len(payloads[key])}}
            for key, name, mime in [('9', 'Player.log', 'text/plain'), ('10', 'screenshot.png', 'image/png')]]
        self.save()
        attachments = self.work / 'attachments'
        attachments.mkdir()
        for key, payload in payloads.items():
            (attachments / (key + '.bin')).write_bytes(payload)
        write_json(attachments / 'manifest.json', {'source_snapshot_sha256': self.review['source_snapshot_sha256'], 'files': {
            key: {'status': 'ready', 'identity_verified': True, 'sha256': sha256(payload).hexdigest(), 'size': len(payload)} for key, payload in payloads.items()}})
        assemble(self.work)
        expected = {suffix: (attachments / name).read_bytes() for suffix, name in [('text', '9.txt'), ('image', '10.jpg')]}
        other = BytesIO()
        Image.new('RGB', (12, 12), 'blue').save(other, 'JPEG')
        for index, incorrect in enumerate([other.getvalue(), b'', b'INVALID JPEG']):
            with self.subTest(case=index):
                (attachments / '9.txt').write_text('Unrelated old cached log.', 'utf-8')
                (attachments / '10.jpg').write_bytes(incorrect)
                assemble(self.work)
                self.assertEqual((attachments / '9.txt').read_bytes(), expected['text'])
                self.assertEqual((attachments / '10.jpg').read_bytes(), expected['image'])
                self.assertEqual(audit_report(self.work / 'report.json', self.work / 'source.json')['status'], 'validated')
                published = self.work.parent / ('publication-' + str(index))
                self.assertEqual(publish(self.work, published)['status'], 'published')
                self.assertEqual((published / '2026-10-28/attachments/10.jpg').read_bytes(), expected['image'])
        (attachments / '9.bin').write_bytes(b'corrupt original')
        with self.assertRaisesRegex(GenerationBlocked, 'ATTACHMENTS_NOT_COMPLETE'):
            assemble(self.work)

    def test_missing_pdf_renderer_does_not_certify_an_unrelated_cached_first_page(self):
        payload = b'%PDF-1.4\nSynthetic PDF renderer-unavailable branch.\n%%EOF'
        self.source['attachments'] = [{'mail_pk': '1', 'payload': {'id': '9', 'message_pk': '1', 'filename': 'document.pdf', 'content_type': 'application/pdf', 'size_bytes': len(payload)}}]
        self.save()
        attachments = self.work / 'attachments'
        attachments.mkdir()
        (attachments / '9.bin').write_bytes(payload)
        (attachments / '9.pdf.jpg').write_bytes(b'UNPROVEN CACHED PDF PAGE')
        write_json(attachments / 'manifest.json', {'source_snapshot_sha256': self.review['source_snapshot_sha256'], 'files': {'9': {'status': 'ready', 'identity_verified': True, 'sha256': sha256(payload).hexdigest(), 'size': len(payload)}}})
        with patch('insights.attachment_preview.shutil.which', return_value=None):
            assemble(self.work)
        item = json.loads((self.work / 'report.json').read_text('utf-8'))['records'][0]['files'][0]
        self.assertFalse(item['preview_image'])
        self.assertEqual(item['preview_error'], 'PDF_RENDERER_UNAVAILABLE')
        self.assertFalse((attachments / '9.pdf.jpg').exists())

    def test_republish_and_prepare_verify_the_actual_published_evidence(self):
        from insights.daily_generation import main, audit_published_report
        payload = b'Synthetic client log for publication integrity.\n'
        self.source['attachments'] = [{'mail_pk': '1', 'payload': {'id': '9', 'message_pk': '1', 'filename': 'Player.log', 'content_type': 'text/plain', 'size_bytes': len(payload)}}]
        self.save()
        attachments = self.work/'attachments'
        attachments.mkdir()
        (attachments/'9.bin').write_bytes(payload)
        write_json(attachments/'manifest.json', {'source_snapshot_sha256': self.review['source_snapshot_sha256'], 'files': {'9': {'status': 'ready', 'identity_verified': True, 'sha256': sha256(payload).hexdigest(), 'size': len(payload)}}})
        assemble(self.work)
        reports = self.work.parent/'isolated-published'
        self.assertEqual(publish(self.work, reports)['status'], 'published')
        destination = reports/'2026-10-28'
        archived = next((destination/'archives').glob('*.zip'))
        targets = [destination/'attachments/9.bin', destination/'attachments/9.txt', archived, destination/'source.json', destination/'review.json', destination/'quality.json', destination/'attachments/manifest.json']
        for target in targets:
            old = target.read_bytes()
            target.write_bytes(b'corrupted-after-publication')
            with self.subTest(target=target.name), self.assertRaisesRegex(GenerationBlocked, 'PUBLISHED_REPORT_NOT_INTACT'):
                publish(self.work, reports)
            self.assertEqual(target.read_bytes(), b'corrupted-after-publication')
            output = StringIO()
            with patch('insights.daily_generation.REPORTS', reports), patch('sys.argv', ['daily_generation', 'prepare', '--date', '2026-10-28']), redirect_stdout(output), self.assertRaises(SystemExit) as stopped:
                main()
            self.assertEqual(stopped.exception.code, 2)
            self.assertEqual(json.loads(output.getvalue())['status'], 'blocked')
            target.write_bytes(old)
            self.assertEqual(audit_published_report(destination)['status'], 'validated')
            self.assertEqual(publish(self.work, reports)['status'], 'already_published')
        old = (destination/'review.json').read_bytes()
        (destination/'review.json').unlink()
        with self.assertRaisesRegex(GenerationBlocked, 'PUBLISHED_EVIDENCE_MISSING:review.json'):
            publish(self.work, reports)
        self.assertFalse((destination/'review.json').exists())
        (destination/'review.json').write_bytes(old)
        self.assertEqual(publish(self.work, reports)['status'], 'already_published')

    def _build_publication_with_log(self):
        payload = b'Publication evidence must be intact before a date becomes visible.\n'
        self.source['attachments'] = [{'mail_pk': '1', 'payload': {'id': '9', 'message_pk': '1',
            'filename': 'Player.log', 'content_type': 'text/plain', 'size_bytes': len(payload)}}]
        self.save()
        attachments = self.work / 'attachments'
        attachments.mkdir()
        (attachments / '9.bin').write_bytes(payload)
        write_json(attachments / 'manifest.json', {'source_snapshot_sha256': self.review['source_snapshot_sha256'],
            'files': {'9': {'status': 'ready', 'identity_verified': True,
                            'sha256': sha256(payload).hexdigest(), 'size': len(payload)}}})
        assemble(self.work)
        return attachments / 'manifest.json'

    def test_first_publication_rejects_evidence_lost_or_revoked_after_build(self):
        manifest = self._build_publication_with_log()
        original = manifest.read_bytes()
        cases = ['missing', 'source', 'identity', 'identity-type', 'status', 'file', 'digest', 'json']
        for case in cases:
            with self.subTest(case=case):
                value = json.loads(original)
                if case == 'missing':
                    manifest.unlink()
                elif case == 'json':
                    manifest.write_bytes(b'{interrupted evidence')
                else:
                    if case == 'source': value['source_snapshot_sha256'] = '0' * 64
                    if case == 'identity': value['files']['9']['identity_verified'] = False
                    if case == 'identity-type': value['files']['9']['identity_verified'] = 1
                    if case == 'status': value['files']['9']['status'] = 'failed'
                    if case == 'file': value['files'].pop('9')
                    if case == 'digest': value['files']['9']['sha256'] = '0' * 64
                    write_json(manifest, value)
                reports = self.work.parent / ('rejected-' + case)
                with self.assertRaisesRegex(GenerationBlocked, 'PUBLISHED_REPORT_NOT_INTACT'):
                    publish(self.work, reports)
                self.assertFalse((reports / '2026-10-28').exists())
                self.assertFalse((self.work / 'state.json').exists())
                manifest.write_bytes(original)
        reports = self.work.parent / 'valid-after-repair'
        self.assertEqual(publish(self.work, reports)['status'], 'published')
        destination = reports / '2026-10-28'
        before = {p.relative_to(destination): p.read_bytes() for p in destination.rglob('*') if p.is_file()}
        self.assertEqual(publish(self.work, reports)['status'], 'already_published')
        self.assertEqual(before, {p.relative_to(destination): p.read_bytes() for p in destination.rglob('*') if p.is_file()})

    def test_copied_staging_evidence_is_checked_before_atomic_visibility(self):
        manifest = self._build_publication_with_log()
        original = manifest.read_bytes()
        real_copytree = shutil.copytree
        for case in ['missing', 'source', 'identity']:
            injected = []

            def copy_with_fault(source, destination, *args, **kwargs):
                result = real_copytree(source, destination, *args, **kwargs)
                target = Path(destination)
                if target.name == 'attachments' and target.parent.name.startswith('.publishing-'):
                    staged_manifest = target / 'manifest.json'
                    if case == 'missing':
                        staged_manifest.unlink()
                    else:
                        value = json.loads(staged_manifest.read_bytes())
                        if case == 'source': value['source_snapshot_sha256'] = '0' * 64
                        if case == 'identity': value['files']['9']['identity_verified'] = False
                        write_json(staged_manifest, value)
                    injected.append(str(target))
                return result

            with self.subTest(case=case):
                reports = self.work.parent / ('staged-' + case)
                with patch('insights.daily_generation.shutil.copytree', side_effect=copy_with_fault):
                    with self.assertRaisesRegex(GenerationBlocked, 'PUBLISHED_REPORT_NOT_INTACT'):
                        publish(self.work, reports)
                self.assertEqual(len(injected), 1)
                self.assertFalse((reports / '2026-10-28').exists())
                self.assertEqual(list(reports.iterdir()), [])
                self.assertFalse((self.work / 'state.json').exists())
                self.assertEqual(manifest.read_bytes(), original)
        self.assertEqual(publish(self.work, self.work.parent / 'valid-staging')['status'], 'published')

    def _unavailable_log(self, *, approved=False):
        self.source['attachments'] = [{'mail_pk': '1', 'payload': {'id': '9', 'message_pk': '1',
            'filename': 'Player.log', 'content_type': 'text/plain', 'size_bytes': 17,
            'attachment_id': 'synthetic-log-9'}}]
        self.save()
        write_json(self.work / 'attachments/manifest.json', {
            'source_snapshot_sha256': self.review['source_snapshot_sha256'],
            'files': {'9': {'status': 'failed', 'error': 'SYNTHETIC_MESSAGE_NOT_AVAILABLE'}}})
        authorization = {'format': 'complaint-daily-attachment-exceptions/v1',
            'source_snapshot_sha256': self.review['source_snapshot_sha256'], 'business_date': '2026-10-28',
            'decision': {'outcome': 'Approved', 'decided_by': 'user',
                'presented': 'Synthetic fixture: one missing original may be skipped?',
                'response': 'Synthetic approval limited to attachment 9.',
                'decided_at': (datetime.now().astimezone()-timedelta(seconds=1)).isoformat(),
                'source_ref': 'synthetic-test-only; not a real user approval'},
            'files': [{'attachment_id': '9', 'mail_pk': '1', 'filename': 'Player.log',
                       'expected_size': 17, 'source_attachment_id': 'synthetic-log-9',
                       'reason': 'Synthetic original no longer available; metadata retained.'}]}
        if approved:
            write_json(self.work / 'attachment-exceptions.json', authorization)
            self.review['attachment_exception_authorization'] = {'file': 'attachment-exceptions.json',
                'sha256': sha256((self.work / 'attachment-exceptions.json').read_bytes()).hexdigest()}
            self.save()
        return authorization

    def test_missing_original_without_explicit_scope_still_blocks(self):
        self._unavailable_log()
        with self.assertRaisesRegex(GenerationBlocked, 'ATTACHMENTS_NOT_COMPLETE'):
            assemble(self.work)

    def test_explicit_unavailable_keeps_metadata_and_disables_incomplete_zip(self):
        self._unavailable_log(approved=True)
        result = assemble(self.work)
        self.assertEqual(result['attachments_unavailable_authorized'], 1)
        report = json.loads((self.work / 'report.json').read_bytes())
        self.assertEqual(report['coverage']['expected'], 2)
        self.assertEqual(report['coverage']['attachments_expected'], 1)
        self.assertEqual(report['coverage']['attachments_ready'], 0)
        self.assertEqual(report['unavailable_attachment_ids'], ['9'])
        item = report['records'][0]['files'][0]
        self.assertIs(item['ready'], False)
        self.assertIsNone(item['sha256'])
        self.assertTrue(item['availability_exception']['reason'])
        self.assertEqual(report['log_archives'], {})
        self.assertEqual(report['subthemes'][0]['log_archive']['status'], 'unavailable')
        root = self.work.parent / 'authorized-missing'
        self.assertEqual(publish(self.work, root)['status'], 'published')
        destination = root / '2026-10-28'
        self.assertEqual((destination / 'attachment-exceptions.json').read_bytes(),
                         (self.work / 'attachment-exceptions.json').read_bytes())
        self.assertEqual(publish(self.work, root)['status'], 'already_published')
        (destination / 'attachment-exceptions.json').unlink()
        with self.assertRaises(GenerationBlocked):
            publish(self.work, root)

    def test_unavailability_cannot_change_source_date_identity_or_user_decision(self):
        authorization = self._unavailable_log(approved=True)
        for case in ['source', 'date', 'owner', 'id', 'size', 'name', 'source-id', 'decision', 'actor', 'duplicate']:
            value = deepcopy(authorization)
            if case == 'source': value['source_snapshot_sha256'] = '0'*64
            if case == 'date': value['business_date'] = '2026-10-27'
            if case == 'owner': value['files'][0]['mail_pk'] = '2'
            if case == 'id': value['files'][0]['attachment_id'] = '10'
            if case == 'size': value['files'][0]['expected_size'] = 18
            if case == 'name': value['files'][0]['filename'] = 'Other.log'
            if case == 'source-id': value['files'][0]['source_attachment_id'] = 'wrong'
            if case == 'decision': value['decision']['outcome'] = 'Pending'
            if case == 'actor': value['decision']['decided_by'] = 'agent'
            if case == 'duplicate': value['files'].append(deepcopy(value['files'][0]))
            write_json(self.work / 'attachment-exceptions.json', value)
            self.review['attachment_exception_authorization']['sha256'] = sha256((self.work / 'attachment-exceptions.json').read_bytes()).hexdigest()
            self.save()
            with self.subTest(case=case), self.assertRaises(GenerationBlocked):
                assemble(self.work)

    def test_publication_rechecks_exception_evidence_after_copy(self):
        self._unavailable_log(approved=True)
        assemble(self.work)
        original_copy = shutil.copy2
        def changed_copy(source, destination, *args, **kwargs):
            result = original_copy(source, destination, *args, **kwargs)
            if Path(destination).name == 'attachment-exceptions.json':
                Path(destination).write_bytes(b'changed during copy')
            return result
        root = self.work.parent / 'changed-exception'
        with patch('insights.daily_generation.shutil.copy2', side_effect=changed_copy):
            with self.assertRaises(GenerationBlocked):
                publish(self.work, root)
        self.assertFalse((root / '2026-10-28').exists())

    def test_unavailability_cannot_mask_existing_bad_bytes_or_extra_missing_files(self):
        self._unavailable_log(approved=True)
        (self.work / 'attachments/9.bin').write_bytes(b'tampered existing bytes')
        with self.assertRaisesRegex(GenerationBlocked, 'CANNOT_MASK_PRESENT_FILE'):
            assemble(self.work)
        (self.work / 'attachments/9.bin').unlink()
        self.source['attachments'].append({'mail_pk': '2', 'payload': {'id': '10', 'message_pk': '2',
            'filename': 'Other.log', 'content_type': 'text/plain', 'size_bytes': 8}})
        # Keep the original authorization scope; rebinding the snapshot cannot authorize an extra ID.
        self.save()
        auth = json.loads((self.work / 'attachment-exceptions.json').read_bytes())
        auth['source_snapshot_sha256'] = self.review['source_snapshot_sha256']
        write_json(self.work / 'attachment-exceptions.json', auth)
        self.review['attachment_exception_authorization']['sha256'] = sha256((self.work / 'attachment-exceptions.json').read_bytes()).hexdigest()
        self.save()
        manifest = json.loads((self.work / 'attachments/manifest.json').read_bytes())
        manifest['source_snapshot_sha256'] = self.review['source_snapshot_sha256']
        write_json(self.work / 'attachments/manifest.json', manifest)
        with self.assertRaisesRegex(GenerationBlocked, 'ATTACHMENTS_NOT_COMPLETE'):
            assemble(self.work)

    def test_subgroup_link_and_review_input_cannot_be_resigned_to_another_source(self):
        self._build_publication_with_log()
        report_path = self.work / 'report.json'
        original = json.loads(report_path.read_bytes())
        broken = deepcopy(original)
        broken['subthemes'][0]['log_archive'] = None
        write_json(report_path, broken)
        with self.assertRaisesRegex(GenerationBlocked, 'SUBGROUP_ARCHIVE_BINDING'):
            audit_report(report_path, self.work / 'source.json')
        write_json(report_path, original)
        self.review['source_snapshot_sha256'] = '0'*64
        write_json(self.work / 'review.json', self.review)
        digest = sha256((self.work / 'review.json').read_bytes()).hexdigest()
        original['grouping_review']['sha256'] = original['uid_review']['sha256'] = digest
        original['review_sources'][0]['sha256'] = digest
        for row in original['records']: row['metadata']['review_sha256'] = digest
        write_json(report_path, original)
        with self.assertRaisesRegex(GenerationBlocked, 'REVIEW_SOURCE_BINDING'):
            audit_report(report_path, self.work / 'source.json')

    def test_zip_self_consistent_replacement_cannot_impersonate_original_log(self):
        from zipfile import ZipFile
        self._build_publication_with_log()
        report_path = self.work / 'report.json'
        report = json.loads(report_path.read_bytes())
        key, meta = next(iter(report['log_archives'].items()))
        archive = self.work / 'archives' / (key + '.zip')
        with ZipFile(archive) as zipped: manifest = json.loads(zipped.read('_manifest.json'))
        replacement = b'This is a different original log.\n'
        manifest['files'][0]['sha256'] = sha256(replacement).hexdigest()
        manifest['files'][0]['size'] = len(replacement)
        with ZipFile(archive, 'w') as zipped:
            zipped.writestr('_manifest.json', json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
            zipped.writestr(manifest['files'][0]['entry'], replacement)
        meta['sha256'] = sha256(archive.read_bytes()).hexdigest()
        meta['size'] = archive.stat().st_size
        report['subthemes'][0]['log_archive'] = meta
        write_json(report_path, report)
        with self.assertRaisesRegex(GenerationBlocked, 'ARCHIVE_SOURCE_BINDING'):
            audit_report(report_path, self.work / 'source.json')

    def _reviewed_log_package(self, *, raw=None, filename='Support-logs.zip'):
        from zipfile import ZipFile
        if raw is None:
            stream = BytesIO()
            with ZipFile(stream, 'w') as archive:
                archive.writestr('Player.log', b'Synthetic log only.\n')
                archive.writestr('identity-note.txt', b'Synthetic member; no real account.')
            raw = stream.getvalue()
        self.source['attachments'] = [{'mail_pk': '1', 'payload': {'id': '9', 'message_pk': '1',
            'filename': filename, 'content_type': 'application/zip' if filename.endswith('.zip') else 'application/octet-stream', 'size_bytes': len(raw)}}]
        self.review['log_packages'] = [{'attachment_id': '9', 'mail_pk': '1', 'source_sha256': sha256(raw).hexdigest(),
            'member_names': ['Player.log', 'identity-note.txt'], 'basis': 'Synthetic inspected archive containing logs.'}]
        self.save()
        write_json(self.work / 'attachments/manifest.json', {'source_snapshot_sha256': self.review['source_snapshot_sha256'],
            'files': {'9': {'status': 'ready', 'identity_verified': True, 'sha256': sha256(raw).hexdigest(), 'size': len(raw)}}})
        (self.work / 'attachments/9.bin').write_bytes(raw)
        return raw

    def test_verified_original_log_package_is_bundled_without_unpacking_or_rewriting(self):
        from zipfile import ZipFile
        raw = self._reviewed_log_package()
        assemble(self.work)
        report = json.loads((self.work / 'report.json').read_bytes())
        item = report['records'][0]['files'][0]
        self.assertEqual(item['kind'], 'log')
        self.assertIs(item['log_package'], True)
        self.assertEqual(item['preview_type'], 'metadata')
        key = next(iter(report['log_archives']))
        with ZipFile(self.work / 'archives' / (key + '.zip')) as archive:
            manifest = json.loads(archive.read('_manifest.json'))
            self.assertEqual(manifest['file_count'], 1)
            self.assertEqual(archive.read(manifest['files'][0]['entry']), raw)
        self.assertEqual((self.work / 'attachments/9.bin').read_bytes(), raw)

    def test_inspected_sevenzip_log_original_is_bundled_byte_for_byte(self):
        from base64 import b64decode
        from zipfile import ZipFile
        # A real 7z containing one locally authored synthetic Player.log.
        raw = b64decode('N3q8ryccAATQKcQoHQAAAAAAAABiAAAAAAAAAORqCN4BABhTeW50aGV0aWMgdGVzdCBsb2cgb25seS4KAAEEBgABCR0ABwsBAAEhIQEADBkACAoBj+5xDAAABQEZDAAAAAAAAAAAAAAAABEXAFAAbABhAHkAZQByAC4AbABvAGcAAAAZBAAAAAAUCgEAx5cAXa9q3QEVBgEAIAAAAAAA')
        self._reviewed_log_package(raw=raw, filename='Player.7z')
        self.review['log_packages'][0]['member_names'] = ['Player.log']
        self.save()
        assemble(self.work)
        report = json.loads((self.work / 'report.json').read_bytes())
        item = report['records'][0]['files'][0]
        self.assertEqual(item['name'], 'Player.7z')
        self.assertEqual(item['kind'], 'log')
        self.assertEqual(item['preview_type'], 'metadata')
        archive_id = next(iter(report['log_archives']))
        with ZipFile(self.work / 'archives' / (archive_id + '.zip')) as archive:
            manifest = json.loads(archive.read('_manifest.json'))
            self.assertEqual(manifest['file_count'], 1)
            self.assertEqual(archive.read(manifest['files'][0]['entry']), raw)
        self.assertEqual((self.work / 'attachments/9.bin').read_bytes(), raw)

    def test_sevenzip_extension_cannot_impersonate_another_archive_or_plain_text(self):
        zip_bytes = self._reviewed_log_package()
        for raw in (zip_bytes, b'This is plain text, not a 7z archive.'):
            self._reviewed_log_package(raw=raw, filename='Player.7z')
            with self.subTest(signature=raw[:8]), self.assertRaisesRegex(GenerationBlocked, 'LOG_PACKAGE_FORMAT_MISMATCH'):
                assemble(self.work)

    def test_log_package_review_cannot_change_owner_digest_or_remove_log_members(self):
        self._reviewed_log_package()
        original = deepcopy(self.review['log_packages'][0])
        for case in ['owner', 'digest', 'no-logs', 'duplicate']:
            entry = deepcopy(original)
            if case == 'owner': entry['mail_pk'] = '2'
            if case == 'digest': entry['source_sha256'] = '0'*64
            if case == 'no-logs': entry['member_names'] = ['picture.png']
            self.review['log_packages'] = [entry, deepcopy(entry)] if case == 'duplicate' else [entry]
            self.save()
            with self.subTest(case=case), self.assertRaises(GenerationBlocked):
                assemble(self.work)

    def test_unready_report_cannot_skip_missing_original_even_with_matching_quality_digest(self):
        manifest_path = self._build_publication_with_log()
        stream = BytesIO()
        Image.new('RGB', (12, 12), 'green').save(stream, 'PNG')
        payload = stream.getvalue()
        self.source['attachments'].append({'mail_pk': '1', 'payload': {'id': '10', 'message_pk': '1',
            'filename': 'screen.png', 'content_type': 'image/png', 'size_bytes': len(payload)}})
        self.save()
        manifest = json.loads(manifest_path.read_bytes())
        manifest['source_snapshot_sha256'] = self.review['source_snapshot_sha256']
        manifest['files']['10'] = {'status': 'ready', 'identity_verified': True,
                                  'sha256': sha256(payload).hexdigest(), 'size': len(payload)}
        write_json(manifest_path, manifest)
        image_path = self.work / 'attachments/10.bin'
        image_path.write_bytes(payload)
        assemble(self.work)
        original = json.loads((self.work / 'report.json').read_bytes())
        quality = json.loads((self.work / 'quality.json').read_bytes())
        for case, ready, status, missing in [('missing', False, 'failed', True),
                ('not-ready', False, 'ready', False), ('status', True, 'failed', False),
                ('boolean-type', 1, 'ready', False)]:
            with self.subTest(case=case):
                report = deepcopy(original)
                item = next(f for r in report['records'] for f in r['files'] if f['id'] == '10')
                item.update(ready=ready, status=status)
                report['coverage']['attachments_ready'] = sum(f['ready'] for r in report['records'] for f in r['files'])
                if missing: image_path.unlink()
                write_json(self.work / 'report.json', report)
                signed = {**quality, 'report_sha256': sha256((self.work / 'report.json').read_bytes()).hexdigest()}
                write_json(self.work / 'quality.json', signed)
                with self.assertRaisesRegex(GenerationBlocked, 'REPORT_ATTACHMENTS_NOT_COMPLETE'):
                    audit_report(self.work / 'report.json', self.work / 'source.json')
                reports = self.work.parent / ('unready-' + case)
                with self.assertRaisesRegex(GenerationBlocked, 'REPORT_ATTACHMENTS_NOT_COMPLETE'):
                    publish(self.work, reports)
                self.assertFalse((reports / '2026-10-28').exists())
                self.assertFalse((self.work / 'state.json').exists())
                image_path.write_bytes(payload)
        write_json(self.work / 'report.json', original)
        write_json(self.work / 'quality.json', quality)
        self.assertEqual(publish(self.work, self.work.parent / 'complete-after-unready')['status'], 'published')


if __name__ == '__main__':
    unittest.main()
