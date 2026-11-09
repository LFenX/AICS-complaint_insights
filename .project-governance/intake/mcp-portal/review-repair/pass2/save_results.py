"""Reuse the evidence writer, then bind this repair's actual proofs and version."""
from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil

ROOT=Path(r'D:\LFEN_project\dev_project\complaint-insights')
INPUT=Path(__file__).parent
TASK='T-INSIGHTS-MCP-REPAIR-20261030-02'
REL=f'LG_project_docs/requirements/{TASK}'
DOCS=ROOT/REL
CHAT=Path(r'C:\Users\Administrator\Documents\Codex\2026-10-30\complaint-insights-mcp')

def save(path,value): path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def main():
    spec=importlib.util.spec_from_file_location('evidence_writer',INPUT.parent/'save_results.py')
    writer=importlib.util.module_from_spec(spec);spec.loader.exec_module(writer)
    writer.TASK=TASK;writer.INPUT=INPUT;writer.TD=ROOT/'.project-governance/tasks'/TASK;writer.REL=REL;writer.DOCS=DOCS
    with redirect_stdout(io.StringIO()): writer.main()
    for name in ['report.md','results.json']:
        shutil.copyfile(CHAT/'work/round2'/name,DOCS/('verification/round-2-'+name))
    shutil.copyfile(CHAT/'work/root-review/repair2-client/client-results.json',DOCS/'verification/client-acl-results.json')
    for name in ['before','after']:
        shutil.copyfile(ROOT/f'.runtime/mcp-portal-repair2-{name}-listeners.json',DOCS/f'verification/{name}-listeners.json')
    fixes=json.loads((DOCS/'verification/fixes.json').read_text(encoding='utf-8'))
    fixes['test_count']=36
    fixes['findings'] += [
        {'id':'R2-01','result':'Fixed','actual':'合法null/[]/{}/[1]/引号/false/数字字符串原样传递；真实source_id字符串null为NOT_FOUND，不再查默认源','evidence_refs':['tests/test_mcp.py',REL+'/verification/results.json']},
        {'id':'R2-02','result':'Fixed','actual':'真实Windows合成Users可读父目录中首次写入前已移除Users读取；完整/部分写入和fsync/ACL故障后无文件；已有配置保留','evidence_refs':['tests/test_mcp.py',REL+'/verification/client-acl-results.json']},
        {'id':'R2-03','result':'Fixed','actual':'非法信封-32600、破损JSON-32700、未知方法-32601、协议参数/未知工具-32602、业务参数isError均通过，非法信封不回显输入','evidence_refs':['tests/test_mcp.py',REL+'/verification/results.json']},
    ]
    for item in fixes['findings']:
        item['evidence_refs']=[v.replace('.runtime/mcp-portal-repair-tests-A02.log','.runtime/mcp-portal-repair2-tests-A01.log') for v in item['evidence_refs']]
    save(DOCS/'verification/fixes.json',fixes)
    coverage=json.loads((DOCS/'verification/coverage.json').read_text(encoding='utf-8'))
    for item in coverage['requirements']:
        item['evidence_refs']=[v.replace('.runtime/mcp-portal-repair-tests-A02.log','.runtime/mcp-portal-repair2-tests-A01.log') for v in item['evidence_refs']]
        if item['id']=='CURRENT-R-02':
            item['actual']='首轮四项与第二轮三项均修复复验；尚未取得当前新版本连续两轮完整无问题，机器登记限制保留'
            item['evidence_refs'] += [REL+'/verification/round-2-report.md',REL+'/verification/client-acl-results.json']
    save(DOCS/'verification/coverage.json',coverage)
    (DOCS/'verification/report.md').write_text('''# MCP第二次返修工程验证

两轮共7项确认问题已修复，逐项见 fixes.json。36项单测/契约测试通过；真实内网严格CA的15项检查通过，含11工具14表、SDK22页、独立管理员登录签发/使用/撤销/退出、字符串来源不回退、原生JSON-RPC错误分层。另在Windows合成Users可读目录复现原客户端反例，新版首字节写出前已限权，故障无残留；分页变版、重复游标和页数上限对照均通过。

管理员登录：https://10.8.61.200:3029/admin/login ，唯一用户名owner。口令仅在当前用户私聊交付，不写入报告/指南/ZIP/日志。分享门户：https://10.8.61.200:3029/ ，MCP：https://10.8.61.200:3037/mcp 。

本次仅重启mcp；desk与3030/3036/15433前后监听PID一致，详情见before/after-listeners.json。watch停止，生产读取false，目标仅127.0.0.1:15433历史副本；无生产连接。公共23文件ZIP已按实际Schema重建。

原始请求和澄清逐项见coverage.json。正式人类门禁与用户验收Pending；另一内网电脑路由/CA未实测。原父结果Deferred导致官方Offer登记被拒绝，保留原失败，不改写父状态、不伪造ManagedByParent或机器Passed。当前工程结果留档后重新进行独立完整审查；连续两轮条件尚未达到。
''',encoding='utf-8')
    manifest=json.loads((DOCS/'verification/delivery-files.json').read_text(encoding='utf-8'))
    names={row['path'] for row in manifest['files']}
    names.add(REL+'/verification/client-acl-results.json')
    entries=[{'path':name,'sha256':hashlib.sha256((ROOT/name).read_bytes()).hexdigest()} for name in sorted(names)]
    manifest['files']=entries
    manifest['version_sha256']=hashlib.sha256(json.dumps(entries,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    save(DOCS/'verification/delivery-files.json',manifest)
    snapshot=json.loads((INPUT/'terminal-snapshot.json').read_text(encoding='utf-8'))
    snapshot['file_manifest_sha256']=hashlib.sha256((DOCS/'verification/delivery-files.json').read_bytes()).hexdigest()
    save(INPUT/'terminal-snapshot.json',snapshot)
    incomplete=json.loads((INPUT/'incomplete.json').read_text(encoding='utf-8'))
    incomplete[-1]['reason']='父Deferred使Offer登记拒绝；两轮共七项均修复，当前新交付的独立完整后续轮次待完成'
    save(INPUT/'incomplete.json',incomplete)
    print(json.dumps({'result':'SAVED','delivery_files':len(entries),'version_sha256':manifest['version_sha256'],'fixed_findings':len(fixes['findings']),'tests':36,'live_checks':15,'formal_gates':'Pending'}))

if __name__=='__main__': main()
