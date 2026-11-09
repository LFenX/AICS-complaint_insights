# MCP内网接入门户 PRD

目标：接收人获得一个内网HTTPS链接，能独立完成了解工具、安装可信CA、配置本人令牌、选择来源和验证查询。

|角色|可执行|禁止/禁用原因|
|---|---|---|
|内网访客|说明、schema、CA公钥、无凭据客户端与示例下载|无管理员会话，不能列身份、发放、撤销；无MCP Bearer不能查询客诉|
|MCP接收人|本人Bearer调用11个只读工具，读取已发布本地来源|MCP Bearer不是管理员凭据；没有写入、任意SQL、采集或生产控制工具|
|唯一所有者管理员|独立登录，列身份元数据、逐人发放和撤销、退出|凭据未配置/失效则管理禁用；同源CSRF或安全会话失败即拒绝；不提供查看旧token|

模块：接入首页、快速开始、原生协议、工具选择、11工具逐参数参考、数据口径、下载、排错、管理员登录及令牌管理。页面适配桌面和窄屏，有键盘焦点、明确标签、错误提示及空态。

动作：docs.read/download.read为LOW只读；admin.login/logout为HIGH认证动作；token.issue/revoke为HIGH GLOBAL，权限insights.tokens.manage -> insights.admin -> insights。

审计：记录request_id、实际TCP来源、管理员标签、动作、目标身份、状态、时长；不记录口令、cookie、csrf、Bearer、表单、查询参数或客户内容。管理响应no-store；所有页面防嵌入、同源CSP、no-referrer、nosniff。登录失败限速，session空闲20分钟/最长8小时，重启或管理员凭据变更失效。

验收契约：访客公开读取成功但管理拒绝；MCP身份不能成为管理员；无/错/跨会话CSRF和跨Origin被拒绝；HTTPS+Host+真实网段验证，代理头不能绕过；单人唯一token、并发无丢写、损坏配置不恢复/覆盖、撤销立即失效且允许撤销最后一枚。下载固定白名单，材料不含任何现存凭据或私钥；源码schema与实际远端发现一致。

数据边界：production-ai-customer为已停采的历史本地副本；显式source_id并查get_sync_status，不承诺实时生产。所有有效MCP令牌有相同只读工具和来源范围，独立身份仅用于分发、审计和撤销，不宣称字段/来源级隔离。
