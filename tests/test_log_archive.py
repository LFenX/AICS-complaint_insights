from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

from starlette.testclient import TestClient

from insights.capabilities import CAPABILITIES, PERMISSIONS
from insights.config import ROOT
from insights.daily_board import create_app
from insights.log_archive import prepare_log_archives


class LogArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT/'.runtime')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.originals = self.root/'attachments'; self.originals.mkdir()
        self.payloads = {'10': b'private-log-A\n', '11': b'private-log-B\n', '12': b'private-log-C\n'}
        self.records = []
        for i, key in enumerate(self.payloads, 1):
            raw = self.payloads[key]; (self.originals/(key+'.bin')).write_bytes(raw)
            self.records.append({'id': str(i), 'summary': 'fixture', 'subtheme_id': 'sub-a' if i < 3 else 'sub-b',
                'files': [{'id': key, 'mail_pk': str(i), 'name': '../bad\\file.log' if i == 2 else 'Player.log',
                           'kind': 'log', 'ready': True, 'size': len(raw), 'sha256': sha256(raw).hexdigest()}]})
        self.subthemes = [{'id': k, 'name': k} for k in ['sub-a', 'sub-b', 'sub-empty']]

    def build(self):
        return prepare_log_archives(self.root/'archives', self.originals, self.records, self.subthemes,
                                    business_date='2026-10-29', source_sha256='source-fixture')

    def test_all_members_are_original_bytes_safe_named_and_bound_to_one_subissue(self):
        result = self.build()
        self.assertEqual(len(result), 2)
        self.assertIsNone(self.subthemes[2]['log_archive'])
        expected = {'sub-a': {'10', '11'}, 'sub-b': {'12'}}
        for key, meta in result.items():
            with ZipFile(self.root/'archives'/(key+'.zip')) as archive:
                manifest = json.loads(archive.read('_manifest.json'))
                self.assertEqual({f['attachment_id'] for f in manifest['files']}, expected[meta['subtheme_id']])
                self.assertEqual(len(archive.namelist()), meta['file_count']+1)
                for f in manifest['files']:
                    self.assertNotIn('..', PurePosixPath(f['entry']).parts)
                    self.assertNotIn('\\', f['entry'])
                    self.assertEqual(archive.read(f['entry']), self.payloads[f['attachment_id']])
        repeated = self.build()
        self.assertEqual({k: v['sha256'] for k, v in result.items()}, {k: v['sha256'] for k, v in repeated.items()})

    def test_incomplete_or_tampered_logs_are_not_silently_exported(self):
        self.records[0]['files'][0]['ready'] = False
        result = self.build()
        self.assertEqual(len(result), 1)
        self.assertEqual(self.subthemes[0]['log_archive']['status'], 'unavailable')
        self.records[0]['files'][0]['ready'] = True
        (self.originals/'10.bin').write_bytes(b'corrupt')
        with self.assertRaisesRegex(ValueError, 'integrity mismatch'): self.build()
        self.assertEqual(list((self.root/'archives').glob('*.tmp')), [])

    def client(self, remote=False):
        result = self.build()
        self.archive = next(iter(result))
        path = self.root/'report.json'
        raw = json.dumps({'coverage': {'expected': 3}, 'records': self.records, 'log_archives': result}).encode()
        path.write_bytes(raw)
        self.version = sha256(raw).hexdigest()
        return TestClient(create_app(path), base_url='http://127.0.0.1:3030',
                          client=('10.8.61.201', 1234) if remote else ('127.0.0.1', 1234))

    def test_version_resource_identity_feature_and_metadata_audit(self):
        client = self.client()
        path = '/log-archive/'+self.archive+'?v='+self.version
        with self.assertLogs('insights.daily_board', level='INFO') as captured:
            response = client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/zip')
        self.assertEqual(response.headers['x-log-count'], '2')
        self.assertIn('attachment', response.headers['content-disposition'])
        self.assertIn('log-archive.read', '\n'.join(captured.output))
        self.assertIn(self.archive, '\n'.join(captured.output))
        self.assertNotIn('private-log', '\n'.join(captured.output))
        with ZipFile(BytesIO(response.content)) as archive: self.assertIsNone(archive.testzip())
        self.assertEqual(client.get('/log-archive/'+self.archive+'?v=old').status_code, 409)
        self.assertEqual(client.get('/log-archive/'+'f'*64+'?v='+self.version).status_code, 404)
        self.assertEqual(client.get('/log-archive/%2e%2e%2fsecret?v='+self.version).status_code, 404)
        self.assertEqual(client.get(path, headers={'Host': 'evil.invalid'}).status_code, 403)
        self.assertEqual(client.get(path, headers={'Origin': 'https://evil.invalid'}).status_code, 403)
        self.assertEqual(client.post(path).status_code, 405)
        self.assertEqual(self.client(remote=True).get(path).status_code, 403)
        with patch.dict('os.environ', {'INSIGHTS_DAILY_LOG_ARCHIVE_ENABLED': '0'}):
            self.assertEqual(client.get(path).status_code, 503)
            feature = client.get('/data.json').json()['features']['daily_log_archive']
            self.assertFalse(feature['enabled']); self.assertTrue(feature['disabled_reason'])
        with patch('insights.daily_board.LOCAL_OPERATOR_PERMISSIONS', frozenset({'insights.daily_report.read'})):
            self.assertEqual(client.get(path).status_code, 403)
            feature = client.get('/data.json').json()['features']['daily_log_archive']
            self.assertFalse(feature['enabled']); self.assertIn('权限', feature['disabled_reason'])
        capability = CAPABILITIES['daily_log_archive']
        self.assertEqual(capability['permission'], 'insights.attachments.logs.export')
        self.assertEqual(capability['scope'], 'RESOURCE')
        chain = []
        permission = capability['permission']
        while permission:
            chain.append(permission); permission = PERMISSIONS[permission]
        self.assertEqual(chain, ['insights.attachments.logs.export', 'insights.attachments.read',
                                 'insights.mail.read', 'insights.read', 'insights'])


if __name__ == '__main__': unittest.main()
