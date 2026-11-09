# Clause Context: T-INSIGHTS-MCP-OPS-20261101-01 / edit_in_scope

- Status: `Expanded`
- Query digest: `a921194984082506c8fa88ef2d2f29ccc38bfc50a70a1e527ab5401faaa82652`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `7/7`
- Budget: `12811/12000` chars
- Fallback: `section`

## Source Index

- `C09`: `references/02_核心规范/C09_Agent_Execution_and_Evidence_Standard.md` / `V6.3 Candidate` / SHA-256 `6897694e362bf48cb3a13bb4e68d79d7173945daad2ba3e8f0b6c75be944c01e`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `C07`: `references/02_核心规范/C07_Human_Agent_Collaboration_Standard.md` / `V6.3 Candidate` / SHA-256 `a1fc4e903d8b690f938d6e8fdf45a57abff2e94bcefbdb9729db1914804f016a`
- `C05`: `references/02_核心规范/C05_Acceptance_Verification_and_Validation_Standard.md` / `V6.3 Candidate` / SHA-256 `7973bcb4ea442030772e36b7418cc1e03f55e0b3aaa6072f4ec1c198d1b537c7`
- `C11`: `references/02_核心规范/C11_Configuration_Version_Baseline_and_Change_Standard.md` / `V6.3 Candidate` / SHA-256 `88ec56f78f6d3da6f94b1684c7b1296ed1825bfcc961f0f8d3636c8c6a26f7e1`

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

### 14. C07 — C07 人机协作与责任规范 > 10. 强制规则 > 10.5 Execution Permission Class

- `P1` · Locator `C07:a1fc4e90:1e571bd7:277:a7e76ec7` · Lines `383-383`

```text
| Autonomous | 已在 COL/ARD/APM 明确允许，操作不触发批准事件，所有前置条件满足 | Agent 可在有效期与最大修改范围内执行并由 C09 记录 |
```

### 15. C05 — C05 验收、验证与确认规范 > 6. 术语与定义

- `P1` · Locator `C05:7973bcb4:642a9692:84:22ddbd6b` · Lines `118-118`

```text
| Acceptance Criteria Set | 在同一受控范围内组织 Criterion 的正式产物 | 使用 ACS 身份和 DOC 状态模型 |
```

### 16. C09 — C09 Agent 执行与证据规范 > 9. 生命周期与工作机制 > 9.7 Failure、Retry 与 Rollback

- `P1` · Locator `C09:6897694e:00fcee58:229:a4dd6a88` · Lines `313-313`

```text
任一 Failed/Blocked、非预期副作用、Stop、验证失败或证据缺失必须建立 FER。Retry 或 Rollback 只能在副作用、权限、Plan、风险和新鲜 Context 可判定时执行。
```

### 17. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.9 Impact Analysis

- `P1` · Locator `C11:88ec56f7:2470b427:382:c81a8d3c` · Lines `519-519`

```text
5. 数据删除、Schema 迁移、密钥轮换、模型变化和 Feature Flag 必须评估不可逆副作用；
```

### 18. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.6 Tool 与权限

- `P1` · Locator `C09:6897694e:d3202194:293:71561ebf` · Lines `398-398`

```text
5. 未知版本、未知 Identity、未知租户、未知数据保留或未知副作用的 Tool 不得用于高风险 Action。
```

### 19. C07 — C07 人机协作与责任规范 > 10. 强制规则 > 10.6 Autonomous 操作

- `P2` · Locator `C07:a1fc4e90:c8a022bf:291:234366cb` · Lines `402-402`

```text
7. 操作可审计，且不会产生未声明的外部副作用；
```

### 20. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:770:ff3aba72` · Lines `1018-1018`

```text
18. Tool 默认行为、缓存、重试和副作用是否可知；
```

### 21. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:793:27098503` · Lines `1041-1041`

```text
41. Retry 是否创建新 Attempt 并检查副作用/幂等；
```

### 22. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.10 变更捕获

- `P2` · Locator `C09:6897694e:2a3669f9:342:35ff06d3` · Lines `457-457`

```text
### 10.10 变更捕获
```

### 23. C07 — C07 人机协作与责任规范 > 10. 强制规则 > 10.10 最小权限与最大修改范围

- `P2` · Locator `C07:a1fc4e90:119952d1:347:fbca0803` · Lines `472-472`

```text
### 10.10 最小权限与最大修改范围
```

### 24. C09 — C09 Agent 执行与证据规范 > 14. 质量要求

- `P2` · Locator `C09:6897694e:0d3fa301:617:e3bea0af` · Lines `815-815`

```text
6. 原子：副作用、权限和失败不可分时拆分 Action/TIL；
```

### 25. C07 — C07 人机协作与责任规范 > 2. 目的

- `P2` · Locator `C07:a1fc4e90:c77e3c5d:30:307cd56b` · Lines `39-39`

```text
5. 使高影响、不可逆、破坏性、跨 Scope、安全、隐私、合规、生产和外部副作用操作获得有权人类批准；
```

### 26. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.5 Step、Action 与 Attempt

- `P2` · Locator `C09:6897694e:e40e94e8:281:25e39cb3` · Lines `384-384`

```text
2. 每个 Action 只承担一个可独立判定授权、副作用和结果的 Operation。
```

### 27. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:806:76d821d4` · Lines `1054-1054`

```text
54. 是否能重建主要副作用、TaskContract Revision、Diff 和验证；
```

### 28. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.3 RUN Completed 条件

- `P2` · Locator `C09:6897694e:4d4144f4:659:92f7e6dd` · Lines `866-866`

```text
- 未发生未记录副作用或 Evidence 缺口。
```

### 29. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.10 Release Ready

- `P2` · Locator `C12:508ab626:4e568be9:410:0916ecf2` · Lines `558-558`

```text
### 10.10 Release Ready
```

### 30. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.7 命令规范

- `P2` · Locator `C09:6897694e:824cdbf7:317:d95f8e3a` · Lines `427-427`

```text
6. 复合命令若任一部分具有副作用、独立权限或独立失败条件，必须拆分 Action/TIL。
```

### 31. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.13 Failure、Stop 与 Retry

- `P2` · Locator `C09:6897694e:7c53d277:379:a3f5a43c` · Lines `501-501`

```text
7. 非幂等或副作用未知的 Action 禁止自动 Retry。
```

### 32. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.0 V6.3 最小执行记录覆盖规则

- `P2` · Locator `C09:6897694e:b1dd146f:139:d80c7578` · Lines `189-189`

```text
2. RUN 与 TIL 语义进入只追加 RunLedger（`run.jsonl`）。普通读取、目录查看、搜索和未产生重要结果的无副作用调用不记录。
```

### 33. C07 — C07 人机协作与责任规范 > 9. 生命周期与工作机制 > 9.3 Boundary and Risk Review

- `P2` · Locator `C07:a1fc4e90:509cf2df:208:9a9a77d5` · Lines `283-283`

```text
4. 确认目标对象、环境、版本、最大修改范围和外部副作用。
```

### 34. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.7 命令规范

- `P2` · Locator `C09:6897694e:824cdbf7:320:956657f2` · Lines `430-430`

```text
9. 命令可重放记录不构成再次执行授权；重放前必须重新核验 Authorization、Context、Snapshot、Risk 和副作用。
```

### 35. C11 — C11 配置、版本、基线与变更控制规范 > 6. 术语与定义

- `P2` · Locator `C11:88ec56f7:7b574ff8:135:f0d09366` · Lines `178-178`

```text
| Rollback | 将当前系统或资产变更到一个先前已知配置的受控变更；不保证外部副作用或数据自动恢复 |
```

### 36. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.6 Tool 与权限

- `P2` · Locator `C09:6897694e:d3202194:292:80041ed7` · Lines `397-397`

```text
4. Tool 自动重试、缓存、会话记忆、插件、扩展、默认工作目录和外部副作用必须可知。
```

### 37. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.13 Failure、Stop 与 Retry

- `P2` · Locator `C09:6897694e:7c53d277:377:47c6c8f5` · Lines `499-499`

```text
5. Retry 必须创建新 Attempt，记录原因、变化参数、修正、授权、幂等/副作用检查和结果。
```

### 38. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.6 Tool 与权限

- `P2` · Locator `C09:6897694e:d3202194:294:1da2eb1f` · Lines `399-399`

```text
6. Dry Run 只有在工具官方语义明确且未产生真实副作用时才能记录为 Dry Run；名称包含 `dry-run` 不构成证明。
```

### 39. C09 — C09 Agent 执行与证据规范 > 13. 必填信息 > 13.8 Failure or Exception Report

- `P2` · Locator `C09:6897694e:4e9aa10b:579:c2c77abc` · Lines `768-768`

```text
- 已发生副作用、Risk ID/Current Risk Level/Impact、Stop/STC/ESP；
```

### 40. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.5 阻断条件

- `P2` · Locator `C09:6897694e:434e9ab2:676:d20470e2` · Lines `890-890`

```text
- 破坏性/外部操作使用宽泛目标、未解析变量或未知副作用；
```

### 41. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.5 Step、Action 与 Attempt

- `P2` · Locator `C09:6897694e:e40e94e8:285:b1b8d8df` · Lines `388-388`

```text
6. Cancelled 必须记录取消 Authority、时间、已发生副作用和安全状态。
```

### 42. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.5 阻断条件

- `P2` · Locator `C09:6897694e:434e9ab2:683:62a587fd` · Lines `897-897`

```text
- 无法重建主要副作用、TaskContract Revision 或 End Snapshot。
```

### 43. C09 — C09 Agent 执行与证据规范 > 2. 目的

- `P2` · Locator `C09:6897694e:cd365db2:28:3dc3dc43` · Lines `37-37`

```text
3. 使会改变状态、失败、验证、产生外部副作用或影响门禁的 Tool Invocation 可追踪，同时避免记录低价值读取和敏感原文；
```

### 44. C11 — C11 配置、版本、基线与变更控制规范 > 19. P2 强制检查

- `P2` · Locator `C11:88ec56f7:40ea1806:1028:270e8ada` · Lines `1355-1355`

```text
| C11-P2-058 | Rollback 已验证 | 覆盖数据和外部副作用 |
```

### 45. C11 — C11 配置、版本、基线与变更控制规范 > 20. 模板、清单与国际标准条款映射 > 20.18 国际标准条款映射

- `P2` · Locator `C11:88ec56f7:8e4eefa9:1171:d584ceb2` · Lines `1921-1921`

```text
| ISO 31000:2018 6.2 | 沟通和协商 | 10.9、10.10、10.14、10.17 |
```

### 46. C09 — C09 Agent 执行与证据规范 > 20. 附录 > 20.13 Retry 与 Rollback 判定表

- `P2` · Locator `C09:6897694e:e0e42fcb:848:70ea76c0` · Lines `1314-1314`

```text
| 幂等、无副作用、参数不变、授权有效 | 按 AEP 新 Attempt | 不需要 | 保留原失败 |
```

### 47. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.18 恢复与回滚

- `P2` · Locator `C11:88ec56f7:a8bfc8c2:521:6ef0c5b9` · Lines `693-693`

```text
4. Rollback 必须记录目标版本、实际动作、数据影响、外部副作用和验证；
```

### 48. C07 — C07 人机协作与责任规范 > 10. 强制规则 > 10.12 Stop Conditions 与 Fail-Closed

- `P2` · Locator `C07:a1fc4e90:1b37117b:373:ede0aec3` · Lines `505-505`

```text
| 结果异常 | 工具输出、变更数量、影响范围或副作用超出预期 | 停止后续步骤，保存证据 |
```

### 49. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.0 V6.3 最小执行记录覆盖规则

- `P2` · Locator `C09:6897694e:b1dd146f:145:abf147f6` · Lines `195-195`

```text
8. 默认只保存结构化摘要、时间、状态、Exit Code、Evidence 引用、外部副作用和脱敏说明。只有复核无法通过其他证据完成时，才把完整命令或原始输出作为受控 Evidence 保存。
```

### 50. C09 — C09 Agent 执行与证据规范 > 20. 附录 > 20.13 Retry 与 Rollback 判定表

- `P2` · Locator `C09:6897694e:e0e42fcb:849:001e668c` · Lines `1315-1315`

```text
| 副作用未知或外部状态未知 | 禁止自动 Retry | 先诊断 | FER、Stop |
```

### 51. C09 — C09 Agent 执行与证据规范 > 6. 术语与定义

- `P2` · Locator `C09:6897694e:041c2647:101:726215f4` · Lines `142-142`

```text
| Action | Step 内一次受授权 Operation，具有精确目标、输入、预期副作用和结果 | 一次 Action 可以产生一个 Tool Invocation；不可审计复合动作必须拆分 |
```

### 52. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.13 Failure、Stop 与 Retry

- `P2` · Locator `C09:6897694e:7c53d277:374:6e5e65e7` · Lines `496-496`

```text
2. FER 必须记录失败时间/步骤、症状、Error Evidence、影响、已发生副作用、即时处置、根因状态、升级和关闭条件。
```

### 53. C09 — C09 Agent 执行与证据规范 > 12. V6.3 必需载体与条件 Profile

- `P2` · Locator `C09:6897694e:0a9756f4:488:e528a9f5` · Lines `652-652`

```text
| RunLedger / `run.jsonl` | 每个实际 Run；无事件时允许空文件 | RUN、重要 TIL、失败、重试、验证、外部副作用和回滚事件 |
```

### 54. C07 — C07 人机协作与责任规范 > 10. 强制规则 > 10.7 必须批准的事件

- `P3` · Locator `C07:a1fc4e90:068b0058:296:40efb036` · Lines `409-409`

```text
### 10.7 必须批准的事件
```

### 55. C07 — C07 人机协作与责任规范 > 10. 强制规则 > 10.1 协作身份与边界

- `P3` · Locator `C07:a1fc4e90:4ccd2e53:242:3d80073d` · Lines `332-332`

```text
### 10.1 协作身份与边界
```

### 56. C07 — C07 人机协作与责任规范 > 10. 强制规则 > 10.4 八类操作与最低授权信息

- `P3` · Locator `C07:a1fc4e90:ccf93f5f:263:3f0ed148` · Lines `362-362`

```text
### 10.4 八类操作与最低授权信息
```

### 57. C07 — C07 人机协作与责任规范 > 10. 强制规则 > 10.8 Agent 禁止行为

- `P3` · Locator `C07:a1fc4e90:c58febea:310:00fe8124` · Lines `426-426`

```text
### 10.8 Agent 禁止行为
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
