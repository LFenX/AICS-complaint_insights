import io
import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import queue
import threading
import unittest
import tempfile
import subprocess
from unittest.mock import patch
from urllib.error import HTTPError

from mcp import Client
from mcp.server.mcpserver.exceptions import ToolError
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from insights.mcp_http import MCPAccessMiddleware, MCPProtocolErrors, MCPSettings, create_http_app
from insights.mcp_server import ReadAPI, create_server, wire_arguments


class FakeAPI:
    def __init__(self):
        self.calls = []

    def get(self,path,**params):
        self.calls.append((path,params))
        return {'meta':{'data_version':7},'items':[{'record_key':'17','payload':{'id':17}}],'next_cursor':None}


class MCPStdioTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        program = '''import runpy,sys
from pathlib import Path
from unittest.mock import patch
root=Path(sys.argv[1]);sys.path.insert(0,str(root))
from insights.mcp_server import ReadAPI
class API:
    default_source='stdio-fixture'
    def __init__(self):self.calls=0
    def get(self,path,**params):
        self.calls+=1
        if params.get('mailbox')=='stdio-stray-output-test':
            print('synthetic-stray-output',flush=True)
            params['stdin_is_eof']=sys.stdin.read(1)==''
        return {'meta':{'data_version':7},'fixture_calls':self.calls,'fixture_params':params,'items':[],'next_cursor':None}
with patch.object(ReadAPI,'load',return_value=API()):runpy.run_path(str(root/'scripts/mcp_server.py'),run_name='__main__')
'''
        import sys
        self.process = subprocess.Popen([sys.executable,'-c',program,str(root)],stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'PYTHONUTF8':'1'},cwd=root)
        self.responses = queue.Queue()
        def read():
            for line in self.process.stdout:
                try:
                    self.responses.put(json.loads(line))
                except (ValueError,UnicodeError) as error:
                    self.responses.put(error)
        self.reader = threading.Thread(target=read,daemon=True)
        self.reader.start()
        response = self.rpc(json.dumps({'jsonrpc':'2.0','id':1,'method':'initialize','params':{
            'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'stdio-regression','version':'1'}}}))
        self.assertEqual(response['id'],1)
        self.send('{"jsonrpc":"2.0","method":"notifications/initialized"}')

    def tearDown(self):
        self.process.stdin.close()
        try:
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=5)
            self.fail('stdio process did not exit after stdin EOF')
        finally:
            self.reader.join(timeout=2)
            self.process.stdout.close()
            self.process.stderr.close()
        self.assertEqual(self.process.returncode,0)

    def send(self, line):
        data = line if isinstance(line,bytes) else line.encode('utf-8')
        self.process.stdin.write(data+b'\n')
        self.process.stdin.flush()

    def receive(self):
        result = self.responses.get(timeout=10)
        if isinstance(result,Exception):
            raise result
        return result

    def rpc(self, line):
        self.send(line)
        return self.receive()

    def test_real_stdio_cli_preserves_integer_argument_precision(self):
        def call(value,index):
            return self.rpc('{"jsonrpc":"2.0","id":'+str(index)+',"method":"tools/call","params":'
                '{"name":"list_mails","arguments":{"limit":'+value+'}}}')['result']
        for index,value in enumerate(['1.00000000000000001','200.00000000000000001','0.99999999999999999',
            '1e9999','1e-9999','1e9999999999999999999'],10):
            self.assertTrue(call(value,index)['isError'],value)
        for count,value in enumerate(['1.0','2e0','200.0'],1):
            result = call(value,20+count)
            self.assertFalse(result.get('isError',False))
            self.assertEqual(result['structuredContent']['fixture_calls'],count)
            self.assertEqual(result['structuredContent']['fixture_params']['limit'],int(float(value)))
        mixed = self.rpc('{"jsonrpc":"2.0","id":900.0,"method":"tools/call","params":{"name":"list_mails","arguments":{"limit":1.00000000000000001}}}')
        self.assertEqual(mixed['id'],900)
        self.assertTrue(mixed['result']['isError'])

    def test_real_stdio_ids_errors_and_recovery(self):
        for literal,expected in [('702.0',702),('703e0',703),('0',0),('"中文-id"','中文-id')]:
            result = self.rpc('{"jsonrpc":"2.0","id":'+literal+',"method":"tools/list"}')
            self.assertEqual(result['id'],expected)
            self.assertEqual(len(result['result']['tools']),11)
        for literal in ['704.00000000000000001','true','null','1e9999999999999999999']:
            result = self.rpc('{"jsonrpc":"2.0","id":'+literal+',"method":"tools/list"}')
            self.assertEqual(result['error']['code'],-32600,literal)
            self.assertIsNone(result['id'])
        for line,code in [(b'{',-32700),(b'\xff',-32700),(b'null',-32600),(b'[]',-32600),
            (b'{"jsonrpc":"2.0","id":8,"method":"tools/call","params":{"name":"list_mails","arguments":{"limit":NaN}}}',-32700)]:
            result = self.rpc(line)
            self.assertEqual(result['error']['code'],code)
            self.assertIsNone(result['id'])
            self.assertNotIn('NaN',json.dumps(result))
        result = self.rpc('{"jsonrpc":"2.0","id":499,"method":"tools/list"}')
        self.assertEqual(len(result['result']['tools']),11)

    def test_stdio_message_context_strings_and_stdout_isolation(self):
        arguments = {'mailbox':'stdio-stray-output-test','cursor':'null','level_one':'中文分类[]','source_id':'null'}
        first = self.rpc(json.dumps({'jsonrpc':'2.0','id':100,'method':'tools/call',
            'params':{'name':'list_mails','arguments':arguments}},ensure_ascii=False))
        self.assertFalse(first['result'].get('isError',False))
        self.assertTrue(first['result']['structuredContent']['fixture_params']['stdin_is_eof'])
        for key,value in arguments.items():
            self.assertEqual(first['result']['structuredContent']['fixture_params'][key],value)
        self.send('{"jsonrpc":"2.0","id":101,"method":"tools/call","params":{"name":"list_mails","arguments":{"limit":1.00000000000000001}}}')
        self.send('{"jsonrpc":"2.0","id":102,"method":"tools/call","params":{"name":"list_mails","arguments":{"limit":2.0}}}')
        results = {result['id']:result for result in [self.receive(),self.receive()]}
        self.assertTrue(results[101]['result']['isError'])
        self.assertFalse(results[102]['result'].get('isError',False))
        self.assertEqual(results[102]['result']['structuredContent']['fixture_calls'],2)


class MCPProtocolTests(unittest.IsolatedAsyncioTestCase):
    async def test_tool_limit_applies_to_stdio_and_recovers_on_sliding_boundary(self):
        now = [0.0]
        api = FakeAPI()
        async with Client(create_server(api,tool_calls_per_minute=2,clock=lambda:now[0])) as client:
            resource = await client.read_resource('complaint-insights://guide')
            self.assertEqual(json.loads(resource.contents[0].text)['tool_rate_limit']['calls'],2)
            first = await client.call_tool('get_data_guide',{})
            self.assertEqual(first.structured_content['tool_rate_limit']['calls'],2)
            now[0] = 30.0
            self.assertFalse((await client.call_tool('list_mails',{})).is_error)
            now[0] = 59.999
            limited = await client.call_tool('list_mails',{})
            self.assertTrue(limited.is_error)
            error = json.loads(limited.content[0].text)
            self.assertEqual(error['code'],'TOOL_RATE_LIMITED')
            self.assertEqual(error['retry_after_seconds'],1)
            self.assertEqual(len(api.calls),1)
            now[0] = 60.0
            self.assertFalse((await client.call_tool('list_source_tables',{})).is_error)
            limited = await client.call_tool('get_data_guide',{})
            self.assertTrue(limited.is_error)
            self.assertEqual(json.loads(limited.content[0].text)['retry_after_seconds'],30)
            now[0] = 90.0
            self.assertFalse((await client.call_tool('list_mails',{})).is_error)
            self.assertEqual(len(api.calls),3)

    async def test_legal_string_literals_are_never_reinterpreted(self):
        api=FakeAPI()
        async with Client(create_server(api)) as client:
            for literal in ['null','[]','{}','[1]','"quoted"','false','0']:
                result=await client.call_tool('list_mails',{'source_id':'null','mailbox':literal,'cursor':literal,'level_one':literal})
                self.assertFalse(result.is_error,literal)
                params=api.calls[-1][1]
                self.assertEqual(params['source_id'],'null')
                for name in ['mailbox','cursor','level_one']:
                    self.assertEqual(params[name],literal)

    async def test_portal_admin_catalog_is_explicitly_disabled_for_mcp_clients(self):
        async with Client(create_server(FakeAPI())) as client:
            result=await client.call_tool('get_capabilities',{})
        value=result.structured_content
        self.assertFalse(value['capabilities']['token_issue']['enabled'])
        self.assertFalse(value['capabilities']['token_revoke']['enabled'])
        self.assertEqual(value['permissions']['insights.tokens.manage'],'insights.admin')
        self.assertIn('不是MCP工具',value['capabilities']['token_issue']['disabled_reason'])

    async def test_tool_discovery_and_resource_contract(self):
        async with Client(create_server(FakeAPI())) as client:
            tools = (await client.list_tools()).tools
            self.assertEqual(len(tools),11)
            self.assertTrue(all(item.annotations.read_only_hint for item in tools))
            self.assertTrue(all(not item.annotations.open_world_hint for item in tools))
            self.assertTrue(all(item.output_schema for item in tools))
            guide = await client.call_tool('get_data_guide',{})
            self.assertFalse(guide.is_error)
            self.assertEqual(len(guide.structured_content['source_tables']),14)
            resource = await client.read_resource('complaint-insights://guide')
            self.assertEqual(json.loads(resource.contents[0].text)['timezone'],'Asia/Shanghai')

    async def test_parameters_forwarded_without_business_reimplementation(self):
        api = FakeAPI()
        async with Client(create_server(api)) as client:
            result = await client.call_tool('query_daily_statistics',{'start':'2026-10-01','end':'2026-10-03','level':3,'scope':'all_issues','source_id':'fixture-local'})
            self.assertFalse(result.is_error)
            path,params = api.calls[-1]
            self.assertEqual(path,'/v1/daily')
            self.assertEqual(str(params['start']),'2026-10-01')
            self.assertEqual(params['scope'],'all_issues')
            self.assertEqual(params['source_id'],'fixture-local')
            await client.call_tool('get_source_record',{'table':'MailAiArtifact','record_key':'17'})
            self.assertEqual(api.calls[-1][1]['table'],'MailAiArtifact')
            self.assertTrue(api.calls[-1][1]['include_payload'])
            self.assertEqual(api.calls[-1][1]['record_key'],'17')

    async def test_invalid_limits_dates_tables_and_path_never_reach_backend(self):
        api = FakeAPI()
        async with Client(create_server(api)) as client:
            for tool,args in [
                ('list_source_records',{'table':'messages; DROP TABLE x'}),
                ('list_source_records',{'table':'messages','limit':51}),
                ('list_mails',{'start':'not-a-date'}),
                ('get_mail_detail',{'mail_pk':'../config'}),
                ('get_report_context',{'start':'2026-10-01','end':'2026-10-03','direction':'unknown'}),
            ]:
                result = await client.call_tool(tool,args)
                self.assertTrue(result.is_error,(tool,args))
            self.assertEqual(api.calls,[])


class MCPBoundaryTests(unittest.TestCase):
    def test_rate_configuration_rejects_coercion_and_disabled_limits(self):
        for value in [0,-1,60001,True,False,1.0,'6000',None]:
            settings = MCPSettings('10.8.61.200',3037,('10.8.0.0/16',),{'test-agent':'x'*48},
                Path('none'),Path('none'),Path('none'),tool_calls_per_minute=value)
            with self.assertRaisesRegex(ValueError,'tool_calls_per_minute'):
                settings.validate()
            with self.assertRaisesRegex(ValueError,'tool_calls_per_minute'):
                create_server(FakeAPI(),tool_calls_per_minute=value)
        for value in [1,60000]:
            create_server(FakeAPI(),tool_calls_per_minute=value)

    def test_http_quota_is_per_identity_shared_by_tools_and_survives_token_reissue(self):
        now = [0.0]
        api = FakeAPI()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'tokens.json'
            path.write_text(json.dumps({'tokens':{'alice':'a'*48,'bob':'b'*48}}),encoding='utf-8')
            settings = MCPSettings('10.8.61.200',3037,('10.8.0.0/16',),{},Path('none'),Path('none'),Path('none'),path,3)
            with patch.object(MCPSettings,'validate',return_value=None):
                app = create_http_app(settings,api,clock=lambda:now[0])
            with TestClient(app,base_url='https://10.8.61.200:3037',client=('10.8.61.201',1234)) as client:
                def rpc(name,args=None,token='a'*48):
                    return client.post('/mcp',json={'jsonrpc':'2.0','id':77,'method':'tools/call',
                        'params':{'name':name,'arguments':args or {}}},headers={
                        'Authorization':'Bearer '+token,'Accept':'application/json, text/event-stream',
                        'MCP-Protocol-Version':'2025-11-25'})
                self.assertTrue(rpc('list_mails',{'limit':True}).json()['result']['isError'])
                self.assertEqual(rpc('unknown_fixture_tool').json()['error']['code'],-32602)
                for name in ['list_mails','get_data_guide','list_source_tables']:
                    self.assertFalse(rpc(name).json()['result'].get('isError',False),name)
                limited = rpc('list_mails')
                self.assertEqual(limited.status_code,200)
                self.assertTrue(limited.json()['result']['isError'])
                error = json.loads(limited.json()['result']['content'][0]['text'])
                self.assertEqual(error['code'],'TOOL_RATE_LIMITED')
                self.assertEqual(error['retry_after_seconds'],60)
                self.assertEqual(len(api.calls),2)
                self.assertFalse(rpc('list_mails',token='b'*48).json()['result'].get('isError',False))
                path.write_text(json.dumps({'tokens':{'alice':'c'*48,'bob':'b'*48}}),encoding='utf-8')
                self.assertEqual(rpc('list_mails').status_code,401)
                self.assertTrue(rpc('list_mails',token='c'*48).json()['result']['isError'])
                self.assertEqual(len(api.calls),3)
                now[0] = 60.0
                self.assertFalse(rpc('list_mails',token='c'*48).json()['result'].get('isError',False))
                self.assertEqual(len(api.calls),4)

    def test_concurrent_http_calls_cannot_overshoot_identity_quota(self):
        api = FakeAPI()
        settings = MCPSettings('10.8.61.200',3037,('10.8.0.0/16',),{'test-agent':'x'*48},
            Path('none'),Path('none'),Path('none'),tool_calls_per_minute=4)
        with patch.object(MCPSettings,'validate',return_value=None):
            app = create_http_app(settings,api,clock=lambda:0.0)
        with TestClient(app,base_url='https://10.8.61.200:3037',client=('10.8.61.201',1234)) as client:
            def rpc(index):
                return client.post('/mcp',json={'jsonrpc':'2.0','id':index,'method':'tools/call',
                    'params':{'name':'list_mails','arguments':{}}},headers={
                    'Authorization':'Bearer '+'x'*48,'Accept':'application/json, text/event-stream',
                    'MCP-Protocol-Version':'2025-11-25'}).json()['result']
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                results = list(pool.map(rpc,range(20)))
        self.assertEqual(sum(not result.get('isError',False) for result in results),4)
        self.assertEqual(len(api.calls),4)
        for result in results:
            if result.get('isError',False):
                self.assertEqual(json.loads(result['content'][0]['text'])['code'],'TOOL_RATE_LIMITED')

    def test_raw_number_precision_and_request_context_isolation(self):
        api = FakeAPI()
        settings = MCPSettings('10.8.61.200',3037,('10.8.0.0/16',),{'test-agent':'x'*48},Path('none'),Path('none'),Path('none'))
        with patch.object(MCPSettings,'validate',return_value=None):
            app = create_http_app(settings,api)
        headers = {'Authorization':'Bearer '+'x'*48,'Accept':'application/json, text/event-stream',
                   'Content-Type':'application/json','MCP-Protocol-Version':'2025-11-25'}
        with TestClient(app,base_url='https://10.8.61.200:3037',client=('10.8.61.201',1234)) as client:
            def rpc(literal,request_id='71'):
                body = '{"jsonrpc":"2.0","id":'+request_id+',"method":"tools/call","params":{"name":"list_mails","arguments":{"limit":'+literal+'}}}'
                response = client.post('/mcp',content=body,headers=headers)
                self.assertEqual(response.status_code,200,literal)
                return response.json()['result']

            for request_id in ['71','1.0']:
                for literal in ['1.5','1.00000000000000001','200.00000000000000001','0.99999999999999999',
                                '1e-9999','1e4300','1e999999999999999999999','true','"1"','null','[]','{}']:
                    count = len(api.calls)
                    self.assertTrue(rpc(literal,request_id)['isError'],literal)
                    self.assertEqual(len(api.calls),count,literal)
                for literal, expected in [('1.0',1),('2e0',2),('2e2',200),('200.00000000000000000',200)]:
                    self.assertFalse(rpc(literal,request_id).get('isError',False),literal)
                    self.assertEqual(api.calls[-1][1]['limit'],expected)
            count = len(api.calls)
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                outputs = list(pool.map(rpc,['1.00000000000000001','2.0']*8))
            self.assertEqual([bool(item.get('isError',False)) for item in outputs],[True,False]*8)
            self.assertEqual(len(api.calls),count+8)
            self.assertTrue(all(call[1]['limit']==2 for call in api.calls[count:]))
        self.assertIsNone(wire_arguments.get())

    def test_request_ids_do_not_fall_back_to_notifications(self):
        settings=MCPSettings('10.8.61.200',3037,('10.8.0.0/16',),{'test-agent':'x'*48},Path('none'),Path('none'),Path('none'))
        with patch.object(MCPSettings,'validate',return_value=None):
            app=create_http_app(settings,FakeAPI())
        headers={'Authorization':'Bearer '+'x'*48,'Accept':'application/json, text/event-stream',
                 'Content-Type':'application/json','MCP-Protocol-Version':'2025-11-25'}
        with TestClient(app,base_url='https://10.8.61.200:3037',client=('10.8.61.201',1234)) as client:
            for raw_id in ['true','false','null','[]','{}','1.5','1.00000000000000001','1e-9999','1e4300','1e999999999999999999999']:
                body='{"jsonrpc":"2.0","id":'+raw_id+',"method":"tools/list","params":{"fixture":"do-not-echo"}}'
                response=client.post('/mcp',content=body,headers=headers)
                self.assertEqual(response.status_code,400,raw_id)
                self.assertEqual(response.json()['error']['code'],-32600,raw_id)
                self.assertIsNone(response.json()['id'])
                self.assertNotIn('do-not-echo',response.text)
            for raw_id,expected in [('0',0),('"fixture-id"','fixture-id'),('1.0',1),('1e3',1000),
                                    ('-0.0',0),('9223372036854775808.0',9223372036854775808)]:
                body='{"jsonrpc":"2.0","id":'+raw_id+',"method":"tools/list"}'
                response=client.post('/mcp',content=body,headers=headers)
                self.assertEqual(response.status_code,200,raw_id)
                self.assertEqual(response.json()['id'],expected)
                self.assertEqual(len(response.json()['result']['tools']),11)
            for raw_id in ['NaN','Infinity','-Infinity']:
                response=client.post('/mcp',content='{"jsonrpc":"2.0","id":'+raw_id+',"method":"tools/list"}',headers=headers)
                self.assertEqual(response.status_code,400)
                self.assertEqual(response.json()['error']['code'],-32700)
            for message in [{'jsonrpc':'2.0','method':'notifications/initialized'},
                            {'jsonrpc':'2.0','id':19,'result':{}},
                            {'jsonrpc':'2.0','id':19,'error':{'code':-32603,'message':'fixture'}},
                            {'jsonrpc':'2.0','id':None,'error':{'code':-32700,'message':'fixture'}}]:
                response=client.post('/mcp',json=message,headers=headers)
                self.assertEqual(response.status_code,202,message)
                self.assertEqual(response.content,b'')

    def test_empty_cursor_is_rejected_before_backend_for_all_paged_tools(self):
        api=FakeAPI()
        settings=MCPSettings('10.8.61.200',3037,('10.8.0.0/16',),{'test-agent':'x'*48},Path('none'),Path('none'),Path('none'))
        with patch.object(MCPSettings,'validate',return_value=None):
            app=create_http_app(settings,api)
        headers={'Authorization':'Bearer '+'x'*48,'Accept':'application/json, text/event-stream','MCP-Protocol-Version':'2025-11-25'}
        cases={'list_taxonomy':{},'list_mails':{},'query_daily_statistics':{'start':'2026-10-29','end':'2026-10-30'},
               'get_report_context':{'start':'2026-10-29','end':'2026-10-30'},'list_source_records':{'table':'messages'}}
        with TestClient(app,base_url='https://10.8.61.200:3037',client=('10.8.61.201',1234)) as client:
            def rpc(name,args):
                return client.post('/mcp',json={'jsonrpc':'2.0','id':71,'method':'tools/call','params':{'name':name,'arguments':args}},headers=headers).json()['result']
            for name,args in cases.items():
                before=len(api.calls)
                self.assertTrue(rpc(name,{**args,'cursor':''})['isError'],name)
                self.assertEqual(len(api.calls),before)
                for good in [args,{**args,'cursor':None},{**args,'cursor':'opaque-fixture'}]:
                    self.assertFalse(rpc(name,good).get('isError',False),name)
                self.assertEqual(len(api.calls),before+3)

    def test_raw_http_schema_validation_and_protocol_error_layer(self):
        api=FakeAPI()
        settings=MCPSettings('10.8.61.200',3037,('10.8.0.0/16',),{'test-agent':'x'*48},Path('none'),Path('none'),Path('none'))
        with patch.object(MCPSettings,'validate',return_value=None):
            app=create_http_app(settings,api)
        headers={'Authorization':'Bearer '+'x'*48,'Accept':'application/json, text/event-stream','MCP-Protocol-Version':'2025-11-25'}
        with TestClient(app,base_url='https://10.8.61.200:3037',client=('10.8.61.201',1234)) as client:
            def rpc(name,args):
                return client.post('/mcp',json={'jsonrpc':'2.0','id':71,'method':'tools/call','params':{'name':name,'arguments':args}},headers=headers)
            listed=client.post('/mcp',json={'jsonrpc':'2.0','id':70,'method':'tools/list','params':{}},headers=headers).json()['result']['tools']
            self.assertTrue(all(tool['inputSchema']['additionalProperties'] is False for tool in listed))
            for name,args in [
                ('list_mails',{'limit':'1'}),('list_mails',{'limit':True}),
                ('list_source_records',{'table':'messages','include_payload':'false'}),
                ('get_report_context',{'start':0,'end':86400}),
                ('get_report_context',{'start':'2026-02-30','end':'2026-10-30'}),
                ('get_report_context',{'start':'2026-10-29','end':'2026-10-30','mailbox':'filter@example.invalid'}),
                ('get_data_guide',{'unexpected':True}),
            ]:
                response=rpc(name,args)
                self.assertEqual(response.status_code,200)
                self.assertTrue(response.json()['result']['isError'],(name,args))
                self.assertEqual(api.calls,[])
            unknown=rpc('unknown_fixture_tool',{}).json()
            self.assertEqual(unknown['id'],71)
            self.assertEqual(unknown['error']['code'],-32602)
            self.assertNotIn('result',unknown)
            for malformed in [[],{},None,{'jsonrpc':'1.0','id':72,'method':'tools/list','params':{'fixture_secret':'do-not-echo'}},
                              {'jsonrpc':'2.0','id':73,'method':123}]:
                response=client.post('/mcp',json=malformed,headers=headers)
                # TestClient json=None means no body; send explicit JSON null.
                if malformed is None:
                    response=client.post('/mcp',content='null',headers={**headers,'Content-Type':'application/json'})
                self.assertEqual(response.status_code,400)
                self.assertEqual(response.json()['error']['code'],-32600)
                self.assertIsNone(response.json()['id'])
                self.assertNotIn('do-not-echo',response.text)
            parsed=client.post('/mcp',content='{',headers={**headers,'Content-Type':'application/json'})
            self.assertEqual(parsed.json()['error']['code'],-32700)
            missing=client.post('/mcp',json={'jsonrpc':'2.0','id':74,'method':'tools/call','params':{}},headers=headers).json()
            self.assertEqual(missing['error']['code'],-32602)
            self.assertEqual(missing['id'],74)
            method=client.post('/mcp',json={'jsonrpc':'2.0','id':75,'method':'unknown_fixture_method'},headers=headers).json()
            self.assertEqual(method['error']['code'],-32601)
            self.assertEqual(method['id'],75)
            good=rpc('get_report_context',{'start':'2026-10-29','end':'2026-10-30','include_body':True,'limit':1}).json()
            self.assertFalse(good['result'].get('isError',False))
            self.assertEqual(len(api.calls),1)
            self.assertEqual(str(api.calls[0][1]['start']),'2026-10-29')
            self.assertIs(api.calls[0][1]['include_body'],True)

    def test_stateless_json_transport_has_no_get_stream_or_delete_session(self):
        async def ok(scope,receive,send):
            await JSONResponse({'ok':True})(scope,receive,send)
        settings=MCPSettings('10.8.61.200',3037,('10.8.0.0/16',),{'test-agent':'x'*48},Path('none'),Path('none'),Path('none'))
        client=TestClient(MCPAccessMiddleware(ok,settings,post_only=True),base_url='https://10.8.61.200:3037',client=('10.8.61.201',1234))
        auth={'Authorization':'Bearer '+'x'*48}
        self.assertEqual(client.get('/mcp',headers=auth).status_code,405)
        self.assertEqual(client.delete('/mcp',headers=auth).status_code,405)
        self.assertEqual(client.post('/mcp',headers=auth).status_code,200)
        self.assertEqual(client.get('/mcp').status_code,401)
        self.assertEqual(client.get('/mcp',headers={**auth,'Host':'evil.example'}).status_code,421)
        self.assertEqual(client.get('/mcp',headers={**auth,'Origin':'https://evil.example'}).status_code,403)

    def test_revoked_token_never_revives_when_file_is_missing_or_invalid(self):
        async def ok(scope, receive, send):
            await JSONResponse({'ok': True})(scope, receive, send)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'tokens.json'
            settings = MCPSettings('10.8.61.200',3037,('10.8.0.0/16',),
                {'revoked-agent':'r'*48,'active-agent':'a'*48},Path('none'),Path('none'),Path('none'),path)
            client = TestClient(MCPAccessMiddleware(ok,settings),base_url='https://10.8.61.200:3037',client=('10.8.61.201',1234))
            path.write_text(json.dumps({'tokens':{'active-agent':'a'*48}}),encoding='utf-8')
            self.assertEqual(client.get('/mcp',headers={'Authorization':'Bearer '+'r'*48}).status_code,401)
            self.assertEqual(client.get('/mcp',headers={'Authorization':'Bearer '+'a'*48}).status_code,200)
            for invalid in ['{','[]','null','{}','{"tokens":{}}',json.dumps({'tokens':{'bad':['x']}}),json.dumps({'tokens':{'one':'x'*48,'two':'x'*48}})]:
                path.write_text(invalid,encoding='utf-8')
                for token in ['r'*48,'a'*48]:
                    self.assertEqual(client.get('/mcp',headers={'Authorization':'Bearer '+token}).status_code,401)
            path.unlink()
            self.assertEqual(client.get('/mcp',headers={'Authorization':'Bearer '+'r'*48}).status_code,401)
            path.write_text(json.dumps({'tokens':{'active-agent':'a'*48}}),encoding='utf-8')
            self.assertEqual(client.get('/mcp',headers={'Authorization':'Bearer '+'a'*48}).status_code,200)

    def test_backend_must_be_loopback_without_embedded_credentials(self):
        for url in ['https://127.0.0.1:3036','http://10.8.61.200:3036','http://a:b@127.0.0.1:3036','http://127.0.0.1:3036/leak']:
            with self.assertRaises(ValueError): ReadAPI(url,'x'*48,'development-local')
        self.assertNotIn('x'*48,repr(ReadAPI('http://127.0.0.1:3036','x'*48,'development-local')))

    def test_backend_cursor_conflict_is_actionable_and_redacted(self):
        api = ReadAPI('http://127.0.0.1:3036','x'*48,'development-local')
        error = HTTPError('http://127.0.0.1:3036',409,'private payload',{},io.BytesIO(b'private body'))
        with patch('insights.mcp_server.build_opener') as opener:
            opener.return_value.open.side_effect = error
            with self.assertRaises(ToolError) as raised: api.get('/v1/mails',cursor='opaque')
        self.assertIn('DATA_VERSION_CHANGED',str(raised.exception))
        self.assertNotIn('private',str(raised.exception))
        self.assertNotIn('x'*48,str(raised.exception))

    def test_https_bearer_network_and_proxy_spoofing_boundaries(self):
        async def ok(scope,receive,send):
            await JSONResponse({'ok':True})(scope,receive,send)
        settings = MCPSettings('10.8.61.200',3037,('10.8.0.0/16',),{'test-agent':'x'*48},Path('none'),Path('none'),Path('none'))
        app = MCPAccessMiddleware(ok,settings)
        secure = TestClient(app,base_url='https://10.8.61.200:3037',client=('10.8.61.201',1234))
        auth = {'Authorization':'Bearer '+'x'*48}
        self.assertEqual(secure.get('/mcp').status_code,401)
        self.assertEqual(secure.get('/mcp',headers={'Authorization':'Bearer wrong'}).status_code,401)
        self.assertEqual(secure.get('/mcp',headers=auth).status_code,200)
        plain = TestClient(app,base_url='http://10.8.61.200:3037',client=('10.8.61.201',1234))
        self.assertEqual(plain.get('/mcp',headers=auth).status_code,403)
        external = TestClient(app,base_url='https://10.8.61.200:3037',client=('203.0.113.12',1234))
        self.assertEqual(external.get('/mcp',headers={**auth,'X-Forwarded-For':'10.8.61.201','X-Forwarded-Proto':'https'}).status_code,403)


class MCPProtocolBodyTests(unittest.IsolatedAsyncioTestCase):
    async def invoke(self,messages):
        seen=[]
        sent=[]
        queue=iter(messages)
        async def receive():
            return next(queue,{'type':'http.disconnect'})
        async def send(message):
            sent.append(message)
        async def app(scope,receive,send):
            seen.append(await receive())
            seen.append(await receive())
            await JSONResponse({'ok':True})(scope,receive,send)
        await MCPProtocolErrors(app)({'type':'http','method':'POST','path':'/mcp','headers':[]},receive,send)
        return seen,sent

    async def test_chunked_unicode_request_is_replayed_without_argument_changes(self):
        value={'jsonrpc':'2.0','id':1.0,'method':'tools/call','params':{'name':'fixture','arguments':{'text':'中文😀'*3000,'literal':'null'}}}
        raw=json.dumps(value,ensure_ascii=False).encode()
        seen,sent=await self.invoke([{'type':'http.request','body':raw[:19],'more_body':True},
                                    {'type':'http.request','body':raw[19:],'more_body':False}])
        replay=json.loads(seen[0]['body'])
        self.assertEqual(replay['params'],value['params'])
        self.assertIs(type(replay['id']),int)
        self.assertFalse(seen[0]['more_body'])
        self.assertEqual(seen[1]['type'],'http.disconnect')
        self.assertEqual(sent[0]['status'],200)

    async def test_oversize_disconnect_and_invalid_encoding_never_reach_sdk(self):
        cases=[([{'type':'http.request','body':b' '*65536,'more_body':True},
                 {'type':'http.request','body':b' '*65537,'more_body':False}],413),
               ([{'type':'http.request','body':b'{','more_body':True},{'type':'http.disconnect'}],None),
               ([{'type':'http.request','body':b'\xff','more_body':False}],400)]
        for messages,status in cases:
            seen,sent=await self.invoke(messages)
            self.assertEqual(seen,[])
            self.assertEqual(sent[0]['status'] if sent else None,status)


class MCPClientConfigurationTests(unittest.TestCase):
    def setUp(self):
        parent=Path('.runtime/mcp-portal-client-config-tests')
        parent.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        path=self.root/'mcp_client.py'
        path.write_bytes((Path(__file__).resolve().parents[1]/'scripts/mcp_client.py').read_bytes())
        template={'url':'https://10.8.61.200:3037/mcp','bearer_token':'REPLACE_WITH_MCP_TOKEN','source_id':'production-ai-customer','ca_file':'mcp-ca.crt'}
        (self.root/'mcp-client.example.json').write_text(json.dumps(template),encoding='utf-8')
        spec=importlib.util.spec_from_file_location('fixture_mcp_client',path)
        self.module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.config=self.root/'private.json'
        self.token='fixture-only-'+'x'*48
        self.addCleanup(patch.stopall)
        patch.object(self.module.getpass,'getpass',return_value=self.token).start()
        patch.object(self.module.subprocess,'check_output',return_value='"fixture-user","S-1-5-21-123"').start()
        self.acl=patch.object(self.module.subprocess,'run').start()

    def test_config_is_protected_before_the_first_credential_write(self):
        original_dump=json.dump
        def inspect_write(value,stream,**kwargs):
            self.assertEqual(self.config.read_bytes(),b'')
            if os.name=='nt':
                self.acl.assert_called_once()
            else:
                self.assertEqual(self.config.stat().st_mode & 0o777,0o600)
            original_dump(value,stream,**kwargs)
        with patch.object(self.module.json,'dump',side_effect=inspect_write):
            result=self.module.configure(self.config)
        self.assertEqual(result['status'],'CONFIGURED')
        self.assertEqual(json.loads(self.config.read_text(encoding='utf-8'))['bearer_token'],self.token)

    def test_partial_write_failure_leaves_no_credential_file(self):
        def broken_write(value,stream,**kwargs):
            stream.write('{"bearer_token":"'+self.token+'"')
            raise OSError('fixture write failure')
        with patch.object(self.module.json,'dump',side_effect=broken_write):
            with self.assertRaises(OSError): self.module.configure(self.config)
        self.assertFalse(self.config.exists())

    def test_flush_failure_cleans_the_fully_written_file(self):
        with patch.object(self.module.os,'fsync',side_effect=OSError('fixture sync failure')):
            with self.assertRaises(OSError): self.module.configure(self.config)
        self.assertFalse(self.config.exists())

    @unittest.skipUnless(os.name=='nt','Windows file ACL boundary')
    def test_acl_failure_prevents_writing_and_cleans_empty_file(self):
        self.acl.side_effect=subprocess.CalledProcessError(1,['icacls'])
        with patch.object(self.module.json,'dump') as dump:
            with self.assertRaises(subprocess.CalledProcessError): self.module.configure(self.config)
        dump.assert_not_called()
        self.assertFalse(self.config.exists())

    def test_existing_configuration_is_never_changed(self):
        self.config.write_text('existing protected data',encoding='utf-8')
        with self.assertRaises(ValueError): self.module.configure(self.config)
        self.assertEqual(self.config.read_text(encoding='utf-8'),'existing protected data')


if __name__=='__main__':
    unittest.main()
