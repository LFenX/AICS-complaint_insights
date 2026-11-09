# Clause Context: T-INSIGHTS-MCP-REPAIR-20261030-06 / independent_review

- Status: `Expanded`
- Query digest: `765b297569cea8d00c572616d5fc89c19203e98459ad838bc199af14c1fb80b8`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `7/7`
- Budget: `9206/12000` chars
- Fallback: `section`

## Source Index

- `C07`: `references/02_核心规范/C07_Human_Agent_Collaboration_Standard.md` / `V6.3 Candidate` / SHA-256 `a1fc4e903d8b690f938d6e8fdf45a57abff2e94bcefbdb9729db1914804f016a`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `C09`: `references/02_核心规范/C09_Agent_Execution_and_Evidence_Standard.md` / `V6.3 Candidate` / SHA-256 `6897694e362bf48cb3a13bb4e68d79d7173945daad2ba3e8f0b6c75be944c01e`
- `C08`: `references/02_核心规范/C08_Agent_Context_Governance_Standard.md` / `V6.3 Candidate` / SHA-256 `262f2a190f130cb97955e58fca57d2216e2edf949d2f271413e5dff5d6faeb6d`
- `C10`: `references/02_核心规范/C10_Decision_Traceability_and_Lineage_Standard.md` / `V6.3 Candidate` / SHA-256 `0eba391e52d509b37f7e6882b631729627eee8d27a887ccf391c58cc8e6a7534`

> 完整 lane rank 和逐条来源字段保存在同目录 `query-result.json`。

## Citations

### 1. C07 — C07 人机协作与责任规范 > 5. 规范性用语 > 5.3 规则优先级

- `P0` · Locator `C07:a1fc4e90:38ee3d27:76:69e5d4b3` · Lines `106-106`

```text
5. 本规范已批准或已基线版本中的“必须”“禁止”及第 10.17 节例外边界；
```

### 2. C07 — C07 人机协作与责任规范 > 5. 规范性用语 > 5.3 规则优先级

- `P0` · Locator `C07:a1fc4e90:38ee3d27:80:c42e79ef` · Lines `110-110`

```text
9. Agent 生成的建议、推断或默认行为。
```

### 3. C07 — C07 人机协作与责任规范 > 5. 规范性用语 > 5.3 规则优先级

- `P0` · Locator `C07:a1fc4e90:38ee3d27:81:ae1605be` · Lines `112-112`

```text
同一优先级冲突、来源有效性不明或无法判断适用范围时，必须停止受影响操作并按 ESP 升级。Agent 禁止自行选择更宽权限的解释。
```

### 4. C07 — C07 人机协作与责任规范 > 8. 治理对象与关系 > 8.0 V6.3 TaskContract 权限边界

- `P0` · Locator `C07:a1fc4e90:9063a02e:152:4c41b9ee` · Lines `207-207`

```text
“我被允许做什么”属于任务执行前输入，必须进入 TaskContract 的 `authority`、`scope`、`required_gates` 和 `stop_conditions`，不得等待任务结束后补写。Run 开始时这些字段冻结；后续权限扩大、范围变化或新 Gate 必须先停止受影响动作，并通过带 Authority 依据的 Amendment 修订。
```

### 5. C12 — C12 评审、质量门禁与产品健康规范 > 2. 目的

- `P0` · Locator `C12:508ab626:28e7276d:36:af7a1d0d` · Lines `45-45`

```text
10. 使 Agent 和自动化工具可以计算、检查和起草，但不能自批高风险输出或风险接受；
```

### 6. C12 — C12 评审、质量门禁与产品健康规范 > 5. 规范性用语与受控判定 > 5.1 中文关键词

- `P0` · Locator `C12:508ab626:e1e3a126:100:edb98f49` · Lines `127-127`

```text
“必须、禁止、应、不应、可以、可选”直接适用 VC-PPG-COM-001 的规范性用语定义；唯一语义以该公共基线为准，本文件不得复制或改写。
```

### 7. C12 — C12 评审、质量门禁与产品健康规范 > 5. 规范性用语与受控判定 > 5.1 中文关键词

- `P0` · Locator `C12:508ab626:e1e3a126:101:6775b219` · Lines `129-129`

```text
“必须”和“禁止”规则不得通过普通 EWR 绕过。法律、监管、合同、Safety、Security、Privacy、不可逆数据和明确 Non-waivable Gate 项不得豁免。
```

### 8. C09 — C09 Agent 执行与证据规范 > 9. 生命周期与工作机制 > 9.7 Failure、Retry 与 Rollback

- `P1` · Locator `C09:6897694e:00fcee58:229:a4dd6a88` · Lines `313-313`

```text
任一 Failed/Blocked、非预期副作用、Stop、验证失败或证据缺失必须建立 FER。Retry 或 Rollback 只能在副作用、权限、Plan、风险和新鲜 Context 可判定时执行。
```

### 9. C12 — C12 评审、质量门禁与产品健康规范 > 9. 生命周期与工作机制 > 9.1 评审与 Gate 总流程

- `P1` · Locator `C12:508ab626:0ed1d6da:236:5944f003` · Lines `305-322`

```text
### 9.1 评审与 Gate 总流程

```text
建立 Approved QGC / Gate Profile
  → 固定 Gate Instance 对象、Revision、Scope 和输入
  → 创建 RVR Planned
  → 核验 Reviewer、独立性、Evidence 和准则
  → RVR Ready → Running
  → 记录 Check Result、Finding 和整改
  → RVR Completed
  → 独立复核 RVR Accepted/Rejected
  → 汇总未满足项、EWR、RAR 和 Condition
  → GTE Proposed → Under Review
  → Approved / Conditionally Approved / Rejected / Waived
  → 进入下一状态/阶段或返回整改
  → 输入变化、条件到期、风险变化
  → Re-evaluate / Supersede / Expire
```
```

### 10. C08 — C08 Agent 上下文治理规范 > 1. 文档控制信息

- `P1` · Locator `C08:262f2a19:fc82ce4e:17:31738525` · Lines `20-20`

```text
| 生产前调研 | RVR-C08-0001 |
```

### 11. C10 — C10 决策、追踪与资产血缘规范 > 10. 强制规则 > 10.5 Rationale、Impact 与 Risk

- `P1` · Locator `C10:0eba391e:247c7a17:286:92fe7ed9` · Lines `393-394`

```text
6. Decision Reviewer 必须能从引用 Revision 独立复核事实，不得只接受摘要。
7.重大不利意见必须保留在 DEC 或 Review History 中。
```

### 12. C09 — C09 Agent 执行与证据规范 > 7. 角色与职责

- `P1` · Locator `C09:6897694e:95fdca46:129:661ed7d0` · Lines `174-174`

```text
| Independent Reviewer | 核对 Run、变更、验证、失败、敏感处理和剩余风险 | 不得评审自己未经独立复核的高风险输出 |
```

### 13. C12 — C12 评审、质量门禁与产品健康规范 > 13. 产物必填信息 > 13.1 RVR — Review Record

- `P2` · Locator `C12:508ab626:59827610:696:4b7ec8cc` · Lines `952-952`

```text
### 13.1 RVR — Review Record
```

### 14. C12 — C12 评审、质量门禁与产品健康规范 > 13. 产物必填信息 > 13.1 RVR — Review Record

- `P2` · Locator `C12:508ab626:59827610:698:3160796c` · Lines `956-956`

```text
- Review ID、Type、Purpose；
```

### 15. C12 — C12 评审、质量门禁与产品健康规范 > 13. 产物必填信息 > 13.1 RVR — Review Record

- `P2` · Locator `C12:508ab626:59827610:700:dfad2be9` · Lines `958-958`

```text
- Review Scope 和 Period；
```

### 16. C12 — C12 评审、质量门禁与产品健康规范 > 13. 产物必填信息 > 13.1 RVR — Review Record

- `P2` · Locator `C12:508ab626:59827610:707:20997a2b` · Lines `965-965`

```text
- Review Conclusion；
```

### 17. C12 — C12 评审、质量门禁与产品健康规范 > 13. 产物必填信息 > 13.1 RVR — Review Record

- `P2` · Locator `C12:508ab626:59827610:701:2bf94351` · Lines `959-959`

```text
- Review Input、Evidence 和缺失项；
```

### 18. C07 — C07 人机协作与责任规范 > 10. 强制规则 > 10.8 Agent 禁止行为

- `P2` · Locator `C07:a1fc4e90:c58febea:318:a921077e` · Lines `436-436`

```text
7. 修改、删除、隐藏或伪造批准、运行、证据、日志、发现项或反对意见；
```

### 19. C12 — C12 评审、质量门禁与产品健康规范 > 13. 产物必填信息 > 13.1 RVR — Review Record

- `P2` · Locator `C12:508ab626:59827610:709:d2746746` · Lines `967-967`

```text
- Re-review Result；
```

### 20. C12 — C12 评审、质量门禁与产品健康规范 > 3. 适用范围

- `P2` · Locator `C12:508ab626:2fb18abb:43:60088e46` · Lines `55-55`

```text
- 人工评审、同行评审、技术评审、管理评审、独立评审、审核、检查、发布评审和事后评审；
```

### 21. C10 — C10 决策、追踪与资产血缘规范 > 11. 受控状态 > 11.3 UCR、OAR

- `P2` · Locator `C10:0eba391e:ae8b7161:429:62ef07e5` · Lines `605-605`

```text
Resolved 必须有补救 Evidence；Closed 必须有独立复核。Cancelled 只表示无需继续处理，不删除发现事实。
```

### 22. C09 — C09 Agent 执行与证据规范 > 2. 目的

- `P2` · Locator `C09:6897694e:cd365db2:32:0c3cfbc6` · Lines `41-41`

```text
7. 使人类能够基于固定 Run、Diff、Evidence 和风险独立复核；
```

### 23. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.22 Retrospective

- `P2` · Locator `C12:508ab626:f1d6d244:601:6fb73ac2` · Lines `805-805`

```text
- Participant、Facilitator、时间和独立复核。
```

### 24. C07 — C07 人机协作与责任规范 > 1. 文档控制信息

- `P2` · Locator `C07:a1fc4e90:d17244bb:17:d81e514f` · Lines `20-20`

```text
| 生产前调研 | RVR-C07-0001 |
```

### 25. C09 — C09 Agent 执行与证据规范 > 1. 文档控制信息

- `P2` · Locator `C09:6897694e:c0f2196c:17:cf0a20e4` · Lines `20-20`

```text
| 生产前调研 | RVR-C09-0001 |
```

### 26. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:116:e32dcd62` · Lines `157-157`

```text
| Human Review | 有权人类基于固定 Run、Diff、Evidence 和 Risk 的独立复核 | 使用 HRR 管理 |
```

### 27. C10 — C10 决策、追踪与资产血缘规范 > 1. 文档控制信息

- `P2` · Locator `C10:0eba391e:97365543:17:48db43ef` · Lines `20-20`

```text
| 生产前调研 | RVR-C10-0001 |
```

### 28. C12 — C12 评审、质量门禁与产品健康规范 > 7. 角色、职责与独立性

- `P2` · Locator `C12:508ab626:44a31d2e:171:d0fea18f` · Lines `221-221`

```text
| Independent Reviewer | 对高风险对象提供组织、职责或技术独立复核 | 接受自身生成或实施的高风险输出 |
```

### 29. C12 — C12 评审、质量门禁与产品健康规范 > 20. 附录：模板、清单、指标与条款映射 > 20.2 RVR 模板

- `P2` · Locator `C12:508ab626:0403a3e5:1135:e147d943` · Lines `1521-1570`

```text
### 20.2 RVR 模板

```yaml
review_record:
  review_id: "RVR-0001"
  formal_state: "Planned"
  review_type: ""
  purpose: ""
  object:
    asset_id: ""
    revision: ""
    snapshot_or_baseline: ""
  scope: ""
  inputs: []
  missing_inputs: []
  criteria_revision: ""
  reviewers:
    - identity: ""
      role: ""
      competence: ""
      independence: ""
  method: ""
  sample:
    population: ""
    method: ""
    size: ""
    limitation: ""
  tool_and_rule_versions: []
  checks:
    - check_id: ""
      result: "Not Evaluated"
      evidence: []
      finding_id: ""
  findings:
    - finding_id: ""
      severity: ""
      blocking_level: ""
      criterion: ""
      fact: ""
      evidence: []
      owner: ""
      due_at: ""
  review_conclusion: ""
  remediation_actions: []
  rereview_result: ""
  acceptance_authority: ""
  started_at: ""
  completed_at: ""
  accepted_at: ""
```
```

### 30. C12 — C12 评审、质量门禁与产品健康规范 > 8. 管理对象、关系与唯一事实源 > 8.2 受控关系

- `P2` · Locator `C12:508ab626:276bc468:208:468c8200` · Lines `271-271`

```text
- RVR `addresses` 被评审对象和适用 Concern；
```

### 31. C12 — C12 评审、质量门禁与产品健康规范 > 8. 管理对象、关系与唯一事实源 > 8.2 受控关系

- `P2` · Locator `C12:508ab626:276bc468:209:5ccd6533` · Lines `272-272`

```text
- RVR `depends-on` 固定 QGC/Review Criteria 和输入 Evidence；
```

### 32. C12 — C12 评审、质量门禁与产品健康规范 > 8. 管理对象、关系与唯一事实源 > 8.2 受控关系

- `P2` · Locator `C12:508ab626:276bc468:210:b90b0e73` · Lines `273-273`

```text
- GTE `depends-on` QGC、RVR、Evidence、EWR、RAR 和当前 Baseline；
```

### 33. C12 — C12 评审、质量门禁与产品健康规范 > 11. 受控状态 > 11.1 EXEC State：RVR、RTR

- `P2` · Locator `C12:508ab626:3124e0bd:658:251df907` · Lines `878-884`

```text
### 11.1 EXEC State：RVR、RTR

```text
Planned → Ready → Running → Completed → Accepted/Rejected
                    ↕ Blocked
                    → Failed/Cancelled
```
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
