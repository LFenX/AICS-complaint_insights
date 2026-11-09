"""Live verification of this portal/MCP only; never connect to a source database."""
import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import http.cookiejar
import io
import json
from pathlib import Path
import re
import ssl
import subprocess
import sys
from urllib.error import HTTPError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPSHandler, ProxyHandler, Request, build_opener, HTTPCookieProcessor
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from insights.config import connection_identity
from insights.mcp_tokens import read_object
from mcp_protocol_client import NoRedirect, ProtocolClient
from mcp_portal_materials import NOTES


def verify():
    client = ProtocolClient(ROOT/'.secrets/mcp-client.json')
    endpoint=json.loads((ROOT/'config/mcp-endpoint.json').read_text(encoding='utf-8'))
    portal=endpoint['url'].replace(':3037/mcp',':3029')
    context=ssl.create_default_context(cafile=str(ROOT/'config/mcp-ca.crt'))
    cookies=http.cookiejar.CookieJar()
    opener=build_opener(ProxyHandler({}),NoRedirect(),HTTPSHandler(context=context),HTTPCookieProcessor(cookies))
    checks={}
    def request(path, data=None, headers=None, method=None):
        request_headers=dict(headers or {})
        body=None
        if data is not None:
            body=urlencode(data).encode()
            request_headers.update({'Origin':portal,'Content-Type':'application/x-www-form-urlencoded'})
        req=Request(portal+path,data=body,headers=request_headers,method=method)
        try:
            response=opener.open(req,timeout=35)
        except HTTPError as error:
            response=error
        with response:
            return response.status,response.read(),{key.lower():value for key,value in response.headers.items()}

    status,landing,headers=request('/')
    assert status==200 and b'existing-agent' not in landing
    assert headers['cache-control']=='no-store'
    checks['public_portal']=True
    assert request('/issue',{'identity':'unauthorized'})[0]==401
    assert request('/revoke',{'identity':'unauthorized'})[0]==401
    assert request('/admin')[0]==303
    assert request('/.secrets/mcp-server.json')[0]==404
    checks['anonymous_admin_denied']=True
    assert request('/',headers={'Host':'evil.example:3029'})[0]==421
    assert request('/',headers={'Origin':'https://evil.example'})[0]==403
    checks['host_origin_denied']=True
    materials={}
    for name in ['mcp-client-kit.zip','mcp-ca.crt','tools-schema.json','client-guide.md','mcp-client.example.json','mcp-endpoint.json','SHA256SUMS.txt']:
        code,body,_=request('/downloads/'+name)
        assert code==200
        materials[name]=body
    assert request('/guide')[0]==200
    assert request('/downloads/token-desk-admin.json')[0]==404
    checks['public_downloads']=True
    initialize=client.initialize()
    assert initialize['protocolVersion']=='2025-11-25'
    tools=client.rpc('tools/list',{})
    assert set(tool['name'] for tool in tools['tools'])==set(NOTES)
    assert tools==json.loads(materials['tools-schema.json'])
    checks['live_tools_schema_equals_public_schema']=True
    checks['all_tools_readonly']=all(tool['annotations']['readOnlyHint'] for tool in tools['tools'])
    methods={}
    for method in ['GET','DELETE']:
        req=Request(endpoint['url'],headers=client.headers,method=method)
        try:
            with client.opener.open(req,timeout=10) as response:
                methods[method]=response.status
        except HTTPError as error:
            methods[method]=error.code
    assert methods=={'GET':405,'DELETE':405}
    checks['no_sse_or_http_sessions']=True
    called=set()
    def call(name,args=None):
        result=client.call(name,args)
        called.add(name)
        return result
    guide=call('get_data_guide')
    assert guide['default_source']=='production-ai-customer'
    state=call('get_sync_status')['source']
    assert state['source_id']=='production-ai-customer'
    caps=call('get_capabilities')
    assert 'not callable by MCP bearer' in caps['capabilities']['token_issue']['audit']
    taxonomy=call('list_taxonomy',{'limit':1})
    mails=call('list_mails',{'start':'2026-10-29','end':'2026-10-30','limit':1})
    if not mails['items']:
        mails=call('list_mails',{'limit':1})
    assert mails['items']
    selected=mails['items'][0]
    day=date.fromisoformat(selected['business_date'])
    interval={'start':str(day),'end':str(day+timedelta(days=1))}
    call('query_daily_statistics',{**interval,'level':3,'scope':'primary','limit':1})
    call('query_daily_statistics',{**interval,'level':3,'scope':'all_issues','limit':1})
    detail=call('get_mail_detail',{'mail_pk':selected['mail_pk'],'include_raw':True})
    assert detail['mail']['mail_pk']==selected['mail_pk']
    call('get_report_context',{**interval,'include_body':True,'limit':1})
    if mails.get('next_cursor'):
        # Preserve the original date filter selection for that cursor.
        arguments={'start':'2026-10-29','end':'2026-10-30','limit':1,'cursor':mails['next_cursor']}
        second=call('list_mails',arguments)
        assert second['meta']['data_version']==mails['meta']['data_version']
        assert not second['items'] or second['items'][0]['mail_pk']!=selected['mail_pk']
    tables=call('list_source_tables')['items']
    assert len(tables)==14
    table_results=[]
    for table in tables:
        records=call('list_source_records',{'table':table['table'],'limit':1})
        if records['items']:
            record=call('get_source_record',{'table':table['table'],'record_key':records['items'][0]['record_key']})
            assert 'payload' in record['record']
        table_results.append({'table':table['table'],'record_present':bool(records['items']),'passed':True})
    assert called==set(NOTES)
    bad=client.rpc('tools/call',{'name':'list_mails','arguments':{'limit':201,'source_id':'production-ai-customer'}})
    assert bad.get('isError') is True
    bad=client.rpc('tools/call',{'name':'query_daily_statistics','arguments':{'start':'2026-10-30','end':'2026-10-29','source_id':'production-ai-customer'}})
    assert bad.get('isError') is True and 'INVALID_ARGUMENT' in json.dumps(bad)
    checks['invalid_arguments_are_tool_errors']=True
    strict_cases=[
        ('list_mails',{'limit':'1'}),('list_mails',{'limit':True}),
        ('list_source_records',{'table':'messages','include_payload':'false'}),
        ('get_report_context',{'start':0,'end':86400}),
        ('get_report_context',{'start':'2026-10-29','end':'2026-10-30','mailbox':'fixture@example.invalid'}),
    ]
    for name,arguments in strict_cases:
        bad=client.rpc('tools/call',{'name':name,'arguments':{**arguments,'source_id':'production-ai-customer'}})
        assert bad.get('isError') is True and 'INVALID_ARGUMENT' in json.dumps(bad)
    unknown=Request(endpoint['url'],data=json.dumps({'jsonrpc':'2.0','id':'unknown-protocol-check','method':'tools/call',
        'params':{'name':'unknown_verification_tool','arguments':{}}}).encode(),headers=client.headers)
    with client.opener.open(unknown,timeout=15) as response:
        envelope=json.load(response)
    assert envelope['id']=='unknown-protocol-check' and envelope['error']['code']==-32602 and 'result' not in envelope
    assert all(tool['inputSchema']['additionalProperties'] is False for tool in tools['tools'])
    checks['raw_json_schema_and_unknown_tool_protocol_error']=True
    literal=client.rpc('tools/call',{'name':'get_sync_status','arguments':{'source_id':'null'}})
    assert literal.get('isError') is True and 'NOT_FOUND' in json.dumps(literal)
    checks['literal_source_string_never_uses_default']=True
    protocol_cases=[
        (b'[]',-32600,None),(b'{}',-32600,None),(b'null',-32600,None),
        (json.dumps({'jsonrpc':'1.0','id':82,'method':'tools/list','params':{'fixture':'do-not-echo'}}).encode(),-32600,None),
        (b'{',-32700,None),
        (json.dumps({'jsonrpc':'2.0','id':83,'method':'tools/call','params':{}}).encode(),-32602,83),
        (json.dumps({'jsonrpc':'2.0','id':84,'method':'unknown_verification_method'}).encode(),-32601,84),
    ]
    for body,code,rpc_id in protocol_cases:
        req=Request(endpoint['url'],data=body,headers=client.headers)
        try:
            response=client.opener.open(req,timeout=15)
        except HTTPError as error:
            response=error
        with response:
            raw=response.read()
            envelope=json.loads(raw)
        assert envelope['error']['code']==code and envelope['id']==rpc_id
        assert b'do-not-echo' not in raw
    checks['jsonrpc_envelope_parse_method_and_parameter_error_layers']=True
    for raw_id in ['true','false','null','[]','{}','1.5','1.00000000000000001']:
        body=('{"jsonrpc":"2.0","id":'+raw_id+',"method":"tools/list","params":{"fixture":"do-not-echo"}}').encode()
        req=Request(endpoint['url'],data=body,headers=client.headers)
        try:
            response=client.opener.open(req,timeout=15)
        except HTTPError as error:
            response=error
        with response:
            raw=response.read()
            assert response.status==400
        envelope=json.loads(raw)
        assert envelope['error']['code']==-32600 and envelope['id'] is None and b'do-not-echo' not in raw
    for raw_id,expected in [('0',0),('"verification-id"','verification-id'),('1.0',1),('1e3',1000),('9223372036854775808.0',9223372036854775808)]:
        req=Request(endpoint['url'],data=('{"jsonrpc":"2.0","id":'+raw_id+',"method":"tools/list"}').encode(),headers=client.headers)
        with client.opener.open(req,timeout=15) as response:
            assert response.status==200 and json.load(response)['id']==expected
    for message in [{'jsonrpc':'2.0','method':'notifications/initialized'},
                    {'jsonrpc':'2.0','id':19,'result':{}},
                    {'jsonrpc':'2.0','id':None,'error':{'code':-32700,'message':'verification fixture'}}]:
        req=Request(endpoint['url'],data=json.dumps(message).encode(),headers=client.headers)
        with client.opener.open(req,timeout=15) as response:
            assert response.status==202 and response.read()==b''
    checks['request_id_integrity_and_client_message_types']=True
    for name,arguments in [('list_taxonomy',{}),('list_mails',{}),('query_daily_statistics',interval),
                           ('get_report_context',interval),('list_source_records',{'table':'messages'})]:
        bad=client.rpc('tools/call',{'name':name,'arguments':{**arguments,'source_id':'production-ai-customer','cursor':''}})
        assert bad.get('isError') is True and 'INVALID_ARGUMENT' in json.dumps(bad)
    checks['all_five_paged_tools_reject_empty_cursor']=True

    initial=read_object(ROOT/'.secrets/token-desk-initial.json')
    status,login_page,_=request('/admin/login')
    assert status==200
    csrf=re.search('name="csrf" value="([^"]+)"',login_page.decode()).group(1)
    assert request('/admin/login',{'username':initial['username'],'password':initial['password'],'csrf':csrf})[0]==303
    status,admin_page,_=request('/admin')
    assert status==200
    csrf=re.search('name="csrf" value="([^"]+)"',admin_page.decode()).group(1)
    assert request('/issue',{'identity':'csrf-test','csrf':'wrong'})[0]==403
    before=set(read_object(ROOT/'.secrets/mcp-server.json')['tokens'])
    identity='portal-verification-'+datetime.now(timezone.utc).strftime('%H%M%S')
    assert identity not in before
    temporary_token=None
    try:
        status,issued,_=request('/issue',{'identity':identity,'csrf':csrf})
        assert status==200
        temporary_token=re.search(r'<textarea[^>]*>([^<]+)</textarea>',issued.decode()).group(1)
        assert temporary_token.encode() not in request('/admin')[1]
        probe=Request(endpoint['url'].replace('/mcp','/health'),headers={'Authorization':'Bearer '+temporary_token})
        with client.opener.open(probe,timeout=15) as response:
            assert response.status==200
    finally:
        if identity in read_object(ROOT/'.secrets/mcp-server.json')['tokens']:
            assert request('/revoke',{'identity':identity,'csrf':csrf,'confirm':'yes'})[0]==303
    assert set(read_object(ROOT/'.secrets/mcp-server.json')['tokens'])==before
    try:
        client.opener.open(Request(endpoint['url'].replace('/mcp','/health'),headers={'Authorization':'Bearer '+temporary_token}),timeout=15)
        raise AssertionError('revoked token still accepted')
    except HTTPError as error:
        assert error.code==401
    assert request('/admin/logout',{'csrf':csrf})[0]==303
    assert request('/admin')[0]==303
    checks['real_owner_issue_use_revoke_and_logout']=True

    secrets_to_scan=[initial['password'],client.config['bearer_token'],temporary_token]
    secrets_to_scan += list(read_object(ROOT/'.secrets/mcp-server.json')['tokens'].values())
    agent=read_object(ROOT/'.secrets/agent.json')
    secrets_to_scan.append(agent['api_token'])
    assert urlsplit(agent['base_url']).hostname=='127.0.0.1'
    production=read_object(ROOT/'.secrets/production.json')
    assert production['allow_production_read'] is False
    target=connection_identity(production['target_reader_url'])
    assert target['host']=='127.0.0.1' and str(target['port'])=='15433'
    for value in [agent.get('readonly_database_url',''),production['target_reader_url']]:
        password=urlsplit(value).password
        if password:
            secrets_to_scan.append(password)
    with zipfile.ZipFile(io.BytesIO(materials['mcp-client-kit.zip'])) as archive:
        assert archive.testzip() is None
        for name in archive.namelist():
            body=archive.read(name)
            assert not any(secret and secret.encode() in body for secret in secrets_to_scan), 'credential in public material'
            assert b'PRIVATE KEY' not in body and b'postgresql://' not in body
            if name.startswith('queries/'):
                assert json.loads(body)['source_id']=='production-ai-customer'
        sums=archive.read('SHA256SUMS.txt').decode()
        for line in sums.splitlines():
            digest,name=line.split('  ',1)
            assert hashlib.sha256(archive.read(name)).hexdigest()==digest
        staging=ROOT/'.runtime/mcp-portal-client-verify'
        staging.mkdir(parents=True,exist_ok=True)
        archive.extractall(staging)
    for filename in ['desk.err.log','mcp.err.log']:
        path=ROOT/'.runtime'/filename
        if path.exists():
            body=path.read_bytes()
            assert not any(secret and secret.encode() in body for secret in secrets_to_scan), 'credential in runtime log'
    checks['public_kit_and_logs_no_credentials']=True
    for script,args in [('mcp_protocol_client.py',['--list-tools']),('mcp_client.py',['--list-tools']),('mcp_workflow.py',['--start',interval['start'],'--end',interval['end']])]:
        result=subprocess.run([sys.executable,str(staging/script),'--config',str(ROOT/'.secrets/mcp-client.json'),*args],capture_output=True,encoding='utf-8',timeout=90)
        assert result.returncode==0, 'downloaded client failed: '+script
        output=json.loads(result.stdout)
        if script=='mcp_workflow.py':
            assert len(output['checked_tools'])==11 and not output['skipped']
        else:
            assert len(output['tools'])==11
    result=subprocess.run([sys.executable,str(staging/'mcp_client.py'),'list_mails','--config',str(ROOT/'.secrets/mcp-client.json'),'--arguments-file',str(staging/'queries/mails.json'),'--all-pages'],capture_output=True,encoding='utf-8',timeout=180)
    assert result.returncode==0
    page_result=json.loads(result.stdout)
    assert page_result['complete'] is True
    checks['downloaded_stdlib_sdk_workflow_and_full_pagination']=True
    checks['production_isolated_local_reader_only']=True
    return {'checked_at':datetime.now(timezone.utc).isoformat(),'result':'Passed','portal':portal+'/',
        'endpoint':endpoint['url'],'strict_ca_verification':True,'protocol_version':initialize['protocolVersion'],
        'tool_count':len(called),'tool_names':sorted(called),'source_tables':table_results,'checks':checks,
        'source':{key:state.get(key) for key in ['source_id','data_version','status','source_snapshot_at','last_sync_at']},
        'client_pagination_pages':page_result['page_count'],'kit_sha256':hashlib.sha256(materials['mcp-client-kit.zip']).hexdigest(),
        'different_computer_tested':False,'production_connected':False,'user_decision':{'outcome':'Pending'}}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=ROOT/'LG_project_docs/requirements/T-INSIGHTS-MCP-PORTAL-20261030-01/verification/results.json')
    args=parser.parse_args()
    try:
        result=verify()
    except Exception as error:
        print(json.dumps({'result':'Failed','error_type':type(error).__name__,'details_redacted':True}))
        raise
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'result':result['result'],'tool_count':result['tool_count'],'checks':len(result['checks']),
                     'strict_tls':True,'different_computer_tested':False},ensure_ascii=False))


if __name__=='__main__': main()
