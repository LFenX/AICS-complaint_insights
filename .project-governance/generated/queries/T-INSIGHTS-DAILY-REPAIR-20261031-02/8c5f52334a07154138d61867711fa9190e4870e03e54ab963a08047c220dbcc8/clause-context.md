# Clause Context: T-INSIGHTS-DAILY-REPAIR-20261031-02 / close_task

- Status: `Expanded`
- Query digest: `8c5f52334a07154138d61867711fa9190e4870e03e54ab963a08047c220dbcc8`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `9/9`
- Budget: `21819/12000` chars
- Fallback: `section`

## Source Index

- `C08`: `references/02_核心规范/C08_Agent_Context_Governance_Standard.md` / `V6.3 Candidate` / SHA-256 `262f2a190f130cb97955e58fca57d2216e2edf949d2f271413e5dff5d6faeb6d`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `VC-PPG-PRO-001`: `references/01_治理基线/Vibe_Coding_任务类型裁剪与统一执行流程规范_V6.3.md` / `V6.3 Candidate` / SHA-256 `548a810a1cbce4fc7970f87778c71f56c9d0921e3ba385a73d085b8ed0276329`
- `C05`: `references/02_核心规范/C05_Acceptance_Verification_and_Validation_Standard.md` / `V6.3 Candidate` / SHA-256 `7973bcb4ea442030772e36b7418cc1e03f55e0b3aaa6072f4ec1c198d1b537c7`
- `E03`: `references/03_扩展规范/E03_Data_and_AI_Data_Governance_Extension_Standard.md` / `V6.3 Candidate` / SHA-256 `bb6a10422c6e672f3f67e6dc109c5bfaa594b195924758b21911fe44a18c603b`
- `C11`: `references/02_核心规范/C11_Configuration_Version_Baseline_and_Change_Standard.md` / `V6.3 Candidate` / SHA-256 `88ec56f78f6d3da6f94b1684c7b1296ed1825bfcc961f0f8d3636c8c6a26f7e1`
- `C09`: `references/02_核心规范/C09_Agent_Execution_and_Evidence_Standard.md` / `V6.3 Candidate` / SHA-256 `6897694e362bf48cb3a13bb4e68d79d7173945daad2ba3e8f0b6c75be944c01e`

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

### 11. C08 — C08 Agent 上下文治理规范 > 3. 适用范围

- `P1` · Locator `C08:262f2a19:2f2b733f:37:0a3b05f7` · Lines `49-49`

```text
- 当前 Task、工作区 Snapshot、工具结果、验证结果、临时 Assumption 和对话内容进入 Execution Context；
```

### 12. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 20. 附录：模板骨架、检查清单与示例 > 20.3 TaskOutcome 最小结构

- `P1` · Locator `VC-PPG-PRO-001:548a810a:e4b9133c:565:d19eac19` · Lines `853-881`

```text
### 20.3 TaskOutcome 最小结构

```json
{
  "schema_version": "6.3-candidate",
  "meta_type": "TaskOutcome",
  "project_id": "P-001",
  "work_item_id": "W-001",
  "task_id": "T-001",
  "revision": 1,
  "status": "Implemented",
  "completed_at": "2026-08-15T00:00:00Z",
  "source_snapshot": {"snapshot": "<result-snapshot>"},
  "established_facts": ["<established-fact>"],
  "actual_changes": ["<actual-change>"],
  "verification": [{"summary": "<check>", "result": "Passed", "evidence_refs": ["<evidence-ref>"], "required": true}],
  "incomplete_items": [],
  "legacy_issues": [],
  "decisions": [],
  "evidence_refs": [],
  "next_tasks": [],
  "artifact_manifest": [
    {"meta_type": "TaskContract", "legacy_kind": null, "action": "Create/Revise", "asset_id": "T-001-before", "content_ref": ".project-governance/tasks/T-001/before.json", "reason": "freeze execution input", "rule_reference": "VC-PPG-PRO-001 §8.1", "owner": "task-initiator", "source_snapshot": "<source-snapshot>", "human_confirmation_refs": [], "outcome": "Revised"},
    {"meta_type": "RunLedger", "legacy_kind": null, "action": "Create/Revise", "asset_id": "T-001-run", "content_ref": ".project-governance/tasks/T-001/run.jsonl", "reason": "record material execution events", "rule_reference": "VC-PPG-PRO-001 §8.2", "owner": "execution-agent", "source_snapshot": "<source-snapshot>", "human_confirmation_refs": [], "outcome": "Revised"},
    {"meta_type": "TaskOutcome", "legacy_kind": null, "action": "Create/Revise", "asset_id": "T-001-after", "content_ref": ".project-governance/tasks/T-001/after.json", "reason": "record terminal facts and residue", "rule_reference": "VC-PPG-PRO-001 §8.3", "owner": "task-initiator", "source_snapshot": "<source-snapshot>", "human_confirmation_refs": [], "outcome": "Created"}
  ],
  "amendments": []
}
```
```

### 13. C05 — C05 验收、验证与确认规范 > 10. 强制规则 > 10.3 Acceptance Criterion 表达

- `P1` · Locator `C05:7973bcb4:dfa671f3:207:50db7fe9` · Lines `333-333`

```text
1. Given 必须可建立和核验，不得包含待验证结果；
```

### 14. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:159:b3346062` · Lines `203-203`

```text
3. 空值禁止代替 Unknown、Not Applicable 或 Not Evaluated；
```

### 15. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.8 Change Request 创建与分流

- `P1` · Locator `C11:88ec56f7:b4040cfb:362:aaee730d` · Lines `494-494`

```text
6. 发现实际变化先于 CHG 时，必须创建 C10 UCR 并按 Risk 决定 Stop、隔离、回滚或追认；追认不消除违规事实。
```

### 16. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:158:ddd9f24f` · Lines `202-202`

```text
2. 未知来源、许可、数据主体、Schema、Owner、阈值、Consumer、Lineage 或 Retention 必须显式标为 Pending/Unknown；
```

### 17. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.8 Change Request 创建与分流

- `P1` · Locator `C11:88ec56f7:b4040cfb:360:9db49fbe` · Lines `492-492`

```text
4. CHG 重复时不得删除，必须连接主 CHG 并进入 `Cancelled` 或 `Closed`；
```

### 18. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:160:c7dfbc1b` · Lines `204-204`

```text
4. 未知的许可、Privacy、Security 或 Legal Hold 禁止由 Agent 推断；
```

### 19. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:161:22992d0f` · Lines `205-205`

```text
5. 未知阈值禁止由 Tool Default、行业惯例或任意百分比填充；
```

### 20. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:162:a8c014d8` · Lines `206-206`

```text
6. 未知 Consumer 禁止批准 Breaking Change；
```

### 21. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:163:bc86dfc6` · Lines `207-207`

```text
7. 未知 Dataset Revision 禁止作为训练、测试、RAG 或 Gate 输入。
```

### 22. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:249:f851c872` · Lines `315-315`

```text
Agent 禁止：
```

### 23. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.8 Change Request 创建与分流

- `P1` · Locator `C11:88ec56f7:b4040cfb:345:e7515c1d` · Lines `474-474`

```text
CHG 创建时必须记录：
```

### 24. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.8 Change Request 创建与分流

- `P1` · Locator `C11:88ec56f7:b4040cfb:358:a384ae80` · Lines `490-490`

```text
2. `Pre-authorized Standard`：必须已有 Approved 变更模型、范围、步骤、验证、回滚和 Authority；超出任一边界立即转 Normal；
```

### 25. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.8 Change Request 创建与分流

- `P1` · Locator `C11:88ec56f7:b4040cfb:361:5fcee191` · Lines `493-493`

```text
5. 未知范围、无 Owner、无原状态或无法识别资产的 CHG 必须 `Blocked`；
```

### 26. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:157:6b0fd6e7` · Lines `201-201`

```text
1. 字段不适用时必须记录理由、Scope、依据和批准人；
```

### 27. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:242:958d7c5d` · Lines `306-306`

```text
Agent 可以：
```

### 28. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:253:70be0f3c` · Lines `320-320`

```text
- 推断未知许可、法律权属、PII 合法性或跨境允许性；
```

### 29. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:246:67a8b9f4` · Lines `311-311`

```text
- 汇总公开或已授权 Evidence；
```

### 30. C09 — C09 Agent 执行与证据规范 > 17. P2 裁剪与扩展适用性 > 17.0 Task Profile 驱动的适用性

- `P1` · Locator `C09:6897694e:39226036:716:28b946f8` · Lines `946-946`

```text
TaskOutcome 是任务级实际变化和遗留问题的事实源；存在代码变化时记录 CCS 兼容语义并引用 Git Diff。VDR 按 Run 汇总 VER/VAE、RunLedger 和 Git，仅作为 `Derived View / On Demand`，不得替代原始 Evidence。
```

### 31. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 6. 术语与定义

- `P2` · Locator `VC-PPG-PRO-001:548a810a:8c711bde:80:f39bc533` · Lines `105-105`

```text
| TaskOutcome | 记录已成立事实、实际变化、验证、未完成项、遗留问题和后续任务的终态对象 | 不保存执行前指令，不替代项目级 ProjectState |
```

### 32. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 9. 生命周期或工作机制 > 9.1 统一八阶段主流程

- `P2` · Locator `VC-PPG-PRO-001:548a810a:3151121b:168:d332662e` · Lines `234-234`

```text
| S8 收尾 | 当前交付不再继续执行 | 形成 TaskOutcome，更新终态 Artifact Manifest、Trace、Change、遗留问题和后继项；重建 ProjectState 和派生审核视图 | 结果为 Implemented、Deferred、Cancelled、Blocked 或 Superseded；事实、Owner、理由和 Evidence 完整 |
```

### 33. C09 — C09 Agent 执行与证据规范 > 12. V6.3 必需载体与条件 Profile

- `P2` · Locator `C09:6897694e:0a9756f4:489:490a3cdd` · Lines `653-653`

```text
| TaskOutcome / `after.json` | 每个结束任务 | CAS、CCS、FER、实际变化、验证、未完成项和遗留问题 |
```

### 34. C11 — C11 配置、版本、基线与变更控制规范 > 8. 正式产物与唯一事实源 > 8.0 V6.3 三阶段修订与生成边界

- `P2` · Locator `C11:88ec56f7:0c539819:171:ee534cd3` · Lines `225-225`

```text
TaskContract 在首个 `run_started` Event 时冻结。之后 Scope、Acceptance、Authority、Plan 或 Task Profile 的变化必须增加 Revision 并写入 `amendments[]`，包含旧值、新值、原因、依据和时间。TaskOutcome 形成后采用同一纠错规则，禁止静默覆盖终态事实。
```

### 35. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 2. 目的

- `P2` · Locator `VC-PPG-PRO-001:548a810a:ea37d4de:23:e2d492d6` · Lines `29-29`

```text
本规范建立跨任务类型的唯一流程路由，使所有任务共用一个八阶段主流程，并以 TaskContract、RunLedger 和 TaskOutcome 分别承载任务执行前、执行中和任务终态事实；Task Profile 作为 TaskContract 字段驱动阶段深度、专业规范、Profile 实例、Evidence、Gate 和人类确认裁剪。
```

### 36. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 13. 三阶段记录必填信息 > 13.4 TaskOutcome / after.json

- `P2` · Locator `VC-PPG-PRO-001:548a810a:bc3580a9:416:87ec80eb` · Lines `566-566`

```text
- 遗留问题的原因、影响、Owner 和重新进入条件；
```

### 37. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 12. 最小物理产物与条件 Profile > 12.1 所有任务的最低集合

- `P2` · Locator `VC-PPG-PRO-001:548a810a:73fc5ef5:351:aadaaa1b` · Lines `480-480`

```text
| 任务终态 | TaskOutcome / `after.json` | 结果、已成立事实、实际变化、验证、未完成项、遗留问题、决定、Evidence、后继任务、终态 Manifest |
```

### 38. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.3 任务终态：TaskOutcome

- `P2` · Locator `VC-PPG-PRO-001:548a810a:f3e42a70:139:b28ea182` · Lines `182-182`

```text
- 遗留问题、原因、影响、Owner 和重新进入条件；
```

### 39. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.4 RUN Accepted 条件

- `P2` · Locator `C09:6897694e:d5731510:661:6238bc88` · Lines `870-870`

```text
### 15.4 RUN Accepted 条件
```

### 40. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.4 RUN Accepted 条件

- `P2` · Locator `C09:6897694e:d5731510:663:9dee3a6d` · Lines `874-874`

```text
- HRR State = Accepted，决定者为授权人类；
```

### 41. C11 — C11 配置、版本、基线与变更控制规范 > 8. 正式产物与唯一事实源 > 8.0 V6.3 三阶段修订与生成边界

- `P2` · Locator `C11:88ec56f7:0c539819:172:3b2cf7dd` · Lines `227-227`

```text
RunLedger 只追加；更正通过新 Event 引用原 Event。ProjectState 和 DerivedView 由生成器重建，禁止直接编辑或纳入独立变更源。Git Commit/Diff 可作为代码和文档变化的权威证据，但外部副作用、失败、验证环境、批准和决定必须由相应元类型或 AuthorityAsset 保存。
```

### 42. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.4 RUN Accepted 条件

- `P2` · Locator `C09:6897694e:d5731510:662:1c1a2862` · Lines `872-872`

```text
RUN 从 Completed 转为 Accepted 必须同时满足：
```

### 43. C12 — C12 评审、质量门禁与产品健康规范 > 11. 受控状态 > 11.2 DOC State：QGC、PHR、IAP

- `P2` · Locator `C12:508ab626:e93b92b4:671:e1a139d6` · Lines `909-909`

```text
3. Approved IAP 表示计划获批，不表示 Action 已完成；
```

### 44. C09 — C09 Agent 执行与证据规范 > 11. 受控状态 > 11.2 EXEC：RUN 与 HRR

- `P2` · Locator `C09:6897694e:13ebbcd8:467:0dcefe6c` · Lines `617-617`

```text
RUN Failed/Cancelled/Accepted/Rejected 为终端结果；继续工作必须建立新 Run。HRR 使用同一 EXEC 模型，Accepted/Rejected 必须由授权人类决定。
```

### 45. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.18 Agent 健康指标

- `P2` · Locator `C12:508ab626:35ebcbd8:547:7ad93ca7` · Lines `733-733`

```text
| AH-005 | 返工率 | 在 Approved Rework Window 内因前次不合格输出产生后继修正 Run/CHG 的 Accepted Change Unit 数 ÷ Accepted Change Unit 总数 × 100% |
```

### 46. C09 — C09 Agent 执行与证据规范 > 9. 生命周期与工作机制 > 9.9 Completion、Acceptance 与 Writeback

- `P2` · Locator `C09:6897694e:422c3eea:233:17a2de1b` · Lines `321-321`

```text
RUN Completed 表示动作已结束且记录完整；RUN Accepted 必须有 HRR Accepted、阻断 Finding 为零、Residual Risk 已按 Authority 处置且写回接口完成。写回只能更新原事实源允许的字段或创建受控 Change/Issue/Trace，不得用 C09 覆盖上游状态。
```

### 47. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.4 项目状态与唯一事实源

- `P2` · Locator `VC-PPG-PRO-001:548a810a:1708baa2:155:1112bf80` · Lines `202-202`

```text
| ProjectState | 仅由有效 TaskOutcome 和当前 AuthorityAsset 物化，禁止直接编辑 |
```

### 48. C09 — C09 Agent 执行与证据规范 > 11. 受控状态 > 11.6 状态转换

- `P2` · Locator `C09:6897694e:80374583:481:5cfb6d26` · Lines `642-642`

```text
4. RUN Completed 禁止自动转为 Accepted。
```

### 49. C11 — C11 配置、版本、基线与变更控制规范 > 20. 模板、清单与国际标准条款映射 > 20.14 Emergency Change 清单

- `P2` · Locator `C11:88ec56f7:38e4507c:1084:4b330c40` · Lines `1773-1773`

```text
- [ ] Post-implementation Review 已完成；
```

### 50. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 12. 最小物理产物与条件 Profile > 12.1 所有任务的最低集合

- `P2` · Locator `VC-PPG-PRO-001:548a810a:73fc5ef5:352:cb66d9df` · Lines `481-481`

```text
| 跨任务消费 | ProjectState / `project-state.json` | 从有效 TaskOutcome 与 AuthorityAsset 自动物化的当前事实、遗留项和任务图 |
```

### 51. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:798:bbb36f93` · Lines `1046-1046`

```text
46. HRR Accepted/Rejected 是否由授权人类决定；
```

### 52. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 12. 最小物理产物与条件 Profile > 12.1 所有任务的最低集合

- `P2` · Locator `VC-PPG-PRO-001:548a810a:73fc5ef5:354:9038bc70` · Lines `485-485`

```text
满足 VC-PPG-DEC-001 §16.4 时，前三行逻辑对象可以聚合到单一 `task-record.json`；字段子集必须与 TaskContract、RunLedger、TaskOutcome 语义兼容。该聚合载体不是新元类型，也不改变 ProjectState 的消费规则。
```

### 53. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 15. 验证与符合性检查 > 15.1 流程就绪检查

- `P2` · Locator `VC-PPG-PRO-001:548a810a:d9098f34:442:81162127` · Lines `601-601`

```text
- 必需专业深化已完成；
```

### 54. C11 — C11 配置、版本、基线与变更控制规范 > 20. 模板、清单与国际标准条款映射 > 20.14 Emergency Change 清单

- `P2` · Locator `C11:88ec56f7:38e4507c:1082:d5516391` · Lines `1771-1771`

```text
- [ ] 独立验证和追溯已完成；
```

### 55. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.8 Specification Ready

- `P2` · Locator `C12:508ab626:ae02edb3:389:a736cf79` · Lines `530-530`

```text
5. Quality Attribute 已完成九类 ISO/IEC 25010 适用性；
```

### 56. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.22 Retrospective

- `P2` · Locator `C12:508ab626:f1d6d244:608:b1fb2723` · Lines `814-814`

```text
6. RTR `Accepted` 后 Learning 才可作为正式改进输入；
```

### 57. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 6. 术语与定义

- `P2` · Locator `VC-PPG-PRO-001:548a810a:8c711bde:81:e2202b95` · Lines `106-106`

```text
| ProjectState | 由有效 TaskOutcome 与当前 AuthorityAsset 生成的项目当前状态 | 禁止直接编辑 |
```

### 58. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 6. 术语与定义

- `P2` · Locator `VC-PPG-PRO-001:548a810a:8c711bde:84:4ffda6f8` · Lines `110-110`

```text
TaskContract、Task Profile、Artifact Manifest、RunLedger、TaskOutcome、ProjectState、Delivery Scenario、Development Type、Change Surface、Risk Level、Extension Trigger、Baseline Inheritance、Execution Mode 和五类实例动作的唯一术语来源是 VC-PPG-COM-001 与 VC-PPG-COM-002。
```

### 59. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.15 Human Review

- `P2` · Locator `C09:6897694e:054c9f5d:398:c3a89ccf` · Lines `524-524`

```text
6. HRR Accepted/Rejected 必须由授权人类决定。
```

### 60. C12 — C12 评审、质量门禁与产品健康规范 > 6. 术语与定义 > 6.1 必须区分的对象

- `P2` · Locator `C12:508ab626:df7d02ad:166:afbf9030` · Lines `213-213`

```text
| IAP | 后续如何改进 | 已完成改进的证据 |
```

### 61. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.5 最低追踪关系

- `P2` · Locator `VC-PPG-PRO-001:548a810a:a1d7e147:157:ce3bb034` · Lines `206-219`

```text
流程必须能够追踪：

```text
ProjectID / WorkItemID / TaskID
  → TaskContract / Task Profile
  → Scope / Requirement / Change 来源
  → Artifact Manifest
  → RunLedger / Git Change
  → Changed Asset
  → Verification / Validation Evidence
  → Acceptance / Gate / Release Decision
  → TaskOutcome / Follow-up
  → ProjectState
```
```

### 62. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.4 RUN Accepted 条件

- `P2` · Locator `C09:6897694e:d5731510:669:1221d6fa` · Lines `880-880`

```text
- 接受范围、条件、失效和后续责任明确。
```

### 63. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 13. 三阶段记录必填信息 > 13.5 ProjectState / project-state.json

- `P2` · Locator `VC-PPG-PRO-001:548a810a:be9921ca:419:738b77c5` · Lines `570-570`

```text
### 13.5 ProjectState / project-state.json
```

### 64. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.4 评审结论与接受

- `P2` · Locator `C12:508ab626:ad9be204:301:dcf51b8d` · Lines `420-420`

```text
6. RVR `Accepted` 必须由授权人类复核评审完整性；
```

### 65. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 11. 受控状态 > 11.2 流程结果

- `P2` · Locator `VC-PPG-PRO-001:548a810a:f7e3b353:337:3e961f44` · Lines `458-458`

```text
| `Implemented` | 当前声明交付已完成并形成要求的受控输出；可以是产品变化，也可以是正式评审、分析或报告，不表示资产已批准或发布 |
```

### 66. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 13. 三阶段记录必填信息 > 13.5 ProjectState / project-state.json

- `P2` · Locator `VC-PPG-PRO-001:548a810a:be9921ca:420:57410148` · Lines `572-572`

```text
ProjectState 必须包含 Source Digest、来源 TaskOutcome、当前事实、遗留项、任务图和 AuthorityAsset 索引；必须由生成器重建，禁止直接编辑。
```

### 67. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.0 V6.3 最小执行记录覆盖规则

- `P2` · Locator `C09:6897694e:b1dd146f:140:e2820809` · Lines `190-190`

```text
3. RunLedger 只记录 `run_started`、`mutation`、`failure`、`retry`、`verification`、`external_effect`、`human_gate`、`authority_decision_reference`、`rollback`、`run_finished`。
```

### 68. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.4 评审结论与接受

- `P2` · Locator `C12:508ab626:ad9be204:302:f6ce6c60` · Lines `421-421`

```text
7. RVR `Accepted` 不改变被评审对象 State；
```

### 69. C12 — C12 评审、质量门禁与产品健康规范 > 13. 产物必填信息 > 13.7 RTR — Retrospective Record

- `P2` · Locator `C12:508ab626:af4c0c49:810:9c7194f0` · Lines `1086-1086`

```text
- Start/End/Accepted Time；
```

### 70. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.2 执行中记录：RunLedger

- `P2` · Locator `VC-PPG-PRO-001:548a810a:5963b45f:132:93865f70` · Lines `172-172`

```text
一个 Task 只使用一个 RunID。验证失败后必须先在当前 AttemptID 追加显式 `failure` 事件，再以未使用的 AttemptID 追加 `retry`；`retry` 一旦切换 AttemptID，禁止回填旧 Attempt。`run_finished` 后禁止追加事件。
```

### 71. C12 — C12 评审、质量门禁与产品健康规范 > 14. 质量准则 > 14.1 Review 质量

- `P2` · Locator `C12:508ab626:f574caf9:840:8e24dfe2` · Lines `1122-1122`

```text
- RVR Accepted 不改写对象 State。
```

### 72. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:109:b611a243` · Lines `150-150`

```text
| Changed Artifact | Run 实际创建、修改、删除、移动或替代的受控资产 | Git/Diff 是低成本变化证据；任务级事实进入 TaskOutcome |
```

### 73. C09 — C09 Agent 执行与证据规范 > 11. 受控状态 > 11.6 状态转换

- `P2` · Locator `C09:6897694e:80374583:479:adad5a72` · Lines `640-640`

```text
2. Approved、Conditionally Approved、Waived、Accepted 和 Baselined 必须由授权人类决定。
```

### 74. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:110:1c22f18f` · Lines `151-151`

```text
| Code Change | 影响可执行行为、构建、测试、配置、Schema、Migration、脚本或基础设施的变化 | TaskOutcome 记录 CCS 兼容语义并引用 Git；不复制完整 Diff |
```

### 75. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.4 RUN Accepted 条件

- `P2` · Locator `C09:6897694e:d5731510:666:ef37c939` · Lines `877-877`

```text
- Blocking Finding、失败、范围外变化和安全事件为零；
```

### 76. C12 — C12 评审、质量门禁与产品健康规范 > 11. 受控状态 > 11.1 EXEC State：RVR、RTR

- `P2` · Locator `C12:508ab626:3124e0bd:662:2e43ea87` · Lines `890-890`

```text
3. `Accepted` 必须由授权人类决定；
```

### 77. C09 — C09 Agent 执行与证据规范 > 17. P2 裁剪与扩展适用性 > 17.0 Task Profile 驱动的适用性

- `P2` · Locator `C09:6897694e:39226036:715:2dfd4b0a` · Lines `944-944`

```text
实际 Agent 变更任务必须具有 TaskContract 和 RunLedger；计划深化通过 TaskContract Amendment 更新，不创建第二份“执行方案”。重要运行事件进入 RunLedger，CAS/CCS/FER 语义进入 TaskOutcome；HRR/RRS 只在实际人类复核或剩余风险事件发生时 `On Event` 创建。
```

### 78. C12 — C12 评审、质量门禁与产品健康规范 > 15. 验证与符合性检查 > 15.5 Learning Closed 检查

- `P2` · Locator `C12:508ab626:3a14c087:908:4870947b` · Lines `1209-1209`

```text
- [ ] RTR Accepted；
```

### 79. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.25 Coding Agent 与自动化边界

- `P2` · Locator `C12:508ab626:8d5c6baf:648:f1a0f47d` · Lines `866-866`

```text
- 将自身输出直接标为 RVR/RTR `Accepted`；
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
