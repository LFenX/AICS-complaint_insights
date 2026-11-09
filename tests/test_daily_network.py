"""LAN access is explicit and read-only; TCP identity cannot be forwarded."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from starlette.testclient import TestClient

from insights.daily_board import BoardNetwork, create_app, serve_board


class DailyNetworkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.report = self.folder / 'report.json'
        self.report.write_text(json.dumps({'coverage': {'expected': 1}, 'records': [
            {'id': '1', 'summary': '合成摘要', 'body': 'synthetic detail', 'files': [
                {'id': '9', 'ready': True, 'preview_type': 'text', 'name': 'fixture.log',
                 'content_type': 'text/plain'}]}]}), encoding='utf-8')
        files = self.folder / 'attachments'
        files.mkdir()
        (files / '9.bin').write_bytes(b'synthetic log')
        (files / '9.txt').write_bytes(b'synthetic log preview')
        self.network = BoardNetwork('192.168.10.20', ('192.168.10.0/24',))

    def client(self, peer='192.168.10.21', host='192.168.10.20'):
        return TestClient(create_app(self.report, network=self.network),
                          base_url=f'http://{host}:3030', client=(peer, 1234))

    def test_config_is_opt_in_and_unknown_or_unsafe_settings_fail(self):
        path = self.folder / 'network.json'
        self.assertEqual(BoardNetwork.load(path).bind_hosts, ('127.0.0.1',))
        path.write_text(json.dumps({'lan_host': self.network.lan_host,
                                    'allowed_networks': list(self.network.allowed_networks)}), encoding='utf-8')
        self.assertEqual(BoardNetwork.load(path), self.network)
        for value in [[], {}, {'lan_host': None, 'allowed_networks': []},
                      {'lan_host': self.network.lan_host, 'allowed_networks': '192.168.10.0/24'},
                      {'lan_host': self.network.lan_host, 'allowed_networks': [], 'proxy': True}]:
            path.write_text(json.dumps(value), encoding='utf-8')
            with self.subTest(value=value), self.assertRaises(ValueError):
                BoardNetwork.load(path)
        for host, networks in [('0.0.0.0', ('0.0.0.0/0',)), ('8.8.8.8', ('8.8.8.0/24',)),
                               ('127.0.0.1', ('127.0.0.0/8',)), ('169.254.2.3', ('169.254.0.0/16',)),
                               ('192.168.10.20', ()), ('192.168.10.20', ('0.0.0.0/0',)),
                               ('192.168.10.20', ('192.168.20.0/24',)),
                               ('192.168.10.20', ('192.168.10.21/24',)),
                               ('192.168.10.20', ('192.168.10.0/24', '192.168.10.0/24'))]:
            with self.subTest(host=host, networks=networks), self.assertRaises(ValueError):
                BoardNetwork(host, networks)

    def test_lan_reader_and_local_operator_can_read_the_same_model_and_files(self):
        for client in [self.client(), self.client('127.0.0.1', '127.0.0.1'),
                       self.client('127.0.0.1', 'localhost')]:
            with self.subTest(base=client.base_url):
                response = client.get('/data.json', headers={'Origin': str(client.base_url).rstrip('/')})
                self.assertEqual(response.status_code, 200)
                self.assertNotIn('body', response.json()['records'][0])
                self.assertEqual(client.get('/mail/1').json()['body'], 'synthetic detail')
                self.assertEqual(client.get('/file/9').content, b'synthetic log')
                self.assertEqual(client.get('/file/9/preview').content, b'synthetic log preview')

    def test_disallowed_real_peer_is_rejected_even_when_proxy_headers_claim_lan(self):
        for peer in ['192.168.11.21', '203.0.113.9', '100.64.0.1', '::ffff:192.168.10.21', 'testclient']:
            with self.subTest(peer=peer):
                response = self.client(peer).get('/data.json', headers={
                    'X-Forwarded-For': '192.168.10.21', 'Forwarded': 'for=192.168.10.21'})
                self.assertEqual(response.status_code, 403)
        self.assertEqual(TestClient(create_app(self.report), base_url='http://192.168.10.20:3030',
                                    client=('192.168.10.21', 1234)).get('/data.json').status_code, 403)

    def test_lan_host_origin_and_method_are_checked_on_every_resource(self):
        client = self.client()
        for path in ['/', '/data.json', '/mail/1', '/file/9', '/file/9/preview', '/log-archive/' + 'a'*64]:
            for headers in [{'Host': '127.0.0.1:3030'}, {'Host': '192.168.10.20:80'},
                            {'Host': 'evil.example:3030'}, {'Origin': 'http://localhost:3030'},
                            {'Origin': 'null'}, {'Origin': 'http://192.168.10.20:3030.evil.example'}]:
                with self.subTest(path=path, headers=headers):
                    self.assertEqual(client.get(path, headers=headers).status_code, 403)
            self.assertEqual(client.post(path).status_code, 405)
        with patch.dict('os.environ', {'INSIGHTS_DAILY_BOARD_ENABLED': '0'}):
            self.assertEqual(client.get('/').status_code, 503)

    def test_audit_identifies_network_audience_without_recording_mail_content(self):
        with self.assertLogs('insights.daily_board', level='INFO') as captured:
            response = self.client().get('/mail/1')
        self.assertEqual(response.status_code, 200)
        record = json.loads(captured.records[-1].getMessage())
        self.assertEqual((record['identity'], record['peer']), ('lan-reader', '192.168.10.21'))
        self.assertEqual(record['action'], 'daily-report.read')
        self.assertNotIn('synthetic detail', str(captured.output))
        self.assertNotIn('合成摘要', str(captured.output))

    def test_bind_failure_closes_every_socket_and_never_starts_partial_server(self):
        first, second = MagicMock(), MagicMock()
        second.bind.side_effect = OSError('fixture address unavailable')
        with patch('insights.daily_board.BoardNetwork.load', return_value=self.network), \
             patch('insights.daily_board.socket.socket', side_effect=[first, second]), \
             patch('uvicorn.Server') as server:
            first.__enter__.return_value = first
            second.__enter__.return_value = second
            with self.assertRaises(OSError):
                serve_board()
            server.assert_not_called()
            first.__exit__.assert_called_once()
            second.__exit__.assert_called_once()

    def test_both_sockets_share_app_and_disable_uvicorn_proxy_identity(self):
        first, second = MagicMock(), MagicMock()
        with patch('insights.daily_board.BoardNetwork.load', return_value=self.network), \
             patch('insights.daily_board.socket.socket', side_effect=[first, second]), \
             patch('uvicorn.Config', wraps=__import__('uvicorn').Config) as config, \
             patch('uvicorn.Server') as server:
            first.__enter__.return_value = first
            second.__enter__.return_value = second
            serve_board()
            first.bind.assert_called_once_with(('127.0.0.1', 3030))
            second.bind.assert_called_once_with(('192.168.10.20', 3030))
            self.assertFalse(config.call_args.kwargs['proxy_headers'])
            server.return_value.run.assert_called_once_with(sockets=[first, second])


PAGE_DIRECTIVES = ("default-src 'self'", "script-src 'self'", "style-src 'self' 'unsafe-inline'",
                   "img-src 'self' data:", "media-src 'self'", "frame-src 'self'", "object-src 'none'",
                   "base-uri 'none'")


def header_values(response, name):
    return [value.decode() for key, value in response.headers.raw if key.lower() == name.encode()]


class FrameAncestorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.report = self.folder / 'report.json'
        self.report.write_text(json.dumps({'coverage': {'expected': 1}, 'records': [
            {'id': '1', 'summary': '合成摘要', 'body': 'synthetic detail', 'files': [
                {'id': '9', 'ready': True, 'preview_type': 'text', 'name': 'fixture.log',
                 'content_type': 'text/plain'}]}]}), encoding='utf-8')
        files = self.folder / 'attachments'
        files.mkdir()
        (files / '9.bin').write_bytes(b'synthetic log')
        (files / '9.txt').write_bytes(b'synthetic log preview')
        self.path = self.folder / 'network.json'
        self.base = {'lan_host': '10.8.61.200', 'allowed_networks': ['10.8.0.0/16']}

    def write_config(self, value):
        self.path.write_text(json.dumps(value), encoding='utf-8')

    def client(self, network, peer='10.8.20.8', host='10.8.61.200'):
        return TestClient(create_app(self.report, network=network),
                          base_url=f'http://{host}:3030', client=(peer, 1234))

    def test_missing_or_empty_allowlist_keeps_embedding_disabled(self):
        self.write_config(self.base)
        loaded = BoardNetwork.load(self.path)
        self.assertEqual(loaded.frame_ancestor_origins, ())
        self.write_config({**self.base, 'frame_ancestor_origins': []})
        self.assertEqual(BoardNetwork.load(self.path).frame_ancestor_origins, ())
        response = self.client(loaded).get('/')
        self.assertEqual(header_values(response, 'content-security-policy'),
                         [loaded.document_csp()])
        self.assertIn("frame-ancestors 'none'", response.headers['content-security-policy'])
        for directive in PAGE_DIRECTIVES:
            self.assertIn(directive, response.headers['content-security-policy'])
        self.assertEqual(header_values(response, 'x-frame-options'), [])
        self.assertEqual(header_values(response, 'access-control-allow-origin'), [])
        self.assertEqual(response.headers['cross-origin-resource-policy'], 'same-origin')
        self.assertEqual(self.client(loaded).get(
            '/', headers={'Origin': 'http://10.8.45.155'}).status_code, 403)

    def test_configured_parent_is_exact_and_does_not_open_the_network(self):
        network = BoardNetwork('10.8.61.200', ('10.8.0.0/16',), ('http://10.8.45.155',))
        client = self.client(network)
        allowed = client.get('/', headers={'Origin': 'http://10.8.45.155'})
        self.assertEqual(allowed.status_code, 200)
        policy = allowed.headers['content-security-policy']
        self.assertEqual(header_values(allowed, 'content-security-policy'), [policy])
        self.assertIn('frame-ancestors http://10.8.45.155', policy)
        self.assertNotIn("frame-ancestors 'none'", policy)
        self.assertNotIn('*', policy.split('frame-ancestors', 1)[1])
        for directive in PAGE_DIRECTIVES:
            self.assertIn(directive, policy)
        self.assertEqual(header_values(allowed, 'x-frame-options'), [])
        self.assertEqual(header_values(allowed, 'access-control-allow-origin'), [])
        self.assertEqual(allowed.headers['cache-control'], 'no-store')
        self.assertEqual(allowed.headers['x-content-type-options'], 'nosniff')
        self.assertEqual(allowed.headers['referrer-policy'], 'no-referrer')
        self.assertEqual(allowed.headers['cross-origin-resource-policy'], 'same-origin')
        for origin in ['http://10.8.45.155:3025', 'https://10.8.45.155', 'http://10.8.45.156',
                       'http://10.8.45.155.evil.example', 'http://evil.example/?http://10.8.45.155',
                       'null', 'http://10.8.45.155/', '*']:
            with self.subTest(origin=origin):
                self.assertEqual(client.get('/data.json', headers={'Origin': origin}).status_code, 403)
        self.assertEqual(self.client(network, peer='203.0.113.9').get(
            '/', headers={'Origin': 'http://10.8.45.155'}).status_code, 403)
        self.assertEqual(client.get('/', headers={'Host': 'evil.example:3030',
                                                   'Origin': 'http://10.8.45.155'}).status_code, 403)
        self.assertEqual(client.post('/', headers={'Origin': 'http://10.8.45.155'}).status_code, 405)
        self.assertEqual(client.get('/data.json').status_code, 200)
        download = client.get('/file/9', headers={'Origin': 'http://10.8.45.155'})
        self.assertEqual(header_values(download, 'content-security-policy'), ["default-src 'none'; sandbox"])
        self.assertIn('attachment', download.headers['content-disposition'])
        self.assertEqual(download.headers['cross-origin-resource-policy'], 'same-origin')

    def test_default_port_is_the_same_origin_and_other_ports_stay_distinct(self):
        self.write_config({**self.base, 'frame_ancestor_origins': ['http://10.8.45.155:80']})
        loaded = BoardNetwork.load(self.path)
        self.assertEqual(loaded.frame_ancestor_origins, ('http://10.8.45.155',))
        client = self.client(loaded)
        self.assertEqual(client.get('/', headers={'Origin': 'http://10.8.45.155'}).status_code, 200)
        self.assertEqual(client.get('/', headers={'Origin': 'http://10.8.45.155:3025'}).status_code, 403)
        explicit = BoardNetwork('10.8.61.200', ('10.8.0.0/16',), ('http://10.8.45.155:3025',))
        self.assertEqual(self.client(explicit).get(
            '/', headers={'Origin': 'http://10.8.45.155'}).status_code, 403)
        self.assertEqual(self.client(explicit).get(
            '/', headers={'Origin': 'http://10.8.45.155:3025'}).status_code, 200)

    def test_local_machine_origins_match_only_their_exact_default_port(self):
        origins = ('http://10.8.45.155', 'http://127.0.0.1', 'http://localhost', 'http://10.8.61.200',
                   'http://127.0.0.1:3016', 'http://localhost:3016', 'http://10.8.61.200:3016')
        network = BoardNetwork('10.8.61.200', ('10.8.0.0/16',), origins)
        client = self.client(network)
        policy = client.get('/').headers['content-security-policy']
        self.assertIn('frame-ancestors ' + ' '.join(origins), policy)
        self.assertEqual(header_values(client.get('/'), 'content-security-policy'), [policy])
        for origin in origins:
            with self.subTest(origin=origin):
                self.assertEqual(client.get('/', headers={'Origin': origin}).status_code, 200)
        for origin in ('http://127.0.0.1:3025', 'http://localhost:8080', 'http://10.8.61.201',
                       'https://127.0.0.1', 'http://10.8.61.200:3030', 'http://10.8.61.200:3017'):
            with self.subTest(origin=origin):
                self.assertEqual(self.client(network, peer='127.0.0.1', host='127.0.0.1').get(
                    '/', headers={'Origin': origin}).status_code, 403)

    def test_illegal_frame_ancestor_configuration_is_rejected(self):
        illegal = ['*', 'http://*', 'http://10.8.45.155:*', 'http://10.8.45.155/', 'http://10.8.45.155/board',
                   'http://10.8.45.155?embed=1', 'http://10.8.45.155#top', 'http://user@10.8.45.155',
                   '', '10.8.45.155', 'ftp://10.8.45.155', 'http://10.8.45.155:0', 'http://10.8.45.155:65536',
                   'http://[::1]', 'http://10.8.45.155; default-src *', ' http://10.8.45.155',
                   'http://*.example.com', 'http://10.8.45.155.']
        for origin in illegal:
            self.write_config({**self.base, 'frame_ancestor_origins': [origin]})
            with self.subTest(origin=origin), self.assertRaises(ValueError) as caught:
                BoardNetwork.load(self.path)
            self.assertIn('invalid frame ancestor origin', str(caught.exception))
        for value in [None, 'http://10.8.45.155', {'origin': 'http://10.8.45.155'}, [80]]:
            self.write_config({**self.base, 'frame_ancestor_origins': value})
            with self.subTest(value=value), self.assertRaises(ValueError):
                BoardNetwork.load(self.path)
        self.write_config({**self.base, 'frame_ancestor_origins': ['http://10.8.45.155', 'http://10.8.45.155:80']})
        with self.assertRaises(ValueError) as duplicate:
            BoardNetwork.load(self.path)
        self.assertIn('unique', str(duplicate.exception))
        with self.assertRaises(ValueError) as mutable:
            BoardNetwork('10.8.61.200', ('10.8.0.0/16',), ['http://10.8.45.155'])
        self.assertIn('immutable tuple', str(mutable.exception))
        self.write_config({**self.base, 'frame_ancestor_origins': ['http://10.8.45.155'], 'proxy': True})
        with self.assertRaises(ValueError) as unknown:
            BoardNetwork.load(self.path)
        self.assertIn('frame_ancestor_origins', str(unknown.exception))


if __name__ == '__main__':
    unittest.main()
