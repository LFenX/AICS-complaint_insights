from __future__ import annotations

from collections import defaultdict
import json

from psycopg import sql
from psycopg.types.json import Jsonb

from .catalog import add_dynamic
from .model import FACT_COLUMNS, ISSUE_COLUMNS, project_mail
from .source import BY_NAME
from .time_rules import detect_fallback_skew


def payloads(conn, source_id, name, *, strip: tuple[str,...] = ()):
    table = BY_NAME[name]
    expression = sql.SQL("payload")
    for field in strip:
        expression += sql.SQL(" - {} ").format(sql.Literal(field))
    query = sql.SQL("SELECT {} AS payload FROM {}.{} WHERE source_id=%s AND deleted_at IS NULL").format(expression,sql.Identifier(table.mirror_schema),sql.Identifier(name))
    return [row["payload"] for row in conn.execute(query,(source_id,))]


def publish_catalog(conn, source_id, static_entries, files):
    entries = add_dynamic(static_entries,payloads(conn,source_id,"TaxonomyCandidate"),payloads(conn,source_id,"IssueTypeRegistry"))
    conn.execute("DELETE FROM analysis.taxonomy WHERE source_id=%s",(source_id,))
    with conn.cursor().copy("COPY analysis.taxonomy(source_id,category_id,level,name,parent_id,level_one,level_two,status,origin,definition) FROM STDIN") as copy:
        for row in entries.values():
            copy.write_row((source_id,row["category_id"],row["level"],row["name"],row["parent_id"],row["level_one"],row["level_two"],row["status"],row["origin"],Jsonb(row["definition"])))
    conn.execute("DELETE FROM analysis.catalog_files WHERE source_id=%s",(source_id,))
    with conn.cursor().copy("COPY analysis.catalog_files(source_id,filename,sha256,content) FROM STDIN") as copy:
        for row in files:
            copy.write_row((source_id,row["filename"],row["sha256"],Jsonb(row["content"])))
    return entries


def rebuild_projection(conn, settings, catalog, *, pks: set[str] | None):
    sid = settings.source_id
    full = pks is None
    if not full and not pks:
        return {"projected":0,"skew_hours":None,"dates":[]}
    params = [sid]
    clause = ""
    if not full:
        clause = " AND record_key = ANY(%s::text[])"
        params.append(list(pks))
    old_dates = {row["business_date"] for row in conn.execute("SELECT DISTINCT business_date FROM analysis.mail_fact WHERE source_id=%s" + (" AND mail_pk = ANY(%s::bigint[])" if not full else ""),params)}
    conn.execute("DELETE FROM analysis.mail_fact WHERE source_id=%s" + (" AND mail_pk = ANY(%s::bigint[])" if not full else ""),params)
    # Narrow, target-side lookups keep body and raw-payload blobs out of projection memory.
    inbound_rows = payloads(conn,sid,"InboundMail")
    inbound = {str(row["sourcePk"]):row for row in inbound_rows}
    artifacts = payloads(conn,sid,"MailAiArtifact",strip=("bodyOriginal","bodyTranslated","materials","issues","fields","quoted","signature"))
    ai_by_inbound = {row["inboundMailId"]:row for row in artifacts}
    bindings = defaultdict(list)
    for row in payloads(conn,sid,"MailIssueBinding"):
        bindings[row["mailAiArtifactId"]].append(row)
    mailboxes = {str(row["id"]):row["email"] for row in payloads(conn,sid,"mailboxes")}
    samples = [row["payload"] for row in conn.execute("SELECT payload - 'raw_payload' - 'body_plain_text' - 'body_html' - 'body_preview' AS payload FROM source_mail.messages WHERE source_id=%s AND deleted_at IS NULL ORDER BY (record_key::bigint) DESC LIMIT 300",(sid,))]
    skew = detect_fallback_skew(samples)
    conn.execute("CREATE TEMP TABLE projected_fact (LIKE analysis.mail_fact INCLUDING DEFAULTS) ON COMMIT DROP")
    conn.execute("CREATE TEMP TABLE projected_issue (LIKE analysis.mail_issue INCLUDING DEFAULTS) ON COMMIT DROP")
    count = 0
    issue_rows = []
    new_dates = set()
    query = "SELECT payload - 'raw_payload' - 'body_plain_text' - 'body_html' - 'body_preview' AS payload FROM source_mail.messages WHERE source_id=%s AND deleted_at IS NULL"+clause+" ORDER BY record_key::bigint"
    # Stream narrow raw rows before writing COPY: psycopg cannot execute a second
    # command on a connection while a COPY operation is active.
    with conn.cursor(name="projection_input") as cursor:
        cursor.itersize = settings.batch_size
        cursor.execute(query,params)
        batch = cursor.fetchmany(settings.batch_size)
        while batch:
            facts = []
            for item in batch:
                raw = item["payload"]
                anchor = inbound.get(str(raw["id"]))
                ai = ai_by_inbound.get(anchor["id"]) if anchor else None
                fact,issues = project_mail(sid,raw,anchor,ai,bindings.get((ai or {}).get("id"),[]),mailboxes,catalog,skew)
                facts.append(tuple(fact[col] for col in FACT_COLUMNS))
                issue_rows.extend(issues)
                new_dates.add(fact["business_date"])
            with conn.cursor().copy(sql.SQL("COPY projected_fact({}) FROM STDIN").format(sql.SQL(",").join(map(sql.Identifier,FACT_COLUMNS)))) as copy:
                for fact in facts:
                    copy.write_row(fact)
            count += len(facts)
            batch = cursor.fetchmany(settings.batch_size)
    with conn.cursor().copy(sql.SQL("COPY projected_issue({}) FROM STDIN").format(sql.SQL(",").join(map(sql.Identifier,ISSUE_COLUMNS)))) as copy:
        for row in issue_rows:
            copy.write_row(tuple(Jsonb(row[col]) if col == "definition" else row[col] for col in ISSUE_COLUMNS))
    conn.execute("INSERT INTO analysis.mail_fact SELECT * FROM projected_fact")
    conn.execute("INSERT INTO analysis.mail_issue SELECT * FROM projected_issue")
    dates = list((old_dates | new_dates) - {None})
    rebuild_daily(conn,sid,dates=dates,full=full)
    return {"projected":count,"skew_hours":skew,"dates":[str(day) for day in sorted(dates)]}


def rebuild_daily(conn, source_id, *, dates, full):
    args = [source_id]
    date_filter = ""
    if not full:
        if not dates:
            return
        args.append(dates)
        date_filter = " AND business_date = ANY(%s::date[])"
    conn.execute("DELETE FROM analysis.daily_category WHERE source_id=%s"+date_filter,args)
    for depth in (1,2,3):
        level_two = "level_two" if depth >= 2 else "''::text"
        issue_id = "issue_type_id" if depth == 3 else "''::text"
        conn.execute(f"""INSERT INTO analysis.daily_category
        SELECT source_id,'primary',{depth},business_date,direction,mailbox,level_one,{level_two},{issue_id},
               count(*),count(*) FILTER (WHERE analysis_state='DONE' AND issue_type_id<>''),
               count(*) FILTER (WHERE analysis_state<>'DONE')
        FROM analysis.mail_fact WHERE source_id=%s AND business_date IS NOT NULL"""+date_filter+" GROUP BY 1,4,5,6,7,8,9",args)
        issue_date_filter = date_filter.replace("business_date", "f.business_date")
        second = "CASE WHEN f.analysis_state='DONE' THEN i.level_two ELSE '' END" if depth >= 2 else "''::text"
        third = "CASE WHEN f.analysis_state='DONE' THEN i.issue_type_id ELSE '' END" if depth == 3 else "''::text"
        conn.execute(f"""INSERT INTO analysis.daily_category
        SELECT f.source_id,'all_issues',{depth},f.business_date,f.direction,f.mailbox,
               CASE WHEN f.analysis_state='DONE' THEN i.level_one ELSE 'PEND' END,
               {second},{third},
               count(DISTINCT f.mail_pk),count(*) FILTER (WHERE i.source_binding_id IS NOT NULL OR (f.analysis_state='DONE' AND i.issue_type_id<>'')),
               count(DISTINCT f.mail_pk) FILTER (WHERE f.analysis_state<>'DONE')
        FROM analysis.mail_fact f JOIN analysis.mail_issue i USING(source_id,mail_pk)
        WHERE f.source_id=%s AND f.business_date IS NOT NULL"""+issue_date_filter+" GROUP BY 1,4,5,6,7,8,9",args)


def verify_projection(conn, source_id):
    row = conn.execute("""SELECT
        (SELECT count(*) FROM source_mail.messages WHERE source_id=%s AND deleted_at IS NULL) AS source_count,
        (SELECT count(*) FROM analysis.mail_fact WHERE source_id=%s) AS fact_count,
        (SELECT count(*) FROM analysis.mail_issue WHERE source_id=%s AND is_primary) AS primary_count,
        (SELECT count(*) FROM analysis.mail_fact WHERE source_id=%s AND business_date IS NOT NULL) AS dated_count,
        (SELECT coalesce(sum(mail_count),0) FROM analysis.daily_category WHERE source_id=%s AND scope='primary' AND category_depth=3) AS bucket_count""",[source_id]*5).fetchone()
    if row["source_count"] != row["fact_count"] or row["fact_count"] != row["primary_count"] or row["dated_count"] != row["bucket_count"]:
        raise RuntimeError("target projection parity failed")
    return {key:int(value) for key,value in row.items()}
