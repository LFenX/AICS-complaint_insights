# Task Review: T-INSIGHTS-DAILY-REPAIR-20261031-01

- Objective: 修复只读附件下载的连接复用UIDVALIDITY遗漏并以正反证据保存
- Contract revision: 9
- Contract state: Frozen
- Depends on: T-INSIGHTS-DAILY-AUTO-20261030-01, T-INSIGHTS-DAILY-REPAIR-20261030-03

## Acceptance criteria

- 每封FETCH前比较冻结UIDVALIDITY与当前选中文件夹实际值，复用连接不能跳过；不匹配明确失败且不下载或认证该封附件
- 同epoch复用、切换folder、瞬断重连及失败后继续的正反用例通过，现有只读EXAMINE/BODY.PEEK、来源摘要和恢复行为不回退
- 安装skill同步逐封epoch边界，全部相关回归、隔离与当前读取模型校验通过，默认昨天与00:30本会话安排保持；保存版本交回父审查

## Outcome

- Status: Implemented
- User decision: 待用户验收
- Adversarial review: {'status': 'ManagedByParent', 'parent_task_id': 'T-INSIGHTS-DAILY-AUTO-20261030-01', 'clean_streak': 0, 'rounds': 0, 'open_findings': []}
- Revision: 1

## Established facts

- 每封FETCH前核对连接选中folder实际UIDVALIDITY，复用不跳过，切换及重连重新取得；错误epoch不下载或认证
- 76项测试、独立7组内存MIME控制、安装skill10文件/完整读取及双地址HTTP与跨日真实UI通过；原634/405/35和历史归档未改
- 仅按原授权恢复3030原地址与网段，生产读取false，其他服务未启动或重启；本地15433实际连接超时，00:30实际触发结果未验证

## Actual changes

- 局部修复attachment_fetcher连接身份生命周期，新增8组实质正反用例，安装skill1.0.4同步逐封边界
- 当前需求原文、逐项覆盖、失败重试、运行恢复、差异与交接日志已保存；安全门实际决定单独留档

## Verification

- Passed: 76项相关回归及8组复用/切换/重连/失败继续身份正反通过
- Passed: 原独立内存MIME反例变为拒绝次封，7组控制保留实际FETCH及manifest证据
- Passed: 安装skill、634索引/最长原文、原报告及双地址详情/预览/ZIP/日期版本边界通过
- Passed: 跨日默认10/30缺报、手选29有634、昨天返回30、白底真实浏览器验证
- Passed: 原文逐项覆盖、条件正反与真实限制明确

## Evidence

- .runtime/daily-automation-20261030/imap-identity-repair/delivery-manifest.json
- .runtime/daily-automation-20261030/imap-identity-repair/source-changes.patch
- .runtime/daily-automation-20261030/imap-identity-repair/security-gate-decision.json
- LG_project_docs/requirements/T-INSIGHTS-DAILY-REPAIR-20261031-01/release/handoff.md

## Incomplete items


## Legacy issues

- 新真实日报仍受本地副本可用性与日终水位限制; reason=本轮实际只读连接127.0.0.1:15433超时，生产采集保持原隔离；不能用旧DEGRADED替代现在状态; impact=10/30未生成，默认查询该日显示未生成，00:30启用不保证数据到齐或成功发布; owner=本地副本与采集维护者（本任务未指定具体个人）; reentry=本地reader可达、状态READY且源/辅助水位覆盖日终后，沿既有授权与skill生成；生产恢复仍需另行明确授权

## Decisions

- 沿用父Accepted修复与复验授权，当前门决定以实际独立记录为准，最终用户验收Pending；新完整审查从本已保存版本计数

## Next tasks


## Terminal artifact manifest

- T-INSIGHTS-DAILY-REPAIR-20261031-01-before / TaskContract / Create/Revise / Revised
- T-INSIGHTS-DAILY-REPAIR-20261031-01-run / RunLedger / Create/Revise / Revised
- T-INSIGHTS-DAILY-REPAIR-20261031-01-after / TaskOutcome / Create/Revise / Created

## Amendments

- r1→r2 task_profile.change_surfaces: 按真实身份与数据影响补足Profile和安全隐私门声明，门尚未通过，不改授权或结果 (basis: .runtime/daily-automation-20261030/imap-identity-repair/survey.md)
- r2→r3 authority.required_gates: 按真实身份与数据影响补足Profile和安全隐私门声明，门尚未通过，不改授权或结果 (basis: .runtime/daily-automation-20261030/imap-identity-repair/survey.md)
- r3→r4 scope.allowed_paths: 实际HTTP失败因3030无监听，沿用既有开启内网看板授权仅恢复同配置服务，保留生产及其他服务边界 (basis: .runtime/daily-automation-20261030/imap-identity-repair/survey.md)
- r4→r5 plan.steps: 实际HTTP失败因3030无监听，沿用既有开启内网看板授权仅恢复同配置服务，保留生产及其他服务边界 (basis: .runtime/daily-automation-20261030/imap-identity-repair/survey.md)
- r5→r6 first_principles_analysis: 实际HTTP失败因3030无监听，沿用既有开启内网看板授权仅恢复同配置服务，保留生产及其他服务边界 (basis: .runtime/daily-automation-20261030/imap-identity-repair/survey.md)
- r6→r7 task_profile.applicability_facts.operations_impact: 实际HTTP失败因3030无监听，沿用既有开启内网看板授权仅恢复同配置服务，保留生产及其他服务边界 (basis: .runtime/daily-automation-20261030/imap-identity-repair/survey.md)
- r7→r8 task_profile.change_surfaces: 对齐新增的原配置3030服务恢复运维变更面，不增加外部服务范围 (basis: .runtime/daily-automation-20261030/imap-identity-repair/survey.md)
- r8→r9 requirement_items: 按真实反例与原文逐条核验工程结果，安全隐私门独立保持未通过，不将已保存证据冒充最终审查通过 (basis: .runtime/daily-automation-20261030/imap-identity-repair/source.md)

## Proof validation

当前契约记录校验通过（不替代人的验收）
