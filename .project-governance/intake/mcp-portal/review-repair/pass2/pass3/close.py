"""Close engineering as Deferred without fabricating human or review gates."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(r'D:\LFEN_project\dev_project\complaint-insights')
SKILL=Path(r'C:\Users\Administrator\.codex\skills\run-governed-product-workflow')
INPUT=Path(__file__).parent
TASK='T-INSIGHTS-MCP-REPAIR-20261030-03'
TD=ROOT/'.project-governance/tasks'/TASK
REL=f'LG_project_docs/requirements/{TASK}'

def run(script,*args):
    subprocess.run([sys.executable,str(SKILL/'scripts'/script),*map(str,args)],check=True)

def main():
    before=json.loads((TD/'before.json').read_text(encoding='utf-8'))
    items=before['requirement_items']
    digest=hashlib.sha256(before['request_snapshot']['text'].encode()).hexdigest()
    refs=[REL+'/verification/results.json',REL+'/verification/coverage.json','.runtime/mcp-portal-repair3-tests-A01.log']
    for item in items:
        item['state']='Deferred' if item['id']=='R-02' else 'Covered'
        item['evidence_refs']=refs
        if item['id']=='R-01':
            item['review']={'source_sha256':digest,'conditions':['独立管理员登录后才能生成token'],'cases':[
                {'condition':0,'branch':'Met','input':'真实owner独立登录并带同会话CSRF发放','expected':'生成单次显示token，可查询且可撤销',
                 'actual':'真实登录303、发放200、使用200、撤销后401；新跨读轮换夹具旧会话303、新口令200','result':'Passed','evidence_refs':refs},
                {'condition':0,'branch':'NotMet','input':'匿名、仅MCP Bearer或无效CSRF发放','expected':'拒绝且不改变授权',
                 'actual':'匿名真实401、无效CSRF真实403、Bearer隔离夹具401，均通过','result':'Passed','evidence_refs':refs}]}
        elif item['id']=='R-03':
            item['review']={'source_sha256':digest,'conditions':[],'cases':[{'condition':None,'branch':'Unconditional','input':'用户开始审查持续授权',
                'expected':'实际审查与同范围返修，不推定人工Gate批准','actual':'三轮11项已修复复验；第三轮外部漂移原报告保留；当前新版本待后续完整审查，正式门禁Pending',
                'result':'Passed','evidence_refs':[REL+'/verification/round-3-report.md',REL+'/verification/fixes.json']}]}
    changes=INPUT/'discharge-amendment.json'
    changes.write_text(json.dumps([{'path':'requirement_items','value':items}],ensure_ascii=False,indent=2),encoding='utf-8')
    run('amend_record.py',TD/'before.json','--changes-json-file',changes,'--reason','按真实工程结果保存；三轮11项已修复，但当前新版本连续两轮待完成，R-02保留Deferred','--basis',REL+'/verification/coverage.json')
    run('append_run_event.py',TD,'--run-id','RUN-MCP-REPAIR-03','--attempt-id','A01','--event-type','run_finished',
        '--summary','11项已修复，41测试和17真实检查通过；冻结当前49文件版本，后续实际审查与人工门禁限制保留',
        '--status','succeeded','--evidence-ref',REL+'/verification/delivery-files.json')
    run('close_task.py',TD,'--status','Deferred','--fact','三轮11项已修复复验并保存新版本；正式人类门禁Pending，后续完整审查另留实际证据',
        '--change','同快照管理员摘要；精确请求ID和有界消息重放；五分页非空游标；更新当前交接证据与实际Schema无凭据包',
        '--verification','Passed::41项单测契约和边界通过::.runtime/mcp-portal-repair3-tests-A01.log',
        '--verification','Passed::真实严格CA17检查、11工具14表完整分页与管理员签发撤销通过::'+REL+'/verification/results.json',
        '--verification','Passed::仅desk/mcp更新；保护服务PID不变；外部能力变更保留重新定版::'+REL+'/verification/deployment.json',
        '--incomplete-json-file',INPUT/'incomplete.json','--artifact-manifest-json-file',INPUT/'terminal-artifacts.json',
        '--source-snapshot-json-file',INPUT/'terminal-snapshot.json','--evidence-ref',REL+'/verification/coverage.json')

if __name__=='__main__':main()
