# 日报IMAP身份修复与3030恢复

# 逐封IMAP身份修复交接

时间：2026-10-30T18:22:14.612567+00:00。任务T-INSIGHTS-DAILY-REPAIR-20261031-01，直接依赖已Accepted父T-INSIGHTS-DAILY-AUTO-20261030-01。

改动：attachment_fetcher仅保留当前选中folder的实际UIDVALIDITY，每封FETCH前比较冻结值；登录或异常重连清空选中状态。身份不符时明确失败，不能FETCH第二封或认证其原件。新单元用8组MIME验证同连接、切换folder、重连、首封失败与后续继续；原独立7组控制另在私有目录重跑。安装skill1.0.4同步该实际边界。接口、项目命名结构、网页、报告及405原件未改。

验证：76项测试通过；原跨epoch反例ready2已变为ready1/failed1且次封无FETCH。安装skill10文件合法、634索引及最长30714正文完整读取；旧报告7d64a仍634/405/35，原始b2658归档保持。双地址HTTP默认10/30未生成，历史29可选；详情、图片/日志/PDF、ZIP、日期400与版本409通过。真实CUA白底日期框默认10/30，手选29看到634，再点昨天回到10/30未生成，无旧日报回填。

运行恢复：实际3030曾无监听，原因未确定。沿用既有人类开启内网看板指令，仅按原配置恢复board，parent162956/listener257224。绑定127.0.0.1与10.8.61.200:3030，允许范围10.8.0.0/16不变，未动防火墙、watch、MCP、desk或既有serve。生产读取保持false。当前本地15433实际探测结果见local-replica-status.json（unavailable），不能继续沿用昨晚DEGRADED当现在状态。00:30配置仍ACTIVE，但首次实际触发结果未验证，不宣称已完成10/30日报。

失败保留：首次Profile遗漏数据变更面与必需门声明，被工具拦截后通过正式Amendment补齐；恢复服务时补运维影响，遗漏Deploy面再次被拦截后正式补齐。新重连夹具先写成已变化epoch应通过，与FETCH前拒绝契约冲突；纠正夹具，不放宽实现。HTTP验证第一次真实连接拒绝；恢复3030后验证器错误假设缺报响应有records，改用真实简响应契约。A01至A04及原日志均保留。

安全边界：没有真实IMAP或生产连接，没有数据库写入，没有凭据输出/新令牌/权限扩大/外部模型。恢复board不运行附件下载器。此修复有Identity/Security/Privacy影响，当前规范解析要求security-privacy-review，已声明但尚无本次已验证版本的真实人工通过记录；不得删门、冒签或拿旧版门禁当本次通过。工程资料先保存，待真实门决定后才能正式以Implemented交回父审查并重新计连续两轮。父已授权审查不用重复询问。

回滚：before保留代码/测试、安装skill及启动前进程记录；恢复这些代码文件不会改变旧报告。board恢复的是既有同配置服务，无数据迁移或新公开端口。不将旧PID文件恢复视为真正回滚进程；必要时只停止核对后的本项目board，其他服务不动。

涉及：insights/attachment_fetcher.py、tests/test_daily_report.py、安装skill的SKILL.md与references/final-standard.md、本任务LG文档与私有验证、.runtime/processes.json及board日志。
