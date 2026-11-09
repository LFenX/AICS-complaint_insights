# Clause Context: T-INSIGHTS-GITHUB-20261030-01 / edit_in_scope

- Status: `Expanded`
- Query digest: `a763aeaef4a627dd69233f8985aaf2f49101a46dd789918f7b796a9df98ba511`
- Index digest: `6ecc4a89f2c95a0331c2718b576f62e5e5a60131795d61caad8bcd4327a8a94c`
- Coverage: `7/7`
- Budget: `18327/12000` chars
- Fallback: `section`

## Source Index

- `C09`: `references/02_核心规范/C09_Agent_Execution_and_Evidence_Standard.md` / `V6.3 Candidate` / SHA-256 `6897694e362bf48cb3a13bb4e68d79d7173945daad2ba3e8f0b6c75be944c01e`
- `C12`: `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` / `V6.3 Candidate` / SHA-256 `508ab6263bb1db5b1568cb16233ce7413a51da2f73bbe9eb39a56c9ad08d5565`
- `C07`: `references/02_核心规范/C07_Human_Agent_Collaboration_Standard.md` / `V6.3 Candidate` / SHA-256 `a1fc4e903d8b690f938d6e8fdf45a57abff2e94bcefbdb9729db1914804f016a`
- `C05`: `references/02_核心规范/C05_Acceptance_Verification_and_Validation_Standard.md` / `V6.3 Candidate` / SHA-256 `7973bcb4ea442030772e36b7418cc1e03f55e0b3aaa6072f4ec1c198d1b537c7`
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

### 15. C05 — C05 验收、验证与确认规范 > 6. 术语与定义

- `P1` · Locator `C05:7973bcb4:642a9692:84:22ddbd6b` · Lines `118-118`

```text
| Acceptance Criteria Set | 在同一受控范围内组织 Criterion 的正式产物 | 使用 ACS 身份和 DOC 状态模型 |
```

### 16. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:252:8841a1d9` · Lines `319-319`

```text
- 擅自运行全表扫描、生产写入、回填、重标注、匿名化或删除；
```

### 17. E03 — E03 数据与 AI 数据治理扩展规范 > 4. 不适用范围

- `P1` · Locator `E03:bb6a1042:0732837e:108:d69a88ca` · Lines `132-132`

```text
E03 可以消费上述事实，但禁止：
```

### 18. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:159:b3346062` · Lines `203-203`

```text
3. 空值禁止代替 Unknown、Not Applicable 或 Not Evaluated；
```

### 19. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:160:c7dfbc1b` · Lines `204-204`

```text
4. 未知的许可、Privacy、Security 或 Legal Hold 禁止由 Agent 推断；
```

### 20. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:161:22992d0f` · Lines `205-205`

```text
5. 未知阈值禁止由 Tool Default、行业惯例或任意百分比填充；
```

### 21. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:162:a8c014d8` · Lines `206-206`

```text
6. 未知 Consumer 禁止批准 Breaking Change；
```

### 22. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:163:bc86dfc6` · Lines `207-207`

```text
7. 未知 Dataset Revision 禁止作为训练、测试、RAG 或 Gate 输入。
```

### 23. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:249:f851c872` · Lines `315-315`

```text
Agent 禁止：
```

### 24. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:157:6b0fd6e7` · Lines `201-201`

```text
1. 字段不适用时必须记录理由、Scope、依据和批准人；
```

### 25. E03 — E03 数据与 AI 数据治理扩展规范 > 5. 规范性用语与受控判定 > 5.5 不适用和未知规则

- `P1` · Locator `E03:bb6a1042:41d8365f:158:ddd9f24f` · Lines `202-202`

```text
2. 未知来源、许可、数据主体、Schema、Owner、阈值、Consumer、Lineage 或 Retention 必须显式标为 Pending/Unknown；
```

### 26. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:242:958d7c5d` · Lines `306-306`

```text
Agent 可以：
```

### 27. E03 — E03 数据与 AI 数据治理扩展规范 > 7. 角色、职责与职责分离 > 7.3 Agent 使用规则

- `P1` · Locator `E03:bb6a1042:91ca75d1:253:70be0f3c` · Lines `320-320`

```text
- 推断未知许可、法律权属、PII 合法性或跨境允许性；
```

### 28. C09 — C09 Agent 执行与证据规范 > 20. 附录 > 20.15 正反例

- `P1` · Locator `C09:6897694e:517bf4ca:858:2e82b2de` · Lines `1348-1348`

```text
> RUN-0043 绑定 AEP-0043 Revision 2、REQ-031 Revision 4、ECP-0043 Revision 3、Commit `abc123` 和 ARD/APM 当前授权。Action RUN-0043-A003 使用 TIL-0187 记录参数化测试调用、工作目录、超时、Exit Code、stdout/stderr Digest 和实际结果。第一次 Attempt 因依赖超时失败，FER-0012 保留；确认无外部副作用后按 AEP 执行第二次 Attempt。CAS/CCS 固定 Diff 和 Result Commit；VDR 逐项记录 Expected/Actual，HRR 由独立人类基于当前 Revision 接受，未解决低 Risk 进入 RRS。
```

### 29. C11 — C11 配置、版本、基线与变更控制规范 > 8. 正式产物与唯一事实源 > 8.0 V6.3 三阶段修订与生成边界

- `P1` · Locator `C11:88ec56f7:0c539819:172:3b2cf7dd` · Lines `227-227`

```text
RunLedger 只追加；更正通过新 Event 引用原 Event。ProjectState 和 DerivedView 由生成器重建，禁止直接编辑或纳入独立变更源。Git Commit/Diff 可作为代码和文档变化的权威证据，但外部副作用、失败、验证环境、批准和决定必须由相应元类型或 AuthorityAsset 保存。
```

### 30. C09 — C09 Agent 执行与证据规范 > 9. 生命周期与工作机制 > 9.7 Failure、Retry 与 Rollback

- `P2` · Locator `C09:6897694e:00fcee58:229:a4dd6a88` · Lines `313-313`

```text
任一 Failed/Blocked、非预期副作用、Stop、验证失败或证据缺失必须建立 FER。Retry 或 Rollback 只能在副作用、权限、Plan、风险和新鲜 Context 可判定时执行。
```

### 31. C07 — C07 人机协作与责任规范 > 10. 强制规则 > 10.6 Autonomous 操作

- `P2` · Locator `C07:a1fc4e90:c8a022bf:291:234366cb` · Lines `402-402`

```text
7. 操作可审计，且不会产生未声明的外部副作用；
```

### 32. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:770:ff3aba72` · Lines `1018-1018`

```text
18. Tool 默认行为、缓存、重试和副作用是否可知；
```

### 33. C11 — C11 配置、版本、基线与变更控制规范 > 2. 目的

- `P2` · Locator `C11:88ec56f7:1e72336b:27:7c14c8ba` · Lines `36-36`

```text
1. 使业务身份与文件路径、数据库键、URL、Git Commit、版本号和状态分离；
```

### 34. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:793:27098503` · Lines `1041-1041`

```text
41. Retry 是否创建新 Attempt 并检查副作用/幂等；
```

### 35. C09 — C09 Agent 执行与证据规范 > 20. 附录 > 20.6 Code Change Summary 模板

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

### 36. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.9 Impact Analysis

- `P2` · Locator `C11:88ec56f7:2470b427:382:c81a8d3c` · Lines `519-519`

```text
5. 数据删除、Schema 迁移、密钥轮换、模型变化和 Feature Flag 必须评估不可逆副作用；
```

### 37. C09 — C09 Agent 执行与证据规范 > 14. 质量要求

- `P2` · Locator `C09:6897694e:0d3fa301:617:e3bea0af` · Lines `815-815`

```text
6. 原子：副作用、权限和失败不可分时拆分 Action/TIL；
```

### 38. C11 — C11 配置、版本、基线与变更控制规范 > 13. 必填信息规范 > 13.4 SNP — Snapshot Record

- `P2` · Locator `C11:88ec56f7:7ef5a391:667:06cfcbcc` · Lines `906-906`

```text
- Commit/Object/Artifact/Data/Model Reference；
```

### 39. C07 — C07 人机协作与责任规范 > 2. 目的

- `P2` · Locator `C07:a1fc4e90:c77e3c5d:30:307cd56b` · Lines `39-39`

```text
5. 使高影响、不可逆、破坏性、跨 Scope、安全、隐私、合规、生产和外部副作用操作获得有权人类批准；
```

### 40. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.5 Step、Action 与 Attempt

- `P2` · Locator `C09:6897694e:e40e94e8:281:25e39cb3` · Lines `384-384`

```text
2. 每个 Action 只承担一个可独立判定授权、副作用和结果的 Operation。
```

### 41. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:806:76d821d4` · Lines `1054-1054`

```text
54. 是否能重建主要副作用、TaskContract Revision、Diff 和验证；
```

### 42. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.3 RUN Completed 条件

- `P2` · Locator `C09:6897694e:4d4144f4:659:92f7e6dd` · Lines `866-866`

```text
- 未发生未记录副作用或 Evidence 缺口。
```

### 43. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.5 Snapshot 与完整性

- `P2` · Locator `C11:88ec56f7:09c87bbf:296:7605d976` · Lines `409-409`

```text
- 解析后的 Commit/Object ID，不只记录 Branch/Tag；
```

### 44. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.7 命令规范

- `P2` · Locator `C09:6897694e:824cdbf7:317:d95f8e3a` · Lines `427-427`

```text
6. 复合命令若任一部分具有副作用、独立权限或独立失败条件，必须拆分 Action/TIL。
```

### 45. C11 — C11 配置、版本、基线与变更控制规范 > 19. P2 强制检查

- `P2` · Locator `C11:88ec56f7:40ea1806:988:ab21e73e` · Lines `1315-1315`

```text
| C11-P2-018 | 实际变化可追 | 有 C09 Diff/Commit/Artifact |
```

### 46. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.13 Failure、Stop 与 Retry

- `P2` · Locator `C09:6897694e:7c53d277:379:a3f5a43c` · Lines `501-501`

```text
7. 非幂等或副作用未知的 Action 禁止自动 Retry。
```

### 47. C11 — C11 配置、版本、基线与变更控制规范 > 13. 必填信息规范 > 13.3 VRR — Version or Revision Record

- `P2` · Locator `C11:88ec56f7:7ccabe1f:652:d2c5da87` · Lines `888-888`

```text
- C09 Run、Actual Diff、Commit/Artifact；
```

### 48. C09 — C09 Agent 执行与证据规范 > 8. 治理对象与关系 > 8.0 V6.3 最小执行记录覆盖规则

- `P2` · Locator `C09:6897694e:b1dd146f:139:d80c7578` · Lines `189-189`

```text
2. RUN 与 TIL 语义进入只追加 RunLedger（`run.jsonl`）。普通读取、目录查看、搜索和未产生重要结果的无副作用调用不记录。
```

### 49. C09 — C09 Agent 执行与证据规范 > 13. 必填信息 > 13.5 Changed Artifact Summary

- `P2` · Locator `C09:6897694e:0e1c6687:545:1d5f11d8` · Lines `725-725`

```text
- Diff/Manifest/Digest/Commit；
```

### 50. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.20 Coding Agent 与自动化边界

- `P2` · Locator `C11:88ec56f7:12b8f4f0:551:ac3667cc` · Lines `732-732`

```text
- 解析 Commit、Digest、Dependency、Diff 和环境元数据；
```

### 51. C07 — C07 人机协作与责任规范 > 9. 生命周期与工作机制 > 9.3 Boundary and Risk Review

- `P2` · Locator `C07:a1fc4e90:509cf2df:208:9a9a77d5` · Lines `283-283`

```text
4. 确认目标对象、环境、版本、最大修改范围和外部副作用。
```

### 52. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.7 命令规范

- `P2` · Locator `C09:6897694e:824cdbf7:320:956657f2` · Lines `430-430`

```text
9. 命令可重放记录不构成再次执行授权；重放前必须重新核验 Authorization、Context、Snapshot、Risk 和副作用。
```

### 53. C07 — C07 人机协作与责任规范 > 10. 强制规则 > 10.4 八类操作与最低授权信息

- `P2` · Locator `C07:a1fc4e90:ccf93f5f:268:4e1b32d0` · Lines `370-370`

```text
| Modify | 允许对象、基线或 Commit、字段/路径边界、最大修改规模、不受影响边界 |
```

### 54. C11 — C11 配置、版本、基线与变更控制规范 > 6. 术语与定义

- `P2` · Locator `C11:88ec56f7:7b574ff8:135:f0d09366` · Lines `178-178`

```text
| Rollback | 将当前系统或资产变更到一个先前已知配置的受控变更；不保证外部副作用或数据自动恢复 |
```

### 55. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.6 Tool 与权限

- `P2` · Locator `C09:6897694e:d3202194:292:80041ed7` · Lines `397-397`

```text
4. Tool 自动重试、缓存、会话记忆、插件、扩展、默认工作目录和外部副作用必须可知。
```

### 56. C09 — C09 Agent 执行与证据规范 > 19. 符合性检查 > 19.2 强制检查项

- `P2` · Locator `C09:6897694e:4fe40d94:761:1fc611dd` · Lines `1009-1009`

```text
9. Workspace/Commit/Dirty/Untracked/Environment Snapshot 是否固定；
```

### 57. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.6 Tool 与权限

- `P2` · Locator `C09:6897694e:d3202194:293:71561ebf` · Lines `398-398`

```text
5. 未知版本、未知 Identity、未知租户、未知数据保留或未知副作用的 Tool 不得用于高风险 Action。
```

### 58. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.12 受控实施

- `P2` · Locator `C11:88ec56f7:018a2dec:421:09de5d5f` · Lines `569-569`

```text
3. 实际命令、Exit Code、stdout/stderr 摘要、Diff、Commit、Artifact 和异常必须记录；
```

### 59. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.13 Failure、Stop 与 Retry

- `P2` · Locator `C09:6897694e:7c53d277:377:47c6c8f5` · Lines `499-499`

```text
5. Retry 必须创建新 Attempt，记录原因、变化参数、修正、授权、幂等/副作用检查和结果。
```

### 60. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.3 身份、Version、Revision、Snapshot 与 Baseline 分离

- `P2` · Locator `C11:88ec56f7:4472cf93:264:0b90035b` · Lines `369-369`

```text
7. BSL 的批准对象是集合，不是单个 Commit 名称；
```

### 61. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.6 Tool 与权限

- `P2` · Locator `C09:6897694e:d3202194:294:1da2eb1f` · Lines `399-399`

```text
6. Dry Run 只有在工具官方语义明确且未产生真实副作用时才能记录为 Dry Run；名称包含 `dry-run` 不构成证明。
```

### 62. C09 — C09 Agent 执行与证据规范 > 13. 必填信息 > 13.3 Agent Run Record

- `P2` · Locator `C09:6897694e:84b2f622:521:31127493` · Lines `695-695`

```text
- CAS/CCS、Diff、Commit、External Change；
```

### 63. C09 — C09 Agent 执行与证据规范 > 9. 生命周期与工作机制 > 9.2 Run Intake

- `P2` · Locator `C09:6897694e:96832846:198:397330f9` · Lines `268-268`

```text
- C11 仓库、Commit、工作区、配置、环境和数据 Snapshot；
```

### 64. C09 — C09 Agent 执行与证据规范 > 13. 必填信息 > 13.8 Failure or Exception Report

- `P2` · Locator `C09:6897694e:4e9aa10b:579:c2c77abc` · Lines `768-768`

```text
- 已发生副作用、Risk ID/Current Risk Level/Impact、Stop/STC/ESP；
```

### 65. C09 — C09 Agent 执行与证据规范 > 13. 必填信息 > 13.6 Code Change Summary

- `P2` · Locator `C09:6897694e:f2244870:558:cb1b0f74` · Lines `741-741`

```text
- Reviewer、Diff/PR/Commit；
```

### 66. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.5 阻断条件

- `P2` · Locator `C09:6897694e:434e9ab2:676:d20470e2` · Lines `890-890`

```text
- 破坏性/外部操作使用宽泛目标、未解析变量或未知副作用；
```

### 67. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.5 Step、Action 与 Attempt

- `P2` · Locator `C09:6897694e:e40e94e8:285:b1b8d8df` · Lines `388-388`

```text
6. Cancelled 必须记录取消 Authority、时间、已发生副作用和安全状态。
```

### 68. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.2 永久标识与命名空间

- `P2` · Locator `C11:88ec56f7:51435be3:251:0779542a` · Lines `354-354`

```text
5. 文件名、目录、URL、数据库主键、工单号、Branch、Tag、Commit 或制品坐标不得替代 Asset ID；
```

### 69. C09 — C09 Agent 执行与证据规范 > 15. 评审、批准与 Run 接受 > 15.5 阻断条件

- `P2` · Locator `C09:6897694e:434e9ab2:683:62a587fd` · Lines `897-897`

```text
- 无法重建主要副作用、TaskContract Revision 或 End Snapshot。
```

### 70. C09 — C09 Agent 执行与证据规范 > 2. 目的

- `P2` · Locator `C09:6897694e:cd365db2:28:3dc3dc43` · Lines `37-37`

```text
3. 使会改变状态、失败、验证、产生外部副作用或影响门禁的 Tool Invocation 可追踪，同时避免记录低价值读取和敏感原文；
```

### 71. C09 — C09 Agent 执行与证据规范 > 10. 强制规则 > 10.2 执行前检查

- `P2` · Locator `C09:6897694e:b953534e:251:86a85667` · Lines `345-345`

```text
- 仓库、Commit、Dirty State、未跟踪变化、环境、配置和数据 Snapshot 固定；
```

### 72. C11 — C11 配置、版本、基线与变更控制规范 > 19. P2 强制检查

- `P2` · Locator `C11:88ec56f7:40ea1806:1028:270e8ada` · Lines `1355-1355`

```text
| C11-P2-058 | Rollback 已验证 | 覆盖数据和外部副作用 |
```

### 73. C11 — C11 配置、版本、基线与变更控制规范 > 20. 模板、清单与国际标准条款映射 > 20.15 Release 重建清单

- `P2` · Locator `C11:88ec56f7:1d301696:1090:e8e9ede2` · Lines `1781-1781`

```text
- [ ] Repository、Commit/Object、Tag 解析结果完整；
```

### 74. C11 — C11 配置、版本、基线与变更控制规范 > 6. 术语与定义 > 6.1 必须区分的五个概念

- `P2` · Locator `C11:88ec56f7:fcb57d98:142:e5460074` · Lines `188-188`

```text
| Asset ID | 这是什么资产 | 永久不变 | 分配规则需批准 | Version、路径、Commit |
```

### 75. C09 — C09 Agent 执行与证据规范 > 20. 附录 > 20.13 Retry 与 Rollback 判定表

- `P2` · Locator `C09:6897694e:e0e42fcb:848:70ea76c0` · Lines `1314-1314`

```text
| 幂等、无副作用、参数不变、授权有效 | 按 AEP 新 Attempt | 不需要 | 保留原失败 |
```

### 76. C09 — C09 Agent 执行与证据规范 > 16. 变更、审计与保留 > 16.2 审计历史

- `P2` · Locator `C09:6897694e:61e785bd:693:75cdd2cd` · Lines `914-914`

```text
- CAS/CCS 的 Old/New、Diff、Commit、Impact 和 Validation；
```

### 77. C11 — C11 配置、版本、基线与变更控制规范 > 10. 配置、版本、基线与变更控制规则 > 10.18 恢复与回滚

- `P2` · Locator `C11:88ec56f7:a8bfc8c2:521:6ef0c5b9` · Lines `693-693`

```text
4. Rollback 必须记录目标版本、实际动作、数据影响、外部副作用和验证；
```

### 78. C07 — C07 人机协作与责任规范 > 10. 强制规则 > 10.12 Stop Conditions 与 Fail-Closed

- `P2` · Locator `C07:a1fc4e90:1b37117b:373:ede0aec3` · Lines `505-505`

```text
| 结果异常 | 工具输出、变更数量、影响范围或副作用超出预期 | 停止后续步骤，保存证据 |
```

### 79. C09 — C09 Agent 执行与证据规范 > 13. 必填信息 > 13.9 Human Review Record

- `P2` · Locator `C09:6897694e:6c125a57:589:b94d53d8` · Lines `781-781`

```text
- CAS/CCS/VDR/FER/RRS/Diff/Commit；
```

> 此文件是 DerivedView。检索定位符不是规范正文的正式 Clause ID，召回命中不构成授权、批准或 Gate Outcome。
