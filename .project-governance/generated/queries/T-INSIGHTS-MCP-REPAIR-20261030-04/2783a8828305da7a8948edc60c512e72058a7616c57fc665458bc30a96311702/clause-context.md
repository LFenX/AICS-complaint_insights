# Clause Context: T-INSIGHTS-MCP-REPAIR-20261030-04 / validate_change

- Status: `Expanded`
- Query digest: `2783a8828305da7a8948edc60c512e72058a7616c57fc665458bc30a96311702`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `8/8`
- Budget: `11140/12000` chars
- Fallback: `section`

## Source Index

- `C08`: `references/02_核心规范/C08_Agent_Context_Governance_Standard.md` / `V6.3 Candidate` / SHA-256 `262f2a190f130cb97955e58fca57d2216e2edf949d2f271413e5dff5d6faeb6d`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `C05`: `references/02_核心规范/C05_Acceptance_Verification_and_Validation_Standard.md` / `V6.3 Candidate` / SHA-256 `7973bcb4ea442030772e36b7418cc1e03f55e0b3aaa6072f4ec1c198d1b537c7`
- `E05`: `references/03_扩展规范/E05_Product_Operations_and_Service_Management_Extension_Standard.md` / `V6.3 Candidate` / SHA-256 `326d746628fd6b214527cd28ca71b5ea7b12148d4a0c102efcb0fb43f5c677da`
- `C09`: `references/02_核心规范/C09_Agent_Execution_and_Evidence_Standard.md` / `V6.3 Candidate` / SHA-256 `6897694e362bf48cb3a13bb4e68d79d7173945daad2ba3e8f0b6c75be944c01e`
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

### 11. C05 — C05 验收、验证与确认规范 > 20. 附录 > 20.8 Acceptance Decision 模板骨架

- `P1` · Locator `C05:7973bcb4:1bf4cad4:682:a172811b` · Lines `1138-1160`

```text
### 20.8 Acceptance Decision 模板骨架

```yaml
acceptance_decision_id: "ACD-0001"
acceptance_scope:
  product: "<Product + Revision>"
  prd: "<PRD + Revision>"
  requirement_set: "<RQS + Revision>"
  release: "<Release>"
  environment: "<环境>"
verification_evidence: []
validation_evidence: []
coverage_matrix: {id: "VCM-0001", revision: "<Revision>", measured_at: "<时间>"}
failed_blocked_invalidated_items: []
residual_risk: []
acceptance_outcome: "<Accept | Accept with Conditions | Reject | Defer>"
conditions: []
approver: {actor: "<授权人>", independence: "<独立性>", basis: "<批准依据>"}
effective_time: "<时间>"
expiry_time: "<时间或 None>"
gate_and_change_references: []
state: "Proposed"
```
```

### 12. E05 — E05 产品运营与服务管理扩展规范 > 20. 模板、检查清单与国际标准条例映射 > 20.1 Extension Applicability Decision 骨架

- `P1` · Locator `E05:326d7466:fb9c3b7f:957:da756f33` · Lines `1314-1343`

```text
### 20.1 Extension Applicability Decision 骨架

```yaml
decision_id:
product_scope_revision:
decision_owner:
evaluation_time:
triggers:
  continuous_operation:
    result: Yes|No|Unknown|Not Applicable
    evidence:
  production_sla_slo_oncall:
    result: Yes|No|Unknown|Not Applicable
    evidence:
  canary_rollback_incident_feedback_control:
    result: Yes|No|Unknown|Not Applicable
    evidence:
  post_release_metrics_drive_evolution:
    result: Yes|No|Unknown|Not Applicable
    evidence:
activation_status: Not Evaluated|Pending|Inactive|Conditionally Active|Active|Retiring|Retired
scope_conditions:
effective_time:
required_artifacts:
open_unknowns:
review_trigger:
change_request:
approver:
evidence:
```
```

### 13. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.13 Failure、Stop 与 Retry

- `P1` · Locator `C09:6897694e:7c53d277:373:bc060034` · Lines `495-495`

```text
1. 以下任一情况必须创建 FER：Failed/Blocked Step、Tool/Command Error、Validation Fail/Blocked、Stop Trigger、非预期副作用、证据丢失、Retry、Rollback 或敏感暴露。
```

### 14. C07 — C07 人机协作与责任规范 > 15. 评审、批准与就绪 > 15.3 阻断条件

- `P1` · Locator `C07:a1fc4e90:468db555:624:c387b145` · Lines `832-832`

```text
以下任一情况必须 Not Ready 或 Blocked：
```

### 15. C08 — C08 Agent 上下文治理规范 > 11. 受控状态 > 11.3 CASE 产物

- `P1` · Locator `C08:262f2a19:6ea3d566:458:63ed7fa6` · Lines `618-618`

```text
`Open`、`In Progress`、`Blocked`、`Resolved`、`Closed`、`Reopened`、`Cancelled`。
```

### 16. C08 — C08 Agent 上下文治理规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C08:262f2a19:946a89f0:721:80ee292d` · Lines `959-959`

```text
45. 非 State 判定是否未写入 State；
```

### 17. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:797:f432e972` · Lines `1045-1045`

```text
45. HRR 是否固定 Run/Change/Evidence Revision；
```

### 18. C07 — C07 人机协作与责任规范 > 10. 强制规则 > 10.11 风险与职责分离

- `P2` · Locator `C07:a1fc4e90:5c87178b:362:fe69734b` · Lines `490-490`

```text
7. 无法满足独立性时必须 Blocked；不得由 Agent 批准 EXA 绕过。
```

### 19. C07 — C07 人机协作与责任规范 > 11. 受控状态 > 11.3 STC 成员状态

- `P2` · Locator `C07:a1fc4e90:36750625:463:63ed7fa6` · Lines `628-628`

```text
`Open`、`In Progress`、`Blocked`、`Resolved`、`Closed`、`Reopened`、`Cancelled`。
```

### 20. C07 — C07 人机协作与责任规范 > 9. 生命周期与工作机制 > 9.2 Collaboration Intake

- `P2` · Locator `C07:a1fc4e90:38a2061d:203:3c922297` · Lines `276-276`

```text
任一必需输入缺失、冲突或失效时，COL 保持 Draft 或 Blocked 结论，不得进入执行。
```

### 21. C09 — C09 Agent 执行与证据规范 > 13. 必填信息 > 13.7 Validation Report

- `P2` · Locator `C09:6897694e:7fee0a05:568:332ff56c` · Lines `754-754`

```text
- Fail/Blocked/Warning/Flaky/Skipped/Not Applicable；
```

### 22. C07 — C07 人机协作与责任规范 > 5. 规范性用语 > 5.2 C07 判定关键词

- `P2` · Locator `C07:a1fc4e90:46743f31:68:c3d946ae` · Lines `94-94`

```text
`Pass`、`Fail` 和 `Blocked` 是 Review Outcome，不是资产 State。
```

### 23. C09 — C09 Agent 执行与证据规范 > 11. 受控状态 > 11.4 CASE：FER

- `P2` · Locator `C09:6897694e:a4d7090c:472:63ed7fa6` · Lines `627-627`

```text
`Open`、`In Progress`、`Blocked`、`Resolved`、`Closed`、`Reopened`、`Cancelled`。
```

### 24. C09 — C09 Agent 执行与证据规范 > 5. 规范性用语与受控判定 > 5.2 执行分类与判定值

- `P2` · Locator `C09:6897694e:bbe8d06d:74:adf9f770` · Lines `99-99`

```text
| Verification Result | `Pass`、`Fail`、`Blocked` |
```

### 25. C12 — C12 评审、质量门禁与产品健康规范 > 13. 产物必填信息 > 13.8 IAP — Improvement Action Plan

- `P2` · Locator `C12:508ab626:405f6b30:827:c2d459e5` · Lines `1106-1106`

```text
- Blocked/Escalation；
```

### 26. C07 — C07 人机协作与责任规范 > 5. 规范性用语 > 5.2 C07 判定关键词

- `P2` · Locator `C07:a1fc4e90:46743f31:67:c24b5a16` · Lines `92-92`

```text
`Collaboration Ready`、`Not Ready` 和 `Blocked` 是 Collaboration Readiness Conclusion，不是资产 State。
```

### 27. C08 — C08 Agent 上下文治理规范 > 20. 附录 > 20.9 Priority 与 Eligibility 判定表

- `P2` · Locator `C08:262f2a19:45809999:751:c8cb2d93` · Lines `1141-1141`

```text
| 必需覆盖和预算是否满足？ | 继续 | Blocked |
```

### 28. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.23 Improvement Action

- `P2` · Locator `C12:508ab626:6d71a991:618:6028d2aa` · Lines `827-827`

```text
- 有 Blocked Reason、Escalation 和变更历史；
```

### 29. C08 — C08 Agent 上下文治理规范 > 5. 规范性用语与受控判定 > 5.2 Context 分类与判定值

- `P2` · Locator `C08:262f2a19:10686e9a:78:892e2462` · Lines `103-103`

```text
| Selection Disposition | `Include`、`Reference`、`Exclude`、`Blocked` |
```

### 30. C08 — C08 Agent 上下文治理规范 > 15. 评审、批准与 Context Ready > 15.2 Context Ready 条件

- `P2` · Locator `C08:262f2a19:a2a36228:597:52351966` · Lines `799-799`

```text
- 无 Open/Blocked 的 Blocking CCF；
```

### 31. C08 — C08 Agent 上下文治理规范 > 10. 强制规则 > 10.13 Minimum Context 与 Context Budget

- `P2` · Locator `C08:262f2a19:b6e30710:359:5debdd98` · Lines `484-484`

```text
5. 必需 Normative Context 仍无法容纳时必须 Blocked，不得静默截断。
```

### 32. C09 — C09 Agent 执行与证据规范 > 14. 质量要求

- `P2` · Locator `C09:6897694e:0d3fa301:618:309f715d` · Lines `816-816`

```text
7. 失败保真：Fail、Blocked、Retry、Rollback 和反对 Evidence 不被覆盖；
```

### 33. C09 — C09 Agent 执行与证据规范 > 13. 必填信息 > 13.3 Agent Run Record

- `P2` · Locator `C09:6897694e:84b2f622:514:93f5abea` · Lines `688-688`

```text
- Start/End、State、Blocked/Resume/Cancel/Failure Time；
```

### 34. C09 — C09 Agent 执行与证据规范 > 5. 规范性用语与受控判定 > 5.2 执行分类与判定值

- `P2` · Locator `C09:6897694e:bbe8d06d:73:e9b82b21` · Lines `98-98`

```text
| Step Outcome | `Succeeded`、`Failed`、`Blocked`、`Skipped`、`Cancelled` |
```

### 35. C09 — C09 Agent 执行与证据规范 > 5. 规范性用语与受控判定 > 5.2 执行分类与判定值

- `P2` · Locator `C09:6897694e:bbe8d06d:75:adc639b3` · Lines `100-100`

```text
| Review Outcome | `Pass`、`Fail`、`Blocked` |
```

### 36. C09 — C09 Agent 执行与证据规范 > 16. 变更、审计与保留 > 16.3 Evidence 完整性

- `P2` · Locator `C09:6897694e:deef9a47:704:28353271` · Lines `927-927`

```text
5. Evidence 不可获得时必须记录原因、影响和 Blocked/限制，禁止补写推测内容。
```

### 37. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.5 QGC 设计与版本

- `P2` · Locator `C12:508ab626:0cc9b66a:313:af5e64d6` · Lines `435-435`

```text
- Pass/Fail/Blocked/N/A 判定规则；
```

### 38. C08 — C08 Agent 上下文治理规范 > 5. 规范性用语与受控判定 > 5.2 Context 分类与判定值

- `P2` · Locator `C08:262f2a19:10686e9a:79:72acb4a0` · Lines `104-104`

```text
| Context Readiness | `Context Ready`、`Not Ready`、`Blocked` |
```

### 39. C08 — C08 Agent 上下文治理规范 > 15. 评审、批准与 Context Ready > 15.3 阻断条件

- `P2` · Locator `C08:262f2a19:d9fe4e7d:603:c387b145` · Lines `808-808`

```text
以下任一情况必须 Not Ready 或 Blocked：
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
