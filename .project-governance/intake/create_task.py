"""Capture the actual chat directive and initialize the governed local task."""
from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SKILL = Path(r"C:\Users\Administrator\.codex\skills\run-governed-product-workflow")
TASK = "T-INSIGHTS-FOUNDATION-20261029-01"
REQUEST = "你可以先用本地开发数据先推进本地的数据库建立，后续只要生产数据库连接接通，可以快速实现我后续的规划"
REF = f"LG_project_docs/requirements/{TASK}/discovery/survey.md"
SCOPE = ["本地独立数据库与原始邮件、AI 分类副本", "增量同步、补充对账和日期分类读取模型", "agent 只读 SQL/API 及生产源切换准备"]
ACCEPTANCE = [
    "独立 PostgreSQL 和数据卷运行，仅监听回环地址，源库连接强制只读，原项目不变",
    "完整导入开发原始邮件、AI 产物、绑定和静态/动态目录，按北京时间日期及分类可追溯原文",
    "新增、更新、删除、AI 补全、无事件变更和重启续传通过隔离夹具验证，失败不前移水位",
    "只读 SQL 与鉴权 API 可查询日汇总、分类、分页邮件、全文及同步状态，拒绝未授权访问",
    "生产配置独立，来源隔离且默认不接触生产；提供切换步骤和未验项",
]
STEPS = ["建立独立运行环境和数据库", "实现源读取及原子同步发布", "实现日期分类读取模型和只读接口", "导入真实开发数据并执行隔离与接口验证", "交付运行、切源说明和实际证据"]

def main():
    now = datetime.now(timezone.utc).isoformat()
    inputs = ROOT / ".project-governance" / "intake"
    decision = [{"id": "D-LOCAL-PROCEED", "kind": "Proceed", "presented": "独立数据库、同步器和查询 API 尚未创建，可以在生产重启前推进；本期使用开发数据，不操作生产服务。", "response": REQUEST, "decided_by": "当前聊天用户", "decided_at": now, "evidence_ref": REF, "outcome": "Approved"}]
    authority = [{"reference": REF, "source_kind": "UserDirective", "status": "Valid", "scope_refs": SCOPE, "evidence_refs": [REF], "verified_at": now, "expires_at": None}]
    requirements = [{"id": "R-01", "source": "request_snapshot", "quote": REQUEST, "reading": "用开发数据交付此前已讨论的独立库、同步器、日期分类读取模型及 agent 查询接口，并预留生产接入", "state": "Open", "evidence_refs": [REF], "acceptance_refs": [0,1,2,3,4]}]
    analysis = {
        "method_version": "first-principles-v1", "depth": "Deep", "outcome": "agent 能通过独立 SQL/API 分析按日期分类的真实开发邮件，并能在接入条件齐备后切换生产来源",
        "facts": [{"id":"F1","statement":"开发 PostgreSQL、源表和 AI 关联已实查；分类同时依赖部署 JSON","evidence_refs":[REF]}, {"id":"F2","statement":"日志存在保留期、缺少事件的表和归档映射，单一 ID 水位不能覆盖全部变化","evidence_refs":[REF]}],
        "constraints": [{"id":"C1","statement":"不写开发源库、不操作生产、不改变原项目结构与命名；仅采纳 AI 分类","source_refs":[REF]}, {"id":"C2","statement":"查询读取独立库的预计算模型，服务只监听回环地址并鉴权","source_refs":[REF]}],
        "assumptions": [{"id":"A1","statement":"Docker 和缓存镜像可建立独立实例","validation":"启动独立容器后运行真实连接与健康检查"}],
        "unknowns": [{"id":"U1","statement":"生产监听、密码及可信证书仍未完成采集端联调","owner":"用户与生产服务器 agent","resolution_condition":"后续交付凭据和证书并完成连接验收","blocking":False}],
        "fundamentals": [{"id":"P1","statement":"副本必须保留源身份、原文和关联，切换来源不能混合主键","derived_from":["F1","C1"]}, {"id":"P2","statement":"及时增量与最终一致性对账必须同时存在","derived_from":["F2"]}, {"id":"P3","statement":"数据获取与查询必须解耦且发布原子化","derived_from":["C2"]}],
        "causal_links": [{"from_ref":"P1","to_ref":"O1","rationale":"来源命名空间加原始 JSON 镜像可保留证据并适应生产字段扩展","evidence_refs":[REF]}, {"from_ref":"P2","to_ref":"O1","rationale":"日志驱动和有界周期对账共同覆盖无事件更新、删除、离线与迟提交","evidence_refs":[REF]}],
        "alternatives": [{"id":"O1","description":"独立 PostgreSQL、Python 同步器与只读 API，日志增量结合内容对账","status":"Selected","derived_from":["P1","P2","P3"],"tradeoffs":["新增独立实例及常驻进程；无需变更源表或复制权限"]}, {"id":"O2","description":"保持现状，agent 直接查询现有开发或生产库","status":"Rejected","derived_from":["C1","C2"],"tradeoffs":["没有隔离分析数据和稳定汇总，查询负载回到业务库"]}, {"id":"O3","description":"使用 PostgreSQL 逻辑复制或 CDC","status":"Rejected","derived_from":["P2","C1"],"tradeoffs":["需要源端复制授权与运行配置变更，超出本期只读边界"]}],
        "decision_criteria": [{"id":"K1","statement":"可追溯全量且来源隔离、无源写入","source_refs":[REF]}, {"id":"K2","statement":"增量可恢复、汇总与明细一致、权限明确","source_refs":[REF]}],
        "selected_approach":"O1", "derivation":[{"plan_step":step,"derived_from":["P1","P2","P3"],"supports":["K1","K2"]} for step in STEPS], "validation_refs":[f"LG_project_docs/requirements/{TASK}/verification/results.json"], "source_refs":[REF],
    }
    for name,value in {"decisions":decision,"authority":authority,"requirements":requirements,"analysis":analysis}.items():
        (inputs/f"{name}.json").write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding="utf-8")
    args=[sys.executable,str(SKILL/"scripts/init_task.py"),"--project-root",str(ROOT),"--project-id","complaint-insights","--work-item-id","LOCAL-ANALYTICS-FOUNDATION","--task-id",TASK,"--ordinal","1","--objective","使用开发数据交付独立客诉分析数据底座，并预留生产只读接入","--request-snapshot",REQUEST,"--development-type","DT-01","--delivery-scenario","DS-01","--risk-level","Medium","--baseline-inheritance","New","--basis",REF,"--authority-reference",REF,"--allowed-path","**","--forbidden-action","写入开发源库或操作生产数据库、服务和配置","--out-of-scope","看板 UI、自动周报、附件文件复制、人工分类和生产联调","--clarification-skipped","--clarification-notice","你的需求已经描述的非常清楚了，并且和项目现状一致，本次跳过向你提问的阶段。","--clarification-basis","此前完成源数据、网络、目录和运行环境勘察，用户明确先用开发数据推进已讨论范围","--survey-ref",REF,"--tailoring-stage","S1"]
    for key in ["API/Integration","Data/Schema","AI/Data Governance","Architecture/Multi-repo","Identity/Security/Privacy","Deploy/Operations"]:
        args += ["--change-surface",key]
    facts={"product_intent_change":"No","initiative_scope_change":"Yes","requirement_change":"Yes","external_behavior_change":"Yes","design_change":"Yes","architecture_impact":"Yes","security_privacy_impact":"Yes","data_ai_impact":"Yes","formal_knowledge_records":"No","operations_impact":"Yes","production_release":"No","irreversible_change":"No","actual_execution":"Yes","authority_available":"Yes","migration_retirement":"No","external_system_effect":"No","formal_review_or_gate":"No"}
    for key,value in facts.items(): args += ["--applicability-fact",f"{key}={value}"]
    for key in ["E01","E02","E03","E05"]: args += ["--extension-trigger",f"{key}=Active","--extension-evidence-ref",f"{key}={REF}"]
    args += ["--extension-trigger","E04=Inactive"]
    for value in SCOPE: args += ["--in-scope",value]
    for value in ACCEPTANCE: args += ["--acceptance",value,"--verification-plan",value]
    for value in STEPS: args += ["--plan-step",value]
    args += ["--rollback","仅停止本项目命名的进程和容器；保留独立卷；源项目和源库无需回滚"]
    for arg,name in [("--decisions-json-file","decisions"),("--authority-assessments-json-file","authority"),("--requirement-items-json-file","requirements"),("--first-principles-json-file","analysis")]: args += [arg,str(inputs/f"{name}.json")]
    subprocess.run(args,check=True)

if __name__ == "__main__": main()
