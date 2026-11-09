from __future__ import annotations

from contextlib import contextmanager
import psycopg
from psycopg.rows import dict_row

from .config import Settings, clean_source_url


@contextmanager
def source_connection(settings: Settings):
    settings.validate(source=True)
    with psycopg.connect(clean_source_url(settings.source_url), connect_timeout=8,
                         application_name="complaint-insights-source-readonly",
                         options="-c default_transaction_read_only=on -c statement_timeout=30000 -c lock_timeout=2000 -c timezone=UTC",
                         row_factory=dict_row) as conn:
        conn.read_only = True
        conn.isolation_level = psycopg.IsolationLevel.REPEATABLE_READ
        yield conn


@contextmanager
def target_connection(settings: Settings, *, reader: bool = False, owner: bool = False):
    settings.validate()
    url = settings.target_owner_url if owner else settings.target_reader_url if reader else settings.target_writer_url
    # Production-sized daily aggregation exceeds the previous 120s local limit.
    options = "-c timezone=UTC -c lock_timeout=5000 -c statement_timeout=600000"
    if reader:
        options += " -c default_transaction_read_only=on -c statement_timeout=15000"
    with psycopg.connect(url, connect_timeout=8, application_name="complaint-insights-reader" if reader else "complaint-insights-sync",
                         options=options, row_factory=dict_row) as conn:
        if reader:
            conn.read_only = True
            conn.isolation_level = psycopg.IsolationLevel.REPEATABLE_READ
        yield conn
