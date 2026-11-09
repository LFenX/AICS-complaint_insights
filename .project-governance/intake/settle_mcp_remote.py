import json
from pathlib import Path
from datetime import datetime, timezone

root = Path(__file__).resolve().parents[2]
task = root / '.project-governance/tasks/T-INSIGHTS-FOUNDATION-20261029-01'
before = json.loads((task/'before.json').read_text(encoding='utf-8'))
ref = 'LG_project_docs/requirements/T-INSIGHTS-FOUNDATION-20261029-01/discovery/mcp-steering.md'
clarification = dict(before['clarification'])
clarification.update(state='Settled', mode='Asked', notice='需确认调用位置，因为远程 MCP 需要增加监听地址和认证配置。',
    survey_refs=before['clarification']['survey_refs']+[ref],
    rounds=[{'ordinal':1,'asked_at':datetime.now(timezone.utc).isoformat(),'exchanges':[{
        'question':'MCP 工具需要在哪里调用？这决定连接配置和服务监听方式。',
        'changes':'Scope','recommended_default':'先供这台采集电脑上的 Agent 使用，交接本地 stdio 配置',
        'answer':'需要其他内网电脑的 Agent 直接远程调用','answer_state':'Answered',
    }]}],
    basis='用户已真实回答远程内网调用；asked_at 为此次补录的采集时间，不冒充原始消息时间。MCP 范围已明确，安全隐私 Gate 未获通过，仍独立待审。')
acceptance = list(before['acceptance']['criteria'])
acceptance[-1] = '真实 HTTPS Streamable HTTP MCP 客户端可发现并按需调用只读工具，覆盖分类、汇总、全文和十四类原始业务副本；独立令牌、可信证书、内网限制、参数、分页与权限测试通过，内网客户端配置与中文交接说明齐备'
analysis = dict(before['first_principles_analysis'])
analysis['constraints'] = analysis['constraints']+[{'id':'C3','statement':'用户指定其他内网电脑远程调用 MCP；监听前必须配置 TLS、独立只读令牌与内网网段限制','source_refs':[ref]}]
plan = dict(before['plan'])
plan['steps'][-1] = '以 HTTPS MCP 复用只读 API，配置内网访问、独立令牌和证书，补齐源数据查询及交接说明并运行真实协议验证'
plan['verification'] = acceptance
analysis['derivation'][-1]['plan_step'] = plan['steps'][-1]
changes=[{'path':k,'value':v} for k,v in {'acceptance.criteria':acceptance,'first_principles_analysis':analysis,'plan':plan,'clarification':clarification}.items()]
(root/'.project-governance/intake/mcp-remote-amendment.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
