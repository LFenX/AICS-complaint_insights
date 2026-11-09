from dataclasses import replace
from datetime import datetime,timezone
from pathlib import Path
import unittest
from unittest.mock import patch

from insights.config import Settings,clean_source_url,connection_identity
from insights.model import folder_track,project_mail
from insights.time_rules import detect_fallback_skew,received_at,SHANGHAI
from insights.api import decode_cursor,encode_cursor,safe_integers
from insights.capabilities import PERMISSIONS,CAPABILITIES


class RulesTests(unittest.TestCase):
    def test_mixed_legacy_time_is_corrected_per_row(self):
        rows=[{"internal_date":"2026-10-01T16:30:00Z","date_header":"Thu, 01 Oct 2026 16:30:00 +0000"}]*9
        rows += [{"internal_date":"2026-10-02T00:30:00Z","date_header":"Thu, 01 Oct 2026 16:30:00 +0000"}]
        self.assertEqual(detect_fallback_skew(rows),0)
        corrected,shift=received_at(rows[-1],0)
        self.assertEqual(shift,8)
        self.assertEqual(corrected,datetime(2026,10,1,16,30,tzinfo=timezone.utc))
        self.assertEqual(str(corrected.astimezone(SHANGHAI).date()),"2026-10-02")

    def test_missing_internal_time_uses_ingestion_time(self):
        instant,shift=received_at({"first_seen_at":"2026-10-01T16:01:00Z"},8)
        self.assertEqual(shift,0)
        self.assertEqual(str(instant.astimezone(SHANGHAI).date()),"2026-10-02")

    def test_no_date_header_uses_measured_fallback(self):
        instant,shift=received_at({"internal_date":"2026-10-02T00:30:00Z"},8)
        self.assertEqual(shift,8)
        self.assertEqual(instant.hour,16)

    def test_folder_aliases_and_utf7(self):
        self.assertEqual(folder_track("&XfJT0ZAB-"),"SENT")
        self.assertEqual(folder_track("[Gmail]/Sent Mail"),"SENT")
        self.assertEqual(folder_track("INBOX"),"INBOX")
        self.assertEqual(folder_track("已删除"),"TRASH")

    def project(self,ai=None,bindings=None):
        return project_mail("fixture-source",{"id":1,"mailbox_id":1,"folder_id":"INBOX","internal_date":"2026-10-01T16:00:00Z"},{"id":"mail-1"},ai,bindings or [],{"1":"fixture@example.invalid"},{},0)

    def test_unanalyzed_mail_is_preserved(self):
        fact,issues=self.project()
        self.assertEqual(fact["analysis_state"],"UNANALYZED")
        self.assertEqual(fact["level_one"],"PEND")
        self.assertEqual(len(issues),1)
        self.assertTrue(issues[0]["is_primary"])

    def test_normalized_pipeline_category_is_not_manual(self):
        fact,_=self.project({"id":"a1","categoryAi":"ACC.OTHER","category":"PAY.OTHER","categorySource":"AI","analysisState":"DONE"})
        self.assertEqual(fact["category_ai"],"ACC.OTHER")
        self.assertEqual(fact["category_normalized"],"PAY.OTHER")
        self.assertEqual(fact["level_one"],"PAY")

    def test_manual_source_is_not_adopted(self):
        fact,issues=self.project({"id":"a1","categoryAi":"ACC.OTHER","category":"PAY.OTHER","categorySource":"MANUAL","analysisState":"DONE"},[{"id":"b1","source":"MANUAL","issuePointKey":"i1","levelOne":"PAY"}])
        self.assertEqual(fact["level_one"],"ACC")
        self.assertEqual(issues[0]["issue_point_key"],"__primary__")

    def test_pending_analysis_keeps_suggestion_but_not_final_bucket(self):
        fact,_=self.project({"categoryAi":"ACC.OTHER","category":"ACC.OTHER","categorySource":"AI","analysisState":"PENDING"})
        self.assertEqual(fact["category_ai"],"ACC.OTHER")
        self.assertEqual(fact["level_one"],"PEND")

    def test_source_url_removes_only_prisma_options(self):
        value=clean_source_url("postgresql://reader:example@127.0.0.1:5432/db?schema=complaint_app&connection_limit=2&pool_timeout=5&sslmode=verify-full")
        self.assertIn("sslmode=verify-full",value)
        self.assertNotIn("schema=",value)

    def test_cursor_is_signed_and_tamper_is_rejected(self):
        secret="x"*48
        encoded=encode_cursor(secret,{"version":1,"last":["2026-10-01","10"]})
        self.assertEqual(decode_cursor(secret,encoded)["version"],1)
        with self.assertRaises(Exception): decode_cursor("y"*48,encoded)

    def test_large_integer_json_is_lossless(self):
        self.assertEqual(safe_integers({"id":9007199254740993,"ok":True}),{"id":"9007199254740993","ok":True})

    def test_permissions_have_complete_parent_chain(self):
        for capability in CAPABILITIES.values():
            current=capability["permission"]; seen=set()
            while current is not None:
                self.assertNotIn(current,seen)
                seen.add(current)
                current=PERMISSIONS[current]

    def test_production_profile_is_disabled(self):
        settings=Settings.load()
        candidate=replace(settings,source_url="postgresql://reader:placeholder@10.8.45.155:5432/ai_complaint_mail",environment="production")
        with self.assertRaisesRegex(ValueError,"disabled"): candidate.validate(source=True)

    def test_api_cannot_bind_to_lan(self):
        with self.assertRaisesRegex(ValueError,"loopback"): replace(Settings.load(),api_host="0.0.0.0").validate()

    def test_source_and_target_cannot_be_identical(self):
        settings=Settings.load()
        with self.assertRaisesRegex(ValueError,"differ"): replace(settings,source_url=settings.target_owner_url).validate(source=True)

    def test_writer_cannot_be_redirected_to_original_database(self):
        settings=Settings.load()
        with self.assertRaisesRegex(ValueError,"isolated"): replace(settings,target_writer_url=settings.source_url).validate()

    def test_libpq_url_destination_overrides_are_rejected(self):
        settings=Settings.load()
        for option in ("hostaddr=10.8.45.155", "service=unexpected-service"):
            separator="&" if "?" in settings.source_url else "?"
            candidate=replace(settings,source_url=settings.source_url+separator+option)
            with self.assertRaisesRegex(ValueError,"overrides"):
                candidate.validate(source=True)
            with self.assertRaisesRegex(ValueError,"overrides"):
                _=candidate.identity_hash
            target=replace(settings,target_writer_url=settings.target_writer_url+"?"+option)
            with self.assertRaisesRegex(ValueError,"overrides"):
                target.validate()

    def test_libpq_environment_destination_overrides_are_rejected(self):
        settings=Settings.load()
        for name,value in (("PGHOSTADDR","203.0.113.1"),("PGSERVICE","unexpected-service")):
            with patch.dict("os.environ",{name:value}):
                with self.assertRaisesRegex(ValueError,"overrides"):
                    settings.validate(source=True)

    def test_implicit_libpq_destination_is_rejected(self):
        settings=Settings.load()
        cases=(
            ("postgresql://placeholder@/synthetic",{"PGHOST":"203.0.113.1","PGPORT":"6543"}),
            ("postgresql://placeholder@127.0.0.1/synthetic",{"PGPORT":"6543"}),
            ("postgresql://placeholder@203.0.113.1:5432",{"PGDATABASE":"synthetic"}),
        )
        for url,env in cases:
            candidate=replace(settings,source_url=url)
            with patch.dict("os.environ",env):
                with self.assertRaisesRegex(ValueError,"explicit"):
                    candidate.validate(source=True)
                with self.assertRaisesRegex(ValueError,"explicit"):
                    _=candidate.identity_hash
        writer="postgresql://insights_sync:placeholder@127.0.0.1/complaint_insights"
        with patch.dict("os.environ",{"PGPORT":"5432"}):
            with self.assertRaisesRegex(ValueError,"explicit"):
                replace(settings,target_writer_url=writer).validate()

    def test_explicit_destination_ignores_environment_defaults(self):
        settings=Settings.load()
        with patch.dict("os.environ",{"PGHOST":"203.0.113.1","PGPORT":"6543","PGDATABASE":"synthetic"}):
            settings.validate(source=True)
            self.assertEqual(connection_identity(settings.source_url),{"host":"127.0.0.1","port":"5432","dbname":"ai_complaint_mail"})
            self.assertEqual(connection_identity(settings.target_owner_url)["port"],"15433")


if __name__=="__main__": unittest.main()
