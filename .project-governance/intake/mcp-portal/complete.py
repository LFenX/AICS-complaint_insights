"""Save factual coverage and delivery hashes. No credential values are read here."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[3]
TASK='T-INSIGHTS-MCP-PORTAL-20261030-01'
REL=f'LG_project_docs/requirements/{TASK}'
DOCS=ROOT/REL
SKILL=Path(r'C:\Users\Administrator\.codex\skills\run-governed-product-workflow')
INPUT=Path(__file__).parent
TASKDIR=ROOT/'.project-governance/tasks'/TASK


def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')


def main():
    now=datetime.now(timezone.utc).isoformat()
    before=json.loads((TASKDIR/'before.json').read_text(encoding='utf-8'))
    result=json.loads((DOCS/'verification/results.json').read_text(encoding='utf-8'))
    assert result['result']=='Passed' and result['tool_count']==11 and len(result['source_tables'])==14
    tests=(ROOT/'.runtime/mcp-portal-tests-A06.log').read_text(encoding='utf-8-sig')
    assert 'Ran 25 tests' in tests and tests.rstrip().endswith('OK')
    for name in ['desktop.png','mobile.png']:
        shutil.copyfile(ROOT/'.runtime/mcp-portal-ui'/name,DOCS/'ui-previews'/name)
    shutil.copyfile(ROOT/'.runtime/mcp-portal-ui/layout-results.json',DOCS/'verification/layout-results.json')
    checks={
        'R-01':('完整接收人指南、schema和23文件无凭据包公开下载成功', [f'{REL}/release/client-guide.md',f'{REL}/verification/results.json']),
        'R-02':('真实原生initialize/initialized/tools/list/tools/call通过；下载的标准库、SDK、11工具程序和22页分页运行通过',[f'{REL}/verification/results.json','scripts/mcp_protocol_client.py']),
        'R-03':('25项安全/并发/协议契约测试与真实管理员签发使用撤销链路通过；普通工程复核完成，正式人类门禁仍Pending',['.runtime/mcp-portal-tests-A06.log',f'{REL}/verification/results.json']),
        'R-04':('3029仅192.168.10.20 HTTPS监听；防火墙限制192.168.10.0/24 Domain/Private；通过内网IP实际请求成功',[f'{REL}/verification/listeners.json',f'{REL}/verification/results.json']),
        'R-05':('同一3029服务提供可读guide、11工具逐参数文档、协议及全部公共下载，公开包秘密扫描通过',[f'{REL}/release/client-guide.md',f'{REL}/verification/results.json']),
        'R-06':('一个入口链接包含快速开始、CA信任、逐人领令牌、客户端安装与查询、选源、排错及管理员入口；桌面与430窄屏无横向溢出',[f'{REL}/verification/layout-results.json',f'{REL}/release/client-guide.md']),
        'R-07':('本新会话只管理desk/mcp，3030/3036监听进程在部署前后保持195256/151136；无主项目、生产、采集或旧封存任务写入',[f'{REL}/verification/listeners.json','.runtime/mcp-portal-survey/pre-deploy-listeners.json',f'{REL}/discovery/survey.md']),
        'R-08':('依继续指令完成既有MCP范围，保留唯一所有者发放，无额外管理员或匿名签发',[f'{REL}/verification/results.json',f'{REL}/prd/portal.md']),
        'R-09':('继续沿用本人发放边界：真实所有者登录发放/撤销成功，访客401及错误CSRF403；接收人Bearer不能成为管理员',[f'{REL}/verification/results.json','.runtime/mcp-portal-tests-A06.log']),
    }
    # Review the complete original text, not just implementation criteria.
    raw=before['request_snapshot']['text']
    requirements=before['requirement_items']
    for item in requirements:
        actual,refs=checks[item['id']]
        text=raw if item['source']=='request_snapshot' else before['clarification']['rounds'][0]['exchanges'][0]['answer']
        cases=[{'condition':None,'branch':'Unconditional','input':item['quote'],'expected':item['reading'],'actual':actual,'result':'Passed','evidence_refs':refs}]
        conditions=[]
        if item['id']=='R-09':
            conditions=['只有独立管理员会话和同源CSRF校验通过时，才可发放或撤销']
            cases=[{'condition':0,'branch':'Met','input':'有效owner口令登录及该会话CSRF','expected':'发放成功，MCP新令牌可用，撤销后旧令牌401','actual':'真实HTTPS链路全部成立；临时身份已撤销','result':'Passed','evidence_refs':refs},
                   {'condition':0,'branch':'NotMet','input':'无管理会话、仅MCP Bearer、跨会话/缺失/错误CSRF或跨Origin','expected':'不能发放或撤销','actual':'真实匿名401/错误CSRF403，契约测试覆盖其余拒绝分支','result':'Passed','evidence_refs':refs}]
        item.update({'state':'Covered','evidence_refs':refs,'review':{'source_sha256':hashlib.sha256(text.encode()).hexdigest(),'conditions':conditions,'cases':cases}})
    save(INPUT/'coverage-amendment.json',[{'path':'requirement_items','value':requirements}])
    save(DOCS/'verification/coverage.json',{'reviewed_at':now,'request_snapshot':raw,'clarification':before['clarification'],
        'items':[{'id':r['id'],'quote':r['quote'],'reading':r['reading'],'status':'已实现','actual':checks[r['id']][0],'evidence_refs':checks[r['id']][1],'review':r['review']} for r in requirements],
        'limits':['本机经内网IP验证，另一台电脑网络与CA安装未实测','正式independent-review和security-privacy-review无真实通过决定','用户验收Pending；多轮对抗性审查尚未启动']})
    lines=['# MCP门户工程验证与原话覆盖','',f'保存时间：{now}。功能工程验证通过，正式人类审查与验收Pending。','',
        '## 原始请求','',raw,'','## 逐条核对（以完整原话为基准）','','|编号|要求|状态|实际证据|','|---|---|---|---|']
    for r in requirements:
        lines.append('|'+r['id']+'|'+r['reading']+'|已实现|'+checks[r['id']][0]+'|')
    lines += ['', '精确原句、来源SHA256、条件成立/不成立分支与证据引用见coverage.json；没有把测试成功记为人工批准。', '', '## 实际验证','',
        '- 25项单元/契约/安全/并发测试通过，包含6个独立进程同时签发无丢写。',
        '- 真实HTTPS共12组检查通过：11工具、14表入口、正文/AI/原始行、管理登录签发使用撤销、公开下载和脱敏。',
        '- 下载包内标准库、SDK、11工具流程均运行通过，SDK完整遍历22页后complete=true；下载schema与运行中tools/list一致。',
        '- 空表IssueTypeRegistry、IssueTypeAlias、IssueGroupLifecycle合法返回空；不制造记录。',
        '- 430/1440视口样式加载、导航与无横向溢出检查通过；截图来自经严格CA取得的公开首页HTML，在隔离无个人资料的无头浏览器渲染。',
        '- 生产读取false、MCP读取回环API与127.0.0.1:15433副本，版本24；状态DEGRADED为上次同步状态，不代表当前门户不可用。',
        '- 初始失败及修正保留在run.jsonl和各Attempt日志：Starlette中间件API、CA文件/DER指纹差异、HTTP头大小写、SDK GET流契约、旧API能力元数据、端口字符串类型。未删除失败凑通过。','',
        '## 未完成项与真实边界','',
        '- 另一台接收人电脑的网络与CA安装未实测；接收人按门户指南验证。',
        '- independent-review、security-privacy-review未取得真实最终决定；不能标为已过门禁。',
        '- 用户验收Pending；未启动多轮对抗性审查，也未改写原review或Cursor历史。',
        '- 本目录不是Git仓库；交付采用逐文件SHA256清单，不编造commit或整仓差异证明。','',
        '## 登录交付','',
        '唯一owner登录地址 https://192.168.10.20:3029/admin/login 。初始口令仍保存在服务器受限文件；用户已明确请求本会话交付，口令不进入本报告、公开门户、ZIP、截图或日志。']
    (DOCS/'verification/report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    incomplete=[{'reason':'另一台内网电脑路由、浏览器CA及接收人客户端未实测','impact':'服务端通过内网IP严格TLS已验证，异机路径仍须接收人复验','owner':'接收人','reentry_condition':'接收人在其电脑按门户快速开始取得11工具与查询结果'},
        {'reason':'independent-review与security-privacy-review尚无真实通过决定','impact':'功能与工程验证已交付，正式门禁保持Pending，结果不得标为门禁通过','owner':'用户或有权独立审查者','reentry_condition':'对当前交付与证据作出真实可核对的独立和安全审查决定'}]
    save(INPUT/'incomplete.json',incomplete)
    manifest=[]
    for item in before['artifact_manifest']:
        manifest.append({**item,'outcome':'Created'})
    for legacy,name in [('PRD','prd/portal.md'),('TDS','design/technical-design.md'),('VER','verification/results.json'),('RCR','verification/coverage.json'),('RLC','release/operator-handoff.md')]:
        manifest.append({'meta_type':'AuthorityAsset','legacy_kind':legacy,'action':'Create/Revise','asset_id':TASK+'-'+legacy.lower(),
            'content_ref':REL+'/'+name,'reason':'本次MCP门户需求、权限、验证与交接的实际载体','rule_reference':'C03/C05/C06/C09/C11/C12','owner':'当前任务用户','source_snapshot':now,'human_confirmation_refs':[],'outcome':'Created'})
    save(INPUT/'terminal-artifacts.json',manifest)
    files=['insights/token_desk.py','insights/mcp_tokens.py','insights/mcp_http.py','insights/mcp_server.py','insights/capabilities.py','scripts/token_desk_admin.py','scripts/mcp_client.py','scripts/mcp_protocol_client.py','scripts/mcp_workflow.py','scripts/mcp_portal_materials.py','scripts/build_mcp_handoff.py','scripts/mcp_portal_verify.py','scripts/verify_mcp.py','scripts/mcp-firewall.ps1','assets/token-desk.css','assets/token-desk.js','tests/test_token_desk.py','tests/test_mcp.py']
    files += [str(p.relative_to(ROOT)).replace('\\','/') for p in (ROOT/'config/mcp-queries').glob('*.json')]
    files += [REL+'/release/'+name for name in ['client-guide.template.md','client-guide.md','tools-schema.json','operator-handoff.md']]
    entries=[{'path':name,'sha256':hashlib.sha256((ROOT/name).read_bytes()).hexdigest()} for name in sorted(files)]
    save(DOCS/'verification/delivery-files.json',{'captured_at':now,'vcs':'unavailable','files':entries,'contains_secrets':False})
    save(INPUT/'terminal-snapshot.json',{'repository':'complaint-insights','root':str(ROOT),'vcs':'unavailable','captured_at':now,
        'file_manifest':REL+'/verification/delivery-files.json','file_manifest_sha256':hashlib.sha256((DOCS/'verification/delivery-files.json').read_bytes()).hexdigest()})
    (DOCS/'README.md').write_text('# MCP内网接入门户\n\n- discovery/survey.md：原话、勘察与所有者发放权限。\n- prd/portal.md：角色、页面、风险、审计、禁用原因及契约。\n- design/technical-design.md：认证、存储、网络与失败设计。\n- release/client-guide.template.md：说明模板；client-guide.md与tools-schema.json：实际schema生成的接入参考。\n- release/operator-handoff.md：唯一所有者登录、运行、材料重建与回滚，不含密码。\n- verification/results.json：真实HTTPS结果；coverage.json/report.md：原话逐条覆盖；delivery-files.json：交付文件哈希；listeners.json和layout-results.json：运行与布局证据。\n- ui-previews/desktop.png、mobile.png：匿名首页实测HTML的桌面与窄屏渲染。\n\n功能已实现和工程验证通过；正式人类门禁与用户验收Pending，异机路由未实测。\n',encoding='utf-8')
    subprocess.run([sys.executable,str(SKILL/'scripts/amend_record.py'),str(TASKDIR/'before.json'),'--changes-json-file',str(INPUT/'coverage-amendment.json'),
        '--reason','工程验证后独立重读完整原话与继续澄清，逐条登记证据和权限条件对照；不替代正式人类门禁',
        '--basis',REL+'/verification/coverage.json'],check=True)
    print(json.dumps({'result':'SAVED','requirements':len(requirements),'delivery_files':len(entries),'human_gates':'Pending','user_decision':'Pending'}))


if __name__=='__main__': main()
