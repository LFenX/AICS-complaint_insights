# Task Review: T-INSIGHTS-MCP-REPAIR-20261030-05

- Objective: 修复工具限频、窄屏提示和当前交接并完成原需求复验
- Contract revision: 4
- Contract state: Frozen
- Depends on: T-INSIGHTS-MCP-PORTAL-20261030-01, T-INSIGHTS-MCP-REPAIR-20261030-04

## Acceptance criteria

- 360px合法64字符身份的签发、撤销及错误提示完整可读且不撑宽页面
- 全部工具在SDK/HTTP及stdio共同执行层按调用身份限频；窗口恢复、身份隔离、并发及未查询后端可验证
- 默认每身份6000次/60秒，HTTP服务可配置为1至60000；限频返回可读TOOL_RATE_LIMITED及retry_after_seconds，不改变工具参数、权限、分页口径
- 公开指南和维护交接解释限频并指向本次真实报告/结果；旧证据明确为历史
- 原测试及新反例、真实11工具14表/客户端/严格CA通过，生产隔离与保护PID保持，保存实际版本和未验项

## Outcome

- Status: Deferred
- User decision: 待用户验收
- Adversarial review: {'status': 'NotApplicable', 'clean_streak': 0, 'rounds': 0, 'open_findings': [], 'current_delivery': {'task_id': 'T-INSIGHTS-MCP-REPAIR-20261030-05', 'subject_sha256': '9ac2ce33f8235fe2bc1894b2cb4f7950f2b12f89051a5748668771ff6138a609'}}
- Revision: 1

## Established facts

- 3个第7轮反例已局部修复复验，工程结果和真实证据保存，人工Gate与用户验收Pending
- 3030/3036/15433及3029监听PID未变；watch停止、生产读取false、没有数据库连接或管理员重置

## Actual changes

- 共同工具层每身份滑动窗口限频，HTTP严格可配置、stdio默认；耗尽返回可操作错误且不访问后端
- 修复长身份alert换行，公开指南补限频并更新维护交接当前证据；同步7个源码/静态/文档/测试文件，仅重启mcp
- 原动作名称查询误用、CRLF预检失败与生成路径漏列均保留失败事实及官方路径修订，不隐瞒副作用

## Verification

- Passed: Git源码和原运行项目均49项回归通过
- Passed: 17组严格CA真实HTTPS覆盖11工具14表及管理员完整链路
- Passed: 360px长身份签发/撤销和错误无溢出，实际服务配额及CSS核对

## Evidence

- LG_project_docs/requirements/T-INSIGHTS-MCP-REPAIR-20261030-05/verification/coverage.json
- LG_project_docs/requirements/T-INSIGHTS-MCP-REPAIR-20261030-05/verification/delivery-files.json

## Incomplete items

- 正式人类门禁Pending; reason=正式独立复核/安全隐私人类Gate与用户验收Pending，不能由Agent批准; impact=工程验证不等于正式Gate批准; owner=当前任务用户; reentry=有权人对当前对象给出真实决定
- 异机路径未实测; reason=另一内网电脑的路由及CA未实测，已完成本机真实内网地址严格CA复验; impact=不能声明另一电脑的环境已经验证; owner=当前任务用户; reentry=接收人按公开指南在另一电脑复验
- 已授权后续审查待开展; reason=用户已明确重启；新版本连续两轮完整独立审查须在本工程保存后开展。父Deferred导致官方Offer登记拒绝限制保留; impact=尚不能宣称两轮收敛或官方Passed; owner=根执行Agent; reentry=同一保存版本完成两轮独立完整无问题审查；官方登记仍遵守原机器限制

## Legacy issues


## Decisions


## Next tasks


## Terminal artifact manifest

- T-INSIGHTS-MCP-REPAIR-20261030-05-before / TaskContract / Create/Revise / Created
- T-INSIGHTS-MCP-REPAIR-20261030-05-run / RunLedger / Create/Revise / Created
- T-INSIGHTS-MCP-REPAIR-20261030-05-after / TaskOutcome / Create/Revise / Created
- T-INSIGHTS-MCP-REPAIR-20261030-05-ver / AuthorityAsset / Create/Revise / Created
- T-INSIGHTS-MCP-REPAIR-20261030-05-rcr / DerivedView / Generate / Generated

## Amendments

- r1→r2 scope.allowed_paths: 补齐已授权公开材料构建器实际生成的guide/schema/query精确路径；保留首次执行已写生成指南的事实，无权限或目标扩展 (basis: C:/Users/Administrator/Documents/Codex/2026-10-30/complaint-insights-mcp/work/repair5/failure-notes.json)
- r2→r3 scope.allowed_paths: 同步已授权MCP测试到原运行项目，使维护交接的当前测试命令实际执行本版49项；不改测试实现或服务行为 (basis: C:\Users\Administrator\Documents\Codex\2026-10-30\complaint-insights-mcp\work\repair5\tests-A01.log)
- r3→r4 requirement_items: 保存当前工程事实；连续两轮须在结果保存后继续，人工门禁Pending (basis: LG_project_docs/requirements/T-INSIGHTS-MCP-REPAIR-20261030-05/verification/coverage.json)

## Proof validation

当前契约记录校验通过（不替代人的验收）
