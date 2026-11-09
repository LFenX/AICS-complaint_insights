# Task Review: T-INSIGHTS-MCP-OPS-20261101-01

- Objective: 恢复MCP和门户并配置独立运行，查明停止原因及证据限制
- Contract revision: 4
- Contract state: Frozen
- Depends on: None

## Acceptance criteria

- 3029门户和3037MCP通过现有CA与密钥正常访问
- 独立Windows计划任务运行，父进程不属于ChatGPT，异常退出后自动恢复
- 停止原因有可核对证据；无法确定的直接原因明确留档
- 旧日志保留，已有令牌不变；不操作数据库、采集和其它业务服务

## Outcome

- Status: Deferred
- User decision: 待用户验收
- Adversarial review: {'status': 'NotApplicable', 'clean_streak': 0, 'rounds': 0, 'open_findings': [], 'current_delivery': {'task_id': 'T-INSIGHTS-MCP-OPS-20261101-01', 'subject_sha256': '05f05bd5d3d11249797363d3425132c8228017f043cc58f7887404adb4246761'}}
- Revision: 1

## Established facts

- MCP3037与门户3029已恢复；现有HTTPS和原密钥使用通过
- 两个S4U当前账户任务父链到Windows服务管理器，脱离ChatGPT；受控终止后自动恢复
- 停止原因调查已执行；历史证据不足，直接触发Unknown，不计Covered

## Actual changes

- 新增scripts/mcp-service-host.ps1、两个命名计划任务、开机与每分钟触发、无限运行及10秒恢复；未改业务接口/依赖/权限
- 修复并验证WindowsPowerShell NullString兼容性，保全旧日志与失败证据，新增退出时间/退出码日志和维护说明

## Verification

- Passed: 门户首页/登录/指南200，严格CA原密钥MCP协商、11工具发现、14表目录和邮件样本成功，无密钥401；自动恢复后再次调用通过
- Blocked: 旧日志、系统启动记录、应用事件与Security审计已检查；无独立托管/恢复已确认，直接停止触发证据不足明确Unknown；直接停止原因的核证受历史退出/终止审计缺失阻断，未认定已查明
- Passed: S4U当前账户Limited任务Running，父链到Windows服务；两服务自动恢复，MCP自有worker退出码-1被记录并11.81秒恢复

## Evidence

- LG_project_docs/requirements/T-INSIGHTS-MCP-OPS-20261101-01/verification/results.json
- LG_project_docs/requirements/T-INSIGHTS-MCP-OPS-20261101-01/release/runtime-operations.md

## Incomplete items

- 原进程直接停止触发无法追溯; reason=旧日志没有退出时间、退出码或明确关停记录；Windows未记录相应进程终止审计; impact=不把连接重置或ChatGPT会话结束推断为已证实停止原因; owner=系统维护者; reentry=取得当时外部进程终止或操作记录后继续追溯
- 未执行整机重启或注销验证; reason=不影响其它业务服务和当前用户会话；已核对S4U、开机触发、无限执行配置并实测独立父链和服务恢复; impact=开机与无登录运行已配置，未声明整机重启/注销已实测; owner=系统维护者; reentry=明确维护窗口重启或注销后复验
- 完整配置回滚未演练; reason=保留已恢复服务；旧日志与任务XML保全，维护说明限定停用/回滚目标; impact=不声称完整禁用/注销回滚已实际执行; owner=系统维护者; reentry=维护窗口按说明演练并复验

## Legacy issues


## Decisions


## Next tasks


## Terminal artifact manifest

- T-INSIGHTS-MCP-OPS-20261101-01-before / TaskContract / Create/Revise / Created
- T-INSIGHTS-MCP-OPS-20261101-01-run / RunLedger / Create/Revise / Created
- T-INSIGHTS-MCP-OPS-20261101-01-after / TaskOutcome / Create/Revise / Created
- T-INSIGHTS-MCP-OPS-20261101-01-verification / AuthorityAsset / Create/Revise / Created

## Amendments

- r1→r2 task_profile: 纠正分类：仅Windows运行托管与恢复，不改变产品/API/UI/数据设计；Deploy/Operations和operations_impact保持 (basis: LG_project_docs/requirements/T-INSIGHTS-MCP-OPS-20261101-01/discovery/survey.md)
- r2→r3 requirement_items: 按原始三项指令交代实际验证和停止原因证据限制；工程结果不替代人的验收 (basis: LG_project_docs/requirements/T-INSIGHTS-MCP-OPS-20261101-01/verification/coverage.json)
- r3→r4 requirement_items: 更正覆盖口径：两个运行要求已完成；调查已执行但直接停止触发Unknown，R-02为Deferred，不把Unknown计为Covered (basis: LG_project_docs/requirements/T-INSIGHTS-MCP-OPS-20261101-01/verification/coverage.json)

## Proof validation

当前契约记录校验通过（不替代人的验收）
