"""Capture the MCP portal directive and its explicit continuation, without secrets."""
from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
SKILL = Path(r'C:\Users\Administrator\.codex\skills\run-governed-product-workflow')
TASK = 'T-INSIGHTS-MCP-PORTAL-20261030-01'
DOCS = ROOT / 'LG_project_docs/requirements' / TASK
REF = f'LG_project_docs/requirements/{TASK}/discovery/survey.md'
REQUEST = '''另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

开一个新会话处理MCP相关事宜，本会话继续完成客诉日报看板

继续'''
PRIOR = '另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，'
PRESENTED = '已核实：MCP 监听 10.8.61.200:3037，令牌页仍只监听 127.0.0.1:3029。旧页面没有登录机制，不能直接开放到内网。我会将普通访客的说明下载入口与管理员的发放权限分开，保留每位接收人独立令牌。'
SCOPE = ['HTTPS 内网接入门户及单一发放管理员登录、会话、CSRF、审计、发放撤销',
         '原生 MCP 协议说明、全部11工具实际 schema、无令牌客户端包及明确选源',
         '本工程3029/3037部署、权限及真实协议验证；保留生产隔离和撤销失效关闭']
ACCEPTANCE = ['内网访客可阅读全部说明和下载不含秘密的材料；无管理员会话不能发放、撤销或列出身份',
              '单一管理员经独立凭据登录，安全会话和同源CSRF有效；逐人发放、即时撤销、并发写入及失效关闭通过验证',
              '协议、TLS/CA、Bearer、全部11工具参数/枚举/分页/错误/计数/来源及可运行客户端均覆盖，schema与真实tools/list一致',
              '3029内网HTTPS及3037 MCP实测通过，仅使用127.0.0.1:15433副本，生产读取关闭，3030未被本任务管理',
              '逐条原话核对并保存实际证据、运行和回滚交接，用户验收Pending；异机路由未实测时明确列出']
STEPS = ['先保存权限、模块、动作风险、审计、禁用原因与契约的PRD和技术设计',
         '实现隔离的管理员认证和安全发放，修复令牌文件与并发、撤销边界',
         '按实际schema构建可读协议工具文档、选源示例和无凭据客户端包',
         '运行权限与契约测试、部署本项目3029/3037并严格TLS验证11工具及材料',
         '按原话逐条保存验证、交接和工程结果，记录Pending与未验项']


def main():
    now = datetime.now(timezone.utc).isoformat()
    for name in ['discovery','prd','design','release','verification','ui-previews']:
        (DOCS/name).mkdir(parents=True,exist_ok=True)
    survey = f'''# MCP门户勘察与授权记录

## 原话

{REQUEST}

既有权限原话（来源：T-INSIGHTS-DAILY-20261030-01/before.json request_snapshot）：{PRIOR}

## 已核实事实

- 2026-10-30：本工程Python服务，内网接口10.8.61.200/23；3029只监听回环，3037只监听10.8.61.200；3036与15433仅回环。
- 经专用CA严格验证的真实initialize协商2025-11-25，tools/list返回11工具；schema存于.runtime/mcp-portal-survey/tools-list.json。
- MCP、agent与客户端的默认来源均为production-ai-customer，production.json allow_production_read=false；不连接源生产。
- token_desk旧实现依赖回环信任、无登录、静态CSRF，无跨进程锁；旧交接包带接收人token且部分例子为development-local。
- current_tokens已修复配置丢失/损坏恢复启动令牌的问题；必须保留fail-closed行为。
- 主会话3030及日报/采集文件明确排除，进程归属已核对。本任务不管理其它进程。

## 澄清与继续

实际询问：令牌发放保留哪种管理员范围？普通内网访客均只能阅读文档、下载无凭据客户端；只有登录管理员才能生成或撤销 MCP 令牌。

选项：仅我持有独立管理员凭据并发放（推荐）；指定多名管理员，各自登录发放。

用户原话回复：继续。

解释边界：继续不是指定额外管理员。沿用此前明确“需要我下发的token”的单一所有者范围；不建立额外管理员，不开放匿名签发。身份权限不扩大。可选的多管理员扩展未被选择，不属于本任务。

## 本任务授权与边界

用户原话授权优化、复核并内网开放令牌服务及说明入口；本会话“继续”延续该范围。可在3029严格HTTPS公开说明，管理员独立认证后发放/撤销；只重启本项目desk与mcp。禁止生产读取、采集、3030和AICS修改。所有秘密留在.secrets，不进入公开页面、日志和下载包。

## 原始证据位置

来源会话01a1866c-6ec4-7f83-9aa8-f75c67aebcf8的新会话转交指令，及当前聊天实际“继续”；本文件记录收件时间{now}，不冒称原始授权发生时间。
'''
    (DOCS/'discovery/survey.md').write_text(survey,encoding='utf-8')
    (DOCS/'README.md').write_text('# MCP内网接入门户\n\n本需求包含 discovery 勘察授权、prd 权限与契约、design 技术设计、release 接收人指南与运维交接、verification 真实证据、ui-previews 页面核查。\n',encoding='utf-8')
    (DOCS/'prd/portal.md').write_text('''# MCP内网接入门户 PRD

目标：接收人获得一个内网HTTPS链接，能独立完成了解工具、安装可信CA、配置本人令牌、选择来源和验证查询。

|角色|可执行|禁止/禁用原因|
|---|---|---|
|内网访客|说明、schema、CA公钥、无凭据客户端与示例下载|无管理员会话，不能列身份、发放、撤销；无MCP Bearer不能查询客诉|
|MCP接收人|本人Bearer调用11个只读工具，读取已发布本地来源|MCP Bearer不是管理员凭据；没有写入、任意SQL、采集或生产控制工具|
|唯一所有者管理员|独立登录，列身份元数据、逐人发放和撤销、退出|凭据未配置/失效则管理禁用；同源CSRF或安全会话失败即拒绝；不提供查看旧token|

模块：接入首页、快速开始、原生协议、工具选择、11工具逐参数参考、数据口径、下载、排错、管理员登录及令牌管理。页面适配桌面和窄屏，有键盘焦点、明确标签、错误提示及空态。

动作：docs.read/download.read为LOW只读；admin.login/logout为HIGH认证动作；token.issue/revoke为HIGH GLOBAL，权限insights.tokens.manage -> insights.admin -> insights。

审计：记录request_id、实际TCP来源、管理员标签、动作、目标身份、状态、时长；不记录口令、cookie、csrf、Bearer、表单、查询参数或客户内容。管理响应no-store；所有页面防嵌入、同源CSP、no-referrer、nosniff。登录失败限速，session空闲20分钟/最长8小时，重启或管理员凭据变更失效。

验收契约：访客公开读取成功但管理拒绝；MCP身份不能成为管理员；无/错/跨会话CSRF和跨Origin被拒绝；HTTPS+Host+真实网段验证，代理头不能绕过；单人唯一token、并发无丢写、损坏配置不恢复/覆盖、撤销立即失效且允许撤销最后一枚。下载固定白名单，材料不含任何现存凭据或私钥；源码schema与实际远端发现一致。

数据边界：production-ai-customer为已停采的历史本地副本；显式source_id并查get_sync_status，不承诺实时生产。所有有效MCP令牌有相同只读工具和来源范围，独立身份仅用于分发、审计和撤销，不宣称字段/来源级隔离。
''',encoding='utf-8')
    inputs=Path(__file__).parent
    decisions=[{'id':'D-MCP-PORTAL-CONTINUE','kind':'Proceed','presented':PRESENTED,'response':'继续',
                'decided_by':'当前聊天用户','decided_at':now,'evidence_ref':REF,'outcome':'Approved'}]
    auth=[{'reference':REF,'source_kind':'UserDirective','status':'Valid','scope_refs':SCOPE,'evidence_refs':[REF],
           'verified_at':now,'expires_at':None}]
    clarification={'state':'Settled','mode':'Asked','notice':'针对权限这一处未明确项，需要先确认发放管理员范围；协议文档和只读门户可以继续实现。',
        'survey_refs':[REF],'rounds':[{'ordinal':1,'asked_at':now,'exchanges':[{'question':'令牌发放保留哪种管理员范围？普通内网访客均只能阅读文档、下载无凭据客户端；只有登录管理员才能生成或撤销 MCP 令牌。',
        'changes':'Authority','recommended_default':'仅我持有独立管理员凭据并发放','answer':'继续','answer_state':'Answered'}]}],
        'basis':'继续沿用原已明确由本人下发的所有者范围，不解释为新增管理员或匿名签发；依据原话及继续指令，具体见survey解释边界。','reopened_by':[]}
    quote=REQUEST.split('\n\n')[0]
    readings=['提供可交付其他人的详细MCP介绍','按MCP原生协议实现说明与可运行程序','优化并复核令牌发放服务','内网开放令牌服务入口','将MCP使用协议、介绍和接入方法放在同一服务','一个内网链接供接收人阅读、下载与接入']
    req=[{'id':f'R-{i+1:02}','source':'request_snapshot','quote':quote,'reading':reading,'state':'Open','evidence_refs':[REF],'acceptance_refs':list(range(5))} for i,reading in enumerate(readings)]
    req.append({'id':'R-07','source':'request_snapshot','quote':REQUEST.split('\n\n')[1],'reading':'本会话仅处理MCP，保留3030和主会话日报工作','state':'Open','evidence_refs':[REF],'acceptance_refs':[3,4]})
    req.append({'id':'R-08','source':'request_snapshot','quote':'继续','reading':'继续已授权的MCP范围；不增加发放管理员','state':'Open','evidence_refs':[REF],'acceptance_refs':[0,1,4]})
    req.append({'id':'R-09','source':'clarification:r1.e1','quote':'继续','reading':'延续既有所有者发放规则，不创建额外管理员','state':'Open','evidence_refs':[REF],'acceptance_refs':[0,1,4]})
    analysis={'method_version':'first-principles-v1','depth':'Deep','outcome':ACCEPTANCE[0],
       'facts':[{'id':'F1','statement':'旧3029无登录，MCP严格HTTPS有11个只读工具','evidence_refs':[REF]}, {'id':'F2','statement':'生产采集关闭，已发布本地副本可查询','evidence_refs':[REF]}],
       'constraints':[{'id':'C1','statement':'保持所有者发放，访客不得匿名签发；秘密不出.secrets','source_refs':[REF]}, {'id':'C2','statement':'不连接生产、不采集、不管理3030、其它项目或历史任务','source_refs':[REF]}],
       'assumptions':[{'id':'A1','statement':'当前CA证书覆盖内网IP，可复用3029TLS','validation':'校验证书SAN、有效期并严格CA验证真实HTTPS'}],
       'unknowns':[{'id':'U1','statement':'接收人另一台电脑路由与CA导入未实测','owner':'接收人','resolution_condition':'接收人按下载包执行验证','blocking':False}],
       'fundamentals':[{'id':'P1','statement':'可达性和发放权限分离','derived_from':['F1','C1']},{'id':'P2','statement':'协议、客户端与来源契约一致','derived_from':['F1','F2','C2']}],
       'causal_links':[{'from_ref':'P1','to_ref':'O1','rationale':'公共说明与独立管理员会话支持分享而不放开签发','evidence_refs':[REF]},{'from_ref':'P2','to_ref':'O1','rationale':'由真实schema生成参数参考、固定来源例子并通过原生请求验证','evidence_refs':[REF]}],
       'alternatives':[{'id':'O1','description':'现有3029升级为HTTPS说明门户与唯一管理员登录','status':'Selected','derived_from':['P1','P2'],'tradeoffs':['需要独立管理员凭据和CA初始化']},{'id':'O0','description':'保留localhost令牌页','status':'Rejected','derived_from':['P1'],'tradeoffs':['无法分享一个内网接入说明入口']},{'id':'O2','description':'新增统一身份SSO/OAuth授权服务器','status':'Rejected','derived_from':['P1'],'tradeoffs':['组织身份平台和OAuth注册均未授权，不是现有Bearer接入的必要依赖']}],
       'decision_criteria':[{'id':'K1','statement':'分享入口并保持所有者发放边界','source_refs':[REF]},{'id':'K2','statement':'严格TLS、真实schema和正确选源；本地副本隔离','source_refs':[REF]}],
       'selected_approach':'O1','derivation':[{'plan_step':step,'derived_from':['P1','P2'],'supports':['K1','K2']} for step in STEPS],
       'validation_refs':[f'LG_project_docs/requirements/{TASK}/verification/results.json'],'source_refs':[REF]}
    for name,data in {'decisions':decisions,'authority':auth,'requirements':req,'clarification':clarification,'analysis':analysis}.items():
        (inputs/f'{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    args=[sys.executable,str(SKILL/'scripts/init_task.py'),'--project-root',str(ROOT),'--project-id','complaint-insights',
          '--work-item-id','MCP-PORTAL','--task-id',TASK,'--ordinal','5','--objective','交付可分享的内网MCP说明与安全令牌发放入口',
          '--request-snapshot',REQUEST,'--request-language','zh','--development-type','DT-04','--delivery-scenario','DS-01',
          '--risk-level','High','--baseline-inheritance','Revise','--basis',REF,'--authority-reference',REF,'--tailoring-stage','S4',
          '--out-of-scope','多管理员扩展、SSO/OAuth、生产接入、采集、日报3030与AICS代码数据库',
          '--forbidden-action','连接10.8.45.155或开启生产读取、采集，重启3030或修改日报/源同步文件及旧任务',
          '--rollback','仅停止本工程desk/mcp并恢复本次代码备份与防火墙规则；不恢复已撤销token，不动生产和3030']
    for path in ['insights/token_desk.py','insights/mcp_http.py','insights/mcp_server.py','insights/mcp_tokens.py','insights/capabilities.py','scripts/mcp*','scripts/build_mcp_handoff.py','scripts/token_desk_admin.py','config/mcp*','assets/token-desk*','tests/test_mcp*','tests/test_token_desk.py',f'LG_project_docs/requirements/{TASK}/**','LG_project_docs/README.md','README.md',f'.project-governance/tasks/{TASK}/**','.project-governance/intake/mcp-portal/**','.runtime/mcp-portal*/**','.runtime/processes.json','.secrets/token-desk*','.secrets/mcp-server.json','.secrets/mcp-token-registry.json','.secrets/mcp-handoff.zip']:
        args+=['--allowed-path',path]
    for surf in ['API/Integration','Identity/Security/Privacy','UI/UX','Deploy/Operations']: args+=['--change-surface',surf]
    for s in SCOPE: args+=['--in-scope',s]
    for a in ACCEPTANCE: args+=['--acceptance',a,'--verification-plan',a]
    for s in STEPS: args+=['--plan-step',s]
    for name,flag in [('decisions','--decisions-json-file'),('authority','--authority-assessments-json-file'),('requirements','--requirement-items-json-file'),('clarification','--clarification-json-file'),('analysis','--first-principles-json-file')]: args+=[flag,str(inputs/f'{name}.json')]
    facts={'product_intent_change':'No','initiative_scope_change':'Yes','requirement_change':'Yes','external_behavior_change':'Yes','design_change':'Yes','architecture_impact':'No','security_privacy_impact':'Yes','data_ai_impact':'No','formal_knowledge_records':'No','operations_impact':'Yes','production_release':'No','irreversible_change':'No','actual_execution':'Yes','authority_available':'Yes','migration_retirement':'No','external_system_effect':'Yes','formal_review_or_gate':'No'}
    for k,v in facts.items(): args+=['--applicability-fact',f'{k}={v}']
    for key in ['E01','E03','E05']: args+=['--extension-trigger',f'{key}=Active','--extension-evidence-ref',f'{key}={REF}']
    for key in ['E02','E04']: args+=['--extension-trigger',f'{key}=Inactive']
    args+=['--execution-permission','read','--execution-permission','edit-in-scope','--execution-permission','validate','--execution-permission','external-effect','--execution-permission','rollback']
    raise SystemExit(subprocess.run(args).returncode)


if __name__=='__main__': main()
