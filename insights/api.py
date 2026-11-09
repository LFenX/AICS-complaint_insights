from collections import defaultdict
from datetime import date, datetime, timezone
from enum import Enum
from typing import Annotated
import base64
import hashlib
import hmac
import json
import logging
import time
import uuid

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import psycopg

from . import __version__
from .capabilities import CAPABILITIES, PERMISSIONS
from .config import Settings
from .db import target_connection
from .datasets import Dataset, dataset_catalog
from .daily_generation import generation_availability
from .source import BY_NAME

logger = logging.getLogger("insights.audit")


def safe_integers(value):
    if type(value) is int and abs(value)>9007199254740991:
        return str(value)
    if isinstance(value,dict):
        return {key:safe_integers(item) for key,item in value.items()}
    if isinstance(value,list):
        return [safe_integers(item) for item in value]
    return value


class AgentJSONResponse(JSONResponse):
    def render(self,content):
        return super().render(safe_integers(content))


class Direction(str, Enum):
    RECEIVED = "RECEIVED"
    SENT = "SENT"
    EXCLUDED = "EXCLUDED"
    ALL = "ALL"


class Scope(str, Enum):
    primary = "primary"
    all_issues = "all_issues"


def encode_cursor(secret, value):
    body = json.dumps(value,sort_keys=True,separators=(",",":")).encode()
    signature = hmac.new(secret.encode(),body,hashlib.sha256).digest()
    return base64.urlsafe_b64encode(signature+body).decode().rstrip("=")


def decode_cursor(secret, token):
    try:
        if len(token)>4096:
            raise ValueError()
        blob = base64.urlsafe_b64decode(token+"="*(-len(token)%4))
        signature,body = blob[:32],blob[32:]
        if not hmac.compare_digest(signature,hmac.new(secret.encode(),body,hashlib.sha256).digest()):
            raise ValueError()
        value = json.loads(body)
        if not isinstance(value,dict):
            raise ValueError()
        return value
    except (ValueError,TypeError,UnicodeError):
        raise HTTPException(422,"invalid pagination cursor") from None


def filter_digest(value):
    return hashlib.sha256(json.dumps(jsonable_encoder(value),sort_keys=True).encode()).hexdigest()


def create_app(settings: Settings | None = None):
    settings = settings or Settings.load()
    settings.validate()
    bearer = HTTPBearer(auto_error=False)

    def authenticate(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]):
        if not credentials or not hmac.compare_digest(credentials.credentials.encode(),settings.api_token.encode()):
            raise HTTPException(401,"valid agent bearer token required",headers={"WWW-Authenticate":"Bearer"})
        return "local-agent"

    app = FastAPI(title="客诉分析数据接口",version=__version__,docs_url=None,redoc_url=None,openapi_url=None,dependencies=[Depends(authenticate)],default_response_class=AgentJSONResponse)

    @app.middleware("http")
    async def audit(request: Request,call_next):
        request_id = uuid.uuid4().hex
        started = time.monotonic()
        try:
            response = await call_next(request)
        except psycopg.Error:
            response = JSONResponse(status_code=503,content={"detail":"analytics database unavailable"})
        response.headers["X-Request-ID"] = request_id
        route = request.scope.get("route")
        logger.info(json.dumps({"request_id":request_id,"route":getattr(route,"path","unmatched"),"method":request.method,
                                "status":response.status_code,"duration_ms":round((time.monotonic()-started)*1000)}))
        return response

    def open_read():
        with target_connection(settings,reader=True) as conn:
            yield conn

    DB = Annotated[psycopg.Connection,Depends(open_read)]
    SourceID = Annotated[str | None,Query(pattern=r"^[a-z][a-z0-9_-]{1,63}$",max_length=64)]

    def state_for(conn,sid):
        state = conn.execute("SELECT * FROM analysis.v_sync_status WHERE source_id=%s",(sid,)).fetchone()
        if not state:
            raise HTTPException(404,"source namespace not found")
        if state["data_version"]==0:
            raise HTTPException(503,"source has no published data")
        return state

    def metadata(state):
        return {key:state[key] for key in ["source_id","data_version","status","source_snapshot_at","last_sync_at","last_aux_at","last_reconcile_at"]}

    def page_state(state,cursor,filters,kind):
        if not cursor:
            return None
        body = decode_cursor(settings.api_token,cursor)
        if body.get("source_id") != state["source_id"] or body.get("kind") != kind or body.get("filter") != filter_digest(filters):
            raise HTTPException(422,"cursor does not belong to these filters/source")
        if body.get("version") != state["data_version"]:
            raise HTTPException(409,"data changed during pagination; restart the query or use a repeatable-read SQL transaction")
        last = body.get("last")
        if kind in {"taxonomy", "source-records"}:
            if not isinstance(last,str): raise HTTPException(422,"invalid taxonomy cursor position")
        else:
            size = 4 if kind == "daily" else 2
            if not isinstance(last,list) or len(last)!=size: raise HTTPException(422,"invalid cursor position")
            try:
                date.fromisoformat(last[0])
                if kind != "daily" and not 1 <= int(last[1]) <= 9223372036854775807: raise ValueError()
                if kind == "daily" and any(not isinstance(item,str) for item in last[1:]): raise ValueError()
            except (ValueError,TypeError): raise HTTPException(422,"invalid cursor position") from None
        return last

    def next_page(state,filters,kind,last):
        return encode_cursor(settings.api_token,{"source_id":state["source_id"],"version":state["data_version"],"filter":filter_digest(filters),"kind":kind,"last":jsonable_encoder(last)})

    @app.get("/health")
    def health(conn:DB):
        conn.execute("SELECT 1")
        return {"status":"ok","service":"complaint-insights"}

    @app.get("/openapi.json")
    def openapi():
        return app.openapi()

    @app.get("/v1/capabilities")
    def capabilities(conn:DB,source_id:SourceID=None):
        sid = source_id or settings.source_id
        state = conn.execute("SELECT * FROM analysis.v_sync_status WHERE source_id=%s",(sid,)).fetchone()
        ready = bool(state and state["data_version"]>0)
        return {"source_id":sid,"permissions":PERMISSIONS,"capabilities":{key:{**value,**(generation_availability(state) if key == "daily_generation" else {"enabled":ready,"disabled_reason":None if ready else "source has no published data"})} for key,value in CAPABILITIES.items()}}

    @app.get("/v1/sync/status")
    def status(conn:DB,source_id:SourceID=None):
        sid = source_id or settings.source_id
        state = state_for(conn,sid)
        latest = conn.execute("SELECT * FROM analysis.v_sync_runs WHERE source_id=%s ORDER BY id DESC LIMIT 1",(sid,)).fetchone()
        stale = (datetime.now(timezone.utc)-state["last_sync_at"]).total_seconds() if state["last_sync_at"] else None
        return {"source":state,"seconds_since_last_success":round(stale,1) if stale is not None else None,"latest_run":latest,
                "schedule":{"poll_seconds":settings.poll_seconds,"auxiliary_seconds":settings.auxiliary_seconds,"full_reconcile_seconds":settings.reconcile_seconds},
                "consistency":"eventual current-state mirror; source events plus periodic reconciliation; not a complete historical CDC log"}

    @app.get("/v1/taxonomy")
    def taxonomy(conn:DB,source_id:SourceID=None,level:Annotated[int | None,Query(ge=1,le=3)]=None,
                 status:Annotated[str | None,Query(max_length=32)]=None,limit:Annotated[int,Query(ge=1,le=1000)]=200,cursor:Annotated[str | None,Query(max_length=4096)]=None):
        sid = source_id or settings.source_id
        state = state_for(conn,sid)
        filters = {"level":level,"status":status}
        last = page_state(state,cursor,filters,"taxonomy")
        conditions,args = ["source_id=%s"],[sid]
        if level is not None: conditions.append("level=%s"); args.append(level)
        if status is not None: conditions.append("status=%s"); args.append(status)
        if last is not None: conditions.append("category_id>%s"); args.append(last)
        rows = conn.execute("SELECT * FROM analysis.taxonomy WHERE "+" AND ".join(conditions)+" ORDER BY category_id LIMIT %s",[*args,limit+1]).fetchall()
        more = len(rows)>limit
        rows = rows[:limit]
        for row in rows: row.pop("source_id",None)
        return {"meta":metadata(state),"items":rows,"next_cursor":next_page(state,filters,"taxonomy",rows[-1]["category_id"]) if more else None}

    @app.get("/v1/source-tables")
    def source_tables(conn:DB,source_id:SourceID=None):
        state = state_for(conn,source_id or settings.source_id)
        return {"meta":metadata(state),"items":dataset_catalog(),
                "note":"原始副本用于追溯与对账；日期分类统计使用 /v1/daily，当前邮件使用 /v1/mails。"}

    @app.get("/v1/source-records")
    def source_records(conn:DB,table:Dataset,source_id:SourceID=None,
                       record_key:Annotated[str | None,Query(min_length=1,max_length=512)]=None,
                       include_deleted:bool=False,include_payload:bool=False,
                       limit:Annotated[int,Query(ge=1,le=50)]=20,
                       cursor:Annotated[str | None,Query(max_length=4096)]=None):
        state = state_for(conn,source_id or settings.source_id)
        selected = BY_NAME[table.value]
        filters = {"table":table.value,"record_key":record_key,"include_deleted":include_deleted,"include_payload":include_payload}
        last = page_state(state,cursor,filters,"source-records")
        conditions,args = ["source_id=%s","source_domain=%s","source_table=%s"],[state["source_id"],selected.domain,selected.name]
        if not include_deleted: conditions.append("deleted_at IS NULL")
        if record_key is not None: conditions.append("record_key=%s");args.append(record_key)
        if last is not None: conditions.append("record_key>%s");args.append(last)
        fields = "source_id,source_domain,source_table,record_key,synced_at,deleted_at"
        if include_payload: fields += ",payload"
        rows = conn.execute("SELECT "+fields+" FROM analysis.v_source_records WHERE "+" AND ".join(conditions)+" ORDER BY record_key LIMIT %s",[*args,limit+1]).fetchall()
        more = len(rows)>limit
        rows = rows[:limit]
        return {"meta":metadata(state),"items":rows,
                "next_cursor":next_page(state,filters,"source-records",rows[-1]["record_key"]) if more else None,
                "note":"默认只返回记录键和同步元数据；include_payload=true 才加载完整源行。键按文本排序。"}

    def checked_dates(start,end):
        if start is not None and end is not None and start>=end:
            raise HTTPException(422,"start must precede exclusive end")

    @app.get("/v1/daily")
    def daily(conn:DB,start:date,end:date,source_id:SourceID=None,level:Annotated[int,Query(ge=1,le=3)]=1,
              scope:Scope=Scope.primary,direction:Direction=Direction.RECEIVED,mailbox:Annotated[str | None,Query(max_length=320)]=None,
              limit:Annotated[int,Query(ge=1,le=1000)]=200,cursor:Annotated[str | None,Query(max_length=4096)]=None):
        checked_dates(start,end)
        sid = source_id or settings.source_id
        state = state_for(conn,sid)
        filters = {"start":start,"end":end,"level":level,"scope":scope,"direction":direction,"mailbox":mailbox}
        last = page_state(state,cursor,filters,"daily")
        conditions,args = ["source_id=%s","scope=%s","category_depth=%s","business_date>=%s","business_date<%s"],[sid,scope.value,level,start,end]
        if direction != Direction.ALL: conditions.append("direction=%s"); args.append(direction.value)
        if mailbox is not None: conditions.append("mailbox=%s"); args.append(mailbox)
        query = "WITH buckets AS (SELECT business_date,level_one,level_two,issue_type_id,sum(mail_count)::bigint AS mail_count,sum(issue_count)::bigint AS issue_count,sum(pending_mail_count)::bigint AS pending_mail_count FROM analysis.daily_category WHERE "+" AND ".join(conditions)+" GROUP BY 1,2,3,4) SELECT b.*,t.name AS category_name,t.status AS category_status FROM buckets b LEFT JOIN analysis.taxonomy t ON t.source_id=%s AND t.category_id=CASE WHEN %s=1 THEN b.level_one WHEN %s=2 THEN nullif(b.level_two,'') ELSE nullif(b.issue_type_id,'') END"
        args += [sid,level,level]
        if last is not None:
            query += " WHERE (b.business_date,b.level_one,b.level_two,b.issue_type_id)>(%s::date,%s,%s,%s)"
            args += last
        rows = conn.execute(query+" ORDER BY b.business_date,b.level_one,b.level_two,b.issue_type_id LIMIT %s",[*args,limit+1]).fetchall()
        more = len(rows)>limit
        rows = rows[:limit]
        last_key = [rows[-1][key] for key in ["business_date","level_one","level_two","issue_type_id"]] if rows else None
        return {"meta":metadata(state),"date_range":{"start":start,"end_exclusive":end,"timezone":"Asia/Shanghai"},"scope":scope.value,
                "items":rows,"next_cursor":next_page(state,filters,"daily",last_key) if more else None,
                "counting_note":"primary 邮件仅归入一个主分类；all_issues 同一邮件可属于多个分类，跨分类相加不能当作去重总数"}

    def read_mails(conn,*,state,start,end,scope,direction,mailbox,level_one,level_two,issue_type_id,limit,cursor,kind,include_body=False):
        checked_dates(start,end)
        sid = state["source_id"]
        filters = {"start":start,"end":end,"scope":scope,"direction":direction,"mailbox":mailbox,"level_one":level_one,"level_two":level_two,"issue_type_id":issue_type_id,"include_body":include_body}
        last = page_state(state,cursor,filters,kind)
        conditions,args = ["f.source_id=%s"],[sid]
        if start is not None: conditions.append("f.business_date>=%s"); args.append(start)
        if end is not None: conditions.append("f.business_date<%s"); args.append(end)
        if direction != Direction.ALL: conditions.append("f.direction=%s"); args.append(direction.value)
        if mailbox is not None: conditions.append("f.mailbox=%s"); args.append(mailbox)
        classification = []
        for key,value in [("level_one",level_one),("level_two",level_two),("issue_type_id",issue_type_id)]:
            if value is not None:
                if scope == Scope.primary:
                    conditions.append("f."+key+"=%s")
                else:
                    expression = f"CASE WHEN f.analysis_state='DONE' THEN i.{key} ELSE " + ("'PEND'" if key=="level_one" else "''") + " END"
                    classification.append(expression+"=%s")
                args.append(value)
        if classification:
            conditions.append("EXISTS(SELECT 1 FROM analysis.mail_issue i WHERE i.source_id=f.source_id AND i.mail_pk=f.mail_pk AND "+" AND ".join(classification)+")")
        if last is not None:
            conditions.append("(coalesce(f.business_date,'9999-12-31'::date),f.mail_pk)>(%s::date,%s::bigint)")
            args += last
        relation = "analysis.v_mail_details" if include_body else "analysis.mail_fact"
        rows = conn.execute("SELECT f.* FROM "+relation+" f WHERE "+" AND ".join(conditions)+" ORDER BY coalesce(f.business_date,'9999-12-31'::date),f.mail_pk LIMIT %s",[*args,limit+1]).fetchall()
        more = len(rows)>limit
        rows = rows[:limit]
        last_key = [rows[-1]["business_date"] or date(9999,12,31),str(rows[-1]["mail_pk"])] if rows else None
        for row in rows:
            row["mail_pk"] = str(row["mail_pk"])
            for key in ["raw_record","ai_record","raw_payload","body_html"]:
                row.pop(key,None)
        return {"meta":metadata(state),"items":rows,"next_cursor":next_page(state,filters,kind,last_key) if more else None}

    @app.get("/v1/mails")
    def mails(conn:DB,source_id:SourceID=None,start:date | None=None,end:date | None=None,scope:Scope=Scope.primary,direction:Direction=Direction.ALL,
              mailbox:Annotated[str | None,Query(max_length=320)]=None,level_one:Annotated[str | None,Query(max_length=100)]=None,
              level_two:Annotated[str | None,Query(max_length=100)]=None,issue_type_id:Annotated[str | None,Query(max_length=200)]=None,
              limit:Annotated[int,Query(ge=1,le=200)]=50,cursor:Annotated[str | None,Query(max_length=4096)]=None):
        state = state_for(conn,source_id or settings.source_id)
        return read_mails(conn,state=state,start=start,end=end,scope=scope,direction=direction,mailbox=mailbox,level_one=level_one,level_two=level_two,issue_type_id=issue_type_id,limit=limit,cursor=cursor,kind="mails")

    @app.get("/v1/mails/{mail_pk}")
    def mail_detail(mail_pk:int,conn:DB,source_id:SourceID=None,include_raw:bool=False):
        if mail_pk < 1 or mail_pk > 9223372036854775807:
            raise HTTPException(422,"invalid source mail primary key")
        sid = source_id or settings.source_id
        state = state_for(conn,sid)
        row = conn.execute("SELECT * FROM analysis.v_mail_details WHERE source_id=%s AND mail_pk=%s",(sid,mail_pk)).fetchone()
        if not row:
            archive = conn.execute("SELECT old_message_pk FROM analysis.v_archives WHERE source_id=%s AND old_message_pk=%s",(sid,str(mail_pk))).fetchone()
            raise HTTPException(410 if archive else 404,"mail was archived or is not present in the current source snapshot")
        row["mail_pk"] = str(row["mail_pk"])
        if not include_raw:
            row.pop("raw_record",None);row.pop("ai_record",None);row.pop("raw_payload",None)
        attachments = [item["payload"] for item in conn.execute("SELECT payload FROM analysis.v_attachments WHERE source_id=%s AND mail_pk=%s",(sid,str(mail_pk)))]
        issues = conn.execute("SELECT * FROM analysis.mail_issue WHERE source_id=%s AND mail_pk=%s ORDER BY is_primary DESC,issue_point_key",(sid,mail_pk)).fetchall()
        for issue in issues: issue["mail_pk"] = str(issue["mail_pk"])
        return {"meta":metadata(state),"mail":row,"attachments":attachments,"issue_bindings":issues}

    @app.get("/v1/report-context")
    def report_context(conn:DB,start:date,end:date,source_id:SourceID=None,scope:Scope=Scope.primary,direction:Direction=Direction.RECEIVED,
                       level_one:Annotated[str | None,Query(max_length=100)]=None,level_two:Annotated[str | None,Query(max_length=100)]=None,
                       issue_type_id:Annotated[str | None,Query(max_length=200)]=None,
                       include_body:bool=False,limit:Annotated[int,Query(ge=1,le=100)]=20,cursor:Annotated[str | None,Query(max_length=4096)]=None):
        state = state_for(conn,source_id or settings.source_id)
        page = read_mails(conn,state=state,start=start,end=end,scope=scope,direction=direction,mailbox=None,level_one=level_one,level_two=level_two,
                          issue_type_id=issue_type_id,limit=limit,cursor=cursor,kind="report-context",include_body=include_body)
        groups = defaultdict(lambda:defaultdict(list))
        items = page.pop("items")
        bindings = defaultdict(list)
        if scope == Scope.all_issues and items:
            for binding in conn.execute("SELECT * FROM analysis.mail_issue WHERE source_id=%s AND mail_pk=ANY(%s::bigint[])",(state["source_id"],[row["mail_pk"] for row in items])):
                bindings[str(binding["mail_pk"])].append(binding)
        for row in items:
            categories = {row["level_two"] or row["level_one"]}
            if scope == Scope.all_issues and row["analysis_state"] == "DONE":
                categories = {binding["level_two"] or binding["level_one"] for binding in bindings[row["mail_pk"]]
                              if (level_one is None or binding["level_one"]==level_one)
                              and (level_two is None or binding["level_two"]==level_two)
                              and (issue_type_id is None or binding["issue_type_id"]==issue_type_id)}
            for category in sorted(categories):
                groups[str(row["business_date"])][category].append(row)
        page["days"] = [{"date":day,"categories":[{"category_id":category,"mails":mails} for category,mails in categories.items()]} for day,categories in groups.items()]
        page["date_range"] = {"start":start,"end_exclusive":end,"timezone":"Asia/Shanghai"}
        page["note"] = "先查询 /v1/daily 获取完整计数，再分页取上下文；本响应仅包含当前页，不代表完整周期总量"
        return page

    return app
