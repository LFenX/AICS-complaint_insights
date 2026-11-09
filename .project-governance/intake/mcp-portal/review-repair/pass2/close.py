"""Save the true repair outcome; the later review remains explicitly pending."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(r'D:\LFEN_project\dev_project\complaint-insights')
SKILL=Path(r'C:\Users\Administrator\.codex\skills\run-governed-product-workflow')
INPUT=Path(__file__).parent
TASK='T-INSIGHTS-MCP-REPAIR-20261030-02'
TD=ROOT/'.project-governance/tasks'/TASK
REL=f'LG_project_docs/requirements/{TASK}'

def main():
    before=json.loads((TD/'before.json').read_text(encoding='utf-8'))
    items=before['requirement_items']
    digest=hashlib.sha256(before['request_snapshot']['text'].encode()).hexdigest()
    refs=[REL+'/verification/results.json',REL+'/verification/coverage.json','.runtime/mcp-portal-repair2-tests-A01.log']
    for item in items:
        item['state']='Deferred' if item['id']=='R-02' else 'Covered';item['evidence_refs']=refs
        if item['id']=='R-01':
            item['review']={'source_sha256':digest,'conditions':['独立管理员登录后才能生成token'],'cases':[
                {'condition':0,'branch':'Met','input':'真实owner独立登录并带同会话CSRF发放','expected':'生成单次显示token，可查询且可撤销','actual':'真实登录303、发放200、使用200、撤销后401，用户私聊交付账号口令和入口','result':'Passed','evidence_refs':refs},
                {'condition':0,'branch':'NotMet','input':'匿名、仅MCP Bearer或无效CSRF发放','expected':'拒绝且不改变授权','actual':'匿名真实401、无效CSRF真实403、Bearer隔离夹具401，均通过','result':'Passed','evidence_refs':refs}]}
        elif item['id']=='R-03':
            item['review']={'source_sha256':digest,'conditions':[],'cases':[{'condition':None,'branch':'Unconditional','input':'用户开始审查持续授权','expected':'实际审查与同范围返修，不推定人工Gate批准','actual':'两轮独立完整审查7项发现均修复复验；正式人类门禁与验收Pending','result':'Passed','evidence_refs':[REL+'/verification/round-2-report.md',REL+'/verification/fixes.json']}]}
    changes=INPUT/'discharge-amendment.json';changes.write_text(json.dumps([{'path':'requirement_items','value':items}],ensure_ascii=False,indent=2),encoding='utf-8')
    subprocess.run([sys.executable,str(SKILL/'scripts/amend_record.py'),str(TD/'before.json'),'--changes-json-file',str(changes),'--reason','按真实工程结果交代；两轮已修复七项，但新版本连续两轮仍未完成，R-02保留Deferred','--basis',REL+'/verification/coverage.json'],check=True)
    subprocess.run([sys.executable,str(SKILL/'scripts/append_run_event.py'),str(TD),'--run-id','RUN-MCP-REPAIR-02','--attempt-id','A01','--event-type','run_finished','--summary','七项已返修并完成36测试、15真实检查和Windows权限反例复验；保存新版本，后续审查和人工门禁限制保留','--status','succeeded','--evidence-ref',REL+'/verification/delivery-files.json'],check=True)
    subprocess.run([sys.executable,str(SKILL/'scripts/close_task.py'),str(TD),'--status','Deferred','--fact','七项确认问题已修复复验，新版本已保存；正式人类门禁Pending，后续独立完整审查另留实际证据','--change','保留合法字符串原值；客户端先限权后写且失败清理；非法信封错误-32600且不回显；同步指南/实际Schema/无凭据包','--verification','Passed::36项单测与契约测试通过::.runtime/mcp-portal-repair2-tests-A01.log','--verification','Passed::真实严格CA15检查、11工具14表22页和管理员签发撤销通过::'+REL+'/verification/results.json','--verification','Passed::Windows真实ACL时序、写入失败和分页恢复对照通过::'+REL+'/verification/client-acl-results.json','--incomplete-json-file',str(INPUT/'incomplete.json'),'--artifact-manifest-json-file',str(INPUT/'terminal-artifacts.json'),'--source-snapshot-json-file',str(INPUT/'terminal-snapshot.json'),'--evidence-ref',REL+'/verification/coverage.json'],check=True)

if __name__=='__main__': main()
