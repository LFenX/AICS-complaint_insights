# Clause Context: T-INSIGHTS-MCP-REPAIR-20261030-02 / close_task

- Status: `Expanded`
- Query digest: `849326e7232d05fcb8384bb34477ee878274f5e65d325949c1f4fdbef4f2323c`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `8/8`
- Budget: `11568/12000` chars
- Fallback: `section`

## Source Index

- `C08`: `references/02_核心规范/C08_Agent_Context_Governance_Standard.md` / `V6.3 Candidate` / SHA-256 `262f2a190f130cb97955e58fca57d2216e2edf949d2f271413e5dff5d6faeb6d`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `C11`: `references/02_核心规范/C11_Configuration_Version_Baseline_and_Change_Standard.md` / `V6.3 Candidate` / SHA-256 `88ec56f78f6d3da6f94b1684c7b1296ed1825bfcc961f0f8d3636c8c6a26f7e1`
- `C10`: `references/02_核心规范/C10_Decision_Traceability_and_Lineage_Standard.md` / `V6.3 Candidate` / SHA-256 `0eba391e52d509b37f7e6882b631729627eee8d27a887ccf391c58cc8e6a7534`
- `C09`: `references/02_核心规范/C09_Agent_Execution_and_Evidence_Standard.md` / `V6.3 Candidate` / SHA-256 `6897694e362bf48cb3a13bb4e68d79d7173945daad2ba3e8f0b6c75be944c01e`
- `C05`: `references/02_核心规范/C05_Acceptance_Verification_and_Validation_Standard.md` / `V6.3 Candidate` / SHA-256 `7973bcb4ea442030772e36b7418cc1e03f55e0b3aaa6072f4ec1c198d1b537c7`

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

### 11. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.8 Change Request 创建与分流

- `P1` · Locator `C11:88ec56f7:b4040cfb:360:9db49fbe` · Lines `492-492`

```text
4. CHG 重复时不得删除，必须连接主 CHG 并进入 `Cancelled` 或 `Closed`；
```

### 12. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.8 Change Request 创建与分流

- `P1` · Locator `C11:88ec56f7:b4040cfb:345:e7515c1d` · Lines `474-474`

```text
CHG 创建时必须记录：
```

### 13. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.8 Change Request 创建与分流

- `P1` · Locator `C11:88ec56f7:b4040cfb:358:a384ae80` · Lines `490-490`

```text
2. `Pre-authorized Standard`：必须已有 Approved 变更模型、范围、步骤、验证、回滚和 Authority；超出任一边界立即转 Normal；
```

### 14. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.8 Change Request 创建与分流

- `P1` · Locator `C11:88ec56f7:b4040cfb:361:5fcee191` · Lines `493-493`

```text
5. 未知范围、无 Owner、无原状态或无法识别资产的 CHG 必须 `Blocked`；
```

### 15. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.8 Change Request 创建与分流

- `P1` · Locator `C11:88ec56f7:b4040cfb:362:aaee730d` · Lines `494-494`

```text
6. 发现实际变化先于 CHG 时，必须创建 C10 UCR 并按 Risk 决定 Stop、隔离、回滚或追认；追认不消除违规事实。
```

### 16. C10 — C10 决策、追踪与资产血缘规范 > 8. 治理对象与关系 > 8.0 V6.3 任务链与元类型追踪

- `P1` · Locator `C10:0eba391e:99d17ee1:145:4e273987` · Lines `192-192`

```text
TaskContract 保存执行前来源和计划关系，RunLedger 保存重要事件和 Evidence 引用，TaskOutcome 保存终态事实及后继 TaskID，ProjectState 只物化有效终态与 AuthorityAsset。跨任务 Agent 默认优先消费 ProjectState 和相关 TaskOutcome；只有定位执行细节时才下钻 RunLedger。DerivedView 禁止成为新追踪事实的唯一来源。
```

### 17. C09 — C09 Agent 执行与证据规范 > 17. P2 裁剪与扩展适用性 > 17.0 Task Profile 驱动的适用性

- `P1` · Locator `C09:6897694e:39226036:716:28b946f8` · Lines `946-946`

```text
TaskOutcome 是任务级实际变化和遗留问题的事实源；存在代码变化时记录 CCS 兼容语义并引用 Git Diff。VDR 按 Run 汇总 VER/VAE、RunLedger 和 Git，仅作为 `Derived View / On Demand`，不得替代原始 Evidence。
```

### 18. C05 — C05 验收、验证与确认规范 > 10. 强制规则 > 10.3 Acceptance Criterion 表达

- `P1` · Locator `C05:7973bcb4:dfa671f3:207:50db7fe9` · Lines `333-333`

```text
1. Given 必须可建立和核验，不得包含待验证结果；
```

### 19. C08 — C08 Agent 上下文治理规范 > 3. 适用范围

- `P1` · Locator `C08:262f2a19:2f2b733f:37:0a3b05f7` · Lines `49-49`

```text
- 当前 Task、工作区 Snapshot、工具结果、验证结果、临时 Assumption 和对话内容进入 Execution Context；
```

### 20. C09 — C09 Agent 执行与证据规范 > 12. V6.3 必需载体与条件 Profile

- `P2` · Locator `C09:6897694e:0a9756f4:489:490a3cdd` · Lines `653-653`

```text
| TaskOutcome / `after.json` | 每个结束任务 | CAS、CCS、FER、实际变化、验证、未完成项和遗留问题 |
```

### 21. C11 — C11 配置、版本、基线与变更控制规范 > 8. 正式产物与唯一事实源 > 8.0 V6.3 三阶段修订与生成边界

- `P2` · Locator `C11:88ec56f7:0c539819:171:ee534cd3` · Lines `225-225`

```text
TaskContract 在首个 `run_started` Event 时冻结。之后 Scope、Acceptance、Authority、Plan 或 Task Profile 的变化必须增加 Revision 并写入 `amendments[]`，包含旧值、新值、原因、依据和时间。TaskOutcome 形成后采用同一纠错规则，禁止静默覆盖终态事实。
```

### 22. C11 — C11 配置、版本、基线与变更控制规范 > 8. 正式产物与唯一事实源 > 8.0 V6.3 三阶段修订与生成边界

- `P2` · Locator `C11:88ec56f7:0c539819:172:3b2cf7dd` · Lines `227-227`

```text
RunLedger 只追加；更正通过新 Event 引用原 Event。ProjectState 和 DerivedView 由生成器重建，禁止直接编辑或纳入独立变更源。Git Commit/Diff 可作为代码和文档变化的权威证据，但外部副作用、失败、验证环境、批准和决定必须由相应元类型或 AuthorityAsset 保存。
```

### 23. C10 — C10 决策、追踪与资产血缘规范 > 15. 评审、批准与接受 > 15.1 评审顺序

- `P2` · Locator `C10:0eba391e:4d81eef3:642:e0753658` · Lines `876-876`

```text
### 15.1 评审顺序
```

### 24. C10 — C10 决策、追踪与资产血缘规范 > 15. 评审、批准与接受 > 15.4 Trace Ready

- `P2` · Locator `C10:0eba391e:b63644e0:668:a108d336` · Lines `910-910`

```text
### 15.4 Trace Ready
```

### 25. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:786:59ad0f4a` · Lines `1034-1034`

```text
34. Commit/PR/Diff 与行为影响、验证和遗留问题是否同时可解析；
```

### 26. C10 — C10 决策、追踪与资产血缘规范 > 15. 评审、批准与接受 > 15.3 Link Active Ready

- `P2` · Locator `C10:0eba391e:72437e1f:658:9c3b7095` · Lines `897-897`

```text
### 15.3 Link Active Ready
```

### 27. C12 — C12 评审、质量门禁与产品健康规范 > 8. 管理对象、关系与唯一事实源 > 8.0 V6.3 最小派生审核视图

- `P2` · Locator `C12:508ab626:af8a98f5:193:f4f6f312` · Lines `248-248`

```text
V6.3 首版固定生成三类审核视图：单任务审核摘要、项目当前状态与遗留问题、137→6 Profile 迁移映射与完整性报告。其他矩阵、报告和清单仅在 Gate、审计、查询或专业触发成立时生成。
```

### 28. C11 — C11 配置、版本、基线与变更控制规范 > 15. 评审、批准与阻断 > 15.5 强制阻断

- `P2` · Locator `C11:88ec56f7:fe00db08:858:eb69a307` · Lines `1142-1142`

```text
### 15.5 强制阻断
```

### 29. C10 — C10 决策、追踪与资产血缘规范 > 15. 评审、批准与接受 > 15.5 阻断条件

- `P2` · Locator `C10:0eba391e:2ecef0aa:679:880fc8f6` · Lines `925-925`

```text
### 15.5 阻断条件
```

### 30. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.0 V6.3 最小执行记录覆盖规则

- `P2` · Locator `C09:6897694e:b1dd146f:140:e2820809` · Lines `190-190`

```text
3. RunLedger 只记录 `run_started`、`mutation`、`failure`、`retry`、`verification`、`external_effect`、`human_gate`、`authority_decision_reference`、`rollback`、`run_finished`。
```

### 31. C10 — C10 决策、追踪与资产血缘规范 > 15. 评审、批准与接受 > 15.2 DEC Review Ready

- `P2` · Locator `C10:0eba391e:4d348089:650:c39cd2ec` · Lines `886-886`

```text
### 15.2 DEC Review Ready
```

### 32. C09 — C09 Agent 执行与证据规范 > 3. 适用范围

- `P2` · Locator `C09:6897694e:44ea503a:45:20e6aec5` · Lines `57-57`

```text
- Run 产生的重要事件、受控 Evidence 引用、Diff、Commit、验证结果、失败和 Residual Risk；
```

### 33. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:99:1138abc0` · Lines `140-140`

```text
| Agent Run | 具有唯一 Run ID、明确输入、开始与结束时间、动作、变更和验证结果的一次 Agent 执行 | 不等同 Agent Role、会话或模型产品 |
```

### 34. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:109:b611a243` · Lines `150-150`

```text
| Changed Artifact | Run 实际创建、修改、删除、移动或替代的受控资产 | Git/Diff 是低成本变化证据；任务级事实进入 TaskOutcome |
```

### 35. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:110:1c22f18f` · Lines `151-151`

```text
| Code Change | 影响可执行行为、构建、测试、配置、Schema、Migration、脚本或基础设施的变化 | TaskOutcome 记录 CCS 兼容语义并引用 Git；不复制完整 Diff |
```

### 36. C09 — C09 Agent 执行与证据规范 > 17. P2 裁剪与扩展适用性 > 17.0 Task Profile 驱动的适用性

- `P2` · Locator `C09:6897694e:39226036:715:2dfd4b0a` · Lines `944-944`

```text
实际 Agent 变更任务必须具有 TaskContract 和 RunLedger；计划深化通过 TaskContract Amendment 更新，不创建第二份“执行方案”。重要运行事件进入 RunLedger，CAS/CCS/FER 语义进入 TaskOutcome；HRR/RRS 只在实际人类复核或剩余风险事件发生时 `On Event` 创建。
```

### 37. C05 — C05 验收、验证与确认规范 > 15. 验证与符合性检查 > 15.2 人工评审

- `P2` · Locator `C05:7973bcb4:3ba2597e:584:70d82a2f` · Lines `806-806`

```text
### 15.2 人工评审
```

### 38. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.3 RUN Completed 条件

- `P2` · Locator `C09:6897694e:4d4144f4:654:09093616` · Lines `861-861`

```text
- 所有变化在 Git/Evidence 和 TaskOutcome 中可解析；
```

### 39. C05 — C05 验收、验证与确认规范 > 15. 验证与符合性检查 > 15.1 自动检查

- `P2` · Locator `C05:7973bcb4:9bd38ad1:559:736da9bb` · Lines `777-777`

```text
### 15.1 自动检查
```

### 40. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.3 RUN Completed 条件

- `P2` · Locator `C09:6897694e:4d4144f4:656:f7816867` · Lines `863-863`

```text
- Fail/Blocked/Retry/Rollback 在 RunLedger 和 TaskOutcome 中可解析；
```

### 41. C05 — C05 验收、验证与确认规范 > 15. 验证与符合性检查 > 15.4 符合性声明限制

- `P2` · Locator `C05:7973bcb4:f2ab898a:618:50104d48` · Lines `846-846`

```text
### 15.4 符合性声明限制
```

### 42. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:783:89586504` · Lines `1031-1031`

```text
31. 每个变化是否在 TaskOutcome 和 Git/Evidence 中可解析；
```

### 43. C08 — C08 Agent 上下文治理规范 > 15. 评审、批准与 Context Ready > 15.1 评审顺序

- `P3` · Locator `C08:262f2a19:c6896026:578:e0753658` · Lines `776-776`

```text
### 15.1 评审顺序
```

### 44. C08 — C08 Agent 上下文治理规范 > 15. 评审、批准与 Context Ready > 15.2 Context Ready 条件

- `P3` · Locator `C08:262f2a19:a2a36228:588:f629e36d` · Lines `788-788`

```text
### 15.2 Context Ready 条件
```

### 45. C08 — C08 Agent 上下文治理规范 > 15. 评审、批准与 Context Ready > 15.3 阻断条件

- `P3` · Locator `C08:262f2a19:d9fe4e7d:602:2e1a5c0c` · Lines `806-806`

```text
### 15.3 阻断条件
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
