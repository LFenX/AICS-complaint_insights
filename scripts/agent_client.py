"""A runnable, read-only client for agents; reads only agent-scoped credentials."""
from pathlib import Path
import argparse
import json
import sys
from urllib.parse import urlencode
from urllib.request import Request,urlopen
from urllib.error import HTTPError

ROOT=Path(__file__).resolve().parents[1]


def main():
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,"reconfigure"): stream.reconfigure(encoding="utf-8")
    parser=argparse.ArgumentParser(description="查询独立客诉数据底座，不生成周报")
    parser.add_argument("command",choices=["status","taxonomy","daily","mails","mail","report-context","capabilities"])
    parser.add_argument("--credentials",type=Path,default=ROOT/".secrets/agent.json")
    parser.add_argument("--source-id")
    parser.add_argument("--start")
    parser.add_argument("--end",help="排除该日，即 [start,end)")
    parser.add_argument("--level",type=int,choices=[1,2,3])
    parser.add_argument("--scope",choices=["primary","all_issues"])
    parser.add_argument("--direction",choices=["RECEIVED","SENT","EXCLUDED","ALL"])
    parser.add_argument("--level-one")
    parser.add_argument("--level-two")
    parser.add_argument("--issue-type-id")
    parser.add_argument("--mail-pk")
    parser.add_argument("--limit",type=int)
    parser.add_argument("--cursor")
    parser.add_argument("--include-body",action="store_true")
    parser.add_argument("--include-raw",action="store_true")
    args=parser.parse_args()
    credentials=json.loads(args.credentials.read_text(encoding="utf-8"))
    paths={"status":"/v1/sync/status","taxonomy":"/v1/taxonomy","daily":"/v1/daily","mails":"/v1/mails","mail":"/v1/mails/","report-context":"/v1/report-context","capabilities":"/v1/capabilities"}
    path=paths[args.command]
    if args.command=="mail":
        if not args.mail_pk or not args.mail_pk.isdecimal(): parser.error("mail requires --mail-pk INTEGER")
        path+=args.mail_pk
    if args.command in {"daily","report-context"} and (not args.start or not args.end): parser.error("date query requires --start and --end")
    query={"source_id":args.source_id or credentials["source_id"]}
    for key in ["start","end","level","scope","direction","level_one","level_two","issue_type_id","limit","cursor"]:
        value=getattr(args,key)
        if value is not None: query[key]=value
    if args.include_body: query["include_body"]="true"
    if args.include_raw: query["include_raw"]="true"
    request=Request(credentials["base_url"]+path+"?"+urlencode(query),headers={"Authorization":"Bearer "+credentials["api_token"]})
    try:
        with urlopen(request,timeout=30) as response:
            print(response.read().decode("utf-8"))
    except HTTPError as error:
        print(json.dumps({"http_status":error.code,"detail":json.loads(error.read().decode())},ensure_ascii=False),file=sys.stderr)
        return 1
    return 0


if __name__=="__main__": raise SystemExit(main())
