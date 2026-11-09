# 第7轮审查返修勘察

持续授权是当前用户“拉取最新代码并重启审查”和此前“开始审查”（含发现问题修复复验直到同版连续两轮无问题）。完整原话/真实问答仍在T-INSIGHTS-MCP-REPAIR-20261030-04/before.json及原任务，不补造新回答。本轮返修沿用你已确认的范围和授权，跳过重复提问。

第7轮权威报告：C:/Users/Administrator/Documents/Codex/2026-10-30/complaint-insights-mcp/work/round7/report.md；最终SHA256 860c10727b48cdd025e20b61b45b9273a1ee9fe44b112fd4d197b2ea6c3a241a。110文件最终不变，cbf64e8冻结已结束。3项确认：R7-001合法64字符提示在360px裁切；R7-002仅有并发上限，工具无时间窗限频；R7-003维护交接仍把task03旧证据称为当前。R6的一轮无发现已因本轮发现归零。

固定官方规范 https://modelcontextprotocol.io/specification/2025-11-25/server/tools#security-considerations 要求服务器对工具调用限频。约束核心为单位时间调用数，与并发数不同。设计在ContractMCPServer共同工具执行入口使用每身份滑动窗口，覆盖HTTP与stdio，校验工具/参数后计合法调用，耗尽在后端前以ToolError拒绝，返回固定错误码与可操作等待秒数；不改业务查询。默认6000次/60秒为工程默认，保留普通批量分页；HTTP私有配置tool_calls_per_minute允许1..60000且严格整数，默认共享常量；无禁用值。不同身份独立，共享该身份所有工具；同名重新发放仍同身份，不能通过重发绕过窗口。使用单调时钟、线程锁，清理过期桶，避免跨线程/并发竞态。测试用低配额+可控时钟，无需压测真实服务。

对比：保留现状不满足明确规范；在HTTP入口按IP限频遗漏stdio并会牵连同NAT接收人；在共同工具层按真实调用身份限频覆盖协议且不扩大授权。拒绝所有工具或改变分页语义不符合原目标。工具限频错误属于MCP工具执行错误isError=true；调用方等待提示时间重试，仍须遵守版本冲突从头重查及不得输出半结果。

最小CSS在alert继承overflow-wrap:anywhere，保留结构和视觉。维护交接指向本次已保存的报告/结果，冻结清单以正式after.source_snapshot.file_manifest为准，旧task03/task04明确历史。

仅操作MCP源码、测试、静态资源、公开材料与本任务文档。不得连接数据库/生产源10.8.45.155:5432，不启动watch，不修改重启3030/3036/15433/日报/附件/AICS及source.py/syncer.py。真实只读经现有API历史副本；不重置真实管理员。旧正式人类Gate/用户验收Pending，父Deferred使官方Offer登记拒绝的限制保留，不伪造ManagedByParent或机器Passed。另一电脑CA/路由未实测。

记录时间2026-10-29T22:59:17.823460+00:00，并非新的用户回答时间；沿用原决策证据。无新增权限、范围或验收未知。
