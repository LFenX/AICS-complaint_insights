# MCP审查返修勘察与授权

用户实际请求及询问答复：

把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。

开始审查

原需求与唯一所有者澄清完整原文沿用只读父记录 .project-governance/tasks/T-INSIGHTS-MCP-PORTAL-20261030-01/before.json。

四项已确认问题：匿名512次GET占满登录挑战；registry损坏使网页紧急撤销不可达；SDK宽松转换输入类型；未知工具被归为执行错误。独立原件：C:/Users/Administrator/Documents/Codex/2026-10-30/complaint-insights-mcp/work/round1/report.md 与 results.json。没有生产/真实凭据故障注入。

用户答复“开始审查”明确覆盖询问中的同范围返修和复验，不代表正式门禁批准。收件归档时间 2026-10-29T19:40:20.310121+00:00，不冒称原始答复时间。

工具限制：父after为Deferred，adversarial_review.py拒绝Offer（only after an Implemented engineering result is saved）。保留该失败；不改写父状态/门禁/已结束账本。此后续普通返修任务直接依赖父任务；在机器不认可父会话时不能声明ManagedByParent或机器审查Passed。用户要求的真实审查仍继续，单独保留非治理报告并明确限制。

实现约定：不改结构命名；现有Starlette/MCP2.3/Pydantic；jsonschema4.26.0是当前MCP已安装依赖，可在公开Schema边界校验，避免SDK预解析字符串后再校验导致漏拦。只部署desk/mcp。3030、3036、15433、生产/采集、日报、AICS与所有原任务保持原范围。

明确未验项：另一内网电脑路由和CA导入不在本机可验证能力内，保留原交付限制；正式人类门禁仍Pending。没有新增阻断未知，沿用用户授权，跳过重复提问。
