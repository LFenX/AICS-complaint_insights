# 实际勘察

第四轮已保存正反反例：同INBOX复用连接，实际epoch77，首封冻结77、次封冻结66仍ready且认证身份。源码attachment_fetcher.work把比较限定在切换folder分支。正确同epoch复用、folder切换和重连已存在正反控制。第四轮运行中断，已正式按Incomplete留档，不补造独立完整结论。

修复所有权在attachment_fetcher，保留选中folder的实际UIDVALIDITY并对每封比较；重连清空该状态，切换folder重新取得。API、页面、读取模型、历史报告及源数据无需修改。以模拟IMAP实际MIME与调用序列验证，禁止真实网络。

依据：.project-governance/tasks/T-INSIGHTS-DAILY-AUTO-20261030-01/evidence/round-04.md，review-04/imap-uidvalidity-counterexample.json与imap-controls/summary.json。

跨日实际复验：3030回环连接拒绝，Get-NetTCPConnection没有3030/15433监听；原processes.json的PID是旧记录，主机当前仍有10.8.61.200。服务中断原因未确定。只恢复既有3030看板，不启动watch/MCP/API/数据库等其他服务；不把数据库无法连接说成已验证DEGRADED。
