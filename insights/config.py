from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import hashlib
import ipaddress
import json
import os
import re
import ssl
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from psycopg.conninfo import conninfo_to_dict

ROOT = Path(__file__).resolve().parents[1]


def clean_source_url(value: str) -> str:
    parts = urlsplit(value)
    options = [(k, v) for k, v in parse_qsl(parts.query) if k not in {"schema", "connection_limit", "pool_timeout"}]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(options), parts.fragment))


def loopback(host: str) -> bool:
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def connection_identity(url: str) -> dict[str, str]:
    parts = conninfo_to_dict(clean_source_url(url))
    # libpq can route to hostaddr while retaining host for authentication/TLS.
    # Service files and PGHOSTADDR/PGSERVICE can replace that destination.
    # An omitted host, port, or database name falls through to PGHOST/PGPORT/PGDATABASE.
    # The identity used for authorization must be the values written in the URL.
    if any(parts.get(key) for key in ("hostaddr", "service")) or any(
            os.environ.get(key) for key in ("PGHOSTADDR", "PGSERVICE")):
        raise ValueError("hostaddr/service overrides are not allowed; use an explicit database host")
    missing = [key for key in ("host", "port", "dbname") if not parts.get(key)]
    if missing:
        raise ValueError("host, port, and database name must be explicit in the connection URL")
    return {"host": parts["host"], "port": str(parts["port"]), "dbname": parts["dbname"]} 


@dataclass(frozen=True)
class Settings:
    source_id: str
    source_url: str = field(repr=False)
    target_owner_url: str = field(repr=False)
    target_writer_url: str = field(repr=False)
    target_reader_url: str = field(repr=False)
    api_token: str = field(repr=False)
    environment: str = "development"
    allow_production_read: bool = False
    source_schema: str = "public"
    app_schema: str = "complaint_app"
    api_host: str = "127.0.0.1"
    api_port: int = 3036
    poll_seconds: int = 30
    auxiliary_seconds: int = 60
    reconcile_seconds: int = 3600
    batch_size: int = 500
    catalog_dir: str = "assets/taxonomy"
    source_certificate_sha256: str = ""

    @classmethod
    def load(cls, path: str | Path | None = None) -> "Settings":
        filename = Path(path or os.environ.get("INSIGHTS_CONFIG", ROOT / ".secrets/local.json"))
        return cls(**json.loads(filename.read_text(encoding="utf-8")))

    def validate(self, *, source: bool = False) -> None:
        if not re.fullmatch(r"[a-z][a-z0-9_-]{1,63}", self.source_id):
            raise ValueError("source_id must be an explicit stable source namespace")
        for name in [self.source_schema, self.app_schema]:
            if not re.fullmatch(r"[a-z_][a-z0-9_]*", name):
                raise ValueError("invalid source schema")
        if not loopback(self.api_host) or len(self.api_token) < 32:
            raise ValueError("API requires loopback binding and a token of at least 32 characters")
        if min(self.poll_seconds, self.auxiliary_seconds, self.reconcile_seconds) < 1 or not 1 <= self.batch_size <= 5000:
            raise ValueError("invalid sync interval or batch size")
        target_ids = [connection_identity(value) for value in [self.target_owner_url, self.target_writer_url, self.target_reader_url]]
        if any(not loopback(value["host"]) or value["port"] != "15433" or not value["dbname"].startswith("complaint_insights") for value in target_ids):
            raise ValueError("target must be the isolated loopback analytics database on port 15433")
        if any(value != target_ids[0] for value in target_ids[1:]):
            raise ValueError("owner, sync and reader URLs must refer to the same analytics database")
        if source:
            identity = connection_identity(self.source_url)
            if identity == target_ids[0]:
                raise ValueError("source and target databases must differ")
            if self.environment == "production" or not loopback(identity["host"]):
                if not self.allow_production_read:
                    raise ValueError("production source is disabled in this profile")
                params = conninfo_to_dict(clean_source_url(self.source_url))
                if params.get("sslmode") != "verify-full" or not params.get("sslrootcert"):
                    raise ValueError("production requires verify-full and an explicit trust certificate")
                certificate = Path(params["sslrootcert"]).read_text(encoding="ascii")
                digest = hashlib.sha256(ssl.PEM_cert_to_DER_cert(certificate)).hexdigest()
                expected = self.source_certificate_sha256.replace(":", "").lower()
                if not expected or digest != expected:
                    raise ValueError("production trust certificate fingerprint does not match")

    @property
    def identity_hash(self) -> str:
        body = {**connection_identity(self.source_url), "source_schema": self.source_schema, "app_schema": self.app_schema}
        return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()

    @property
    def catalog_path(self) -> Path:
        path = Path(self.catalog_dir)
        return path if path.is_absolute() else ROOT / path
