"""Dated reports never fall back or share mail/file identity across dates."""
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from starlette.testclient import TestClient
from insights.daily_board import create_app


class DailyDatesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for day, text in [('2026-10-28', 'first'), ('2026-10-29', 'second')]:
            directory = self.root / day
            (directory / 'attachments').mkdir(parents=True)
            (directory / 'attachments/9.bin').write_bytes(text.encode())
            (directory / 'attachments/9.txt').write_text(text+' preview', 'utf-8')
            (directory / 'report.json').write_text(json.dumps({'business_date': day, 'coverage': {'expected': 1},
                'records': [{'id': '1', 'summary': '合成摘要', 'body': text, 'uid': {'value': '', 'state': 'not_found'}, 'files': [
                    {'id': '9', 'ready': True, 'preview_type': 'text', 'name': 'fixture.log', 'content_type': 'text/plain'}]}]}), 'utf-8')
        self.client = TestClient(create_app(reports_root=self.root), base_url='http://127.0.0.1:3030', client=('127.0.0.1', 1234))

    def test_default_is_shanghai_yesterday_and_date_label_matches_data(self):
        with patch('insights.daily_board.business_today', return_value='2026-10-30'):
            value = self.client.get('/data.json').json()
            self.assertEqual(value['business_date'], '2026-10-29')
            self.assertEqual(value['today'], '2026-10-30')
            self.assertEqual(value['default_date'], '2026-10-29')
            self.assertEqual(value['report_status'], 'generated')
            self.assertEqual(self.client.get('/mail/1').json()['body'], 'second')
            self.assertEqual(self.client.get('/file/9').text, 'second')
            self.assertEqual(value['available_dates'], ['2026-10-29', '2026-10-28'])

    def test_missing_yesterday_never_falls_back_to_an_older_report(self):
        with patch('insights.daily_board.business_today', return_value='2026-10-31'):
            value = self.client.get('/data.json').json()
            self.assertEqual(value['business_date'], '2026-10-30')
            self.assertEqual(value['report_status'], 'not_generated')
            self.assertNotIn('records', value)
            for route in ['/mail/1', '/file/9', '/file/9/preview', '/log-archive/'+'a'*64]:
                self.assertEqual(self.client.get(route).status_code, 404)

    def test_default_date_handles_month_year_and_leap_day_boundaries(self):
        for today, yesterday in [('2026-11-01', '2026-10-31'), ('2027-01-01', '2026-12-31'), ('2024-03-01', '2024-02-29')]:
            with self.subTest(today=today), patch('insights.daily_board.business_today', return_value=today):
                value = self.client.get('/data.json').json()
                self.assertEqual(value['business_date'], yesterday)
                self.assertEqual(value['default_date'], yesterday)
                self.assertEqual(value['today'], today)

    def test_explicit_today_is_not_replaced_by_yesterday(self):
        with patch('insights.daily_board.business_today', return_value='2026-10-30'):
            value = self.client.get('/data.json?date=2026-10-30').json()
            self.assertEqual(value['business_date'], '2026-10-30')
            self.assertEqual(value['default_date'], '2026-10-29')
            self.assertEqual(value['report_status'], 'not_generated')
            self.assertNotIn('records', value)

    def test_explicit_date_reads_only_its_model_and_files(self):
        for day, text in [('2026-10-28', 'first'), ('2026-10-29', 'second')]:
            overview = self.client.get('/data.json', params={'date': day}).json()
            self.assertEqual(overview['report_status'], 'generated')
            self.assertNotIn('body', overview['records'][0])
            params = {'date': day, 'v': overview['report_sha256']}
            self.assertEqual(self.client.get('/mail/1', params=params).json()['body'], text)
            self.assertEqual(self.client.get('/file/9', params=params).text, text)
            self.assertEqual(self.client.get('/file/9/preview', params=params).text, text+' preview')
        self.assertEqual(self.client.get('/file/9?date=2026-10-29&v=wrong').status_code, 409)

    def test_invalid_or_repeated_dates_fail_before_filesystem_access(self):
        for value in ['../2026-10-29', '2026-2-01', '2026-02-29', '2026-10-32', '', '0000-01-01', '2026-10-29/report.json']:
            with self.subTest(value=value):
                self.assertEqual(self.client.get('/data.json', params={'date': value}).status_code, 400)
        self.assertEqual(self.client.get('/data.json?date=2026-10-28&date=2026-10-29').status_code, 400)
        self.assertEqual(self.client.get('/data.json?date=2024-02-29').json()['report_status'], 'not_generated')

    def test_corrupt_and_misdated_models_are_failures_not_missing(self):
        path = self.root / '2026-10-29/report.json'
        path.write_text('{broken', 'utf-8')
        self.assertEqual(self.client.get('/data.json?date=2026-10-29').status_code, 503)
        other = json.loads((self.root / '2026-10-28/report.json').read_text('utf-8'))
        path.write_text(json.dumps(other), 'utf-8')
        self.assertEqual(self.client.get('/data.json?date=2026-10-29').status_code, 503)

    def test_publication_is_detected_after_missing_response_without_restart(self):
        self.assertEqual(self.client.get('/data.json?date=2026-10-27').json()['report_status'], 'not_generated')
        directory = self.root / '2026-10-27'
        directory.mkdir()
        doc = json.loads((self.root / '2026-10-28/report.json').read_text('utf-8'))
        doc['business_date'] = '2026-10-27'
        (directory / 'report.json').write_text(json.dumps(doc), 'utf-8')
        self.assertEqual(self.client.get('/data.json?date=2026-10-27').json()['report_status'], 'generated')

    def test_date_selection_keeps_identity_permission_and_audit_boundaries(self):
        with self.assertLogs('insights.daily_board', level='INFO') as captured:
            self.assertEqual(self.client.get('/data.json?date=2026-10-29').status_code, 200)
        self.assertEqual(json.loads(captured.records[-1].getMessage())['business_date'], '2026-10-29')
        self.assertNotIn('合成摘要', str(captured.output))
        self.assertEqual(self.client.get('/data.json?date=2026-10-29', headers={'Origin': 'http://evil.example'}).status_code, 403)
        with patch('insights.daily_board.LOCAL_OPERATOR_PERMISSIONS', frozenset()):
            self.assertEqual(self.client.get('/data.json?date=2026-10-29').status_code, 403)
        with patch('insights.daily_board.LOCAL_OPERATOR_PERMISSIONS', frozenset({'insights.daily_report.read'})):
            self.assertEqual(self.client.get('/file/9?date=2026-10-29').status_code, 403)

    def test_archive_and_version_use_selected_date(self):
        key = 'a'*64
        for day in ['2026-10-28', '2026-10-29']:
            folder = self.root / day
            (folder / 'archives').mkdir()
            (folder / 'archives' / (key+'.zip')).write_bytes(day.encode())
            path = folder / 'report.json'
            value = json.loads(path.read_text('utf-8'))
            value['log_archives'] = {key: {'status': 'ready', 'filename': 'logs.zip', 'file_count': 1}}
            path.write_text(json.dumps(value), 'utf-8')
            version = sha256(path.read_bytes()).hexdigest()
            self.assertEqual(self.client.get('/log-archive/'+key, params={'date': day, 'v': version}).text, day)
        self.assertEqual(self.client.get('/log-archive/'+key, params={'date': '2026-10-28', 'v': version}).status_code, 409)


if __name__ == '__main__':
    unittest.main()
