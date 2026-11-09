# MCP与门户恢复结果

两个HTTPS服务已恢复，Windows当前账户S4U/Limited计划任务独立托管。原密钥可用；门户页面、11工具发现、14表目录和邮件样本读取通过，无密钥401。历史数据版本25，DEGRADED。

独立父链：powershell→svchost→services→wininit。MCP与门户分别故障后3.42/4.63秒恢复；新托管器自有MCP worker退出后11.81秒恢复，退出码-1留存。任务配置开机20秒触发、每分钟防遗漏、无限执行时长和失败重启。

旧部署为普通后台进程，无独立守护。机器未重启；原日志无明确致命退出/正常关停或终止审计，直接停止触发Unknown，不能归咎ChatGPT或连接重置。确定的管理缺口是退出后不自动恢复。

首次PowerShell null状态替换失败已复现并修正为NullString；失败日志和所有更正保留。原密钥、管理员、生产配置哈希和其它服务PID不变，采集仍停止。

原话逐条覆盖见coverage.json，完整结果/限制见results.json，旧日志见before/，任务XML及独立父链、故障恢复证据均随目录保存。维护命令见../release/runtime-operations.md。

原话交代为2项Covered、1项Deferred：调查已执行但原停止直接原因未查明。未执行整机重启/注销和完整禁用注销回滚；人的验收Pending，不把工程验证当作人的批准。
