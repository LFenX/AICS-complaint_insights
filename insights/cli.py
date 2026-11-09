from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import time
from urllib.parse import quote

from .config import ROOT, Settings, connection_identity
from .db import source_connection, target_connection
from .initialize import initialize_database
from .source import check_contract
from .syncer import code_of, sync_once, watch


def load_env(path: Path):
    values = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key,value = line.split("=",1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def protect_directory(path: Path):
    path.mkdir(parents=True,exist_ok=True)
    if sys.platform == "win32":
        import csv
        identity = subprocess.check_output(["whoami","/user","/fo","csv","/nh"],text=True).strip()
        sid = next(csv.reader([identity]))[-1]
        subprocess.run(["icacls",str(path),"/inheritance:r","/grant:r",f"*{sid}:(OI)(CI)F","*S-1-5-18:(OI)(CI)F"],check=True,stdout=subprocess.DEVNULL)
    else:
        path.chmod(0o700)


def create_local_profile(original_project: Path):
    private = ROOT / ".secrets"
    protect_directory(private)
    protect_directory(ROOT / ".runtime")
    filename = private / "local.json"
    if filename.exists():
        return Settings.load(filename)
    original = load_env(original_project / ".env")
    source_url = original.get("MAIL_DATABASE_URL")
    if not source_url or connection_identity(source_url)["host"] not in {"127.0.0.1","localhost","::1"}:
        raise ValueError("bootstrap accepts only an existing loopback development mail database")
    passwords = {name:secrets.token_urlsafe(32) for name in ["insights_owner","insights_sync","insights_reader"]}
    def url(role):
        return f"postgresql://{role}:{quote(passwords[role],safe='')}@127.0.0.1:15433/complaint_insights"
    settings = Settings(source_id="development-local",source_url=source_url,target_owner_url=url("insights_owner"),target_writer_url=url("insights_sync"),target_reader_url=url("insights_reader"),api_token=secrets.token_urlsafe(48))
    filename.write_text(json.dumps(asdict(settings),ensure_ascii=False,indent=2),encoding="utf-8")
    (private/"postgres.env").write_text("POSTGRES_USER=insights_owner\nPOSTGRES_DB=complaint_insights\nPOSTGRES_PASSWORD="+passwords["insights_owner"]+"\n",encoding="utf-8")
    (private/"role-passwords.json").write_text(json.dumps(passwords),encoding="utf-8")
    # Public, versioned taxonomy assets; copy without altering their bytes.
    taxonomy = original_project / "LG_project_docs/requirements/T-WEB-TAXONOMY-REDESIGN-20260922-01"
    target = ROOT / "assets/taxonomy"
    target.mkdir(parents=True,exist_ok=True)
    for relative in ["design/taxonomy-v2.json","design/severity-baseline.json","discovery/embedding-adjudication-decisions.json"]:
        shutil.copyfile(taxonomy/relative,target/Path(relative).name)
    return settings


def bootstrap(original_project: Path):
    settings = create_local_profile(original_project)
    existing = subprocess.run(["docker","inspect","complaint-insights-postgres","--format",'{{index .Config.Labels "com.lfen.project"}}'],capture_output=True,text=True)
    if existing.returncode==0 and existing.stdout.strip() != "complaint-insights":
        raise RuntimeError("container name is already owned by another project")
    subprocess.run(["docker","compose","-f",str(ROOT/"deploy/compose.yml"),"up","-d","--pull","never"],check=True)
    for _ in range(40):
        try:
            with target_connection(settings,owner=True) as conn:
                conn.execute("SELECT 1")
            break
        except Exception:
            time.sleep(1)
    else:
        raise RuntimeError("isolated PostgreSQL did not become ready")
    passwords = json.loads((ROOT/".secrets/role-passwords.json").read_text(encoding="utf-8"))
    initialize_database(settings,passwords)
    # Safe handoff for analysis agents: no source, owner or writer credentials.
    (ROOT/".secrets/agent.json").write_text(json.dumps({"base_url":f"http://{settings.api_host}:{settings.api_port}","source_id":settings.source_id,
        "api_token":settings.api_token,"readonly_database_url":settings.target_reader_url},indent=2),encoding="utf-8")
    print(json.dumps({"status":"INITIALIZED","database":"complaint_insights","endpoint":"127.0.0.1:15433","source_id":settings.source_id,"credentials_file":str(ROOT/".secrets/local.json")},ensure_ascii=False))


def main():
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,"reconfigure"): stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="独立客诉分析数据底座")
    parser.add_argument("command",choices=["bootstrap","preflight","sync","reconcile","watch","serve","status","mcp","desk","board"])
    parser.add_argument("--config",type=Path)
    parser.add_argument("--original-project",type=Path)
    args = parser.parse_args()
    try:
        if args.command == "bootstrap":
            if not args.original_project:
                parser.error("bootstrap requires --original-project")
            bootstrap(args.original_project)
            return 0
        if args.command == "mcp":
            from .mcp_http import serve_remote
            serve_remote()
            return 0
        if args.command == "desk":
            from .token_desk import serve_desk
            serve_desk()
            return 0
        if args.command == "board":
            from .daily_board import serve_board
            serve_board()
            return 0
        settings = Settings.load(args.config)
        if args.command == "preflight":
            with source_connection(settings) as conn:
                contract = check_contract(conn,settings)
                print(json.dumps({"source_id":settings.source_id,"read_only":contract["read_only"],"tables":{key:len(value) for key,value in contract["tables"].items()}},ensure_ascii=False))
        elif args.command in {"sync","reconcile"}:
            print(json.dumps(sync_once(settings,force_reconcile=args.command=="reconcile"),ensure_ascii=False))
        elif args.command == "watch":
            watch(settings)
        elif args.command == "status":
            with target_connection(settings,reader=True) as conn:
                row = conn.execute("SELECT * FROM analysis.v_sync_status WHERE source_id=%s",(settings.source_id,)).fetchone()
                print(json.dumps(row,default=str,ensure_ascii=False))
        else:
            import logging
            import uvicorn
            from .api import create_app
            logging.basicConfig(level=logging.INFO,format="%(message)s")
            uvicorn.run(create_app(settings),host=settings.api_host,port=settings.api_port,access_log=False,limit_concurrency=8)
        return 0
    except KeyboardInterrupt:
        return 130
    except Exception as error:
        print(json.dumps({"status":"FAILED","error_code":code_of(error)},ensure_ascii=False),file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
