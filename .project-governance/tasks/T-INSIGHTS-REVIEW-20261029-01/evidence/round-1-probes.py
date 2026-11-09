from __future__ import annotations

import asyncio
from dataclasses import replace
from datetime import datetime, timezone
import hashlib
from importlib.metadata import metadata
import json
from pathlib import Path
import socket
import ssl
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client
import psycopg
from psycopg import sql

from insights.config import Settings
from insights.db import source_connection,target_connection
from insights.api import create_app
from insights.syncer import sync_once
from fastapi.testclient import TestClient
from tests.test_integration import DatabaseTests

OUTPUT=ROOT/'.runtime/review-one-results.json'
RESULT={'started_at':'2026-10-29T10:49:30Z','reviewer':'review_one','checks':{},'observations':{}}

def put(name,value):
    RESULT['checks'][name]=value
    print(json.dumps({'check':name,'result':value},ensure_ascii=False),flush=True)

def compare_live():
    setting=Settings.load()
    names=[('public','mailboxes','id'),('public','folders','id'),('public','messages','id'),('public','attachments','id'),('public','imap_reconcile_archive','old_message_pk'),('complaint_app','InboundMail','id'),('complaint_app','MailAiArtifact','id'),('complaint_app','MailIssueBinding','id'),('complaint_app','TaxonomyCandidate','id'),('complaint_app','IssueTypeProposal','id'),('complaint_app','TaxonomyCandidateSupport','id'),('complaint_app','IssueTypeRegistry','id'),('complaint_app','IssueTypeAlias','id'),('complaint_app','IssueGroupLifecycle','groupKey')]
    checks=[]
    with source_connection(setting) as src,target_connection(setting,reader=True) as dst:
        assert src.execute('SHOW transaction_read_only').fetchone()['transaction_read_only']=='on'
        for schema,table,key in names:
            data=sql.SQL("to_jsonb(t)-'last_fetched_at'") if table=='messages' else sql.SQL('to_jsonb(t)')
            q=sql.SQL("SELECT {}::text AS k,encode(sha256(convert_to(({})::text,'UTF8')),'hex') AS h FROM {}.{} t").format(sql.Identifier(key),data,sql.Identifier(schema),sql.Identifier(table))
            expected={r['k']:r['h'] for r in src.execute(q)}
            expression=sql.SQL("payload-'last_fetched_at'") if table=='messages' else sql.SQL('payload')
            q=sql.SQL("SELECT record_key AS k,encode(sha256(convert_to(({})::text,'UTF8')),'hex') AS h FROM analysis.v_source_records WHERE source_id=%s AND source_table=%s AND deleted_at IS NULL").format(expression)
            actual={r['k']:r['h'] for r in dst.execute(q,(setting.source_id,table))}
            assert actual==expected,table
            checks.append({'table':table,'rows':len(actual),'all_content_equal':True})
        RESULT['observations']['facts']=dst.execute("SELECT count(*) AS total,count(*) FILTER(WHERE direction='RECEIVED') AS received,min(business_date)::text AS first_date,max(business_date)::text AS last_date FROM analysis.mail_fact WHERE source_id=%s",(setting.source_id,)).fetchone()
        RESULT['observations']['reader_role']=dst.execute("SELECT current_user AS role,rolsuper,rolcreatedb,rolcreaterole,rolreplication,rolbypassrls,has_schema_privilege(current_user,'source_mail','USAGE') AS raw_schema,has_table_privilege(current_user,'analysis.mail_fact','INSERT') AS can_insert FROM pg_roles WHERE rolname=current_user").fetchone()
    put('independent_live_full_content',checks)

def isolated_probes():
    DatabaseTests.setUpClass()
    case=DatabaseTests('test_initial_import_counts_and_source_fields')
    try:
        case.setUp()
        s=case.settings
        assert ':15433/' in s.source_url and 'source_test_' in s.source_url
        # Move a business anchor rather than repeating a simple mail body update.
        case.source_write('UPDATE complaint_app."InboundMail" SET "sourcePk"=3 WHERE id=\'mail-1\'')
        sync_once(s)
        f={r['mail_pk']:r for r in case.facts()}
        assert f[1]['analysis_state']=='UNANALYZED' and f[3]['analysis_state']=='DONE'
        put('anchor_reassignment_updates_old_and_new_mail',True)

        case.setUp()
        # Source down while target remains reachable: old snapshot must stay readable,
        # no source watermarks advance, status must truthfully degrade and recover.
        previous=case.state()
        broken=replace(s,source_url='postgresql://unavailable@127.0.0.1:1/fixture')
        # Preserve identity to inject a connection outage after the identity guard.
        from unittest.mock import patch
        from insights import syncer
        original=syncer.source_connection
        def unavailable(settings):
            return original(broken)
        with patch('insights.syncer.source_connection',unavailable):
            try:
                sync_once(s)
                raise AssertionError('expected source outage')
            except psycopg.OperationalError:
                pass
        failed=case.state()
        RESULT['observations']['source_outage_status']={'status':failed['status'],'error_code':failed['last_error_code']}
        assert failed['status']=='DEGRADED' and failed['last_error_code'] in {'OperationalError','ConnectionTimeout','08001'}
        assert failed['data_version']==previous['data_version'] and failed['source_event_id']==previous['source_event_id']
        response=case.client().get('/v1/mails/1',headers=case.headers)
        assert response.status_code==200
        sync_once(replace(s))
        assert case.state()['status']=='READY'
        put('source_connection_outage_old_api_and_retry',True)

        case.setUp()
        with target_connection(s,reader=True) as snapshot:
            old=snapshot.execute('SELECT count(*) AS n FROM analysis.mail_fact').fetchone()['n']
            with psycopg.connect(s.source_url) as source:
                case.insert_mail(source,4)
            sync_once(s)
            still=snapshot.execute('SELECT count(*) AS n FROM analysis.mail_fact').fetchone()['n']
            assert old==still==3
        assert len(case.facts())==4
        put('sql_repeatable_read_survives_new_publication',True)

        case.setUp()
        # Same primary key removed and recreated; stale tombstone must not hide it.
        case.source_write('DELETE FROM public.messages WHERE id=1')
        sync_once(s)
        assert len(case.facts())==2
        with psycopg.connect(s.source_url) as source:
            case.insert_mail(source,1,day='2026-10-04T15:30:00Z')
        sync_once(s)
        recovered=case.client().get('/v1/source-records?table=messages&record_key=1&include_payload=true',headers=case.headers).json()['items'][0]
        assert recovered['deleted_at'] is None and len(case.facts())==3
        assert str(case.facts()[0]['business_date'])=='2026-10-04'
        put('delete_reinsert_revives_record_and_bucket',True)

        case.setUp()
        # Multi-issue parent summaries must equal a separate direct distinct-mail oracle.
        with psycopg.connect(s.source_url) as source:
            source.execute('''INSERT INTO complaint_app."MailIssueBinding"(id,"mailAiArtifactId","issuePointKey","catalogIssueTypeId","levelOne","levelTwo","isPrimary","bindingStatus") VALUES('review-second','ai-1','review-second','ADJ-ACC-03','ACC','ACC.LINKNEW',false,'BOUND'),('review-third','ai-1','review-third','review-pay','PAY','PAY.OTHER',false,'BOUND')''')
        sync_once(s,force_reconcile=True)
        api=case.client()
        expected={'ACC':1,'PAY':1,'PEND':1}
        rows=api.get('/v1/daily?start=2026-10-01&end=2026-10-03&level=1&scope=all_issues',headers=case.headers).json()['items']
        assert {r['level_one']:r['mail_count'] for r in rows}==expected
        for category in ['ACC','PAY','PEND']:
            mails=api.get('/v1/mails',params={'scope':'all_issues','direction':'RECEIVED','level_one':category},headers=case.headers).json()['items']
            assert len(mails)==expected[category]
            context=api.get('/v1/report-context',params={'start':'2026-10-01','end':'2026-10-03','scope':'all_issues','level_one':category},headers=case.headers).json()
            grouped={m['mail_pk'] for d in context['days'] for c in d['categories'] for m in c['mails']}
            assert grouped=={m['mail_pk'] for m in mails}
        put('all_issue_daily_list_context_differential',True)

        # Invalid and filter-rebound cursors are checked at every paginated API family.
        for endpoint,params in [('/v1/taxonomy',{'limit':1}),('/v1/daily',{'start':'2026-10-01','end':'2026-10-03','direction':'ALL','limit':1}),('/v1/mails',{'limit':1}),('/v1/report-context',{'start':'2026-10-01','end':'2026-10-03','direction':'ALL','limit':1}),('/v1/source-records',{'table':'messages','limit':1})]:
            first=api.get(endpoint,params=params,headers=case.headers).json()
            assert first['next_cursor']
            bad=api.get(endpoint,params={**params,'cursor':first['next_cursor']+'bad'},headers=case.headers)
            assert bad.status_code==422
            pages=[];cursor=None
            while True:
                response=api.get(endpoint,params={**params,**({'cursor':cursor} if cursor else {})},headers=case.headers)
                assert response.status_code==200
                body=response.json();pages.append(body);cursor=body['next_cursor']
                if cursor is None:break
                assert len(pages)<3000
        put('five_pagination_families_complete_and_reject_tamper',True)

        # Delayed app and mail transaction commits are independently repeated with
        # an interrupted worker between polls, not relying on any process cache.
        case.setUp()
        delayed=psycopg.connect(s.source_url)
        try:
            case.insert_mail(delayed,4)
            case.analyze(delayed,4)
            with psycopg.connect(s.source_url) as source:
                case.insert_mail(source,5)
                case.analyze(source,5)
            sync_once(replace(s))
            assert 4 not in {r['mail_pk'] for r in case.facts()}
            delayed.commit()
            sync_once(replace(s))
            facts={r['mail_pk']:r for r in case.facts()}
            assert facts[4]['analysis_state']==facts[5]['analysis_state']=='DONE'
        finally:
            delayed.close()
        put('late_mail_and_ai_commit_across_new_worker_objects',True)

        # A source change without a surviving log must become consistent after
        # forced full reconciliation; current-state mirror does not promise CDC.
        case.source_write('ALTER TABLE public.messages DISABLE TRIGGER fixture_mail')
        case.source_write("UPDATE public.messages SET subject='review hidden mutation' WHERE id=1")
        case.source_write('TRUNCATE public.message_change_log RESTART IDENTITY')
        sync_once(s,force_reconcile=True)
        assert case.facts()[0]['subject']=='review hidden mutation'
        put('unlogged_mutation_and_truncated_log_full_reconcile',True)
    finally:
        DatabaseTests.tearDownClass()

async def remote_probes():
    private=json.loads((ROOT/'.secrets/mcp-client.json').read_text(encoding='utf-8'))
    endpoint=json.loads((ROOT/'config/mcp-endpoint.json').read_text(encoding='utf-8'))
    context=ssl.create_default_context(cafile=str(ROOT/'config/mcp-ca.crt'))
    from urllib.parse import urlsplit
    parsed=urlsplit(endpoint['url'])
    with socket.create_connection((parsed.hostname,parsed.port),timeout=10) as raw:
        with context.wrap_socket(raw,server_hostname=parsed.hostname) as tls:
            assert hashlib.sha256(tls.getpeercert(binary_form=True)).hexdigest()==endpoint['server_certificate_sha256']
            tls_protocol=tls.version()
    with socket.create_connection((parsed.hostname,parsed.port),timeout=10) as raw:
        try:
            with context.wrap_socket(raw,server_hostname='wrong-review-host.invalid'):
                raise AssertionError('wrong hostname accepted')
        except ssl.SSLCertVerificationError:
            pass
    put('remote_tls_strict_ip_and_wrong_hostname_rejected',{'protocol':tls_protocol,'passed':True})
    auth={'Authorization':'Bearer '+private['bearer_token']}
    async with httpx2.AsyncClient(verify=context,trust_env=False,timeout=30) as http:
        for headers,status in [({},401),({'Authorization':'Bearer invalid'},401),(auth,200)]:
            response=await http.get(f'https://{parsed.hostname}:{parsed.port}/health',headers=headers)
            assert response.status_code==status
        for extra in [{'Host':'wrong-review-host.invalid'},{'Origin':'https://wrong-review-host.invalid'}]:
            response=await http.post(endpoint['url'],headers={**auth,**extra,'Accept':'application/json, text/event-stream'},json={'jsonrpc':'2.0','id':1,'method':'tools/list'})
            assert response.status_code in {403,421}
        body=b'x'*140000
        response=await http.post(endpoint['url'],headers={**auth,'Accept':'application/json, text/event-stream','Content-Type':'application/json'},content=body)
        assert response.status_code==413
    put('remote_auth_host_origin_body_limit',True)
    async with httpx2.AsyncClient(verify=context,headers=auth,trust_env=False,timeout=30) as http:
        async with Client(streamable_http_client(endpoint['url'],http_client=http),read_timeout_seconds=35) as client:
            tools=(await client.list_tools()).tools
            assert len(tools)==11 and all(t.annotations.read_only_hint and not t.annotations.open_world_hint for t in tools)
            async def call(name,args):
                result=await client.call_tool(name,args)
                assert not result.is_error,name
                assert isinstance(result.structured_content,dict)
                return result.structured_content
            guide=await call('get_data_guide',{})
            assert len(guide['source_tables'])==14
            state=await call('get_sync_status',{})
            assert state['source']['source_id']=='development-local'
            await call('get_capabilities',{})
            await call('list_taxonomy',{'level':1,'limit':1000})
            await call('query_daily_statistics',{'start':'2026-10-15','end':'2026-10-23','scope':'all_issues','level':2})
            mails=await call('list_mails',{'start':'2026-10-15','end':'2026-10-23','limit':1})
            mail=await call('get_mail_detail',{'mail_pk':mails['items'][0]['mail_pk'],'include_raw':True})
            assert 'raw_record' in mail['mail'] and 'ai_record' in mail['mail']
            await call('get_report_context',{'start':'2026-10-15','end':'2026-10-23','scope':'all_issues','include_body':True,'limit':1})
            tablelist=await call('list_source_tables',{})
            for item in tablelist['items']:
                page=await call('list_source_records',{'table':item['table'],'limit':1})
                if page['items']:
                    assert 'payload' not in page['items'][0]
                    original=await call('get_source_record',{'table':item['table'],'record_key':page['items'][0]['record_key']})
                    assert 'payload' in original['record']
            invalid=[('get_mail_detail',{'mail_pk':'../secrets'}),('list_source_records',{'table':'messages;select 1'}),('query_daily_statistics',{'start':'2026-10-23','end':'2026-10-15'}),('list_mails',{'limit':201})]
            for name,args in invalid:
                assert (await client.call_tool(name,args)).is_error
            resource=await client.read_resource('complaint-insights://guide')
            assert json.loads(resource.contents[0].text)['timezone']=='Asia/Shanghai'
    put('all_11_remote_tools_14_types_and_error_branches',True)

def handoff_checks():
    with zipfile.ZipFile(ROOT/'.secrets/mcp-handoff.zip') as archive:
        names=archive.namelist()
        assert archive.testzip() is None
        assert not any(n.endswith('.key') or n.endswith('agent.json') or n.endswith('local.json') for n in names)
        c=json.loads(archive.read('mcp-client.json'))
        assert set(c)=={'url','bearer_token','ca_file','source_id'}
        text=archive.read('MCP使用说明.md').decode('utf-8')
        assert 'Python 3.10+' in text
        assert archive.read('client-dependencies.txt')==(ROOT/'client-dependencies.txt').read_bytes()
        assert archive.read('mcp-ca.crt')==(ROOT/'config/mcp-ca.crt').read_bytes()
        RESULT['observations']['handoff_dependency_min_python']={'documented':'3.10+','httpx2_requires_python':metadata('httpx2')['Requires-Python'],'httpx2_pinned':'2.16.0'}
        put('handoff_archive_scope_integrity',{'file_count':len(names),'no_sql_credentials_or_private_keys':True})

def main():
    try:
        if '--skip-live' not in sys.argv: compare_live()
        isolated_probes()
        asyncio.run(remote_probes())
        handoff_checks()
    finally:
        RESULT['finished_at']=datetime.now(timezone.utc).isoformat()
        OUTPUT.write_text(json.dumps(RESULT,ensure_ascii=False,indent=2,default=str),encoding='utf-8')

if __name__=='__main__':
    main()
