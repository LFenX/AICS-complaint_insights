"""Save actual repair evidence without changing the parent's terminal records."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[4]
SKILL=Path(r'C:\Users\Administrator\.codex\skills\run-governed-product-workflow')
TASK='T-INSIGHTS-MCP-REPAIR-20261030-01'
PARENT='T-INSIGHTS-MCP-PORTAL-20261030-01'
INPUT=Path(__file__).parent
TD=ROOT/'.project-governance/tasks'/TASK
REL=f'LG_project_docs/requirements/{TASK}'
DOCS=ROOT/REL
CHAT=Path(r'C:\Users\Administrator\Documents\Codex\2026-10-30\complaint-insights-mcp')

def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def main():
    now=datetime.now(timezone.utc).isoformat()
    before=json.loads((TD/'before.json').read_text(encoding='utf-8'))
    original=json.loads((ROOT/f'.project-governance/tasks/{PARENT}/before.json').read_text(encoding='utf-8'))
    live=json.loads((DOCS/'verification/results.json').read_text(encoding='utf-8'))
    assert live['result']=='Passed'
    shutil.copyfile(CHAT/'work/round1/report.md',DOCS/'verification/round-1-report.md')
    shutil.copyfile(CHAT/'work/round1/results.json',DOCS/'verification/round-1-results.json')
    for name in ['before','after']:
        shutil.copyfile(ROOT/f'.runtime/mcp-portal-repair-{name}-listeners.json',DOCS/f'verification/{name}-listeners.json')
    fixes=[{'id':'R1-01','result':'Fixed','evidence_refs':['tests/test_token_desk.py', '.runtime/mcp-portal-repair-tests-A02.log'],'actual':'同Cookie512次刷新复用；清Cookie第9活跃挑战429；另一peer登录303；601秒恢复'},
        {'id':'R1-02','result':'Fixed','evidence_refs':['tests/test_token_desk.py','.runtime/mcp-portal-repair-tests-A02.log'],'actual':'registry损坏网页登录303、管理200有撤销表单、发放400、撤销303，授权归零且原损坏文件保留'},
        {'id':'R1-03','result':'Fixed','evidence_refs':['tests/test_mcp.py',REL+'/verification/results.json'],'actual':'原始HTTP错误JSON类型、日期和额外参数isError，夹具后端零调用；真实服务相同拒绝'},
        {'id':'R1-04','result':'Fixed','evidence_refs':['tests/test_mcp.py',REL+'/verification/results.json'],'actual':'未知工具顶层error.code=-32602、原请求id保留、无result'}]
    save(DOCS/'verification/fixes.json',{'verified_at':now,'findings':fixes,'test_count':30,'live_check_count':len(live['checks'])})
    coverage=[]
    readings=['可分享的MCP说明与客户端','原生协议与11工具真实Schema','优化并复核安全发放服务','内网HTTPS3029入口','同服务承载协议介绍与方法','一个内网链接接入','仅MCP任务且日报不改','延续原授权','唯一所有者发放']
    for item,reading in zip(original['requirement_items'],readings,strict=True):
        coverage.append({'id':'ORIGINAL-'+item['id'],'quote':item['quote'],'source':item['source'],'reading':reading,'status':'工程已实现，异机与正式门禁限制保留','evidence_refs':[REL+'/verification/results.json',REL+'/verification/fixes.json','.runtime/mcp-portal-repair-tests-A02.log'],
            'actual':'公开指南和7项下载200；原生2025-11-25；11工具14表、22页SDK遍历；独立owner登录签发使用撤销退出；匿名管理/MCP拒绝；生产读取false且目标127.0.0.1:15433；3030/3036/15433监听PID前后不变'})
    coverage.extend([{'id':'CURRENT-R-01','quote':before['requirement_items'][0]['quote'],'status':'已实现','evidence_refs':[REL+'/verification/results.json',REL+'/discovery/survey.md'],'actual':'唯一owner凭据已在当前私聊交付；公开文档、ZIP和日志无密码；真实网页登录/生成/撤销通过'},
        {'id':'CURRENT-R-02','quote':before['requirement_items'][1]['quote'],'status':'返修完成，后续完整审查进行中','evidence_refs':[REL+'/verification/round-1-report.md',REL+'/verification/fixes.json'],'actual':'首轮四项发现已修复复验，尚未取得修复版连续两轮完整无问题；机器登记限制保留'},
        {'id':'CURRENT-R-03','quote':'开始审查','status':'已启动','evidence_refs':[REL+'/discovery/survey.md',REL+'/verification/round-1-report.md'],'actual':'用户明确授权后执行实际审查，无人工Gate批准推断'}])
    save(DOCS/'verification/coverage.json',{'captured_at':now,'basis':'完整父request_snapshot及唯一所有者澄清、当前请求和真实开始答复','requirements':coverage,'different_computer_tested':False,'formal_human_gates':'Pending','user_decision':'Pending'})
    (DOCS/'verification/report.md').write_text('''# MCP返修工程验证

四项独立首轮问题均已修复，证据见 fixes.json。30项单测/契约测试和真实内网严格CA验证的13项检查通过；11工具、14表、SDK22页、独立管理员登录签发/使用/撤销/退出均通过。7项公开下载与无凭据23文件ZIP可用。

登录：https://192.168.10.20:3029/admin/login ，唯一用户名owner，口令仅在用户本次私聊交付，不写入此报告。分享入口：https://192.168.10.20:3029/ ，MCP：https://192.168.10.20:3037/mcp 。

原始需求逐项覆盖见 coverage.json。仅desk/mcp重启；3030、3036和15433监听PID前后不变，生产读取保持false、目标仅127.0.0.1:15433、watch停止。数据仍是历史本地副本。

限制：另一内网电脑路由/CA尚未实测；正式独立/安全人类门禁与用户验收Pending。父工程结果Deferred导致官方adversarial_review.py拒绝Offer，原失败保留；没有改写父状态、人工门禁或旧账本，不能声明机器登记Passed/ManagedByParent。当前仅保存返修工程版本，修复版后续独立审查仍在进行。
''',encoding='utf-8')
    (DOCS/'README.md').write_text('# MCP审查返修\n\n- discovery/survey.md：真实授权和机器限制。\n- design/repair.md：四项修复与回滚边界。\n- verification/results.json：真实内网验证。\n- verification/fixes.json、coverage.json、report.md：修复、原话逐条核对与限制。\n- verification/delivery-files.json：当前交付摘要；首轮报告原件独立保存。\n\n正式人类门禁及用户验收Pending；后续实际独立审查不改写原工程结果。\n',encoding='utf-8')
    original_files=json.loads((ROOT/f'LG_project_docs/requirements/{PARENT}/verification/delivery-files.json').read_text(encoding='utf-8'))['files']
    files={row['path'] for row in original_files}
    files.add('requirements.txt')
    for name in ['discovery/survey.md','design/repair.md','verification/results.json','verification/fixes.json','verification/coverage.json','verification/report.md']:
        files.add(REL+'/'+name)
    for path in (ROOT/'.runtime/mcp-portal-public').iterdir():
        if path.is_file(): files.add(path.relative_to(ROOT).as_posix())
    entries=[{'path':name,'sha256':hashlib.sha256((ROOT/name).read_bytes()).hexdigest()} for name in sorted(files)]
    digest=hashlib.sha256(json.dumps(entries,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    save(DOCS/'verification/delivery-files.json',{'captured_at':now,'version_sha256':digest,'vcs':'unavailable','files':entries,'contains_secrets':False})
    save(INPUT/'terminal-snapshot.json',{'repository':'complaint-insights','root':str(ROOT),'vcs':'unavailable','captured_at':now,'file_manifest':REL+'/verification/delivery-files.json','file_manifest_sha256':hashlib.sha256((DOCS/'verification/delivery-files.json').read_bytes()).hexdigest()})
    artifacts=[{**item,'outcome':'Created'} for item in before['artifact_manifest']]
    for kind,ref in [('PRD',f'LG_project_docs/requirements/{PARENT}/prd/portal.md'),('TDS',REL+'/design/repair.md'),('VER',REL+'/verification/results.json'),('RCR',REL+'/verification/coverage.json'),('RLC',f'LG_project_docs/requirements/{PARENT}/release/operator-handoff.md')]:
        artifacts.append({'meta_type':'DerivedView' if kind=='RCR' else 'AuthorityAsset','legacy_kind':kind,'action':'Generate' if kind=='RCR' else 'Create/Revise','asset_id':TASK+'-'+kind.lower(),'content_ref':ref,'reason':'返修需求设计验证与交接，原文覆盖为派生视图','rule_reference':'C03/C05/C06/C09/C11/C12','owner':'当前任务用户','source_snapshot':now,'human_confirmation_refs':[],'outcome':'Generated' if kind=='RCR' else 'Created'})
    save(INPUT/'terminal-artifacts.json',artifacts)
    incomplete=[{'summary':'正式人类门禁Pending','reason':'independent-review与security-privacy-review没有真实通过决定','impact':'工程已验证，正式Gate不可标为通过','owner':'用户或有权审查者','reentry_condition':'对当前交付给出真实可核对决定'},
        {'summary':'异机路径未实测','reason':'另一内网电脑路由和CA安装未测试','impact':'仅本机经内网IP严格CA已验证','owner':'接收人','reentry_condition':'另一电脑按公开指南复验'},
        {'summary':'修复版后续审查进行中及机器登记受限','reason':'父Deferred导致Offer拒绝；当前返修已验证，独立后续轮次尚未完成','impact':'不能宣称官方审查Passed或两轮收敛','owner':'当前任务执行者','reentry_condition':'完成同版本两轮真实完整审查；官方登记仍需合法父工程前置状态，不绕过门禁'}]
    save(INPUT/'incomplete.json',incomplete)
    print(json.dumps({'result':'SAVED','delivery_files':len(entries),'version_sha256':digest,'verification':'Passed','formal_gates':'Pending'},ensure_ascii=False))

if __name__=='__main__': main()
