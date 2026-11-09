"""Prepare the authorized follow-on repair after the completed second review."""
from pathlib import Path
from datetime import datetime, timezone
import copy
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SKILL = Path(r'C:\Users\Administrator\.codex\skills\run-governed-product-workflow')
PARENT = 'T-INSIGHTS-REVIEW-20261029-01'
TASK = 'T-INSIGHTS-REPAIR-20261029-02'
before = json.loads((ROOT/f'.project-governance/tasks/{PARENT}/before.json').read_text(encoding='utf-8'))
REF = f'LG_project_docs/requirements/{TASK}/discovery/survey.md'
inputs = ROOT/'.project-governance/intake/repair-round2'
inputs.mkdir(exist_ok=True)
now = datetime.now(timezone.utc).isoformat()
steps = ['拒绝缺省主机、端口或数据库名的连接串', '验证显式连接参数不受环境缺省值影响并回归全部查询', '保存返修结果并归属已授权的父审查会话']
analysis = copy.deepcopy(before['first_principles_analysis'])
for fact in analysis['facts']:
 if fact['id'] == 'F5':
  fact['evidence_refs'] = [f'.project-governance/tasks/{PARENT}/evidence/round-1.md',f'.project-governance/tasks/{PARENT}/evidence/root-round1-probes.json']
analysis['facts'].append({'id':'F6','statement':'第二轮离线参数解析和隔离连接复现：省略host/port时PGHOST/PGPORT改变实际目的地，但原校验报告localhost:5432','evidence_refs':[f'.project-governance/tasks/{PARENT}/evidence/round-2.md']})
analysis['fundamentals'].append({'id':'P7','statement':'主机、端口、数据库均须显式，校验和身份绑定不能代入与libpq实际缺省不同的值','derived_from':['F6','C1']})
analysis['outcome'] = '连接前拒绝依赖隐式目的地的配置，显式配置继续使用相同来源和现有只读查询'
analysis['alternatives'] = [
 {'id':'O1','description':'强制host/port/dbname显式，保留既有hostaddr/service拒绝','status':'Selected','derived_from':['P7'],'tradeoffs':['不再接受省略目的地的配置；现有交付配置已显式，无须修改']},
 {'id':'O0','description':'保持现状','status':'Rejected','derived_from':['P7'],'tradeoffs':['继续允许环境默认值改变真实源而不改变身份摘要']},
 {'id':'O2','description':'解析并固化所有libpq环境与service缺省','status':'Rejected','derived_from':['P7'],'tradeoffs':['需追踪可变全局环境和外部service文件，增加隐藏依赖；本期无需隐式配置']},
]
analysis['selected_approach'] = 'O1'
analysis['derivation'] = [{'plan_step':s,'derived_from':['P6','P7'],'supports':['K1','K2']} for s in steps]
analysis['source_refs'].append(REF)
analysis['causal_links'] = [{'from_ref':'P7','to_ref':'O1','rationale':'显式三元目的地与libpq显式参数优先规则一致，环境默认不再介入地址身份','evidence_refs':[f'.project-governance/tasks/{PARENT}/evidence/round-2.md']}]
clarification = copy.deepcopy(before['clarification'])
clarification['survey_refs'] = [REF]
clarification['basis'] = '已核对第二轮反例与原始多轮修复授权；修复只收紧隐式目的地，不新增监听、权限、读取范围或生产操作，无新授权未知；保留原真实问答，不补造提问。'
scope = before['scope']['in_scope']
authority = [{'reference':REF,'source_kind':'UserDirective','status':'Valid','scope_refs':scope,'evidence_refs':[REF],'verified_at':now,'expires_at':None}]
decisions = copy.deepcopy(before['decisions'])
artifacts = copy.deepcopy(before['artifact_manifest'][:3])
for a in artifacts:
 a['asset_id'] = a['asset_id'].replace(PARENT,TASK)
 a['content_ref'] = a['content_ref'].replace(PARENT,TASK)
values = {'analysis':analysis,'clarification':clarification,'authority':authority,'decisions':decisions,'requirements':before['requirement_items'],'artifacts':artifacts}
for name,value in values.items():
 (inputs/f'{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
args = [sys.executable,str(SKILL/'scripts/init_task.py'),'--project-root',str(ROOT),'--project-id','complaint-insights','--work-item-id','LOCAL-ANALYTICS-FOUNDATION','--task-id',TASK,'--ordinal','3',
 '--objective','修复第二轮审查确认的libpq隐式主机端口及数据库目的地校验缺陷','--request-snapshot',before['request_snapshot']['text'],
 '--development-type','DT-06','--delivery-scenario','DS-03','--risk-level','Medium','--baseline-inheritance','Revise','--depends-on',PARENT,
 '--change-surface','API/Integration','--change-surface','Agent/Collaboration','--basis',REF,'--authority-reference',REF,'--tailoring-stage','S4',
 '--out-of-scope','生产接入与重启、数据库结构或数据变更、权限/认证/监听变更、扩大读取范围',
 '--forbidden-action','写开发源库、连接或重启生产、改变项目结构或命名、修改父任务封存账本',
 '--rollback','保留config和规则测试的修复前字节；仅回退本次代码与说明，数据与权限不变',
 '--clarification-json-file',str(inputs/'clarification.json'),'--decisions-json-file',str(inputs/'decisions.json'),'--authority-assessments-json-file',str(inputs/'authority.json'),
 '--requirement-items-json-file',str(inputs/'requirements.json'),'--first-principles-json-file',str(inputs/'analysis.json'),'--artifact-manifest-json-file',str(inputs/'artifacts.json')]
for path in ['insights/config.py','tests/test_rules.py','LG_project_docs/**','update_log/**','.project-governance/**']:
 args += ['--allowed-path',path]
for value in scope: args += ['--in-scope',value]
for value in before['acceptance']['criteria']: args += ['--acceptance',value,'--verification-plan',value]
for value in steps: args += ['--plan-step',value]
facts = dict(before['task_profile']['applicability_facts'])
facts.update(external_behavior_change='Yes',security_privacy_impact='No',data_ai_impact='No',production_release='No',irreversible_change='No',external_system_effect='No')
for key,value in facts.items(): args += ['--applicability-fact',f'{key}={value}']
for key in ['E01','E02','E03','E05']: args += ['--extension-trigger',f'{key}=Active','--extension-evidence-ref',f'{key}={REF}']
args += ['--extension-trigger','E04=Inactive']
subprocess.run(args,check=True)
