# Clause Context: T-INSIGHTS-GITHUB-20261030-01 / close_task

- Status: `Expanded`
- Query digest: `fb835ee1b84a9bb4a25a85e48576921054de1e44c0169fe1f643bcf30f8d944d`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `10/10`
- Budget: `7164/12000` chars
- Fallback: `section`

## Source Index

- `C08`: `references/02_核心规范/C08_Agent_Context_Governance_Standard.md` / `V6.3 Candidate` / SHA-256 `262f2a190f130cb97955e58fca57d2216e2edf949d2f271413e5dff5d6faeb6d`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `C09`: `references/02_核心规范/C09_Agent_Execution_and_Evidence_Standard.md` / `V6.3 Candidate` / SHA-256 `6897694e362bf48cb3a13bb4e68d79d7173945daad2ba3e8f0b6c75be944c01e`
- `C05`: `references/02_核心规范/C05_Acceptance_Verification_and_Validation_Standard.md` / `V6.3 Candidate` / SHA-256 `7973bcb4ea442030772e36b7418cc1e03f55e0b3aaa6072f4ec1c198d1b537c7`
- `C10`: `references/02_核心规范/C10_Decision_Traceability_and_Lineage_Standard.md` / `V6.3 Candidate` / SHA-256 `0eba391e52d509b37f7e6882b631729627eee8d27a887ccf391c58cc8e6a7534`
- `C07`: `references/02_核心规范/C07_Human_Agent_Collaboration_Standard.md` / `V6.3 Candidate` / SHA-256 `a1fc4e903d8b690f938d6e8fdf45a57abff2e94bcefbdb9729db1914804f016a`

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

### 11. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.11 CAS 与 CCS

- `P1` · Locator `C09:6897694e:8c131c15:352:c68648b5` · Lines `470-470`

```text
1. 每个实际变化必须在 TaskOutcome 的 `actual_changes` 或独立 AuthorityAsset Profile 中可解析；不要求每个文件建立单独 CAS。
```

### 12. C05 — C05 验收、验证与确认规范 > 10. 强制规则 > 10.3 Acceptance Criterion 表达

- `P1` · Locator `C05:7973bcb4:dfa671f3:207:50db7fe9` · Lines `333-333`

```text
1. Given 必须可建立和核验，不得包含待验证结果；
```

### 13. C08 — C08 Agent 上下文治理规范 > 3. 适用范围

- `P1` · Locator `C08:262f2a19:2f2b733f:37:0a3b05f7` · Lines `49-49`

```text
- 当前 Task、工作区 Snapshot、工具结果、验证结果、临时 Assumption 和对话内容进入 Execution Context；
```

### 14. C10 — C10 决策、追踪与资产血缘规范 > 8. 治理对象与关系 > 8.0 V6.3 任务链与元类型追踪

- `P1` · Locator `C10:0eba391e:99d17ee1:145:4e273987` · Lines `192-192`

```text
TaskContract 保存执行前来源和计划关系，RunLedger 保存重要事件和 Evidence 引用，TaskOutcome 保存终态事实及后继 TaskID，ProjectState 只物化有效终态与 AuthorityAsset。跨任务 Agent 默认优先消费 ProjectState 和相关 TaskOutcome；只有定位执行细节时才下钻 RunLedger。DerivedView 禁止成为新追踪事实的唯一来源。
```

### 15. C09 — C09 Agent 执行与证据规范 > 17. P2 裁剪与扩展适用性 > 17.0 Task Profile 驱动的适用性

- `P1` · Locator `C09:6897694e:39226036:716:28b946f8` · Lines `946-946`

```text
TaskOutcome 是任务级实际变化和遗留问题的事实源；存在代码变化时记录 CCS 兼容语义并引用 Git Diff。VDR 按 Run 汇总 VER/VAE、RunLedger 和 Git，仅作为 `Derived View / On Demand`，不得替代原始 Evidence。
```

### 16. C07 — C07 人机协作与责任规范 > 8. 治理对象与关系 > 8.0 V6.3 TaskContract 权限边界

- `P1` · Locator `C07:a1fc4e90:9063a02e:153:ae19c847` · Lines `209-209`

```text
TaskOutcome 只引用实际使用的权限、发生的人类决定和未决 Gate，不复制完整协作策略。COL、RMA、ARD、APM、ESP、STC、EXA 继续作为 AuthorityAsset Profile 保存长期规则。
```

### 17. C09 — C09 Agent 执行与证据规范 > 12. V6.3 必需载体与条件 Profile

- `P2` · Locator `C09:6897694e:0a9756f4:489:490a3cdd` · Lines `653-653`

```text
| TaskOutcome / `after.json` | 每个结束任务 | CAS、CCS、FER、实际变化、验证、未完成项和遗留问题 |
```

### 18. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.0 V6.3 最小执行记录覆盖规则

- `P2` · Locator `C09:6897694e:b1dd146f:140:e2820809` · Lines `190-190`

```text
3. RunLedger 只记录 `run_started`、`mutation`、`failure`、`retry`、`verification`、`external_effect`、`human_gate`、`authority_decision_reference`、`rollback`、`run_finished`。
```

### 19. C05 — C05 验收、验证与确认规范 > 10. 强制规则 > 10.17 Change、Re-execution 与版本控制

- `P2` · Locator `C05:7973bcb4:633f88bc:360:f5058bc9` · Lines `519-519`

```text
6. 新 ACD 生效时必须保留旧 ACD 的范围、Evidence、条件和有效期，不得无痕覆盖。
```

### 20. C08 — C08 Agent 上下文治理规范 > 14. 质量要求

- `P2` · Locator `C08:262f2a19:213f5c3f:573:225c0620` · Lines `769-769`

```text
12. 可审计：来源、获取、转换、选择、排除、变化、决定和历史可追踪；
```

### 21. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:109:b611a243` · Lines `150-150`

```text
| Changed Artifact | Run 实际创建、修改、删除、移动或替代的受控资产 | Git/Diff 是低成本变化证据；任务级事实进入 TaskOutcome |
```

### 22. C10 — C10 决策、追踪与资产血缘规范 > 15. 评审、批准与接受 > 15.1 评审顺序

- `P2` · Locator `C10:0eba391e:4d81eef3:647:63f2c592` · Lines `882-882`

```text
5. Records Steward 核对元数据、访问、保留和历史；
```

### 23. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:110:1c22f18f` · Lines `151-151`

```text
| Code Change | 影响可执行行为、构建、测试、配置、Schema、Migration、脚本或基础设施的变化 | TaskOutcome 记录 CCS 兼容语义并引用 Git；不复制完整 Diff |
```

### 24. C10 — C10 决策、追踪与资产血缘规范 > 6. 术语与定义

- `P3` · Locator `C10:0eba391e:d4d33c86:108:55c574b6` · Lines `145-145`

```text
| Trace Link Register | 保存正式 Trace Link、成员状态、版本范围和历史的权威受控集合 |
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
