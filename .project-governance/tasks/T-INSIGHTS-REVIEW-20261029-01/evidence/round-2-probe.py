"""Independent round 2: only test databases are writable; no sensitive outputs."""
from __future__ import annotations
import asyncio
from contextlib import contextmanager
from dataclasses import asdict, replace
from datetime import datetime, timezone
import hashlib
import json
import logging
from pathlib import Path
import ssl
import subprocess
import sys
import uuid
from urllib.parse import quote, urlsplit, urlunsplit
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
import psycopg
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict
from psycopg._conninfo_utils import get_param
from psycopg.rows import dict_row
from fastapi.testclient import TestClient
import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client
from starlette.responses import JSONResponse
from starlette.testclient import TestClient as ASGIClient
from insights.api import create_app
from insights.config import Settings, connection_identity
from insights.db import source_connection, target_connection
from insights.initialize import initialize_database
from insights.source import TABLES, schema_of
from insights.syncer import sync_once
from insights.mcp_http import MCPAccessMiddleware, MCPSettings
from insights.mcp_server import create_server
from tests.test_integration import DatabaseTests

logging.disable(logging.CRITICAL)
OUT = Path(__file__).with_name('round-2-results.json')
result = {'started_at': datetime.now(timezone.utc).isoformat(), 'checks': [], 'findings': []}

def check(name, condition, actual=None, expected=None):
    record = {'name': name, 'passed': bool(condition)}
    if actual is not None: record['actual'] = actual
    if expected is not None: record['expected'] = expected
    result['checks'].append(record)
    print(json.dumps({'check': name, 'passed': bool(condition)}), flush=True)
    return bool(condition)

def phase(name, action):
    try:
        action()
    except Exception as error:
        check(name + ':execution', False, {'error_type': type(error).__name__})
        # Exception strings and tracebacks may contain customer data or DSNs.

def dburl(url, name):
    p = urlsplit(url)
    return urlunsplit((p.scheme, p.netloc, '/' + name, p.query, p.fragment))

def baseline():
    p = ROOT/'LG_project_docs/requirements/T-INSIGHTS-REVIEW-20261029-01/verification/delivery-manifest.json'
    m = json.loads(p.read_text(encoding='utf-8-sig'))
    mismatches = [n for n, h in m['files'].items() if hashlib.sha256((ROOT/n).read_bytes()).hexdigest() != h]
    result['baseline'] = {'files': len(m['files']), 'mismatches': mismatches, 'manifest_sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
    check('baseline-63-files', len(m['files']) == 63 and not mismatches, result['baseline'])

def hashes(conn, query, args=()):
    digest, count = hashlib.sha256(), 0
    with conn.cursor(name='round2_' + uuid.uuid4().hex[:8]) as cur:
        cur.itersize = 500
        cur.execute(query, args)
        for row in cur:
            key, body = (row['record_key'], row['payload']) if isinstance(row, dict) else row
            digest.update(json.dumps([key, body], ensure_ascii=False, separators=(',', ':')).encode())
            digest.update(b'\n')
            count += 1
    return {'count': count, 'sha256': digest.hexdigest()}

def actual_parity():
    s = Settings.load()
    rows = []
    with source_connection(s) as src, target_connection(s, reader=True) as dst:
        check('real-source-transaction-readonly', src.execute('SHOW transaction_read_only').fetchone()['transaction_read_only'] == 'on')
        for t in TABLES:
            source_payload = sql.SQL("to_jsonb(t) - 'last_fetched_at'") if t.name == 'messages' else sql.SQL('to_jsonb(t)')
            mirror_payload = sql.SQL("payload - 'last_fetched_at'") if t.name == 'messages' else sql.SQL('payload')
            a = hashes(src, sql.SQL('SELECT {}::text AS record_key,({})::text AS payload FROM {}.{} t ORDER BY {}::text').format(sql.Identifier(t.key), source_payload, sql.Identifier(schema_of(s,t)), sql.Identifier(t.name), sql.Identifier(t.key)))
            b = hashes(dst, sql.SQL('SELECT record_key,({})::text AS payload FROM analysis.v_source_records WHERE source_id=%s AND source_table=%s AND deleted_at IS NULL ORDER BY record_key').format(mirror_payload), (s.source_id, t.name))
            rows.append({'table': t.name, 'source': a, 'mirror': b, 'equal': a == b})
        files = dst.execute('SELECT filename,sha256 FROM analysis.catalog_files WHERE source_id=%s ORDER BY filename', (s.source_id,)).fetchall()
        check('three-catalog-files-byte-hashes', len(files) == 3 and all(hashlib.sha256((s.catalog_path/r['filename']).read_bytes()).hexdigest() == r['sha256'] for r in files), {'count': len(files)})
        status = dst.execute('SELECT source_id,status,data_version FROM analysis.v_sync_status WHERE source_id=%s', (s.source_id,)).fetchone()
        check('real-source-ready', status['status'] == 'READY' and status['data_version'] > 0, status)
    result['real_parity'] = rows
    check('all-14-current-source-row-sha256', len(rows) == 14 and all(r['equal'] for r in rows), {'tables': len(rows), 'equal': sum(r['equal'] for r in rows)})

class Fixture:
    def __init__(self):
        self.base = Settings.load()
        suffix = uuid.uuid4().hex[:12]
        self.names = ['complaint_insights_r2_source_test_' + suffix, 'complaint_insights_r2_target_test_' + suffix]
        self.s = replace(self.base, source_id='r2-fixture', source_url=dburl(self.base.target_owner_url, self.names[0]), target_owner_url=dburl(self.base.target_owner_url, self.names[1]), target_writer_url=dburl(self.base.target_writer_url, self.names[1]), target_reader_url=dburl(self.base.target_reader_url, self.names[1]), auxiliary_seconds=3600, reconcile_seconds=86400)
        self.created = []

    def __enter__(self):
        self.s.validate(source=True)
        with psycopg.connect(self.base.target_owner_url, autocommit=True) as c:
            assert c.info.host == '127.0.0.1' and c.info.port == 15433
            for name in self.names:
                assert name.startswith('complaint_insights_r2_') and '_test_' in name
                c.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(name)))
                self.created.append(name)
        # Reuse schema fixture only. Do not run its setUpClass or any old probes.
        with self.write() as c:
            DatabaseTests.create_fixture_schema(c)
        skipped = []
        class Proxy:
            def __init__(self, c): self.c = c
            def __getattr__(self, k): return getattr(self.c, k)
            def execute(self, q, args=()):
                text = q if isinstance(q, str) else q.as_string(self.c)
                if text.startswith('ALTER ROLE '):
                    skipped.append(text.split()[2])
                    return self.c.execute('SELECT 1')
                if text.startswith('CREATE ROLE '):
                    raise RuntimeError('fixture must not change cluster authentication')
                return self.c.execute(q, args)
        @contextmanager
        def isolated_target(s, **kwargs):
            with target_connection(s, **kwargs) as c:
                assert c.info.dbname == self.names[1] and c.info.port == 15433
                yield Proxy(c)
        passwords = {urlsplit(v).username: urlsplit(v).password for v in [self.base.target_writer_url, self.base.target_reader_url]}
        with patch('insights.initialize.target_connection', isolated_target):
            initialize_database(self.s, passwords)
        result['fixture'] = {'databases': self.names, 'cluster_role_mutations_skipped': len(skipped), 'test_only': True}
        self.client = TestClient(create_app(self.s))
        self.auth = {'Authorization': 'Bearer ' + self.s.api_token}
        return self

    def __exit__(self, *args):
        self.client.close()
        with psycopg.connect(self.base.target_owner_url, autocommit=True) as c:
            assert c.info.host == '127.0.0.1' and c.info.port == 15433
            for name in self.created:
                assert name in self.names and '_test_' in name
                c.execute(sql.SQL('DROP DATABASE {} WITH (FORCE)').format(sql.Identifier(name)))
        result['fixture']['destroyed'] = len(self.created)

    def write(self):
        c = psycopg.connect(self.s.source_url)
        assert c.info.dbname == self.names[0] and c.info.port == 15433
        return c

    def owner(self):
        return target_connection(self.s, owner=True)

    def get(self, path, **params):
        r = self.client.get(path, params=params, headers=self.auth)
        assert r.status_code == 200
        return r.json()

    def state(self):
        with target_connection(self.s, reader=True) as c:
            return c.execute('SELECT * FROM analysis.v_sync_status WHERE source_id=%s', (self.s.source_id,)).fetchone()

    def add(self, c, pk, instant='2026-10-01T16:00:00Z', folder='INBOX', header=None):
        c.execute("INSERT INTO public.messages(id,mailbox_id,message_id,folder_id,subject,from_address,internal_date,date_header,first_seen_at,body_plain_text,body_html,raw_payload) VALUES(%s,1,%s,%s,'synthetic r2','synthetic@example.invalid',%s,%s,%s,'synthetic body','<p>synthetic body</p>','{\"fixture\":\"r2\"}')", (pk,'synthetic-r2-' + str(pk),folder,instant,header,instant))

    def ai(self,c,pk,category='ACC.LINKNEW', state='DONE', source='AI'):
        c.execute('INSERT INTO complaint_app."InboundMail"(id,"sourcePk") VALUES(%s,%s)', ('r2-mail-' + str(pk), pk))
        c.execute('INSERT INTO complaint_app."MailAiArtifact"(id,"inboundMailId","categoryAi",category,"categorySource","analysisState","analysisVersion","bodyOriginal","bodyTranslated") VALUES(%s,%s,\'ACC.OTHER\',%s,%s,%s,\'r2-v1\',\'["synthetic original"]\',\'["synthetic translation"]\')', ('r2-ai-' + str(pk), 'r2-mail-' + str(pk),category,source,state))

    def binding(self,c,pk,point,one='ACC',two='ACC.LINKNEW',kind='ADJ-ACC-01',source='AI',primary=False):
        c.execute('INSERT INTO complaint_app."MailIssueBinding"(id,"mailAiArtifactId","issuePointKey","levelOne","levelTwo","catalogIssueTypeId",source,"isPrimary","bindingStatus") VALUES(%s,%s,%s,%s,%s,%s,%s,%s,\'BOUND\')', ('r2-binding-' + str(pk) + '-' + point,'r2-ai-' + str(pk),point,one,two,kind,source,primary))

    def seed(self):
        with self.write() as c:
            c.execute("INSERT INTO public.mailboxes VALUES(1,'r2@example.invalid')")
            c.execute("INSERT INTO public.folders VALUES(1,1,'INBOX','synthetic inbox')")
            self.add(c,10,'2026-10-01T15:59:59Z')
            self.add(c,11)
            self.add(c,12,'2026-10-02T00:01:00Z',header='Thu, 01 Oct 2026 16:01:00 +0000')
            for pk,folder in [(13,'Sent'),(14,'草稿箱'),(15,'已删除'),(16,'垃圾邮件')]: self.add(c,pk,folder=folder)
            self.add(c,17,None)
            self.add(c,9007199254740993)
            self.ai(c,10)
            self.binding(c,10,'a',primary=True)
            self.binding(c,10,'b',kind='ADJ-ACC-03')
            self.ai(c,11,'PAY.OTHER',source='MANUAL')
            self.binding(c,11,'manual','PAY','PAY.OTHER','synthetic-manual','MANUAL',True)
            self.binding(c,11,'ai',primary=False)
            self.ai(c,12,state='PENDING')
            self.binding(c,12,'partial',primary=True)
            self.ai(c,123456)
            c.execute("INSERT INTO public.attachments VALUES(7,11,'synthetic.txt','done')")
            c.execute("INSERT INTO public.imap_reconcile_archive VALUES(9999,11,'{\"synthetic\":true}','{}','synthetic')")
            c.execute('INSERT INTO complaint_app."TaxonomyCandidate"(id,name,"levelOne","levelTwo",status) VALUES(\'r2-candidate\',\'synthetic candidate\',\'ACC\',\'ACC.LINKNEW\',\'PENDING\')')
            c.execute('INSERT INTO complaint_app."IssueTypeProposal"(id,"mailAiArtifactId","candidateId") VALUES(\'r2-proposal\',\'r2-ai-10\',\'r2-candidate\')')
            c.execute('INSERT INTO complaint_app."TaxonomyCandidateSupport"(id,"candidateId","mailAiArtifactId") VALUES(\'r2-support\',\'r2-candidate\',\'r2-ai-10\')')
            c.execute('INSERT INTO complaint_app."IssueTypeRegistry" VALUES(\'r2-legacy\',\'synthetic legacy\',\'ACC.OTHER\',\'ACTIVE\')')
            c.execute('INSERT INTO complaint_app."IssueTypeAlias" VALUES(\'r2-alias\',\'r2-legacy\',\'synthetic alias\')')
            c.execute('INSERT INTO complaint_app."IssueGroupLifecycle" VALUES(\'r2-group\',NULL)')
        r=sync_once(self.s)
        check('fixture-initial-14-tables',len(r['tables'])==14 and all(v['scanned']>0 for v in r['tables'].values()), {'tables':len(r['tables'])})

    def pagination(self,path,params,key):
        got, cursor = [], None
        for index in range(300):
            page=self.get(path,**params,limit=1 if index%2==0 else 3,**({'cursor':cursor} if cursor else {}))
            got.extend(key(item) for item in page['items'])
            cursor=page['next_cursor']
            if cursor is None: return got
        raise AssertionError('pagination did not terminate')

    def reads(self):
        rows=self.get('/v1/mails')['items']
        bypk={r['mail_pk']:r for r in rows}
        check('beijing-midnight-and-per-row-legacy-offset', [bypk[k]['business_date'] for k in ['10','11','12']]==['2026-10-01','2026-10-02','2026-10-02'] and bypk['12']['time_shift_hours']==8)
        check('all-current-mail-retained-null-date-bigint-and-direction',len(rows)==9 and bypk['17']['business_date'] is None and bypk['13']['direction']=='SENT' and bypk['14']['direction']=='EXCLUDED' and bypk['15']['direction']=='EXCLUDED' and bypk['16']['direction']=='RECEIVED',{'count':len(rows)})
        detail=self.get('/v1/mails/11',include_raw=True)
        check('manual-classification-excluded-raw-ai-retained',detail['mail']['level_one']=='ACC' and detail['mail']['category_ai']=='ACC.OTHER' and detail['mail']['category_normalized']=='ACC.OTHER' and len(detail['issue_bindings'])==1 and detail['issue_bindings'][0]['definition']['source']=='AI')
        check('full-original-ai-html-and-attachment-metadata',all(k in detail['mail'] for k in ['body_plain_text','body_html','raw_record','ai_record','ai_body_original','body_translated']) and len(detail['attachments'])==1)
        check('incomplete-ai-keeps-pending-bucket',bypk['12']['level_one']=='PEND' and bypk['12']['analysis_state']=='PENDING')
        daily=self.get('/v1/daily',start='2026-10-01',end='2026-10-02',scope='all_issues',level=1)['items']
        acc=next(r for r in daily if r['level_one']=='ACC')
        check('all-issues-parent-dedup-and-exclusive-end',len(daily)==1 and acc['mail_count']==1 and acc['issue_count']==2,{'rows':len(daily),'mail_count':acc['mail_count'],'issue_count':acc['issue_count']})
        ordinary=self.get('/v1/report-context',start='2026-10-01',end='2026-10-04')
        bodies=self.get('/v1/report-context',start='2026-10-01',end='2026-10-04',include_body=True)
        flatten=lambda p:[m for d in p['days'] for cat in d['categories'] for m in cat['mails']]
        check('report-date-category-structure-and-explicit-body','body_plain_text' not in flatten(ordinary)[0] and 'body_plain_text' in flatten(bodies)[0] and all(d['date']<'2026-10-04' for d in bodies['days']))
        keys=self.pagination('/v1/mails',{},lambda r:r['mail_pk'])
        check('mails-pagination-null-date-and-bigint-lossless',len(keys)==9 and len(set(keys))==9 and keys[-1]=='17' and '9007199254740993' in keys)
        tkeys=self.pagination('/v1/taxonomy',{},lambda r:r['category_id'])
        check('taxonomy-pagination-retains-dynamic-and-legacy',len(tkeys)==len(set(tkeys)) and 'r2-candidate' in tkeys and 'r2-legacy' in tkeys,{'categories':len(tkeys)})
        tables=self.get('/v1/source-tables')['items']
        allkeys={t['table']:self.pagination('/v1/source-records',{'table':t['table']},lambda r:r['record_key']) for t in tables}
        check('all-14-source-record-pagination-including-orphan-ai',len(allkeys)==14 and all(allkeys.values()) and 'r2-ai-123456' in allkeys['MailAiArtifact'])
        for table,keys in allkeys.items():
            p=self.get('/v1/source-records',table=table,record_key=keys[0],include_payload=True)
            assert len(p['items'])==1 and 'payload' in p['items'][0]
        check('all-14-complete-source-record-payloads',True)
        invalid=[('/v1/daily',{'start':'2026-10-02','end':'2026-10-02'}),('/v1/mails',{'limit':0}),('/v1/mails',{'direction':'DROP'}),('/v1/source-records',{'table':'messages; DROP TABLE x'}),('/v1/mails/9223372036854775808',{}),('/v1/source-records',{'table':'messages','limit':51})]
        statuses=[self.client.get(p,params=a,headers=self.auth).status_code for p,a in invalid]
        check('api-parameter-rejection',all(s==422 for s in statuses),statuses)
        protected=['/health','/openapi.json','/v1/source-tables','/v1/source-records?table=messages','/v1/mails','/v1/sync/status']
        check('api-auth-all-registered-query-types',all(self.client.get(p).status_code==401 and self.client.get(p,headers={'Authorization':'Bearer bad'}).status_code==401 for p in protected))
        check('api-no-write-method',self.client.post('/v1/mails',headers=self.auth).status_code==405)
        check('sql-injection-value-is-data',self.get('/v1/mails',level_one="ACC' OR true--")['items']==[])
        archived=self.client.get('/v1/mails/9999',headers=self.auth)
        check('archive-not-double-counted-and-410',archived.status_code==410 and len(rows)==9)
        offline=TestClient(create_app(replace(self.s,source_url='postgresql://unavailable@127.0.0.1:1/offline')))
        check('query-uses-target-with-source-disconnected',offline.get('/v1/mails/11',headers=self.auth).status_code==200)
        offline.close()
        check('api-capability-parent-chain-and-disabled-source',not self.get('/v1/capabilities',source_id='r2-missing')['capabilities']['mails']['enabled'])

    def privileges(self):
        blocked=[]
        for statement in ['CREATE TEMP TABLE r2_forbidden(id int)','CREATE TABLE public.r2_forbidden(id int)','INSERT INTO analysis.mail_fact(source_id,mail_pk) SELECT \'x\',1 WHERE false','SELECT * FROM source_mail.messages LIMIT 0']:
            with target_connection(self.s,reader=True) as c:
                c.execute('SET TRANSACTION READ WRITE')
                try: c.execute(statement)
                except psycopg.errors.InsufficientPrivilege: blocked.append(True); c.rollback()
                else: blocked.append(False)
        check('sql-reader-privileges-after-readonly-disabled',all(blocked),blocked)
        try:
            with source_connection(self.s) as c: c.execute("INSERT INTO public.mailboxes VALUES(999,'forbidden@example.invalid')")
        except psycopg.errors.ReadOnlySqlTransaction: check('source-connection-write-blocked',True)
        else: check('source-connection-write-blocked',False)

    def mutations(self):
        shadow=replace(self.s,source_id='r2-shadow')
        sync_once(shadow)
        first=self.get('/v1/mails',limit=1)
        foreign=self.client.get('/v1/mails',params={'source_id':shadow.source_id,'cursor':first['next_cursor']},headers=self.auth)
        changedfilter=self.client.get('/v1/mails',params={'direction':'RECEIVED','cursor':first['next_cursor']},headers=self.auth)
        check('cursor-source-and-filter-binding',foreign.status_code==422 and changedfilter.status_code==422)
        with target_connection(self.s,reader=True) as snap:
            old=snap.execute('SELECT data_version FROM analysis.v_sync_status WHERE source_id=%s',(self.s.source_id,)).fetchone()['data_version']
            with self.write() as c:
                self.add(c,20,'2026-10-03T16:00:00Z')
                c.execute("UPDATE public.messages SET body_plain_text='r2 changed synthetic' WHERE id=11")
                c.execute('DELETE FROM public.messages WHERE id=13')
            synced=sync_once(replace(self.s))
            same=snap.execute('SELECT data_version FROM analysis.v_sync_status WHERE source_id=%s',(self.s.source_id,)).fetchone()['data_version']
            check('sql-repeatable-read-retains-published-snapshot',same==old and synced['data_version']>old)
        check('event-incremental-iud',synced['mode']=='INCREMENTAL' and self.get('/v1/mails/11')['mail']['body_plain_text']=='r2 changed synthetic' and self.client.get('/v1/mails/13',headers=self.auth).status_code==404)
        check('cursor-version-conflict',self.client.get('/v1/mails',params={'cursor':first['next_cursor']},headers=self.auth).status_code==409)
        check('source-namespace-no-cross-update',self.get('/v1/mails/11',source_id='r2-shadow')['mail']['body_plain_text']=='synthetic body')
        tombstone=self.get('/v1/source-records',table='messages',record_key='13',include_deleted=True,include_payload=True)['items'][0]
        check('deleted-source-tombstone-keeps-original-payload',tombstone['deleted_at'] is not None and tombstone['payload']['id']==13)
        stable=sync_once(self.s)
        check('empty-poll-no-version-increase',stable['changed_rows']==0 and stable['data_version']==synced['data_version'])
        with self.write() as c:
            c.execute('UPDATE complaint_app."MailAiArtifact" SET "analysisState"=\'DONE\',category=\'PAY.OTHER\' WHERE id=\'r2-ai-12\'')
            c.execute('DELETE FROM complaint_app."MailIssueBinding" WHERE "mailAiArtifactId"=\'r2-ai-12\'')
        sync_once(self.s)
        check('late-ai-completion-original-business-day',self.get('/v1/mails/12')['mail']['business_date']=='2026-10-02' and self.get('/v1/mails/12')['mail']['level_one']=='PAY')
        with self.write() as c:
            c.execute("UPDATE public.attachments SET download_status='r2-new-state' WHERE id=7")
            c.execute('UPDATE complaint_app."TaxonomyCandidate" SET status=\'ARCHIVED\' WHERE id=\'r2-candidate\'')
            c.execute('DELETE FROM complaint_app."IssueTypeAlias" WHERE id=\'r2-alias\'')
        with self.owner() as c: c.execute("UPDATE sync.sources SET last_aux_at=clock_timestamp()-interval '2 hours' WHERE source_id=%s",(self.s.source_id,))
        aux=sync_once(self.s)
        check('no-event-aux-update-delete-and-catalog-state',aux['mode']=='INCREMENTAL' and self.get('/v1/mails/11')['attachments'][0]['download_status']=='r2-new-state' and self.get('/v1/taxonomy',status='ARCHIVED')['items'][0]['category_id']=='r2-candidate' and self.get('/v1/source-records',table='IssueTypeAlias')['items']==[])
        delayed=self.write()
        try:
            self.add(delayed,21)
            with self.write() as c: self.add(c,22)
            sync_once(self.s)
            absent=self.client.get('/v1/mails/21',headers=self.auth).status_code==404
            delayed.commit()
            sync_once(self.s)
            check('late-commit-new-counterexample',absent and self.client.get('/v1/mails/21',headers=self.auth).status_code==200)
        finally: delayed.close()
        delayed=self.write()
        try:
            self.add(delayed,23)
            with self.write() as c: c.execute("INSERT INTO public.message_change_log(id,message_pk,operation) VALUES(1000000,11,'U')")
            sync_once(self.s)
            delayed.commit()
            nofull=sync_once(self.s)
            waits=self.client.get('/v1/mails/23',headers=self.auth).status_code==404
            with self.owner() as c: c.execute("UPDATE sync.sources SET last_reconcile_at=clock_timestamp()-interval '2 days' WHERE source_id=%s",(self.s.source_id,))
            recovered=sync_once(self.s)
            check('outside-tail-recovered-by-due-full-reconcile',nofull['mode']=='INCREMENTAL' and waits and recovered['mode']=='RECONCILE' and self.client.get('/v1/mails/23',headers=self.auth).status_code==200)
        finally: delayed.close()
        with self.write() as c:
            c.execute('TRUNCATE public.message_change_log RESTART IDENTITY')
            c.execute("UPDATE public.messages SET subject='synthetic after prune' WHERE id=10")
            c.execute('DELETE FROM public.messages WHERE id=22')
        pruned=sync_once(self.s)
        check('pruned-reset-log-full-recovery',pruned['mode']=='RECONCILE' and self.client.get('/v1/mails/22',headers=self.auth).status_code==404 and self.get('/v1/mails/10')['mail']['subject']=='synthetic after prune')
        before=self.state()
        with self.write() as c: self.add(c,24)
        failed=False
        try: sync_once(self.s,fail_before_publish=True)
        except RuntimeError: failed=True
        after=self.state()
        check('atomic-failure-no-data-or-watermark-publish',failed and after['data_version']==before['data_version'] and after['source_event_id']==before['source_event_id'] and after['status']=='DEGRADED' and self.client.get('/v1/mails/24',headers=self.auth).status_code==404)
        child="import json,sys;from insights.config import Settings;from insights.syncer import sync_once;s=Settings(**json.loads(sys.stdin.read()));r=sync_once(s);print(json.dumps({k:r[k] for k in ['status','data_version','mode','changed_rows']}))"
        p=subprocess.run([sys.executable,'-c',child],input=json.dumps(asdict(self.s)),capture_output=True,text=True,cwd=ROOT)
        child_result=json.loads(p.stdout) if p.returncode==0 else {'error_type':'child_failed'}
        check('fresh-process-restart-resumes-persisted-watermark',p.returncode==0 and child_result['status']=='READY' and self.client.get('/v1/mails/24',headers=self.auth).status_code==200,child_result)
        before=self.state()
        try: sync_once(replace(self.s,catalog_dir=str(ROOT/'.runtime'/('missing-r2-'+uuid.uuid4().hex))))
        except FileNotFoundError: pass
        after=self.state()
        check('missing-catalog-degraded-preserves-published-version',after['status']=='DEGRADED' and after['last_error_code']=='FileNotFoundError' and after['data_version']==before['data_version'])
        sync_once(self.s)
        check('catalog-restoration-recovers-ready',self.state()['status']=='READY')
        with self.write() as c: c.execute('ALTER TABLE complaint_app."MailAiArtifact" RENAME COLUMN "categoryAi" TO "r2_removed_ai"')
        before=self.state()
        failed=False
        try: sync_once(self.s)
        except RuntimeError: failed=True
        finally:
            with self.write() as c: c.execute('ALTER TABLE complaint_app."MailAiArtifact" RENAME COLUMN "r2_removed_ai" TO "categoryAi"')
        check('schema-contract-drift-stops-publication',failed and self.state()['data_version']==before['data_version'])
        sync_once(self.s)
        check('schema-contract-restoration-recovers',self.state()['status']=='READY')

    def destination_environment(self):
        parsed=urlsplit(self.s.source_url)
        missing=f'postgresql://{quote(parsed.username,safe="")}:{quote(parsed.password,safe="")}@/{self.names[0]}'
        candidate=replace(self.s,source_url=missing)
        with patch.dict('os.environ',{'PGHOST':'127.0.0.1','PGPORT':'15433'}):
            candidate.validate(source=True)
            identity=connection_identity(missing)
            with source_connection(candidate) as c:
                observed={'host':c.info.host,'port':str(c.info.port),'dbname':c.info.dbname}
            result['destination_environment']={'validated_identity':identity,'actual_local_connection':observed}
            reproduced=identity!=observed
            check('R2-01-implicit-environment-destination-reproduced',reproduced,result['destination_environment'])
        with patch.dict('os.environ',{'PGHOST':'203.0.113.1','PGPORT':'6543'}):
            no_password='postgresql://placeholder@/synthetic'
            replace(self.base,source_url=no_password).validate(source=True)
            params=conninfo_to_dict(no_password)
            result['destination_environment']['offline_remote_validation']={'accepted':True,'identity':connection_identity(no_password),'effective_host':get_param(params,'host'),'effective_port':get_param(params,'port'),'connection_attempted':False}
        if reproduced: result['findings'].append({'id':'R2-01','summary':'省略主机/端口时忽略 PGHOST/PGPORT 环境目的地址，生产门禁和来源绑定与实际连接脱离'})

async def remote():
    config=json.loads((ROOT/'.secrets/mcp-client.json').read_text(encoding='utf-8'))
    ca=ROOT/'config/mcp-ca.crt'
    ctx=ssl.create_default_context(cafile=str(ca))
    token=config['bearer_token']
    async with httpx2.AsyncClient(verify=ctx,headers={'Authorization':'Bearer '+token},trust_env=False,timeout=30) as http:
        async with Client(streamable_http_client(config['url'],http_client=http),read_timeout_seconds=35) as client:
            tools=(await client.list_tools()).tools
            expected={'get_data_guide','get_sync_status','get_capabilities','list_taxonomy','query_daily_statistics','list_mails','get_mail_detail','get_report_context','list_source_tables','list_source_records','get_source_record'}
            check('real-https-mcp-11-readonly-structured-tools',{t.name for t in tools}==expected and all(t.annotations.read_only_hint and not t.annotations.open_world_hint and t.output_schema for t in tools),{'count':len(tools)})
            called=[]
            async def call(name,arguments):
                r=await client.call_tool(name,arguments)
                assert not r.is_error
                called.append(name)
                return r.structured_content
            await call('get_data_guide',{})
            await call('get_sync_status',{})
            await call('get_capabilities',{})
            await call('list_taxonomy',{'limit':1})
            await call('query_daily_statistics',{'start':'2026-01-01','end':'2027-01-01','limit':1})
            mails=await call('list_mails',{'limit':1})
            await call('get_mail_detail',{'mail_pk':mails['items'][0]['mail_pk']})
            await call('get_report_context',{'start':'2026-01-01','end':'2027-01-01','limit':1})
            tables=await call('list_source_tables',{})
            source=await call('list_source_records',{'table':'messages','limit':1})
            await call('get_source_record',{'table':'messages','record_key':source['items'][0]['record_key']})
            check('real-https-all-11-tools-called',set(called)==expected,{'called':len(set(called)),'tables':len(tables['items'])})
            invalid=[('list_mails',{'limit':201}),('get_mail_detail',{'mail_pk':'../synthetic'}),('query_daily_statistics',{'start':'2026-10-02','end':'2026-10-01'}),('list_source_records',{'table':'HumanClassification'}),('list_mails',{'cursor':'synthetic-not-a-cursor'})]
            errors=[(await client.call_tool(n,a)).is_error for n,a in invalid]
            check('real-mcp-invalid-parameters-and-cursor',all(errors),{'rejected':sum(errors)})
            resource=await client.read_resource('complaint-insights://guide')
            check('real-mcp-guide-resource',json.loads(resource.contents[0].text)['timezone']=='Asia/Shanghai')
        tests=[('wrong-token',{'Authorization':'Bearer synthetic-wrong-token'}),('api-token-cannot-auth-mcp',{'Authorization':'Bearer '+Settings.load().api_token}),('bad-host',{'Host':'attacker.invalid:3037'}),('bad-origin',{'Origin':'https://attacker.invalid'}),('proxy-host-spoof',{'Host':'attacker.invalid:3037','X-Forwarded-Host':'10.8.61.200:3037'})]
        status={}
        payload={'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'r2-synthetic','version':'1'}}}
        for name,headers in tests:
            r=await http.post(config['url'],headers={**headers,'Accept':'application/json, text/event-stream'},json=payload)
            status[name]=r.status_code
        check('real-https-token-host-origin-and-proxy-host',status['wrong-token']==401 and status['api-token-cannot-auth-mcp']==401 and all(status[n] in (400,403,421) for n in ['bad-host','bad-origin','proxy-host-spoof']),status)
    async def ok(scope,receive,send): await JSONResponse({'ok':True})(scope,receive,send)
    settings=MCPSettings('10.8.61.200',3037,('10.8.0.0/16',),{'r2-synthetic':'x'*48},Path('unused'),Path('unused'),Path('unused'))
    middleware=MCPAccessMiddleware(ok,settings)
    auth={'Authorization':'Bearer '+'x'*48}
    inside=ASGIClient(middleware,base_url='https://10.8.61.200:3037',client=('10.8.9.17',40000))
    outside=ASGIClient(middleware,base_url='https://10.8.61.200:3037',client=('192.168.4.5',40000))
    plain=ASGIClient(middleware,base_url='http://10.8.61.200:3037',client=('10.8.9.17',40000))
    statuses=[inside.post('/mcp',headers=auth).status_code,outside.post('/mcp',headers={**auth,'Forwarded':'for=10.8.9.17;proto=https','X-Forwarded-For':'10.8.9.17','X-Real-IP':'10.8.9.17'}).status_code,plain.post('/mcp',headers={**auth,'X-Forwarded-Proto':'https'}).status_code]
    check('actual-peer-and-scheme-asgi-branch-tests',statuses==[200,403,403],statuses)
    async with httpx2.AsyncClient(verify=True,trust_env=False,timeout=10) as untrusted:
        rejected=False
        try: await untrusted.get(config['url'])
        except Exception as error: rejected='certificate' in str(error).lower() or 'ssl' in str(error).lower()
        check('server-private-ca-required',rejected)

def handoff():
    # Inspect archive names and safe hashes only, never persist or print token values.
    with zipfile.ZipFile(ROOT/'.secrets/mcp-handoff.zip') as z:
        names=set(z.namelist())
        expected={'mcp-client.json','mcp-client-config.json','mcp-ca.crt','mcp-endpoint.json','mcp_client.py','client-dependencies.txt','MCP使用说明.md','queries/daily.json','queries/mails.json','queries/context.json','queries/ai-records.json'}
        check('handoff-exact-11-allowlisted-files-and-integrity',names==expected and z.testzip() is None,{'count':len(names)})
        public={'mcp-ca.crt':'config/mcp-ca.crt','mcp-endpoint.json':'config/mcp-endpoint.json','mcp_client.py':'scripts/mcp_client.py','client-dependencies.txt':'client-dependencies.txt','MCP使用说明.md':'LG_project_docs/requirements/T-INSIGHTS-FOUNDATION-20261029-01/release/mcp-handoff.md'}
        check('handoff-public-file-hashes-current',all(hashlib.sha256(z.read(n)).digest()==hashlib.sha256((ROOT/p).read_bytes()).digest() for n,p in public.items()))
        local=json.loads((ROOT/'.secrets/mcp-client.json').read_text(encoding='utf-8'))
        portable=json.loads(z.read('mcp-client.json'))
        forbidden=['-----BEGIN PRIVATE KEY-----','-----BEGIN RSA PRIVATE KEY-----','postgresql://','readonly_database_url','target_writer_url','source_url']
        check('handoff-token-current-no-db-password-or-private-key',portable['bearer_token']==local['bearer_token'] and all(not any(b.encode() in z.read(n) for b in forbidden) for n in ['mcp-client.json','mcp-client-config.json']))
        pem=z.read('mcp-ca.crt').decode('ascii')
        endpoint=json.loads(z.read('mcp-endpoint.json'))
        result['handoff']={'file_count':len(names),'ca_der_sha256':hashlib.sha256(ssl.PEM_cert_to_DER_cert(pem)).hexdigest(),'endpoint_keys':list(endpoint)}
    production=json.loads((ROOT/'config/production.example.json').read_text(encoding='utf-8'))
    check('production-config-disabled-isolated-source-verify-full',not production['allow_production_read'] and production['source_id']!='development-local' and 'sslmode=verify-full' in production['source_url'] and bool(production['source_certificate_sha256']))

def main():
    phase('baseline',baseline)
    phase('actual-parity',actual_parity)
    f=None
    try:
        with Fixture() as f:
            phase('fixture-seed',f.seed)
            phase('fixture-reads',f.reads)
            phase('fixture-privileges',f.privileges)
            phase('fixture-mutations',f.mutations)
            phase('destination-environment',f.destination_environment)
    except Exception as e:
        check('fixture-lifecycle',False,{'error_type':type(e).__name__})
    phase('remote',lambda:asyncio.run(remote()))
    phase('handoff',handoff)
    phase('final-baseline',baseline)
    result['completed_at']=datetime.now(timezone.utc).isoformat()
    result['summary']={'passed':sum(c['passed'] for c in result['checks']),'checks':len(result['checks']),'failed_checks':[c['name'] for c in result['checks'] if not c['passed']],'findings':len(result['findings'])}
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
    print(json.dumps({'summary':result['summary'],'results_file':str(OUT)},ensure_ascii=False))

if __name__=='__main__': main()
