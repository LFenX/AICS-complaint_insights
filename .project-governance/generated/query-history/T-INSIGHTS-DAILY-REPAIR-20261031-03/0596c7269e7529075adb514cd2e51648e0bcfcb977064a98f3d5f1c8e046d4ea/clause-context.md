# Clause Context: T-INSIGHTS-DAILY-REPAIR-20261031-03 / edit_in_scope

- Status: `Expanded`
- Query digest: `0596c7269e7529075adb514cd2e51648e0bcfcb977064a98f3d5f1c8e046d4ea`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `5/5`
- Budget: `15201/12000` chars
- Fallback: `section`

## Source Index

- `C09`: `references/02_核心规范/C09_Agent_Execution_and_Evidence_Standard.md` / `V6.3 Candidate` / SHA-256 `6897694e362bf48cb3a13bb4e68d79d7173945daad2ba3e8f0b6c75be944c01e`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `C07`: `references/02_核心规范/C07_Human_Agent_Collaboration_Standard.md` / `V6.3 Candidate` / SHA-256 `a1fc4e903d8b690f938d6e8fdf45a57abff2e94bcefbdb9729db1914804f016a`
- `C11`: `references/02_核心规范/C11_Configuration_Version_Baseline_and_Change_Standard.md` / `V6.3 Candidate` / SHA-256 `88ec56f78f6d3da6f94b1684c7b1296ed1825bfcc961f0f8d3636c8c6a26f7e1`
- `C10`: `references/02_核心规范/C10_Decision_Traceability_and_Lineage_Standard.md` / `V6.3 Candidate` / SHA-256 `0eba391e52d509b37f7e6882b631729627eee8d27a887ccf391c58cc8e6a7534`
- `C08`: `references/02_核心规范/C08_Agent_Context_Governance_Standard.md` / `V6.3 Candidate` / SHA-256 `262f2a190f130cb97955e58fca57d2216e2edf949d2f271413e5dff5d6faeb6d`

> 完整 lane rank 和逐条来源字段保存在同目录 `query-result.json`。

## Citations

### 1. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:322:d81d2e63` · Lines `434-434`

```text
1. Delete、Deploy、External Mutation、生产操作、权限变化、不可逆操作和 High/Critical Risk Action 至少为 Approval Required；Prohibited 仍禁止。
```

### 2. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:325:f5a1c28d` · Lines `437-437`

```text
4. 执行前必须记录 Before Snapshot、影响范围、可恢复性、备份/回滚、幂等策略、观察窗口和验证。
```

### 3. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:327:c4bf94d5` · Lines `439-439`

```text
6. Deploy 必须引用 C11 Release Configuration、C12 Gate/Approval、窗口、监测、回滚和 Owner。
```

### 4. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:328:befa9592` · Lines `440-440`

```text
7. “清理”“修复”“格式化”“回滚”“恢复”不得扩大批准目标。
```

### 5. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:329:48963d8d` · Lines `441-441`

```text
8. Retry 高影响 Action 前必须先确认上次 Attempt 的外部副作用和幂等状态。
```

### 6. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:331:0e9a1176` · Lines `443-443`

```text
10. 操作后必须验证 Actual Effect；只有命令成功但目标状态未知时为 Blocked。
```

### 7. C12 — C12 评审、质量门禁与产品健康规范 > 2. 目的

- `P0` · Locator `C12:508ab626:28e7276d:36:af7a1d0d` · Lines `45-45`

```text
10. 使 Agent 和自动化工具可以计算、检查和起草，但不能自批高风险输出或风险接受；
```

### 8. C12 — C12 评审、质量门禁与产品健康规范 > 5. 规范性用语与受控判定 > 5.1 中文关键词

- `P0` · Locator `C12:508ab626:e1e3a126:100:edb98f49` · Lines `127-127`

```text
“必须、禁止、应、不应、可以、可选”直接适用 VC-PPG-COM-001 的规范性用语定义；唯一语义以该公共基线为准，本文件不得复制或改写。
```

### 9. C12 — C12 评审、质量门禁与产品健康规范 > 5. 规范性用语与受控判定 > 5.1 中文关键词

- `P0` · Locator `C12:508ab626:e1e3a126:101:6775b219` · Lines `129-129`

```text
“必须”和“禁止”规则不得通过普通 EWR 绕过。法律、监管、合同、Safety、Security、Privacy、不可逆数据和明确 Non-waivable Gate 项不得豁免。
```

### 10. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:323:8502f895` · Lines `435-435`

```text
2. 目标必须解析为精确仓库、路径、资源、记录、租户、账户、环境和版本。
```

### 11. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:324:2a399565` · Lines `436-436`

```text
3. 工作区根、用户主目录、系统根、整个账户/租户、未解析变量、宽泛通配符或计算后未复核目标禁止作为破坏性 Target。
```

### 12. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:326:32ce4083` · Lines `438-438`

```text
5. External Mutation 必须使用服务支持的 Idempotency Key 或记录不可幂等及补偿措施。
```

### 13. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.8 高影响、破坏性与外部操作

- `P0` · Locator `C09:6897694e:47ee626b:330:7404e213` · Lines `442-442`

```text
9. 删除或覆盖前必须识别用户已有、未提交、未跟踪和并行 Agent 变化；未知时 Stop。
```

### 14. C07 — C07 人机协作与责任规范 > 7. 参与者与职责 > 7.2 Agent 角色

- `P1` · Locator `C07:a1fc4e90:63ef8775:140:08fad459` · Lines `189-189`

```text
| Orchestrator Agent | 在授权范围内分解任务、分派子任务、收集结果和报告冲突 | 子 Agent 授权不得超过自身授权与子任务 Scope 的交集 |
```

### 15. C11 — C11 配置、版本、基线与变更控制规范 > 8. 正式产物与唯一事实源 > 8.0 V6.3 三阶段修订与生成边界

- `P1` · Locator `C11:88ec56f7:0c539819:172:3b2cf7dd` · Lines `227-227`

```text
RunLedger 只追加；更正通过新 Event 引用原 Event。ProjectState 和 DerivedView 由生成器重建，禁止直接编辑或纳入独立变更源。Git Commit/Diff 可作为代码和文档变化的权威证据，但外部副作用、失败、验证环境、批准和决定必须由相应元类型或 AuthorityAsset 保存。
```

### 16. C10 — C10 决策、追踪与资产血缘规范 > 10. 强制规则 > 10.12 关系约束与图完整性

- `P1` · Locator `C10:0eba391e:f53add28:341:16476ad1` · Lines `463-463`

```text
6. Active Link 的端点必须在有效范围内同时可用。
```

### 17. C08 — C08 Agent 上下文治理规范 > 7. 角色与职责

- `P1` · Locator `C08:262f2a19:5cc59f06:150:f5930fc9` · Lines `196-196`

```text
| Requirement/Design/Decision Owner | 处理相应事实源语义、Revision 和冲突 | 不得通过 C08 修改源资产 |
```

### 18. C09 — C09 Agent 执行与证据规范 > 9. 生命周期与工作机制 > 9.7 Failure、Retry 与 Rollback

- `P2` · Locator `C09:6897694e:00fcee58:229:a4dd6a88` · Lines `313-313`

```text
任一 Failed/Blocked、非预期副作用、Stop、验证失败或证据缺失必须建立 FER。Retry 或 Rollback 只能在副作用、权限、Plan、风险和新鲜 Context 可判定时执行。
```

### 19. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.4 RUN Accepted 条件

- `P2` · Locator `C09:6897694e:d5731510:661:6238bc88` · Lines `870-870`

```text
### 15.4 RUN Accepted 条件
```

### 20. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.4 RUN Accepted 条件

- `P2` · Locator `C09:6897694e:d5731510:663:9dee3a6d` · Lines `874-874`

```text
- HRR State = Accepted，决定者为授权人类；
```

### 21. C07 — C07 人机协作与责任规范 > 10. 强制规则 > 10.6 Autonomous 操作

- `P2` · Locator `C07:a1fc4e90:c8a022bf:291:234366cb` · Lines `402-402`

```text
7. 操作可审计，且不会产生未声明的外部副作用；
```

### 22. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.4 RUN Accepted 条件

- `P2` · Locator `C09:6897694e:d5731510:662:1c1a2862` · Lines `872-872`

```text
RUN 从 Completed 转为 Accepted 必须同时满足：
```

### 23. C09 — C09 Agent 执行与证据规范 > 11. 受控状态 > 11.2 EXEC：RUN 与 HRR

- `P2` · Locator `C09:6897694e:13ebbcd8:467:0dcefe6c` · Lines `617-617`

```text
RUN Failed/Cancelled/Accepted/Rejected 为终端结果；继续工作必须建立新 Run。HRR 使用同一 EXEC 模型，Accepted/Rejected 必须由授权人类决定。
```

### 24. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:770:ff3aba72` · Lines `1018-1018`

```text
18. Tool 默认行为、缓存、重试和副作用是否可知；
```

### 25. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:793:27098503` · Lines `1041-1041`

```text
41. Retry 是否创建新 Attempt 并检查副作用/幂等；
```

### 26. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.18 Agent 健康指标

- `P2` · Locator `C12:508ab626:35ebcbd8:547:7ad93ca7` · Lines `733-733`

```text
| AH-005 | 返工率 | 在 Approved Rework Window 内因前次不合格输出产生后继修正 Run/CHG 的 Accepted Change Unit 数 ÷ Accepted Change Unit 总数 × 100% |
```

### 27. C09 — C09 Agent 执行与证据规范 > 9. 生命周期与工作机制 > 9.9 Completion、Acceptance 与 Writeback

- `P2` · Locator `C09:6897694e:422c3eea:233:17a2de1b` · Lines `321-321`

```text
RUN Completed 表示动作已结束且记录完整；RUN Accepted 必须有 HRR Accepted、阻断 Finding 为零、Residual Risk 已按 Authority 处置且写回接口完成。写回只能更新原事实源允许的字段或创建受控 Change/Issue/Trace，不得用 C09 覆盖上游状态。
```

### 28. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.9 Impact Analysis

- `P2` · Locator `C11:88ec56f7:2470b427:382:c81a8d3c` · Lines `519-519`

```text
5. 数据删除、Schema 迁移、密钥轮换、模型变化和 Feature Flag 必须评估不可逆副作用；
```

### 29. C09 — C09 Agent 执行与证据规范 > 11. 受控状态 > 11.6 状态转换

- `P2` · Locator `C09:6897694e:80374583:481:5cfb6d26` · Lines `642-642`

```text
4. RUN Completed 禁止自动转为 Accepted。
```

### 30. C09 — C09 Agent 执行与证据规范 > 14. 质量要求

- `P2` · Locator `C09:6897694e:0d3fa301:617:e3bea0af` · Lines `815-815`

```text
6. 原子：副作用、权限和失败不可分时拆分 Action/TIL；
```

### 31. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:798:bbb36f93` · Lines `1046-1046`

```text
46. HRR Accepted/Rejected 是否由授权人类决定；
```

### 32. C07 — C07 人机协作与责任规范 > 2. 目的

- `P2` · Locator `C07:a1fc4e90:c77e3c5d:30:307cd56b` · Lines `39-39`

```text
5. 使高影响、不可逆、破坏性、跨 Scope、安全、隐私、合规、生产和外部副作用操作获得有权人类批准；
```

### 33. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.5 Step、Action 与 Attempt

- `P2` · Locator `C09:6897694e:e40e94e8:281:25e39cb3` · Lines `384-384`

```text
2. 每个 Action 只承担一个可独立判定授权、副作用和结果的 Operation。
```

### 34. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.22 Retrospective

- `P2` · Locator `C12:508ab626:f1d6d244:608:b1fb2723` · Lines `814-814`

```text
6. RTR `Accepted` 后 Learning 才可作为正式改进输入；
```

### 35. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:806:76d821d4` · Lines `1054-1054`

```text
54. 是否能重建主要副作用、TaskContract Revision、Diff 和验证；
```

### 36. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.15 Human Review

- `P2` · Locator `C09:6897694e:054c9f5d:398:c3a89ccf` · Lines `524-524`

```text
6. HRR Accepted/Rejected 必须由授权人类决定。
```

### 37. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.3 RUN Completed 条件

- `P2` · Locator `C09:6897694e:4d4144f4:659:92f7e6dd` · Lines `866-866`

```text
- 未发生未记录副作用或 Evidence 缺口。
```

### 38. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.7 命令规范

- `P2` · Locator `C09:6897694e:824cdbf7:317:d95f8e3a` · Lines `427-427`

```text
6. 复合命令若任一部分具有副作用、独立权限或独立失败条件，必须拆分 Action/TIL。
```

### 39. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.4 RUN Accepted 条件

- `P2` · Locator `C09:6897694e:d5731510:669:1221d6fa` · Lines `880-880`

```text
- 接受范围、条件、失效和后续责任明确。
```

### 40. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.13 Failure、Stop 与 Retry

- `P2` · Locator `C09:6897694e:7c53d277:379:a3f5a43c` · Lines `501-501`

```text
7. 非幂等或副作用未知的 Action 禁止自动 Retry。
```

### 41. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.4 评审结论与接受

- `P2` · Locator `C12:508ab626:ad9be204:301:dcf51b8d` · Lines `420-420`

```text
6. RVR `Accepted` 必须由授权人类复核评审完整性；
```

### 42. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.4 评审结论与接受

- `P2` · Locator `C12:508ab626:ad9be204:302:f6ce6c60` · Lines `421-421`

```text
7. RVR `Accepted` 不改变被评审对象 State；
```

### 43. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.0 V6.3 最小执行记录覆盖规则

- `P2` · Locator `C09:6897694e:b1dd146f:139:d80c7578` · Lines `189-189`

```text
2. RUN 与 TIL 语义进入只追加 RunLedger（`run.jsonl`）。普通读取、目录查看、搜索和未产生重要结果的无副作用调用不记录。
```

### 44. C12 — C12 评审、质量门禁与产品健康规范 > 13. 产物必填信息 > 13.7 RTR — Retrospective Record

- `P2` · Locator `C12:508ab626:af4c0c49:810:9c7194f0` · Lines `1086-1086`

```text
- Start/End/Accepted Time；
```

### 45. C12 — C12 评审、质量门禁与产品健康规范 > 14. 质量准则 > 14.1 Review 质量

- `P2` · Locator `C12:508ab626:f574caf9:840:8e24dfe2` · Lines `1122-1122`

```text
- RVR Accepted 不改写对象 State。
```

### 46. C09 — C09 Agent 执行与证据规范 > 11. 受控状态 > 11.6 状态转换

- `P2` · Locator `C09:6897694e:80374583:479:adad5a72` · Lines `640-640`

```text
2. Approved、Conditionally Approved、Waived、Accepted 和 Baselined 必须由授权人类决定。
```

### 47. C07 — C07 人机协作与责任规范 > 9. 生命周期与工作机制 > 9.3 Boundary and Risk Review

- `P2` · Locator `C07:a1fc4e90:509cf2df:208:9a9a77d5` · Lines `283-283`

```text
4. 确认目标对象、环境、版本、最大修改范围和外部副作用。
```

### 48. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.4 RUN Accepted 条件

- `P2` · Locator `C09:6897694e:d5731510:666:ef37c939` · Lines `877-877`

```text
- Blocking Finding、失败、范围外变化和安全事件为零；
```

### 49. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.7 命令规范

- `P2` · Locator `C09:6897694e:824cdbf7:320:956657f2` · Lines `430-430`

```text
9. 命令可重放记录不构成再次执行授权；重放前必须重新核验 Authorization、Context、Snapshot、Risk 和副作用。
```

### 50. C12 — C12 评审、质量门禁与产品健康规范 > 11. 受控状态 > 11.1 EXEC State：RVR、RTR

- `P2` · Locator `C12:508ab626:3124e0bd:662:2e43ea87` · Lines `890-890`

```text
3. `Accepted` 必须由授权人类决定；
```

### 51. C11 — C11 配置、版本、基线与变更控制规范 > 6. 术语与定义

- `P2` · Locator `C11:88ec56f7:7b574ff8:135:f0d09366` · Lines `178-178`

```text
| Rollback | 将当前系统或资产变更到一个先前已知配置的受控变更；不保证外部副作用或数据自动恢复 |
```

### 52. C12 — C12 评审、质量门禁与产品健康规范 > 15. 验证与符合性检查 > 15.5 Learning Closed 检查

- `P2` · Locator `C12:508ab626:3a14c087:908:4870947b` · Lines `1209-1209`

```text
- [ ] RTR Accepted；
```

### 53. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.6 Tool 与权限

- `P2` · Locator `C09:6897694e:d3202194:292:80041ed7` · Lines `397-397`

```text
4. Tool 自动重试、缓存、会话记忆、插件、扩展、默认工作目录和外部副作用必须可知。
```

### 54. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.25 Coding Agent 与自动化边界

- `P2` · Locator `C12:508ab626:8d5c6baf:648:f1a0f47d` · Lines `866-866`

```text
- 将自身输出直接标为 RVR/RTR `Accepted`；
```

### 55. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.6 Tool 与权限

- `P2` · Locator `C09:6897694e:d3202194:293:71561ebf` · Lines `398-398`

```text
5. 未知版本、未知 Identity、未知租户、未知数据保留或未知副作用的 Tool 不得用于高风险 Action。
```

### 56. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.4 RUN Accepted 条件

- `P2` · Locator `C09:6897694e:d5731510:665:f0c18de4` · Lines `876-876`

```text
- 必需 Verification Result 满足 C05 要求；
```

### 57. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.13 Failure、Stop 与 Retry

- `P2` · Locator `C09:6897694e:7c53d277:377:47c6c8f5` · Lines `499-499`

```text
5. Retry 必须创建新 Attempt，记录原因、变化参数、修正、授权、幂等/副作用检查和结果。
```

### 58. C12 — C12 评审、质量门禁与产品健康规范 > 13. 产物必填信息 > 13.1 RVR — Review Record

- `P2` · Locator `C12:508ab626:59827610:710:9c7194f0` · Lines `968-968`

```text
- Start/End/Accepted Time；
```

### 59. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.6 Tool 与权限

- `P2` · Locator `C09:6897694e:d3202194:294:1da2eb1f` · Lines `399-399`

```text
6. Dry Run 只有在工具官方语义明确且未产生真实副作用时才能记录为 Dry Run；名称包含 `dry-run` 不构成证明。
```

### 60. C09 — C09 Agent 执行与证据规范 > 13. 必填信息 > 13.8 Failure or Exception Report

- `P2` · Locator `C09:6897694e:4e9aa10b:579:c2c77abc` · Lines `768-768`

```text
- 已发生副作用、Risk ID/Current Risk Level/Impact、Stop/STC/ESP；
```

### 61. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.5 阻断条件

- `P2` · Locator `C09:6897694e:434e9ab2:676:d20470e2` · Lines `890-890`

```text
- 破坏性/外部操作使用宽泛目标、未解析变量或未知副作用；
```

### 62. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.5 Step、Action 与 Attempt

- `P2` · Locator `C09:6897694e:e40e94e8:285:b1b8d8df` · Lines `388-388`

```text
6. Cancelled 必须记录取消 Authority、时间、已发生副作用和安全状态。
```

### 63. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.5 阻断条件

- `P2` · Locator `C09:6897694e:434e9ab2:683:62a587fd` · Lines `897-897`

```text
- 无法重建主要副作用、TaskContract Revision 或 End Snapshot。
```

### 64. C09 — C09 Agent 执行与证据规范 > 2. 目的

- `P2` · Locator `C09:6897694e:cd365db2:28:3dc3dc43` · Lines `37-37`

```text
3. 使会改变状态、失败、验证、产生外部副作用或影响门禁的 Tool Invocation 可追踪，同时避免记录低价值读取和敏感原文；
```

### 65. C11 — C11 配置、版本、基线与变更控制规范 > 19. P2 强制检查

- `P2` · Locator `C11:88ec56f7:40ea1806:1028:270e8ada` · Lines `1355-1355`

```text
| C11-P2-058 | Rollback 已验证 | 覆盖数据和外部副作用 |
```

### 66. C12 — C12 评审、质量门禁与产品健康规范 > 20. 附录：模板、清单、指标与条款映射 > 20.11 Gate Decision 清单

- `P2` · Locator `C12:508ab626:f1ebdf1f:1154:dc9d4317` · Lines `1877-1877`

```text
- [ ] RVR Accepted；
```

### 67. C09 — C09 Agent 执行与证据规范 > 20. 附录 > 20.13 Retry 与 Rollback 判定表

- `P2` · Locator `C09:6897694e:e0e42fcb:848:70ea76c0` · Lines `1314-1314`

```text
| 幂等、无副作用、参数不变、授权有效 | 按 AEP 新 Attempt | 不需要 | 保留原失败 |
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
