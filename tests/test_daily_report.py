"""Read-model boundaries and inert attachments; no production or source database."""
from email.message import EmailMessage
from hashlib import sha1, sha256
from io import BytesIO
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image

from starlette.testclient import TestClient

from insights.attachment_fetcher import download, mime_attachments
from insights.attachment_preview import decode_text, file_kind, prepare_files
from insights.config import ROOT
from insights.daily_board import create_app
from insights.daily_report import (apply_mail_refinements, group_read_model, main_read_model,
                                   original_body, received_hour, statistics, uid_evidence)


class DailyDataTests(unittest.TestCase):
    def test_operational_groups_keep_diagnostic_leaves_and_rank_only_complaint_mail(self):
        records = [{'id': str(i), 'scope': scope, 'theme_id': 'old:' + leaf,
                    'theme_name': leaf, 'subtheme_id': leaf, 'subtheme_name': leaf,
                    'metadata': {}, 'uid': {}, **({'mail_status': 'follow_up'} if i == 2 else {})}
                   for i, leaf, scope in [(1, 'black-screen', 'complaint'), (2, 'script-failed', 'complaint'),
                                          (3, 'compatibility', 'non_complaint'), (4, 'download-stall', 'complaint')]]
        groups = [{'id': key, 'name': key, 'definition': key, 'domain_id': 'entry-update',
                   'domain_name': '进入游戏与更新', 'eligible_top10': True}
                  for key in ['update-launch', 'download-progress']]
        main, sub, domains = main_read_model(records, groups, {
            'black-screen': 'update-launch', 'script-failed': 'update-launch',
            'compatibility': 'update-launch', 'download-stall': 'download-progress'})
        launch = next(g for g in main if g['id'] == 'main:update-launch')
        self.assertEqual((launch['count'], launch['rank_count']), (3, 2))
        self.assertEqual(launch['rank_share'], 50)
        self.assertEqual(len(sub), 4)
        self.assertEqual(sum(d['count'] for d in domains), 4)
        self.assertEqual(records[1]['mail_status'], 'follow_up')
        self.assertEqual(records[0]['metadata']['diagnostic_group']['id'], 'old:black-screen')

    def test_reclassification_retains_prior_decision_and_requires_identification_consistency(self):
        record = {'id': '1', 'summary': '旧摘要', 'basis': '旧依据', 'scope': 'unclear', 'metadata': {}}
        decision = {'mail_pk': 1, 'reviewed': True, 'summary_zh': '截图明确空间不足', 'basis': '真实图片提示',
                    'main_id': 'storage-capacity', 'scope': 'complaint', 'identified': True,
                    'mail_status': 'materials', 'specific_issue_id': 'storage-prompt', 'specific_issue_name': '空间提示'}
        apply_mail_refinements([record], [decision], review_sha256='review-fixture')
        self.assertEqual(record['summary'], '截图明确空间不足')
        self.assertEqual(record['metadata']['final_reclassification']['previous']['summary'], '旧摘要')
        apply_mail_refinements([record], [{**decision, 'body_zh': '沿用的系统译文', 'translation_origin': 'source-ai'}], review_sha256='review-fixture')
        self.assertEqual(record['translation_origin'], 'source-ai')
        apply_mail_refinements([record], [{**decision, 'body_zh': 'HTML补译', 'translation_origin': 'review-agent-html'}], review_sha256='review-fixture')
        self.assertEqual(record['translation_origin'], 'review-agent')
        with self.assertRaises(ValueError):
            apply_mail_refinements([record], [{**decision, 'main_id': 'unknown'}], review_sha256='review-fixture')

    def test_semantic_groups_merge_same_error_and_split_source_taxonomy_collisions(self):
        records=[{'id':str(n),'scope':'complaint','theme_id':leaf,'theme_name':name,
                  'uid':{},'original_classification':{'issue_type_id':old}}
                 for n,leaf,name,old in [(1,'complaint:space-a','空间不足提示','old-a'),
                                         (2,'complaint:space-b','更新空间不足提示','old-b'),
                                         (3,'complaint:download-reset','下载归零','old-a')]]
        def definition(parent,name):
            return {'parent_id':parent,'parent_name':name,'definition':name,
                    'domain_id':'entry','domain_name':'进入游戏与更新','concrete':True}
        definitions={'complaint:space-a':definition('space','提示可用空间不足'),
                     'complaint:space-b':definition('space','提示可用空间不足'),
                     'complaint:download-reset':definition('reset','下载进度丢失或归零')}
        parents,children,domains=group_read_model(records,definitions)
        self.assertEqual([p['count'] for p in parents],[2,1])
        self.assertEqual(len(children),3)
        self.assertEqual(sum(d['count'] for d in domains),3)
        self.assertEqual(records[0]['theme_id'],records[1]['theme_id'])
        self.assertNotEqual(records[0]['theme_id'],records[2]['theme_id'])
        with self.assertRaises(ValueError):group_read_model([{'id':'1','scope':'complaint','theme_id':'missing'}],definitions)

    def test_growth_uses_unrounded_average_and_handles_missing_or_zero_base(self):
        daily=[{'business_date':f'2026-10-{day}','count':count} for day,count in
               [(22,371),(23,329),(24,309),(25,298),(26,277),(27,281),(28,259),(29,634)]]
        result=statistics(daily,'2026-10-29')
        self.assertAlmostEqual(result['previous_seven_average'],2124/7)
        self.assertAlmostEqual(result['growth_seven'],(634/(2124/7)-1)*100)
        self.assertIsNone(statistics([{'business_date':'2026-10-28','count':0}], '2026-10-29')['growth_previous'])
        self.assertIsNone(statistics([], '2026-10-29')['previous_seven_average'])

    def test_original_html_is_only_text_never_active_instructions(self):
        body=original_body({'body_html':'<p>Original evidence</p><script>alert("leak")</script><img src="https://example.invalid">'})
        self.assertIn('Original evidence',body)
        self.assertNotIn('alert',body)
        self.assertNotIn('https://',body)

    def test_uid_ambiguity_never_selects_an_arbitrary_value_or_other_mailbox(self):
        mail={'from_address':'sender@example.invalid','mailbox':'inbox@example.invalid'}
        base={'state':'multiple_accounts_or_conflict','from_address':mail['from_address'],
              'delivery_mailbox':mail['mailbox'],'value':'300000000001','verified':True,'fields':[]}
        self.assertEqual(uid_evidence(base,mail)['value'],'')
        self.assertEqual(uid_evidence(base,mail)['state'],'conflict')
        for state in ['not_found','unverified_candidate']:
            self.assertEqual(uid_evidence({**base,'state':state},mail)['value'],'')
        with self.assertRaises(ValueError):uid_evidence({**base,'delivery_mailbox':'other@example.invalid'},mail)
        with self.assertRaises(ValueError):uid_evidence({**base,'state':'message_text_supported','verified':False},mail)
        self.assertEqual(uid_evidence({**base,'state':'conversation_text_supported'},mail)['state'],'verified_thread')
        roles=[{'role':'primary','value':'300000000001'},{'role':'accidental','value':'300000000002'}]
        evidence=uid_evidence({**base,'uid_roles':roles},mail)
        self.assertEqual(evidence['uid_roles'],roles)
        self.assertEqual(evidence['value'],'')

    def test_hourly_distribution_uses_beijing_date_and_rejects_ambiguous_timestamps(self):
        self.assertEqual(received_hour({'received_at':'2026-10-28T16:00:00+00:00'},'2026-10-29'),0)
        self.assertEqual(received_hour({'received_at':'2026-10-29T15:59:59Z'},'2026-10-29'),23)
        for stamp in ['2026-10-29T16:00:00+00:00','2026-10-29T00:00:00']:
            with self.assertRaises(ValueError):received_hour({'received_at':stamp},'2026-10-29')

    def test_log_mime_and_binary_are_not_mislabeled_as_text(self):
        self.assertEqual(file_kind('client.log','application/octet-stream'),'log')
        self.assertEqual(file_kind('phone.heic','image/heic'),'image')
        self.assertEqual(file_kind('client.log.zst','application/octet-stream'),'log')
        self.assertEqual(file_kind('proof.pdf','application/pdf'),'document')
        with self.assertRaises(ValueError):decode_text(b'\x00'*100)
        self.assertEqual(decode_text('真实日志'.encode('utf-16')),'真实日志')


class AttachmentDownloadTests(unittest.TestCase):
    def test_each_mail_epoch_is_checked_on_reuse_switch_and_reconnect(self):
        cases = [
            ('reuse-valid', [77, 77], ['INBOX', 'INBOX'], [{'INBOX': 77}], False, 2, 0, 1),
            ('reuse-stale', [77, 66], ['INBOX', 'INBOX'], [{'INBOX': 77}], False, 1, 1, 1),
            ('switch-valid', [77, 88], ['INBOX', 'Archive'], [{'INBOX': 77, 'Archive': 88}], False, 2, 0, 2),
            ('switch-stale', [77, 66], ['INBOX', 'Archive'], [{'INBOX': 77, 'Archive': 88}], False, 1, 1, 2),
            ('reconnect-valid', [77, 77], ['INBOX', 'INBOX'], [{'INBOX': 77}, {'INBOX': 77}], True, 2, 0, 2),
            ('reconnect-stale', [77, 77], ['INBOX', 'INBOX'], [{'INBOX': 77}, {'INBOX': 88}], True, 1, 1, 2),
            ('first-stale', [66, 77], ['INBOX', 'INBOX'], [{'INBOX': 77}], False, 1, 1, 2),
            ('continue-after-stale', [77, 66, 77], ['INBOX', 'INBOX', 'INBOX'], [{'INBOX': 77}], False, 2, 1, 2),
        ]
        for name, epochs, folders, namespaces, disconnect, ready, failed, selects in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory(dir=ROOT/'.runtime') as temp:
                directory = Path(temp)
                calls, messages, attachments, mails = [], {}, [], []
                for index, (epoch, folder) in enumerate(zip(epochs, folders), 1):
                    uid = str(7000 + index)
                    message = EmailMessage()
                    message['Message-ID'] = f'<{name}-{uid}@example.invalid>'
                    message.set_content('Frozen synthetic mail')
                    payload = f'Original epoch test {uid}'.encode()
                    message.add_attachment(payload, maintype='application', subtype='octet-stream', filename='client.log')
                    messages[uid] = message.as_bytes()
                    attachments.append({'payload': {'id': uid, 'message_pk': uid,
                        'attachment_id': f'imap-{uid}-2-'+sha1(payload).hexdigest()[:16],
                        'filename': 'client.log', 'size_bytes': len(payload), 'content_type': 'application/octet-stream'}})
                    mails.append({'mail_pk': uid, 'mailbox': 'epoch@example.invalid',
                        'smtp_message_id': str(message['Message-ID']),
                        'raw_payload': {'imap_uid': int(uid), 'imap_uidvalidity': epoch, 'imap_folder': folder}})
                (directory/'source.json').write_text(json.dumps({'source_id': name, 'business_date': '2026-10-29',
                    'mails': mails, 'attachments': attachments}), encoding='utf-8')
                (directory/'service.json').write_text(json.dumps({'host': 'imap.feishu.cn', 'port': 993,
                    'accounts': {'epoch@example.invalid': 'synthetic-password'}}), encoding='utf-8')
                instances, transient = [0], [disconnect]

                class MemoryIMAP:
                    def __init__(self, *args, **kwargs):
                        self.namespace = namespaces[min(instances[0], len(namespaces)-1)]
                        instances[0] += 1
                        self.folder = None
                    def login(self, *args):
                        return 'OK', []
                    def select(self, folder, readonly=False):
                        self.folder = folder.strip('"')
                        calls.append(('EXAMINE', self.folder, readonly))
                        return 'OK', []
                    def response(self, kind):
                        calls.append(('UIDVALIDITY', self.namespace[self.folder]))
                        return kind, [str(self.namespace[self.folder]).encode()]
                    def uid(self, command, uid, query):
                        calls.append(('FETCH', uid, self.namespace[self.folder], query))
                        if uid == '7002' and transient[0]:
                            transient[0] = False
                            raise OSError('synthetic disconnect')
                        raw = messages[uid]
                        if 'RFC822.SIZE' in query:
                            return 'OK', [f'1 (UID {uid} RFC822.SIZE {len(raw)})'.encode()]
                        return 'OK', [(f'1 (UID {uid} BODY[] {{{len(raw)}}}'.encode(), raw), b')']
                    def logout(self):
                        calls.append(('LOGOUT',))
                        return 'BYE', []

                with patch('insights.attachment_fetcher.imaplib.IMAP4_SSL', MemoryIMAP), patch('insights.attachment_fetcher.time.sleep'):
                    result = download(directory/'source.json', directory/'service.json', directory/'files', workers=1)
                self.assertEqual((result['ready'], result['failed']), (ready, failed))
                self.assertEqual(sum(c[0] == 'EXAMINE' for c in calls), selects)
                self.assertTrue(all(c[2] is True for c in calls if c[0] == 'EXAMINE'))
                expected_epochs = {str(m['mail_pk']): m['raw_payload']['imap_uidvalidity'] for m in mails}
                self.assertTrue(all(c[2] == expected_epochs[c[1]] for c in calls if c[0] == 'FETCH'))
                manifest = json.loads((directory/'files/manifest.json').read_text('utf-8'))
                for key, item in manifest['files'].items():
                    if item['status'] == 'ready':
                        self.assertTrue(item['identity_verified'])
                        self.assertEqual(item['uidvalidity'], expected_epochs[key])
                    else:
                        self.assertEqual(item['error'], 'UIDVALIDITY_MISMATCH')
                        self.assertFalse(item.get('identity_verified', False))
                        self.assertFalse((directory/'files'/(key+'.bin')).exists())

    def test_jpeg_without_extension_or_image_mime_still_gets_a_real_preview(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'.runtime') as temp:
            folder=Path(temp)
            stream=BytesIO();Image.new('RGB',(8,6),'white').save(stream,format='JPEG');raw=stream.getvalue()
            (folder/'9.bin').write_bytes(raw)
            (folder/'manifest.json').write_text(json.dumps({'source_snapshot_sha256':'fixture',
                'files':{'9':{'status':'ready','identity_verified':True,'size':len(raw),'sha256':sha256(raw).hexdigest()}}}),encoding='utf-8')
            result=prepare_files(folder,[{'payload':{'id':9,'message_pk':1,'filename':'opaque-name',
                'size_bytes':len(raw),'content_type':'application/octet-stream'}}],snapshot_sha256='fixture')[0]
            self.assertEqual(result['content_type'],'application/octet-stream')
            self.assertEqual(result['detected_content_type'],'image/jpeg')
            self.assertEqual((result['kind'],result['preview_type']),('image','image'))
            with Image.open(folder/'9.jpg') as preview:self.assertEqual(preview.size,(8,6))

    def test_imap_is_readonly_identity_checked_and_resume_does_not_refetch(self):
        message=EmailMessage();message['Message-ID']='<fixture@invalid>';message['From']='sender@example.invalid'
        message.set_content('UID: 300000000001')
        payload=b'fixture log\n'
        message.add_attachment(payload,maintype='application',subtype='octet-stream',filename='client.log')
        raw=message.as_bytes()
        attachment_id='imap-17-2-'+sha1(payload).hexdigest()[:16]
        expected={'id':9,'message_pk':1,'attachment_id':attachment_id,'filename':'client.log','size_bytes':len(payload),'content_type':'application/octet-stream'}
        self.assertEqual(mime_attachments(raw,17,[expected],'<fixture@invalid>')['9'],payload)
        with self.assertRaises(ValueError):mime_attachments(raw,17,[expected],'<different@invalid>')
        calls=[]
        class FakeIMAP:
            def __init__(self,*args,**kwargs):calls.append(('TLS',kwargs.get('ssl_context') is not None))
            def login(self,*args):return 'OK',[]
            def select(self,folder,readonly=False):calls.append(('EXAMINE',readonly));return 'OK',[b'1']
            def response(self,kind):return kind,[b'1']
            def uid(self,command,uid,query):
                calls.append((command,query))
                return ('OK',[b'1 (UID 17 RFC822.SIZE '+str(len(raw)).encode()+b')']) if 'RFC822.SIZE' in query else ('OK',[(b'1 (UID 17 BODY[] {1}',raw),b')'])
            def logout(self):return 'BYE',[]
        with tempfile.TemporaryDirectory(dir=ROOT/'.runtime') as temp:
            folder=Path(temp);snapshot=folder/'snapshot.json';service=folder/'service.json'
            snapshot.write_text(json.dumps({'source_id':'fixture','business_date':'2026-10-29','attachments':[{'payload':expected}],
                'mails':[{'mail_pk':1,'mailbox':'box@example.invalid','smtp_message_id':'<fixture@invalid>',
                          'raw_payload':{'imap_uid':17,'imap_uidvalidity':1,'imap_folder':'INBOX'}}]}),encoding='utf-8')
            service.write_text(json.dumps({'host':'imap.feishu.cn','port':993,'accounts':{'box@example.invalid':'fixture-secret'}}),encoding='utf-8')
            with patch('insights.attachment_fetcher.imaplib.IMAP4_SSL',FakeIMAP):
                result=download(snapshot,service,folder/'copies')
            self.assertEqual(result['ready'],1)
            self.assertIn(('EXAMINE',True),calls)
            self.assertIn(('FETCH','(UID BODY.PEEK[])'),calls)
            with patch('insights.attachment_fetcher.imaplib.IMAP4_SSL',side_effect=AssertionError('resume connected')):
                self.assertEqual(download(snapshot,service,folder/'copies')['ready'],1)
            self.assertEqual((folder/'copies/9.bin').read_bytes(),payload)


class DailyBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'.runtime');self.addCleanup(self.temp.cleanup)
        self.folder=Path(self.temp.name);self.path=self.folder/'report.json'
        self.file_dir=self.folder/'attachments';self.file_dir.mkdir()
        (self.file_dir/'9.bin').write_bytes(b'<script>never execute</script>')
        (self.file_dir/'9.txt').write_text('safe log preview',encoding='utf-8')
        self.path.write_text(json.dumps({'coverage':{'expected':1},'records':[{'id':'1','summary':'fixture summary',
            'body':'private original','body_zh':'private translation','source_summary':'source summary',
            'files':[{'id':'9','ready':True,'preview_type':'text','name':'untrusted.html','content_type':'text/html'}]}]}),encoding='utf-8')

    def client(self,**kwargs):
        return TestClient(create_app(self.path),base_url='http://127.0.0.1:3030',client=kwargs.pop('client',('127.0.0.1',1234)),**kwargs)

    def test_loopback_host_origin_read_only_and_disabled_feature(self):
        c=self.client()
        self.assertEqual(c.get('/data.json').status_code,200)
        self.assertEqual(c.get('/data.json',headers={'Host':'malicious.example'}).status_code,403)
        self.assertEqual(c.get('/data.json',headers={'Origin':'https://malicious.example'}).status_code,403)
        self.assertEqual(self.client(client=('10.8.61.201',1234)).get('/data.json',headers={'X-Forwarded-For':'127.0.0.1'}).status_code,403)
        self.assertEqual(c.post('/data.json').status_code,405)
        with patch.dict('os.environ',{'INSIGHTS_DAILY_BOARD_ENABLED':'0'}):self.assertEqual(c.get('/').status_code,503)

    def test_overview_omits_full_text_but_detail_and_opaque_allowlist_work(self):
        c=self.client();r=c.get('/data.json')
        self.assertNotIn('body',r.json()['records'][0])
        self.assertEqual(c.get('/mail/1').json()['body'],'private original')
        self.assertEqual(c.get('/mail/2').status_code,404)
        self.assertEqual(c.get('/file/9/preview').text,'safe log preview')
        response=c.get('/file/9')
        self.assertIn('attachment',response.headers['content-disposition'])
        self.assertEqual(response.headers['content-type'],'application/octet-stream')
        self.assertIn('sandbox',response.headers['content-security-policy'])
        self.assertEqual(c.get('/file/999').status_code,404)
        self.assertEqual(c.get('/file/9%2f..%2fsecret').status_code,404)
        self.assertEqual(r.headers['cache-control'],'no-store')
        self.assertEqual(r.headers['x-content-type-options'],'nosniff')

    def test_pdf_preview_serves_only_the_prepared_first_page_image(self):
        doc = json.loads(self.path.read_text('utf-8'))
        doc['records'][0]['files'][0].update(preview_type='pdf', preview_image=True,
                                           content_type='application/pdf', name='fixture.pdf')
        self.path.write_text(json.dumps(doc), encoding='utf-8')
        Image.new('RGB', (8, 6), 'white').save(self.file_dir/'9.pdf.jpg', format='JPEG')
        response = self.client().get('/file/9/preview')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'image/jpeg')
        self.assertEqual(response.content, (self.file_dir/'9.pdf.jpg').read_bytes())

    def test_missing_or_incomplete_model_fails_without_loading_a_database(self):
        self.path.unlink()
        self.assertEqual(self.client().get('/data.json').status_code,503)
        self.path.write_text(json.dumps({'coverage':{'expected':2},'records':[]}),encoding='utf-8')
        self.assertEqual(self.client().get('/data.json').status_code,503)


if __name__=='__main__':
    unittest.main()
