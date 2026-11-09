# Task Review: T-INSIGHTS-MCP-REPAIR-20261030-06

- Objective: 修复stdio精度与请求ID并完成原需求复验
- Contract revision: 2
- Contract state: Frozen
- Depends on: T-INSIGHTS-MCP-PORTAL-20261030-01, T-INSIGHTS-MCP-REPAIR-20261030-05

## Acceptance criteria

- 真实stdio启动脚本在SDK解码前保留工具JSON数值，数学非整数不得绕过integer schema且后端零调用；合法整数表示仍按值接受
- stdio数学整数请求ID的小数/指数表示正常响应并保留整数值；非法ID/畸形JSON错误分层正确，不泄露输入且后续合法请求可恢复
- 原生stdio与HTTP协议、并发上下文隔离、中文和JSON形字符串保持；SDK标准输入输出保护保持，不改依赖/结构/工具签名
- 原有49回归及新增真实stdio子进程回归通过，真实HTTPS和生产保护边界无回退；维护交接指向本次实际证据
- 保存工程版本和真实限制后继续已有完整独立审查，直到同一版本连续两轮无问题

## Outcome

- Status: Deferred
- User decision: 待用户验收
- Adversarial review: {'status': 'NotApplicable', 'clean_streak': 0, 'rounds': 0, 'open_findings': [], 'current_delivery': {'task_id': 'T-INSIGHTS-MCP-REPAIR-20261030-06', 'subject_sha256': '82efbb467fb63b37bd2856f0139fd2e48c348b0df28490eceef9ce5ec887dc1e'}}
- Revision: 4

## Established facts

- 真实stdio数值精度与合法整数表示ID两个P2反例已修复，工程结果和原始反例证据保存
- 3029/3030/3036/15433监听PID未变、watch停止、生产读取false；没有数据库连接、管理员重置或历史口令重新交付
- 工程保存后，第9轮和第10轮在同一138文件交付394610f667cd75378be565733a84fc80d58ee438a57e709f7be33cc3d87789b4独立完整审查，均无新增/未决/未检查的当前必需产品项，21项历史问题在两轮分别复验；实际报告与哈希可核对
- 本次技术审查收敛不改变原Deferred、Pending与官方Offer登记限制，不写正式审查数组或已结束Run

## Actual changes

- 共享HTTP/stdio原始JSON和数学整数ID预检，stdio逐消息保留参数；固定错误响应后可恢复并保留SDK标准句柄保护
- 同步4个代码/测试/交接文件，仅重启mcp，更新当前工程证据指针与实际tools/list公开包；不改结构依赖工具签名
- 预检顺序和补账Attempt错误及纠正保留，没有产品测试失败或隐去记录

## Verification

- Passed: Git和运行项目各52项通过，包含真实stdio启动脚本原始协议子进程
- Passed: 严格CA真实HTTPS17组覆盖11工具14表、客户端完整分页及原管理员链路
- Passed: 4部署文件与Git逐字节相同，保护监听PID不变

## Evidence

- LG_project_docs/requirements/T-INSIGHTS-MCP-REPAIR-20261030-06/verification/coverage.json
- LG_project_docs/requirements/T-INSIGHTS-MCP-REPAIR-20261030-06/verification/delivery-files.json
- C:\Users\Administrator\Documents\Codex\2026-10-30\complaint-insights-mcp\work\round9\report.md
- C:\Users\Administrator\Documents\Codex\2026-10-30\complaint-insights-mcp\work\round9\results.json
- C:\Users\Administrator\Documents\Codex\2026-10-30\complaint-insights-mcp\work\round10\report.md
- C:\Users\Administrator\Documents\Codex\2026-10-30\complaint-insights-mcp\work\round10\results.json
- C:\Users\Administrator\Documents\Codex\2026-10-30\complaint-insights-mcp\work\repair6\actual-review-completion.json

## Incomplete items

- 正式人类门禁Pending; reason=正式独立复核/安全隐私人类Gate与用户验收Pending，不能由Agent批准; impact=工程验证不等于正式Gate批准; owner=当前任务用户; reentry=有权人对当前对象给出真实决定
- 异机路径未实测; reason=另一内网电脑的路由及CA未实测，已完成本机真实内网地址严格CA复验; impact=不能声明另一电脑的环境已经验证; owner=当前任务用户; reentry=接收人按公开指南在另一电脑复验
- 原生浏览器缓存POST历史重绘未实测; reason=IAB后退POST结果触发ERR_CACHE_MISS和URL策略拦截；没有绕过或将该场景标为已执行; impact=不声明缓存POST历史重绘已实测；关闭后新GET、退出后后退刷新及原生确认已验证; owner=当前任务用户及可用浏览器环境; reentry=在可用且已信任CA的实际浏览器环境补充该场景
- 历史口令交付消息未追溯核验; reason=当前无可回读的旧assistant交付消息原件；没有重新读取、重发或重置初始口令; impact=当前登录签发功能已验证；不把历史口令消息交付当作本轮已核证事实; owner=当前任务用户; reentry=提供可核对的原消息来源后追溯核对，无需改动当前账号

## Legacy issues


## Decisions


## Next tasks


## Terminal artifact manifest

- T-INSIGHTS-MCP-REPAIR-20261030-06-before / TaskContract / Create/Revise / Created
- T-INSIGHTS-MCP-REPAIR-20261030-06-run / RunLedger / Create/Revise / Created
- T-INSIGHTS-MCP-REPAIR-20261030-06-after / TaskOutcome / Create/Revise / Created
- T-INSIGHTS-MCP-REPAIR-20261030-06-ver / AuthorityAsset / Create/Revise / Created
- T-INSIGHTS-MCP-REPAIR-20261030-06-rcr / DerivedView / Generate / Generated

## Amendments

- r1→r2 requirement_items: 保存当前工程事实；连续两轮须在结果保存后继续，人工门禁Pending (basis: LG_project_docs/requirements/T-INSIGHTS-MCP-REPAIR-20261030-06/verification/coverage.json)
- r1→r2 established_facts: 补记保存交付后两轮实际完整独立技术审查及明确限制；不更改正式审批、审查数组、交付或已结束账本 (basis: C:\Users\Administrator\Documents\Codex\2026-10-30\complaint-insights-mcp\work\repair6\actual-review-completion.json)
- r2→r3 incomplete_items: 补记保存交付后两轮实际完整独立技术审查及明确限制；不更改正式审批、审查数组、交付或已结束账本 (basis: C:\Users\Administrator\Documents\Codex\2026-10-30\complaint-insights-mcp\work\repair6\actual-review-completion.json)
- r3→r4 evidence_refs: 补记保存交付后两轮实际完整独立技术审查及明确限制；不更改正式审批、审查数组、交付或已结束账本 (basis: C:\Users\Administrator\Documents\Codex\2026-10-30\complaint-insights-mcp\work\repair6\actual-review-completion.json)

## Proof validation

当前契约记录校验通过（不替代人的验收）
