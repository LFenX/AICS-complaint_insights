"""Real PostgreSQL tests, exclusively in disposable databases in the NEW instance.

Never execute fixtures, truncation or writes against the existing development source.
"""
from __future__ import annotations

from dataclasses import replace
from datetime import datetime,timezone,timedelta
from pathlib import Path
import json
import tempfile
import unittest
import uuid
from urllib.parse import urlsplit,urlunsplit

from fastapi.testclient import TestClient
import psycopg
from psycopg import sql

from insights.api import create_app
from insights.config import ROOT,Settings
from insights.db import source_connection,target_connection
from insights.initialize import initialize_database
from insights.source import TABLES
from insights.syncer import sync_once


def database_url(url,name):
    parsed=urlsplit(url)
    return urlunsplit((parsed.scheme,parsed.netloc,"/"+name,parsed.query,parsed.fragment))


class DatabaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=Settings.load()
        suffix=uuid.uuid4().hex[:10]
        cls.source_db="complaint_insights_source_test_"+suffix
        cls.target_db="complaint_insights_test_"+suffix
        cls.settings=replace(cls.base,source_id="fixture-local",source_url=database_url(cls.base.target_owner_url,cls.source_db),
                             target_owner_url=database_url(cls.base.target_owner_url,cls.target_db),
                             target_writer_url=database_url(cls.base.target_writer_url,cls.target_db),
                             target_reader_url=database_url(cls.base.target_reader_url,cls.target_db),auxiliary_seconds=1)
        with psycopg.connect(cls.base.target_owner_url,autocommit=True) as conn:
            for name in [cls.source_db,cls.target_db]:
                assert name.startswith("complaint_insights_") and name!="complaint_insights"
                conn.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(name)))
        passwords=json.loads((ROOT/".secrets/role-passwords.json").read_text(encoding="utf-8"))
        initialize_database(cls.settings,passwords)
        with psycopg.connect(cls.settings.source_url) as conn:
            cls.create_fixture_schema(conn)

    @classmethod
    def tearDownClass(cls):
        with psycopg.connect(cls.base.target_owner_url,autocommit=True) as conn:
            for name in [cls.source_db,cls.target_db]:
                assert name.startswith("complaint_insights_") and name!="complaint_insights"
                conn.execute(sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(name)))

    @staticmethod
    def create_fixture_schema(conn):
        conn.execute("CREATE SCHEMA complaint_app")
        definitions={
            "mailboxes":"id bigint PRIMARY KEY,email text",
            "folders":"id bigint PRIMARY KEY,mailbox_id bigint,folder_id text,name text",
            "messages":"id bigint PRIMARY KEY,mailbox_id bigint,message_id text,folder_id text,subject text,from_address text,internal_date timestamptz,date_header text,first_seen_at timestamptz DEFAULT now(),last_fetched_at timestamptz DEFAULT now(),body_plain_text text,body_html text,raw_payload jsonb DEFAULT '{}',has_attachment boolean DEFAULT false,smtp_message_id text,in_reply_to text,references_json jsonb DEFAULT '[]',thread_id text,to_json jsonb DEFAULT '[]',cc_json jsonb DEFAULT '[]'",
            "attachments":"id bigint PRIMARY KEY,message_pk bigint,filename text,download_status text",
            "imap_reconcile_archive":"old_message_pk bigint PRIMARY KEY,active_message_pk bigint,old_message jsonb,old_ai_artifact jsonb,ai_disposition text",
            "InboundMail":'id text PRIMARY KEY,"sourcePk" bigint,"receivedAt" timestamp',
            "MailAiArtifact":'id text PRIMARY KEY,"inboundMailId" text,"categoryAi" text,"category" text,"categorySource" text DEFAULT \'AI\',"priorityAi" text,"intent" text,"analysisState" text,"analysisVersion" text,"taxonomyGroupId" text,"summaryZh" text,"bodyOriginal" jsonb,"bodyTranslated" jsonb,"updatedAt" timestamp DEFAULT now()',
            "MailIssueBinding":'id text PRIMARY KEY,"mailAiArtifactId" text,"issuePointKey" text,"catalogIssueTypeId" text,"candidateId" text,"levelOne" text,"levelTwo" text,"isPrimary" boolean,"bindingStatus" text,source text DEFAULT \'AI\',"updatedAt" timestamp DEFAULT now()',
            "TaxonomyCandidate":'id text PRIMARY KEY,name text,"levelOne" text,"levelTwo" text,status text,"updatedAt" timestamp DEFAULT now()',
            "IssueTypeProposal":'id text PRIMARY KEY,"mailAiArtifactId" text,"candidateId" text,"updatedAt" timestamp DEFAULT now()',
            "TaxonomyCandidateSupport":'id text PRIMARY KEY,"candidateId" text,"mailAiArtifactId" text,"createdAt" timestamp DEFAULT now()',
            "IssueTypeRegistry":'id text PRIMARY KEY,"canonicalName" text,"canonicalParentCategory" text,status text',
            "IssueTypeAlias":'id text PRIMARY KEY,"registryId" text,alias text',
            "IssueGroupLifecycle":'"groupKey" text PRIMARY KEY,"archivedAt" timestamp',
        }
        for item in TABLES:
            schema="public" if item.domain=="mail" else "complaint_app"
            conn.execute(sql.SQL("CREATE TABLE {}.{} ({})").format(sql.Identifier(schema),sql.Identifier(item.name),sql.SQL(definitions[item.name])))
        conn.execute("CREATE TABLE public.message_change_log(id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,message_pk bigint,operation char(1),changed_at timestamptz DEFAULT clock_timestamp())")
        conn.execute('CREATE TABLE complaint_app."MailboxAppChange"(id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,"mailId" text,"sourceTable" text,"changedAt" timestamp DEFAULT now())')
        conn.execute("""CREATE FUNCTION public.fixture_mail_event() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN
            IF TG_OP='DELETE' THEN INSERT INTO public.message_change_log(message_pk,operation) VALUES(OLD.id,'D');RETURN OLD;
            ELSE INSERT INTO public.message_change_log(message_pk,operation) VALUES(NEW.id,CASE WHEN TG_OP='INSERT' THEN 'I' ELSE 'U' END);RETURN NEW;END IF;END $$""")
        conn.execute("CREATE TRIGGER fixture_mail AFTER INSERT OR UPDATE OR DELETE ON public.messages FOR EACH ROW EXECUTE FUNCTION public.fixture_mail_event()")
        conn.execute('''CREATE FUNCTION complaint_app.fixture_app_event() RETURNS trigger LANGUAGE plpgsql AS $$ DECLARE p jsonb;m text;BEGIN
            p=CASE WHEN TG_OP='DELETE' THEN to_jsonb(OLD) ELSE to_jsonb(NEW) END;
            m=CASE WHEN TG_TABLE_NAME='InboundMail' THEN p->>'id' ELSE p->>'inboundMailId' END;
            INSERT INTO complaint_app."MailboxAppChange"("mailId","sourceTable") VALUES(m,TG_TABLE_NAME);
            IF TG_OP='DELETE' THEN RETURN OLD;ELSE RETURN NEW;END IF;END $$''')
        for name in ["InboundMail","MailAiArtifact"]:
            conn.execute(sql.SQL('CREATE TRIGGER fixture_app AFTER INSERT OR UPDATE OR DELETE ON complaint_app.{} FOR EACH ROW EXECUTE FUNCTION complaint_app.fixture_app_event()').format(sql.Identifier(name)))

    def setUp(self):
        with psycopg.connect(self.settings.source_url) as conn:
            self.assertEqual(conn.info.dbname,self.source_db)
            for schema in ["public","complaint_app"]:
                names=conn.execute("SELECT tablename FROM pg_tables WHERE schemaname=%s",(schema,)).fetchall()
                for (name,) in names:
                    conn.execute(sql.SQL("TRUNCATE {}.{} RESTART IDENTITY CASCADE").format(sql.Identifier(schema),sql.Identifier(name)))
            conn.execute("INSERT INTO public.mailboxes VALUES(1,'fixture@example.invalid')")
            self.insert_mail(conn,1)
            self.insert_mail(conn,2,folder="Sent",day="2026-10-02T01:00:00Z")
            self.insert_mail(conn,3,day="2026-10-02T03:00:00Z")
            self.analyze(conn,1)
        with target_connection(self.settings,owner=True) as conn:
            self.assertEqual(conn.info.dbname,self.target_db)
            names=conn.execute("SELECT schemaname,tablename FROM pg_tables WHERE schemaname IN ('source_mail','source_app','analysis','sync') AND tablename<>'schema_migrations'").fetchall()
            for row in names:
                conn.execute(sql.SQL("TRUNCATE {}.{} RESTART IDENTITY CASCADE").format(sql.Identifier(row["schemaname"]),sql.Identifier(row["tablename"])))
        sync_once(self.settings)

    @staticmethod
    def insert_mail(conn,pk,folder="INBOX",day="2026-10-01T16:30:00Z"):
        conn.execute("INSERT INTO public.messages(id,mailbox_id,message_id,folder_id,subject,from_address,internal_date,body_plain_text) VALUES(%s,1,%s,%s,'fixture subject','sender@example.invalid',%s,'original fixture body')",(pk,f"fixture-{pk}",folder,day))

    @staticmethod
    def analyze(conn,pk):
        conn.execute('INSERT INTO complaint_app."InboundMail"(id,"sourcePk") VALUES(%s,%s)',(f"mail-{pk}",pk))
        conn.execute('''INSERT INTO complaint_app."MailAiArtifact"(id,"inboundMailId","categoryAi","category","priorityAi","analysisState","analysisVersion","taxonomyGroupId","summaryZh","bodyOriginal","bodyTranslated") VALUES(%s,%s,'ACC.OTHER','ACC.LINKNEW','P2','DONE','fixture-v1','ADJ-ACC-01','fixture summary','["original fixture body"]','["translated fixture body"]')''',(f"ai-{pk}",f"mail-{pk}"))
        conn.execute('''INSERT INTO complaint_app."MailIssueBinding"(id,"mailAiArtifactId","issuePointKey","catalogIssueTypeId","levelOne","levelTwo","isPrimary","bindingStatus") VALUES(%s,%s,'issue-1','ADJ-ACC-01','ACC','ACC.LINKNEW',true,'BOUND')''',(f"binding-{pk}",f"ai-{pk}"))

    def source_write(self,query,args=()):
        with psycopg.connect(self.settings.source_url) as conn:
            self.assertEqual(conn.info.dbname,self.source_db)
            conn.execute(query,args)

    def state(self):
        with target_connection(self.settings,reader=True) as conn:
            return conn.execute("SELECT * FROM analysis.v_sync_status WHERE source_id=%s",(self.settings.source_id,)).fetchone()

    def facts(self):
        with target_connection(self.settings,reader=True) as conn:
            return conn.execute("SELECT * FROM analysis.mail_fact WHERE source_id=%s ORDER BY mail_pk",(self.settings.source_id,)).fetchall()

    def client(self,settings=None):
        return TestClient(create_app(settings or self.settings))

    @property
    def headers(self): return {"Authorization":"Bearer "+self.settings.api_token}

    def test_mail_backlog_over_5000_does_not_skip_first_unread_event(self):
        settings=replace(self.settings,auxiliary_seconds=86400,reconcile_seconds=86400)
        with psycopg.connect(settings.source_url) as conn:
            self.insert_mail(conn,4)
            conn.execute("INSERT INTO public.message_change_log(message_pk,operation) SELECT 1,'U' FROM generate_series(1,5100)")
        sync_once(settings)
        self.assertIn(4,{r['mail_pk'] for r in self.facts()})
        checkpoint=self.state()['source_event_id']
        self.assertGreater(checkpoint,5000)
        sync_once(settings)
        self.assertIn(4,{r['mail_pk'] for r in self.facts()})

    def test_app_backlog_over_5000_preserves_earliest_artifact_change(self):
        settings=replace(self.settings,auxiliary_seconds=86400,reconcile_seconds=86400)
        with psycopg.connect(settings.source_url) as conn:
            self.analyze(conn,3)
            conn.execute('''INSERT INTO complaint_app."MailboxAppChange"("mailId","sourceTable") SELECT 'mail-1','MailAiArtifact' FROM generate_series(1,5100)''')
        result=sync_once(settings)
        self.assertEqual(result['mode'],'INCREMENTAL')
        fact=next(r for r in self.facts() if r['mail_pk']==3)
        self.assertEqual(fact['ai_artifact_id'],'ai-3')
        self.assertEqual(fact['analysis_state'],'DONE')

    def test_initial_import_counts_and_source_fields(self):
        rows=self.facts()
        self.assertEqual(len(rows),3)
        self.assertEqual(str(rows[0]["business_date"]),"2026-10-02")
        self.assertEqual(rows[0]["category_ai"],"ACC.OTHER")
        self.assertEqual(rows[0]["category_normalized"],"ACC.LINKNEW")
        self.assertEqual(rows[1]["direction"],"SENT")
        self.assertEqual(rows[2]["analysis_state"],"UNANALYZED")

    def test_incremental_insert_update_delete_and_resume(self):
        prior=self.state()
        with psycopg.connect(self.settings.source_url) as conn:
            self.insert_mail(conn,4)
            conn.execute("UPDATE public.messages SET body_plain_text='changed body' WHERE id=1")
            conn.execute("DELETE FROM public.messages WHERE id=2")
        result=sync_once(replace(self.settings))
        self.assertEqual([row["mail_pk"] for row in self.facts()],[1,3,4])
        self.assertGreater(result["data_version"],prior["data_version"])
        body=self.client().get('/v1/mails/1',headers=self.headers).json()["mail"]["body_plain_text"]
        self.assertEqual(body,"changed body")
        stable=sync_once(replace(self.settings))
        self.assertEqual(stable["changed_rows"],0)
        self.assertEqual(stable["data_version"],result["data_version"])

    def test_late_ai_completion_updates_original_received_day(self):
        with psycopg.connect(self.settings.source_url) as conn: self.analyze(conn,3)
        sync_once(self.settings)
        self.assertEqual(self.facts()[-1]["analysis_state"],"DONE")
        self.assertEqual(str(self.facts()[-1]["business_date"]),"2026-10-02")

    def test_ai_reclassification_replaces_old_bucket(self):
        with psycopg.connect(self.settings.source_url) as conn:
            conn.execute('''UPDATE complaint_app."MailAiArtifact" SET "category"='PAY.OTHER',"categoryAi"='PAY.OTHER',"taxonomyGroupId"=NULL WHERE id='ai-1' ''')
            conn.execute('''DELETE FROM complaint_app."MailIssueBinding" WHERE "mailAiArtifactId"='ai-1' ''')
        sync_once(self.settings)
        rows=self.client().get('/v1/daily?start=2026-10-01&end=2026-10-03',headers=self.headers).json()['items']
        self.assertFalse(any(row['level_one']=='ACC' for row in rows))
        self.assertEqual(next(row['mail_count'] for row in rows if row['level_one']=='PAY'),1)

    def test_removing_ai_keeps_raw_mail_as_unanalyzed(self):
        self.source_write('DELETE FROM complaint_app."MailAiArtifact" WHERE id=\'ai-1\'')
        sync_once(self.settings)
        self.assertEqual(len(self.facts()),3)
        self.assertEqual(self.facts()[0]['analysis_state'],'UNANALYZED')

    def test_unlogged_category_binding_attachment_and_support_changes(self):
        with psycopg.connect(self.settings.source_url) as conn:
            conn.execute("INSERT INTO public.attachments VALUES(1,1,'fixture.txt','done')")
            conn.execute('''INSERT INTO complaint_app."TaxonomyCandidate"(id,name,"levelOne","levelTwo",status) VALUES('candidate-1','fixture category','ACC','ACC.LINKNEW','PENDING')''')
            conn.execute('''UPDATE complaint_app."MailIssueBinding" SET "candidateId"='candidate-1',"catalogIssueTypeId"=NULL WHERE id='binding-1' ''')
            conn.execute('''INSERT INTO complaint_app."TaxonomyCandidateSupport"(id,"candidateId","mailAiArtifactId") VALUES('support-1','candidate-1','ai-1')''')
        with target_connection(self.settings,owner=True) as conn:
            conn.execute("UPDATE sync.sources SET last_aux_at=now()-interval '5 minutes'")
        sync_once(self.settings)
        self.assertEqual(self.facts()[0]["issue_type_id"],"candidate-1")
        detail=self.client().get('/v1/mails/1',headers=self.headers).json()
        self.assertEqual(len(detail["attachments"]),1)
        self.source_write('DELETE FROM complaint_app."TaxonomyCandidateSupport" WHERE id=\'support-1\'')
        sync_once(self.settings,force_reconcile=True)
        with target_connection(self.settings,reader=True) as conn:
            count=conn.execute("SELECT count(*) AS n FROM analysis.v_source_records WHERE source_id=%s AND source_table='TaxonomyCandidateSupport' AND deleted_at IS NULL",(self.settings.source_id,)).fetchone()["n"]
        self.assertEqual(count,0)

    def test_atomic_failure_does_not_advance_data_or_cursor(self):
        before=self.state()
        with psycopg.connect(self.settings.source_url) as conn: self.insert_mail(conn,4)
        with self.assertRaisesRegex(RuntimeError,"injected"):
            sync_once(self.settings,fail_before_publish=True)
        after=self.state()
        self.assertEqual(after["data_version"],before["data_version"])
        self.assertEqual(after["source_event_id"],before["source_event_id"])
        self.assertEqual(len(self.facts()),3)
        self.assertEqual(after["status"],"DEGRADED")
        sync_once(replace(self.settings))
        self.assertEqual(len(self.facts()),4)
        self.assertEqual(self.state()["status"],"READY")

    def test_catalog_failures_preserve_data_and_record_degraded_then_recover(self):
        before=self.state()
        with tempfile.TemporaryDirectory(prefix="insights-catalog-test-") as directory:
            broken=replace(self.settings,catalog_dir=directory)
            for invalid_json,expected_error in ((False,"FileNotFoundError"),(True,"JSONDecodeError")):
                if invalid_json:
                    Path(directory,"taxonomy-v2.json").write_text("{broken",encoding="utf-8")
                with self.assertRaises((FileNotFoundError,json.JSONDecodeError)):
                    sync_once(broken)
                after=self.state()
                self.assertEqual(after["status"],"DEGRADED")
                self.assertEqual(after["last_error_code"],expected_error)
                self.assertEqual(after["data_version"],before["data_version"])
                self.assertEqual(after["source_event_id"],before["source_event_id"])
                self.assertEqual(len(self.facts()),3)
                with target_connection(self.settings,reader=True) as conn:
                    latest=conn.execute("SELECT status,error_code FROM analysis.v_sync_runs WHERE source_id=%s ORDER BY id DESC LIMIT 1",(self.settings.source_id,)).fetchone()
                self.assertEqual(latest,{"status":"FAILED","error_code":expected_error})
        sync_once(self.settings)
        self.assertEqual(self.state()["status"],"READY")
        self.assertIsNone(self.state()["last_error_code"])

    def test_reconcile_recovers_pruned_log_window(self):
        with psycopg.connect(self.settings.source_url) as conn:
            conn.execute("TRUNCATE public.message_change_log RESTART IDENTITY")
            conn.execute("UPDATE public.messages SET subject='changed without prior log' WHERE id=1")
        sync_once(self.settings)
        self.assertEqual(self.facts()[0]["subject"],"changed without prior log")

    def test_full_reconcile_recovers_events_older_than_tail(self):
        with psycopg.connect(self.settings.source_url) as conn:
            conn.execute("INSERT INTO public.message_change_log(id,message_pk,operation) VALUES(10000,1,'U')")
        sync_once(self.settings)
        with psycopg.connect(self.settings.source_url) as conn:
            self.insert_mail(conn,4)
        # Event id 4 is older than the bounded 5000-id tail. Its recovery relies
        # on the explicitly scheduled full reconciliation, not a false CDC promise.
        sync_once(self.settings,force_reconcile=True)
        self.assertEqual(len(self.facts()),4)

    def test_missing_required_source_column_fails_without_publication(self):
        before=self.state()
        self.source_write('ALTER TABLE complaint_app."MailAiArtifact" RENAME COLUMN "categoryAi" TO "removedCategoryAi"')
        try:
            with self.assertRaisesRegex(RuntimeError,'missing columns'): sync_once(self.settings)
            self.assertEqual(self.state()['data_version'],before['data_version'])
            self.assertEqual(len(self.facts()),3)
        finally:
            self.source_write('ALTER TABLE complaint_app."MailAiArtifact" RENAME COLUMN "removedCategoryAi" TO "categoryAi"')

    def test_out_of_order_commits_are_caught_by_log_tail(self):
        delayed=psycopg.connect(self.settings.source_url)
        try:
            self.insert_mail(delayed,4)
            with psycopg.connect(self.settings.source_url) as conn: self.insert_mail(conn,5)
            sync_once(self.settings)
            self.assertEqual([row["mail_pk"] for row in self.facts()],[1,2,3,5])
            delayed.commit()
            sync_once(self.settings)
            self.assertEqual([row["mail_pk"] for row in self.facts()],[1,2,3,4,5])
        finally: delayed.close()

    def test_archive_is_preserved_without_duplicate_current_mail(self):
        with psycopg.connect(self.settings.source_url) as conn:
            conn.execute("INSERT INTO public.imap_reconcile_archive VALUES(2,1,'{\"id\":2}','{}','archived')")
            conn.execute("DELETE FROM public.messages WHERE id=2")
        sync_once(self.settings,force_reconcile=True)
        self.assertEqual(len(self.facts()),2)
        self.assertEqual(self.client().get('/v1/mails/2',headers=self.headers).status_code,410)
        with target_connection(self.settings,reader=True) as conn:
            self.assertEqual(conn.execute("SELECT count(*) AS n FROM analysis.v_archives WHERE source_id=%s",(self.settings.source_id,)).fetchone()["n"],1)

    def test_source_namespace_isolation_and_identity_binding(self):
        second=replace(self.settings,source_id="fixture-second")
        sync_once(second)
        with target_connection(self.settings,reader=True) as conn:
            self.assertEqual(conn.execute("SELECT count(*) AS n FROM analysis.mail_fact").fetchone()["n"],6)
        different=replace(self.settings,source_url=self.settings.source_url.replace('127.0.0.1','localhost'))
        with self.assertRaisesRegex(ValueError,"different connection"): sync_once(different)
        self.assertEqual(len(self.facts()),3)

    def test_source_connection_rejects_writes(self):
        with self.assertRaises(psycopg.errors.ReadOnlySqlTransaction):
            with source_connection(self.settings) as conn:
                conn.execute("INSERT INTO public.mailboxes VALUES(999,'blocked@example.invalid')")

    def test_reader_has_no_write_even_after_readonly_is_disabled(self):
        with self.assertRaises(psycopg.errors.InsufficientPrivilege):
            with target_connection(self.settings,reader=True) as conn:
                conn.execute("SET TRANSACTION READ WRITE")
                conn.execute("DELETE FROM analysis.mail_fact WHERE false")
        with self.assertRaises(psycopg.errors.InsufficientPrivilege):
            with target_connection(self.settings,reader=True) as conn:
                conn.execute("SELECT * FROM source_mail.messages LIMIT 1")

    def test_authentication_parameter_validation_and_sql_injection(self):
        client=self.client()
        for path in ['/health','/openapi.json','/v1/capabilities','/v1/mails','/v1/taxonomy','/v1/sync/status']:
            self.assertEqual(client.get(path).status_code,401,path)
            self.assertEqual(client.get(path,headers={'Authorization':'Bearer invalid'}).status_code,401,path)
        self.assertEqual(client.post('/v1/mails',headers=self.headers).status_code,405)
        self.assertEqual(client.get('/v1/mails?limit=10000',headers=self.headers).status_code,422)
        self.assertEqual(client.get('/v1/daily?start=2026-10-03&end=2026-10-01',headers=self.headers).status_code,422)
        self.assertEqual(client.get('/v1/mails',params={'level_one':"ACC' OR 1=1--"},headers=self.headers).json()["items"],[])

    def test_pagination_is_complete_signed_and_revision_bound(self):
        client=self.client()
        first=client.get('/v1/mails?limit=2',headers=self.headers).json()
        second=client.get('/v1/mails',params={'limit':2,'cursor':first["next_cursor"]},headers=self.headers).json()
        self.assertEqual([row['mail_pk'] for row in first['items']+second['items']],['1','2','3'])
        self.assertEqual(client.get('/v1/mails',params={'cursor':first['next_cursor']+'x'},headers=self.headers).status_code,422)
        with psycopg.connect(self.settings.source_url) as conn: self.insert_mail(conn,4)
        sync_once(self.settings)
        self.assertEqual(client.get('/v1/mails',params={'cursor':first['next_cursor']},headers=self.headers).status_code,409)

    def test_parent_rollup_deduplicates_multi_issue_mail(self):
        self.source_write('''INSERT INTO complaint_app."MailIssueBinding"(id,"mailAiArtifactId","issuePointKey","catalogIssueTypeId","levelOne","levelTwo","isPrimary","bindingStatus") VALUES('binding-second','ai-1','issue-2','ADJ-ACC-03','ACC','ACC.LINKNEW',false,'BOUND')''')
        sync_once(self.settings,force_reconcile=True)
        client=self.client()
        rows=client.get('/v1/daily?start=2026-10-01&end=2026-10-03&level=1&scope=all_issues',headers=self.headers).json()['items']
        acc=next(row for row in rows if row['level_one']=='ACC')
        self.assertEqual(acc['mail_count'],1)
        self.assertEqual(acc['issue_count'],2)
        # Default incoming excludes the sent fixture but retains the unanalyzed one.
        self.assertEqual(sum(row['mail_count'] for row in rows),2)

    def test_secondary_category_context_has_correct_group(self):
        self.source_write('''INSERT INTO complaint_app."MailIssueBinding"(id,"mailAiArtifactId","issuePointKey","catalogIssueTypeId","levelOne","levelTwo","isPrimary","bindingStatus") VALUES('binding-second','ai-1','issue-2','unknown-pay','PAY','PAY.OTHER',false,'BOUND')''')
        sync_once(self.settings,force_reconcile=True)
        response=self.client().get('/v1/report-context?start=2026-10-01&end=2026-10-03&scope=all_issues&level_one=PAY&include_body=true',headers=self.headers)
        self.assertEqual(response.status_code,200)
        category=response.json()['days'][0]['categories'][0]
        self.assertEqual(category['category_id'],'PAY.OTHER')
        self.assertEqual(category['mails'][0]['body_plain_text'],'original fixture body')

    def test_read_api_works_without_source_connection(self):
        settings=replace(self.settings,source_url='postgresql://unavailable@127.0.0.1:1/not_connected')
        self.assertEqual(self.client(settings).get('/v1/mails/1',headers=self.headers).status_code,200)

    def test_bigint_primary_key_does_not_lose_precision(self):
        pk=9007199254740993
        with psycopg.connect(self.settings.source_url) as conn: self.insert_mail(conn,pk)
        sync_once(self.settings)
        response=self.client().get('/v1/mails/'+str(pk)+'?include_raw=true',headers=self.headers)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['mail']['mail_pk'],str(pk))
        self.assertEqual(response.json()['mail']['raw_record']['id'],str(pk))

    def test_openapi_and_capabilities_are_queryable(self):
        client=self.client()
        self.assertIn('/v1/report-context',client.get('/openapi.json',headers=self.headers).json()['paths'])
        caps=client.get('/v1/capabilities',headers=self.headers).json()
        self.assertTrue(caps['capabilities']['mails']['enabled'])
        self.assertEqual(client.get('/v1/mails/1?include_raw=true',headers=self.headers).json()['mail']['raw_record']['body_plain_text'],'original fixture body')

    def test_source_table_allowlist_auth_and_raw_content(self):
        client=self.client()
        self.assertEqual(client.get('/v1/source-tables').status_code,401)
        self.assertEqual(client.get('/v1/source-records?table=messages').status_code,401)
        catalog=client.get('/v1/source-tables',headers=self.headers).json()['items']
        self.assertEqual(len(catalog),14)
        self.assertEqual(next(row['key_field'] for row in catalog if row['table']=='imap_reconcile_archive'),'old_message_pk')
        page=client.get('/v1/source-records?table=messages',headers=self.headers).json()
        self.assertNotIn('payload',page['items'][0])
        detail=client.get('/v1/source-records',params={'table':'messages','record_key':'1','include_payload':True},headers=self.headers).json()
        self.assertEqual(detail['items'][0]['payload']['body_plain_text'],'original fixture body')
        self.assertEqual(client.get('/v1/source-records',params={'table':"messages' OR 1=1--"},headers=self.headers).status_code,422)
        self.assertEqual(client.get('/v1/source-records',params={'table':'messages','record_key':"1' OR 1=1--"},headers=self.headers).json()['items'],[])
        self.assertEqual(client.get('/v1/source-records?table=messages&limit=51',headers=self.headers).status_code,422)

    def test_source_record_pagination_filters_and_version_binding(self):
        client=self.client()
        first=client.get('/v1/source-records?table=messages&limit=2',headers=self.headers).json()
        second=client.get('/v1/source-records',params={'table':'messages','cursor':first['next_cursor']},headers=self.headers).json()
        self.assertEqual([row['record_key'] for row in first['items']+second['items']],['1','2','3'])
        self.assertEqual(client.get('/v1/source-records',params={'table':'messages','include_payload':True,'cursor':first['next_cursor']},headers=self.headers).status_code,422)
        self.source_write("UPDATE public.messages SET subject='revision change' WHERE id=1")
        sync_once(self.settings)
        self.assertEqual(client.get('/v1/source-records',params={'table':'messages','cursor':first['next_cursor']},headers=self.headers).status_code,409)

    def test_source_record_tombstones_are_explicit_and_preserve_payload(self):
        self.source_write('DELETE FROM public.messages WHERE id=2')
        sync_once(self.settings)
        client=self.client()
        self.assertEqual(client.get('/v1/source-records?table=messages&record_key=2',headers=self.headers).json()['items'],[])
        row=client.get('/v1/source-records?table=messages&record_key=2&include_deleted=true&include_payload=true',headers=self.headers).json()['items'][0]
        self.assertIsNotNone(row['deleted_at'])
        self.assertEqual(row['payload']['id'],2)


if __name__=='__main__': unittest.main()
