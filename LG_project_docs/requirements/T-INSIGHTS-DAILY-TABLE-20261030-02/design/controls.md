# 控件与契约

|ID|控件或能力|输入/出口|数据与权限|验证|
|---|---|---|---|---|
|C-025|优先排序选择框|uid/log/image/document；有内容先；重置页码|读取模型records，daily_board|四项各自排序且集合不变|
|C-026|子问题工具行ZIP入口|选subtheme后启用；整组文件/邮件计数|预生成subthemes.log_archive，daily_log_archive / insights.attachments.logs.export|无选择/无日志/Feature关闭原因；整组含跨页日志|
|C-027|日志ZIP只读GET|固定摘要ID、当前报告版本|本机身份、Feature、允许ID、RESOURCE，action log-archive.read|403/404/409/503；审计不含日志正文|

现有C-010分页、C-022子问题筛选、原译与附件侧栏沿用；时间/主键仅从表格移除。ZIP按源快照、子问题及日志ID/摘要绑定，成员路径固定mail/attachment前缀+清洗文件名；不在请求中打包或接受文件路径。
