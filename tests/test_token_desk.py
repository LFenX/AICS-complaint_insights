import concurrent.futures
from html import unescape
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from starlette.responses import JSONResponse
from starlette.testclient import TestClient
from insights.mcp_http import MCPAccessMiddleware, MCPSettings
from insights.mcp_tokens import read_object, token_rows
from insights.token_desk import COOKIE, PREAUTH, DeskSettings, configure_admin, create_app, issue_token, revoke_token
import insights.token_desk as token_desk


class TokenDeskTests(unittest.TestCase):
    def setUp(self):
        parent = Path('.runtime/mcp-portal-tests')
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.server, self.registry, self.admin = [self.root/name for name in ['server.json','registry.json','admin.json']]
        self.server.write_text(json.dumps({'tokens':{'existing-agent':'a'*48},'preserved':'setting'}),encoding='utf-8')
        self.password = 'test-owner-password-123456'
        configure_admin('owner', self.password, self.admin)
        self.now = 1000.
        self.settings = DeskSettings('10.8.61.200')
        self.app = create_app(self.server, self.registry, self.admin, settings=self.settings, public_path=self.root, clock=lambda:self.now)
        self.client = self.client_for(self.app)

    def client_for(self, app, peer='10.8.61.201', scheme='https'):
        client = TestClient(app, base_url=f'{scheme}://10.8.61.200:3029', client=(peer,1234), follow_redirects=False)
        self.addCleanup(client.close)
        return client

    def csrf(self, response):
        return re.search('name="csrf" value="([^"]+)"', response.text).group(1)

    def login(self, client=None, password=None):
        client = client or self.client
        challenge = self.csrf(client.get('/admin/login'))
        return client.post('/admin/login', data={'username':'owner','password':password or self.password,'csrf':challenge},headers={'Origin':self.settings.origin})

    def post(self, path, data):
        return self.client.post(path, data=data, headers={'Origin':self.settings.origin})

    def test_public_portal_has_no_registry_and_bearer_cannot_manage(self):
        page = self.client.get('/')
        self.assertEqual(page.status_code,200)
        self.assertNotIn('existing-agent',page.text)
        self.assertNotIn('a'*48,page.text)
        self.assertIn('production-ai-customer',page.text)
        self.assertEqual(self.client.get('/admin').status_code,303)
        for path in ['/issue','/revoke']:
            self.assertEqual(self.client.post(path,headers={'Authorization':'Bearer '+'a'*48},data={'identity':'visitor'}).status_code,401)
        self.assertEqual(self.client.get('/downloads/admin.json').status_code,404)
        self.assertEqual(self.client.get('/.secrets/mcp-server.json').status_code,404)
        for header,value in [('cache-control','no-store'),('x-frame-options','DENY'),('referrer-policy','same-origin')]:
            self.assertEqual(page.headers[header],value)

    def test_home_configuration_example_is_json(self):
        page = self.client.get('/')
        snippet = re.search(r'<pre class="snippet">(.*?)</pre>', page.text, re.S).group(1)
        config = json.loads(unescape(re.sub(r'<[^>]+>', '', snippet)))
        self.assertEqual(config['bearer_token'], 'REPLACE_WITH_YOUR_MCP_TOKEN')

    def test_null_origin_stays_denied_for_native_form_endpoints(self):
        nonce = self.csrf(self.client.get('/admin/login'))
        denied = self.client.post('/admin/login',data={'username':'owner','password':self.password,'csrf':nonce},headers={'Origin':'null'})
        self.assertEqual(denied.status_code,403)
        self.assertEqual(self.login().status_code,303)
        nonce = self.csrf(self.client.get('/admin'))
        before = self.server.read_bytes()
        for path in ['/issue','/revoke','/admin/logout']:
            response = self.client.post(path,data={'csrf':nonce,'identity':'existing-agent','confirm':'yes'},headers={'Origin':'null'})
            self.assertEqual(response.status_code,403,path)
        self.assertEqual(self.server.read_bytes(),before)
        self.assertEqual(self.client.get('/admin').status_code,200)

    def test_success_during_another_failed_login_does_not_crash_retry(self):
        other = self.client_for(self.app)
        nonce = self.csrf(other.get('/admin/login'))
        started, release = threading.Event(), threading.Event()
        original = token_desk._password_ok

        def verify(data, user, password):
            if password == 'delayed-wrong':
                started.set()
                if not release.wait(10):
                    raise RuntimeError('fixture coordination timeout')
            return original(data,user,password)

        with patch.object(token_desk,'_password_ok',side_effect=verify), concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            bad = pool.submit(other.post,'/admin/login',data={'username':'owner','password':'delayed-wrong','csrf':nonce},headers={'Origin':self.settings.origin})
            try:
                self.assertTrue(started.wait(10))
                self.assertEqual(self.login().status_code,303)
            finally:
                release.set()
            retry = bad.result(timeout=15)
        self.assertEqual(retry.status_code,401)
        self.assertIn('管理员名称或口令错误',retry.text)
        self.assertEqual(self.client.get('/admin').status_code,200)
        new_nonce = self.csrf(retry)
        self.assertNotEqual(nonce,new_nonce)
        self.assertEqual(other.post('/admin/login',data={'username':'owner','password':self.password,'csrf':new_nonce},headers={'Origin':self.settings.origin}).status_code,303)

    def test_https_peer_host_origin_and_proxy_headers(self):
        self.assertEqual(self.client_for(self.app,scheme='http').get('/').status_code,403)
        external = self.client_for(self.app,peer='203.0.113.12')
        self.assertEqual(external.get('/',headers={'X-Forwarded-For':'10.8.61.201','X-Forwarded-Proto':'https'}).status_code,403)
        self.assertEqual(self.client.get('/',headers={'Host':'evil.example:3029'}).status_code,421)
        self.assertEqual(self.client.get('/',headers={'Origin':'https://evil.example'}).status_code,403)

    def test_login_secure_cookie_challenge_and_session_rotation(self):
        page = self.client.get('/admin/login')
        self.assertIn('Secure',page.headers['set-cookie'])
        self.assertIn('HttpOnly',page.headers['set-cookie'])
        self.assertIn('SameSite=strict',page.headers['set-cookie'])
        self.assertEqual(self.post('/admin/login',{'username':'owner','password':self.password,'csrf':'wrong'}).status_code,403)
        self.assertEqual(self.login(password='invalid-password').status_code,401)
        result = self.login()
        self.assertEqual(result.status_code,303)
        self.assertIn(COOKIE,self.client.cookies)
        page = self.client.get('/admin')
        self.assertEqual(page.status_code,200)
        self.assertIn('existing-agent',page.text)
        self.assertNotIn('a'*48,page.text)

    def test_missing_or_corrupt_admin_fails_closed(self):
        for content in ['{}','[]','{',json.dumps({'username':'owner','algorithm':'pbkdf2-sha256','iterations':1})]:
            self.admin.write_text(content,encoding='utf-8')
            self.assertEqual(self.client.get('/admin/login').status_code,503)
            self.assertEqual(self.client.get('/').status_code,200)
        self.admin.unlink()
        self.assertEqual(self.client.get('/admin/login').status_code,503)

    def test_login_rate_limit_and_window_expiry(self):
        for _ in range(5):
            self.assertEqual(self.login(password='wrong').status_code,401)
        self.assertEqual(self.login().status_code,429)
        self.now += 901
        self.assertEqual(self.login().status_code,303)

    def test_refresh_and_cookie_clearing_cannot_exhaust_other_peer_login(self):
        first = self.csrf(self.client.get('/admin/login'))
        for _ in range(512):
            page = self.client.get('/admin/login')
            self.assertEqual(page.status_code,200)
            self.assertEqual(self.csrf(page),first)
        self.assertEqual(self.client_for(self.app,peer='10.8.61.202').get('/admin/login').status_code,200)
        for _ in range(7):
            self.client.cookies.clear()
            self.assertEqual(self.client.get('/admin/login').status_code,200)
        self.client.cookies.clear()
        self.assertEqual(self.client.get('/admin/login').status_code,429)
        other = self.client_for(self.app,peer='10.8.61.203')
        self.assertEqual(self.login(other).status_code,303)
        self.now += 601
        self.assertEqual(self.client.get('/admin/login').status_code,200)

    def test_challenge_is_bound_to_peer_and_not_refreshed_past_expiry(self):
        nonce = self.csrf(self.client.get('/admin/login'))
        other = self.client_for(self.app,peer='10.8.61.202')
        other.cookies.set(PREAUTH,nonce)
        data={'csrf':nonce,'username':'owner','password':self.password}
        self.assertEqual(other.post('/admin/login',data=data,headers={'Origin':self.settings.origin}).status_code,403)
        nonce = self.csrf(self.client.get('/admin/login'))
        self.now += 601
        self.assertNotEqual(self.csrf(self.client.get('/admin/login')),nonce)

    def test_login_challenge_replay_and_binding(self):
        nonce = self.csrf(self.client.get('/admin/login'))
        another = self.client_for(self.app)
        self.assertEqual(another.post('/admin/login',data={'csrf':nonce,'username':'owner','password':self.password},headers={'Origin':self.settings.origin}).status_code,403)
        data={'csrf':nonce,'username':'owner','password':self.password}
        self.assertEqual(self.post('/admin/login',data).status_code,303)
        self.assertEqual(self.post('/admin/login',data).status_code,403)

    def test_session_expiry_logout_and_credential_change(self):
        self.login()
        self.now += 1201
        self.assertEqual(self.client.get('/admin').status_code,303)
        self.login()
        csrf = self.csrf(self.client.get('/admin'))
        self.assertEqual(self.post('/admin/logout',{'csrf':csrf}).status_code,303)
        self.assertEqual(self.client.get('/admin').status_code,303)
        self.login()
        configure_admin('owner','a-new-owner-password-123456',self.admin)
        self.assertEqual(self.client.get('/admin').status_code,303)

    def test_absolute_session_expiry_even_when_active(self):
        self.login()
        for _ in range(28):
            self.now += 1000
            self.assertEqual(self.client.get('/admin').status_code,200)
        self.now += 1000
        self.assertEqual(self.client.get('/admin').status_code,303)

    def test_credential_replacement_between_reads_cannot_bless_old_login(self):
        challenge = self.csrf(self.client.get('/admin/login'))
        original_read = token_desk.read_object
        rotated = False
        def rotate_after_snapshot(path):
            nonlocal rotated
            data = original_read(path)
            if path == self.admin and not rotated:
                rotated = True
                configure_admin('owner','replacement-owner-password-123456',self.admin)
            return data
        with patch.object(token_desk,'read_object',side_effect=rotate_after_snapshot):
            response = self.post('/admin/login',{'username':'owner','password':self.password,'csrf':challenge})
        self.assertTrue(rotated)
        self.assertEqual(response.status_code,303)
        self.assertEqual(self.client.get('/admin').status_code,303)
        self.assertNotIn(COOKIE,self.client.cookies)
        self.assertEqual(self.login(password='replacement-owner-password-123456').status_code,303)
        self.assertEqual(self.client.get('/admin').status_code,200)

    def test_csrf_missing_wrong_other_session_origin_and_body_limit(self):
        self.login()
        good = self.csrf(self.client.get('/admin'))
        for fields in [{'identity':'new'},{'identity':'new','csrf':'bad'}]:
            self.assertEqual(self.post('/issue',fields).status_code,403)
        another = self.client_for(self.app)
        self.login(another)
        self.assertEqual(another.post('/issue',data={'identity':'new','csrf':good},headers={'Origin':self.settings.origin}).status_code,403)
        self.assertEqual(self.client.post('/issue',data={'identity':'new','csrf':good}).status_code,403)
        self.assertEqual(self.client.post('/issue',data={'identity':'new','csrf':good},headers={'Origin':'https://evil.example'}).status_code,403)
        self.assertEqual(self.post('/issue',{'identity':'new','csrf':good,'padding':'x'*5000}).status_code,403)
        self.assertEqual(self.post('/issue',{'identity':'new','csrf':good}).status_code,200)

    def test_issue_reveal_once_duplicate_confirmed_revoke_and_audit_redaction(self):
        self.login()
        csrf = self.csrf(self.client.get('/admin'))
        with self.assertLogs('insights.token_desk',level='INFO') as logs:
            result = self.post('/issue',{'identity':'analyst-wang','csrf':csrf})
        self.assertEqual(result.status_code,200)
        token = re.search(r'<textarea[^>]*>([^<]+)</textarea>',result.text).group(1)
        self.assertGreaterEqual(len(token),32)
        self.assertNotIn(token,self.client.get('/admin').text)
        self.assertNotIn(token,' '.join(logs.output))
        self.assertNotIn(csrf,' '.join(logs.output))
        self.assertEqual(read_object(self.server)['preserved'],'setting')
        self.assertEqual(self.post('/issue',{'identity':'analyst-wang','csrf':csrf}).status_code,400)
        self.assertEqual(self.post('/revoke',{'identity':'analyst-wang','csrf':csrf}).status_code,400)
        self.assertEqual(self.post('/revoke',{'identity':'analyst-wang','csrf':csrf,'confirm':'yes'}).status_code,303)
        self.assertNotIn('analyst-wang',read_object(self.server)['tokens'])

    def test_last_token_revoked_and_reissue_without_mcp_restart(self):
        async def ok(scope,receive,send):
            await JSONResponse({'ok':True})(scope,receive,send)
        settings = MCPSettings('10.8.61.200',3037,('10.8.0.0/16',),{'existing-agent':'a'*48},Path('none'),Path('none'),Path('none'),self.server)
        mcp = TestClient(MCPAccessMiddleware(ok,settings),base_url='https://10.8.61.200:3037',client=('10.8.61.201',1234))
        revoke_token('existing-agent',self.server,self.registry)
        self.assertEqual(mcp.get('/mcp',headers={'Authorization':'Bearer '+'a'*48}).status_code,401)
        new = issue_token('new-agent',self.server,self.registry)
        self.assertEqual(mcp.get('/mcp',headers={'Authorization':'Bearer '+new}).status_code,200)
        self.assertEqual(mcp.get('/mcp').status_code,401)

    def test_corrupt_token_store_never_overwritten(self):
        for content in ['{}','[]','null','{',json.dumps({'tokens':{'one':'same'*12,'two':'same'*12}}),'{"tokens":{},"tokens":{}}']:
            self.server.write_text(content,encoding='utf-8')
            with self.assertRaises((ValueError,TypeError)):
                issue_token('new',self.server,self.registry)
            self.assertEqual(self.server.read_text(encoding='utf-8'),content)
        self.server.unlink()
        with self.assertRaises(OSError):
            issue_token('new',self.server,self.registry)

    def test_corrupt_metadata_prevents_issue_but_not_emergency_revoke(self):
        self.registry.write_text('{',encoding='utf-8')
        with self.assertRaises(ValueError):
            issue_token('new',self.server,self.registry)
        revoke_token('existing-agent',self.server,self.registry)
        self.assertEqual(read_object(self.server)['tokens'],{})

    def test_corrupt_metadata_retains_authenticated_web_emergency_revoke(self):
        self.registry.write_text('{',encoding='utf-8')
        self.assertEqual(self.login().status_code,303)
        page=self.client.get('/admin')
        self.assertEqual(page.status_code,200)
        self.assertIn('发放元数据不可用',page.text)
        self.assertIn('action="/revoke"',page.text)
        self.assertNotIn('action="/issue"',page.text)
        self.assertNotIn('a'*48,page.text)
        csrf=self.csrf(page)
        self.assertEqual(self.post('/issue',{'identity':'new','csrf':csrf}).status_code,400)
        self.assertEqual(read_object(self.server)['tokens'],{'existing-agent':'a'*48})
        self.assertEqual(self.post('/revoke',{'identity':'existing-agent','csrf':csrf,'confirm':'yes'}).status_code,303)
        self.assertEqual(read_object(self.server)['tokens'],{})
        self.assertEqual(self.client.get('/admin').status_code,200)
        self.assertEqual(self.registry.read_text(encoding='utf-8'),'{')

    def test_corrupt_authorization_still_stops_web_management(self):
        self.login()
        self.server.write_text('{',encoding='utf-8')
        self.assertEqual(self.client.get('/admin').status_code,503)
        self.assertEqual(self.server.read_text(encoding='utf-8'),'{')

    def test_thread_concurrency_and_same_identity_conflict(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results=list(pool.map(lambda i:issue_token('agent-'+str(i),self.server,self.registry),range(20)))
        self.assertEqual(len(set(results)),20)
        self.assertEqual(len(token_rows(self.server,self.registry)),21)
        def same(_):
            try:
                issue_token('same',self.server,self.registry)
                return True
            except ValueError:
                return False
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            self.assertEqual(sum(pool.map(same,range(8))),1)

    def test_cross_process_concurrency_has_no_lost_updates(self):
        code='from pathlib import Path; from insights.mcp_tokens import issue_token; import sys; issue_token(sys.argv[1],Path(sys.argv[2]),Path(sys.argv[3]))'
        processes=[subprocess.Popen([sys.executable,'-c',code,'process-'+str(i),str(self.server),str(self.registry)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL) for i in range(6)]
        self.assertTrue(all(process.wait(timeout=30)==0 for process in processes))
        self.assertEqual(len(read_object(self.server)['tokens']),7)

    def test_download_allowlist_and_no_traversal(self):
        (self.root/'tools-schema.json').write_text('{"tools":[]}',encoding='utf-8')
        self.assertEqual(self.client.get('/downloads/tools-schema.json').status_code,200)
        for path in ['/downloads/server.json','/downloads/..%2Fserver.json','/downloads/%2E%2E%5Cserver.json','/assets/token-desk-admin.json']:
            self.assertEqual(self.client.get(path).status_code,404)


if __name__=='__main__':
    unittest.main()
