from __future__ import annotations

from datetime import datetime, timezone
import json
import time

from psycopg import sql
from psycopg.types.json import Jsonb

from .catalog import load_static
from .config import Settings, connection_identity
from .db import source_connection, target_connection
from .projection import payloads, publish_catalog, rebuild_projection, verify_projection
from .source import TABLES, BY_NAME, check_contract, log_events, schema_fingerprint, schema_of, source_rows


def mirror_relation(table):
    return sql.SQL("{}.{}").format(sql.Identifier(table.mirror_schema), sql.Identifier(table.name))


def mirror_index(conn, sid, table):
    return {row["record_key"]:row for row in conn.execute(sql.SQL("SELECT record_key,content_hash,deleted_at FROM {} WHERE source_id=%s").format(mirror_relation(table)),(sid,))}


def related_keys(conn, settings, table, field, values):
    if not values:
        return set()
    value_type = "bigint[]" if field in {"sourcePk", "message_pk"} else "text[]"
    query = sql.SQL("SELECT {}::text AS record_key FROM {}.{} WHERE {}=ANY(%s::{})").format(sql.Identifier(table.key),sql.Identifier(schema_of(settings,table)),sql.Identifier(table.name),sql.Identifier(field),sql.SQL(value_type))
    return {row["record_key"] for row in conn.execute(query,(list(values),))}


def local_related_keys(conn, sid, table, field, values):
    if not values:
        return set()
    query = sql.SQL("SELECT record_key FROM {} WHERE source_id=%s AND deleted_at IS NULL AND payload->>{}=ANY(%s::text[])").format(mirror_relation(table),sql.Literal(field))
    return {row["record_key"] for row in conn.execute(query,(sid,list(values)))}


def affected_pks(conn, sid, table, keys):
    if not keys:
        return set()
    if table.name == "messages":
        return set(keys)
    if table.name not in {"InboundMail","MailAiArtifact","MailIssueBinding"}:
        return set()
    records = conn.execute(sql.SQL("SELECT payload FROM {} WHERE source_id=%s AND record_key=ANY(%s::text[])").format(mirror_relation(table)),(sid,list(keys))).fetchall()
    if table.name == "InboundMail":
        return {str(row["payload"]["sourcePk"]) for row in records}
    if table.name == "MailIssueBinding":
        artifact_ids = {row["payload"]["mailAiArtifactId"] for row in records}
        records = conn.execute('SELECT payload FROM source_app."MailAiArtifact" WHERE source_id=%s AND record_key=ANY(%s::text[])',(sid,list(artifact_ids))).fetchall() if artifact_ids else []
    inbound_ids = {row["payload"]["inboundMailId"] for row in records}
    return {str(row["payload"]["sourcePk"]) for row in conn.execute('SELECT payload FROM source_app."InboundMail" WHERE source_id=%s AND record_key=ANY(%s::text[])',(sid,list(inbound_ids)))} if inbound_ids else set()


def sync_table(src, dst, settings, table, *, keys=None):
    sid = settings.source_id
    old = mirror_index(dst,sid,table)
    wanted = set(keys) if keys is not None else None
    current = set()
    changed = []
    for row in source_rows(src,settings,table,keys=list(wanted) if wanted is not None else None,hashes_only=True):
        key = row["record_key"]
        current.add(key)
        previous = old.get(key)
        if not previous or previous["deleted_at"] is not None or previous["content_hash"] != row["content_hash"]:
            changed.append(key)
    removed = {key for key,row in old.items() if row["deleted_at"] is None and key not in current and (wanted is None or key in wanted)}
    touched = set(changed) | removed
    affected = affected_pks(dst,sid,table,touched)
    if changed:
        dst.execute("CREATE TEMP TABLE IF NOT EXISTS mirror_stage(source_id text,record_key text,payload jsonb,content_hash text) ON COMMIT DROP")
        for offset in range(0,len(changed),settings.batch_size):
            batch = changed[offset:offset+settings.batch_size]
            # Buffer one bounded source batch while COPY owns the target connection.
            rows = list(source_rows(src,settings,table,keys=batch))
            dst.execute("TRUNCATE mirror_stage")
            with dst.cursor().copy("COPY mirror_stage(source_id,record_key,payload,content_hash) FROM STDIN") as copy:
                for row in rows:
                    copy.write_row((sid,row["record_key"],row["payload"],row["content_hash"]))
            dst.execute(sql.SQL("""INSERT INTO {}(source_id,record_key,payload,content_hash)
                SELECT source_id,record_key,payload,content_hash FROM mirror_stage
                ON CONFLICT(source_id,record_key) DO UPDATE SET payload=excluded.payload,content_hash=excluded.content_hash,synced_at=now(),deleted_at=NULL""").format(mirror_relation(table)))
    if removed:
        dst.execute(sql.SQL("UPDATE {} SET deleted_at=now(),synced_at=now() WHERE source_id=%s AND record_key=ANY(%s::text[]) AND deleted_at IS NULL").format(mirror_relation(table)),(sid,list(removed)))
    affected |= affected_pks(dst,sid,table,touched)
    return {"changed":len(changed),"deleted":len(removed),"scanned":len(current),"affected":affected,"touched":bool(touched)}


def event_bounds(conn, settings, kind):
    relation = sql.SQL("{}.{}").format(sql.Identifier(settings.source_schema if kind=="mail" else settings.app_schema),sql.Identifier("message_change_log" if kind=="mail" else "MailboxAppChange"))
    row = conn.execute(sql.SQL("SELECT coalesce(min(id),0) AS lo,coalesce(max(id),0) AS hi FROM {}").format(relation)).fetchone()
    return int(row["lo"]),int(row["hi"])


def unseen_events(dst, sid, kind, rows):
    seen = {int(row["event_id"]) for row in dst.execute("SELECT event_id FROM sync.seen_events WHERE source_id=%s AND kind=%s",(sid,kind))}
    return [row for row in rows if int(row["id"]) not in seen]


def remember_events(dst, sid, kind, events, high):
    if events:
        with dst.cursor() as cursor:
            cursor.executemany("INSERT INTO sync.seen_events(source_id,kind,event_id) VALUES(%s,%s,%s) ON CONFLICT DO NOTHING",[(sid,kind,int(row["id"])) for row in events])
    dst.execute("DELETE FROM sync.seen_events WHERE source_id=%s AND kind=%s AND event_id<%s",(sid,kind,max(0,high-10000)))


def code_of(error):
    # PostgreSQL errors can embed customer values and SQL; persist only their class/code.
    return getattr(error,"sqlstate",None) or type(error).__name__


def sync_once(settings: Settings, *, force_reconcile=False, fail_before_publish=False):
    settings.validate(source=True)
    started = time.monotonic()
    sid = settings.source_id
    try:
        static,files,catalog_hash = load_static(settings.catalog_path)
        with target_connection(settings) as dst:
            if not dst.execute("SELECT pg_try_advisory_xact_lock(hashtext('complaint-insights:'||%s)) AS acquired",(sid,)).fetchone()["acquired"]:
                return {"status":"BUSY","source_id":sid}
            state = dst.execute("SELECT * FROM sync.sources WHERE source_id=%s FOR UPDATE",(sid,)).fetchone()
            if state and state["identity_hash"] != settings.identity_hash:
                raise ValueError("source_id is already bound to a different connection; choose a new source_id")
            if not state:
                dst.execute("INSERT INTO sync.sources(source_id,identity_hash,connection_identity) VALUES(%s,%s,%s)",(sid,settings.identity_hash,Jsonb(connection_identity(settings.source_url))))
                state = dst.execute("SELECT * FROM sync.sources WHERE source_id=%s",(sid,)).fetchone()
            with source_connection(settings) as src:
                contract = check_contract(src,settings)
                schema_hash = schema_fingerprint(contract)
                snapshot_at = src.execute("SELECT transaction_timestamp() AS time").fetchone()["time"]
                now = datetime.now(timezone.utc)
                def overdue(value,seconds):
                    return value is None or (now-value).total_seconds() >= seconds
                bounds = {kind:event_bounds(src,settings,kind) for kind in ["mail","app"]}
                reset = any(bounds[kind][1] < state[field] or (bounds[kind][0] > state[field]+1 and state[field]>0) for kind,field in [("mail","source_event_id"),("app","app_event_id")])
                full = force_reconcile or state["data_version"]==0 or state["schema_hash"] != schema_hash or reset or overdue(state["last_reconcile_at"],settings.reconcile_seconds)
                auxiliary = full or overdue(state["last_aux_at"],settings.auxiliary_seconds)
                # A full scan covers the snapshot, so only seed its open tail.
                # An incremental scan must consume the ENTIRE unread range.
                events = {kind:log_events(src,settings,kind=kind,after=bounds[kind][1] if full else int(state[field])) for kind,field in [("mail","source_event_id"),("app","app_event_id")]}
                if reset:
                    dst.execute("DELETE FROM sync.seen_events WHERE source_id=%s",(sid,))
                fresh = {kind:unseen_events(dst,sid,kind,rows) for kind,rows in events.items()}
                metrics = {}
                affected = set()
                full_projection = full or state["catalog_hash"] != catalog_hash
                def apply(table,keys=None):
                    nonlocal full_projection
                    result = sync_table(src,dst,settings,table,keys=keys)
                    affected.update(result.pop("affected"))
                    touched = result.pop("touched")
                    metrics[table.name] = result
                    if touched and table.name in {"TaxonomyCandidate","IssueTypeRegistry","IssueGroupLifecycle","mailboxes"}:
                        full_projection = True
                    return touched
                if full:
                    for table in TABLES:
                        apply(table)
                else:
                    pks = {row["record_key"] for row in fresh["mail"]}
                    if pks:
                        apply(BY_NAME["messages"],pks)
                        attachment_ids = related_keys(src,settings,BY_NAME["attachments"],"message_pk",pks)
                        attachment_ids |= local_related_keys(dst,sid,BY_NAME["attachments"],"message_pk",pks)
                        if attachment_ids:
                            apply(BY_NAME["attachments"],attachment_ids)
                    mail_ids = {row["record_key"] for row in fresh["app"] if row.get("source_table") in {"InboundMail","MailAiArtifact"} and row["record_key"]}
                    mail_ids |= related_keys(src,settings,BY_NAME["InboundMail"],"sourcePk",pks)
                    mail_ids |= local_related_keys(dst,sid,BY_NAME["InboundMail"],"sourcePk",pks)
                    if mail_ids:
                        apply(BY_NAME["InboundMail"],mail_ids)
                        artifact_ids = related_keys(src,settings,BY_NAME["MailAiArtifact"],"inboundMailId",mail_ids)
                        artifact_ids |= local_related_keys(dst,sid,BY_NAME["MailAiArtifact"],"inboundMailId",mail_ids)
                        apply(BY_NAME["MailAiArtifact"],artifact_ids)
                        if not auxiliary:
                            binding_ids = related_keys(src,settings,BY_NAME["MailIssueBinding"],"mailAiArtifactId",artifact_ids)
                            binding_ids |= local_related_keys(dst,sid,BY_NAME["MailIssueBinding"],"mailAiArtifactId",artifact_ids)
                            apply(BY_NAME["MailIssueBinding"],binding_ids)
                    if auxiliary:
                        for table in TABLES:
                            if table.auxiliary:
                                apply(table)
                changed_rows = sum(item["changed"]+item["deleted"] for item in metrics.values())
            # Production reads stop here. Classification totals are computed on the local copy.
            if full_projection:
                catalog = publish_catalog(dst,sid,static,files)
            else:
                catalog = {row["category_id"]:row for row in dst.execute("SELECT * FROM analysis.taxonomy WHERE source_id=%s",(sid,))}
            projection = rebuild_projection(dst,settings,catalog,pks=None if full_projection else affected)
            parity = verify_projection(dst,sid)
            if fail_before_publish:
                raise RuntimeError("injected pre-publication failure")
            changed = bool(changed_rows or full_projection)
            version = int(state["data_version"])+(1 if changed else 0)
            for kind in ["mail","app"]:
                remember_events(dst,sid,kind,events[kind],bounds[kind][1])
            dst.execute("""UPDATE sync.sources SET data_version=%s,source_event_id=%s,app_event_id=%s,
                source_snapshot_at=%s,last_sync_at=clock_timestamp(),
                last_aux_at=CASE WHEN %s THEN clock_timestamp() ELSE last_aux_at END,
                last_reconcile_at=CASE WHEN %s THEN clock_timestamp() ELSE last_reconcile_at END,
                fallback_skew_hours=coalesce(%s,fallback_skew_hours),schema_hash=%s,source_contract=%s,
                catalog_hash=%s,status='READY',last_error_code=NULL WHERE source_id=%s""",
                (version,bounds["mail"][1],bounds["app"][1],snapshot_at,auxiliary,full,projection["skew_hours"],schema_hash,Jsonb(contract),catalog_hash,sid))
            result = {"source_id":sid,"status":"READY","data_version":version,"mode":"RECONCILE" if full else "INCREMENTAL",
                      "changed_rows":changed_rows,"tables":metrics,"projection":projection,"parity":parity,
                      "duration_ms":round((time.monotonic()-started)*1000)}
            dst.execute("INSERT INTO sync.runs(source_id,finished_at,status,mode,changed_rows,metrics) VALUES(%s,clock_timestamp(),'SUCCEEDED',%s,%s,%s)",(sid,result["mode"],changed_rows,Jsonb(result)))
            return result
    except Exception as error:
        with target_connection(settings) as conn:
            conn.execute("UPDATE sync.sources SET status='DEGRADED',last_error_code=%s WHERE source_id=%s AND identity_hash=%s",(code_of(error),sid,settings.identity_hash))
            conn.execute("INSERT INTO sync.runs(source_id,finished_at,status,mode,error_code) VALUES(%s,clock_timestamp(),'FAILED','RECONCILE'::text,%s)",(sid,code_of(error)))
        raise


def watch(settings: Settings):
    settings.validate(source=True)
    while True:
        started = time.monotonic()
        try:
            result = sync_once(settings)
            print(json.dumps({key:result.get(key) for key in ["source_id","status","mode","data_version","changed_rows","duration_ms"]}),flush=True)
        except Exception as error:
            print(json.dumps({"source_id":settings.source_id,"status":"FAILED","error_code":code_of(error)}),flush=True)
        time.sleep(max(1,settings.poll_seconds-(time.monotonic()-started)))
