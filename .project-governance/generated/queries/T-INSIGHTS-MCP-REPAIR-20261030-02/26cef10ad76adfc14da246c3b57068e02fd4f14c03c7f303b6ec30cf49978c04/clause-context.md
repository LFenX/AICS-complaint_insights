# Clause Context: T-INSIGHTS-MCP-REPAIR-20261030-02 / edit_in_scope

- Status: `Expanded`
- Query digest: `26cef10ad76adfc14da246c3b57068e02fd4f14c03c7f303b6ec30cf49978c04`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `6/6`
- Budget: `21781/12000` chars
- Fallback: `section`

## Source Index

- `C09`: `references/02_核心规范/C09_Agent_Execution_and_Evidence_Standard.md` / `V6.3 Candidate` / SHA-256 `6897694e362bf48cb3a13bb4e68d79d7173945daad2ba3e8f0b6c75be944c01e`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `E03`: `references/03_扩展规范/E03_Data_and_AI_Data_Governance_Extension_Standard.md` / `V6.3 Candidate` / SHA-256 `bb6a10422c6e672f3f67e6dc109c5bfaa594b195924758b21911fe44a18c603b`
- `VC-PPG-PRO-001`: `references/01_治理基线/Vibe_Coding_任务类型裁剪与统一执行流程规范_V6.3.md` / `V6.3 Candidate` / SHA-256 `548a810a1cbce4fc7970f87778c71f56c9d0921e3ba385a73d085b8ed0276329`
- `C11`: `references/02_核心规范/C11_Configuration_Version_Baseline_and_Change_Standard.md` / `V6.3 Candidate` / SHA-256 `88ec56f78f6d3da6f94b1684c7b1296ed1825bfcc961f0f8d3636c8c6a26f7e1`

> 完整 lane rank 和逐条来源字段保存在同目录 `query-result.json`。

## Citations

### 1. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:322:d81d2e63` · Lines `434-434`

```text
1. Delete、Deploy、External Mutation、生产操作、权限变化、不可逆操作和 High/Critical Risk Action 至少为 Approval Required；Prohibited 仍禁止。
```

### 2. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:325:f5a1c28d` · Lines `437-437`

```text
4. 执行前必须记录 Before Snapshot、影响范围、可恢复性、备份/回滚、幂等策略、观察窗口和验证。
```

### 3. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:327:c4bf94d5` · Lines `439-439`

```text
6. Deploy 必须引用 C11 Release Configuration、C12 Gate/Approval、窗口、监测、回滚和 Owner。
```

### 4. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:328:befa9592` · Lines `440-440`

```text
7. “清理”“修复”“格式化”“回滚”“恢复”不得扩大批准目标。
```

### 5. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:329:48963d8d` · Lines `441-441`

```text
8. Retry 高影响 Action 前必须先确认上次 Attempt 的外部副作用和幂等状态。
```

### 6. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:331:0e9a1176` · Lines `443-443`

```text
10. 操作后必须验证 Actual Effect；只有命令成功但目标状态未知时为 Blocked。
```

### 7. C12 — C12 评审、质量门禁与产品健康规范 > 2. 目的

- `P0` · Locator `C12:508ab626:28e7276d:36:af7a1d0d` · Lines `45-45`

```text
10. 使 Agent 和自动化工具可以计算、检查和起草，但不能自批高风险输出或风险接受；
```

### 8. C12 — C12 评审、质量门禁与产品健康规范 > 5. 规范性用语与受控判定 > 5.1 中文关键词

- `P0` · Locator `C12:508ab626:e1e3a126:100:edb98f49` · Lines `127-127`

```text
“必须、禁止、应、不应、可以、可选”直接适用 VC-PPG-COM-001 的规范性用语定义；唯一语义以该公共基线为准，本文件不得复制或改写。
```

### 9. C12 — C12 评审、质量门禁与产品健康规范 > 5. 规范性用语与受控判定 > 5.1 中文关键词

- `P0` · Locator `C12:508ab626:e1e3a126:101:6775b219` · Lines `129-129`

```text
“必须”和“禁止”规则不得通过普通 EWR 绕过。法律、监管、合同、Safety、Security、Privacy、不可逆数据和明确 Non-waivable Gate 项不得豁免。
```

### 10. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:323:8502f895` · Lines `435-435`

```text
2. 目标必须解析为精确仓库、路径、资源、记录、租户、账户、环境和版本。
```

### 11. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:324:2a399565` · Lines `436-436`

```text
3. 工作区根、用户主目录、系统根、整个账户/租户、未解析变量、宽泛通配符或计算后未复核目标禁止作为破坏性 Target。
```

### 12. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:326:32ce4083` · Lines `438-438`

```text
5. External Mutation 必须使用服务支持的 Idempotency Key 或记录不可幂等及补偿措施。
```

### 13. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:330:7404e213` · Lines `442-442`

```text
9. 删除或覆盖前必须识别用户已有、未提交、未跟踪和并行 Agent 变化；未知时 Stop。
```

### 14. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:252:8841a1d9` · Lines `319-319`

```text
- 擅自运行全表扫描、生产写入、回填、重标注、匿名化或删除；
```

### 15. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:159:b3346062` · Lines `203-203`

```text
3. 空值禁止代替 Unknown、Not Applicable 或 Not Evaluated；
```

### 16. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:160:c7dfbc1b` · Lines `204-204`

```text
4. 未知的许可、Privacy、Security 或 Legal Hold 禁止由 Agent 推断；
```

### 17. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:161:22992d0f` · Lines `205-205`

```text
5. 未知阈值禁止由 Tool Default、行业惯例或任意百分比填充；
```

### 18. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:162:a8c014d8` · Lines `206-206`

```text
6. 未知 Consumer 禁止批准 Breaking Change；
```

### 19. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:163:bc86dfc6` · Lines `207-207`

```text
7. 未知 Dataset Revision 禁止作为训练、测试、RAG 或 Gate 输入。
```

### 20. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:249:f851c872` · Lines `315-315`

```text
Agent 禁止：
```

### 21. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:157:6b0fd6e7` · Lines `201-201`

```text
1. 字段不适用时必须记录理由、Scope、依据和批准人；
```

### 22. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:158:ddd9f24f` · Lines `202-202`

```text
2. 未知来源、许可、数据主体、Schema、Owner、阈值、Consumer、Lineage 或 Retention 必须显式标为 Pending/Unknown；
```

### 23. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:242:958d7c5d` · Lines `306-306`

```text
Agent 可以：
```

### 24. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:253:70be0f3c` · Lines `320-320`

```text
- 推断未知许可、法律权属、PII 合法性或跨境允许性；
```

### 25. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 20. 附录：模板骨架、检查清单与示例 > 20.1 TaskContract 最小结构

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

### 26. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.6 Tool 与权限

- `P1` · Locator `C09:6897694e:d3202194:293:71561ebf` · Lines `398-398`

```text
5. 未知版本、未知 Identity、未知租户、未知数据保留或未知副作用的 Tool 不得用于高风险 Action。
```

### 27. C11 — C11 配置、版本、基线与变更控制规范 > 8. 正式产物与唯一事实源 > 8.0 V6.3 三阶段修订与生成边界

- `P1` · Locator `C11:88ec56f7:0c539819:172:3b2cf7dd` · Lines `227-227`

```text
RunLedger 只追加；更正通过新 Event 引用原 Event。ProjectState 和 DerivedView 由生成器重建，禁止直接编辑或纳入独立变更源。Git Commit/Diff 可作为代码和文档变化的权威证据，但外部副作用、失败、验证环境、批准和决定必须由相应元类型或 AuthorityAsset 保存。
```

### 28. C09 — C09 Agent 执行与证据规范 > 9. 生命周期与工作机制 > 9.7 Failure、Retry 与 Rollback

- `P2` · Locator `C09:6897694e:00fcee58:229:a4dd6a88` · Lines `313-313`

```text
任一 Failed/Blocked、非预期副作用、Stop、验证失败或证据缺失必须建立 FER。Retry 或 Rollback 只能在副作用、权限、Plan、风险和新鲜 Context 可判定时执行。
```

### 29. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 10. 强制规则 > 10.18 确定性裁剪解析

- `P2` · Locator `VC-PPG-PRO-001:548a810a:1542a080:317:96557369` · Lines `429-429`

```text
7. `authority_available=Yes` 必须具有 Authority 引用，且每个引用必须绑定结构化 `authority_assessments`。只有所有评估状态均为 `Valid`、验证时间不在未来、未过期、Evidence 非空且作用域精确覆盖全部 `scope.in_scope` 才允许 S4 就绪。`execution_permissions` 只使用 `read / edit-in-scope / validate / external-effect / rollback`；Fact 触发所需权限必须在 S4 齐备，每个 Run Event 还必须在写入时再校验对应权限。High/Critical 必须计划 `independent-review`，Critical 还必须计划 `human-acceptance`；安全/隐私、生产发布和不可逆变化分别要求 `security-privacy-review`、`release-approval` 和 `irreversible-change-approval`。
```

### 30. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:770:ff3aba72` · Lines `1018-1018`

```text
18. Tool 默认行为、缓存、重试和副作用是否可知；
```

### 31. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:793:27098503` · Lines `1041-1041`

```text
41. Retry 是否创建新 Attempt 并检查副作用/幂等；
```

### 32. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.9 Impact Analysis

- `P2` · Locator `C11:88ec56f7:2470b427:382:c81a8d3c` · Lines `519-519`

```text
5. 数据删除、Schema 迁移、密钥轮换、模型变化和 Feature Flag 必须评估不可逆副作用；
```

### 33. C09 — C09 Agent 执行与证据规范 > 14. 质量要求

- `P2` · Locator `C09:6897694e:0d3fa301:617:e3bea0af` · Lines `815-815`

```text
6. 原子：副作用、权限和失败不可分时拆分 Action/TIL；
```

### 34. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.2 执行中记录：RunLedger

- `P2` · Locator `VC-PPG-PRO-001:548a810a:5963b45f:129:aeb0771f` · Lines `167-167`

```text
- 外部副作用；
```

### 35. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.5 Step、Action 与 Attempt

- `P2` · Locator `C09:6897694e:e40e94e8:281:25e39cb3` · Lines `384-384`

```text
2. 每个 Action 只承担一个可独立判定授权、副作用和结果的 Operation。
```

### 36. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:806:76d821d4` · Lines `1054-1054`

```text
54. 是否能重建主要副作用、TaskContract Revision、Diff 和验证；
```

### 37. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.3 RUN Completed 条件

- `P2` · Locator `C09:6897694e:4d4144f4:659:92f7e6dd` · Lines `866-866`

```text
- 未发生未记录副作用或 Evidence 缺口。
```

### 38. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.7 命令规范

- `P2` · Locator `C09:6897694e:824cdbf7:317:d95f8e3a` · Lines `427-427`

```text
6. 复合命令若任一部分具有副作用、独立权限或独立失败条件，必须拆分 Action/TIL。
```

### 39. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.13 Failure、Stop 与 Retry

- `P2` · Locator `C09:6897694e:7c53d277:379:a3f5a43c` · Lines `501-501`

```text
7. 非幂等或副作用未知的 Action 禁止自动 Retry。
```

### 40. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.0 V6.3 最小执行记录覆盖规则

- `P2` · Locator `C09:6897694e:b1dd146f:139:d80c7578` · Lines `189-189`

```text
2. RUN 与 TIL 语义进入只追加 RunLedger（`run.jsonl`）。普通读取、目录查看、搜索和未产生重要结果的无副作用调用不记录。
```

### 41. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 13. 三阶段记录必填信息 > 13.3 RunLedger / run.jsonl

- `P2` · Locator `VC-PPG-PRO-001:548a810a:1fd4e52a:408:9938b1fa` · Lines `554-554`

```text
- 适用的 exit_code、Evidence/Git 引用和外部副作用；
```

### 42. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.7 命令规范

- `P2` · Locator `C09:6897694e:824cdbf7:320:956657f2` · Lines `430-430`

```text
9. 命令可重放记录不构成再次执行授权；重放前必须重新核验 Authorization、Context、Snapshot、Risk 和副作用。
```

### 43. C11 — C11 配置、版本、基线与变更控制规范 > 6. 术语与定义

- `P2` · Locator `C11:88ec56f7:7b574ff8:135:f0d09366` · Lines `178-178`

```text
| Rollback | 将当前系统或资产变更到一个先前已知配置的受控变更；不保证外部副作用或数据自动恢复 |
```

### 44. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.6 Tool 与权限

- `P2` · Locator `C09:6897694e:d3202194:292:80041ed7` · Lines `397-397`

```text
4. Tool 自动重试、缓存、会话记忆、插件、扩展、默认工作目录和外部副作用必须可知。
```

### 45. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.13 Failure、Stop 与 Retry

- `P2` · Locator `C09:6897694e:7c53d277:377:47c6c8f5` · Lines `499-499`

```text
5. Retry 必须创建新 Attempt，记录原因、变化参数、修正、授权、幂等/副作用检查和结果。
```

### 46. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.6 Tool 与权限

- `P2` · Locator `C09:6897694e:d3202194:294:1da2eb1f` · Lines `399-399`

```text
6. Dry Run 只有在工具官方语义明确且未产生真实副作用时才能记录为 Dry Run；名称包含 `dry-run` 不构成证明。
```

### 47. C09 — C09 Agent 执行与证据规范 > 13. 必填信息 > 13.8 Failure or Exception Report

- `P2` · Locator `C09:6897694e:4e9aa10b:579:c2c77abc` · Lines `768-768`

```text
- 已发生副作用、Risk ID/Current Risk Level/Impact、Stop/STC/ESP；
```

### 48. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.5 阻断条件

- `P2` · Locator `C09:6897694e:434e9ab2:676:d20470e2` · Lines `890-890`

```text
- 破坏性/外部操作使用宽泛目标、未解析变量或未知副作用；
```

### 49. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.5 Step、Action 与 Attempt

- `P2` · Locator `C09:6897694e:e40e94e8:285:b1b8d8df` · Lines `388-388`

```text
6. Cancelled 必须记录取消 Authority、时间、已发生副作用和安全状态。
```

### 50. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.5 阻断条件

- `P2` · Locator `C09:6897694e:434e9ab2:683:62a587fd` · Lines `897-897`

```text
- 无法重建主要副作用、TaskContract Revision 或 End Snapshot。
```

### 51. C09 — C09 Agent 执行与证据规范 > 2. 目的

- `P2` · Locator `C09:6897694e:cd365db2:28:3dc3dc43` · Lines `37-37`

```text
3. 使会改变状态、失败、验证、产生外部副作用或影响门禁的 Tool Invocation 可追踪，同时避免记录低价值读取和敏感原文；
```

### 52. C11 — C11 配置、版本、基线与变更控制规范 > 19. P2 强制检查

- `P2` · Locator `C11:88ec56f7:40ea1806:1028:270e8ada` · Lines `1355-1355`

```text
| C11-P2-058 | Rollback 已验证 | 覆盖数据和外部副作用 |
```

### 53. C09 — C09 Agent 执行与证据规范 > 20. 附录 > 20.13 Retry 与 Rollback 判定表

- `P2` · Locator `C09:6897694e:e0e42fcb:848:70ea76c0` · Lines `1314-1314`

```text
| 幂等、无副作用、参数不变、授权有效 | 按 AEP 新 Attempt | 不需要 | 保留原失败 |
```

### 54. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.18 恢复与回滚

- `P2` · Locator `C11:88ec56f7:a8bfc8c2:521:6ef0c5b9` · Lines `693-693`

```text
4. Rollback 必须记录目标版本、实际动作、数据影响、外部副作用和验证；
```

### 55. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.0 V6.3 最小执行记录覆盖规则

- `P2` · Locator `C09:6897694e:b1dd146f:145:abf147f6` · Lines `195-195`

```text
8. 默认只保存结构化摘要、时间、状态、Exit Code、Evidence 引用、外部副作用和脱敏说明。只有复核无法通过其他证据完成时，才把完整命令或原始输出作为受控 Evidence 保存。
```

### 56. C09 — C09 Agent 执行与证据规范 > 20. 附录 > 20.13 Retry 与 Rollback 判定表

- `P2` · Locator `C09:6897694e:e0e42fcb:849:001e668c` · Lines `1315-1315`

```text
| 副作用未知或外部状态未知 | 禁止自动 Retry | 先诊断 | FER、Stop |
```

### 57. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:101:726215f4` · Lines `142-142`

```text
| Action | Step 内一次受授权 Operation，具有精确目标、输入、预期副作用和结果 | 一次 Action 可以产生一个 Tool Invocation；不可审计复合动作必须拆分 |
```

### 58. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.13 Failure、Stop 与 Retry

- `P2` · Locator `C09:6897694e:7c53d277:374:6e5e65e7` · Lines `496-496`

```text
2. FER 必须记录失败时间/步骤、症状、Error Evidence、影响、已发生副作用、即时处置、根因状态、升级和关闭条件。
```

### 59. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.2 执行中记录：RunLedger

- `P2` · Locator `VC-PPG-PRO-001:548a810a:5963b45f:131:853657b7` · Lines `170-170`

```text
RunLedger 保存结构化摘要、时间、状态、结果码、Evidence 引用、副作用和脱敏说明；禁止默认保存完整命令输出、文件内容、凭据、Token 或其他敏感值。普通读取、目录查看和搜索不记录。Git Commit/Diff 作为变化证据引用，不要求在账本复制 Diff。
```

### 60. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 17. 裁剪规则 > 17.3 禁止裁剪方式

- `P2` · Locator `VC-PPG-PRO-001:548a810a:427e57cc:524:2c59919c` · Lines `708-708`

```text
- 用聊天、工单或工具成功替代正式 Evidence 和 Decision；Git 可以作为代码/文档 Diff 证据，但不能替代外部副作用、失败、验证环境、Approval 或 Decision 记录；
```

### 61. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 6. 术语与定义

- `P2` · Locator `VC-PPG-PRO-001:548a810a:8c711bde:79:ddd77a56` · Lines `104-104`

```text
| RunLedger | 只追加记录变更、失败、验证、外部副作用、门禁和回滚的重要事件 | 不记录普通读取、搜索和可由 Git 低成本重建的信息 |
```

### 62. C09 — C09 Agent 执行与证据规范 > 12. V6.3 必需载体与条件 Profile

- `P2` · Locator `C09:6897694e:0a9756f4:488:e528a9f5` · Lines `652-652`

```text
| RunLedger / `run.jsonl` | 每个实际 Run；无事件时允许空文件 | RUN、重要 TIL、失败、重试、验证、外部副作用和回滚事件 |
```

### 63. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 12. 最小物理产物与条件 Profile > 12.2 条件产物

- `P2` · Locator `VC-PPG-PRO-001:548a810a:7865df37:360:3a982009` · Lines `495-495`

```text
| 实际 Tool Invocation | 普通读取和搜索不记录；变更、失败、重试、验证、外部副作用、人工门禁和回滚追加到 RunLedger；超时、取消、非零退出、未知状态和部分返回不得省略 |
```

### 64. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.13 Failure、Stop 与 Retry

- `P2` · Locator `C09:6897694e:7c53d277:373:bc060034` · Lines `495-495`

```text
1. 以下任一情况必须创建 FER：Failed/Blocked Step、Tool/Command Error、Validation Fail/Blocked、Stop Trigger、非预期副作用、证据丢失、Retry、Rollback 或敏感暴露。
```

### 65. C09 — C09 Agent 执行与证据规范 > 9. 生命周期与工作机制 > 9.5 AEP 与 RUN Ready

- `P2` · Locator `C09:6897694e:02e65cf9:215:e37635a1` · Lines `294-294`

```text
AEP 将理解摘要转换为有序 Step、Action、Tool、Command/Invocation、预期副作用、验证、回滚、批准点和 Stop。AEP 达到 Approved/Baselined 且全部 Preflight 通过后，RUN 可以从 Planned 转为 Ready。
```

### 66. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 12. 最小物理产物与条件 Profile > 12.1 所有任务的最低集合

- `P2` · Locator `VC-PPG-PRO-001:548a810a:73fc5ef5:350:d9ff0ecd` · Lines `479-479`

```text
| 执行中 | RunLedger / `run.jsonl` | RunID、AttemptID、顺序、重要事件、失败/重试、验证、外部副作用、Evidence 和 Git 引用；无执行动作时允许空账本 |
```

### 67. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.9 Tool Invocation Log

- `P2` · Locator `C09:6897694e:89ce8493:335:5719ca20` · Lines `449-449`

```text
3. Event 的必需字段以 VC-PPG-PRO-001 §13.3 和 `run-event.schema.json` 为准：Run/Attempt、Sequence、Time、Event Type、Summary、Status、Exit Code、Evidence References、Side Effects 和 Redactions。Tool/操作类别、Permission、Input/Output Summary 与 Actual Effect 只在解释重要事件、权限边界或副作用所必需时进入 Summary、Evidence 或外置 Raw Log，不为普通调用强制扩展账本字段。
```

### 68. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 9. 生命周期或工作机制 > 9.1 统一八阶段主流程

- `P2` · Locator `VC-PPG-PRO-001:548a810a:3151121b:165:13a83867` · Lines `231-231`

```text
| S5 执行 | TaskContract 已冻结；计划与权限有效；当前裁剪快照无 blocker | Agent 或人工实施按最小 RunLedger 执行；Git 保存代码/文档 Diff，RunLedger 保存变化摘要、失败、重试、验证、外部副作用和 Evidence 引用 | 计划动作完成或触发 Stop；Actual 与 Planned Change 已比较；账本顺序连续 |
```

### 69. C09 — C09 Agent 执行与证据规范 > 20. 附录 > 20.15 正反例

- `P2` · Locator `C09:6897694e:517bf4ca:858:2e82b2de` · Lines `1348-1348`

```text
> RUN-0043 绑定 AEP-0043 Revision 2、REQ-031 Revision 4、ECP-0043 Revision 3、Commit `abc123` 和 ARD/APM 当前授权。Action RUN-0043-A003 使用 TIL-0187 记录参数化测试调用、工作目录、超时、Exit Code、stdout/stderr Digest 和实际结果。第一次 Attempt 因依赖超时失败，FER-0012 保留；确认无外部副作用后按 AEP 执行第二次 Attempt。CAS/CCS 固定 Diff 和 Result Commit；VDR 逐项记录 Expected/Actual，HRR 由独立人类基于当前 Revision 接受，未解决低 Risk 进入 RRS。
```

### 70. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.16 Drift 与无来源变化

- `P2` · Locator `C11:88ec56f7:b6b18321:505:3563c097` · Lines `673-673`

```text
6. 自动 Drift Remediation 只在预授权范围内执行，超界必须停止。
```

### 71. C11 — C11 配置、版本、基线与变更控制规范 > 6. 术语与定义

- `P2` · Locator `C11:88ec56f7:7b574ff8:133:3008f216` · Lines `176-176`

```text
| Retirement | 资产停止在指定范围内使用并进入受控保留或处置状态 |
```

### 72. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.20 Coding Agent 与自动化边界

- `P2` · Locator `C11:88ec56f7:12b8f4f0:552:5c3fc816` · Lines `733-733`

```text
- 在 C07 Authorization 与 C09 Run 范围内执行版本、快照、构建、迁移和回滚命令；
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
