# Clause Context: T-INSIGHTS-MCP-REPAIR-20261030-05 / validate_change

- Status: `Complete`
- Query digest: `b22a6e5910b3e8e0940dea3fc981ee114fbaf45bd54a5bbd057547b651759466`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `6/6`
- Budget: `9442/12000` chars
- Fallback: `none`

## Source Index

- `C08`: `references/02_核心规范/C08_Agent_Context_Governance_Standard.md` / `V6.3 Candidate` / SHA-256 `262f2a190f130cb97955e58fca57d2216e2edf949d2f271413e5dff5d6faeb6d`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `C10`: `references/02_核心规范/C10_Decision_Traceability_and_Lineage_Standard.md` / `V6.3 Candidate` / SHA-256 `0eba391e52d509b37f7e6882b631729627eee8d27a887ccf391c58cc8e6a7534`
- `C01`: `references/02_核心规范/C01_Product_Discovery_Evidence_and_Intent_Standard.md` / `V6.3 Candidate` / SHA-256 `afd73ffbde490eb2774af346046034692c83093612d0d60e0649cae8744c1773`

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

### 11. C12 — C12 评审、质量门禁与产品健康规范 > 18. 扩展接口与上下游交接 > 18.3 E02 安全、隐私与合规

- `P1` · Locator `C12:508ab626:6b8b1938:1101:526812cb` · Lines `1450-1450`

```text
当前未激活。目标产品处理账号、外部 API、Secret、个人信息、支付或监管数据时必须复评。激活后向 C12 提供 Security/Privacy/Compliance Gate、Risk、Waiver 和 Verification Evidence。Non-waivable 法规项禁止 EWR。
```

### 12. C08 — C08 Agent 上下文治理规范 > 11. 受控状态 > 11.3 CASE 产物

- `P1` · Locator `C08:262f2a19:6ea3d566:458:63ed7fa6` · Lines `618-618`

```text
`Open`、`In Progress`、`Blocked`、`Resolved`、`Closed`、`Reopened`、`Cancelled`。
```

### 13. C10 — C10 决策、追踪与资产血缘规范 > 11. 受控状态 > 11.1 Decision Record

- `P1` · Locator `C10:0eba391e:071911d6:421:90f0c1a8` · Lines `568-568`

```text
### 11.1 Decision Record
```

### 14. C01 — C01 产品发现、证据与意图规范 > 10. 强制规则 > 10.2 Evidence 分类与可靠性规则

- `P2` · Locator `C01:afd73ffb:17aa3526:171:9ddc8cdd` · Lines `285-285`

```text
6. Coding Agent 可以根据已记录事实计算分数，禁止自行补充缺失依据或把 Evidence 标记为 Accepted。
```

### 15. C01 — C01 产品发现、证据与意图规范 > 4. 不适用范围

- `P2` · Locator `C01:afd73ffb:1a4446a8:46:76c1152f` · Lines `61-61`

```text
- Acceptance Criteria、Verification 和 Validation 策略，由 C05 管理；
```

### 16. C01 — C01 产品发现、证据与意图规范 > 4. 不适用范围

- `P2` · Locator `C01:afd73ffb:1a4446a8:53:1db799b3` · Lines `68-68`

```text
- Quality Gate、风险接受和 Product Health，由 C12 管理；
```

### 17. C01 — C01 产品发现、证据与意图规范 > 4. 不适用范围

- `P2` · Locator `C01:afd73ffb:1a4446a8:55:b9b7dade` · Lines `71-71`

```text
本规范可以规定研究方法必须记录的信息和接受条件，但禁止将某一种研究方法规定为所有场景的唯一方法。
```

### 18. C01 — C01 产品发现、证据与意图规范 > 10. 强制规则 > 10.9 评审与批准规则

- `P2` · Locator `C01:afd73ffb:532f01fd:249:33e9f10f` · Lines `391-391`

```text
- Evidence 从 Under Review 转为 Accepted；
```

### 19. C01 — C01 产品发现、证据与意图规范 > 15. 验证与符合性检查 > 15.1 自动检查

- `P2` · Locator `C01:afd73ffb:5f598d1f:429:9f6a6bd0` · Lines `624-624`

```text
6. 是否存在 Problem 没有 Accepted Evidence 且未标记 Hypothesis-driven；
```

### 20. C01 — C01 产品发现、证据与意图规范 > 11. 受控状态 > 11.1 产物状态模型

- `P2` · Locator `C01:afd73ffb:64b43b4a:274:56ebc569` · Lines `425-425`

```text
| Evidence Record | EVD | EVID | Planned、Collected、Under Review、Accepted、Rejected、Invalidated |
```

### 21. C01 — C01 产品发现、证据与意图规范 > 11. 受控状态 > 11.1 产物状态模型

- `P2` · Locator `C01:afd73ffb:64b43b4a:275:33bb9ce8` · Lines `426-426`

```text
| Problem Definition | PRB | DOC | Draft、In Review、Changes Required、Approved、Baselined、Rejected、Superseded、Retired |
```

### 22. C01 — C01 产品发现、证据与意图规范 > 11. 受控状态 > 11.1 产物状态模型

- `P2` · Locator `C01:afd73ffb:64b43b4a:276:56ba7716` · Lines `427-427`

```text
| Product Definition | PDF | DOC | Draft、In Review、Changes Required、Approved、Baselined、Rejected、Superseded、Retired |
```

### 23. C01 — C01 产品发现、证据与意图规范 > 11. 受控状态 > 11.1 产物状态模型

- `P2` · Locator `C01:afd73ffb:64b43b4a:277:17532cf7` · Lines `428-428`

```text
| Product Intent & Goal Record | PIG | DOC | Draft、In Review、Changes Required、Approved、Baselined、Rejected、Superseded、Retired |
```

### 24. C01 — C01 产品发现、证据与意图规范 > 11. 受控状态 > 11.1 产物状态模型

- `P2` · Locator `C01:afd73ffb:64b43b4a:278:7c8658be` · Lines `429-429`

```text
| Assumption Register | ASM | DOC | Draft、In Review、Changes Required、Approved、Baselined、Rejected、Superseded、Retired |
```

### 25. C01 — C01 产品发现、证据与意图规范 > 10. 强制规则 > 10.4 Problem Definition 规则

- `P2` · Locator `C01:afd73ffb:8a0e204c:187:cec5a12f` · Lines `309-309`

```text
4. 引用至少一项 Accepted Evidence；
```

### 26. C01 — C01 产品发现、证据与意图规范 > 10. 强制规则 > 10.4 Problem Definition 规则

- `P2` · Locator `C01:afd73ffb:8a0e204c:195:d1b3a851` · Lines `320-320`

```text
| Hypothesis-driven | 没有达到 Accepted Evidence 条件，但存在已批准 Assumption 和验证计划 |
```

### 27. C01 — C01 产品发现、证据与意图规范 > 10. 强制规则 > 10.4 Problem Definition 规则

- `P2` · Locator `C01:afd73ffb:8a0e204c:196:0b37f701` · Lines `321-321`

```text
| Supported | 至少一项 Accepted Evidence 支持，且冲突 Evidence 已解释或形成开放问题 |
```

### 28. C01 — C01 产品发现、证据与意图规范 > 20. 附录 > 20.8 C01 质量检查清单

- `P2` · Locator `C01:afd73ffb:8fc4f14a:546:58de31ed` · Lines `1013-1013`

```text
| C01-CHK-008 | Problem 证据 | 每个 Problem 有 Accepted Evidence 或批准的 Hypothesis-driven 计划 | 待检查 |
```

### 29. C01 — C01 产品发现、证据与意图规范 > 15. 验证与符合性检查 > 15.3 Discovery Ready 阻断条件

- `P2` · Locator `C01:afd73ffb:9ef4a05d:450:037960f5` · Lines `650-650`

```text
存在任一条件时必须拒绝 Discovery Ready：
```

### 30. C01 — C01 产品发现、证据与意图规范 > 15. 验证与符合性检查 > 15.3 Discovery Ready 阻断条件

- `P2` · Locator `C01:afd73ffb:9ef4a05d:454:e01b6af4` · Lines `655-655`

```text
- 关键 Evidence 为 Rejected 或 Invalidated；
```

### 31. C01 — C01 产品发现、证据与意图规范 > 9. 生命周期与工作机制 > 9.8 Review and Gate

- `P2` · Locator `C01:afd73ffb:b3eb5708:131:321df5a8` · Lines `228-228`

```text
Independent Reviewer 必须检查第 15 章全部阻断项。Gate Approver 只能在阻断项为零时作出 Discovery Ready 通过决定；有未满足项时只能拒绝或按 C12 形成有期限的条件通过或 Waiver。
```

### 32. C01 — C01 产品发现、证据与意图规范 > 11. 受控状态 > 11.2 状态转换

- `P2` · Locator `C01:afd73ffb:cd398364:283:38ec4df2` · Lines `437-437`

```text
2. Evidence 只有在来源、方法、范围、局限和评分经过人类复核后才可以 Accepted。
```

### 33. C01 — C01 产品发现、证据与意图规范 > 11. 受控状态 > 11.2 状态转换

- `P2` · Locator `C01:afd73ffb:cd398364:286:dc744450` · Lines `440-440`

```text
5. Superseded、Retired、Rejected、Cancelled 和 Invalidated 资产禁止作为当前默认输入，但必须保留历史。
```

### 34. C01 — C01 产品发现、证据与意图规范 > 16. 追踪与记录要求 > 16.2 记录保留

- `P2` · Locator `C01:afd73ffb:d4d59ef2:479:03512dc1` · Lines `689-689`

```text
- 被拒绝、冲突和 Invalidated Evidence；
```

### 35. C01 — C01 产品发现、证据与意图规范 > 10. 强制规则 > 10.10 Coding Agent 约束

- `P2` · Locator `C01:afd73ffb:f3b5b89f:266:8a6c69bc` · Lines `413-413`

```text
- 独立把 Evidence 标记为 Accepted；
```

### 36. C01 — C01 产品发现、证据与意图规范 > 11. 受控状态 > 11.1 产物状态模型

- `P2` · Locator `C01:afd73ffb:64b43b4a:271:eafacb10` · Lines `420-420`

```text
### 11.1 产物状态模型
```

### 37. C01 — C01 产品发现、证据与意图规范 > 11. 受控状态 > 11.2 状态转换

- `P2` · Locator `C01:afd73ffb:cd398364:280:e48833e0` · Lines `432-432`

```text
### 11.2 状态转换
```

### 38. C10 — C10 决策、追踪与资产血缘规范 > 11. 受控状态 > 11.6 状态禁止混用

- `P3` · Locator `C10:0eba391e:a39c105e:435:da396d95` · Lines `628-628`

```text
### 11.6 状态禁止混用
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
