"""Record the real, user-authorized repair; retain the parent's pending gates."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
SKILL = Path(r'C:\Users\Administrator\.codex\skills\run-governed-product-workflow')
PARENT = 'T-INSIGHTS-MCP-PORTAL-20261030-01'
TASK = 'T-INSIGHTS-MCP-REPAIR-20261030-01'
INPUT = Path(__file__).parent
DOCS = ROOT / 'LG_project_docs/requirements' / TASK
REF = f'LG_project_docs/requirements/{TASK}/discovery/survey.md'
QUESTION = '工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。'
REQUEST = '把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token\n\n' + QUESTION + '\n\n开始审查'
SCOPE = ['修复独立第一轮确认的四项MCP门户/协议问题并回归原需求全部范围', '保持唯一所有者和历史本地副本边界，重建材料并只部署desk/mcp', '逐轮保存审查证据；保持原工程结果、人工门禁与验收原意']
ACCEPTANCE = ['同一匿名来源重复刷新或清除Cookie不能耗尽另一来源登录页；限制有期限且不扩大登录权限', 'registry损坏时独立管理员可在网页列出有效身份和撤销，发放仍拒绝；授权文件损坏保持全部拒绝', '工具调用执行前按公布JSON Schema验证类型/日期/额外参数；无效输入不查询后端，未知工具为JSON-RPC -32602', '全部单测、真实TLS签发查询撤销、11工具14表和接收人客户端验证通过；只重启3029/3037，生产读取关闭', '原话全部覆盖，保存版本摘要和真实限制；不把普通测试或开始审查冒充正式人工门禁批准']
STEPS = ['保存四项反例、原文与授权，推导最小修复方案', '实施按来源分配挑战、元数据故障可撤销与Schema/协议错误边界并回归', '安全重启desk/mcp、捕获实际Schema、重建公共材料并验证真实使用链路', '保存返修版本和逐条覆盖，再进行独立完整审查直至满足实际停止条件']

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def main():
    now = datetime.now(timezone.utc).isoformat()
    parent = json.loads((ROOT/f'.project-governance/tasks/{PARENT}/before.json').read_text(encoding='utf-8'))
    for name in ['discovery', 'design', 'verification', 'release']:
        (DOCS/name).mkdir(parents=True, exist_ok=True)
    (DOCS/'discovery/survey.md').write_text(f'''# MCP审查返修勘察与授权

用户实际请求及询问答复：

{REQUEST}

原需求与唯一所有者澄清完整原文沿用只读父记录 .project-governance/tasks/{PARENT}/before.json。

四项已确认问题：匿名512次GET占满登录挑战；registry损坏使网页紧急撤销不可达；SDK宽松转换输入类型；未知工具被归为执行错误。独立原件：C:/Users/Administrator/Documents/Codex/2026-10-30/complaint-insights-mcp/work/round1/report.md 与 results.json。没有生产/真实凭据故障注入。

用户答复“开始审查”明确覆盖询问中的同范围返修和复验，不代表正式门禁批准。收件归档时间 {now}，不冒称原始答复时间。

工具限制：父after为Deferred，adversarial_review.py拒绝Offer（only after an Implemented engineering result is saved）。保留该失败；不改写父状态/门禁/已结束账本。此后续普通返修任务直接依赖父任务；在机器不认可父会话时不能声明ManagedByParent或机器审查Passed。用户要求的真实审查仍继续，单独保留非治理报告并明确限制。

实现约定：不改结构命名；现有Starlette/MCP2.3/Pydantic；jsonschema4.26.0是当前MCP已安装依赖，可在公开Schema边界校验，避免SDK预解析字符串后再校验导致漏拦。只部署desk/mcp。3030、3036、15433、生产/采集、日报、AICS与所有原任务保持原范围。

明确未验项：另一内网电脑路由和CA导入不在本机可验证能力内，保留原交付限制；正式人类门禁仍Pending。没有新增阻断未知，沿用用户授权，跳过重复提问。
''', encoding='utf-8')
    decisions = [{'id':'D-MCP-REPAIR-START','kind':'Proceed','presented':QUESTION,'response':'开始审查','decided_by':'当前聊天用户','decided_at':now,'evidence_ref':REF,'outcome':'Approved'}]
    authority = [{'reference':REF,'source_kind':'UserDirective','status':'Valid','scope_refs':SCOPE,'evidence_refs':[REF],'verified_at':now,'expires_at':None}]
    req = [{'id':'RR-01','source':'request_snapshot','quote':REQUEST.split('\n\n')[0],'reading':'交付已核对的唯一管理员凭据和可生成token的登录入口，密码仅在用户本次私聊交付','state':'Open','evidence_refs':[REF],'acceptance_refs':[1,3,4]},
           {'id':'RR-02','source':'request_snapshot','quote':QUESTION,'reading':'依用户明确开始授权，按原需求完整审查、修复及复验，直到同一版本连续两轮完整无问题；保留机器登记限制','state':'Open','evidence_refs':[REF],'acceptance_refs':list(range(5))},
           {'id':'RR-03','source':'request_snapshot','quote':'开始审查','reading':'启动实际审查与同范围返修，不冒称正式人工批准','state':'Open','evidence_refs':[REF],'acceptance_refs':list(range(5))}]
    analysis = json.loads((ROOT/'.project-governance/intake/mcp-portal/analysis.json').read_text(encoding='utf-8'))
    analysis.update(outcome=ACCEPTANCE[0], facts=[{'id':'F1','statement':'第一轮四项反例在隔离夹具确认，当前运行门户及11工具可用','evidence_refs':[REF]},{'id':'F2','statement':'SDK2.3预解析JSON字符串，Pydantic字段strict不足以阻止原始错误类型','evidence_refs':[REF]}],
        constraints=[{'id':'C1','statement':'唯一所有者、生产关闭与既有保护范围保持，原人工门禁Pending','source_refs':[REF]}],
        assumptions=[], unknowns=[{'id':'U1','statement':'异机路由/CA未实测','owner':'接收人','resolution_condition':'接收人按公开指南验证','blocking':False}],
        fundamentals=[{'id':'P1','statement':'未认证单来源不能独占全局登录资源，授权撤销不依赖展示元数据','derived_from':['F1','C1']},{'id':'P2','statement':'执行前输入与错误分层必须符合已发布协议契约','derived_from':['F2','C1']}],
        causal_links=[{'from_ref':'P1','to_ref':'O1','rationale':'按真实peer限额、复用Cookie并保留故障撤销界面','evidence_refs':[REF]},{'from_ref':'P2','to_ref':'O1','rationale':'公开SDK扩展点在预解析之前校验JSON Schema并区分未知工具','evidence_refs':[REF]}],
        alternatives=[{'id':'O1','description':'保留现有接口并修正四条边界','status':'Selected','derived_from':['P1','P2'],'tradeoffs':['必须重建Schema和客户端包并回归']},{'id':'O0','description':'保持当前实现','status':'Rejected','derived_from':['P1','P2'],'tradeoffs':['四条可复现问题继续存在']},{'id':'O2','description':'替换登录和MCP框架','status':'Rejected','derived_from':['P1','P2'],'tradeoffs':['超出修复所需范围并增加兼容风险']}],
        decision_criteria=[{'id':'K1','statement':'四条反例拒绝且合法链路通过','source_refs':[REF]},{'id':'K2','statement':'保持范围、真实证据和人工门禁状态','source_refs':[REF]}],selected_approach='O1',
        derivation=[{'plan_step':step,'derived_from':['P1','P2'],'supports':['K1','K2']} for step in STEPS],validation_refs=[f'LG_project_docs/requirements/{TASK}/verification/results.json'],source_refs=[REF])
    for ordinal, item in enumerate(req, 1):
        item['id'] = f'R-{ordinal:02}'
    for name, value in [('decisions',decisions),('authority',authority),('requirements',req),('analysis',analysis)]:
        save(INPUT/f'{name}.json',value)
    args=[sys.executable,str(SKILL/'scripts/init_task.py'),'--project-root',str(ROOT),'--project-id','complaint-insights','--work-item-id','MCP-REPAIR','--task-id',TASK,'--ordinal','6','--objective','修复已授权MCP审查发现并验证当前交付','--request-snapshot',REQUEST,'--request-language','zh','--development-type','DT-02','--delivery-scenario','DS-01','--risk-level','High','--baseline-inheritance','Revise','--basis',REF,'--authority-reference',REF,'--tailoring-stage','S4','--depends-on',PARENT,'--out-of-scope','多管理员、生产读取采集、日报3030、API3036重启、AICS、原任务结果改写','--forbidden-action','生产连接、开启采集、操作3030或改写人工门禁','--rollback','仅回退本轮desk/mcp代码；不得恢复已撤销token或操作3030']
    paths=['insights/token_desk.py','insights/mcp_tokens.py','insights/mcp_server.py','requirements.txt','tests/test_token_desk.py','tests/test_mcp.py','scripts/mcp_portal_verify.py','scripts/mcp_portal_materials.py',f'LG_project_docs/requirements/{TASK}/**',f'LG_project_docs/requirements/{PARENT}/release/**','LG_project_docs/README.md',f'.project-governance/tasks/{TASK}/**','.project-governance/intake/mcp-portal/review-repair/**','.runtime/mcp-portal*/**','.runtime/processes.json','.secrets/mcp-server.json','.secrets/mcp-token-registry.json','.secrets/mcp-handoff.zip']
    for path in paths: args += ['--allowed-path',path]
    for surface in ['Identity/Security/Privacy','API/Integration','UI/UX','Deploy/Operations']: args += ['--change-surface',surface]
    for value in SCOPE: args += ['--in-scope',value]
    for value in ACCEPTANCE: args += ['--acceptance',value,'--verification-plan',value]
    for value in STEPS: args += ['--plan-step',value]
    for name,flag in [('decisions','--decisions-json-file'),('authority','--authority-assessments-json-file'),('requirements','--requirement-items-json-file'),('analysis','--first-principles-json-file')]: args += [flag,str(INPUT/f'{name}.json')]
    args += ['--clarification-skipped','--clarification-notice','本轮返修沿用你已确认的范围和授权，跳过重复提问。','--clarification-basis','独立反例给出单义期望，同范围返修已由开始审查明确授权，无新增权限未知','--survey-ref',REF]
    for key,value in parent['task_profile']['applicability_facts'].items(): args += ['--applicability-fact',f'{key}={value}']
    for key in ['E01','E02','E03','E05']: args += ['--extension-trigger',f'{key}=Active','--extension-evidence-ref',f'{key}={REF}']
    args += ['--extension-trigger','E04=Inactive','--required-gate','independent-review','--required-gate','security-privacy-review']
    for value in ['read','edit-in-scope','validate','external-effect','rollback']: args += ['--execution-permission',value]
    raise SystemExit(subprocess.run(args).returncode)

if __name__=='__main__': main()
