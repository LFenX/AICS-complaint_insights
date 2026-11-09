# Clause Context: T-INSIGHTS-MCP-REPAIR-20261030-05 / close_task

- Status: `Complete`
- Query digest: `24c9da811bcb1c9dc8329f35d0292cb57f790450274f0ad838ba09717c1c049c`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `8/8`
- Budget: `10043/12000` chars
- Fallback: `none`

## Source Index

- `C08`: `references/02_核心规范/C08_Agent_Context_Governance_Standard.md` / `V6.3 Candidate` / SHA-256 `262f2a190f130cb97955e58fca57d2216e2edf949d2f271413e5dff5d6faeb6d`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
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

### 11. C09 — C09 Agent 执行与证据规范 > 17. P2 裁剪与扩展适用性 > 17.0 Task Profile 驱动的适用性

- `P1` · Locator `C09:6897694e:39226036:716:28b946f8` · Lines `946-946`

```text
TaskOutcome 是任务级实际变化和遗留问题的事实源；存在代码变化时记录 CCS 兼容语义并引用 Git Diff。VDR 按 Run 汇总 VER/VAE、RunLedger 和 Git，仅作为 `Derived View / On Demand`，不得替代原始 Evidence。
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

### 14. C09 — C09 Agent 执行与证据规范 > 12. V6.3 必需载体与条件 Profile

- `P2` · Locator `C09:6897694e:0a9756f4:489:490a3cdd` · Lines `653-653`

```text
| TaskOutcome / `after.json` | 每个结束任务 | CAS、CCS、FER、实际变化、验证、未完成项和遗留问题 |
```

### 15. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:786:59ad0f4a` · Lines `1034-1034`

```text
34. Commit/PR/Diff 与行为影响、验证和遗留问题是否同时可解析；
```

### 16. C12 — C12 评审、质量门禁与产品健康规范 > 8. 管理对象、关系与唯一事实源 > 8.0 V6.3 最小派生审核视图

- `P2` · Locator `C12:508ab626:af8a98f5:193:f4f6f312` · Lines `248-248`

```text
V6.3 首版固定生成三类审核视图：单任务审核摘要、项目当前状态与遗留问题、137→6 Profile 迁移映射与完整性报告。其他矩阵、报告和清单仅在 Gate、审计、查询或专业触发成立时生成。
```

### 17. C12 — C12 评审、质量门禁与产品健康规范 > 13. 产物必填信息 > 13.3 GTE — Gate Decision

- `P2` · Locator `C12:508ab626:b9342b30:730:2afc9ab6` · Lines `994-994`

```text
- Gate Type/Profile、Parent Mandatory Gate；
```

### 18. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.6 Gate Instance 与决定

- `P2` · Locator `C12:508ab626:abff342c:332:3e8f2055` · Lines `459-459`

```text
- Gate ID、Type/Profile 和 Parent Mandatory Gate；
```

### 19. C12 — C12 评审、质量门禁与产品健康规范 > 20. 附录：模板、清单、指标与条款映射 > 20.10 五个强制 Gate 映射

- `P2` · Locator `C12:508ab626:efe2285e:1144:565f28d5` · Lines `1864-1865`

```text
| Mandatory Gate | 主要规范输入 | 允许的领域子 Gate |
|---|---|---|
```

### 20. C12 — C12 评审、质量门禁与产品健康规范 > 13. 产物必填信息 > 13.2 QGC — Quality Gate Checklist

- `P2` · Locator `C12:508ab626:3d819942:715:599d3c04` · Lines `976-976`

```text
- QGC ID、Gate Type/Profile、Parent Mandatory Gate；
```

### 21. C12 — C12 评审、质量门禁与产品健康规范 > 20. 附录：模板、清单、指标与条款映射 > 20.11 Gate Decision 清单

- `P2` · Locator `C12:508ab626:f1ebdf1f:1151:98f06b74` · Lines `1874-1874`

```text
- [ ] Gate Type/Profile 和 Parent Mandatory Gate 明确；
```

### 22. C09 — C09 Agent 执行与证据规范 > 3. 适用范围

- `P2` · Locator `C09:6897694e:44ea503a:45:20e6aec5` · Lines `57-57`

```text
- Run 产生的重要事件、受控 Evidence 引用、Diff、Commit、验证结果、失败和 Residual Risk；
```

### 23. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.0 V6.3 最小执行记录覆盖规则

- `P2` · Locator `C09:6897694e:b1dd146f:140:e2820809` · Lines `190-190`

```text
3. RunLedger 只记录 `run_started`、`mutation`、`failure`、`retry`、`verification`、`external_effect`、`human_gate`、`authority_decision_reference`、`rollback`、`run_finished`。
```

### 24. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:99:1138abc0` · Lines `140-140`

```text
| Agent Run | 具有唯一 Run ID、明确输入、开始与结束时间、动作、变更和验证结果的一次 Agent 执行 | 不等同 Agent Role、会话或模型产品 |
```

### 25. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.6 Gate Instance 与决定

- `P2` · Locator `C12:508ab626:abff342c:343:85f61a50` · Lines `471-471`

```text
Gate 规则：
```

### 26. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:109:b611a243` · Lines `150-150`

```text
| Changed Artifact | Run 实际创建、修改、删除、移动或替代的受控资产 | Git/Diff 是低成本变化证据；任务级事实进入 TaskOutcome |
```

### 27. C12 — C12 评审、质量门禁与产品健康规范 > 5. 规范性用语与受控判定 > 5.3 Gate Outcome 与 DEC State 映射

- `P2` · Locator `C12:508ab626:fc8dc95b:122:b0be322a` · Lines `158-158`

```text
| Waive | Waived | Gate 或可豁免项在 EWR/RAR 支持下有界跳过；不表示要求满足 |
```

### 28. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:110:1c22f18f` · Lines `151-151`

```text
| Code Change | 影响可执行行为、构建、测试、配置、Schema、Migration、脚本或基础设施的变化 | TaskOutcome 记录 CCS 兼容语义并引用 Git；不复制完整 Diff |
```

### 29. C12 — C12 评审、质量门禁与产品健康规范 > 14. 质量准则 > 14.2 Gate 质量

- `P2` · Locator `C12:508ab626:98a34764:841:39dcb6ca` · Lines `1124-1124`

```text
### 14.2 Gate 质量
```

### 30. C09 — C09 Agent 执行与证据规范 > 17. P2 裁剪与扩展适用性 > 17.0 Task Profile 驱动的适用性

- `P2` · Locator `C09:6897694e:39226036:715:2dfd4b0a` · Lines `944-944`

```text
实际 Agent 变更任务必须具有 TaskContract 和 RunLedger；计划深化通过 TaskContract Amendment 更新，不创建第二份“执行方案”。重要运行事件进入 RunLedger，CAS/CCS/FER 语义进入 TaskOutcome；HRR/RRS 只在实际人类复核或剩余风险事件发生时 `On Event` 创建。
```

### 31. C12 — C12 评审、质量门禁与产品健康规范 > 14. 质量准则 > 14.2 Gate 质量

- `P2` · Locator `C12:508ab626:98a34764:847:1035467a` · Lines `1131-1131`

```text
- 到期/输入变化 Gate 不被继续使用。
```

### 32. C12 — C12 评审、质量门禁与产品健康规范 > 13. 产物必填信息 > 13.3 GTE — Gate Decision

- `P2` · Locator `C12:508ab626:b9342b30:729:45090b4f` · Lines `993-993`

```text
- Gate Decision ID；
```

### 33. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.3 RUN Completed 条件

- `P2` · Locator `C09:6897694e:4d4144f4:654:09093616` · Lines `861-861`

```text
- 所有变化在 Git/Evidence 和 TaskOutcome 中可解析；
```

### 34. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.3 RUN Completed 条件

- `P2` · Locator `C09:6897694e:4d4144f4:656:f7816867` · Lines `863-863`

```text
- Fail/Blocked/Retry/Rollback 在 RunLedger 和 TaskOutcome 中可解析；
```

### 35. C12 — C12 评审、质量门禁与产品健康规范 > 14. 质量准则 > 14.2 Gate 质量

- `P2` · Locator `C12:508ab626:98a34764:842:894b5d1c` · Lines `1126-1126`

```text
- 五个强制 Gate 均有 Approved QGC；
```

### 36. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:783:89586504` · Lines `1031-1031`

```text
31. 每个变化是否在 TaskOutcome 和 Git/Evidence 中可解析；
```

### 37. C12 — C12 评审、质量门禁与产品健康规范 > 20. 附录：模板、清单、指标与条款映射 > 20.10 五个强制 Gate 映射

- `P2` · Locator `C12:508ab626:efe2285e:1145:ca77f42d` · Lines `1866-1866`

```text
| Discovery Ready | C01、C10、C11、C12 | Evidence Ready、Problem Ready |
```

### 38. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.11 CAS 与 CCS

- `P2` · Locator `C09:6897694e:8c131c15:352:c68648b5` · Lines `470-470`

```text
1. 每个实际变化必须在 TaskOutcome 的 `actual_changes` 或独立 AuthorityAsset Profile 中可解析；不要求每个文件建立单独 CAS。
```

### 39. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.11 CAS 与 CCS

- `P2` · Locator `C09:6897694e:8c131c15:355:a6fc09c6` · Lines `473-473`

```text
4. 涉及代码、测试、配置、Schema、Migration、构建脚本或基础设施即代码时，TaskOutcome 必须包含 CCS 兼容语义。
```

### 40. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.6 Gate Instance 与决定

- `P2` · Locator `C12:508ab626:abff342c:330:3ba8e8ed` · Lines `455-455`

```text
### 10.6 Gate Instance 与决定
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
