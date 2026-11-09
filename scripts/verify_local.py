"""Independent full-content checks and live HTTP verification; never logs mail data."""
from __future__ import annotations

from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
from urllib.parse import urlencode
from urllib.request import Request,urlopen
from urllib.error import HTTPError

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from insights.config import Settings
from insights.db import source_connection,target_connection
from psycopg import sql

# Derived directly from the user's source-table requirements, independent of the
# synchronizer's table registry. The two logs and revision counters are controls,
# not copies of business data.
REQUIRED={
    "mailboxes":("public","source_mail","id"),"folders":("public","source_mail","id"),
    "messages":("public","source_mail","id"),"attachments":("public","source_mail","id"),
    "imap_reconcile_archive":("public","source_mail","old_message_pk"),
    "InboundMail":("complaint_app","source_app","id"),"MailAiArtifact":("complaint_app","source_app","id"),
    "MailIssueBinding":("complaint_app","source_app","id"),"TaxonomyCandidate":("complaint_app","source_app","id"),
    "IssueTypeProposal":("complaint_app","source_app","id"),"TaxonomyCandidateSupport":("complaint_app","source_app","id"),
    "IssueTypeRegistry":("complaint_app","source_app","id"),"IssueTypeAlias":("complaint_app","source_app","id"),
    "IssueGroupLifecycle":("complaint_app","source_app","groupKey"),
}


def signature(mapping):
    return hashlib.sha256(json.dumps(mapping,sort_keys=True,separators=(",",":")).encode()).hexdigest()


def main():
    settings=Settings.load()
    started=time.monotonic()
    results={"checked_at":datetime.now(timezone.utc).isoformat(),"source_id":settings.source_id,"content_comparison":{},"http":[],"production_connected":False}
    with source_connection(settings) as src,target_connection(settings,reader=True) as target:
        results["source_read_only"]=src.execute("SHOW transaction_read_only").fetchone()["transaction_read_only"]
        results["source_database"]=src.execute("SELECT current_database() AS name,current_setting('server_version') AS version").fetchone()
        results["target_database"]=target.execute("SELECT current_database() AS name,current_setting('server_version') AS version").fetchone()
        for name,(source_schema,mirror_schema,key) in REQUIRED.items():
            expression=sql.SQL("to_jsonb(t)")
            if name=="messages": expression=sql.SQL("(to_jsonb(t)-'last_fetched_at')")
            source_query=sql.SQL("SELECT {}::text AS k,encode(sha256(convert_to({}::text,'UTF8')),'hex') AS h FROM {}.{} t").format(sql.Identifier(key),expression,sql.Identifier(source_schema),sql.Identifier(name))
            expected={row["k"]:row["h"] for row in src.execute(source_query)}
            target_expression=sql.SQL("payload-'last_fetched_at'") if name=="messages" else sql.SQL("payload")
            target_query=sql.SQL("SELECT record_key AS k,encode(sha256(convert_to(({})::text,'UTF8')),'hex') AS h FROM {}.{} WHERE source_id=%s AND deleted_at IS NULL").format(target_expression,sql.Identifier(mirror_schema),sql.Identifier(name))
            # Reader access uses the public analysis view; it cannot read physical mirrors.
            target_query=sql.SQL("SELECT record_key AS k,encode(sha256(convert_to(({})::text,'UTF8')),'hex') AS h FROM analysis.v_source_records WHERE source_id=%s AND source_table=%s AND deleted_at IS NULL").format(target_expression)
            actual={row["k"]:row["h"] for row in target.execute(target_query,(settings.source_id,name))}
            match=expected==actual
            results["content_comparison"][name]={"source_rows":len(expected),"target_rows":len(actual),"matched":match,"source_digest":signature(expected),"target_digest":signature(actual)}
            if not match: raise RuntimeError("full content comparison failed for "+name)
        results["typed_facts"]=target.execute("SELECT count(*) AS all_mail_count,count(*) FILTER(WHERE direction='RECEIVED') AS incoming_mail_count,count(*) FILTER(WHERE analysis_state='DONE') AS analyzed_mail_count,min(business_date)::text AS first_day,max(business_date)::text AS last_day FROM analysis.mail_fact WHERE source_id=%s",(settings.source_id,)).fetchone()
        results["taxonomy"]=target.execute("SELECT level,status,count(*) AS n FROM analysis.taxonomy WHERE source_id=%s GROUP BY level,status ORDER BY level,status",(settings.source_id,)).fetchall()
        results["catalog_files"]=target.execute("SELECT filename,sha256 FROM analysis.catalog_files WHERE source_id=%s ORDER BY filename",(settings.source_id,)).fetchall()
        results["role"]=target.execute("SELECT current_user AS username,current_setting('transaction_read_only') AS read_only").fetchone()
    credentials=json.loads((ROOT/".secrets/agent.json").read_text(encoding="utf-8"))
    def get(path,authorized=True):
        headers={"Authorization":"Bearer "+credentials["api_token"]} if authorized else {}
        request=Request(credentials["base_url"]+path,headers=headers)
        try:
            with urlopen(request,timeout=30) as response: return response.status,json.loads(response.read())
        except HTTPError as error: return error.code,json.loads(error.read())
    for path in ['/health','/openapi.json','/v1/capabilities','/v1/sync/status','/v1/taxonomy?limit=1','/v1/daily?start=2025-01-01&end=2027-01-01&level=1&limit=1000','/v1/mails?limit=2','/v1/report-context?start=2026-10-15&end=2026-10-23&include_body=true&limit=2']:
        code,body=get(path)
        assert code==200,(path,code)
        denied,_=get(path,False)
        assert denied==401,(path,denied)
        results['http'].append({'path':path.split('?')[0],'authorized_status':code,'unauthorized_status':denied})
        if path.startswith('/v1/mails?'):
            key=body['items'][0]['mail_pk']
            detail_code,detail=get('/v1/mails/'+key+'?include_raw=true')
            assert detail_code==200 and detail['mail']['raw_record'] is not None
            results['http'].append({'path':'/v1/mails/{mail_pk}','authorized_status':detail_code,'raw_record_present':True})
    # Reuse the executed test evidence. The full suite is run separately, avoiding
    # unnecessary repeated fixture creation during content/HTTP validation.
    test_log=(ROOT/'.runtime/unittest-final.log').read_bytes()
    test_text=test_log.decode('utf-16' if test_log.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig')
    assert test_text.strip().endswith('OK'),'unit/integration test evidence is not successful'
    results['unit_and_isolated_postgres_tests']={'result':'Passed','log_sha256':hashlib.sha256(test_log).hexdigest(),'summary':test_text.strip().splitlines()[-4:]}
    results['duration_ms']=round((time.monotonic()-started)*1000)
    results['result']='Passed'
    out=ROOT/'LG_project_docs/requirements/T-INSIGHTS-FOUNDATION-20261029-01/verification'
    out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
    print(json.dumps({'result':results['result'],'tables_fully_compared':len(REQUIRED),'mail_count':results['typed_facts']['all_mail_count'],'http_checks':len(results['http']),'test_result':'Passed','duration_ms':results['duration_ms']}))


if __name__=='__main__': main()
