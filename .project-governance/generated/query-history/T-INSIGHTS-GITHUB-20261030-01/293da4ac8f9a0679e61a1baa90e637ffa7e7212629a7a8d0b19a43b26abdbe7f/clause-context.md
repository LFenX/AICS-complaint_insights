# Clause Context: T-INSIGHTS-GITHUB-20261030-01 / edit_in_scope

- Status: `Expanded`
- Query digest: `293da4ac8f9a0679e61a1baa90e637ffa7e7212629a7a8d0b19a43b26abdbe7f`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `6/6`
- Budget: `17285/12000` chars
- Fallback: `section`

## Source Index

- `C09`: `references/02_核心规范/C09_Agent_Execution_and_Evidence_Standard.md` / `V6.3 Candidate` / SHA-256 `6897694e362bf48cb3a13bb4e68d79d7173945daad2ba3e8f0b6c75be944c01e`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `C07`: `references/02_核心规范/C07_Human_Agent_Collaboration_Standard.md` / `V6.3 Candidate` / SHA-256 `a1fc4e903d8b690f938d6e8fdf45a57abff2e94bcefbdb9729db1914804f016a`
- `E03`: `references/03_扩展规范/E03_Data_and_AI_Data_Governance_Extension_Standard.md` / `V6.3 Candidate` / SHA-256 `bb6a10422c6e672f3f67e6dc109c5bfaa594b195924758b21911fe44a18c603b`
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

### 14. C07 — C07 人机协作与责任规范 > 7. 参与者与职责 > 7.2 Agent 角色

- `P1` · Locator `C07:a1fc4e90:63ef8775:140:08fad459` · Lines `189-189`

```text
| Orchestrator Agent | 在授权范围内分解任务、分派子任务、收集结果和报告冲突 | 子 Agent 授权不得超过自身授权与子任务 Scope 的交集 |
```

### 15. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:252:8841a1d9` · Lines `319-319`

```text
- 擅自运行全表扫描、生产写入、回填、重标注、匿名化或删除；
```

### 16. E03 — E03 数据与 AI 数据治理扩展规范 > 1. 文档控制信息

- `P1` · Locator `E03:bb6a1042:ec6bb5ec:24:90277acf` · Lines `28-28`

```text
本文件在项目负责人批准前不得作为正式数据或 AI 数据治理约束。E03 当前未激活，不对本规范文档仓库强加目标产品数据治理控制；未激活不影响本文件必须编制、评审和建立 Git 基线。
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

### 24. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:158:ddd9f24f` · Lines `202-202`

```text
2. 未知来源、许可、数据主体、Schema、Owner、阈值、Consumer、Lineage 或 Retention 必须显式标为 Pending/Unknown；
```

### 25. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:242:958d7c5d` · Lines `306-306`

```text
Agent 可以：
```

### 26. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:253:70be0f3c` · Lines `320-320`

```text
- 推断未知许可、法律权属、PII 合法性或跨境允许性；
```

### 27. C09 — C09 Agent 执行与证据规范 > 20. 附录 > 20.15 正反例

- `P1` · Locator `C09:6897694e:517bf4ca:858:2e82b2de` · Lines `1348-1348`

```text
> RUN-0043 绑定 AEP-0043 Revision 2、REQ-031 Revision 4、ECP-0043 Revision 3、Commit `abc123` 和 ARD/APM 当前授权。Action RUN-0043-A003 使用 TIL-0187 记录参数化测试调用、工作目录、超时、Exit Code、stdout/stderr Digest 和实际结果。第一次 Attempt 因依赖超时失败，FER-0012 保留；确认无外部副作用后按 AEP 执行第二次 Attempt。CAS/CCS 固定 Diff 和 Result Commit；VDR 逐项记录 Expected/Actual，HRR 由独立人类基于当前 Revision 接受，未解决低 Risk 进入 RRS。
```

### 28. C11 — C11 配置、版本、基线与变更控制规范 > 8. 正式产物与唯一事实源 > 8.0 V6.3 三阶段修订与生成边界

- `P1` · Locator `C11:88ec56f7:0c539819:172:3b2cf7dd` · Lines `227-227`

```text
RunLedger 只追加；更正通过新 Event 引用原 Event。ProjectState 和 DerivedView 由生成器重建，禁止直接编辑或纳入独立变更源。Git Commit/Diff 可作为代码和文档变化的权威证据，但外部副作用、失败、验证环境、批准和决定必须由相应元类型或 AuthorityAsset 保存。
```

### 29. C09 — C09 Agent 执行与证据规范 > 9. 生命周期与工作机制 > 9.7 Failure、Retry 与 Rollback

- `P2` · Locator `C09:6897694e:00fcee58:229:a4dd6a88` · Lines `313-313`

```text
任一 Failed/Blocked、非预期副作用、Stop、验证失败或证据缺失必须建立 FER。Retry 或 Rollback 只能在副作用、权限、Plan、风险和新鲜 Context 可判定时执行。
```

### 30. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:630:6cc80eaa` · Lines `842-842`

```text
### 10.24 审核、管理评审与纠正
```

### 31. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:776:e764677d` · Lines `1024-1024`

```text
24. 未信任输入是否未通过字符串拼接进入命令；
```

### 32. C07 — C07 人机协作与责任规范 > 10. 强制规则 > 10.6 Autonomous 操作

- `P2` · Locator `C07:a1fc4e90:c8a022bf:291:234366cb` · Lines `402-402`

```text
7. 操作可审计，且不会产生未声明的外部副作用；
```

### 33. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:636:2b0ad86d` · Lines `849-849`

```text
6. 重复 Nonconformity 禁止只延长 Due；
```

### 34. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:635:b16c0d93` · Lines `848-848`

```text
5. Corrective Action 可以进入 IAP，但必须标记其来源和强制性；
```

### 35. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:770:ff3aba72` · Lines `1018-1018`

```text
18. Tool 默认行为、缓存、重试和副作用是否可知；
```

### 36. C12 — C12 评审、质量门禁与产品健康规范 > 3. 适用范围 > 3.2 蓝图必备主题映射

- `P2` · Locator `C12:508ab626:422f5c08:71:a0eedbb9` · Lines `90-90`

```text
| 审计 | 10.24、16 |
```

### 37. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:793:27098503` · Lines `1041-1041`

```text
41. Retry 是否创建新 Attempt 并检查副作用/幂等；
```

### 38. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:633:df69dc6c` · Lines `846-846`

```text
3. Audit Scope、Criteria、Sample、Independence 和 Finding 必须可复核；
```

### 39. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:637:ea5e64ad` · Lines `850-850`

```text
7. 审核结果禁止由被审核 Agent 自动接受；
```

### 40. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.9 Impact Analysis

- `P2` · Locator `C11:88ec56f7:2470b427:382:c81a8d3c` · Lines `519-519`

```text
5. 数据删除、Schema 迁移、密钥轮换、模型变化和 Feature Flag 必须评估不可逆副作用；
```

### 41. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:638:4dbf1bc2` · Lines `851-851`

```text
8. Audit/Management Review 不建立新的 C12 正式产物类型。
```

### 42. C07 — C07 人机协作与责任规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C07:a1fc4e90:1e6c56d2:727:0afe1cde` · Lines `971-971`

```text
24. ESP 是否有通知目标、时限、决定 Authority 和替代路线；
```

### 43. C09 — C09 Agent 执行与证据规范 > 14. 质量要求

- `P2` · Locator `C09:6897694e:0d3fa301:617:e3bea0af` · Lines `815-815`

```text
6. 原子：副作用、权限和失败不可分时拆分 Action/TIL；
```

### 44. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:634:78a3c905` · Lines `847-847`

```text
4. Nonconformity 必须控制当前影响、分析原因、识别类似问题、执行纠正并验证有效性；
```

### 45. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:631:455a044f` · Lines `844-844`

```text
1. Internal Audit 使用 RVR，Review Type=`Internal Audit`；
```

### 46. C07 — C07 人机协作与责任规范 > 2. 目的

- `P2` · Locator `C07:a1fc4e90:c77e3c5d:30:307cd56b` · Lines `39-39`

```text
5. 使高影响、不可逆、破坏性、跨 Scope、安全、隐私、合规、生产和外部副作用操作获得有权人类批准；
```

### 47. C12 — C12 评审、质量门禁与产品健康规范 > 20. 附录：模板、清单、指标与条款映射 > 20.18 国际标准条款映射

- `P2` · Locator `C12:508ab626:a0723fde:1236:62fc9869` · Lines `2051-2051`

```text
| ISO 9001:2015 第 9.2 章 | 内部审核 | 10.24 |
```

### 48. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.5 Step、Action 与 Attempt

- `P2` · Locator `C09:6897694e:e40e94e8:281:25e39cb3` · Lines `384-384`

```text
2. 每个 Action 只承担一个可独立判定授权、副作用和结果的 Operation。
```

### 49. C12 — C12 评审、质量门禁与产品健康规范 > 20. 附录：模板、清单、指标与条款映射 > 20.18 国际标准条款映射

- `P2` · Locator `C12:508ab626:a0723fde:1237:711d3055` · Lines `2052-2052`

```text
| ISO 9001:2015 第 9.3 章 | 管理评审 | 10.24、14.5 |
```

### 50. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:806:76d821d4` · Lines `1054-1054`

```text
54. 是否能重建主要副作用、TaskContract Revision、Diff 和验证；
```

### 51. C12 — C12 评审、质量门禁与产品健康规范 > 20. 附录：模板、清单、指标与条款映射 > 20.18 国际标准条款映射

- `P2` · Locator `C12:508ab626:a0723fde:1292:f1fd00a2` · Lines `2107-2107`

```text
| ISO/IEC 42001:2023 第 10 章 | 改进 | 10.22 至 10.24 |
```

### 52. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.3 RUN Completed 条件

- `P2` · Locator `C09:6897694e:4d4144f4:659:92f7e6dd` · Lines `866-866`

```text
- 未发生未记录副作用或 Evidence 缺口。
```

### 53. C12 — C12 评审、质量门禁与产品健康规范 > 20. 附录：模板、清单、指标与条款映射 > 20.18 国际标准条款映射

- `P2` · Locator `C12:508ab626:a0723fde:1239:00f4815d` · Lines `2054-2054`

```text
| ISO 9001:2015 第 10.2 章 | 不符合与纠正措施 | 10.3、10.23、10.24 |
```

### 54. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.7 命令规范

- `P2` · Locator `C09:6897694e:824cdbf7:317:d95f8e3a` · Lines `427-427`

```text
6. 复合命令若任一部分具有副作用、独立权限或独立失败条件，必须拆分 Action/TIL。
```

### 55. C12 — C12 评审、质量门禁与产品健康规范 > 10. 强制规则 > 10.24 审核、管理评审与纠正

- `P2` · Locator `C12:508ab626:8bc9bc0e:632:ebc052a8` · Lines `845-845`

```text
2. Management Review 使用 RVR，必须消费 PHR、Gate、Waiver、RAR、Finding、Incident 和 IAP；
```

### 56. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.13 Failure、Stop 与 Retry

- `P2` · Locator `C09:6897694e:7c53d277:379:a3f5a43c` · Lines `501-501`

```text
7. 非幂等或副作用未知的 Action 禁止自动 Retry。
```

### 57. C12 — C12 评审、质量门禁与产品健康规范 > 20. 附录：模板、清单、指标与条款映射 > 20.18 国际标准条款映射

- `P2` · Locator `C12:508ab626:a0723fde:1291:fbe66b2e` · Lines `2106-2106`

```text
| ISO/IEC 42001:2023 第 9 章 | 绩效评价 | 10.15 至 10.21、10.24 |
```

### 58. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.0 V6.3 最小执行记录覆盖规则

- `P2` · Locator `C09:6897694e:b1dd146f:139:d80c7578` · Lines `189-189`

```text
2. RUN 与 TIL 语义进入只追加 RunLedger（`run.jsonl`）。普通读取、目录查看、搜索和未产生重要结果的无副作用调用不记录。
```

### 59. C07 — C07 人机协作与责任规范 > 9. 生命周期与工作机制 > 9.3 Boundary and Risk Review

- `P2` · Locator `C07:a1fc4e90:509cf2df:208:9a9a77d5` · Lines `283-283`

```text
4. 确认目标对象、环境、版本、最大修改范围和外部副作用。
```

### 60. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.7 命令规范

- `P2` · Locator `C09:6897694e:824cdbf7:320:956657f2` · Lines `430-430`

```text
9. 命令可重放记录不构成再次执行授权；重放前必须重新核验 Authorization、Context、Snapshot、Risk 和副作用。
```

### 61. C11 — C11 配置、版本、基线与变更控制规范 > 2. 目的

- `P2` · Locator `C11:88ec56f7:1e72336b:27:7c14c8ba` · Lines `36-36`

```text
1. 使业务身份与文件路径、数据库键、URL、Git Commit、版本号和状态分离；
```

### 62. C09 — C09 Agent 执行与证据规范 > 20. 附录 > 20.6 Code Change Summary 模板

- `P2` · Locator `C09:6897694e:2f848604:820:3a705f44` · Lines `1182-1199`

```text
### 20.6 Code Change Summary 模板

```markdown
# CCS-<NNNN> <Code Change>

<通用头部；State 使用 REC>

| Run / Repo / Base Commit / Result Commit / Branch / Dirty State | |
|---|---|
| File / Component / Module / Change Type | |
| Code Change / Behavior Impact | |
| Requirement / Design / Decision / Engineering Change | |
| Interface / Data / Security / Performance / Compatibility | |
| Dependency / Lockfile / Generated / Migration / Config | |
| Test / Static / Build / Scan / VDR / VER | |
| Deployment / Migration / Rollback / Operational Impact | |
| Reviewer / Diff / PR / Commit / History | |
```
```

### 63. C11 — C11 配置、版本、基线与变更控制规范 > 6. 术语与定义

- `P2` · Locator `C11:88ec56f7:7b574ff8:135:f0d09366` · Lines `178-178`

```text
| Rollback | 将当前系统或资产变更到一个先前已知配置的受控变更；不保证外部副作用或数据自动恢复 |
```

### 64. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.6 Tool 与权限

- `P2` · Locator `C09:6897694e:d3202194:292:80041ed7` · Lines `397-397`

```text
4. Tool 自动重试、缓存、会话记忆、插件、扩展、默认工作目录和外部副作用必须可知。
```

### 65. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.6 Tool 与权限

- `P2` · Locator `C09:6897694e:d3202194:293:71561ebf` · Lines `398-398`

```text
5. 未知版本、未知 Identity、未知租户、未知数据保留或未知副作用的 Tool 不得用于高风险 Action。
```

### 66. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.13 Failure、Stop 与 Retry

- `P2` · Locator `C09:6897694e:7c53d277:377:47c6c8f5` · Lines `499-499`

```text
5. Retry 必须创建新 Attempt，记录原因、变化参数、修正、授权、幂等/副作用检查和结果。
```

### 67. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.6 Tool 与权限

- `P2` · Locator `C09:6897694e:d3202194:294:1da2eb1f` · Lines `399-399`

```text
6. Dry Run 只有在工具官方语义明确且未产生真实副作用时才能记录为 Dry Run；名称包含 `dry-run` 不构成证明。
```

### 68. C09 — C09 Agent 执行与证据规范 > 13. 必填信息 > 13.8 Failure or Exception Report

- `P2` · Locator `C09:6897694e:4e9aa10b:579:c2c77abc` · Lines `768-768`

```text
- 已发生副作用、Risk ID/Current Risk Level/Impact、Stop/STC/ESP；
```

### 69. C11 — C11 配置、版本、基线与变更控制规范 > 13. 必填信息规范 > 13.4 SNP — Snapshot Record

- `P2` · Locator `C11:88ec56f7:7ef5a391:667:06cfcbcc` · Lines `906-906`

```text
- Commit/Object/Artifact/Data/Model Reference；
```

### 70. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.5 阻断条件

- `P2` · Locator `C09:6897694e:434e9ab2:676:d20470e2` · Lines `890-890`

```text
- 破坏性/外部操作使用宽泛目标、未解析变量或未知副作用；
```

### 71. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.5 Step、Action 与 Attempt

- `P2` · Locator `C09:6897694e:e40e94e8:285:b1b8d8df` · Lines `388-388`

```text
6. Cancelled 必须记录取消 Authority、时间、已发生副作用和安全状态。
```

### 72. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.5 阻断条件

- `P2` · Locator `C09:6897694e:434e9ab2:683:62a587fd` · Lines `897-897`

```text
- 无法重建主要副作用、TaskContract Revision 或 End Snapshot。
```

### 73. C09 — C09 Agent 执行与证据规范 > 2. 目的

- `P2` · Locator `C09:6897694e:cd365db2:28:3dc3dc43` · Lines `37-37`

```text
3. 使会改变状态、失败、验证、产生外部副作用或影响门禁的 Tool Invocation 可追踪，同时避免记录低价值读取和敏感原文；
```

### 74. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.5 Snapshot 与完整性

- `P2` · Locator `C11:88ec56f7:09c87bbf:296:7605d976` · Lines `409-409`

```text
- 解析后的 Commit/Object ID，不只记录 Branch/Tag；
```

### 75. C11 — C11 配置、版本、基线与变更控制规范 > 19. P2 强制检查

- `P2` · Locator `C11:88ec56f7:40ea1806:988:ab21e73e` · Lines `1315-1315`

```text
| C11-P2-018 | 实际变化可追 | 有 C09 Diff/Commit/Artifact |
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
