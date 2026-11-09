CREATE SCHEMA IF NOT EXISTS sync;
CREATE SCHEMA IF NOT EXISTS source_mail;
CREATE SCHEMA IF NOT EXISTS source_app;
CREATE SCHEMA IF NOT EXISTS analysis;

CREATE TABLE IF NOT EXISTS sync.schema_migrations (
    name text PRIMARY KEY, sha256 text NOT NULL, applied_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS sync.sources (
    source_id text PRIMARY KEY,
    identity_hash text NOT NULL,
    connection_identity jsonb NOT NULL,
    data_version bigint NOT NULL DEFAULT 0,
    source_event_id bigint NOT NULL DEFAULT 0,
    app_event_id bigint NOT NULL DEFAULT 0,
    source_snapshot_at timestamptz,
    last_sync_at timestamptz,
    last_aux_at timestamptz,
    last_reconcile_at timestamptz,
    status text NOT NULL DEFAULT 'EMPTY',
    last_error_code text,
    fallback_skew_hours integer NOT NULL DEFAULT 0,
    schema_hash text,
    source_contract jsonb NOT NULL DEFAULT '{}',
    catalog_hash text
);
CREATE TABLE IF NOT EXISTS sync.runs (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_id text NOT NULL,
    started_at timestamptz NOT NULL DEFAULT now(),
    finished_at timestamptz,
    status text NOT NULL,
    mode text NOT NULL,
    changed_rows integer NOT NULL DEFAULT 0,
    metrics jsonb NOT NULL DEFAULT '{}',
    error_code text
);
CREATE INDEX IF NOT EXISTS runs_source_time ON sync.runs(source_id, id DESC);
CREATE TABLE IF NOT EXISTS sync.seen_events (
    source_id text NOT NULL, kind text NOT NULL, event_id bigint NOT NULL,
    PRIMARY KEY(source_id, kind, event_id)
);

CREATE TABLE IF NOT EXISTS analysis.taxonomy (
    source_id text NOT NULL,
    category_id text NOT NULL,
    level integer NOT NULL,
    name text NOT NULL,
    parent_id text,
    level_one text NOT NULL DEFAULT '',
    level_two text NOT NULL DEFAULT '',
    status text NOT NULL,
    origin text NOT NULL,
    definition jsonb NOT NULL,
    PRIMARY KEY(source_id, category_id)
);
CREATE INDEX IF NOT EXISTS taxonomy_parent ON analysis.taxonomy(source_id, parent_id, status);
CREATE TABLE IF NOT EXISTS analysis.catalog_files (
    source_id text NOT NULL, filename text NOT NULL, sha256 text NOT NULL,
    content jsonb NOT NULL,
    PRIMARY KEY(source_id, filename)
);
CREATE TABLE IF NOT EXISTS analysis.mail_fact (
    source_id text NOT NULL,
    mail_pk bigint NOT NULL,
    inbound_mail_id text,
    ai_artifact_id text,
    mailbox text NOT NULL,
    folder_id text NOT NULL,
    folder_track text NOT NULL,
    direction text NOT NULL,
    received_at timestamptz,
    business_date date,
    time_shift_hours integer NOT NULL,
    subject text NOT NULL,
    from_address text NOT NULL,
    language text NOT NULL,
    region text,
    intent text,
    category_ai text,
    category_normalized text,
    level_one text NOT NULL,
    level_two text NOT NULL,
    issue_type_id text NOT NULL,
    priority_ai text,
    analysis_state text NOT NULL,
    analysis_version text,
    summary_zh text NOT NULL,
    raw_message_id text,
    smtp_message_id text,
    thread_id text,
    has_attachment boolean NOT NULL,
    PRIMARY KEY(source_id, mail_pk)
);
CREATE INDEX IF NOT EXISTS mail_fact_day ON analysis.mail_fact(source_id, business_date, mail_pk);
CREATE INDEX IF NOT EXISTS mail_fact_classification ON analysis.mail_fact(source_id, level_one, level_two, issue_type_id, business_date, mail_pk);
CREATE INDEX IF NOT EXISTS mail_fact_mailbox ON analysis.mail_fact(source_id, mailbox, direction, business_date, mail_pk);
CREATE TABLE IF NOT EXISTS analysis.mail_issue (
    source_id text NOT NULL,
    mail_pk bigint NOT NULL,
    issue_point_key text NOT NULL,
    source_binding_id text,
    is_primary boolean NOT NULL,
    level_one text NOT NULL,
    level_two text NOT NULL,
    issue_type_id text NOT NULL,
    binding_status text NOT NULL,
    severity text,
    definition jsonb NOT NULL,
    PRIMARY KEY(source_id, mail_pk, issue_point_key),
    FOREIGN KEY(source_id, mail_pk) REFERENCES analysis.mail_fact(source_id, mail_pk) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS mail_issue_category ON analysis.mail_issue(source_id, issue_type_id, mail_pk);
CREATE UNIQUE INDEX IF NOT EXISTS mail_issue_one_primary ON analysis.mail_issue(source_id, mail_pk) WHERE is_primary;
CREATE TABLE IF NOT EXISTS analysis.daily_category (
    source_id text NOT NULL,
    scope text NOT NULL,
    category_depth integer NOT NULL,
    business_date date NOT NULL,
    direction text NOT NULL,
    mailbox text NOT NULL,
    level_one text NOT NULL,
    level_two text NOT NULL,
    issue_type_id text NOT NULL,
    mail_count bigint NOT NULL,
    issue_count bigint NOT NULL,
    pending_mail_count bigint NOT NULL,
    PRIMARY KEY(source_id,scope,category_depth,business_date,direction,mailbox,level_one,level_two,issue_type_id)
);

CREATE OR REPLACE VIEW analysis.v_sync_status AS
SELECT source_id, connection_identity, data_version, source_event_id, app_event_id,
       source_snapshot_at,last_sync_at,last_aux_at,last_reconcile_at,status,last_error_code,
       fallback_skew_hours,schema_hash,catalog_hash
FROM sync.sources;
CREATE OR REPLACE VIEW analysis.v_sync_runs AS
SELECT id,source_id,started_at,finished_at,status,mode,changed_rows,metrics,error_code FROM sync.runs;
