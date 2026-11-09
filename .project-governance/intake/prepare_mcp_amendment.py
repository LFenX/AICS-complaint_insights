import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
task = root / '.project-governance/tasks/T-INSIGHTS-FOUNDATION-20261029-01'
before = json.loads((task / 'before.json').read_text(encoding='utf-8'))
evidence = 'LG_project_docs/requirements/T-INSIGHTS-FOUNDATION-20261029-01/discovery/mcp-steering.md'
scope = dict(before['scope'])
scope['in_scope'] = before['scope']['in_scope'] + ['MCP 只读查询工具、数据类型说明和交接配置']
authority = dict(before['authority'])
authority['authority_references'] = before['authority']['authority_references'] + [evidence]
authority['authority_assessments'] = before['authority']['authority_assessments'] + [{
    'reference': evidence, 'source_kind': 'UserDirective', 'status': 'Valid',
    'scope_refs': [scope['in_scope'][-1]], 'evidence_refs': [evidence],
    'verified_at': __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
    'expires_at': None,
}]
criteria = before['acceptance']['criteria'] + ['真实 stdio MCP 客户端可发现并按需调用只读工具，覆盖分类、汇总、全文和十四类原始业务副本；参数、分页、错误和权限测试通过，连接配置与中文交接说明齐备']
plan = dict(before['plan'])
plan['steps'] = before['plan']['steps'] + ['以 MCP 复用本地只读 API，补齐源数据查询与交接说明并运行真实协议验证']
plan['verification'] = criteria
analysis = dict(before['first_principles_analysis'])
analysis['outcome'] += '；通过 MCP 按需调用并可交接'
analysis['facts'] = analysis['facts'] + [{'id':'F3','statement':'本地数据库及鉴权 API 已运行；用户要求 MCP 工具和使用交接说明','evidence_refs':[evidence,'LG_project_docs/requirements/T-INSIGHTS-FOUNDATION-20261029-01/verification/results.json']}]
analysis['fundamentals'] = analysis['fundamentals'] + [{'id':'P4','statement':'MCP 与 HTTP 使用同一查询契约，按需分页避免重复业务规则与全量正文加载','derived_from':['F3','C2','P3']}]
analysis['derivation'] = analysis['derivation'] + [{'plan_step':plan['steps'][-1],'derived_from':['P3','P4'],'supports':['K1','K2']}]
analysis['source_refs'] = analysis['source_refs'] + [evidence]
requirements = before['requirement_items'] + [
 {'id':'R-02','source':evidence,'quote':'提供查询不同数据的接口','reading':'按数据类型提供只读查询工具','state':'Open','evidence_refs':[evidence],'acceptance_refs':[5]},
 {'id':'R-03','source':evidence,'quote':'并给出说明，注意接口工具以MCP形式构建，并提供相关说明，后续方便和其他人交接如何使用这些工具，按需调用所需数据','reading':'交付 MCP 工具、配置和中文交接手册，真实客户端验证按需查询','state':'Open','evidence_refs':[evidence],'acceptance_refs':[5]},
]
changes = [{'path':k,'value':v} for k,v in {
 'scope':scope,'authority':authority,'acceptance.criteria':criteria,'plan':plan,
 'first_principles_analysis':analysis,'requirement_items':requirements,
}.items()]
(root/'.project-governance/intake/mcp-amendment.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
