# Clause Context: T-INSIGHTS-GITHUB-20261030-01 / close_task

- Status: `Complete`
- Query digest: `ca6bcdb658d12f19a70321854415a1657af4edd162007f4e57a9bdbb40121e22`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `8/8`
- Budget: `10337/12000` chars
- Fallback: `none`

## Source Index

- `C08`: `references/02_核心规范/C08_Agent_Context_Governance_Standard.md` / `V6.3 Candidate` / SHA-256 `262f2a190f130cb97955e58fca57d2216e2edf949d2f271413e5dff5d6faeb6d`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `C05`: `references/02_核心规范/C05_Acceptance_Verification_and_Validation_Standard.md` / `V6.3 Candidate` / SHA-256 `7973bcb4ea442030772e36b7418cc1e03f55e0b3aaa6072f4ec1c198d1b537c7`
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

### 11. C05 — C05 验收、验证与确认规范 > 10. 强制规则 > 10.3 Acceptance Criterion 表达

- `P1` · Locator `C05:7973bcb4:dfa671f3:207:50db7fe9` · Lines `333-333`

```text
1. Given 必须可建立和核验，不得包含待验证结果；
```

### 12. C08 — C08 Agent 上下文治理规范 > 3. 适用范围

- `P1` · Locator `C08:262f2a19:2f2b733f:37:0a3b05f7` · Lines `49-49`

```text
- 当前 Task、工作区 Snapshot、工具结果、验证结果、临时 Assumption 和对话内容进入 Execution Context；
```

### 13. C09 — C09 Agent 执行与证据规范 > 17. P2 裁剪与扩展适用性 > 17.0 Task Profile 驱动的适用性

- `P1` · Locator `C09:6897694e:39226036:716:28b946f8` · Lines `946-946`

```text
TaskOutcome 是任务级实际变化和遗留问题的事实源；存在代码变化时记录 CCS 兼容语义并引用 Git Diff。VDR 按 Run 汇总 VER/VAE、RunLedger 和 Git，仅作为 `Derived View / On Demand`，不得替代原始 Evidence。
```

### 14. C09 — C09 Agent 执行与证据规范 > 12. V6.3 必需载体与条件 Profile

- `P2` · Locator `C09:6897694e:0a9756f4:489:490a3cdd` · Lines `653-653`

```text
| TaskOutcome / `after.json` | 每个结束任务 | CAS、CCS、FER、实际变化、验证、未完成项和遗留问题 |
```

### 15. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:630:6cc80eaa` · Lines `842-842`

```text
### 10.24 审核、管理评审与纠正
```

### 16. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:776:e764677d` · Lines `1024-1024`

```text
24. 未信任输入是否未通过字符串拼接进入命令；
```

### 17. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.22 Retrospective

- `P2` · Locator `C12:508ab626:f1d6d244:597:24c66588` · Lines `801-801`

```text
- 已验证 Learning 与待验证假设；
```

### 18. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:636:2b0ad86d` · Lines `849-849`

```text
6. 重复 Nonconformity 禁止只延长 Due；
```

### 19. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:635:b16c0d93` · Lines `848-848`

```text
5. Corrective Action 可以进入 IAP，但必须标记其来源和强制性；
```

### 20. C08 — C08 Agent 上下文治理规范 > 15. 评审、批准与 Context Ready > 15.2 Context Ready 条件

- `P2` · Locator `C08:262f2a19:a2a36228:598:a76fb957` · Lines `800-800`

```text
- Sensitive Context 最小化、隔离和供应商边界已验证；
```

### 21. C12 — C12 评审、质量门禁与产品健康规范 > 3. 适用范围 > 3.2 蓝图必备主题映射

- `P2` · Locator `C12:508ab626:422f5c08:71:a0eedbb9` · Lines `90-90`

```text
| 审计 | 10.24、16 |
```

### 22. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:633:df69dc6c` · Lines `846-846`

```text
3. Audit Scope、Criteria、Sample、Independence 和 Finding 必须可复核；
```

### 23. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:637:ea5e64ad` · Lines `850-850`

```text
7. 审核结果禁止由被审核 Agent 自动接受；
```

### 24. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:638:4dbf1bc2` · Lines `851-851`

```text
8. Audit/Management Review 不建立新的 C12 正式产物类型。
```

### 25. C12 — C12 评审、质量门禁与产品健康规范 > 15. 验证与符合性检查 > 15.7 P2 强制检查

- `P2` · Locator `C12:508ab626:4265692c:988:7c1dbc4e` · Lines `1295-1295`

```text
| C12-P2-056 | Action 关闭有 Evidence | 效果已验证 |
```

### 26. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:634:78a3c905` · Lines `847-847`

```text
4. Nonconformity 必须控制当前影响、分析原因、识别类似问题、执行纠正并验证有效性；
```

### 27. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:631:455a044f` · Lines `844-844`

```text
1. Internal Audit 使用 RVR，Review Type=`Internal Audit`；
```

### 28. C12 — C12 评审、质量门禁与产品健康规范 > 20. 附录：模板、清单、指标与条款映射 > 20.18 国际标准条款映射

- `P2` · Locator `C12:508ab626:a0723fde:1236:62fc9869` · Lines `2051-2051`

```text
| ISO 9001:2015 第 9.2 章 | 内部审核 | 10.24 |
```

### 29. C12 — C12 评审、质量门禁与产品健康规范 > 20. 附录：模板、清单、指标与条款映射 > 20.18 国际标准条款映射

- `P2` · Locator `C12:508ab626:a0723fde:1237:711d3055` · Lines `2052-2052`

```text
| ISO 9001:2015 第 9.3 章 | 管理评审 | 10.24、14.5 |
```

### 30. C12 — C12 评审、质量门禁与产品健康规范 > 20. 附录：模板、清单、指标与条款映射 > 20.18 国际标准条款映射

- `P2` · Locator `C12:508ab626:a0723fde:1292:f1fd00a2` · Lines `2107-2107`

```text
| ISO/IEC 42001:2023 第 10 章 | 改进 | 10.22 至 10.24 |
```

### 31. C12 — C12 评审、质量门禁与产品健康规范 > 20. 附录：模板、清单、指标与条款映射 > 20.18 国际标准条款映射

- `P2` · Locator `C12:508ab626:a0723fde:1239:00f4815d` · Lines `2054-2054`

```text
| ISO 9001:2015 第 10.2 章 | 不符合与纠正措施 | 10.3、10.23、10.24 |
```

### 32. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:632:ebc052a8` · Lines `845-845`

```text
2. Management Review 使用 RVR，必须消费 PHR、Gate、Waiver、RAR、Finding、Incident 和 IAP；
```

### 33. C12 — C12 评审、质量门禁与产品健康规范 > 20. 附录：模板、清单、指标与条款映射 > 20.18 国际标准条款映射

- `P2` · Locator `C12:508ab626:a0723fde:1291:fbe66b2e` · Lines `2106-2106`

```text
| ISO/IEC 42001:2023 第 9 章 | 绩效评价 | 10.15 至 10.21、10.24 |
```

### 34. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.0 V6.3 最小执行记录覆盖规则

- `P2` · Locator `C09:6897694e:b1dd146f:140:e2820809` · Lines `190-190`

```text
3. RunLedger 只记录 `run_started`、`mutation`、`failure`、`retry`、`verification`、`external_effect`、`human_gate`、`authority_decision_reference`、`rollback`、`run_finished`。
```

### 35. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:786:59ad0f4a` · Lines `1034-1034`

```text
34. Commit/PR/Diff 与行为影响、验证和遗留问题是否同时可解析；
```

### 36. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:109:b611a243` · Lines `150-150`

```text
| Changed Artifact | Run 实际创建、修改、删除、移动或替代的受控资产 | Git/Diff 是低成本变化证据；任务级事实进入 TaskOutcome |
```

### 37. C12 — C12 评审、质量门禁与产品健康规范 > 8. 管理对象、关系与唯一事实源 > 8.0 V6.3 最小派生审核视图

- `P2` · Locator `C12:508ab626:af8a98f5:193:f4f6f312` · Lines `248-248`

```text
V6.3 首版固定生成三类审核视图：单任务审核摘要、项目当前状态与遗留问题、137→6 Profile 迁移映射与完整性报告。其他矩阵、报告和清单仅在 Gate、审计、查询或专业触发成立时生成。
```

### 38. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:110:1c22f18f` · Lines `151-151`

```text
| Code Change | 影响可执行行为、构建、测试、配置、Schema、Migration、脚本或基础设施的变化 | TaskOutcome 记录 CCS 兼容语义并引用 Git；不复制完整 Diff |
```

### 39. C09 — C09 Agent 执行与证据规范 > 17. P2 裁剪与扩展适用性 > 17.0 Task Profile 驱动的适用性

- `P2` · Locator `C09:6897694e:39226036:715:2dfd4b0a` · Lines `944-944`

```text
实际 Agent 变更任务必须具有 TaskContract 和 RunLedger；计划深化通过 TaskContract Amendment 更新，不创建第二份“执行方案”。重要运行事件进入 RunLedger，CAS/CCS/FER 语义进入 TaskOutcome；HRR/RRS 只在实际人类复核或剩余风险事件发生时 `On Event` 创建。
```

### 40. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.3 RUN Completed 条件

- `P2` · Locator `C09:6897694e:4d4144f4:654:09093616` · Lines `861-861`

```text
- 所有变化在 Git/Evidence 和 TaskOutcome 中可解析；
```

### 41. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.3 RUN Completed 条件

- `P2` · Locator `C09:6897694e:4d4144f4:656:f7816867` · Lines `863-863`

```text
- Fail/Blocked/Retry/Rollback 在 RunLedger 和 TaskOutcome 中可解析；
```

### 42. C08 — C08 Agent 上下文治理规范 > 19. 符合性检查 > 19.2 强制检查项

- `P3` · Locator `C08:262f2a19:946a89f0:700:646cc767` · Lines `938-938`

```text
24. Retrieval Score 是否未提升 Trust/Authority/Priority；
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
