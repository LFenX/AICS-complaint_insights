"""Targeted correction of round-2 fixture assumptions; retains original results."""
import asyncio
from dataclasses import replace
from datetime import datetime, timezone
from email.utils import format_datetime
import hashlib
import json
from pathlib import Path
import runpy
import ssl
import sys
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
ns=runpy.run_path(str(HERE/'round-2-probe.py'),run_name='round2_import')
ROOT=ns['ROOT']
Settings=ns['Settings']
Fixture=ns['Fixture']
check=ns['check']
phase=ns['phase']
results=ns['result']
results['purpose']='原始57项结果不改写；只复核三项错误探针前提，补充当前疑点的条件对照与必要契约。'

class AnchoredFixture(Fixture):
    def add(self,c,pk,instant='2026-10-01T16:00:00Z',folder='INBOX',header=None):
        if header is None and instant is not None:
            header=format_datetime(datetime.fromisoformat(instant.replace('Z','+00:00')))
        super().add(c,pk,instant,folder,header)

def fixture_checks():
    with AnchoredFixture() as f:
        f.seed()
        f.reads()
        detail=f.get('/v1/mails/11')['mail']
        dates=f.get('/v1/mails')['items']
        results['anchored_fixture']={'dates':{r['mail_pk']:r['business_date'] for r in dates},'fallback_skew_hours':f.state()['fallback_skew_hours']}
        with f.owner() as c:
            c.execute("SELECT pg_advisory_xact_lock(hashtext('complaint-insights:'||%s))",(f.s.source_id,))
            before=f.state()
            busy=ns['sync_once'](f.s)
            after=f.state()
            check('concurrent-same-source-worker-busy-no-watermark-change',busy['status']=='BUSY' and before['data_version']==after['data_version'] and before['source_event_id']==after['source_event_id'])
        with f.write() as c:
            c.execute('ALTER TABLE public.messages ADD COLUMN r2_extra text')
            c.execute("UPDATE public.messages SET r2_extra='synthetic extra' WHERE id=11")
        changed=ns['sync_once'](f.s)
        payload=f.get('/v1/source-records',table='messages',record_key='11',include_payload=True)['items'][0]['payload']
        check('new-source-column-kept-in-complete-json-mirror',changed['mode']=='RECONCILE' and payload['r2_extra']=='synthetic extra')
        state=f.state()
        changed=replace(f.s,source_url=f.s.source_url.replace('127.0.0.1','localhost'))
        denied=False
        try: ns['sync_once'](changed)
        except ValueError: denied=True
        check('existing-source-id-different-explicit-identity-rejected',denied and f.state()['data_version']==state['data_version'])

def fallback_assumption():
    from insights.time_rules import detect_fallback_skew,received_at
    samples=[{'internal_date':'2026-10-02T00:01:00Z','date_header':'Thu, 01 Oct 2026 16:01:00 +0000'}]
    skew=detect_fallback_skew(samples)
    instant,shift=received_at({'internal_date':'2026-10-01T16:00:00Z'},skew)
    actual={'fallback_skew_hours':skew,'no_header_shift_hours':shift,'utc_after_correction':instant.isoformat()}
    results['initial_date_assumption']=actual
    check('initial-unanchored-fixture-correctly-triggered-measured-fallback',skew==8 and shift==8,actual)

async def tls_checks():
    import httpx2
    config=json.loads((ROOT/'.secrets/mcp-client.json').read_text(encoding='utf-8'))
    ca=ROOT/'config/mcp-ca.crt'
    fingerprint=hashlib.sha256(ssl.PEM_cert_to_DER_cert(ca.read_text(encoding='ascii'))).hexdigest()
    trusted=ssl.create_default_context(cafile=str(ca))
    empty=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    headers={'Authorization':'Bearer '+config['bearer_token']}
    async with httpx2.AsyncClient(verify=trusted,trust_env=False,timeout=10) as c:
        r=await c.get(config['url'].removesuffix('/mcp')+'/health',headers=headers)
        check('explicit-delivered-ca-verifies-real-https',r.status_code==200,{'http_status':r.status_code})
    denied=False
    error_type=None
    async with httpx2.AsyncClient(verify=empty,trust_env=False,timeout=10) as c:
        try: await c.get(config['url'].removesuffix('/mcp')+'/health',headers=headers)
        except Exception as e:
            denied='certificate verify failed' in str(e).lower()
            error_type=type(e).__name__
    check('empty-trust-store-rejects-untrusted-server-certificate',denied,{'error_type':error_type,'verify_mode':int(empty.verify_mode),'check_hostname':empty.check_hostname,'trust_anchors':empty.cert_store_stats()['x509_ca']})
    matching=0
    if sys.platform=='win32':
        matching=sum(hashlib.sha256(c).hexdigest()==fingerprint for c,encoding,trust in ssl.enum_certificates('ROOT') if encoding=='x509_asn')
    results['system_ca_store']={'delivered_ca_present':matching>0,'matching_certificates':matching}
    check('initial-default-trust-assumption-explained',matching>0,results['system_ca_store'])

def production_condition_checks():
    s=Settings.load()
    cases=[]
    candidates=[
        replace(s,source_url='postgresql://placeholder@203.0.113.1:5432/synthetic'),
        replace(s,source_url='postgresql://placeholder@203.0.113.1:5432/synthetic?sslmode=require',allow_production_read=True),
        replace(s,source_url='postgresql://placeholder@203.0.113.1:5432/synthetic?sslmode=verify-full&sslrootcert='+str(ROOT/'config/mcp-ca.crt').replace('\\','/'),allow_production_read=True,source_certificate_sha256='00'*32),
    ]
    for candidate in candidates:
        try: candidate.validate(source=True)
        except ValueError: cases.append(True)
        else: cases.append(False)
    check('explicit-production-disabled-weak-tls-wrong-fingerprint-rejected-offline',all(cases),{'cases_rejected':sum(cases),'connections_attempted':0})
    with patch.dict('os.environ',{'PGHOST':'203.0.113.1','PGPORT':'6543','PGDATABASE':'synthetic'}):
        s.validate(source=True)
        check('complete-existing-dsn-retains-explicit-identity',ns['connection_identity'](s.source_url)['host']=='127.0.0.1')

def main():
    phase('fallback-assumption',fallback_assumption)
    phase('anchored-fixture',fixture_checks)
    phase('tls',lambda:asyncio.run(tls_checks()))
    phase('production-condition',production_condition_checks)
    phase('baseline',ns['baseline'])
    results['completed_at']=datetime.now(timezone.utc).isoformat()
    results['summary']={'checks':len(results['checks']),'passed':sum(c['passed'] for c in results['checks']),'failed_checks':[c['name'] for c in results['checks'] if not c['passed']]}
    (HERE/'round-2-followup-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
    print(json.dumps({'summary':results['summary']}))

if __name__=='__main__':main()
