第一轮独立只读对抗性审查结果：发现 4 项可复现问题，本轮不是干净轮次。未修改产品、服务、凭据、防火墙及既有治理记录；未读取任何 .secrets 文件，未连接数据库，未进行真实管理员登录或签发。

审查基线：D:/LFEN_project/dev_project/complaint-insights；交付任务 T-INSIGHTS-MCP-PORTAL-20261030-01。独立读取 before.json 的完整 request_snapshot、clarification（唯一一轮、真实答复“继续”）、scope、acceptance 和 authority；另读 discovery/survey.md 的既有权限原话。当前 30 个 delivery-files.json 文件摘要全部匹配，捕获的真实工具 Schema 与隔离进程当前代码生成的 11 工具 Schema 相同。原交付 after.json 的 Deferred、user_decision Pending 和两个正式人类门禁 Pending 保持原意，本次审查不替人类批准。

原文逐项覆盖（同一完整长句保存在上述 request_snapshot，以下为独立拆解）：

|编号|原文要求/限定|状态|独立证据及差异|
|---|---|---|---|
|U01|“MCP工具后续我会给其他人使用”|部分实现|公开 ZIP 有 23 项、校验和正确、脚本与当前代码一致；真实独立接收人电脑未检查，另见 U03、U04 的反例。|
|U02|“MCP工具的介绍需要比较详细”|已实现|独立读完整指南模板、逐参数生成器、真实 Schema、数据/权限/来源/分页/错误/交接说明；11 工具与 14 表目录齐全。|
|U03|“请按照MCP本身的协议来制作文档或者程序”|部分实现|隔离 HTTP 完成 initialize→initialized(202)→tools/list(11)，协商 2025-11-25、无会话头、GET/DELETE 405、超限体 413、非法协议头 400；R1-03、R1-04 仍违背公开输入契约及错误分层。|
|U04|“给其他要用该MCP的人，让他们能够使用我的MCP”|部分实现|指南和两类客户端完整；ZIP、所有指南离线本地引用和参数示例核对通过。当前真实数据查询沿用已保存证据，本轮不加载接收人凭据；异机接入仍未实测。|
|U05|“MCP token生成所运行的服务你也需要优化并复核一下”|部分实现|唯一所有者、独立认证、会话/CSRF/退出、最后一枚撤销、并发、损坏关闭的现有 25 项测试重跑全部通过；新增 R1-01/R1-02 证明登录可被匿名阻断、故障下网页撤销不可达。|
|U06|“然后在内网开放该服务入口（生成token的服务）”|已实现，异机未验证|现场监听 3029/3037 为 192.168.10.20；通过现有 CA 严格验证公开 3029 首页/指南/下载均 200；匿名 /admin 为 303，匿名 MCP 为 401。另一台电脑的路由/CA安装尚无本轮证据。|
|U07|“将该MCP的使用协议介绍方法等，放置在生成token的服务上”|已实现|实际 /guide 为 200；七个公开下载均与本地发布文件逐字节相同，首页公开材料、身份和接入链接完整。|
|U08|“后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多”|部分实现|一个入口包含 CA 首次信任、本人令牌、客户端、工具/表参考及排错；两张既有 UI 预览可读，源码有窄屏和键盘焦点支持；R1-01 的匿名请求会阻断唯一发放入口。|
|U09|“开一个新会话处理MCP相关事宜，本会话继续完成客诉日报看板”|已遵守本轮范围|未改 3030、日报、附件、source.py、syncer.py、旧任务或 AICS；只读必要依赖及限定产品面。本轮没有服务/防火墙修改。|
|U10|“继续”及澄清答复“继续”|已遵守|不解释为新增管理员、OAuth、SSO、生产操作或正式人类门禁批准。|
|U11|既有原话：“需要我下发的token才能够实际访问MCP”|已实现，故障撤销部分实现|匿名真实 MCP tools/list 为 401；隔离 Bearer 不可管理测试、失效关闭和撤销旧令牌测试均通过；R1-02 使所有者在元数据损坏时无法通过网页完成撤销。|
|U12|澄清：“普通内网访客均只能阅读文档、下载无凭据客户端；只有登录管理员才能生成或撤销 MCP 令牌”，沿用唯一所有者|部分实现|独立认证/会话/CSRF、匿名禁止管理、公开白名单成立；R1-01/R1-02 影响被授权管理员的可用性；没有确认权限提升。|

完整审查面：逐条原文及澄清；token_desk.py 全文、mcp_tokens.py 全文、mcp_http.py 全文、mcp_server.py 全文；MCP 公开构建、协议/SDK/工作流客户端、管理配置脚本、验证器、防火墙脚本、manage.ps1 的受限服务运行约定；MCP config 示例与 CA 公钥；token-desk CSS/JS；两组现有测试全文及重跑；任务 PRD/设计/发布指南/交接/Schema/覆盖/结果/清单/布局及两张预览；必要的 capabilities、datasets、API 参数/分页边界以及 MCP SDK 的参数验证和错误处理依赖。没有以实施者“Passed”报告代替反例验证。

|ID|级别|位置|复现输入/步骤|预期|实际|影响|
|---|---|---|---|---|---|---|
|R1-01|P2|insights/token_desk.py:194-200（挑战回收/全局上限），201-204（每次发新挑战）|同一匿名合成 TCP 来源、同一 TestClient 连续 GET /admin/login 512 次；随后另一 TCP 来源的新客户端打开登录页。|单个访客反复重载应被限制在该来源，不耗尽所有管理员的登录入口。|512 次均 200；另一来源 GET 为 429，没有登录表单；时间推进 601 秒后恢复 200。|无需管理员或 MCP 凭据即可阻断唯一发放管理员登录约 10 分钟；重复填满可持续阻断。所有旧挑战都保留，即使同一客户端 Cookie 已被新挑战替换。|
|R1-02|P2|insights/token_desk.py:162-166（元数据故障直接返回），251-253（管理页）；对照 insights/mcp_tokens.py:119-133|隔离 token 授权文件正常、管理员凭据正常、registry.json 写入一个不完整 JSON“{”；完成管理员登录后 GET /admin。|独立管理员应保留可达的紧急撤销表单，元数据损坏不能阻止撤销有效授权。|登录 303；管理页 503，没有 CSRF、身份列表或 /revoke 表单；授权文件仍有 1 枚有效令牌。同条件直接调用 revoke_token 成功变成 0。|“元数据失败不阻止紧急撤销”的底层能力未接到网页；所有者必须依赖服务器修复/代码调用，不能用已交付入口阻断泄露的有效凭据。现有 test_corrupt_metadata_prevents_issue_but_not_emergency_revoke 仅测函数，未测 UI 可达性。|
|R1-03|P2|insights/mcp_server.py:117-131（注册/默认参数验证），157-190（声明类型）；release/client-guide.template.md:109/154；SDK utilities/func_metadata.py:139-147|真实隔离 HTTP tools/call：list_mails(limit="1")；list_mails(limit=true)；list_source_records(table="messages", include_payload="false")；get_report_context(start=0,end=86400)。|按公布 inputSchema 的 integer/boolean/string(date) 校验；错误类型返回 isError，且不调用查询后端。|全部 HTTP 200、isError=false，并调用 FakeAPI；分别隐式转换为 limit=1、limit=1、include_payload=false、日期 1970-01-01/1970-01-02。|公开 Schema 与执行接受范围不一致，错误客户端输入被当成成功查询；日期/敏感载荷开关存在隐式解释。指南明确要求真实 JSON 类型，却没有对应的服务边界校验。额外参数 mailbox 被 get_report_context 静默丢弃亦已观察，作为同一宽松验证问题的补充，不另建重复问题。|
|R1-04|P2|insights/mcp_server.py:111-131（沿用默认 MCPServer 错误处理）；SDK tools/tool_manager.py:83-85、server.py:437-456|隔离 HTTP：{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"fixture_unknown_tool","arguments":{}}}。|固定版官方 Tools 的 Error Handling 将 Unknown tools 归为顶层 JSON-RPC 协议错误，示例为 -32602。|HTTP 200、没有顶层 error；响应为 result.isError=true。SDK 将 Unknown tool 抛为 ToolError 后统一转换为执行错误。|调用方不能按协议错误与业务执行错误区分工具发现/命名故障；“按 MCP 协议”交付存在一条未覆盖错误分支。不能仅以依赖默认行为证明符合固定版规范。|

协议核对只使用官方固定版：

- [MCP 2025-11-25 Transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)：Origin、POST/GET、202 通知、协商版本头和 405 边界。
- [MCP 2025-11-25 Lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)：初始化、就绪通知与后续协商版本头。
- [MCP 2025-11-25 Tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)：inputSchema 和 Error Handling（Unknown tools 为协议错误，输入值/业务失败为 isError）。
- [MCP 2025-11-25 Authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)：核对文档明确为手工发放认证、没有宣称提供 OAuth 发现或完整 OAuth 实现；本轮没有扩展 OAuth 要求。

复现证据（全部位于本轮独立目录）：

- reproduce.py：新建独立合成授权文件/管理员文件，使用同一产品 create_app/create_http_app；FakeAPI 不连接数据库；唯一的内存 patch 为跳过 MCPSettings.validate 对真实私钥路径的启动校验，未 patch 登录、令牌、工具输入或错误处理代码。
- results.json：23 组隔离观察，含控制案例、4 项反例、Schema/清单/ZIP/离线引用核对。
- public_read.py / public-read.json：仅匿名读取真实公开路由；严格 CA 验证；7 个公开下载与当前发布文件一致；保护文件路径 404、管理页重定向、MCP 匿名 401。未调用真实数据工具或管理员签发。
- existing-tests.log：在本轮目录作为 cwd，PYTHONDONTWRITEBYTECODE=1，TEMP/TMP 指向本轮目录，重跑现有 25 项测试，全通过；夹具写入均在本轮目录。全绿没有覆盖或否定上述反例。

未检查或受限项：

1. 不使用真实管理员/接收人秘密，故本轮没有真实签发→读取→撤销、真实 11 工具和真实 22 页遍历的新证据；已读既有 results.json，但不把既有通过当成本轮独立执行。
2. 未在另一台内网电脑测试路由、私有 CA 安装、本人配置及 SDK；该项原交付本已明确未验收。
3. 不读取 .secrets，因此 allow_production_read=false、当前后端凭据和目标数据库配置只核对已有脱敏结果及回环监听，未独立读取当前秘密配置；没有数据库连接。
4. 未对真实服务执行挑战耗尽、高负载、存储损坏、凭据轮换或并发写入；这些使用隔离夹具/现有隔离测试。
5. 只读检查既有 UI 截图、CSS、语义标记及布局证据；没有新增真实浏览器管理员交互和不同浏览器渲染证据。
6. 未检查与本任务无关的日报、附件下载、本地数据库内容、AICS 或旧审查历史；未触碰正式人类门禁。它们不是本轮产品范围扩展。

结论：当前版本至少有 R1-01 至 R1-04，第一轮连续干净计数为 0。原交付已声明的异机实测及正式人类门禁缺口仍保留。范围阅读完整，实际验证有上述明确限制，不能声明全部运行链路已由本轮独立验收。
