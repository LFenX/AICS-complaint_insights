from __future__ import annotations

import hashlib
from pathlib import Path

from psycopg import sql

from .config import ROOT, Settings
from .db import target_connection
from .source import TABLES


def initialize_database(settings: Settings, passwords: dict[str, str]) -> None:
    settings.validate()
    with target_connection(settings, owner=True) as conn:
        # This marker belongs exclusively to the separately named analytics database.
        for path in sorted((ROOT / "sql").glob("*.sql")):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            exists = conn.execute("SELECT to_regclass('sync.schema_migrations') AS value").fetchone()["value"]
            previous = conn.execute("SELECT sha256 FROM sync.schema_migrations WHERE name=%s", (path.name,)).fetchone() if exists else None
            if previous:
                if previous["sha256"] != digest:
                    raise RuntimeError("applied migration was modified: " + path.name)
                continue
            conn.execute(path.read_text(encoding="utf-8"))
            conn.execute("INSERT INTO sync.schema_migrations(name,sha256) VALUES(%s,%s)", (path.name,digest))
        for table in TABLES:
            conn.execute(sql.SQL("CREATE TABLE IF NOT EXISTS {}.{} (source_id text NOT NULL,record_key text NOT NULL,payload jsonb NOT NULL,content_hash text NOT NULL,synced_at timestamptz NOT NULL DEFAULT now(),deleted_at timestamptz,PRIMARY KEY(source_id,record_key))").format(sql.Identifier(table.mirror_schema),sql.Identifier(table.name)))
        indexes = [("source_app","InboundMail","inbound_source_pk","sourcePk"), ("source_app","MailAiArtifact","artifact_inbound","inboundMailId"),
                   ("source_app","MailIssueBinding","binding_artifact","mailAiArtifactId"), ("source_mail","attachments","attachment_mail","message_pk")]
        for schema,table,index,field in indexes:
            conn.execute(sql.SQL("CREATE INDEX IF NOT EXISTS {} ON {}.{} (source_id, (payload->>{})) WHERE deleted_at IS NULL").format(sql.Identifier(index),sql.Identifier(schema),sql.Identifier(table),sql.Literal(field)))
        conn.execute('''CREATE OR REPLACE VIEW analysis.v_mail_details AS
            SELECT f.*,m.payload->>'body_plain_text' AS body_plain_text,m.payload->>'body_html' AS body_html,
                   m.payload->>'date_header' AS date_header,m.payload->'internal_date' AS source_internal_date,
                   m.payload->'to_json' AS recipients,m.payload->'cc_json' AS cc,
                   m.payload->'in_reply_to' AS in_reply_to,m.payload->'references_json' AS references_json,
                   m.payload->'raw_payload' AS raw_payload,
                   a.payload->'bodyOriginal' AS ai_body_original,a.payload->'bodyTranslated' AS body_translated,
                   a.payload->>'translation' AS translation_state,a.payload->'issues' AS ai_issues,
                   a.payload->'fields' AS ai_fields,a.payload->'secondaryCategories' AS secondary_categories,
                   a.payload->>'issueTypeCandidate' AS issue_type_candidate,
                   a.payload->>'resolutionStatus' AS resolution_status,
                   a.payload->>'replyDecision' AS reply_decision,a.payload->>'replyGroupKey' AS reply_group_key,
                   m.payload AS raw_record,a.payload AS ai_record
            FROM analysis.mail_fact f
            JOIN source_mail.messages m ON m.source_id=f.source_id AND m.record_key=f.mail_pk::text AND m.deleted_at IS NULL
            LEFT JOIN source_app."MailAiArtifact" a ON a.source_id=f.source_id AND a.record_key=f.ai_artifact_id AND a.deleted_at IS NULL''')
        conn.execute("CREATE OR REPLACE VIEW analysis.v_attachments AS SELECT source_id,payload->>'message_pk' AS mail_pk,payload FROM source_mail.attachments WHERE deleted_at IS NULL")
        conn.execute("CREATE OR REPLACE VIEW analysis.v_archives AS SELECT source_id,record_key AS old_message_pk,payload FROM source_mail.imap_reconcile_archive WHERE deleted_at IS NULL")
        branches = [sql.SQL("SELECT source_id,{}::text AS source_domain,{}::text AS source_table,record_key,payload,synced_at,deleted_at FROM {}.{}").format(sql.Literal(table.domain),sql.Literal(table.name),sql.Identifier(table.mirror_schema),sql.Identifier(table.name)) for table in TABLES]
        conn.execute(sql.SQL("CREATE OR REPLACE VIEW analysis.v_source_records AS ")+sql.SQL(" UNION ALL ").join(branches))
        for name in ("insights_sync","insights_reader"):
            existing = conn.execute("SELECT 1 FROM pg_roles WHERE rolname=%s",(name,)).fetchone()
            if not existing:
                conn.execute(sql.SQL("CREATE ROLE {} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS PASSWORD {}").format(sql.Identifier(name),sql.Literal(passwords[name])))
            conn.execute(sql.SQL("ALTER ROLE {} CONNECTION LIMIT {}").format(sql.Identifier(name),sql.Literal(4 if name=="insights_sync" else 8)))
        database = conn.info.dbname
        conn.execute(sql.SQL("REVOKE ALL ON DATABASE {} FROM PUBLIC").format(sql.Identifier(database)))
        conn.execute(sql.SQL("GRANT CONNECT,TEMPORARY ON DATABASE {} TO insights_sync").format(sql.Identifier(database)))
        conn.execute(sql.SQL("GRANT CONNECT ON DATABASE {} TO insights_reader").format(sql.Identifier(database)))
        conn.execute("REVOKE ALL ON SCHEMA public FROM PUBLIC")
        for schema in ("sync","source_mail","source_app","analysis"):
            conn.execute(sql.SQL("REVOKE ALL ON SCHEMA {} FROM PUBLIC").format(sql.Identifier(schema)))
            conn.execute(sql.SQL("GRANT USAGE ON SCHEMA {} TO insights_sync").format(sql.Identifier(schema)))
            conn.execute(sql.SQL("GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA {} TO insights_sync").format(sql.Identifier(schema)))
            conn.execute(sql.SQL("GRANT USAGE,SELECT ON ALL SEQUENCES IN SCHEMA {} TO insights_sync").format(sql.Identifier(schema)))
        conn.execute("GRANT USAGE ON SCHEMA analysis TO insights_reader")
        conn.execute("GRANT SELECT ON ALL TABLES IN SCHEMA analysis TO insights_reader")
        conn.execute("ALTER ROLE insights_reader SET default_transaction_read_only=on")
        conn.execute("ALTER ROLE insights_reader SET statement_timeout='15s'")
        conn.execute("ALTER ROLE insights_sync SET statement_timeout='120s'")
