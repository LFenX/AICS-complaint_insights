"""Exercise the installed reader's output budget and lossless field pages."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
READER = Path(os.environ.get('CODEX_HOME', str(Path.home()/'.codex')))/'skills/complaint-daily-report/scripts/read_packet.py'


@unittest.skipUnless(READER.is_file(), 'installed complaint-daily-report reader required')
class DailySkillReaderTests(unittest.TestCase):
    def setUp(self):
        parent = Path(os.environ.get('INSIGHTS_READER_TEST_ROOT', str(ROOT/'.runtime')))
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='daily-reader-test-', dir=parent)
        self.directory = Path(self.temp.name).resolve()
        self.assertTrue(self.directory.is_relative_to((ROOT/'.runtime').resolve()))
        self.addCleanup(self.temp.cleanup)
        self.long = {'mail_pk': '1', 'from_address': 'player@example.test', 'mailbox': 'support@example.test',
            'subject': '完整主题'*8000, 'summary_zh': '完整源摘要'*5000, 'body_plain_text': '完整正文'*7000,
            'received_at': '2026-10-28T11:20:00+08:00'}
        self.packet = {'business_date': '2026-10-28', 'mails': [self.long, {'mail_pk': '2', 'subject': 'Small subject', 'body_plain_text': 'Small body'}, {'mail_pk': '3', 'subject': 'Another small subject', 'body_plain_text': 'Another small body'}], 'attachments': [], 'conversation_context': []}
        self.source = self.directory/'source.json'
        self.source.write_text(json.dumps(self.packet, ensure_ascii=False), 'utf-8')

    def run_reader(self, *args):
        result = subprocess.run([sys.executable, str(READER), '--project-root', str(ROOT), '--snapshot', str(self.source), *args], capture_output=True, text=True, encoding='utf-8', cwd=ROOT, env={**os.environ, 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}, check=True)
        return json.loads(result.stdout), len(result.stdout)

    def field(self, field):
        parts, offset = [], 0
        while offset is not None:
            value, _ = self.run_reader('--mode', 'field', '--mail-pk', '1', '--field', field, '--offset', str(offset), '--max-chars', '16000')
            self.assertLessEqual(len(value['text']), 16000)
            parts.append(value['text'])
            self.assertTrue(value['next_offset'] is None or value['next_offset'] > offset)
            offset = value['next_offset']
        return ''.join(parts)

    def test_long_subject_and_metadata_are_bounded_and_have_complete_followups(self):
        for mode in ['index', 'batch']:
            value, length = self.run_reader('--mode', mode, '--limit', '1', '--max-chars', '1000')
            self.assertLessEqual(sum(len(json.dumps(row, ensure_ascii=False)) for row in value['records']), 1000)
            self.assertLess(length, 2200)
            self.assertEqual(value['records'][0]['mail_pk'], '1')
            self.assertTrue(value['records'][0]['requires_field_pagination'])
            self.assertTrue({'subject', 'metadata'}.issubset(value['required_followups'][0]['fields']))
            self.assertFalse(value['body_included'])
        self.assertEqual(self.field('subject'), self.long['subject'])
        metadata = json.loads(self.field('metadata'))
        self.assertEqual(metadata['summary_zh'], self.long['summary_zh'])
        self.assertEqual(metadata['from_address'], self.long['from_address'])
        self.assertEqual(metadata['mailbox'], self.long['mailbox'])
        self.assertEqual(metadata['received_at'], self.long['received_at'])
        self.assertEqual(self.field('body'), self.long['body_plain_text'])

    def test_minimum_budget_still_advances_without_losing_mail_ids(self):
        for mode in ['index', 'batch']:
            offset, seen = 0, []
            while offset is not None:
                value, length = self.run_reader('--mode', mode, '--limit', '2', '--max-chars', '100', '--offset', str(offset))
                self.assertLess(length, 1400)
                self.assertLessEqual(sum(len(json.dumps(row, ensure_ascii=False)) for row in value['records']), 100)
                self.assertTrue(value['records'])
                seen.extend(row['mail_pk'] for row in value['records'])
                self.assertTrue(value['next_offset'] is None or value['next_offset'] > offset)
                offset = value['next_offset']
            self.assertEqual(seen, ['1', '2', '3'])


if __name__ == '__main__':
    unittest.main()
