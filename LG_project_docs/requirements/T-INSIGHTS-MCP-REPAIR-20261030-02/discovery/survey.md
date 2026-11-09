# 第二次MCP审查返修

完整原文、澄清与“开始审查”答复继承只读父任务 T-INSIGHTS-MCP-PORTAL-20261030-01/before.json 和前次返修 T-INSIGHTS-MCP-REPAIR-20261030-01/before.json；不改写它们。用户同意原问题中的“发现问题将修复并复验，直至同一版本连续两轮完整审查无问题”，持续授权本次同范围返修，不是新门禁批准。

第二轮独立观察原件在 C:/Users/Administrator/Documents/Codex/2026-10-30/complaint-insights-mcp/work/round2：fixture-results.json（原始字符串null被清空）、client-results.json（先写凭据后ACL及失败残留，合成Users可读父目录）、protocol-edges.json（非法信封错误码）。第一返修45文件版本继续保持直到独立报告末次校验完成。本记录捕获于 2026-10-29T20:05:05.628409+00:00。

已核实依赖：MCP2.3公开构造参数tools、Tool.from_function和FuncMetadata允许构造工具元数据；禁用二次JSON字符串预解析仍保留Pydantic日期与SDK执行/输出处理。SDK transport在信封模型验证失败时HTTP400/-32602；只规范化该错误输出为-32600与简短信息，保留正常请求/通知/业务错误。Windows configure在空新文件设置受限ACL后才允许写入；失败仅清理本次O_EXCL创建的文件。

授权和环境边界均不变：唯一owner、接收人Bearer、10.8内网HTTPS、本地15433历史副本、生产读取false/watch停止；不操作3030/3036/数据库、AICS、日报、附件及source.py/syncer.py。另一电脑路由/CA与正式人类门禁仍未确认。父Deferred导致官方Offer登记拒绝；不得伪造Implemented、ManagedByParent或机器Passed。

本轮仍沿用已告知的跳过重复提问决定，范围内技术修复没有新增权限或验收未知。
