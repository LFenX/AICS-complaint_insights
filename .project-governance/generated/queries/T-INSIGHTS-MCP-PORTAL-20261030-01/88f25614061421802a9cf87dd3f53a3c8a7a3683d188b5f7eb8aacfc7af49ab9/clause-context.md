# Clause Context: T-INSIGHTS-MCP-PORTAL-20261030-01 / validate_change

- Status: `Expanded`
- Query digest: `88f25614061421802a9cf87dd3f53a3c8a7a3683d188b5f7eb8aacfc7af49ab9`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `7/7`
- Budget: `7175/12000` chars
- Fallback: `section`

## Source Index

- `C08`: `references/02_核心规范/C08_Agent_Context_Governance_Standard.md` / `V6.3 Candidate` / SHA-256 `262f2a190f130cb97955e58fca57d2216e2edf949d2f271413e5dff5d6faeb6d`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `C05`: `references/02_核心规范/C05_Acceptance_Verification_and_Validation_Standard.md` / `V6.3 Candidate` / SHA-256 `7973bcb4ea442030772e36b7418cc1e03f55e0b3aaa6072f4ec1c198d1b537c7`
- `E03`: `references/03_扩展规范/E03_Data_and_AI_Data_Governance_Extension_Standard.md` / `V6.3 Candidate` / SHA-256 `bb6a10422c6e672f3f67e6dc109c5bfaa594b195924758b21911fe44a18c603b`
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

### 11. C05 — C05 验收、验证与确认规范 > 11. 受控状态 > 11.4 非 State 受控值

- `P1` · Locator `C05:7973bcb4:80fd77b5:392:279e23cc` · Lines `564-564`

```text
| Verification Result | Pass、Fail、Blocked |
```

### 12. C08 — C08 Agent 上下文治理规范 > 11. 受控状态 > 11.3 CASE 产物

- `P1` · Locator `C08:262f2a19:6ea3d566:458:63ed7fa6` · Lines `618-618`

```text
`Open`、`In Progress`、`Blocked`、`Resolved`、`Closed`、`Reopened`、`Cancelled`。
```

### 13. E03 — E03 数据与 AI 数据治理扩展规范 > 2. 目的

- `P1` · Locator `E03:bb6a1042:2522fc9a:30:d3019592` · Lines `39-39`

```text
2. 使 Data Contract 的提供方、使用方、Schema、Semantics、Quality SLO、Compatibility、Change 和 Verification 受控；
```

### 14. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:252:8841a1d9` · Lines `319-319`

```text
- 擅自运行全表扫描、生产写入、回填、重标注、匿名化或删除；
```

### 15. C10 — C10 决策、追踪与资产血缘规范 > 16. 变更、审计与保留 > 16.1 变更控制

- `P1` · Locator `C10:0eba391e:4da3bc26:693:05adee83` · Lines `944-944`

```text
1. C10 文档、Schema、关系 Profile、Coverage Rule、Query Rule 和自动化策略变化必须进入 C11 Change。
```

### 16. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:158:ddd9f24f` · Lines `202-202`

```text
2. 未知来源、许可、数据主体、Schema、Owner、阈值、Consumer、Lineage 或 Retention 必须显式标为 Pending/Unknown；
```

### 17. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:159:b3346062` · Lines `203-203`

```text
3. 空值禁止代替 Unknown、Not Applicable 或 Not Evaluated；
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

### 23. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:157:6b0fd6e7` · Lines `201-201`

```text
1. 字段不适用时必须记录理由、Scope、依据和批准人；
```

### 24. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:242:958d7c5d` · Lines `306-306`

```text
Agent 可以：
```

### 25. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:253:70be0f3c` · Lines `320-320`

```text
- 推断未知许可、法律权属、PII 合法性或跨境允许性；
```

### 26. E03 — E03 数据与 AI 数据治理扩展规范 > 11. 数据与 AI 数据控制 > 11.11 RAG 与 Corpus 控制

- `P2` · Locator `E03:bb6a1042:8211c80f:627:357f1ba4` · Lines `828-828`

```text
### 11.11 RAG 与 Corpus 控制
```

### 27. C10 — C10 决策、追踪与资产血缘规范 > 11. 受控状态 > 11.1 Decision Record

- `P2` · Locator `C10:0eba391e:071911d6:421:90f0c1a8` · Lines `568-568`

```text
### 11.1 Decision Record
```

### 28. C10 — C10 决策、追踪与资产血缘规范 > 11. 受控状态 > 11.6 状态禁止混用

- `P3` · Locator `C10:0eba391e:a39c105e:435:da396d95` · Lines `628-628`

```text
### 11.6 状态禁止混用
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
