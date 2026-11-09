"""Initialize the authorized implicit-destination repair."""
from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SKILL = Path(r"C:\Users\Administrator\.codex\skills\run-governed-product-workflow")
TASK = "T-INSIGHTS-REPAIR-20261029-02"
REQUEST = "先把修复做了呗"
REF = f"LG_project_docs/requirements/{TASK}/discovery/survey.md"
EVIDENCE = ".project-governance/tasks/T-INSIGHTS-REVIEW-20261029-01/evidence/round-2-results.json"
SCOPE = ["连接前拒绝缺少主机、端口或数据库名的连接串"]
ACCEPTANCE = [
    "省略主机、端口或数据库名的连接串在建立连接前被拒绝，PGHOST、PGPORT、PGDATABASE 不能代替这三项",
    "已写明主机、端口和数据库名的连接串，在上述环境变量指向其他地址时身份保持为连接串中的值",
    "既有 hostaddr 与 service 拒绝仍然有效，当前显式本地配置的规则测试通过",
]
STEPS = [
    "拒绝缺省主机、端口或数据库名的连接串",
    "验证显式连接参数不受环境缺省值影响并回归规则测试",
    "保存返修结果并归属已授权的父审查会话",
]
NOTICE = "你的需求已经描述的非常清楚了，并且和项目现状一致，本次跳过向你提问的阶段"


def main() -> None:
    now = datetime.now(timezone.utc).isoformat()
    inputs = ROOT / ".project-governance" / "intake" / "repair-round2"
    inputs.mkdir(parents=True, exist_ok=True)
    decisions = [{
        "id": "D-REPAIR-PROCEED",
        "kind": "Proceed",
        "presented": "第二轮已确认：省略主机或端口时 PGHOST/PGPORT 改变实际连接地址，原校验仍按 localhost:5432 放行。修复要求连接串写明主机、端口和数据库名，并保持显式配置不受环境默认值影响。",
        "response": REQUEST,
        "decided_by": "lfenink",
        "decided_at": now,
        "evidence_ref": REF,
        "outcome": "Approved",
    }]
    authority = [{
        "reference": REF,
        "source_kind": "UserDirective",
        "status": "Valid",
        "scope_refs": SCOPE,
        "evidence_refs": [REF, EVIDENCE],
        "verified_at": now,
        "expires_at": None,
    }]
    requirements = [{
        "id": "R-01",
        "source": "request_snapshot",
        "quote": REQUEST,
        "reading": "修复第二轮确认的连接串隐式主机、端口和数据库名校验缺陷，不扩大读取范围，不连接生产",
        "state": "Open",
        "evidence_refs": [REF, EVIDENCE],
        "acceptance_refs": [0, 1, 2],
    }]
    analysis = {
        "method_version": "first-principles-v1",
        "depth": "Deep",
        "outcome": "缺少主机、端口或数据库名的连接配置在连接前失败，显式配置的实际目的地与校验身份一致",
        "facts": [
            {"id": "F1", "statement": "conninfo_to_dict 不补齐省略的主机、端口和数据库名；connection_identity 自行填入 localhost、5432 和空库名", "evidence_refs": [REF]},
            {"id": "F2", "statement": "第二轮隔离连接复现：省略主机和端口时 PGHOST/PGPORT 决定实际连接，校验身份仍是 localhost:5432", "evidence_refs": [EVIDENCE, REF]},
        ],
        "constraints": [
            {"id": "C1", "statement": "不写开发源库，不连接或重启生产，不改变监听、权限或读取范围", "source_refs": [REF]},
            {"id": "C2", "statement": "目的地身份必须在连接前绑定，不能与 libpq 实际地址分离", "source_refs": [EVIDENCE]},
        ],
        "assumptions": [
            {"id": "A1", "statement": "当前交付的本地配置和生产示例 URL 已写明主机、端口和数据库名", "validation": "对这两份配置调用 connection_identity，确认三项均来自连接串"},
        ],
        "unknowns": [
            {"id": "U1", "statement": "生产监听范围变更是否已经生效、凭据是否已交付到采集端", "owner": "lfenink", "resolution_condition": "用户通知监听完成后，再做生产连通和只读预检", "blocking": False},
        ],
        "fundamentals": [
            {"id": "P1", "statement": "校验使用的主机、端口和数据库名必须就是连接串中的显式值", "derived_from": ["F1", "F2", "C2"]},
            {"id": "P2", "statement": "环境默认值只在参数省略时介入，因此省略必须在连接前失败", "derived_from": ["F2", "C2"]},
            {"id": "P3", "statement": "已写明的参数优先于进程环境，不能为了防绕过而改写显式配置", "derived_from": ["F1", "C1"]},
        ],
        "causal_links": [
            {"from_ref": "P1", "to_ref": "O1", "rationale": "省略参数时拒绝连接，环境默认值不再进入身份计算", "evidence_refs": [REF, EVIDENCE]},
            {"from_ref": "P2", "to_ref": "O1", "rationale": "失败发生在连接前，避免先连到未声明地址再解释身份", "evidence_refs": [EVIDENCE]},
            {"from_ref": "P3", "to_ref": "O1", "rationale": "显式连接串保持原值，现有交付配置不需要改写", "evidence_refs": [REF]},
        ],
        "alternatives": [
            {"id": "O1", "description": "强制主机、端口和数据库名显式，保留既有 hostaddr 与 service 拒绝", "status": "Selected", "derived_from": ["P1"], "tradeoffs": ["省略目的地的配置不再可用；现有交付 URL 已显式，无需改配置"]},
            {"id": "O0", "description": "保持现状", "status": "Rejected", "derived_from": ["P1"], "tradeoffs": ["环境默认值仍可改变真实源，而身份摘要不变"]},
            {"id": "O2", "description": "解析并固化全部 libpq 环境与 service 缺省后再连接", "status": "Rejected", "derived_from": ["P1"], "tradeoffs": ["要追踪可变全局环境和外部 service 文件；本期不需要隐式配置"]},
        ],
        "decision_criteria": [
            {"id": "K1", "statement": "隐式目的地在连接前失败", "source_refs": [REF]},
            {"id": "K2", "statement": "显式配置的身份不被环境默认值改写，现有拒绝规则保持有效", "source_refs": [REF]},
        ],
        "selected_approach": "O1",
        "derivation": [{"plan_step": step, "derived_from": ["P1", "P2", "P3"], "supports": ["K1", "K2"]} for step in STEPS],
        "validation_refs": [f"LG_project_docs/requirements/{TASK}/verification/results.json"],
        "source_refs": [REF, EVIDENCE],
    }
    for name, value in {"decisions": decisions, "authority": authority, "requirements": requirements, "analysis": analysis}.items():
        (inputs / f"{name}.json").write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    args = [
        sys.executable, str(SKILL / "scripts" / "init_task.py"),
        "--project-root", str(ROOT),
        "--project-id", "complaint-insights",
        "--work-item-id", "LOCAL-ANALYTICS-FOUNDATION",
        "--task-id", TASK,
        "--ordinal", "3",
        "--objective", "修复第二轮确认的连接串隐式主机、端口和数据库名校验缺陷",
        "--request-snapshot", REQUEST,
        "--development-type", "DT-06",
        "--delivery-scenario", "DS-03",
        "--risk-level", "Medium",
        "--confidence", "High",
        "--baseline-inheritance", "Revise",
        "--depends-on", "T-INSIGHTS-REVIEW-20261029-01",
        "--change-surface", "API/Integration",
        "--change-surface", "Identity/Security/Privacy",
        "--basis", REF,
        "--authority-reference", REF,
        "--tailoring-stage", "S4",
        "--out-of-scope", "生产接入与重启、数据库结构或数据变更、监听或权限变更、扩大读取范围",
        "--forbidden-action", "写开发源库、连接或重启生产、修改父任务封存账本",
        "--rollback", "回退 insights/config.py 与 tests/test_rules.py 的本次改动；数据和权限不变",
        "--clarification-skipped",
        "--clarification-notice", NOTICE,
        "--clarification-basis", "已核对第二轮反例、连接串解析和现有显式配置；用户要求直接修复，没有新的目标、范围或授权分歧",
        "--survey-ref", REF,
        "--decisions-json-file", str(inputs / "decisions.json"),
        "--authority-assessments-json-file", str(inputs / "authority.json"),
        "--requirement-items-json-file", str(inputs / "requirements.json"),
        "--first-principles-json-file", str(inputs / "analysis.json"),
    ]
    for path in [
        "insights/config.py",
        "tests/test_rules.py",
        "LG_project_docs/requirements/T-INSIGHTS-REPAIR-20261029-02/**",
        "update_log/**",
        ".project-governance/**",
    ]:
        args += ["--allowed-path", path]
    for value in SCOPE:
        args += ["--in-scope", value]
    for value in ACCEPTANCE:
        args += ["--acceptance", value, "--verification-plan", value]
    for value in STEPS:
        args += ["--plan-step", value]
    facts = {
        "product_intent_change": "No",
        "initiative_scope_change": "No",
        "requirement_change": "No",
        "external_behavior_change": "Yes",
        "design_change": "Yes",
        "architecture_impact": "No",
        "security_privacy_impact": "Yes",
        "data_ai_impact": "No",
        "formal_knowledge_records": "No",
        "operations_impact": "No",
        "production_release": "No",
        "irreversible_change": "No",
        "actual_execution": "Yes",
        "authority_available": "Yes",
        "migration_retirement": "No",
        "external_system_effect": "No",
        "formal_review_or_gate": "No",
    }
    for key, value in facts.items():
        args += ["--applicability-fact", f"{key}={value}"]
    for key in ["E01", "E03", "E04", "E05"]:
        args += ["--extension-trigger", f"{key}=Inactive"]
    args += ["--extension-trigger", "E02=Active", "--extension-evidence-ref", f"E02={REF}"]
    subprocess.run(args, check=True)


if __name__ == "__main__":
    main()
