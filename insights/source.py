from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator
import json

from psycopg import Connection, sql


@dataclass(frozen=True)
class SourceTable:
    name: str
    domain: str
    key: str = "id"
    auxiliary: bool = False

    @property
    def mirror_schema(self):
        return "source_mail" if self.domain == "mail" else "source_app"


TABLES = (
    SourceTable("mailboxes", "mail", auxiliary=True),
    SourceTable("folders", "mail", auxiliary=True),
    SourceTable("messages", "mail"),
    SourceTable("attachments", "mail", auxiliary=True),
    SourceTable("imap_reconcile_archive", "mail", "old_message_pk", True),
    SourceTable("InboundMail", "app"),
    SourceTable("MailAiArtifact", "app"),
    SourceTable("MailIssueBinding", "app", auxiliary=True),
    SourceTable("TaxonomyCandidate", "app", auxiliary=True),
    SourceTable("IssueTypeProposal", "app", auxiliary=True),
    SourceTable("TaxonomyCandidateSupport", "app", auxiliary=True),
    SourceTable("IssueTypeRegistry", "app", auxiliary=True),
    SourceTable("IssueTypeAlias", "app", auxiliary=True),
    SourceTable("IssueGroupLifecycle", "app", "groupKey", True),
)
BY_NAME = {item.name: item for item in TABLES}
REQUIRED_COLUMNS = {
    "mailboxes": {"id","email"},
    "messages": {"id","mailbox_id","message_id","folder_id","subject","from_address","internal_date","date_header","first_seen_at","body_plain_text","body_html","raw_payload"},
    "InboundMail": {"id","sourcePk"},
    "MailAiArtifact": {"id","inboundMailId","categoryAi","category","categorySource","analysisState","analysisVersion","bodyOriginal","bodyTranslated"},
    "MailIssueBinding": {"id","mailAiArtifactId","issuePointKey","source","levelOne","levelTwo","isPrimary","bindingStatus"},
    "TaxonomyCandidate": {"id","name","levelOne","levelTwo","status"},
}


def schema_of(settings, table: SourceTable) -> str:
    return settings.source_schema if table.domain == "mail" else settings.app_schema


def check_contract(conn: Connection, settings) -> dict:
    result = {"tables": {}, "read_only": conn.execute("SHOW transaction_read_only").fetchone()["transaction_read_only"]}
    if result["read_only"] != "on":
        raise RuntimeError("source transaction is not read-only")
    for item in TABLES:
        schema = schema_of(settings, item)
        columns = conn.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema=%s AND table_name=%s ORDER BY ordinal_position", (schema, item.name)).fetchall()
        missing = (REQUIRED_COLUMNS.get(item.name,set()) | {item.key}) - {row["column_name"] for row in columns}
        if missing:
            raise RuntimeError(f"source contract missing columns: {schema}.{item.name}: {','.join(sorted(missing))}")
        result["tables"][item.name] = columns
    for schema, name in [(settings.source_schema, "message_change_log"), (settings.app_schema, "MailboxAppChange")]:
        if not conn.execute("SELECT to_regclass(%s) AS relation", (f'{schema}."{name}"',)).fetchone()["relation"]:
            raise RuntimeError(f"required change log missing: {schema}.{name}")
    return result


def _key_value(table: SourceTable, value: str):
    return int(value) if table.domain == "mail" else value


def source_rows(conn: Connection, settings, table: SourceTable, *, keys: list[str] | None = None, hashes_only: bool = False) -> Iterator[dict]:
    schema = schema_of(settings, table)
    payload = sql.SQL("to_jsonb(t)")
    # Fetch timestamps are operational heartbeats, not substantive mail changes.
    hash_payload = sql.SQL("(to_jsonb(t) - 'last_fetched_at')") if table.name == "messages" else payload
    selection = sql.SQL("{key}::text AS record_key, md5({payload}::text) AS content_hash").format(key=sql.Identifier(table.key), payload=hash_payload)
    if not hashes_only:
        selection += sql.SQL(", to_jsonb(t)::text AS payload")
    base = sql.SQL("SELECT {} FROM {}.{} t").format(selection, sql.Identifier(schema), sql.Identifier(table.name))
    order = sql.SQL(" ORDER BY {}").format(sql.Identifier(table.key))
    # The production role cancels any statement still running at 30 seconds.
    # Keyset pages keep each statement inside that limit.
    page = 20 if table.name == "messages" else min(settings.batch_size, 200)
    if keys is not None:
        if not keys:
            return
        key_type = "bigint" if table.domain == "mail" else "text"
        query = base + sql.SQL(" WHERE {} = ANY(%s::{})").format(sql.Identifier(table.key), sql.SQL(key_type + "[]")) + order
        for offset in range(0, len(keys), page):
            chunk = keys[offset:offset + page]
            values = [_key_value(table, item) for item in chunk] if table.domain == "mail" else chunk
            yield from conn.execute(query, (values,)).fetchall()
        return
    last = None
    while True:
        if last is None:
            rows = conn.execute(base + order + sql.SQL(" LIMIT %s"), (page,)).fetchall()
        else:
            rows = conn.execute(base + sql.SQL(" WHERE {} > %s").format(sql.Identifier(table.key)) + order + sql.SQL(" LIMIT %s"), (_key_value(table, last), page)).fetchall()
        if not rows:
            return
        yield from rows
        if len(rows) < page:
            return
        last = rows[-1]["record_key"]


def log_events(conn: Connection, settings, *, kind: str, after: int, tail: int = 5000) -> list[dict]:
    if kind == "mail":
        query = sql.SQL("""SELECT id, message_pk::text AS record_key FROM {schema}.message_change_log
            WHERE id > %s ORDER BY id LIMIT %s""").format(schema=sql.Identifier(settings.source_schema))
    else:
        query = sql.SQL("""SELECT "id" AS id, "mailId" AS record_key, "sourceTable" AS source_table
            FROM {schema}."MailboxAppChange"
            WHERE "id" > %s ORDER BY "id" LIMIT %s""").format(schema=sql.Identifier(settings.app_schema))
    # Replay the committed tail AND every unread event. A global max-tail cutoff
    # silently loses a backlog larger than tail when the checkpoint advances.
    cursor = max(0, after - tail)
    page_size = max(1, min(settings.batch_size, 200))
    events = []
    while True:
        page = conn.execute(query, (cursor, page_size)).fetchall()
        events.extend(page)
        if len(page) < page_size:
            return events
        cursor = int(page[-1]['id'])


def schema_fingerprint(contract: dict) -> str:
    import hashlib
    return hashlib.sha256(json.dumps(contract["tables"], sort_keys=True).encode()).hexdigest()
