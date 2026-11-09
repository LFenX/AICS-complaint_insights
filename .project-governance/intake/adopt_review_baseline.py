from datetime import datetime,timezone
from pathlib import Path
import copy,hashlib,json,subprocess,sys

ROOT=Path(__file__).resolve().parents[2]
SKILL=Path(r'C:\Users\Administrator\.codex\skills\run-governed-product-workflow')
OLD='T-INSIGHTS-FOUNDATION-20261029-01'
TASK='T-INSIGHTS-REVIEW-20261029-01'
REF=f'LG_project_docs/requirements/{TASK}/discovery/survey.md'
before=json.loads((ROOT/f'.project-governance/tasks/{OLD}/before.json').read_text(encoding='utf-8'))
now=datetime.now(timezone.utc).isoformat()
inputs=ROOT/'.project-governance/intake/review-baseline'
inputs.mkdir(exist_ok=True)
scope=before['scope']['in_scope']
clarification=copy.deepcopy(before['clarification'])
clarification['notice']='这里缺少的是独立的安全门禁决定。'
clarification['survey_refs']=[REF]
clarification['basis']='原功能与实际交付、用户的审查及门禁回答已实查明确；旧记录封存，承接同一份字节交付；时间为采集/登记时刻。'
clarification['reopened_by']=[]
clarification['rounds'] += [
 {'ordinal':2,'asked_at':now,'exchanges':[{'question':'本地数据库与内网 MCP 工程结果已保存，47 项测试和实际 HTTPS 调用通过。是否启动多轮对抗性审查？发现问题会修复并复验，直到同一版本连续两轮完整审查未发现问题。','changes':'Authority','recommended_default':'暂不启动，先使用工具','answer':'启动多轮对抗性审查','answer_state':'Answered'}]},
 {'ordinal':3,'asked_at':now,'exchanges':[{'question':'审查启动授权已收到。当前正式结果因 security-privacy-review 待审而处于 Deferred，流程工具只接受 Implemented 结果进入对抗审查。是否通过当前本地副本与内网只读 MCP 的安全隐私门禁？已验证源只读、HTTPS、独立令牌、内网限制；门禁材料：D:/LFEN_project/dev_project/complaint-insights/LG_project_docs/requirements/T-INSIGHTS-FOUNDATION-20261029-01/verification/mcp-acceptance.md','changes':'Authority','recommended_default':'通过本次安全隐私门禁，继续审查','answer':'通过本次安全隐私门禁，继续审查','answer_state':'Answered'}]},
]
requirements=copy.deepcopy(before['requirement_items'])
requirements += [
 {'id':'R-05','source':'clarification:r2.e1','quote':'启动多轮对抗性审查','reading':'这是后置审查的真实启动授权，审查进度由 adversarial_review 单一字段承载，不伪装成本次基线承接已经完成了两轮审查','state':'NotARequirement','evidence_refs':[REF],'acceptance_refs':[]},
 {'id':'R-06','source':'clarification:r3.e1','quote':'通过本次安全隐私门禁，继续审查','reading':'这是当前同一交付版本的真实 Gate 与持续授权，不是生产授权或最终人工验收；用 Gate 账本和后置审查记录承载','state':'NotARequirement','evidence_refs':[REF],'acceptance_refs':[]},
]
decision=[{'id':'D-REVIEW-PROCEED','kind':'Proceed','presented':'原本地与 MCP 工程已保存并提供 47 项测试、真实 HTTPS 证据和交接材料，因安全门禁待审未获正式工程通过；现确认当前版本门禁并继续已授权审查。','response':'通过本次安全隐私门禁，继续审查','decided_by':'当前聊天用户','decided_at':now,'evidence_ref':REF,'outcome':'Approved'}]
authority=[{'reference':REF,'source_kind':'UserDirective','status':'Valid','scope_refs':scope,'evidence_refs':[REF],'verified_at':now,'expires_at':None}]
steps=['核对原交付字节、原始工程证据和当前运行状态','登记真实通过的当前版本安全门禁，保存工程基线','在正式基线保存后登记已收到的真实审查同意，执行后置多轮审查']
analysis=copy.deepcopy(before['first_principles_analysis'])
analysis['outcome']='在不修改业务和封存历史的前提下，承接已通过安全门禁的同一份本地/MCP 工程交付，作为多轮审查基线'
analysis['facts'].append({'id':'F4','statement':'原交付59个公开文件有SHA256清单，47项普通测试与真实MCP证据已保存；用户已明确通过当前版本安全门禁并启动审查','evidence_refs':[REF,f'LG_project_docs/requirements/{OLD}/verification/delivery-manifest.json']})
analysis['alternatives']=[
 {'id':'O1','description':'用新完整任务承接同一份交付和真实新 Gate，保留封存历史，再登记后置审查','status':'Selected','derived_from':['P1','P3','F4'],'tradeoffs':['增加一份可核对的承接记录，不能改写旧账本']},
 {'id':'O0','description':'维持原 Deferred 记录','status':'Rejected','derived_from':['F4'],'tradeoffs':['真实新决定无法进入封存账本，原审查登记仍不适用']},
 {'id':'O3','description':'改写原封存账本或伪造此前 Gate 已通过','status':'Rejected','derived_from':['C1','F4'],'tradeoffs':['违反追加式事实记录，不可采用']},
]
analysis['derivation']=[{'plan_step':step,'derived_from':['P3','F4'],'supports':['K1','K2']} for step in steps]
analysis['source_refs'].append(REF)
artifacts=copy.deepcopy(before['artifact_manifest'])
for item in artifacts[:3]:
 item['asset_id']=item['asset_id'].replace(OLD,TASK)
 item['content_ref']=item['content_ref'].replace(OLD,TASK)
artifacts[-1]['asset_id']=TASK+'-adopted-source-manifest'
artifacts[-1]['reason']='引用原59个实际交付文件的不可变摘要清单；本次只承接工程，不声明已完成审查'
for name,value in {'clarification':clarification,'requirements':requirements,'decisions':decision,'authority':authority,'analysis':analysis,'artifacts':artifacts}.items():
 (inputs/(name+'.json')).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
args=[sys.executable,str(SKILL/'scripts/init_task.py'),'--project-root',str(ROOT),'--project-id','complaint-insights','--work-item-id','LOCAL-ANALYTICS-FOUNDATION','--task-id',TASK,'--ordinal','2',
 '--objective','承接已通过安全门禁的本地数据库与 MCP 工程，建立已授权多轮审查的正式基线','--request-snapshot',before['request_snapshot']['text'],
 '--development-type','DT-01','--delivery-scenario','DS-01','--risk-level','Medium','--baseline-inheritance','Reference','--depends-on',OLD,'--basis',REF,'--authority-reference',REF,
 '--allowed-path','.project-governance/**','--allowed-path','LG_project_docs/**','--allowed-path','update_log/**','--forbidden-action','改写封存账本、修改业务代码、写开发源或操作生产服务','--out-of-scope','生产联调和重启、UI、自动周报、修改当前交付字节；后置返修另建依赖任务',
 '--tailoring-stage','S4','--required-gate','security-privacy-review','--rollback','本次只增加承接和真实决定记录，无业务或运行配置变更；保留旧结果',
 '--clarification-json-file',str(inputs/'clarification.json'),'--decisions-json-file',str(inputs/'decisions.json'),'--authority-assessments-json-file',str(inputs/'authority.json'),
 '--requirement-items-json-file',str(inputs/'requirements.json'),'--first-principles-json-file',str(inputs/'analysis.json'),'--artifact-manifest-json-file',str(inputs/'artifacts.json')]
for value in scope: args += ['--in-scope',value]
for value in before['acceptance']['criteria']: args += ['--acceptance',value,'--verification-plan',value]
for value in steps: args += ['--plan-step',value]
for value in before['task_profile']['change_surfaces']: args += ['--change-surface',value]
facts=dict(before['task_profile']['applicability_facts'])
facts.update(product_intent_change='No',initiative_scope_change='No',requirement_change='No',external_behavior_change='No',design_change='No',architecture_impact='No',operations_impact='No',external_system_effect='No',formal_review_or_gate='Yes')
for key,value in facts.items(): args += ['--applicability-fact',f'{key}={value}']
for key in ['E01','E02','E03','E05']: args += ['--extension-trigger',f'{key}=Active','--extension-evidence-ref',f'{key}={REF}']
args += ['--extension-trigger','E04=Inactive']
subprocess.run(args,check=True)
print('Baseline task created; no product file or old ledger modified.')
