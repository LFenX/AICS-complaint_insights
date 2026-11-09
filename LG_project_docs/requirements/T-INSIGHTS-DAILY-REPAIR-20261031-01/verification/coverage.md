# 本轮原文逐项核验

实际人类问题与回答见requirements/source.md；完整日报原话继续由父任务保存。

## R-001 每封FETCH前比较冻结UIDVALIDITY与当前选中文件夹实际值，复用连接不能跳过；不匹配明确失败且不下载或认证该封附件

工程已实现并验证。

- 输入：同INBOX连续77/77，两封MIME、part与摘要正确。预期：两封ready，同一连接仅一次EXAMINE，FETCH前身份一致。实际：ready2/failed0/EXAMINE1；8组参数正反还核验每次FETCH的真实命名空间。
- 输入：同INBOX首封77次封66，服务实际77。预期：次封拒绝、不FETCH、不认证且无bin文件。实际：ready1/failed1/UIDVALIDITY_MISMATCH；原独立反例从旧ready2变为拒绝第二封。

证据：`insights/attachment_fetcher.py`、`.runtime/daily-automation-20261030/imap-identity-repair/imap-controls/summary.json`、`.runtime/daily-automation-20261030/imap-identity-repair/tests-A02.log`。

## R-002 同epoch复用、切换folder、瞬断重连及失败后继续的正反用例通过，现有只读EXAMINE/BODY.PEEK、来源摘要和恢复行为不回退

工程已实现并验证。

- 输入：切换Archive、瞬断重连，正确与错误epoch。预期：重新EXAMINE取得实际值，正确继续、错误拒绝；每次EXAMINE只读。实际：8组单元正反及7组原独立控制通过；新连接实际88对冻结77拒绝；失败后下一封正确可继续。
- 输入：正常复用同INBOX同epoch，已核验缓存再次恢复。预期：保留复用效率和原只读读取/缓存恢复契约。实际：76项测试通过；同epoch仅一次EXAMINE，既有resume不重新连接测试通过。

证据：`tests/test_daily_report.py`、`.runtime/daily-automation-20261030/imap-identity-repair/tests-A02.log`、`.runtime/daily-automation-20261030/imap-identity-repair/imap-controls/summary.json`。

## R-003 安装skill同步逐封epoch边界，全部相关回归、隔离与当前读取模型校验通过，默认昨天与00:30本会话安排保持；保存版本交回父审查

工程已实现并验证。

- 输入：安装skill1.0.4，真实双地址HTTP及日期UI、默认昨天、76项回归。预期：固化每封epoch身份；保持默认昨天、历史634/405/35、白底与00:30同会话；保存可复核资料。实际：安装10文件合法、完整634索引和最长正文30714读取；双地址默认10/30未生成且历史29可读，详情/图/日志/PDF/ZIP和日期版本边界通过，UI日期选择及昨天返回通过；代码清单和交接已保存，最终Implemented与父新版本审查仍待安全隐私门。

证据：`C:/Users/Administrator/.codex/skills/complaint-daily-report/references/final-standard.md`、`.runtime/daily-automation-20261030/imap-identity-repair/verification.json`、`.runtime/daily-automation-20261030/imap-identity-repair/ui-verification.json`、`.runtime/daily-automation-20261030/imap-identity-repair/runtime-verification.json`。

正式工程收口仍受security-privacy-review门约束，未冒填通过。第四轮Incomplete及旧R03发现仍交后续完整独立轮判定。
