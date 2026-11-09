"""Prepare the second repair under the original explicit review authorization."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(r'D:\LFEN_project\dev_project\complaint-insights')
SKILL=Path(r'C:\Users\Administrator\.codex\skills\run-governed-product-workflow')
PARENT='T-INSIGHTS-MCP-PORTAL-20261030-01'
PREVIOUS='T-INSIGHTS-MCP-REPAIR-20261030-01'
TASK='T-INSIGHTS-MCP-REPAIR-20261030-02'
INPUT=Path(__file__).parent
REL=f'LG_project_docs/requirements/{TASK}'
DOCS=ROOT/REL
REF=REL+'/discovery/survey.md'
SCOPE=['修复第二轮确认的原始字符串、客户端凭据创建与非法信封协议边界，回归两轮全部七项问题', '同步真实Schema、公开指南和无凭据包，只部署desk/mcp并验证全部原始MCP需求', '保存新交付版本，沿用用户多轮审查授权与正式人类门禁Pending，不改旧结果']
ACCEPTANCE=['合法JSON字符串原样保留，尤其null不能变为None，日期等合法转换和严格Schema负向边界均保持', '客户端空文件创建后先限制ACL再写凭据；权限/写入失败清理本次新建文件，原有配置不覆盖', '非法JSON-RPC信封-32600、解析错误-32700、未知方法-32601、未知工具/协议参数-32602、业务参数isError分层正确，不回显原始非法信封', '全部工程测试及真实HTTPS11工具14表、完整分页、发放撤销和公共材料检查通过；3030/3036/15433不操作且生产采集关闭', '同一版本的后续完整独立审查和真实证据如实留存；异机、人工门禁与机器登记限制保留']
STEPS=['根据第二轮独立证据保存范围、最小修复设计和原文授权', '禁用SDK参数预解析，先保护客户端配置再写入，规范化传输信封错误并回归所有发现', '仅部署desk/mcp并构建真实Schema材料，完整测试与内网真实链路复验', '保存交付与原话逐条证据，完成后续独立完整审查并按实际结果收口']

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=json.loads((ROOT/f'.project-governance/tasks/{PREVIOUS}/before.json').read_text(encoding='utf-8'))
    for name in ['discovery','design','verification','release']:
        (DOCS/name).mkdir(parents=True,exist_ok=True)
    (DOCS/'discovery/survey.md').write_text(f'''# 第二次MCP审查返修

完整原文、澄清与“开始审查”答复继承只读父任务 {PARENT}/before.json 和前次返修 {PREVIOUS}/before.json；不改写它们。用户同意原问题中的“发现问题将修复并复验，直至同一版本连续两轮完整审查无问题”，持续授权本次同范围返修，不是新门禁批准。

第二轮独立观察原件在 C:/Users/Administrator/Documents/Codex/2026-10-30/complaint-insights-mcp/work/round2：fixture-results.json（原始字符串null被清空）、client-results.json（先写凭据后ACL及失败残留，合成Users可读父目录）、protocol-edges.json（非法信封错误码）。第一返修45文件版本继续保持直到独立报告末次校验完成。本记录捕获于 {now}。

已核实依赖：MCP2.3公开构造参数tools、Tool.from_function和FuncMetadata允许构造工具元数据；禁用二次JSON字符串预解析仍保留Pydantic日期与SDK执行/输出处理。SDK transport在信封模型验证失败时HTTP400/-32602；只规范化该错误输出为-32600与简短信息，保留正常请求/通知/业务错误。Windows configure在空新文件设置受限ACL后才允许写入；失败仅清理本次O_EXCL创建的文件。

授权和环境边界均不变：唯一owner、接收人Bearer、10.8内网HTTPS、本地15433历史副本、生产读取false/watch停止；不操作3030/3036/数据库、AICS、日报、附件及source.py/syncer.py。另一电脑路由/CA与正式人类门禁仍未确认。父Deferred导致官方Offer登记拒绝；不得伪造Implemented、ManagedByParent或机器Passed。

本轮仍沿用已告知的跳过重复提问决定，范围内技术修复没有新增权限或验收未知。
''',encoding='utf-8')
    req=json.loads(json.dumps(previous['requirement_items'],ensure_ascii=False))
    for item in req:
        item['state']='Open'; item.pop('review',None); item['evidence_refs']=[REF]
    decisions=previous['decisions']
    authority=[{'reference':REF,'source_kind':'UserDirective','status':'Valid','scope_refs':SCOPE,'evidence_refs':[REF,f'LG_project_docs/requirements/{PREVIOUS}/discovery/survey.md'],'verified_at':now,'expires_at':None}]
    analysis=json.loads((ROOT/'.project-governance/intake/mcp-portal/review-repair/analysis.json').read_text(encoding='utf-8'))
    analysis.update(outcome=ACCEPTANCE[0],facts=[{'id':'F1','statement':'第二轮独立确认合法字符串重解释、凭据ACL时序及失败残留、非法信封错误码三项反例','evidence_refs':[REF]},{'id':'F2','statement':'MCP2.3公开tools构造与元数据接口以及Windows空文件ACL保护机制已核实','evidence_refs':[REF]}],
        constraints=[{'id':'C1','statement':'原权限、保护路径、生产关闭与待人工门禁保持；仅同范围返修','source_refs':[REF]}],
        fundamentals=[{'id':'P1','statement':'类型合格输入的值不能被隐式重解释；秘密首字节写出前访问控制必须成立','derived_from':['F1','C1']},{'id':'P2','statement':'协议错误与执行错误层次必须一致，正常SDK流程保持','derived_from':['F2','C1']}],
        causal_links=[{'from_ref':'P1','to_ref':'O1','rationale':'自定义工具元数据保留解码值；空文件先限权且失败清理','evidence_refs':[REF]},{'from_ref':'P2','to_ref':'O1','rationale':'只规范化SDK2.3特定传输信封错误，不重写MCP路由','evidence_refs':[REF]}],
        alternatives=[{'id':'O1','description':'扩展已核实SDK工具元数据、修复配置原子创建和特定传输错误','status':'Selected','derived_from':['P1','P2'],'tradeoffs':['依赖锁定MCP2.3，升级须回归']},{'id':'O0','description':'保持当前版本','status':'Rejected','derived_from':['P1','P2'],'tradeoffs':['三项真实问题保留']},{'id':'O2','description':'替换完整协议与客户端实现','status':'Rejected','derived_from':['P1','P2'],'tradeoffs':['扩大改动并损失现有验证的兼容性']}],
        decision_criteria=[{'id':'K1','statement':'三个新反例和首轮四项均通过且合法路径不回归','source_refs':[REF]},{'id':'K2','statement':'没有秘密泄漏、范围扩大或虚构批准','source_refs':[REF]}],
        derivation=[{'plan_step':step,'derived_from':['P1','P2'],'supports':['K1','K2']} for step in STEPS],validation_refs=[REL+'/verification/results.json'],source_refs=[REF])
    for name,value in [('decisions',decisions),('authority',authority),('requirements',req),('analysis',analysis)]: save(INPUT/f'{name}.json',value)
    args=[sys.executable,str(SKILL/'scripts/init_task.py'),'--project-root',str(ROOT),'--project-id','complaint-insights','--work-item-id','MCP-REPAIR-2','--task-id',TASK,'--ordinal','7','--objective','修复第二轮MCP完整审查发现并保持原权限与协议边界','--request-snapshot',previous['request_snapshot']['text'],'--request-language','zh','--development-type','DT-02','--delivery-scenario','DS-01','--risk-level','High','--baseline-inheritance','Revise','--basis',REF,'--authority-reference',REF,'--tailoring-stage','S4','--depends-on',PARENT,'--depends-on',PREVIOUS,'--out-of-scope','生产、采集、日报、数据库、AICS、多管理员和原任务改写','--forbidden-action','连接源生产、启动watch、操作3030/3036/15433、读取私钥或扩大权限','--rollback','只回退本轮desk/mcp代码和公开材料，不恢复已撤销令牌；客户端失败仅删除本次新建文件']
    for path in ['insights/mcp_server.py','insights/mcp_http.py','scripts/mcp_client.py','scripts/mcp_portal_verify.py','scripts/mcp_portal_materials.py','tests/test_mcp.py','tests/test_token_desk.py',REL+'/**',f'LG_project_docs/requirements/{PARENT}/release/**','LG_project_docs/README.md',f'.project-governance/tasks/{TASK}/**','.project-governance/intake/mcp-portal/review-repair/pass2/**','.runtime/mcp-portal*/**','.runtime/processes.json','.secrets/mcp-server.json','.secrets/mcp-token-registry.json','.secrets/mcp-handoff.zip']: args+=['--allowed-path',path]
    for surface in ['API/Integration','Identity/Security/Privacy','UI/UX','Deploy/Operations']: args+=['--change-surface',surface]
    for value in SCOPE: args+=['--in-scope',value]
    for value in ACCEPTANCE: args+=['--acceptance',value,'--verification-plan',value]
    for value in STEPS: args+=['--plan-step',value]
    for name,flag in [('decisions','--decisions-json-file'),('authority','--authority-assessments-json-file'),('requirements','--requirement-items-json-file'),('analysis','--first-principles-json-file')]: args += [flag,str(INPUT/f'{name}.json')]
    args+=['--clarification-skipped','--clarification-notice','本轮返修沿用你已确认的范围和授权，跳过重复提问。','--clarification-basis','用户持续多轮审查授权包含同范围返修，反例期望单义，无新增权限未知','--survey-ref',REF]
    for key,value in previous['task_profile']['applicability_facts'].items(): args+=['--applicability-fact',f'{key}={value}']
    for key in ['E01','E02','E03','E05']: args+=['--extension-trigger',f'{key}=Active','--extension-evidence-ref',f'{key}={REF}']
    args+=['--extension-trigger','E04=Inactive','--required-gate','independent-review','--required-gate','security-privacy-review']
    for value in ['read','edit-in-scope','validate','external-effect','rollback']: args+=['--execution-permission',value]
    raise SystemExit(subprocess.run(args).returncode)

if __name__=='__main__': main()
