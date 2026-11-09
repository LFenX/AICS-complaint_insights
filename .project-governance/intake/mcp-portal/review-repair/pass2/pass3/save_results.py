"""Save the third repair's actual evidence and freeze its delivery bytes."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

ROOT=Path(r'D:\LFEN_project\dev_project\complaint-insights')
CHAT=Path(r'C:\Users\Administrator\Documents\Codex\2026-10-30\complaint-insights-mcp')
INPUT=Path(__file__).parent
TASK='T-INSIGHTS-MCP-REPAIR-20261030-03'
PREVIOUS='T-INSIGHTS-MCP-REPAIR-20261030-02'
PARENT='T-INSIGHTS-MCP-PORTAL-20261030-01'
REL=f'LG_project_docs/requirements/{TASK}'
OLD=f'LG_project_docs/requirements/{PREVIOUS}'
DOCS=ROOT/REL

def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def save(path,value): path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def main():
    now=datetime.now(timezone.utc).isoformat()
    live=read(DOCS/'verification/results.json')
    assert live['result']=='Passed' and len(live['checks'])==17
    test_log=(ROOT/'.runtime/mcp-portal-repair3-tests-A01.log').read_text(encoding='utf-8')
    assert 'Ran 41 tests' in test_log and test_log.rstrip().endswith('OK')
    for round_number in [1,2,3]:
        for name in ['report.md','results.json']:
            shutil.copyfile(CHAT/f'work/round{round_number}'/name,DOCS/f'verification/round-{round_number}-{name}')
    shutil.copyfile(ROOT/OLD/'verification/client-acl-results.json',DOCS/'verification/client-acl-results.json')
    shutil.copyfile(DOCS/'design/review3-design.md',DOCS/'design/repair.md')
    for name in ['before','after']:
        shutil.copyfile(ROOT/f'.runtime/mcp-portal-repair3-{name}-listeners.json',DOCS/f'verification/{name}-listeners.json')
    listeners={name:read(DOCS/f'verification/{name}-listeners.json') for name in ['before','after']}
    unchanged={str(port):next(row['OwningProcess'] for row in listeners['before'] if row['LocalPort']==port)
        == next(row['OwningProcess'] for row in listeners['after'] if row['LocalPort']==port) for port in [3030,3036,15433]}
    assert all(unchanged.values())
    cap_hash=hashlib.sha256((ROOT/'insights/capabilities.py').read_bytes()).hexdigest()
    save(DOCS/'verification/deployment.json',{'checked_at':now,'changed_services':['desk','mcp'],
        'protected_listener_pids_unchanged':unchanged,'production_connected':False,'watch_started':False,
        'concurrent_capabilities':{'previous_sha256':'72f11bacf9d0343e6bb4691d9bae166fc6770d53639917188b1ca25ba25ec2cb',
            'observed_sha256':cap_hash,'root_or_review3_wrote_file':False,'specific_external_actor_verified':False,
            'delta':'新增附件日志导出权限/能力，MCP及token管理条目未变；保留新字节重新定版，未操作附件实现'}})
    fixes=read(ROOT/OLD/'verification/fixes.json')
    fixes['verified_at']=now
    fixes['test_count']=41
    fixes['live_check_count']=17
    for item in fixes['findings']:
        item['evidence_refs']=[ref.replace(OLD,REL).replace('mcp-portal-repair2-tests','mcp-portal-repair3-tests') for ref in item['evidence_refs']]
    for finding,actual in [
        ('R3-01','严格管理员JSON一次读取同时用于认证及版本摘要；跨读原子轮换后旧会话303、新口令正常200；真实管理员凭据未重置'),
        ('R3-02','非法ID-32600且不回显；Decimal保留精度，1.0/1e3及大整数表示正确响应；通知和客户端error id=null仍202；分块/Unicode/超限/断连通过'),
        ('R3-03','五分页工具空cursor被Schema拒绝且夹具后端零调用；省略/null/非空对照正常；真实五工具空cursor均INVALID_ARGUMENT'),
        ('R3-04','维护交接不再把25/12历史数量标为当前；引用本次实际报告、结果和交付摘要，历史视口证据明确标注')]:
        fixes['findings'].append({'id':finding,'result':'Fixed','actual':actual,'evidence_refs':[
            REL+'/design/repair.md',REL+'/verification/results.json','.runtime/mcp-portal-repair3-tests-A01.log']})
    save(DOCS/'verification/fixes.json',fixes)
    coverage=read(ROOT/OLD/'verification/coverage.json')
    coverage['captured_at']=now
    for item in coverage['requirements']:
        item['evidence_refs']=[ref.replace(OLD,REL).replace('mcp-portal-repair2-tests','mcp-portal-repair3-tests') for ref in item['evidence_refs']]
        if item['id']=='CURRENT-R-02':
            item['actual']='三轮共11项已修复复验；第三轮外部漂移和原始失败保留；当前重新定版后继续完整独立审查，尚未达到连续两轮条件；正式机器限制保留'
            item['evidence_refs'] += [REL+'/verification/round-3-report.md',REL+'/verification/deployment.json']
        if item['id']=='CURRENT-R-03':
            item['actual']='按真实开始授权实际执行三轮及同范围返修；不推定人类Gate批准'
    save(DOCS/'verification/coverage.json',coverage)
    (DOCS/'verification/report.md').write_text('''# MCP第三次返修工程验证

三轮共11项确认问题已修复复验，逐项见fixes.json。41项单元/契约/边界测试与真实内网严格CA的17组检查通过；包括11工具14表、SDK22页、独立管理员登录签发/使用/撤销/退出、合法字符串原值、原生错误分层、ID精度/消息类别与五工具空游标边界。客户端ACL真实Windows反例的既有证据保留，客户端本轮未改；独立下一轮将重新核对完整范围。

登录：https://192.168.10.20:3029/admin/login ，唯一用户名owner；口令仅在当前用户私聊交付，不写入报告/指南/ZIP/日志。分享门户：https://192.168.10.20:3029/ ，MCP：https://192.168.10.20:3037/mcp 。

本次仅重启desk/mcp，3030/3036/15433监听PID前后相同，见deployment.json及before/after-listeners.json。watch停止、生产读取false、目标仅127.0.0.1:15433历史副本；未连接生产或数据库。公共23文件ZIP按运行中实际Schema重建。第三轮末次检测到capabilities.py外部变更，原报告不计干净；新增的非MCP能力保留，当前版本重新纳入摘要，未回退并发工作。

原文需求逐项见coverage.json，完整三轮独立原始报告另存。第三轮缺陷、基线漂移和夹具失败原样保留。根执行准备时误用文档目录代替治理task目录、目录本身不匹配/**写入守卫、误读根manage.ps1路径，均在工具返回中暴露；改用实际任务目录、具体许可文件和scripts/manage.ps1后执行。未把失败调用冒称通过，未由这些调用改变产品或扩大权限。

正式人类门禁与用户验收Pending；另一内网电脑路由/CA未实测。父Deferred导致官方Offer登记拒绝，原拒绝保留，不改父状态、不伪造ManagedByParent或机器Passed。此报告是工程保存时快照：当前重新定版后后续独立完整审查尚未完成，不能宣称连续两轮收敛。后续实际轮次另存证据，不覆盖本快照。
''',encoding='utf-8')
    (DOCS/'README.md').write_text('# MCP第三次审查返修\n\n- discovery/survey.md：授权、边界与机器限制。\n- design/repair.md：本轮四项局部修复。\n- verification/results.json、fixes.json、coverage.json、report.md：实际验证及原文覆盖。\n- verification/deployment.json：进程隔离与外部能力漂移。\n- verification/round-1/2/3-report.md：原始独立审查留档。\n- verification/delivery-files.json：重新冻结的真实交付摘要。\n\n本工程快照的正式人类门禁及用户验收Pending；后续审查报告另存，不改写历史结论。\n',encoding='utf-8')
    previous_manifest=read(ROOT/OLD/'verification/delivery-files.json')
    names={row['path'].replace(OLD,REL) for row in previous_manifest['files']}
    names.update(REL+'/'+name for name in ['README.md','design/review3-design.md','verification/deployment.json'])
    entries=[{'path':name,'sha256':hashlib.sha256((ROOT/name).read_bytes()).hexdigest()} for name in sorted(names)]
    digest=hashlib.sha256(json.dumps(entries,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    save(DOCS/'verification/delivery-files.json',{'captured_at':now,'version_sha256':digest,'vcs':'unavailable','files':entries,'contains_secrets':False})
    save(INPUT/'terminal-snapshot.json',{'repository':'complaint-insights','root':str(ROOT),'vcs':'unavailable','captured_at':now,
        'file_manifest':REL+'/verification/delivery-files.json','file_manifest_sha256':hashlib.sha256((DOCS/'verification/delivery-files.json').read_bytes()).hexdigest()})
    before=read(ROOT/f'.project-governance/tasks/{TASK}/before.json')
    artifacts=[{**item,'outcome':'Created'} for item in before['artifact_manifest']]
    for kind,ref in [('PRD',f'LG_project_docs/requirements/{PARENT}/prd/portal.md'),('TDS',REL+'/design/repair.md'),
                     ('VER',REL+'/verification/results.json'),('RCR',REL+'/verification/coverage.json'),
                     ('RLC',f'LG_project_docs/requirements/{PARENT}/release/operator-handoff.md')]:
        derived=kind=='RCR'
        artifacts.append({'meta_type':'DerivedView' if derived else 'AuthorityAsset','legacy_kind':kind,
            'action':'Generate' if derived else 'Create/Revise','asset_id':TASK+'-'+kind.lower(),'content_ref':ref,
            'reason':'第三轮返修需求设计验证与交接；原文覆盖为派生视图','rule_reference':'C03/C05/C06/C09/C11/C12',
            'owner':'当前任务用户','source_snapshot':now,'human_confirmation_refs':[],'outcome':'Generated' if derived else 'Created'})
    save(INPUT/'terminal-artifacts.json',artifacts)
    incomplete=read(INPUT.parent/'incomplete.json')
    incomplete[-1]['reason']='父Deferred使Offer登记拒绝；三轮11项已修复，当前新版本实际独立后续审查待完成'
    save(INPUT/'incomplete.json',incomplete)
    print(json.dumps({'result':'SAVED','delivery_files':len(entries),'version_sha256':digest,'fixed_findings':11,
        'tests':41,'live_checks':17,'formal_gates':'Pending'},ensure_ascii=False))

if __name__=='__main__':main()
