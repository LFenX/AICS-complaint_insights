# Clause Context: T-INSIGHTS-DAILY-TABLE-20261030-02 / validate_change

- Status: `Expanded`
- Query digest: `1e91757e7d98567e356fb34bf7925f247a219fd461bff8ee52365160f07eb832`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `7/7`
- Budget: `11508/12000` chars
- Fallback: `section`

## Source Index

- `C08`: `references/02_核心规范/C08_Agent_Context_Governance_Standard.md` / `V6.3 Candidate` / SHA-256 `262f2a190f130cb97955e58fca57d2216e2edf949d2f271413e5dff5d6faeb6d`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `VC-PPG-PRO-001`: `references/01_治理基线/Vibe_Coding_任务类型裁剪与统一执行流程规范_V6.3.md` / `V6.3 Candidate` / SHA-256 `548a810a1cbce4fc7970f87778c71f56c9d0921e3ba385a73d085b8ed0276329`
- `C05`: `references/02_核心规范/C05_Acceptance_Verification_and_Validation_Standard.md` / `V6.3 Candidate` / SHA-256 `7973bcb4ea442030772e36b7418cc1e03f55e0b3aaa6072f4ec1c198d1b537c7`
- `C11`: `references/02_核心规范/C11_Configuration_Version_Baseline_and_Change_Standard.md` / `V6.3 Candidate` / SHA-256 `88ec56f78f6d3da6f94b1684c7b1296ed1825bfcc961f0f8d3636c8c6a26f7e1`

> 完整 lane rank 和逐条来源字段保存在同目录 `query-result.json`。

## Citations

### 1. C08 — C08 Agent 上下文治理规范 > 5. 规范性用语与受控判定 > 5.4 规则优先级

- `P0` · Locator `C08:262f2a19:416d3219:103:b1aad2c4` · Lines `138-138`

```text
高优先级 Context 失效时必须排除并报告，禁止退而使用其过期版本。相同优先级或不同事实源存在语义冲突时，禁止仅按时间戳、文件名、搜索排名或出现次数自动解决。
```

### 2. C08 — C08 Agent 上下文治理规范 > 10. 强制规则 > 10.12 Attachment、Retrieval 与 Transformation

- `P0` · Locator `C08:262f2a19:a5c224ba:353:c80124a4` · Lines `476-476`

```text
8. 解析失败、内容截断、编码异常、OCR 不确定或附件版本不明时必须报告，不得静默补写。
```

### 3. C12 — C12 评审、质量门禁与产品健康规范 > 2. 目的

- `P0` · Locator `C12:508ab626:28e7276d:36:af7a1d0d` · Lines `45-45`

```text
10. 使 Agent 和自动化工具可以计算、检查和起草，但不能自批高风险输出或风险接受；
```

### 4. C12 — C12 评审、质量门禁与产品健康规范 > 5. 规范性用语与受控判定 > 5.1 中文关键词

- `P0` · Locator `C12:508ab626:e1e3a126:100:edb98f49` · Lines `127-127`

```text
“必须、禁止、应、不应、可以、可选”直接适用 VC-PPG-COM-001 的规范性用语定义；唯一语义以该公共基线为准，本文件不得复制或改写。
```

### 5. C12 — C12 评审、质量门禁与产品健康规范 > 5. 规范性用语与受控判定 > 5.1 中文关键词

- `P0` · Locator `C12:508ab626:e1e3a126:101:6775b219` · Lines `129-129`

```text
“必须”和“禁止”规则不得通过普通 EWR 绕过。法律、监管、合同、Safety、Security、Privacy、不可逆数据和明确 Non-waivable Gate 项不得豁免。
```

### 6. C08 — C08 Agent 上下文治理规范 > 10. 强制规则 > 10.12 Attachment、Retrieval 与 Transformation

- `P0` · Locator `C08:262f2a19:a5c224ba:352:17878c15` · Lines `475-475`

```text
7. Summary 禁止替代 Normative Source；如用于辅助，必须标记 Derived、Coverage、Omission 和生成者。
```

### 7. C08 — C08 Agent 上下文治理规范 > 10. 强制规则 > 10.12 Attachment、Retrieval 与 Transformation

- `P0` · Locator `C08:262f2a19:a5c224ba:346:bfe312a1` · Lines `469-469`

```text
1. Attachment 必须记录文件名、媒体类型、大小、Source Owner、上传时间、Digest、Access 和用途。
```

### 8. C08 — C08 Agent 上下文治理规范 > 10. 强制规则 > 10.12 Attachment、Retrieval 与 Transformation

- `P0` · Locator `C08:262f2a19:a5c224ba:348:83b980eb` · Lines `471-471`

```text
3. OCR、Parser、Converter、Translator、Summarizer 和 Chunker 必须记录工具/版本、参数、输入、输出、范围、错误和遗漏。
```

### 9. C08 — C08 Agent 上下文治理规范 > 10. 强制规则 > 10.12 Attachment、Retrieval 与 Transformation

- `P0` · Locator `C08:262f2a19:a5c224ba:349:effe49e0` · Lines `472-472`

```text
4. Retrieval 必须记录 Query、Corpus/Index Snapshot、Filter、检索时间、候选、选择依据、未选项和 Source Locator。
```

### 10. C08 — C08 Agent 上下文治理规范 > 10. 强制规则 > 10.12 Attachment、Retrieval 与 Transformation

- `P0` · Locator `C08:262f2a19:a5c224ba:351:b8e85ec4` · Lines `474-474`

```text
6. Chunk 必须可定位回原 Source 范围；跨 Source 拼接必须保留每段 Provenance。
```

### 11. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 20. 附录：模板骨架、检查清单与示例 > 20.1 TaskContract 最小结构

- `P1` · Locator `VC-PPG-PRO-001:548a810a:2e556586:562:cb718e70` · Lines `757-817`

```text
### 20.1 TaskContract 最小结构

```json
{
  "schema_version": "6.3-candidate",
  "meta_type": "TaskContract",
  "project_id": "P-001",
  "work_item_id": "W-001",
  "task_id": "T-001",
  "ordinal": 1,
  "revision": 1,
  "lifecycle_state": "Ready",
  "created_at": "2026-08-15T00:00:00Z",
  "frozen_at": null,
  "depends_on": [],
  "supersedes": [],
  "blocked_by": [],
  "source_snapshot": {"snapshot": "<source-snapshot>"},
  "objective": "<期望结果>",
  "scope": {"in_scope": ["<scope>"], "out_of_scope": [], "allowed_paths": [], "forbidden_actions": []},
  "authority": {
    "execution_permissions": ["read", "edit-in-scope", "validate"], "required_gates": [], "stop_conditions": ["scope-expansion"],
    "authority_references": ["user:task-directive"],
    "authority_assessments": [{"reference": "user:task-directive", "source_kind": "UserDirective", "status": "Valid", "scope_refs": ["<scope>"], "evidence_refs": ["conversation:<task-id>:user-directive"], "verified_at": "2026-08-15T00:00:00Z", "expires_at": null}]
  },
  "acceptance": {"criteria": ["<criterion>"], "decision_owner": "task-initiator"},
  "plan": {"steps": ["inspect", "execute", "verify", "close"], "verification": ["<check>"], "rollback": ["<rollback>" ]},
  "task_profile": {
    "delivery_scenario": "DS-03",
    "development_types": ["DT-06"],
    "primary_development_type": "DT-06",
    "development_type_scopes": {"DT-06": ["defect correction scope"]},
    "change_surfaces": ["Agent/Collaboration"],
    "risk_level": "Medium",
    "extension_triggers": {"E01": "Inactive", "E02": "Inactive", "E03": "Inactive", "E04": "Inactive", "E05": "Inactive"},
    "extension_evidence_refs": {"E01": [], "E02": [], "E03": [], "E04": [], "E05": []},
    "baseline_inheritance": ["Revise"],
    "mode": "Normal",
    "confidence": "Medium",
    "basis": ["<basis>"],
    "open_questions": [],
    "applicability_facts": {
      "product_intent_change": "No", "initiative_scope_change": "No", "requirement_change": "No", "external_behavior_change": "No", "design_change": "No",
      "architecture_impact": "No", "security_privacy_impact": "No", "data_ai_impact": "No", "formal_knowledge_records": "No", "operations_impact": "No",
      "production_release": "No", "irreversible_change": "No", "actual_execution": "Yes", "authority_available": "Yes", "migration_retirement": "No",
      "external_system_effect": "No", "formal_review_or_gate": "Yes"
    }
  },
  "tailoring_resolution": {
    "rule_set_id": "VC-PPG-TAIL-001", "rule_set_version": "6.3 Candidate", "rule_set_status": "In Review",
    "rule_set_sha256": "<64-char-sha256>", "normative_sources_sha256": "<64-char-sha256>", "resolver_sha256": "<64-char-sha256>", "task_contract_schema_sha256": "<64-char-sha256>", "input_digest": "<64-char-sha256>", "stage": "S4",
    "applicable_standards": ["C02", "C04", "C05", "C07", "C08", "C09", "C10", "C11", "C12"],
    "pending_standards": [], "stage_context_standards": ["C02", "C05", "C07", "C08", "C09", "C10", "C11", "C12"],
    "control_strength": "standard", "independent_review": false, "explicit_human_gate": false, "blocking_reasons": [],
    "rule_ids": ["VC-PPG-TAIL-001:always_applicable"], "source_sections": [{"source_id": "VC-PPG-DEC-001", "path": "references/01_治理基线/Vibe_Coding_P2裁剪与扩展规范适用性决议_V6.3.md", "sections": ["9", "10", "11", "12", "13", "14", "15", "16", "17"]}],
    "complete_source_files": [
      {"source_id": "VC-PPG-COM-001", "path": "references/01_治理基线/Vibe_Coding_公共术语与规范性用语基线_V6.3.md", "sha256": "<64-char-sha256>"},
      {"source_id": "VC-PPG-COM-002", "path": "references/01_治理基线/Vibe_Coding_受控产物目录与状态模型_V6.3.md", "sha256": "<64-char-sha256>"},
      {"source_id": "VC-PPG-DEC-001", "path": "references/01_治理基线/Vibe_Coding_P2裁剪与扩展规范适用性决议_V6.3.md", "sha256": "<64-char-sha256>"},
      {"source_id": "VC-PPG-PRO-001", "path": "references/01_治理基线/Vibe_Coding_任务类型裁剪与统一执行流程规范_V6.3.md", "sha256": "<64-char-sha256>"},
      {"source_id": "VC-PPG-IDX-001", "path": "references/05_记录与登记册/V6.
```

### 12. C05 — C05 验收、验证与确认规范 > 10. 强制规则 > 10.15 Failure、Waiver、Risk Acceptance 与 Acceptance

- `P1` · Locator `C05:7973bcb4:8d60943e:337:23a84cb6` · Lines `492-492`

```text
2. Blocked 必须记录阻塞原因、解除条件、责任人和重新执行计划。
```

### 13. C08 — C08 Agent 上下文治理规范 > 15. 评审、批准与 Context Ready > 15.3 阻断条件

- `P1` · Locator `C08:262f2a19:d9fe4e7d:603:c387b145` · Lines `808-808`

```text
以下任一情况必须 Not Ready 或 Blocked：
```

### 14. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.8 Change Request 创建与分流

- `P1` · Locator `C11:88ec56f7:b4040cfb:361:5fcee191` · Lines `493-493`

```text
5. 未知范围、无 Owner、无原状态或无法识别资产的 CHG 必须 `Blocked`；
```

### 15. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.8 Change Request 创建与分流

- `P1` · Locator `C11:88ec56f7:b4040cfb:358:a384ae80` · Lines `490-490`

```text
2. `Pre-authorized Standard`：必须已有 Approved 变更模型、范围、步骤、验证、回滚和 Authority；超出任一边界立即转 Normal；
```

### 16. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.8 Change Request 创建与分流

- `P1` · Locator `C11:88ec56f7:b4040cfb:362:aaee730d` · Lines `494-494`

```text
6. 发现实际变化先于 CHG 时，必须创建 C10 UCR 并按 Risk 决定 Stop、隔离、回滚或追认；追认不消除违规事实。
```

### 17. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.8 Change Request 创建与分流

- `P1` · Locator `C11:88ec56f7:b4040cfb:360:9db49fbe` · Lines `492-492`

```text
4. CHG 重复时不得删除，必须连接主 CHG 并进入 `Cancelled` 或 `Closed`；
```

### 18. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.8 Change Request 创建与分流

- `P1` · Locator `C11:88ec56f7:b4040cfb:345:e7515c1d` · Lines `474-474`

```text
CHG 创建时必须记录：
```

### 19. C11 — C11 配置、版本、基线与变更控制规范 > 15. 评审、批准与阻断 > 15.5 强制阻断

- `P2` · Locator `C11:88ec56f7:fe00db08:858:eb69a307` · Lines `1142-1142`

```text
### 15.5 强制阻断
```

### 20. C05 — C05 验收、验证与确认规范 > 15. 验证与符合性检查 > 15.2 人工评审

- `P2` · Locator `C05:7973bcb4:3ba2597e:584:70d82a2f` · Lines `806-806`

```text
### 15.2 人工评审
```

### 21. C05 — C05 验收、验证与确认规范 > 15. 验证与符合性检查 > 15.1 自动检查

- `P2` · Locator `C05:7973bcb4:9bd38ad1:559:736da9bb` · Lines `777-777`

```text
### 15.1 自动检查
```

### 22. C05 — C05 验收、验证与确认规范 > 15. 验证与符合性检查 > 15.4 符合性声明限制

- `P2` · Locator `C05:7973bcb4:f2ab898a:618:50104d48` · Lines `846-846`

```text
### 15.4 符合性声明限制
```

### 23. C11 — C11 配置、版本、基线与变更控制规范 > 15. 评审、批准与阻断 > 15.1 Configuration Ready

- `P2` · Locator `C11:88ec56f7:374f754a:813:fc86d3f6` · Lines `1085-1085`

```text
### 15.1 Configuration Ready
```

### 24. C11 — C11 配置、版本、基线与变更控制规范 > 15. 评审、批准与阻断 > 15.3 Baseline Ready

- `P2` · Locator `C11:88ec56f7:5a31c640:837:da9eb9fc` · Lines `1115-1115`

```text
### 15.3 Baseline Ready
```

### 25. C11 — C11 配置、版本、基线与变更控制规范 > 15. 评审、批准与阻断 > 15.2 Change Ready

- `P2` · Locator `C11:88ec56f7:65b372a0:825:e03fffbf` · Lines `1100-1100`

```text
### 15.2 Change Ready
```

### 26. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 15. 验证与符合性检查 > 15.3 验收就绪检查

- `P2` · Locator `VC-PPG-PRO-001:548a810a:a1c5c618:453:b611a4eb` · Lines `616-616`

```text
### 15.3 验收就绪检查
```

### 27. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 15. 验证与符合性检查 > 15.1 流程就绪检查

- `P2` · Locator `VC-PPG-PRO-001:548a810a:d9098f34:436:6a22e459` · Lines `593-593`

```text
### 15.1 流程就绪检查
```

### 28. C08 — C08 Agent 上下文治理规范 > 15. 评审、批准与 Context Ready > 15.1 评审顺序

- `P3` · Locator `C08:262f2a19:c6896026:578:e0753658` · Lines `776-776`

```text
### 15.1 评审顺序
```

### 29. C08 — C08 Agent 上下文治理规范 > 15. 评审、批准与 Context Ready > 15.2 Context Ready 条件

- `P3` · Locator `C08:262f2a19:a2a36228:588:f629e36d` · Lines `788-788`

```text
### 15.2 Context Ready 条件
```

### 30. C08 — C08 Agent 上下文治理规范 > 15. 评审、批准与 Context Ready > 15.3 阻断条件

- `P3` · Locator `C08:262f2a19:d9fe4e7d:602:2e1a5c0c` · Lines `806-806`

```text
### 15.3 阻断条件
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
