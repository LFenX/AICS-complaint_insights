# Clause Context: T-INSIGHTS-DAILY-20261030-01 / validate_change

- Status: `Complete`
- Query digest: `cd15af25bcdf77d86e73c69aedbd685a66dadbf9052829aee1f1f8a72dd586e9`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `5/5`
- Budget: `5339/12000` chars
- Fallback: `none`

## Source Index

- `C08`: `references/02_核心规范/C08_Agent_Context_Governance_Standard.md` / `V6.3 Candidate` / SHA-256 `262f2a190f130cb97955e58fca57d2216e2edf949d2f271413e5dff5d6faeb6d`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `C05`: `references/02_核心规范/C05_Acceptance_Verification_and_Validation_Standard.md` / `V6.3 Candidate` / SHA-256 `7973bcb4ea442030772e36b7418cc1e03f55e0b3aaa6072f4ec1c198d1b537c7`
- `C10`: `references/02_核心规范/C10_Decision_Traceability_and_Lineage_Standard.md` / `V6.3 Candidate` / SHA-256 `0eba391e52d509b37f7e6882b631729627eee8d27a887ccf391c58cc8e6a7534`

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

### 11. C05 — C05 验收、验证与确认规范 > 16. 追踪与记录要求 > 16.4 记录保留

- `P1` · Locator `C05:7973bcb4:9a2f233b:627:13d80a37` · Lines `883-883`

```text
1. Fail、Blocked、Rejected、Invalidated 和被替代 Evidence 禁止删除或覆盖。
```

### 12. C08 — C08 Agent 上下文治理规范 > 10. 强制规则 > 10.13 Minimum Context 与 Context Budget

- `P1` · Locator `C08:262f2a19:b6e30710:359:5debdd98` · Lines `484-484`

```text
5. 必需 Normative Context 仍无法容纳时必须 Blocked，不得静默截断。
```

### 13. C10 — C10 决策、追踪与资产血缘规范 > 11. 受控状态 > 11.3 UCR、OAR

- `P1` · Locator `C10:0eba391e:ae8b7161:428:7e427ce9` · Lines `596-603`

```text
两类产物使用 CASE State：

```text
Open → In Progress → Resolved → Closed
In Progress → Blocked
Closed → Reopened
Open / In Progress / Blocked → Cancelled
```
```

### 14. C08 — C08 Agent 上下文治理规范 > 16. 变更、审计与保留 > 16.3 保留与处置

- `P2` · Locator `C08:262f2a19:7c6dbf35:630:c51d53be` · Lines `844-844`

```text
### 16.3 保留与处置
```

### 15. C08 — C08 Agent 上下文治理规范 > 16. 变更、审计与保留 > 16.1 变更控制

- `P2` · Locator `C08:262f2a19:86e67079:617:9a20d4ce` · Lines `825-825`

```text
### 16.1 变更控制
```

### 16. C08 — C08 Agent 上下文治理规范 > 16. 变更、审计与保留 > 16.2 审计历史

- `P2` · Locator `C08:262f2a19:dc81220b:620:7ac6ea43` · Lines `831-831`

```text
### 16.2 审计历史
```

### 17. C10 — C10 决策、追踪与资产血缘规范 > 16. 变更、审计与保留 > 16.4 保留与处置

- `P2` · Locator `C10:0eba391e:3617ca63:714:c4981583` · Lines `971-971`

```text
### 16.4 保留与处置
```

### 18. C10 — C10 决策、追踪与资产血缘规范 > 16. 变更、审计与保留 > 16.1 变更控制

- `P2` · Locator `C10:0eba391e:4da3bc26:692:9a20d4ce` · Lines `942-942`

```text
### 16.1 变更控制
```

### 19. C10 — C10 决策、追踪与资产血缘规范 > 16. 变更、审计与保留 > 16.2 审计事件

- `P2` · Locator `C10:0eba391e:4e144ac1:699:98631c55` · Lines `951-951`

```text
### 16.2 审计事件
```

### 20. C10 — C10 决策、追踪与资产血缘规范 > 16. 变更、审计与保留 > 16.3 更正

- `P2` · Locator `C10:0eba391e:6518811c:708:54d6a434` · Lines `963-963`

```text
### 16.3 更正
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
