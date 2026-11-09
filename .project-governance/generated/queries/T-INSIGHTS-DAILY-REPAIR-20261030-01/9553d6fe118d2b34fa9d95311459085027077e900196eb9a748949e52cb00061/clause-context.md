# Clause Context: T-INSIGHTS-DAILY-REPAIR-20261030-01 / close_task

- Status: `Expanded`
- Query digest: `9553d6fe118d2b34fa9d95311459085027077e900196eb9a748949e52cb00061`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `9/9`
- Budget: `20249/12000` chars
- Fallback: `section`

## Source Index

- `C08`: `references/02_核心规范/C08_Agent_Context_Governance_Standard.md` / `V6.3 Candidate` / SHA-256 `262f2a190f130cb97955e58fca57d2216e2edf949d2f271413e5dff5d6faeb6d`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `E03`: `references/03_扩展规范/E03_Data_and_AI_Data_Governance_Extension_Standard.md` / `V6.3 Candidate` / SHA-256 `bb6a10422c6e672f3f67e6dc109c5bfaa594b195924758b21911fe44a18c603b`
- `C09`: `references/02_核心规范/C09_Agent_Execution_and_Evidence_Standard.md` / `V6.3 Candidate` / SHA-256 `6897694e362bf48cb3a13bb4e68d79d7173945daad2ba3e8f0b6c75be944c01e`
- `VC-PPG-PRO-001`: `references/01_治理基线/Vibe_Coding_任务类型裁剪与统一执行流程规范_V6.3.md` / `V6.3 Candidate` / SHA-256 `548a810a1cbce4fc7970f87778c71f56c9d0921e3ba385a73d085b8ed0276329`

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

### 11. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:159:b3346062` · Lines `203-203`

```text
3. 空值禁止代替 Unknown、Not Applicable 或 Not Evaluated；
```

### 12. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:160:c7dfbc1b` · Lines `204-204`

```text
4. 未知的许可、Privacy、Security 或 Legal Hold 禁止由 Agent 推断；
```

### 13. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:161:22992d0f` · Lines `205-205`

```text
5. 未知阈值禁止由 Tool Default、行业惯例或任意百分比填充；
```

### 14. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:162:a8c014d8` · Lines `206-206`

```text
6. 未知 Consumer 禁止批准 Breaking Change；
```

### 15. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:163:bc86dfc6` · Lines `207-207`

```text
7. 未知 Dataset Revision 禁止作为训练、测试、RAG 或 Gate 输入。
```

### 16. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:249:f851c872` · Lines `315-315`

```text
Agent 禁止：
```

### 17. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:157:6b0fd6e7` · Lines `201-201`

```text
1. 字段不适用时必须记录理由、Scope、依据和批准人；
```

### 18. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:158:ddd9f24f` · Lines `202-202`

```text
2. 未知来源、许可、数据主体、Schema、Owner、阈值、Consumer、Lineage 或 Retention 必须显式标为 Pending/Unknown；
```

### 19. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:242:958d7c5d` · Lines `306-306`

```text
Agent 可以：
```

### 20. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:253:70be0f3c` · Lines `320-320`

```text
- 推断未知许可、法律权属、PII 合法性或跨境允许性；
```

### 21. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:246:67a8b9f4` · Lines `311-311`

```text
- 汇总公开或已授权 Evidence；
```

### 22. C09 — C09 Agent 执行与证据规范 > 17. P2 裁剪与扩展适用性 > 17.0 Task Profile 驱动的适用性

- `P1` · Locator `C09:6897694e:39226036:716:28b946f8` · Lines `946-946`

```text
TaskOutcome 是任务级实际变化和遗留问题的事实源；存在代码变化时记录 CCS 兼容语义并引用 Git Diff。VDR 按 Run 汇总 VER/VAE、RunLedger 和 Git，仅作为 `Derived View / On Demand`，不得替代原始 Evidence。
```

### 23. C08 — C08 Agent 上下文治理规范 > 3. 适用范围

- `P1` · Locator `C08:262f2a19:2f2b733f:37:0a3b05f7` · Lines `49-49`

```text
- 当前 Task、工作区 Snapshot、工具结果、验证结果、临时 Assumption 和对话内容进入 Execution Context；
```

### 24. C12 — C12 评审、质量门禁与产品健康规范 > 8. 管理对象、关系与唯一事实源 > 8.0 V6.3 最小派生审核视图

- `P1` · Locator `C12:508ab626:af8a98f5:194:b842a677` · Lines `250-250`

```text
所有 DerivedView 必须记录生成器、Source Snapshot、来源对象、生成时间和完整性状态；可以删除后重建，禁止直接写入新的批准、事实或风险接受结论。Reviewer 发现视图与 TaskOutcome、AuthorityAsset 或 Evidence 冲突时，必须修正权威来源或生成规则，再重新生成视图。
```

### 25. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.4 项目状态与唯一事实源

- `P1` · Locator `VC-PPG-PRO-001:548a810a:1708baa2:154:5db3cf5f` · Lines `201-201`

```text
| TaskContract/RunLedger/TaskOutcome Schema 与生成器 | `run-governed-product-workflow`；不得重定义上述语义 |
```

### 26. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 6. 术语与定义

- `P2` · Locator `VC-PPG-PRO-001:548a810a:8c711bde:80:f39bc533` · Lines `105-105`

```text
| TaskOutcome | 记录已成立事实、实际变化、验证、未完成项、遗留问题和后续任务的终态对象 | 不保存执行前指令，不替代项目级 ProjectState |
```

### 27. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 9. 生命周期或工作机制 > 9.1 统一八阶段主流程

- `P2` · Locator `VC-PPG-PRO-001:548a810a:3151121b:168:d332662e` · Lines `234-234`

```text
| S8 收尾 | 当前交付不再继续执行 | 形成 TaskOutcome，更新终态 Artifact Manifest、Trace、Change、遗留问题和后继项；重建 ProjectState 和派生审核视图 | 结果为 Implemented、Deferred、Cancelled、Blocked 或 Superseded；事实、Owner、理由和 Evidence 完整 |
```

### 28. C09 — C09 Agent 执行与证据规范 > 12. V6.3 必需载体与条件 Profile

- `P2` · Locator `C09:6897694e:0a9756f4:489:490a3cdd` · Lines `653-653`

```text
| TaskOutcome / `after.json` | 每个结束任务 | CAS、CCS、FER、实际变化、验证、未完成项和遗留问题 |
```

### 29. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 2. 目的

- `P2` · Locator `VC-PPG-PRO-001:548a810a:ea37d4de:23:e2d492d6` · Lines `29-29`

```text
本规范建立跨任务类型的唯一流程路由，使所有任务共用一个八阶段主流程，并以 TaskContract、RunLedger 和 TaskOutcome 分别承载任务执行前、执行中和任务终态事实；Task Profile 作为 TaskContract 字段驱动阶段深度、专业规范、Profile 实例、Evidence、Gate 和人类确认裁剪。
```

### 30. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 13. 三阶段记录必填信息 > 13.4 TaskOutcome / after.json

- `P2` · Locator `VC-PPG-PRO-001:548a810a:bc3580a9:416:87ec80eb` · Lines `566-566`

```text
- 遗留问题的原因、影响、Owner 和重新进入条件；
```

### 31. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.3 任务终态：TaskOutcome

- `P2` · Locator `VC-PPG-PRO-001:548a810a:f3e42a70:139:b28ea182` · Lines `182-182`

```text
- 遗留问题、原因、影响、Owner 和重新进入条件；
```

### 32. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 12. 最小物理产物与条件 Profile > 12.1 所有任务的最低集合

- `P2` · Locator `VC-PPG-PRO-001:548a810a:73fc5ef5:351:aadaaa1b` · Lines `480-480`

```text
| 任务终态 | TaskOutcome / `after.json` | 结果、已成立事实、实际变化、验证、未完成项、遗留问题、决定、Evidence、后继任务、终态 Manifest |
```

### 33. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:786:59ad0f4a` · Lines `1034-1034`

```text
34. Commit/PR/Diff 与行为影响、验证和遗留问题是否同时可解析；
```

### 34. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.4 项目状态与唯一事实源

- `P2` · Locator `VC-PPG-PRO-001:548a810a:1708baa2:155:1112bf80` · Lines `202-202`

```text
| ProjectState | 仅由有效 TaskOutcome 和当前 AuthorityAsset 物化，禁止直接编辑 |
```

### 35. C12 — C12 评审、质量门禁与产品健康规范 > 8. 管理对象、关系与唯一事实源 > 8.0 V6.3 最小派生审核视图

- `P2` · Locator `C12:508ab626:af8a98f5:193:f4f6f312` · Lines `248-248`

```text
V6.3 首版固定生成三类审核视图：单任务审核摘要、项目当前状态与遗留问题、137→6 Profile 迁移映射与完整性报告。其他矩阵、报告和清单仅在 Gate、审计、查询或专业触发成立时生成。
```

### 36. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 12. 最小物理产物与条件 Profile > 12.1 所有任务的最低集合

- `P2` · Locator `VC-PPG-PRO-001:548a810a:73fc5ef5:352:cb66d9df` · Lines `481-481`

```text
| 跨任务消费 | ProjectState / `project-state.json` | 从有效 TaskOutcome 与 AuthorityAsset 自动物化的当前事实、遗留项和任务图 |
```

### 37. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 12. 最小物理产物与条件 Profile > 12.1 所有任务的最低集合

- `P2` · Locator `VC-PPG-PRO-001:548a810a:73fc5ef5:354:9038bc70` · Lines `485-485`

```text
满足 VC-PPG-DEC-001 §16.4 时，前三行逻辑对象可以聚合到单一 `task-record.json`；字段子集必须与 TaskContract、RunLedger、TaskOutcome 语义兼容。该聚合载体不是新元类型，也不改变 ProjectState 的消费规则。
```

### 38. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 6. 术语与定义

- `P2` · Locator `VC-PPG-PRO-001:548a810a:8c711bde:81:e2202b95` · Lines `106-106`

```text
| ProjectState | 由有效 TaskOutcome 与当前 AuthorityAsset 生成的项目当前状态 | 禁止直接编辑 |
```

### 39. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 6. 术语与定义

- `P2` · Locator `VC-PPG-PRO-001:548a810a:8c711bde:84:4ffda6f8` · Lines `110-110`

```text
TaskContract、Task Profile、Artifact Manifest、RunLedger、TaskOutcome、ProjectState、Delivery Scenario、Development Type、Change Surface、Risk Level、Extension Trigger、Baseline Inheritance、Execution Mode 和五类实例动作的唯一术语来源是 VC-PPG-COM-001 与 VC-PPG-COM-002。
```

### 40. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.5 最低追踪关系

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

### 41. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 13. 三阶段记录必填信息 > 13.5 ProjectState / project-state.json

- `P2` · Locator `VC-PPG-PRO-001:548a810a:be9921ca:419:738b77c5` · Lines `570-570`

```text
### 13.5 ProjectState / project-state.json
```

### 42. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 13. 三阶段记录必填信息 > 13.5 ProjectState / project-state.json

- `P2` · Locator `VC-PPG-PRO-001:548a810a:be9921ca:420:57410148` · Lines `572-572`

```text
ProjectState 必须包含 Source Digest、来源 TaskOutcome、当前事实、遗留项、任务图和 AuthorityAsset 索引；必须由生成器重建，禁止直接编辑。
```

### 43. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.0 V6.3 最小执行记录覆盖规则

- `P2` · Locator `C09:6897694e:b1dd146f:140:e2820809` · Lines `190-190`

```text
3. RunLedger 只记录 `run_started`、`mutation`、`failure`、`retry`、`verification`、`external_effect`、`human_gate`、`authority_decision_reference`、`rollback`、`run_finished`。
```

### 44. C09 — C09 Agent 执行与证据规范 > 3. 适用范围

- `P2` · Locator `C09:6897694e:44ea503a:45:20e6aec5` · Lines `57-57`

```text
- Run 产生的重要事件、受控 Evidence 引用、Diff、Commit、验证结果、失败和 Residual Risk；
```

### 45. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.2 执行中记录：RunLedger

- `P2` · Locator `VC-PPG-PRO-001:548a810a:5963b45f:132:93865f70` · Lines `172-172`

```text
一个 Task 只使用一个 RunID。验证失败后必须先在当前 AttemptID 追加显式 `failure` 事件，再以未使用的 AttemptID 追加 `retry`；`retry` 一旦切换 AttemptID，禁止回填旧 Attempt。`run_finished` 后禁止追加事件。
```

### 46. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:99:1138abc0` · Lines `140-140`

```text
| Agent Run | 具有唯一 Run ID、明确输入、开始与结束时间、动作、变更和验证结果的一次 Agent 执行 | 不等同 Agent Role、会话或模型产品 |
```

### 47. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:109:b611a243` · Lines `150-150`

```text
| Changed Artifact | Run 实际创建、修改、删除、移动或替代的受控资产 | Git/Diff 是低成本变化证据；任务级事实进入 TaskOutcome |
```

### 48. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:110:1c22f18f` · Lines `151-151`

```text
| Code Change | 影响可执行行为、构建、测试、配置、Schema、Migration、脚本或基础设施的变化 | TaskOutcome 记录 CCS 兼容语义并引用 Git；不复制完整 Diff |
```

### 49. C09 — C09 Agent 执行与证据规范 > 17. P2 裁剪与扩展适用性 > 17.0 Task Profile 驱动的适用性

- `P2` · Locator `C09:6897694e:39226036:715:2dfd4b0a` · Lines `944-944`

```text
实际 Agent 变更任务必须具有 TaskContract 和 RunLedger；计划深化通过 TaskContract Amendment 更新，不创建第二份“执行方案”。重要运行事件进入 RunLedger，CAS/CCS/FER 语义进入 TaskOutcome；HRR/RRS 只在实际人类复核或剩余风险事件发生时 `On Event` 创建。
```

### 50. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.3 RUN Completed 条件

- `P2` · Locator `C09:6897694e:4d4144f4:654:09093616` · Lines `861-861`

```text
- 所有变化在 Git/Evidence 和 TaskOutcome 中可解析；
```

### 51. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.3 RUN Completed 条件

- `P2` · Locator `C09:6897694e:4d4144f4:656:f7816867` · Lines `863-863`

```text
- Fail/Blocked/Retry/Rollback 在 RunLedger 和 TaskOutcome 中可解析；
```

### 52. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:783:89586504` · Lines `1031-1031`

```text
31. 每个变化是否在 TaskOutcome 和 Git/Evidence 中可解析；
```

### 53. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.11 CAS 与 CCS

- `P2` · Locator `C09:6897694e:8c131c15:352:c68648b5` · Lines `470-470`

```text
1. 每个实际变化必须在 TaskOutcome 的 `actual_changes` 或独立 AuthorityAsset Profile 中可解析；不要求每个文件建立单独 CAS。
```

### 54. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.11 CAS 与 CCS

- `P2` · Locator `C09:6897694e:8c131c15:355:a6fc09c6` · Lines `473-473`

```text
4. 涉及代码、测试、配置、Schema、Migration、构建脚本或基础设施即代码时，TaskOutcome 必须包含 CCS 兼容语义。
```

### 55. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.11 CAS 与 CCS

- `P2` · Locator `C09:6897694e:8c131c15:357:6d59839b` · Lines `475-475`

```text
6. Git Commit/PR/Diff 可以作为变化范围和内容的权威证据；TaskOutcome 仍必须解释行为影响、来源、验证和未解决项。
```

### 56. C09 — C09 Agent 执行与证据规范 > 13. 必填信息 > 13.1 通用必填信息

- `P2` · Locator `C09:6897694e:9e280442:495:28110c09` · Lines `663-663`

```text
TaskContract、RunLedger 和 TaskOutcome 必须满足对应 JSON Schema；独立 AuthorityAsset/DerivedView Profile 必须引用 VC-PPG-COM-002 第 3 章通用信息和第 3.1 节公共字段组。以下旧 Profile 字段作为兼容信息按需嵌入，不要求拆成九份文件。
```

### 57. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.1 九类正式产物

- `P2` · Locator `C09:6897694e:9f1a69b3:159:0de62ed8` · Lines `214-214`

```text
兼容 TIL Profile 只记录一次重要 Tool Invocation；V6.3 默认以 RunLedger Event ID 保持独立身份。CAS/CCS/FER 语义进入 TaskOutcome 时必须保留来源、范围和 History，聚合视图不得消除可追踪性。
```

### 58. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.0 V6.3 最小执行记录覆盖规则

- `P2` · Locator `C09:6897694e:b1dd146f:141:43296ed4` · Lines `191-191`

```text
4. CAS、CCS、FER 的任务级事实进入 TaskOutcome（`after.json`）；需要独立长期治理时仍可建立 AuthorityAsset Profile。
```

### 59. C09 — C09 Agent 执行与证据规范 > 17. P2 裁剪与扩展适用性 > 17.2 未来档位

- `P2` · Locator `C09:6897694e:dd4b3fe5:724:03108851` · Lines `958-958`

```text
P1/P2 可以通过 TaskContract、RunLedger、TaskOutcome 和 DerivedView 联合展示旧 Profile 语义，但必须保留 Run/Event/Asset ID、关键动作、Evidence、Failure、Risk、State 和逻辑身份。HRR、RRS 在触发时仍需独立权威记录。
```

### 60. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.12 验证与 Evidence

- `P2` · Locator `C09:6897694e:fd93cb49:360:50b4a24d` · Lines `480-480`

```text
1. 每个产生变化、运行结果或质量主张的 Run 必须在 RunLedger/TaskOutcome 记录验证事实；Gate、审计或人类审核需要汇总时按需生成 VDR DerivedView。
```

### 61. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 20. 附录：模板骨架、检查清单与示例 > 20.1 TaskContract 最小结构

- `P2` · Locator `VC-PPG-PRO-001:548a810a:2e556586:563:2df842f6` · Lines `817-828`

```text
3_跨规范产物归属索引.md", "sha256": "<64-char-sha256>"}
    ],
    "profile_coverage_digest": {"applicable": 0, "total": 137, "sha256": "<64-char-sha256>"}
  },
  "artifact_manifest": [
    {"meta_type": "TaskContract", "legacy_kind": null, "action": "Create/Revise", "asset_id": "T-001-before", "content_ref": ".project-governance/tasks/T-001/before.json", "reason": "freeze execution input", "rule_reference": "VC-PPG-PRO-001 §8.1", "owner": "task-initiator", "source_snapshot": "<source-snapshot>", "human_confirmation_refs": []},
    {"meta_type": "RunLedger", "legacy_kind": null, "action": "Create/Revise", "asset_id": "T-001-run", "content_ref": ".project-governance/tasks/T-001/run.jsonl", "reason": "record material execution events", "rule_reference": "VC-PPG-PRO-001 §8.2", "owner": "execution-agent", "source_snapshot": "<source-snapshot>", "human_confirmation_refs": []},
    {"meta_type": "TaskOutcome", "legacy_kind": null, "action": "Create/Revise", "asset_id": "T-001-after", "content_ref": ".project-governance/tasks/T-001/after.json", "reason": "record terminal facts and residue", "rule_reference": "VC-PPG-PRO-001 §8.3", "owner": "task-initiator", "source_snapshot": "<source-snapshot>", "human_confirmation_refs": []}
  ],
  "amendments": []
}
```
```

### 62. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 10. 强制规则 > 10.7 DT-04 需求澄清流程

- `P2` · Locator `VC-PPG-PRO-001:548a810a:496786d5:238:d7656587` · Lines `327-327`

```text
4. 纯澄清没有实际产品变化时，TaskOutcome 记录未执行产品变更的事实、检查方法和范围，S7 记录无发布或运行观察范围的规则依据；相关 Profile 按 Artifact Manifest 规则使用 `N/A`，S6 执行需求质量复核而非产品验收。
```

### 63. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 10. 强制规则 > 10.17 Emergency 叠加规则

- `P2` · Locator `VC-PPG-PRO-001:548a810a:56588531:309:91092981` · Lines `419-419`

```text
4. 恢复后必须补齐 TaskContract、Emergency CHG ID、最低 Impact/Risk、RunLedger、TaskOutcome、Verification、Trace，以及 C11 在适用 Policy 时限内要求补齐的 IMA、CHD、VRR、SNP、CIR、BSL 或 RLC Profile。
```

### 64. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 10. 强制规则 > 10.16 Artifact Manifest 规则

- `P2` · Locator `VC-PPG-PRO-001:548a810a:57b857f9:304:59533946` · Lines `412-412`

```text
9. 终态 Manifest 可追加收尾时实际发生的资产，追加项的 Outcome 只能是 `Created / Revised / Referenced / Generated`；TaskOutcome 建立后的追加必须通过 Amendment 记录。
```

### 65. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 17. 裁剪规则 > 17.1 不可裁剪项

- `P2` · Locator `VC-PPG-PRO-001:548a810a:72144562:504:e94d0644` · Lines `681-681`

```text
- TaskContract/TaskOutcome 中的 Artifact Manifest；
```

### 66. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 12. 最小物理产物与条件 Profile > 12.1 所有任务的最低集合

- `P2` · Locator `VC-PPG-PRO-001:548a810a:73fc5ef5:353:3cc70dc7` · Lines `483-483`

```text
Task Profile 和 Artifact Manifest 是 TaskContract/TaskOutcome 字段，不再是独立物理产物。长期需求、设计、决定、证据和基线按触发条件保存为 AuthorityAsset；审核报告、矩阵和索引保存为 DerivedView。
```

### 67. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 12. 最小物理产物与条件 Profile > 12.2 条件产物

- `P2` · Locator `VC-PPG-PRO-001:548a810a:7865df37:361:30270adf` · Lines `496-496`

```text
| Agent Run 产生变化、运行结果或质量主张 | Git 保存 Diff；RunLedger 保存必要事件；TaskOutcome 保存 CAS/CCS/FER 语义；需要审核时从 RunLedger、VER/VAE 和 Git 引用生成 VDR |
```

### 68. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 18. 扩展接口

- `P2` · Locator `VC-PPG-PRO-001:548a810a:862ef4c0:541:f18e11bf` · Lines `728-728`

```text
| C09 | 实际执行使用 RunLedger、TaskOutcome 和 Evidence | 重要运行事件、变化和失败记录 |
```

### 69. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 17. 裁剪规则 > 17.2 可以缩放项

- `P2` · Locator `VC-PPG-PRO-001:548a810a:9cb59572:519:96794b0e` · Lines `700-700`

```text
- 满足 VC-PPG-DEC-001 §16.4 时，TaskContract、RunLedger 和 TaskOutcome 的物理文件数量可缩为一个聚合载体，并跳过不产生 Authority 结论的 Shadow 检索派生物；控制目标、事实、验证、历史和升级检查不得删除。
```

### 70. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 9. 生命周期或工作机制 > 9.3 最小流程与完整流程

- `P2` · Locator `VC-PPG-PRO-001:548a810a:a0be4851:178:e9b33fe0` · Lines `248-248`

```text
- 默认最小流程仍必须经过 S1、S2、S4、S6 和 S8。专业规范未触发时可以缩短 S3；没有执行动作时可以缩短 S5；没有发布或运行观察范围时可以缩短 S7。每个被缩短阶段仍必须在 TaskContract 或 TaskOutcome 记录适用性依据、活动事实和退出结论，相关 Profile 在 Artifact Manifest 中使用受控实例动作。
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
