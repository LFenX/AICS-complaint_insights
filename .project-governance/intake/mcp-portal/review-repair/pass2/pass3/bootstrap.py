"""Capture the third review's confirmed boundaries under continuing authority."""
from datetime import datetime,timezone
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(r'D:\LFEN_project\dev_project\complaint-insights')
SKILL=Path(r'C:\Users\Administrator\.codex\skills\run-governed-product-workflow')
PARENT='T-INSIGHTS-MCP-PORTAL-20261030-01'
PREVIOUS='T-INSIGHTS-MCP-REPAIR-20261030-02'
TASK='T-INSIGHTS-MCP-REPAIR-20261030-03'
INPUT=Path(__file__).parent
REL=f'LG_project_docs/requirements/{TASK}'
DOCS=ROOT/REL
REF=REL+'/discovery/survey.md'
SCOPE=['修复第三轮确认的管理员凭据双读竞态、JSON-RPC请求ID误降级通知和空cursor，回归此前七项边界', '只部署必要desk/mcp进程与实际Schema材料，完整验证原MCP接入和发放需求', '保存新版本并持续用户已授权审查，正式人类门禁与机器登记限制保持原意']
CRITERIA=['管理员认证内容与会话版本来自同一快照，轮换期间旧口令不能获得匹配新凭据的可用会话', '无效请求ID返回-32600而非202通知；字符串、整数及等值整数数字表示合法，真实通知和客户端响应不受误伤', '五个分页工具空字符串cursor在MCP边界拒绝，不查询后端或返回首页；省略/null和有效非空游标正常', '全部工程测试与严格CA真实15检查、11工具14表、完整分页、登录签发撤销及无凭据材料通过，生产保持隔离', '原文全覆盖与新版本摘要可核对，当前独立后续轮次与正式人类门禁状态如实保留']
STEPS=['保存第三轮独立证据与原文授权，确认最小局部修复设计', '同快照绑定管理员版本、在SDK前守卫请求ID并拒绝空cursor，运行所有反例与合法控制', '部署必要进程、捕获实际Schema重建材料并完整真实复验', '保存工程结果后进行新的独立完整审查，实际满足停止条件才收口']

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=json.loads((ROOT/f'.project-governance/tasks/{PREVIOUS}/before.json').read_text(encoding='utf-8'))
    for name in ['discovery','design','verification','release']:(DOCS/name).mkdir(parents=True,exist_ok=True)
    (DOCS/'discovery/survey.md').write_text(f'''# 第三次MCP审查返修

持续授权来源：原任务{PARENT}/before.json的完整原始请求与唯一所有者澄清、前次返修{PREVIOUS}/before.json中的实际询问及“开始审查”。原问题明确包括发现问题修复复验直到同版连续两轮完整无问题。本次同范围修复不增加管理员、生产、采集或正式门禁权限，不重复索取同一授权。

第三轮确认：管理员read_object与后续文件hash两次读取间轮换，会使旧认证数据绑定新版本；非法请求ID被SDK通知分支吞为202，合法1.0/1e3也被吞；五个分页工具cursor空字符串回到首页。独立证据在 C:/Users/Administrator/Documents/Codex/2026-10-30/complaint-insights-mcp/work/round3，根夹具在work/root-review/admin-snapshot-race.json。此记录时间{now}为捕获时间，原授权时间不重造。

根已核实固定MCP2025-11-25基础规范：请求ID必须字符串/整数且非null；通知不能包含ID；客户端错误响应id=null须保留允许。实现使用已解码的原始请求检查并重放给SDK；合法整数数值表示按等值整数处理，不改字符串值。空cursor仅需MCP的min_length=1，不改3036 API。管理员版本可对一次读取的严格JSON对象计算规范化摘要，消除第二次文件读取。

生产读取false/watch停止，源10.8.45.155:5432及所有数据库禁止连接。3030、3036、15433、日报、附件、AICS、source.py/syncer.py与历史任务不操作。异常时序与破坏性输入仅在合成夹具；真实验证只通过现有只读MCP/门户。

另一内网电脑路由/CA、正式人类门禁与验收Pending。父Deferred导致官方Offer登记拒绝，保留失败，不改写旧状态或冒称机器Passed/ManagedByParent。延续已向用户告知的跳过重复提问；没有新增权限未知。
''',encoding='utf-8')
    req=json.loads(json.dumps(previous['requirement_items'],ensure_ascii=False))
    for item in req:item.update(state='Open',evidence_refs=[REF]);item.pop('review',None)
    authority=[{'reference':REF,'source_kind':'UserDirective','status':'Valid','scope_refs':SCOPE,'evidence_refs':[REF,f'LG_project_docs/requirements/{PREVIOUS}/discovery/survey.md'],'verified_at':now,'expires_at':None}]
    analysis=json.loads((INPUT.parents[2]/'analysis.json').read_text(encoding='utf-8'))
    analysis.update(outcome=CRITERIA[0],facts=[{'id':'F1','statement':'第三轮三个反例独立复现；旧七项原反例和真实完整使用范围有复验','evidence_refs':[REF]},{'id':'F2','statement':'SDK宽松消息联合分支会把含非法ID请求当通知；后端空cursor使用首页','evidence_refs':[REF]}],constraints=[{'id':'C1','statement':'原单管理员权限、生产隔离和保护路径保持，正式Gate不由Agent批准','source_refs':[REF]}],fundamentals=[{'id':'P1','statement':'认证事实与版本必须同源，非法分页状态不能默认为有效首页','derived_from':['F1','C1']},{'id':'P2','statement':'消息类别不能丢失请求ID或误伤合法响应','derived_from':['F2','C1']}],causal_links=[{'from_ref':'P1','to_ref':'O1','rationale':'从同一管理员对象计算摘要，游标边界拒绝空字符串','evidence_refs':[REF]},{'from_ref':'P2','to_ref':'O1','rationale':'SDK前保留原始ID存在性和类型，正常消息仍交SDK处理','evidence_refs':[REF]}],alternatives=[{'id':'O1','description':'局部修复同快照、请求ID边界和非空cursor','status':'Selected','derived_from':['P1','P2'],'tradeoffs':['须回归SDK消息接收重放与合法整数表示']},{'id':'O0','description':'保持当前版本','status':'Rejected','derived_from':['P1','P2'],'tradeoffs':['三个已证实反例继续存在']},{'id':'O2','description':'替换认证及协议框架或修改3036','status':'Rejected','derived_from':['P1','P2'],'tradeoffs':['扩大影响且无需改动既有API']}],decision_criteria=[{'id':'K1','statement':'新旧反例与正常路径均通过','source_refs':[REF]},{'id':'K2','statement':'原值/原权限/保护边界和真实证据保持','source_refs':[REF]}],derivation=[{'plan_step':s,'derived_from':['P1','P2'],'supports':['K1','K2']} for s in STEPS],validation_refs=[REL+'/verification/results.json'],source_refs=[REF])
    for name,value in [('decisions',previous['decisions']),('authority',authority),('requirements',req),('analysis',analysis)]:save(INPUT/f'{name}.json',value)
    args=[sys.executable,str(SKILL/'scripts/init_task.py'),'--project-root',str(ROOT),'--project-id','complaint-insights','--work-item-id','MCP-REPAIR-3','--task-id',TASK,'--ordinal','8','--objective','关闭第三轮MCP认证与消息分页边界并完成原需求复核','--request-snapshot',previous['request_snapshot']['text'],'--request-language','zh','--development-type','DT-02','--delivery-scenario','DS-01','--risk-level','High','--baseline-inheritance','Revise','--basis',REF,'--authority-reference',REF,'--tailoring-stage','S4','--depends-on',PARENT,'--depends-on',PREVIOUS,'--out-of-scope','生产、采集、3030/3036/15433、AICS、多管理员及旧结果改写','--forbidden-action','源生产或数据库连接、watch、日报附件或旧任务操作、伪造Gate','--rollback','仅恢复本轮desk/mcp代码和公开材料，不恢复撤销令牌，不操作保护服务']
    for path in ['insights/token_desk.py','insights/mcp_http.py','insights/mcp_server.py','scripts/mcp_portal_verify.py','tests/test_mcp.py','tests/test_token_desk.py',REL+'/**',f'LG_project_docs/requirements/{PARENT}/release/**','LG_project_docs/README.md',f'.project-governance/tasks/{TASK}/**','.project-governance/intake/mcp-portal/review-repair/pass2/pass3/**','.runtime/mcp-portal*/**','.runtime/processes.json','.secrets/mcp-server.json','.secrets/mcp-token-registry.json','.secrets/mcp-handoff.zip']:args+=['--allowed-path',path]
    for surface in ['Identity/Security/Privacy','API/Integration','UI/UX','Deploy/Operations']:args+=['--change-surface',surface]
    for value in SCOPE:args+=['--in-scope',value]
    for value in CRITERIA:args+=['--acceptance',value,'--verification-plan',value]
    for value in STEPS:args+=['--plan-step',value]
    for name,flag in [('decisions','--decisions-json-file'),('authority','--authority-assessments-json-file'),('requirements','--requirement-items-json-file'),('analysis','--first-principles-json-file')]:args += [flag,str(INPUT/f'{name}.json')]
    args+=['--clarification-skipped','--clarification-notice','本轮返修沿用你已确认的范围和授权，跳过重复提问。','--clarification-basis','用户持续授权覆盖三个同范围反例修复，无新增权限或验收未知','--survey-ref',REF]
    for key,value in previous['task_profile']['applicability_facts'].items():args+=['--applicability-fact',f'{key}={value}']
    for key in ['E01','E02','E03','E05']:args+=['--extension-trigger',f'{key}=Active','--extension-evidence-ref',f'{key}={REF}']
    args+=['--extension-trigger','E04=Inactive','--required-gate','independent-review','--required-gate','security-privacy-review']
    for value in ['read','edit-in-scope','validate','external-effect','rollback']:args+=['--execution-permission',value]
    raise SystemExit(subprocess.run(args).returncode)

if __name__=='__main__':main()
