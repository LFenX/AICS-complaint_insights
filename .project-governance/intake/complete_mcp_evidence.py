import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

root=Path(__file__).resolve().parents[2]
task=root/'.project-governance/tasks/T-INSIGHTS-FOUNDATION-20261029-01'
before=json.loads((task/'before.json').read_text(encoding='utf-8'))
verification='LG_project_docs/requirements/T-INSIGHTS-FOUNDATION-20261029-01/verification/'
files=[]
for name in ['insights','scripts','tests','sql','assets','config','deploy','LG_project_docs']:
    for path in (root/name).rglob('*'):
        if path.is_file() and '__pycache__' not in path.parts and path.name!='delivery-manifest.json':
            files.append(path)
for name in ['.gitignore','README.md','requirements.txt','requirements.lock','dev-dependencies.txt','client-dependencies.txt']:
    files.append(root/name)
manifest={'recorded_at':datetime.now(timezone.utc).isoformat(),'files':{
    path.relative_to(root).as_posix():hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(set(files))}}
(root/(verification+'delivery-manifest.json')).write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

# Preserve all three real instruction messages, keeping the earlier version in the
# official amendment history. No synthetic question or approval is introduced.
initial='你可以先用本地开发数据先推进本地的数据库建立，后续只要生产数据库连接接通，可以快速实现我后续的规划'
second='提供查询不同数据的接口'
third='并给出说明，注意接口工具以MCP形式构建，并提供相关说明，后续方便和其他人交接如何使用这些工具，按需调用所需数据'
snapshot=dict(before['request_snapshot'])
snapshot['text']='\n'.join([initial,second,third])
snapshot['source']='真实用户持续指令；初次采集时间保留，后补原话的采集时间由 Amendment.changed_at 记录；原问答见 discovery/mcp-steering.md'
source_digest=hashlib.sha256(snapshot['text'].encode('utf-8')).hexdigest()
proofs=[verification+'results.json',verification+'mcp-results.json',verification+'mcp-acceptance.md']

def review(digest,actual,conditions=None,cases=None):
    return {'source_sha256':digest,'conditions':conditions or [],'cases':cases or [{
        'condition':None,'branch':'Unconditional','input':'当前已运行的开发副本、真实 HTTPS MCP 与解压后的交接客户端',
        'expected':'按用户指定的数据类型和 MCP 形式只读查询，并能按文档交接',
        'actual':actual,'result':'Passed','evidence_refs':proofs,
    }]}

requirements=[
    {'id':'R-01','source':'request_snapshot','quote':initial,
     'reading':'本期开发数据库、增量、日期分类读取模型和接口已完成；生产接通后的真实联调仍是未来条件，已预备配置与手册，不能记为已经完成',
     'state':'Deferred','evidence_refs':proofs+['LG_project_docs/requirements/T-INSIGHTS-FOUNDATION-20261029-01/release/production-switch.md'],
     'acceptance_refs':[0,1,2,3,4],
     'review':review(source_digest,'开发部分完成',conditions=['后续生产数据库连接接通'],cases=[
        {'condition':0,'branch':'NotMet','input':'生产尚未内网监听，未取得采集端生产连接验证',
         'expected':'用开发数据交付本地底座并预留生产切换',
         'actual':'53119 封邮件完整复制；增量/API/MCP 运行；47 项测试及十四表内容核对通过；生产默认关闭',
         'result':'Passed','evidence_refs':proofs},
        {'condition':0,'branch':'Met','input':'未来真实生产只读连接接通后',
         'expected':'按独立来源配置完成生产预检、首批导入和实际负载验证',
         'actual':'仅完成配置、来源隔离测试和切换手册；真实生产连接、导入和负载未执行',
         'result':'NotRun','evidence_refs':['LG_project_docs/requirements/T-INSIGHTS-FOUNDATION-20261029-01/release/production-switch.md']},
     ])},
    {'id':'R-02','source':'request_snapshot','quote':second,'reading':'按数据类型提供只读接口',
     'state':'Covered','evidence_refs':proofs,'acceptance_refs':[3,5],
     'review':review(source_digest,'11 个工具覆盖分类、统计、邮件原文/AI、状态及十四类业务副本，真实调用 26 次通过')},
    {'id':'R-03','source':'request_snapshot','quote':third,'reading':'标准 MCP、中文工具说明、配置与按需调用交接',
     'state':'Covered','evidence_refs':proofs,'acceptance_refs':[5],
     'review':review(source_digest,'HTTPS MCP 工具发现/调用、资源、旧版 initialize 通过；含真实只读令牌的交接包解压后客户端发现 11 个工具；文档含参数、分页、口径与故障步骤')},
]
remote=before['clarification']['rounds'][0]['exchanges'][0]['answer']
requirements.append({'id':'R-04','source':'clarification:r1.e1','quote':remote,
    'reading':'提供内网远程可调用的 HTTPS MCP 入口；接收方电脑实际路由与客户端验收保留未验项',
    'state':'Covered','evidence_refs':proofs,'acceptance_refs':[5],
    'review':review(hashlib.sha256(remote.encode('utf-8')).hexdigest(),'192.168.10.20:3037 真实严格 HTTPS MCP 验证成功，独立令牌、Host/Origin、网段及防火墙已生效；未声称另一台电脑已验收')})
artifacts=[dict(item) for item in before['artifact_manifest']]
artifacts[-1]['reason']=f"绑定 {len(manifest['files'])} 个实际公开交付文件的 SHA256；私有凭据与运行缓存不纳入公开清单"
clarification=dict(before['clarification'])
clarification['state']='Settled'
changes=[{'path':key,'value':value} for key,value in {
    'request_snapshot':snapshot,'requirement_items':requirements,'artifact_manifest':artifacts,'clarification':clarification,
}.items()]
(root/'.project-governance/intake/mcp-final-amendment.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'.project-governance/intake/terminal-artifacts.json').write_text(json.dumps(artifacts,ensure_ascii=False,indent=2),encoding='utf-8')
incomplete=[
    {'reason':'security-privacy-review 待真实用户审查；用户回复是 MCP 功能指令，没有通过门禁',
     'impact':'本地工程和服务已交付，正式工程 Gate 不能标为通过；用户验收独立 Pending',
     'owner':'task-initiator','reentry_condition':'有权用户对当前已验证交付作出可核对的安全隐私门禁决定'},
    {'reason':'生产连接是未来条件，尚未接通并验证；没有重启权限',
     'impact':'当前数据明确标记 development-local，不能称为实时生产数据',
     'owner':'用户与生产服务器 agent','reentry_condition':'监听与凭据/证书到位且授权采集端进行生产只读联调'},
    {'reason':'尚未从另一台内网电脑执行路由与客户端验收',
     'impact':'服务端与采集电脑通过内网 IP 的真实协议验证已完成，接收方网络路径仍未实测',
     'owner':'待指定的接收方','reentry_condition':'接收方导入专用 CA、配置独立令牌并按交接手册连接验证'},
]
(root/'.project-governance/intake/terminal-incomplete.json').write_text(json.dumps(incomplete,ensure_ascii=False,indent=2),encoding='utf-8')

# Scan only public handoff assets, never echo a matched secret or source content.
local=json.loads((root/'.secrets/local.json').read_text(encoding='utf-8'))
mcp=json.loads((root/'.secrets/mcp-server.json').read_text(encoding='utf-8'))
secret_values=[local[key] for key in ['source_url','target_owner_url','target_writer_url','target_reader_url','api_token']]+list(mcp['tokens'].values())
for relative in manifest['files']:
    data=(root/relative).read_bytes()
    if any(value.encode() in data for value in secret_values):
        raise ValueError('actual private credential found in a public artifact')
print(json.dumps({'public_files':len(manifest['files']),'credential_scan':'Passed','manifest_sha256':hashlib.sha256((root/(verification+'delivery-manifest.json')).read_bytes()).hexdigest()}))
