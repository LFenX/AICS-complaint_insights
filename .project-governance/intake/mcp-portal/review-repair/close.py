"""Discharge actual work and save the true Deferred repair result."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[4]
SKILL=Path(r'C:\Users\Administrator\.codex\skills\run-governed-product-workflow')
TASK='T-INSIGHTS-MCP-REPAIR-20261030-01'
INPUT=Path(__file__).parent
TD=ROOT/'.project-governance/tasks'/TASK
REL=f'LG_project_docs/requirements/{TASK}'

def main():
    before=json.loads((TD/'before.json').read_text(encoding='utf-8'))
    items=before['requirement_items']
    digest=hashlib.sha256(before['request_snapshot']['text'].encode()).hexdigest()
    evidence=[REL+'/verification/results.json',REL+'/verification/coverage.json','.runtime/mcp-portal-repair-tests-A02.log']
    for item in items:
        item['evidence_refs']=evidence
        item['state']='Deferred' if item['id']=='R-02' else 'Covered'
        if item['id']=='R-01':
            item['review']={'source_sha256':digest,'conditions':['登录管理员后才能生成token'],'cases':[
                {'condition':0,'branch':'Met','input':'独立owner凭据登录后以本会话CSRF发放','expected':'可生成并单次显示，令牌可用于MCP','actual':'真实登录303、生成200、Bearer健康200、撤销后401，凭据仅在用户私聊交付','result':'Passed','evidence_refs':evidence},
                {'condition':0,'branch':'NotMet','input':'匿名和仅MCP Bearer发放','expected':'拒绝且不改变授权','actual':'匿名真实发放401；Bearer与CSRF负向夹具通过','result':'Passed','evidence_refs':evidence}]}
        elif item['id']=='R-03':
            item['review']={'source_sha256':digest,'conditions':[],'cases':[{'condition':None,'branch':'Unconditional','input':'用户明确答复开始审查','expected':'实际审查并修复确认问题，不能冒称人工Gate批准','actual':'独立首轮四项问题已返修复验；后续轮次待开展，原门禁Pending','result':'Passed','evidence_refs':[REL+'/verification/round-1-report.md',REL+'/verification/fixes.json']}]}
    change=INPUT/'discharge-amendment.json'
    change.write_text(json.dumps([{'path':'requirement_items','value':items}],ensure_ascii=False,indent=2),encoding='utf-8')
    subprocess.run([sys.executable,str(SKILL/'scripts/amend_record.py'),str(TD/'before.json'),'--changes-json-file',str(change),'--reason','按真实结果交代：账号入口和开始指令Covered；连续两轮仍进行中，R-02 Deferred，不伪造完成','--basis',REL+'/verification/coverage.json'],check=True)
    args=[sys.executable,str(SKILL/'scripts/close_task.py'),str(TD),'--status','Deferred','--fact','四项缺陷修复并验证，45文件版本已固定；正式人类门禁Pending及后续完整审查待完成','--change','按来源限额和复用挑战；元数据故障保留网页撤销；SDK转换前JSON Schema校验；未知工具顶层-32602；公共指南和无凭据包同步更新','--verification','Passed::30项单测和契约测试通过::.runtime/mcp-portal-repair-tests-A02.log','--verification','Passed::严格CA真实内网13检查、11工具14表、22页和登录签发使用撤销退出通过::'+REL+'/verification/results.json','--incomplete-json-file',str(INPUT/'incomplete.json'),'--artifact-manifest-json-file',str(INPUT/'terminal-artifacts.json'),'--source-snapshot-json-file',str(INPUT/'terminal-snapshot.json'),'--evidence-ref',REL+'/verification/coverage.json']
    subprocess.run(args,check=True)

if __name__=='__main__': main()
