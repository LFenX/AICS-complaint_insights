# Clause Context: T-INSIGHTS-FOUNDATION-20261029-01 / plan_execution

- Status: `Expanded`
- Query digest: `6a5f1c1fd65c6f6806a8b6696b96473c42bc610b551f78670f79ac44b8c2c1d6`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `8/8`
- Budget: `19433/12000` chars
- Fallback: `section`

## Source Index

- `C09`: `references/02_核心规范/C09_Agent_Execution_and_Evidence_Standard.md` / `V6.3 Candidate` / SHA-256 `6897694e362bf48cb3a13bb4e68d79d7173945daad2ba3e8f0b6c75be944c01e`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `C11`: `references/02_核心规范/C11_Configuration_Version_Baseline_and_Change_Standard.md` / `V6.3 Candidate` / SHA-256 `88ec56f78f6d3da6f94b1684c7b1296ed1825bfcc961f0f8d3636c8c6a26f7e1`
- `VC-PPG-PRO-001`: `references/01_治理基线/Vibe_Coding_任务类型裁剪与统一执行流程规范_V6.3.md` / `V6.3 Candidate` / SHA-256 `548a810a1cbce4fc7970f87778c71f56c9d0921e3ba385a73d085b8ed0276329`
- `E03`: `references/03_扩展规范/E03_Data_and_AI_Data_Governance_Extension_Standard.md` / `V6.3 Candidate` / SHA-256 `bb6a10422c6e672f3f67e6dc109c5bfaa594b195924758b21911fe44a18c603b`
- `C05`: `references/02_核心规范/C05_Acceptance_Verification_and_Validation_Standard.md` / `V6.3 Candidate` / SHA-256 `7973bcb4ea442030772e36b7418cc1e03f55e0b3aaa6072f4ec1c198d1b537c7`

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

### 14. C11 — C11 配置、版本、基线与变更控制规范 > 8. 正式产物与唯一事实源 > 8.0 V6.3 三阶段修订与生成边界

- `P1` · Locator `C11:88ec56f7:0c539819:171:ee534cd3` · Lines `225-225`

```text
TaskContract 在首个 `run_started` Event 时冻结。之后 Scope、Acceptance、Authority、Plan 或 Task Profile 的变化必须增加 Revision 并写入 `amendments[]`，包含旧值、新值、原因、依据和时间。TaskOutcome 形成后采用同一纠错规则，禁止静默覆盖终态事实。
```

### 15. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.4 项目状态与唯一事实源

- `P1` · Locator `VC-PPG-PRO-001:548a810a:1708baa2:154:5db3cf5f` · Lines `201-201`

```text
| TaskContract/RunLedger/TaskOutcome Schema 与生成器 | `run-governed-product-workflow`；不得重定义上述语义 |
```

### 16. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:159:b3346062` · Lines `203-203`

```text
3. 空值禁止代替 Unknown、Not Applicable 或 Not Evaluated；
```

### 17. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:160:c7dfbc1b` · Lines `204-204`

```text
4. 未知的许可、Privacy、Security 或 Legal Hold 禁止由 Agent 推断；
```

### 18. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:161:22992d0f` · Lines `205-205`

```text
5. 未知阈值禁止由 Tool Default、行业惯例或任意百分比填充；
```

### 19. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:162:a8c014d8` · Lines `206-206`

```text
6. 未知 Consumer 禁止批准 Breaking Change；
```

### 20. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:163:bc86dfc6` · Lines `207-207`

```text
7. 未知 Dataset Revision 禁止作为训练、测试、RAG 或 Gate 输入。
```

### 21. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:249:f851c872` · Lines `315-315`

```text
Agent 禁止：
```

### 22. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:157:6b0fd6e7` · Lines `201-201`

```text
1. 字段不适用时必须记录理由、Scope、依据和批准人；
```

### 23. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:158:ddd9f24f` · Lines `202-202`

```text
2. 未知来源、许可、数据主体、Schema、Owner、阈值、Consumer、Lineage 或 Retention 必须显式标为 Pending/Unknown；
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

### 26. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:246:67a8b9f4` · Lines `311-311`

```text
- 汇总公开或已授权 Evidence；
```

### 27. C05 — C05 验收、验证与确认规范 > 10. 强制规则 > 10.15 Failure、Waiver、Risk Acceptance 与 Acceptance

- `P1` · Locator `C05:7973bcb4:8d60943e:337:23a84cb6` · Lines `492-492`

```text
2. Blocked 必须记录阻塞原因、解除条件、责任人和重新执行计划。
```

### 28. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 7. 角色与职责

- `P1` · Locator `VC-PPG-PRO-001:548a810a:fb42d478:90:88e4e04f` · Lines `119-119`

```text
| Agent | 检查环境和 Baseline；起草 TaskContract、Task Profile、Artifact Manifest、Evidence 汇总和检查结果 | 不得自批、虚构 Evidence 或扩大 Scope |
```

### 29. C09 — C09 Agent 执行与证据规范 > 13. 必填信息 > 13.1 通用必填信息

- `P1` · Locator `C09:6897694e:9e280442:495:28110c09` · Lines `663-663`

```text
TaskContract、RunLedger 和 TaskOutcome 必须满足对应 JSON Schema；独立 AuthorityAsset/DerivedView Profile 必须引用 VC-PPG-COM-002 第 3 章通用信息和第 3.1 节公共字段组。以下旧 Profile 字段作为兼容信息按需嵌入，不要求拆成九份文件。
```

### 30. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 15. 验证与符合性检查 > 15.2 执行就绪检查

- `P2` · Locator `VC-PPG-PRO-001:548a810a:8b9280f4:447:0541dcf7` · Lines `609-609`

```text
- 唯一执行计划已固定；
```

### 31. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 13. 三阶段记录必填信息 > 13.1 TaskContract / before.json

- `P2` · Locator `VC-PPG-PRO-001:548a810a:e16b56ff:388:719a0bb9` · Lines `528-528`

```text
- 唯一执行计划、验证、回退、Stop Condition；
```

### 32. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 13. 三阶段记录必填信息 > 13.3 RunLedger / run.jsonl

- `P2` · Locator `VC-PPG-PRO-001:548a810a:1fd4e52a:410:d238a05e` · Lines `557-557`

```text
RunLedger 禁止默认保存完整命令、完整输出、文件正文、Token、凭据或其他敏感值。需要保留原始日志时只保存受控 Evidence 引用。
```

### 33. C09 — C09 Agent 执行与证据规范 > 2. 目的

- `P2` · Locator `C09:6897694e:cd365db2:24:5c1c9a04` · Lines `31-31`

```text
本规范规定 Coding Agent 从需求理解、执行计划、工具调用、命令运行、资产修改、验证、失败、重试、回滚、人类复核到交付的可审计记录。
```

### 34. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 9. 生命周期或工作机制 > 9.1 统一八阶段主流程

- `P2` · Locator `VC-PPG-PRO-001:548a810a:3151121b:164:93f12644` · Lines `230-230`

```text
| S4 计划 | Scope 已固定到受控 Revision/Snapshot；Blocking Risk/Unknown 已处置；被触发设计输入达到所属规范的计划就绪条件 | 形成唯一执行计划；按 VC-PPG-TAIL-001 重新计算裁剪快照和阶段上下文；列步骤、目标、工具、路径、验证、回退、Stop 和 Gate；生产发布适用时固定 RBP、MAP Revision | `tailoring_resolution` 为 S4 或更晚、与 Task Profile/规则表哈希一致且无 blocker；计划可执行、可验证、可回退；所需事前批准可解析 |
```

### 35. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.17 敏感信息与日志

- `P2` · Locator `C09:6897694e:3b9b0163:413:c26a57d2` · Lines `543-543`

```text
2. 明文密钥、Token、密码、私钥、Session Cookie 和可复用认证材料禁止进入 AEP/RUN/TIL/VDR/FER/HRR 或 Raw Log。
```

### 36. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.0 V6.3 最小执行记录覆盖规则

- `P2` · Locator `C09:6897694e:b1dd146f:146:977f0a8f` · Lines `196-196`

```text
9. 明文密钥、Token、密码、私钥、Session Cookie 和可复用认证材料在所有情况下均禁止写入任务记录。
```

### 37. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.2 执行中记录：RunLedger

- `P2` · Locator `VC-PPG-PRO-001:548a810a:5963b45f:131:853657b7` · Lines `170-170`

```text
RunLedger 保存结构化摘要、时间、状态、结果码、Evidence 引用、副作用和脱敏说明；禁止默认保存完整命令输出、文件内容、凭据、Token 或其他敏感值。普通读取、目录查看和搜索不记录。Git Commit/Diff 作为变化证据引用，不要求在账本复制 Diff。
```

### 38. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.4 项目状态与唯一事实源

- `P2` · Locator `VC-PPG-PRO-001:548a810a:1708baa2:145:7e4a9199` · Lines `192-192`

```text
| 六类元类型、Task Profile 与 Artifact Manifest 术语 | VC-PPG-COM-001 |
```

### 39. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 9. 生命周期或工作机制 > 9.1 统一八阶段主流程

- `P2` · Locator `VC-PPG-PRO-001:548a810a:3151121b:163:1380db65` · Lines `229-229`

```text
| S3 条件深化 | `Proceed` 且专业触发成立 | 按任务类型深化产品、需求、验收、设计、扩展规范或影响分析 | 被触发规范的输入达到计划就绪；稳定资产已在 Artifact Manifest 中记录 `Reference`，不适用的正式类型已记录带规则依据的 `N/A` |
```

### 40. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 9. 生命周期或工作机制 > 9.1 统一八阶段主流程

- `P2` · Locator `VC-PPG-PRO-001:548a810a:3151121b:168:d332662e` · Lines `234-234`

```text
| S8 收尾 | 当前交付不再继续执行 | 形成 TaskOutcome，更新终态 Artifact Manifest、Trace、Change、遗留问题和后继项；重建 ProjectState 和派生审核视图 | 结果为 Implemented、Deferred、Cancelled、Blocked 或 Superseded；事实、Owner、理由和 Evidence 完整 |
```

### 41. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 10. 强制规则 > 10.7 DT-04 需求澄清流程

- `P2` · Locator `VC-PPG-PRO-001:548a810a:496786d5:238:d7656587` · Lines `327-327`

```text
4. 纯澄清没有实际产品变化时，TaskOutcome 记录未执行产品变更的事实、检查方法和范围，S7 记录无发布或运行观察范围的规则依据；相关 Profile 按 Artifact Manifest 规则使用 `N/A`，S6 执行需求质量复核而非产品验收。
```

### 42. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 10. 强制规则 > 10.16 Artifact Manifest 规则

- `P2` · Locator `VC-PPG-PRO-001:548a810a:57b857f9:295:147a1e63` · Lines `402-402`

```text
### 10.16 Artifact Manifest 规则
```

### 43. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 10. 强制规则 > 10.16 Artifact Manifest 规则

- `P2` · Locator `VC-PPG-PRO-001:548a810a:57b857f9:296:818dea02` · Lines `404-404`

```text
1. `Create/Revise` 只用于本任务实际创建或修订的权威实例。
```

### 44. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 10. 强制规则 > 10.16 Artifact Manifest 规则

- `P2` · Locator `VC-PPG-PRO-001:548a810a:57b857f9:297:9e228232` · Lines `405-405`

```text
2. `Reference` 必须解析到固定 Revision/Snapshot 和有效范围。
```

### 45. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 10. 强制规则 > 10.16 Artifact Manifest 规则

- `P2` · Locator `VC-PPG-PRO-001:548a810a:57b857f9:298:f27c9fb8` · Lines `406-406`

```text
3. `Generate` 只用于可从权威事实重建的矩阵、报告或查询视图。
```

### 46. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 10. 强制规则 > 10.16 Artifact Manifest 规则

- `P2` · Locator `VC-PPG-PRO-001:548a810a:57b857f9:299:a193fabe` · Lines `407-407`

```text
4. `On Event` 只在 Failure、Incident、Waiver、Risk Acceptance、Release 等事实发生后创建。
```

### 47. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 10. 强制规则 > 10.16 Artifact Manifest 规则

- `P2` · Locator `VC-PPG-PRO-001:548a810a:57b857f9:300:eac0ee9c` · Lines `408-408`

```text
5. `N/A` 必须记录规则和范围；Risk 为 High/Critical，或安全、隐私、数据、不可逆性、生产影响、Extension Trigger、Authority 任一项为 Unknown 时禁止使用。
```

### 48. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 10. 强制规则 > 10.16 Artifact Manifest 规则

- `P2` · Locator `VC-PPG-PRO-001:548a810a:57b857f9:301:cd6a381c` · Lines `409-409`

```text
6. Artifact Manifest 不复制全量 137 项 Profile；未列项必须能通过 VC-PPG-IDX-001 和 VC-PPG-MAP-001 解析。
```

### 49. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 10. 强制规则 > 10.16 Artifact Manifest 规则

- `P2` · Locator `VC-PPG-PRO-001:548a810a:57b857f9:302:476e6ab2` · Lines `410-410`

```text
7. 执行前 Manifest 位于 `before.json`；执行结束后实际动作和结果写入 `after.json`，禁止单独维护第三份 Manifest 文件。
```

### 50. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 10. 强制规则 > 10.16 Artifact Manifest 规则

- `P2` · Locator `VC-PPG-PRO-001:548a810a:57b857f9:303:97ba4c3c` · Lines `411-411`

```text
8. 终态 Manifest 不得删除执行前计划项，也不得改写其计划字段；只在原项上增加 Outcome。
```

### 51. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 10. 强制规则 > 10.16 Artifact Manifest 规则

- `P2` · Locator `VC-PPG-PRO-001:548a810a:57b857f9:304:59533946` · Lines `412-412`

```text
9. 终态 Manifest 可追加收尾时实际发生的资产，追加项的 Outcome 只能是 `Created / Revised / Referenced / Generated`；TaskOutcome 建立后的追加必须通过 Amendment 记录。
```

### 52. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 17. 裁剪规则 > 17.1 不可裁剪项

- `P2` · Locator `VC-PPG-PRO-001:548a810a:72144562:504:e94d0644` · Lines `681-681`

```text
- TaskContract/TaskOutcome 中的 Artifact Manifest；
```

### 53. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 10. 强制规则 > 10.1 分类顺序

- `P2` · Locator `VC-PPG-PRO-001:548a810a:72c75244:195:a5450b31` · Lines `269-269`

```text
10. 生成 TaskContract，其中包含 Artifact Manifest；
```

### 54. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 12. 最小物理产物与条件 Profile > 12.1 所有任务的最低集合

- `P2` · Locator `VC-PPG-PRO-001:548a810a:73fc5ef5:349:493812fb` · Lines `478-478`

```text
| 执行前 | TaskContract / `before.json` | 身份链、任务关系、目标、Scope、权限、Task Profile、Artifact Manifest、Acceptance、计划、验证、回退、Gate、Source Snapshot |
```

### 55. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 12. 最小物理产物与条件 Profile > 12.1 所有任务的最低集合

- `P2` · Locator `VC-PPG-PRO-001:548a810a:73fc5ef5:353:3cc70dc7` · Lines `483-483`

```text
Task Profile 和 Artifact Manifest 是 TaskContract/TaskOutcome 字段，不再是独立物理产物。长期需求、设计、决定、证据和基线按触发条件保存为 AuthorityAsset；审核报告、矩阵和索引保存为 DerivedView。
```

### 56. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 12. 最小物理产物与条件 Profile > 12.2 条件产物

- `P2` · Locator `VC-PPG-PRO-001:548a810a:7865df37:356:c9edd00e` · Lines `489-489`

```text
下表只汇总跨任务高频触发，不是 137 个领域 Profile 的第二套目录。未列 Profile 必须通过 VC-PPG-IDX-001、VC-PPG-MAP-001 和所属专业规范解析；专业触发一旦成立，即使本表未单列也必须进入 Artifact Manifest。
```

### 57. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 6. 术语与定义

- `P2` · Locator `VC-PPG-PRO-001:548a810a:8c711bde:78:8dac3976` · Lines `103-103`

```text
| TaskContract | 执行前目标、范围、权限、验收、计划、Task Profile 和 Artifact Manifest 的结构化契约 | Run 开始时冻结，后续变化通过 Amendment 留痕 |
```

### 58. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 6. 术语与定义

- `P2` · Locator `VC-PPG-PRO-001:548a810a:8c711bde:83:e93b46a0` · Lines `108-108`

```text
| 阶段缩短 | 某阶段的适用控制目标已由有效 Baseline 覆盖，或该阶段在当前 Scope 内无适用控制活动 | 阶段仍保留进入、活动与退出记录；必须记录覆盖或不适用依据、适用范围和关联 Artifact Manifest 项，不得对阶段使用产物实例动作 |
```

### 59. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 6. 术语与定义

- `P2` · Locator `VC-PPG-PRO-001:548a810a:8c711bde:84:4ffda6f8` · Lines `110-110`

```text
TaskContract、Task Profile、Artifact Manifest、RunLedger、TaskOutcome、ProjectState、Delivery Scenario、Development Type、Change Surface、Risk Level、Extension Trigger、Baseline Inheritance、Execution Mode 和五类实例动作的唯一术语来源是 VC-PPG-COM-001 与 VC-PPG-COM-002。
```

### 60. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 9. 生命周期或工作机制 > 9.3 最小流程与完整流程

- `P2` · Locator `VC-PPG-PRO-001:548a810a:a0be4851:178:e9b33fe0` · Lines `248-248`

```text
- 默认最小流程仍必须经过 S1、S2、S4、S6 和 S8。专业规范未触发时可以缩短 S3；没有执行动作时可以缩短 S5；没有发布或运行观察范围时可以缩短 S7。每个被缩短阶段仍必须在 TaskContract 或 TaskOutcome 记录适用性依据、活动事实和退出结论，相关 Profile 在 Artifact Manifest 中使用受控实例动作。
```

### 61. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.5 最低追踪关系

- `P2` · Locator `VC-PPG-PRO-001:548a810a:a1d7e147:157:ce3bb034` · Lines `206-219`

```text
流程必须能够追踪：

```text
ProjectID / WorkItemID / TaskID
  → TaskContract / Task Profile
  → Scope / Requirement / Change 来源
  → Artifact Manifest
  → RunLedger / Git Change
  → Changed Asset
  → Verification / Validation Evidence
  → Acceptance / Gate / Release Decision
  → TaskOutcome / Follow-up
  → ProjectState
```
```

### 62. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.1 执行前输入：TaskContract

- `P2` · Locator `VC-PPG-PRO-001:548a810a:b19a9e27:121:e6b6ff1c` · Lines `155-155`

```text
- Artifact Manifest。
```

### 63. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 13. 三阶段记录必填信息 > 13.4 TaskOutcome / after.json

- `P2` · Locator `VC-PPG-PRO-001:548a810a:bc3580a9:418:8373133f` · Lines `568-568`

```text
- 终态 Artifact Manifest 和 amendments。
```

### 64. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 15. 验证与符合性检查 > 15.1 流程就绪检查

- `P2` · Locator `VC-PPG-PRO-001:548a810a:d9098f34:443:933372cc` · Lines `602-602`

```text
- TaskContract 中的 Artifact Manifest 无无据 N/A；
```

### 65. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 13. 三阶段记录必填信息 > 13.1 TaskContract / before.json

- `P2` · Locator `VC-PPG-PRO-001:548a810a:e16b56ff:387:5832e0bf` · Lines `527-527`

```text
- Artifact Manifest；
```

### 66. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 8. 管理对象与关系 > 8.3 任务终态：TaskOutcome

- `P2` · Locator `VC-PPG-PRO-001:548a810a:f3e42a70:141:5641775f` · Lines `184-184`

```text
- 终态 Artifact Manifest。
```

### 67. VC-PPG-PRO-001 — 任务类型裁剪与统一执行流程规范 > 9. 生命周期或工作机制 > 9.2 转换规则

- `P2` · Locator `VC-PPG-PRO-001:548a810a:f68986e2:176:5fd38f5b` · Lines `244-244`

```text
7. 重新分类必须通过 TaskContract Amendment 更新 Task Profile、Artifact Manifest、影响分析和计划，不得只修改标签。
```

### 68. C09 — C09 Agent 执行与证据规范 > 12. V6.3 必需载体与条件 Profile

- `P2` · Locator `C09:6897694e:0a9756f4:487:4d7c2fae` · Lines `651-651`

```text
| TaskContract / `before.json` | 每个拟执行任务在 Run 前创建并冻结 | AEP、ECP、Scope、Authorization、计划、验证、回退和 Stop |
```

### 69. C09 — C09 Agent 执行与证据规范 > 17. P2 裁剪与扩展适用性 > 17.0 Task Profile 驱动的适用性

- `P2` · Locator `C09:6897694e:39226036:715:2dfd4b0a` · Lines `944-944`

```text
实际 Agent 变更任务必须具有 TaskContract 和 RunLedger；计划深化通过 TaskContract Amendment 更新，不创建第二份“执行方案”。重要运行事件进入 RunLedger，CAS/CCS/FER 语义进入 TaskOutcome；HRR/RRS 只在实际人类复核或剩余风险事件发生时 `On Event` 创建。
```

### 70. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.5 阻断条件

- `P2` · Locator `C09:6897694e:434e9ab2:683:62a587fd` · Lines `897-897`

```text
- 无法重建主要副作用、TaskContract Revision 或 End Snapshot。
```

### 71. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:806:76d821d4` · Lines `1054-1054`

```text
54. 是否能重建主要副作用、TaskContract Revision、Diff 和验证；
```

### 72. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.0 V6.3 最小执行记录覆盖规则

- `P2` · Locator `C09:6897694e:b1dd146f:138:10b8517c` · Lines `188-188`

```text
1. AEP 与 ECP 语义进入 TaskContract（`before.json`）。
```

### 73. C09 — C09 Agent 执行与证据规范 > 17. P2 裁剪与扩展适用性 > 17.2 未来档位

- `P2` · Locator `C09:6897694e:dd4b3fe5:724:03108851` · Lines `958-958`

```text
P1/P2 可以通过 TaskContract、RunLedger、TaskOutcome 和 DerivedView 联合展示旧 Profile 语义，但必须保留 Run/Event/Asset ID、关键动作、Evidence、Failure、Risk、State 和逻辑身份。HRR、RRS 在触发时仍需独立权威记录。
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
