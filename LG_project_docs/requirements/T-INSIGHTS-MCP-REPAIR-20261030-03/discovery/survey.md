# 第三次MCP审查返修

持续授权来源：原任务T-INSIGHTS-MCP-PORTAL-20261030-01/before.json的完整原始请求与唯一所有者澄清、前次返修T-INSIGHTS-MCP-REPAIR-20261030-02/before.json中的实际询问及“开始审查”。原问题明确包括发现问题修复复验直到同版连续两轮完整无问题。本次同范围修复不增加管理员、生产、采集或正式门禁权限，不重复索取同一授权。

第三轮确认：管理员read_object与后续文件hash两次读取间轮换，会使旧认证数据绑定新版本；非法请求ID被SDK通知分支吞为202，合法1.0/1e3也被吞；五个分页工具cursor空字符串回到首页。独立证据在 C:/Users/Administrator/Documents/Codex/2026-10-30/complaint-insights-mcp/work/round3，根夹具在work/root-review/admin-snapshot-race.json。此记录时间2026-10-29T20:32:23.429677+00:00为捕获时间，原授权时间不重造。

根已核实固定MCP2025-11-25基础规范：请求ID必须字符串/整数且非null；通知不能包含ID；客户端错误响应id=null须保留允许。实现使用已解码的原始请求检查并重放给SDK；合法整数数值表示按等值整数处理，不改字符串值。空cursor仅需MCP的min_length=1，不改3036 API。管理员版本可对一次读取的严格JSON对象计算规范化摘要，消除第二次文件读取。

生产读取false/watch停止，源10.8.45.155:5432及所有数据库禁止连接。3030、3036、15433、日报、附件、AICS、source.py/syncer.py与历史任务不操作。异常时序与破坏性输入仅在合成夹具；真实验证只通过现有只读MCP/门户。

另一内网电脑路由/CA、正式人类门禁与验收Pending。父Deferred导致官方Offer登记拒绝，保留失败，不改写旧状态或冒称机器Passed/ManagedByParent。延续已向用户告知的跳过重复提问；没有新增权限未知。
