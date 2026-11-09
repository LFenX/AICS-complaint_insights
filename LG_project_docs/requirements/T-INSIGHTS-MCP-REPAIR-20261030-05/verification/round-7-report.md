# 第7轮独立只读对抗性审查

结论：完整覆盖约定范围，确认3项问题（P2×1、P3×2），本轮不干净，连续计数0。coverage=Complete。未修改产品、旧轮次或已保存工程结果。

时间：2026-10-29T22:42:51.195611+00:00 → 2026-10-29T22:57:33.696570+00:00。HEAD `cbf64e8566bc58849db6e10c27dfacbf05554c67`。110项冻结版本 `afeaa7c6ee6bddad8f7942c9f9cc040013190aec7af2bc60a46251d7ba521190`。起止全部hash匹配，git status为空。

本次任务使用skill：run-governed-product-workflow。亲自读完整SKILL.md与verify.md，并直接读取3个before的全部原文/真实澄清、portal survey，以及其引用DAILY before原权限完整上下文。旧报告仅用于问题追踪，未把上一轮“无问题”作为本轮前提。当前最新“拉取最新代码并重启审查”重新绑定冻结Git；暂停第四轮与旧版均不计数。

## 确认问题

### R7-001 · P3 · 合法64字符身份的签发/撤销成功提示在360px窄屏被裁切

位置：assets/token-desk.css:17；assets/token-desk.css:63；insights/token_desk.py:228；insights/token_desk.py:404；insights/token_desk.py:407

复现：浏览器360×800，唯一合成管理员登录，发放review7-加56个c的64字符身份，复制/关闭后再确认撤销。

预期：成功提示完整显示接收人身份；长串应在卡片内换行，不撑宽正文。

实际：签发后document client345/scroll417；撤销flash client345/scroll431；alert宽313且overflow-wrap:normal，长串越过卡片并被html overflow-x:clip裁切。

影响：不能完整核对生成/撤销反馈中的接收人身份；不影响令牌实际授权结果。

证据：browser-results.json；browser-long-revoke-flash-360.png；../AICS-database-MCP/assets/token-desk.css

### R7-002 · P2 · MCP工具调用无频率限制，未落实固定协议Servers MUST Rate limit tool invocations

位置：insights/mcp_http.py:279；insights/mcp_http.py:294；insights/mcp_server.py:79

复现：独立合成MCP应用、同一Bearer和实际peer，以并发度1连续发送96个list_mails(limit=1)；无需真实数据库。

预期：具有服务器工具调用频率限制及超额拒绝/恢复机制；并发度上限不能替代频率限制。

实际：96请求约0.246秒全部HTTP200，FakeAPI接收96次；完整应用和SDK不存在频率桶/时间窗/调用拒绝，只有uvicorn limit_concurrency=16。

影响：任何有效接收令牌可以持续以单连接高速驱动只读API，工具调用缺少协议要求的资源保护。

证据：synthetic-results.json；synthetic_review.py；https://modelcontextprotocol.io/specification/2025-11-25/server/tools#security-considerations

### R7-003 · P3 · 维护交接把第三次返修旧证据称为当前工程证据

位置：LG_project_docs/requirements/T-INSIGHTS-MCP-PORTAL-20261030-01/release/operator-handoff.md:55

复现：按维护交接“当前工程证据”链接进入task03报告和同目录results/delivery-files；对照已保存task04 after与冻结HEAD。

预期：当前交接指向已保存第四次返修版本及45测试/5项修复证据；旧第三次报告应标历史。

实际：operator-handoff第55行仍称第三次报告为当前，目标正文明确41测试与旧版本快照；当前task04已保存且有45测试。

影响：维护者按当前指引无法找到本版交付摘要和新修复证明；旧R3-04同类证据新旧混淆再次出现。

证据：../AICS-database-MCP/LG_project_docs/requirements/T-INSIGHTS-MCP-PORTAL-20261030-01/release/operator-handoff.md；../AICS-database-MCP/LG_project_docs/requirements/T-INSIGHTS-MCP-REPAIR-20261030-04/verification/results.json；original-sources.json

R7-002依据固定[官方2025-11-25 Tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#security-considerations)。本轮同时核对[Base](https://modelcontextprotocol.io/specification/2025-11-25/basic)、[Lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)、[Transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)及[Resources](https://modelcontextprotocol.io/specification/2025-11-25/server/resources)原文。客户端Accept双类型及初始化MUST，不能据此额外臆造服务器必须拒绝所有不合客户端行为的义务。

## 原文逐条对照

每项quote保留同来源完整原句；同一句复合要求独立拆条。完整source_sha256、条件及Met/NotMet输入预期实际在results.json.requirements。3个任务的重复“开始审查”与凭据原句分别保留，未用另一轮同字答复替换。

### Q01 · 提供可交给其他接收人的详细MCP介绍

来源：T-INSIGHTS-MCP-PORTAL-20261030-01:request_snapshot。状态：已实现。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

在线指南、全部11工具Schema及逐参数表、14表说明、原生协议与错误/分页/来源说明均与真实对象对照。

证据：live-results.json；body-provenance.json；client-results.json

### Q02 · 文档及程序符合MCP本身协议

来源：T-INSIGHTS-MCP-PORTAL-20261030-01:request_snapshot。状态：部分实现。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

初始化、通知、资源、请求ID和分层错误通过；工具调用缺少官方MUST要求的频率限制。

证据：synthetic-results.json；R7-002

### Q03 · 接收人能够配置并实际使用MCP

来源：T-INSIGHTS-MCP-PORTAL-20261030-01:request_snapshot。状态：已实现。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

下载标准库、SDK和11工具workflow接入成功，公开包无凭据。

证据：client-results.json；live-results.json

### Q04 · 优化并复核MCP令牌生成服务

来源：T-INSIGHTS-MCP-PORTAL-20261030-01:request_snapshot。状态：部分实现。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

认证、会话、CSRF、撤销故障安全及原子并发通过；窄屏成功反馈裁切及MCP工具限频缺口待修复。

证据：regression.log；synthetic-results.json；R7-001；R7-002

### Q05 · 内网开放令牌服务入口

来源：T-INSIGHTS-MCP-PORTAL-20261030-01:request_snapshot。状态：已实现。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

3029真实内网HTTPS可读，严格CA、Host/Origin边界成立。异机路由及CA另列外部限制。

证据：boundary-results.json；live-results.json

### Q06 · MCP协议、介绍和接入方法放于生成令牌的同一服务

来源：T-INSIGHTS-MCP-PORTAL-20261030-01:request_snapshot。状态：已实现。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

同一3029提供完整在线指南、7项下载、23项通用包；全部Schema逐对象相同。

证据：live-results.json

### Q07 · 一个内网链接可供接收人阅读、下载和找到管理员入口

来源：T-INSIGHTS-MCP-PORTAL-20261030-01:request_snapshot。状态：部分实现。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

首页导航/指南/下载/登录表单可用；64字符身份的管理成功反馈在360px被裁切。

证据：live-results.json；browser-results.json；R7-001

### Q08 · 本轮只处理MCP及历史副本，不干涉日报/采集/保护服务

来源：T-INSIGHTS-MCP-PORTAL-20261030-01:request_snapshot。状态：已实现。

> 开一个新会话处理MCP相关事宜，本会话继续完成客诉日报看板

只写round7证据；未连接任何数据库/源生产、未重启或修改服务；受保护冻结文件起止相同。

证据：hash-start.json；hash-end.json；boundary-results.json

### Q09 · 沿用已有MCP范围与所有者权限，不增加管理员

来源：T-INSIGHTS-MCP-PORTAL-20261030-01:request_snapshot。状态：已实现。

> 继续

仅唯一管理员机制；本轮认证/发放/撤销全在合成夹具，没有扩大权限。

证据：synthetic-results.json；regression.log

### Q10 · MCP可读取约定历史副本的全部类型数据并保留完整源payload；早期线上一致性要求按后续生产隔离范围理解

来源：T-INSIGHTS-DAILY-20261030-01:request_snapshot。状态：已实现。

> 搞定以后，测试数据是否完整，MCP访问是否能够正常取出所有数据，并且数据和线上一致没有遗漏

14表入口全部执行，11非空表完整行列表与get_source_record逐对象相同、3合法空表无伪造数据；五分页小集合完整、正文/译文/业务键来源可核对。未扩展为生产实时一致审计。

证据：live-results.json；body-provenance.json

### Q11 · 简单权限发放网页能够生成访问令牌

来源：T-INSIGHTS-DAILY-20261030-01:request_snapshot。状态：部分实现。

> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

原生登录发放可用；合法长身份成功反馈在窄屏裁切。

证据：browser-results.json；synthetic-results.json；R7-001

条件：有效唯一管理员会话和同源CSRF成立后才允许发放/撤销；匿名、仅MCP Bearer、伪造或失效会话不得管理。正反分支见results.json对应cases；涉及两轮收敛的正向前提当前不成立，明确NotRun而未伪造。

### Q12 · 内网MCP仍须本人下发的独立访问令牌

来源：T-INSIGHTS-DAILY-20261030-01:request_snapshot。状态：已实现。

> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

有效Bearer放行；匿名、错误、撤销及配置失效关闭。

证据：regression.log；live-results.json

条件：虽然在内网，读取MCP数据仍必须具有所有者下发且当前有效的独立Bearer。正反分支见results.json对应cases；涉及两轮收敛的正向前提当前不成立，明确NotRun而未伪造。

### Q13 · 部署3029；后续明确内网开放覆盖早期localhost绑定

来源：T-INSIGHTS-DAILY-20261030-01:request_snapshot。状态：已实现。

> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

3029只监听10.8.61.200，实际指定内网peer/HTTPS/Host/Origin验证成立，伪造代理头不放行。

证据：boundary-results.json

条件：后续内网开放授权成立时采用指定内网HTTPS；仍须拒绝HTTP/非授权实际peer/错误Host和Origin。正反分支见results.json对应cases；涉及两轮收敛的正向前提当前不成立，明确NotRun而未伪造。

### Q14 · 普通访客只读指南及无凭据客户端；仅唯一所有者独立登录后发放/撤销

来源：T-INSIGHTS-MCP-PORTAL-20261030-01:clarification:r1.e1。状态：部分实现。

> 继续

澄清上下文：令牌发放保留哪种管理员范围？普通内网访客均只能阅读文档、下载无凭据客户端；只有登录管理员才能生成或撤销 MCP 令牌。 推荐默认：仅我持有独立管理员凭据并发放

唯一所有者和角色分离成立；登录后的长身份反馈有窄屏缺陷。

证据：browser-results.json；regression.log；R7-001

条件：有效唯一管理员会话和同源CSRF成立后才允许发放/撤销；匿名、仅MCP Bearer、伪造或失效会话不得管理。正反分支见results.json对应cases；涉及两轮收敛的正向前提当前不成立，明确NotRun而未伪造。

### Q15a · 提供唯一管理员账号

来源：T-INSIGHTS-MCP-REPAIR-20261030-03:request_snapshot。状态：已实现。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

维护交接明确owner、唯一管理员存储；合成唯一管理员机制实测，不重读真实口令。

证据：original-sources.json；../AICS-database-MCP/LG_project_docs/requirements/T-INSIGHTS-MCP-PORTAL-20261030-01/release/operator-handoff.md

### Q15b · 管理员口令经受控渠道交付

来源：T-INSIGHTS-MCP-REPAIR-20261030-03:request_snapshot。状态：部分实现。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

既有维护记录记载已在用户私聊交付；本轮未获得原始私聊消息作实际收件证据，未读取/重发/重置真实口令。该历史收件事实留给用户验收确认。

证据：../AICS-database-MCP/LG_project_docs/requirements/T-INSIGHTS-MCP-PORTAL-20261030-01/release/operator-handoff.md

### Q15c · 提供直接管理员登录入口

来源：T-INSIGHTS-MCP-REPAIR-20261030-03:request_snapshot。状态：已实现。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

/admin/login真实页面可达，原生浏览器登录成功。

证据：boundary-results.json；browser-results.json

### Q15d · 登录该唯一管理员后即可生成可用token

来源：T-INSIGHTS-MCP-REPAIR-20261030-03:request_snapshot。状态：部分实现。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

原生登录/签发/复制/关闭与合成撤销认证链路成立；合法长身份反馈裁切。

证据：browser-results.json；synthetic-results.json；regression.log；R7-001

条件：有效唯一管理员会话和同源CSRF成立后才允许发放/撤销；匿名、仅MCP Bearer、伪造或失效会话不得管理。正反分支见results.json对应cases；涉及两轮收敛的正向前提当前不成立，明确NotRun而未伪造。

### Q16a · 提供唯一管理员账号

来源：T-INSIGHTS-MCP-REPAIR-20261030-04:request_snapshot。状态：已实现。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

维护交接明确owner、唯一管理员存储；合成唯一管理员机制实测，不重读真实口令。

证据：original-sources.json；../AICS-database-MCP/LG_project_docs/requirements/T-INSIGHTS-MCP-PORTAL-20261030-01/release/operator-handoff.md

### Q16b · 管理员口令经受控渠道交付

来源：T-INSIGHTS-MCP-REPAIR-20261030-04:request_snapshot。状态：部分实现。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

既有维护记录记载已在用户私聊交付；本轮未获得原始私聊消息作实际收件证据，未读取/重发/重置真实口令。该历史收件事实留给用户验收确认。

证据：../AICS-database-MCP/LG_project_docs/requirements/T-INSIGHTS-MCP-PORTAL-20261030-01/release/operator-handoff.md

### Q16c · 提供直接管理员登录入口

来源：T-INSIGHTS-MCP-REPAIR-20261030-04:request_snapshot。状态：已实现。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

/admin/login真实页面可达，原生浏览器登录成功。

证据：boundary-results.json；browser-results.json

### Q16d · 登录该唯一管理员后即可生成可用token

来源：T-INSIGHTS-MCP-REPAIR-20261030-04:request_snapshot。状态：部分实现。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

原生登录/签发/复制/关闭与合成撤销认证链路成立；合法长身份反馈裁切。

证据：browser-results.json；synthetic-results.json；regression.log；R7-001

条件：有效唯一管理员会话和同源CSRF成立后才允许发放/撤销；匿名、仅MCP Bearer、伪造或失效会话不得管理。正反分支见results.json对应cases；涉及两轮收敛的正向前提当前不成立，明确NotRun而未伪造。

### Q17a · 完成已授权多轮对抗审查、问题返修和复验，直到同版连续两轮无问题

来源：T-INSIGHTS-MCP-REPAIR-20261030-03:request_snapshot。状态：部分实现。

> 工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。

本轮有三项确认问题，等待同范围返修并保存新版后继续；不能宣称两轮收敛。

证据：results.json；report.md

条件：只有同一交付版本连续两轮完整审查零确认问题且无未决覆盖缺口，才可标记对抗审查通过；发现问题或版本变化须归零。正反分支见results.json对应cases；涉及两轮收敛的正向前提当前不成立，明确NotRun而未伪造。

### Q17b · 实际进行独立完整审查

来源：T-INSIGHTS-MCP-REPAIR-20261030-03:request_snapshot。状态：已实现。

> 开始审查

新只读执行者独立读取原文、构造新失效视角并完成全部领域；没有把上一轮无问题作为前提。

证据：results.json；original-sources.json

### Q18a · 完成已授权多轮对抗审查、问题返修和复验，直到同版连续两轮无问题

来源：T-INSIGHTS-MCP-REPAIR-20261030-04:request_snapshot。状态：部分实现。

> 工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。

本轮有三项确认问题，等待同范围返修并保存新版后继续；不能宣称两轮收敛。

证据：results.json；report.md

条件：只有同一交付版本连续两轮完整审查零确认问题且无未决覆盖缺口，才可标记对抗审查通过；发现问题或版本变化须归零。正反分支见results.json对应cases；涉及两轮收敛的正向前提当前不成立，明确NotRun而未伪造。

### Q18b · 实际进行独立完整审查

来源：T-INSIGHTS-MCP-REPAIR-20261030-04:request_snapshot。状态：已实现。

> 开始审查

新只读执行者独立读取原文、构造新失效视角并完成全部领域；没有把上一轮无问题作为前提。

证据：results.json；original-sources.json

### Q19 · 绑定当前最新Git交付，暂停/旧版轮次不计数

来源：T-INSIGHTS-MCP-REPAIR-20261030-04:request_snapshot。状态：已实现。

> 拉取最新代码并重启审查

审查固定cbf64e8与110项afeaa7c6...；旧轮次/暂停第四轮不累计；本轮有问题计数0。

证据：hash-start.json；hash-end.json；../restart-20261030/session.json

## 全部领域与实际检查

|范围|状态与实际检查|证据|
|---|---|---|
|S01 原始需求、原澄清、权限源与冻结版本|Complete；完整重读3个before原文和澄清，并直接读取DAILY before原权限与完整上下文；无预设结论。|original-sources.json；hash-start/end.json|
|S02 原生2025-11-25初始化/通知/资源/ID/错误/原值|Complete；新ID数值和literal字符串、严格类型、精度、协议媒体/版本边界全部执行。官方客户端MUST不误当服务器额外拒绝义务。|synthetic-results.json；regression.log；live-results.json|
|S03 11工具、14表payload、正文译文业务ID来源版本|Complete；全部11工具、14表执行，11非空+3空；实际body_plain_text等键存在且原值相等，无缺键None==None证明。|live-results.json；body-provenance.json|
|S04 五分页完整小集合、cursor和version冲突、禁止半结果|Complete；五类均有第二页并遍历结束与单大页逐对象相同；改过滤/篡改游标拒绝、五类合成409/422、SDK重复/版本/超页/工具失败不输出部分汇总。|live-results.json；synthetic-results.json；client-results.json|
|S05 日期统计、primary/all_issues与历史副本限制|Complete；一日634来信完整分页，primary三级mail/issue/pending逐桶独立重算；all_issues一级每桶完整成员数与daily一致，选中小集合context唯一成员一致；all_issues问题数及父级去重SQL逐行核对。|live-results.json；insights/projection.py:97-125|
|S06 完整指南/Schema/7下载/23文件KIT与秘密隔离|Complete；7项真实下载逐字节匹配，11 Schema逐对象相同，23包路径及全部校验和，三程序源码一致，无真实Bearer/私钥/数据库URL。维护交接R7-003。|live-results.json|
|S07 下载stdlib+SDK+workflow与Windows安全配置|Complete；三客户端接入、全11workflow；真实首字节前ACL，已有文件保护和partial/fsync/ACL失败清理。|client-results.json；live-results.json|
|S08 单管理员/会话/CSRF/Host/Origin/实际peer/限流/并发|Complete；唯一凭据、挑战/会话时效、轮换、注销Cookie、重复字段、跨会话、KDF竞态、peer代理头边界；登录限流成立，MCP工具频率限制缺失R7-002。|regression.log；synthetic-results.json；boundary-results.json|
|S09 令牌原子存储/线程及进程并发/撤销故障安全|Complete；新server-commit注入、orphan元数据重试、损坏metadata紧急撤销、最后枚撤销、损坏授权原字节保留、12线程与原跨进程测试。|regression.log；synthetic-results.json|
|S10 原生网页/复制/筛选/确认/窄屏/历史|Complete；本人设计、根执行原生UI新用例；恶意身份拒绝、合法64字符、复制相等、关闭/历史、取消不POST、确认撤销、退出历史；筛选无匹配/清空7行/前缀1行全部实际执行，指南11Schema中首个展开复制与剪贴板相同、正文窄屏正常；发现flash裁切R7-001。|browser-results.json；browser-supplement.json；filter-vm-results.json；browser-long-revoke-flash-360.png|
|S11 真实严格CA/部署/保护范围/证据真实性|Complete；严格CA握手、错误CA拒绝、实际Host/Origin、6部署文件一致、监听；未做真实管理员或生产/数据库操作；任何夹具失误均保留。|boundary-results.json；hash-start/end.json|

45项现有测试全部通过；新增真实249项、合成70项、客户端下载与ACL9项、真实CA与边界12项、正文/AI精确键6项检查全部通过。计数为不同粒度检查组，不能相加冒充单元测试数。确认反例R7-001/002/003独立保留，不用正向全绿掩盖。

五类完整小集合均有第二页并遍历到null，与同条件单大页逐对象比较；不是遍历全部历史库。版次24、production-ai-customer、历史副本DEGRADED。完整一日邮件634封用于primary三级统计独立重算，不声称已验证当前生产或全历史所有记录。真实ID/payload/正文只在内存，证据仅布尔、聚合、文件hash。

浏览器由根按本审查者新设计用例执行；本人读取browser-results及亲自查看截图独立评定。3041只改HTTPS/peer/cookie运输，不作TLS/权限安全证据；本版6部署文件与Git逐字节一致另有真实3029/3037严格CA/Host/Origin证据。

## 旧问题处置

|旧ID|本轮处置|依据|
|---|---|---|
|R1-01|Fixed|challenge限额、刷新复用、时效恢复；45测试当前重跑|
|R1-02|Fixed|损坏metadata仍能网页登录撤销；新合成损坏文件撤销对照|
|R1-03|Fixed|原始类型与精度先于SDK验证，后端零调用|
|R1-04|Fixed|未知工具顶层-32602且id保留|
|R2-01|Fixed|字符串null/[]/{}/引号值逐值保持|
|R2-02|Fixed|新真实Windows Users可读父目录，首字节前ACL及失败清理|
|R2-03|Fixed|新分层错误、无敏感回显；Content-Type400属于传输拒绝|
|R3-01|Fixed|凭据单快照绑定与轮换失效，当前45测试|
|R3-02|Fixed|新ID整数/字符串/精度反例，通知202/资源正常|
|R3-03|Fixed|五工具空cursor拒绝及新五游标版本/过滤绑定|
|R3-04|PartiallyFixed/Recurred|原25/12已标历史，但当前又错误指task03为当前；R7-003|
|R5-001|Fixed|同peer成功/失败KDF竞态当前45测试通过|
|R5-002|Fixed|新增高精度fraction/exponent拒绝及合法整数保留、后端调用计数对照|
|R5-003|Fixed|首页JSON可解析、真实页含带引号占位值|
|R5-004|Fixed|same-origin策略及原生表单登录/发放/撤销/退出成功，null仍拒绝|
|R5-005|Fixed|table/grid及revoke inline确认在360px可以操作；新alert反馈缺陷另列R7-001|

R3-04原25/12历史数量更正仍存在，但交接把第三次旧报告称当前的同类问题已复现，不能登记整个旧项Fixed。R5-005原grid/表格修复已验证；新alert文本不属于该修复覆盖，独立编号R7-001。

## 外部限制、未验事实和证据更正

- 另一台内网电脑的路由、CA安装及真实接收人环境未实测，不能宣称已验证。
- 正式独立/安全隐私人类Gate和user_decision仍Pending；当前保存结果Deferred，原官方Offer拒绝未绕过。
- 未读、重发或重置真实管理员口令；历史交付只有既有维护记录，本轮未重核用户私聊实际收件。
- 历史副本版本24、状态DEGRADED；本轮不做生产实时一致审计。
- IAB从POST结果真实后退到chrome-error且无新HTTP；forward无令牌。不能把该行为声称产品POST重执行或真实BFCache检验；server GET/重复POST及当前pagehide/pageshow源码另有分工。

这些已明确外部限制不冒充产品失败；3项确认产品/交付问题仍Open。正式人类Gate与用户验收Pending；不写官方Passed/ManagedByParent。

- 最初HTTP头dict按大小写敏感读取，导致8项错误失败；修正小写归一后全部249项通过，旧JSON/日志保留。
- SDK max-pages的RuntimeError经anyio包装为ExceptionGroup；夹具改递归检查，不改产品，保留原失败日志。
- 合成Content-Type预期415过严；实际SDK security层先400拒绝，官方未规定该具体码；更正测试预期为400并保留旧输出。
- 两次相对路径只读Get-Content误在repo下找round7日志；原命令报错，改绝对/正确cwd重读，未影响产品。

所有写入都在本轮独立round7；45测试的临时.runtime也因cwd置于round7而隔离。没有运行真实管理验证器、配置/令牌变更、build、生产/数据库/watch或服务重启。发现问题后保持冻结至终hash，根应先修复、保存新版再从0启动完整审查。
