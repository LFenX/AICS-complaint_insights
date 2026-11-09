# 第8轮stdio返修勘察

持续授权是当前用户“拉取最新代码并重启审查”及此前“开始审查”，包含发现问题修复复验直到同版连续两轮无问题。完整真实原话和决定沿用T-INSIGHTS-MCP-REPAIR-20261030-05/before.json；不补造新回答。本轮返修沿用你已确认的范围和授权，跳过重复提问。

独立报告：C:/Users/Administrator/Documents/Codex/2026-10-30/complaint-insights-mcp/work/round8/report.md，SHA256 2cc0dd10d179a388f02fbadf821395f8b9024d5e14794acf8f8f28737daf498e。固定源码88ef76c，125文件7fb70b2a88eff771a9da327c80ec5c6ca9aad039bfefdcbe616071ae381acb47。R8-001：stdio把1.00000000000000001等数学非整数舍入进入integer工具参数；R8-002：702.0与703e0等数学整数请求ID在stdio无响应。真实scripts/mcp_server.py入口通过runpy仅替换ReadAPI.load为合成API复现，HTTP对照分别正确拒绝/接受。没有真实数据库/生产连接。

固定依赖mcp2.3.0的stdio_server先validate_json后处理参数，精度已丢失；HTTP的wire_arguments保护没有覆盖stdio。已读当前SDK源码：context-aware streams在send时复制ContextVar；公开stdio_server支持显式stdin/stdout，但没有parser钩子。设计在ContractMCPServer.run_stdio_async接入原始行精确预检，复用固定SDK已核对的标准句柄保护和stdio transport。原始JSON用Decimal保留数值，只规范数学整数请求ID；已知工具仍在共同schema层以原始参数验证，quota与权限不变。共享JSON解码与ID检查供HTTP/stdin使用，避免再出现两种数值规则。输入错误返回固定JSONRPC错误不回显原值，继续读取后续行。stdout每完整消息以锁串行写入，SDK输出与预检错误同一写端；不让日志/杂散输出进入协议。

备选：保持现状会误收参数/合法请求超时；只拒绝全部float会误拒合法1.0/2e0；更改或全局monkey-patch SDK会影响其他进程且不满足固定依赖隔离。选精确传输适配，保留SDK会话/工具执行与标准句柄保护，代价是增加局部适配和真实子进程错误恢复/并发/Unicode回归。所有SDK内部接口均以当前已固定2.3.0源码实际核对，不假设不存在的公开parser参数。

仅局部MCP代码、测试、指南/当前维护证据与本任务文档。不改结构命名、工具签名、来源/AI统计/权限/限频策略，不连接数据库或192.168.10.155:5432，不运行watch/bootstrap/sync，不操作3030/3036/15433/日报/附件/AICS/source.py/syncer.py；只在必要时更新原mcp3037工程实例，desk不重启。不重置真实owner。正式人类Gate与用户验收Pending、官方父Deferred登记限制及另一电脑/历史口令回读限制如实保留。

记录时间2026-10-29T23:39:43.093969+00:00，并非用户新回答时间。stdio可逆局部修复在持续授权范围内，无新增权限、安全边界或外部目标未知。
