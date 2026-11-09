# 第8轮独立只读对抗性审查

本次使用 skill：run-governed-product-workflow / verify。

**结论：覆盖 Complete，发现2项确认问题，非干净轮次；不满足审查通过条件。**

审查时间：2026-10-29T23:16:12.8683243Z 至 2026-10-29T23:38:44.5222365Z（UTC；北京时间+08:00）。
交付：task05；HEAD `88ef76cc582c2cb36eeb51febace6ada57afef00`；125文件版本 `7fb70b2a88eff771a9da327c80ec5c6ca9aad039bfefdcbe616071ae381acb47`。
工程结果保存于2026-10-29T23:14:35.915100Z，正式状态Deferred；本轮独立读取摘要为 `9ac2ce33f8235fe2bc1894b2cb4f7950f2b12f89051a5748668771ff6138a609`。

起止125文件逐项SHA一致、Git均干净、3029/3037/3030/3036/15433的PID与监听地址完全相同，详见start.json/end.json。本轮只在round8留证；没有产品修改、真令牌变更、重启或数据库连接。

本轮先独立重读需求原件，再读取前轮问题以核对处置；没有采用前轮“无问题”为正确前提。全量原话/所有实际澄清保存在original-sources.json，各条SHA取完整request_snapshot.text或该次实际answer，不是摘录quote。

## 确认问题

### R8-001 · P2 · 保留的stdio CLI在精度丢失后验证工具整数参数，非整数被静默取整并进入后端

- 位置：scripts/mcp_server.py:10；insights/mcp_server.py:138；insights/mcp_server.py:139
- 复现：运行本轮stdio_fixture.py：runpy执行冻结scripts/mcp_server.py，唯一patch为ReadAPI.load返回FakeAPI；完成initialize/initialized后逐条发送probe_stdio.py保存的原始JSON行。
- 预期：数学值均非整数，第三项还小于最小值1；应返回isError且后端调用数不增加。1.0和2e0为数学整数，应允许。
- 实际：三个原始反例均isError=false，FakeAPI依次收到limit=1/200/1，backend_calls=1/2/3；2.5/true/字符串1拒绝；1.0/2e0允许。真实HTTP同三反例均isError=true。
- 原因：wire_arguments只由HTTP的MCPProtocolErrors设置。stdio SDK已将原始小数转成binary float，ContractMCPServer退回arguments后无法恢复原值。
- 影响：stdio调用接受公布integer/范围契约不允许的输入并改写查询参数，返回成功；不构成远程鉴权绕过或数据库写入。
- 证据：stdio-results.json；stdio_fixture.py；probe_stdio.py；live-results.json#/groups/raw_number_precision
- 规范来源：[tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)、[json-schema-validation](https://json-schema.org/draft/2020-12/json-schema-validation)

### R8-002 · P2 · stdio实际CLI静默丢弃合法整数值的小数/指数形式请求ID

- 位置：scripts/mcp_server.py:10；insights/mcp_server.py:133；insights/mcp_http.py:178
- 复现：同一真实stdio CLI夹具完成初始化；发送tools/list，id依次为701、702.0、703e0、704.00000000000000001、true、字符串string-705；每条单独原始JSON行。
- 预期：701、702.0、703e0与字符串均须收到对应ID的结果；704.00000000000000001和true属于非法请求ID，应按Invalid Request处理，不能要求保留其非法原ID。
- 实际：701和string-705均返回11工具；数学整数702.0和703e0各2秒无响应。两项非法ID也无响应，作为独立非法控制记录。HTTP相同合法表示均200并归一整数ID，非法fraction/bool均400/-32600/id=null。
- 原因：stdio入口直接使用SDK validate_json，未经过HTTP的请求ID原值与整数表示归一保护。锁定SDK的联合模型将702.0/703e0等带ID输入解析为JSONRPCNotification，id丢失，产品没有相应修正边界；原始解析模型实测见stdio-parser.json。
- 影响：使用合法数值ID表示的本机MCP客户端等待到超时；与公开MCP整数ID契约不一致。远程HTTP路径不受本反例影响。
- 证据：stdio-results.json#/request_ids；stdio-parser.json；stdio_fixture.py；synthetic-results.json#/parameters/request_id_http_counterparts
- 规范来源：[basic](https://modelcontextprotocol.io/specification/2025-11-25/basic)、[json-schema-validation](https://json-schema.org/draft/2020-12/json-schema-validation)

R8-001是旧HTTP精度问题在保留stdio路径的新反例，不声称HTTP修复失效；R8-002把数学整数形式702.0/703e0与非法非整数704.00000000000000001、布尔true明确分开。非法ID不要求在错误中回原ID。夹具执行实际冻结CLI，仅替换凭据/后端依赖，未替换stdio解析、工具验证、SDK或输出。

## 方法与覆盖

C与D代码各49测试通过。新增187项参数拒绝、11工具全参数有效组合/输出Schema、低配额假时钟与24并发仅5个后端调用、五分页工具30个条件分支、5个日期边界/4个AI分类对照、6项客户端异常/真实Windows合成ACL对照。

真实HTTPS采用现有CA严格验证且禁用环境代理、禁止重定向；17组只读结果涵盖11工具/guide、14表、正文与完整AI/源行、845封当日邮件5页与API逐行内存相同，primary总数845、all_issues跨类869。公开7下载与冻结文件逐字节相同，ZIP23项、22个内部checksum全部匹配。未输出口令、token、私钥、正文或完整业务行。

原生浏览器由root按本轮独立用例通过cua执行，360×800纯合成loopback夹具；12项观察覆盖required、非法身份400、合法长身份签发/复制/重载一次显示、同名400、撤销和退出后back/reload。没有响应策略覆写或cookie注入。此证据不证明真实TLS、实际TCP来源或Secure Cookie；它们由独立HTTPS/ASGI与工程证据分工覆盖。

|领域|结果|实际与证据|
|---|---|---|
|本地只读/生产隔离|Checked|只经HTTPS或回环API读现有副本；生产false/watch停止；没有数据库连接。 证据：runtime-boundaries.json；readmodel-results.json|
|11工具与guide资源|Checked|实际tools/list与公开schema相等，资源与tool策略相等。 证据：live-results.json|
|14白名单/原始追溯|Checked|14表一页及非空表完整行可达，3空表保留合法；无任意SQL。 证据：live-results.json；synthetic-results.json|
|统计/日期/AI规则|Checked|845邮件与primary总数相等；all_issues869交叉不误作去重总数；PEND/人工排除及UTC+8边界。 证据：live-results.json；readmodel-results.json|
|正文/译文/完整AI|Checked|include_raw默认剔除、显式读取完整AI/原始字段；正文开关与API逐对象内存核对，不输出正文。 证据：live-results.json|
|全量分页/冲突|Checked|5页845无重复；五工具变筛选/来源/版本冲突；客户端中断无伪完整。 证据：live-results.json；readmodel-results.json；synthetic-results.json|
|全工具参数/输出|CheckedWithFindings|11工具每个公布参数有有效组合，187非法值后端零调用；stdio精度R8-001。 证据：synthetic-results.json；stdio-results.json|
|协商/JSONRPC/错误|CheckedWithFindings|2025-11-25初始化/通知/资源/错误层级；stdio整数表示ID R8-002。 证据：live-results.json；C-tests.log；stdio-results.json|
|限频|Checked|严格1..60000，无禁用，按真实身份跨工具合并；同名重发不重置；默认stdio与HTTP均执行。 证据：synthetic-results.json；C-tests.log；live-results.json|
|单管理员/挑战/会话|Checked|独立凭据hash、peer绑定挑战、失败限额、会话轮换/超时/退出；不重置真实owner。 证据：C-tests.log；synthetic-results.json；browser-native.json|
|CSRF/Origin/null/权限分离|Checked|所有native表单same-origin，缺失/null/外源Origin和重复csrf拒绝；Bearer不授管理。 证据：browser-native.json；synthetic-results.json；C-tests.log|
|一次显示/重发/撤销/恢复|Checked|同名拒绝、原生复制和重载移除、最后撤销/并发/损坏授权关闭/损坏metadata可撤销。 证据：browser-native.json；synthetic-results.json；C-tests.log|
|静态UI/窄屏真实表单|Checked|360x800真实cua原生操作；没有改响应策略或注入cookie；合成HTTP不替代TLS证明。 证据：browser-native.json；mobile-duplicate.png；mobile-revoked.png|
|文档/下载ZIP/秘密/ACL|Checked|7下载一致、23项ZIP内部checksum全匹配；无当前Bearer/API凭据/私钥标记；真实Windows合成ACL。 证据：live-results.json；synthetic-results.json；documentation-observed.json|
|真实TLS/网络/Host/代理|Checked|实际内网IP正确CA验证；Host421/Origin403；实际peer/代理拒绝在ASGI和当前49中覆盖；外机未实测。 证据：live-results.json；firewall.json；C-tests.log|
|证据/失败留存/部署边界|Checked|当前task05工程结果与旧阶段隔离；保留本轮夹具失败；125冻结/PID/Git起止核对。 证据：governance-observed.json；failure-notes.json；start.json；end.json|

## 原文逐条对照

以下逐条保留同来源完整原句，不用单词摘录或其他轮同字答复抵消。每条状态、实际、差缺和证据独立给出；有条件则同时列Met/NotMet，未执行明确NotRun。未来生产接通、异机环境、历史私聊消息和两轮收敛属于限定/证明状态，不伪装为本轮已实现验收。

### F01 · 已实现 · 先用本地开发数据建立独立数据库与读取模型

来源：T-INSIGHTS-FOUNDATION-20261029-01 / `request_snapshot`；完整原文SHA256 `8eb32ed764ff33f6a20052cbd7c0abe22ea9d1614f2031da5d0e628604b1da53`。

> 你可以先用本地开发数据先推进本地的数据库建立，后续只要生产数据库连接接通，可以快速实现我后续的规划

实际：现有独立副本/回环API可查；本轮未建立或连接任何数据库，只读模型与配置分离代码已核对。
差缺：本条未确认实现差缺。
证据：readmodel-results.json；live-results.json#/groups/source_state；runtime-boundaries.json

- Unconditional / Passed：输入 先用本地开发数据建立独立数据库与读取模型；预期 先用本地开发数据建立独立数据库与读取模型；实际 现有独立副本/回环API可查；本轮未建立或连接任何数据库，只读模型与配置分离代码已核对。。证据 readmodel-results.json；live-results.json#/groups/source_state；runtime-boundaries.json

### F02 · 部分实现 · 生产接通后的快速切换准备，保留条件

来源：T-INSIGHTS-FOUNDATION-20261029-01 / `request_snapshot`；完整原文SHA256 `8eb32ed764ff33f6a20052cbd7c0abe22ea9d1614f2031da5d0e628604b1da53`。

> 你可以先用本地开发数据先推进本地的数据库建立，后续只要生产数据库连接接通，可以快速实现我后续的规划

实际：生产模板与source_id分离已实现；当前allow_production_read=false、watch停止；未来连通分支未执行。
差缺：本轮禁止连接源库；不能把准备配置等同已完成生产连接验收。
证据：readmodel-results.json#/source_isolation；runtime-boundaries.json；original-sources.json

- Met / NotRun：输入 未来经授权连接生产；预期 可按独立来源切换并核对；实际 NotRun：没有进行连接。证据 runtime-boundaries.json
- NotMet / Passed：输入 production且allow_production_read=false；预期 连接前拒绝；实际 validate(source=True)在连接前抛disabled；watch PID不存在。证据 readmodel-results.json；runtime-boundaries.json

### F03 · 已实现 · 提供查询不同数据的接口

来源：T-INSIGHTS-FOUNDATION-20261029-01 / `request_snapshot`；完整原文SHA256 `8eb32ed764ff33f6a20052cbd7c0abe22ea9d1614f2031da5d0e628604b1da53`。

> 提供查询不同数据的接口

实际：全部11工具、14源表及全文/原始AI行入口可用。
差缺：本条未确认实现差缺。
证据：live-results.json；synthetic-results.json#/parameters

- Unconditional / Passed：输入 提供查询不同数据的接口；预期 提供查询不同数据的接口；实际 全部11工具、14源表及全文/原始AI行入口可用。。证据 live-results.json；synthetic-results.json#/parameters

### F04 · 部分实现 · 接口以MCP形式构建

来源：T-INSIGHTS-FOUNDATION-20261029-01 / `request_snapshot`；完整原文SHA256 `8eb32ed764ff33f6a20052cbd7c0abe22ea9d1614f2031da5d0e628604b1da53`。

> 并给出说明，注意接口工具以MCP形式构建，并提供相关说明，后续方便和其他人交接如何使用这些工具，按需调用所需数据

实际：真实HTTPS协商2025-11-25；stdio实际CLI可初始化，但R8-001/R8-002存在。
差缺：stdio数字原值和整数ID处理有缺陷。
证据：live-results.json；synthetic-results.json；readmodel-results.json；stdio-results.json

- Unconditional / Failed：输入 接口以MCP形式构建；预期 接口以MCP形式构建；实际 真实HTTPS协商2025-11-25；stdio实际CLI可初始化，但R8-001/R8-002存在。。证据 live-results.json；synthetic-results.json；readmodel-results.json；stdio-results.json

### F05 · 已实现 · 提供使用说明并支持交接

来源：T-INSIGHTS-FOUNDATION-20261029-01 / `request_snapshot`；完整原文SHA256 `8eb32ed764ff33f6a20052cbd7c0abe22ea9d1614f2031da5d0e628604b1da53`。

> 并给出说明，注意接口工具以MCP形式构建，并提供相关说明，后续方便和其他人交接如何使用这些工具，按需调用所需数据

实际：完整中文指南、公开无凭据23文件包、全部schema与运行工具一致。
差缺：本条未确认实现差缺。
证据：live-results.json；synthetic-results.json；readmodel-results.json；stdio-results.json

- Unconditional / Passed：输入 提供使用说明并支持交接；预期 提供使用说明并支持交接；实际 完整中文指南、公开无凭据23文件包、全部schema与运行工具一致。。证据 live-results.json；synthetic-results.json；readmodel-results.json；stdio-results.json

### F06 · 已实现 · 按需调用所需数据

来源：T-INSIGHTS-FOUNDATION-20261029-01 / `request_snapshot`；完整原文SHA256 `8eb32ed764ff33f6a20052cbd7c0abe22ea9d1614f2031da5d0e628604b1da53`。

> 并给出说明，注意接口工具以MCP形式构建，并提供相关说明，后续方便和其他人交接如何使用这些工具，按需调用所需数据

实际：日期分类/来源、正文和payload显式加载、完整分页与版本冲突已独立检查。
差缺：本条未确认实现差缺。
证据：live-results.json；synthetic-results.json；readmodel-results.json；stdio-results.json

- Unconditional / Passed：输入 按需调用所需数据；预期 按需调用所需数据；实际 日期分类/来源、正文和payload显式加载、完整分页与版本冲突已独立检查。。证据 live-results.json；synthetic-results.json；readmodel-results.json；stdio-results.json

### F07 · 部分实现 · 供其他内网电脑的Agent直接远程调用

来源：T-INSIGHTS-FOUNDATION-20261029-01 / `clarification:r1.e1`；完整原文SHA256 `cea98928f5577bcb9b5a100ee2f1cf962249b99d23d08227c4c61197d383099f`。

> 需要其他内网电脑的 Agent 直接远程调用

实际：服务监听内网指定IP、严格CA验证成功；另一台电脑环境未实测。
差缺：已实现远程服务能力；接收方机器的路由、CA安装、本人配置仍须在该机器验收。
证据：live-results.json；firewall.json；original-sources.json

- Met / Passed：输入 本机用真实内网IP/正确CA/有效Bearer；预期 允许标准MCP查询；实际 11工具/14表成功；异机相同前提未实际执行。证据 live-results.json
- NotMet / Passed：输入 无效Bearer或不在网段；Origin=null/错误Host；预期 拒绝；实际 49测试中鉴权/真实peer拒绝；真实HTTPS Host421/Origin403。证据 C-tests.log；D-tests.log；live-results.json

### H01 · 已实现 · 保留本地独立数据底座

来源：T-INSIGHTS-REVIEW-20261029-01 / `request_snapshot`；完整原文SHA256 `8eb32ed764ff33f6a20052cbd7c0abe22ea9d1614f2031da5d0e628604b1da53`。

> 你可以先用本地开发数据先推进本地的数据库建立，后续只要生产数据库连接接通，可以快速实现我后续的规划

实际：历史同文要求在本版重新对照；本地查询/文档可用，协议stdio缺陷另列。
差缺：本条未确认实现差缺。
证据：readmodel-results.json；live-results.json；stdio-results.json

- Unconditional / Passed：输入 保留本地独立数据底座；预期 保留本地独立数据底座；实际 历史同文要求在本版重新对照；本地查询/文档可用，协议stdio缺陷另列。。证据 readmodel-results.json；live-results.json；stdio-results.json

### H02 · 已实现 · 保留不同数据查询接口

来源：T-INSIGHTS-REVIEW-20261029-01 / `request_snapshot`；完整原文SHA256 `8eb32ed764ff33f6a20052cbd7c0abe22ea9d1614f2031da5d0e628604b1da53`。

> 提供查询不同数据的接口

实际：历史同文要求在本版重新对照；本地查询/文档可用，协议stdio缺陷另列。
差缺：本条未确认实现差缺。
证据：readmodel-results.json；live-results.json；stdio-results.json

- Unconditional / Passed：输入 保留不同数据查询接口；预期 保留不同数据查询接口；实际 历史同文要求在本版重新对照；本地查询/文档可用，协议stdio缺陷另列。。证据 readmodel-results.json；live-results.json；stdio-results.json

### H03 · 部分实现 · 保留MCP/说明/按需交接

来源：T-INSIGHTS-REVIEW-20261029-01 / `request_snapshot`；完整原文SHA256 `8eb32ed764ff33f6a20052cbd7c0abe22ea9d1614f2031da5d0e628604b1da53`。

> 并给出说明，注意接口工具以MCP形式构建，并提供相关说明，后续方便和其他人交接如何使用这些工具，按需调用所需数据

实际：历史同文要求在本版重新对照；本地查询/文档可用，协议stdio缺陷另列。
差缺：R8-001/R8-002
证据：readmodel-results.json；live-results.json；stdio-results.json

- Unconditional / Failed：输入 保留MCP/说明/按需交接；预期 保留MCP/说明/按需交接；实际 历史同文要求在本版重新对照；本地查询/文档可用，协议stdio缺陷另列。。证据 readmodel-results.json；live-results.json；stdio-results.json

### H07 · 部分实现 · 本轮历史任务原话也单独保留生产连通条件，不能用foundation同文替代

来源：T-INSIGHTS-REVIEW-20261029-01 / `request_snapshot`；完整原文SHA256 `8eb32ed764ff33f6a20052cbd7c0abe22ea9d1614f2031da5d0e628604b1da53`。

> 你可以先用本地开发数据先推进本地的数据库建立，后续只要生产数据库连接接通，可以快速实现我后续的规划

实际：生产准备配置与来源隔离存在；当前重新授权连通前提不成立。
差缺：生产连通后的实际切换/当前线上一致性未执行；没有当前生产权限。
证据：original-sources.json；readmodel-results.json；runtime-boundaries.json

- Met / NotRun：输入 经重新授权已连通生产；预期 可执行独立来源切换及核对；实际 NotRun：没有连接生产。证据 runtime-boundaries.json
- NotMet / Passed：输入 生产读取禁止；预期 连接前阻止；实际 纯函数配置验证disabled；watch停止。证据 readmodel-results.json；runtime-boundaries.json

### H04 · 已实现 · 远程内网调用澄清

来源：T-INSIGHTS-REVIEW-20261029-01 / `clarification:r1.e1`；完整原文SHA256 `cea98928f5577bcb9b5a100ee2f1cf962249b99d23d08227c4c61197d383099f`。

> 需要其他内网电脑的 Agent 直接远程调用

实际：内网HTTPS能力本轮已查；异机验收限制不变。
差缺：本条未确认实现差缺。
证据：original-sources.json；live-results.json

- Unconditional / Passed：输入 远程内网调用澄清；预期 远程内网调用澄清；实际 内网HTTPS能力本轮已查；异机验收限制不变。。证据 original-sources.json；live-results.json

### H05 · 已实现 · 历史对抗审查授权原话

来源：T-INSIGHTS-REVIEW-20261029-01 / `clarification:r2.e1`；完整原文SHA256 `3895c17df2116237d64ec458bd565d90fa1e2ea9842faf5db2915e94a80b4b3c`。

> 启动多轮对抗性审查

实际：原话确为“启动多轮对抗性审查”；本轮另受最新重启授权。
差缺：本条未确认实现差缺。
证据：original-sources.json；live-results.json

- Unconditional / Passed：输入 历史对抗审查授权原话；预期 历史对抗审查授权原话；实际 原话确为“启动多轮对抗性审查”；本轮另受最新重启授权。。证据 original-sources.json；live-results.json

### H06 · 已实现 · 历史安全隐私Gate答复仅绑定当时对象

来源：T-INSIGHTS-REVIEW-20261029-01 / `clarification:r3.e1`；完整原文SHA256 `1e4f14b1ba75383a5f9bf653068c15c2ff67d55b47cab961289f66c8e9ca5cb3`。

> 通过本次安全隐私门禁，继续审查

实际：已读取该历史答复；不将该旧对象的回答转作当前task05人类Gate批准。
差缺：本条未确认实现差缺。
证据：original-sources.json；live-results.json

- Unconditional / Passed：输入 历史安全隐私Gate答复仅绑定当时对象；预期 历史安全隐私Gate答复仅绑定当时对象；实际 已读取该历史答复；不将该旧对象的回答转作当前task05人类Gate批准。。证据 original-sources.json；live-results.json

### D01 · 已实现 · 隔离生产库；MCP工作与3030日报分工

来源：T-INSIGHTS-DAILY-20261030-01 / `request_snapshot`；完整原文SHA256 `f136041515b0fc751dc801e3b229702bb338403f61eac1ac3aedecefaeaabe6e`。

> 我已经暂停cursor的工作，请隔离生产库，然后做审查并修复问题后，接续cursor的工作，即生成昨天邮件问题的客诉日报看板网页，运行在3030，cursor 的看板做的一塌糊塌，没有严格按照我的要求来，请你严格按照我的标准来完成任务

实际：生产读取false、watch停止；本轮未连库、未改/重启3030/3036/15433或AICS。
差缺：本条未确认实现差缺。
证据：runtime-boundaries.json；start.json；end.json

- Unconditional / Passed：输入 隔离生产库；MCP工作与3030日报分工；预期 隔离生产库；MCP工作与3030日报分工；实际 生产读取false、watch停止；本轮未连库、未改/重启3030/3036/15433或AICS。。证据 runtime-boundaries.json；start.json；end.json

### D02 · 已实现 · 本机副本供复杂聚合

来源：T-INSIGHTS-DAILY-20261030-01 / `request_snapshot`；完整原文SHA256 `f136041515b0fc751dc801e3b229702bb338403f61eac1ac3aedecefaeaabe6e`。

> 你可以把原始数据拿到本机后再做复杂聚合

实际：查询只使用ReadAPI回环和已发布本地读取模型。
差缺：本条未确认实现差缺。
证据：readmodel-results.json；live-results.json

- Unconditional / Passed：输入 本机副本供复杂聚合；预期 本机副本供复杂聚合；实际 查询只使用ReadAPI回环和已发布本地读取模型。。证据 readmodel-results.json；live-results.json

### D03 · 已实现 · 测试MCP能完整取出全部数据

来源：T-INSIGHTS-DAILY-20261030-01 / `request_snapshot`；完整原文SHA256 `f136041515b0fc751dc801e3b229702bb338403f61eac1ac3aedecefaeaabe6e`。

> 搞定以后，测试数据是否完整，MCP访问是否能够正常取出所有数据，并且数据和线上一致没有遗漏
> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

实际：当日845邮件5页无重复，逐行等于API；14表按白名单可查询，3空表合法；未用一页当总数。
差缺：本条未确认实现差缺。
证据：live-results.json#/groups/full_mails_pagination；synthetic-results.json#/parameters；readmodel-results.json

- Unconditional / Passed：输入 测试MCP能完整取出全部数据；预期 测试MCP能完整取出全部数据；实际 当日845邮件5页无重复，逐行等于API；14表按白名单可查询，3空表合法；未用一页当总数。。证据 live-results.json#/groups/full_mails_pagination；synthetic-results.json#/parameters；readmodel-results.json

### D04 · 部分实现 · 数据与线上一致无遗漏的证明边界

来源：T-INSIGHTS-DAILY-20261030-01 / `request_snapshot`；完整原文SHA256 `f136041515b0fc751dc801e3b229702bb338403f61eac1ac3aedecefaeaabe6e`。

> 搞定以后，测试数据是否完整，MCP访问是否能够正常取出所有数据，并且数据和线上一致没有遗漏
> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

实际：本地历史版本24/DEGRADED，最后成功同步2026-10-30T01:14:02.122651+08:00；当前线上一致性未重验。
差缺：禁止生产连接，不能把MCP/API同副本一致当作当前线上一致。
证据：live-results.json#/groups/source_state；runtime-boundaries.json

- Met / NotRun：输入 当前生产可比快照；预期 逐源核对无遗漏；实际 NotRun：禁止连接生产。证据 runtime-boundaries.json
- NotMet / Passed：输入 只读历史副本、生产隔离；预期 明确快照/版本/DEGRADED，不宣称实时线上一致；实际 真实status与公开指南一致。证据 live-results.json

### D05 · 已实现 · 权限网页生成访问token

来源：T-INSIGHTS-DAILY-20261030-01 / `request_snapshot`；完整原文SHA256 `f136041515b0fc751dc801e3b229702bb338403f61eac1ac3aedecefaeaabe6e`。

> 搞定以后，测试数据是否完整，MCP访问是否能够正常取出所有数据，并且数据和线上一致没有遗漏
> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

实际：真实原生合成表单完成签发/复制/一次显示/撤销；实际owner链路采用task05工程证据。
差缺：本条未确认实现差缺。
证据：browser-native.json；synthetic-results.json#/desk；C-tests.log

- Unconditional / Passed：输入 权限网页生成访问token；预期 权限网页生成访问token；实际 真实原生合成表单完成签发/复制/一次显示/撤销；实际owner链路采用task05工程证据。。证据 browser-native.json；synthetic-results.json#/desk；C-tests.log

### D06 · 已实现 · 只有本人下发token才可实际访问MCP

来源：T-INSIGHTS-DAILY-20261030-01 / `request_snapshot`；完整原文SHA256 `f136041515b0fc751dc801e3b229702bb338403f61eac1ac3aedecefaeaabe6e`。

> 搞定以后，测试数据是否完整，MCP访问是否能够正常取出所有数据，并且数据和线上一致没有遗漏
> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

实际：有效Bearer能查询，撤销旧令牌401，管理员会话和Bearer分离。
差缺：本条未确认实现差缺。
证据：C-tests.log；synthetic-results.json#/rate；live-results.json

- Met / Passed：输入 有效Bearer；预期 只读查询可达；实际 真实11工具成功。证据 live-results.json
- NotMet / Passed：输入 无效/已撤销Bearer；预期 401且无后端查询；实际 新合成同名重发旧token401，普通回归无凭据401。证据 synthetic-results.json；C-tests.log

### D07 · 已实现 · 部署3029；旧localhost被后续明确内网开放替代

来源：T-INSIGHTS-DAILY-20261030-01 / `request_snapshot`；完整原文SHA256 `f136041515b0fc751dc801e3b229702bb338403f61eac1ac3aedecefaeaabe6e`。

> 搞定以后，测试数据是否完整，MCP访问是否能够正常取出所有数据，并且数据和线上一致没有遗漏
> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

实际：3029指定192.168.10.20严格HTTPS；不是0.0.0.0；后续门户原话明确改为内网分享。
差缺：本条未确认实现差缺。
证据：start.json；firewall.json；live-results.json

- Met / Passed：输入 当前门户原话已要求内网开放；预期 保持3029并限定内网IP/网段/TLS；实际 监听/防火墙/真实TLS一致。证据 start.json；firewall.json；live-results.json
- NotMet / NotRun：输入 最初localhost阶段；预期 仅回环发放；实际 历史勘察原件记载旧3029仅回环；本轮不回滚到旧实现。证据 original-sources.json
- Exception / Passed：输入 最新明确内网分享指令；预期 使用新授权监听范围；实际 按当前入口验证，无新增匿名签发。证据 live-results.json

### D08 · 已实现 · 完整说明核对

来源：T-INSIGHTS-DAILY-20261030-01 / `request_snapshot`；完整原文SHA256 `f136041515b0fc751dc801e3b229702bb338403f61eac1ac3aedecefaeaabe6e`。

> MCP介绍完整吗

实际：11工具逐参数、14表、协议/来源/分页/AI计数/错误/TLS/客户端/发放权限均有当前说明。
差缺：本条未确认实现差缺。
证据：live-results.json；synthetic-results.json

- Unconditional / Passed：输入 完整说明核对；预期 完整说明核对；实际 11工具逐参数、14表、协议/来源/分页/AI计数/错误/TLS/客户端/发放权限均有当前说明。。证据 live-results.json；synthetic-results.json

### P01 · 已实现 · 其他人可以使用MCP

来源：T-INSIGHTS-MCP-PORTAL-20261030-01 / `request_snapshot`；完整原文SHA256 `e77269c0023755f364d6925428a499d342b101f0c06bc6f73ed97663879d0311`。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

实际：无凭据通用包、两类客户端与本人令牌流程齐全；异机环境限制单列。
差缺：本条未确认实现差缺。
证据：live-results.json；synthetic-results.json；browser-native.json；stdio-results.json

- Unconditional / Passed：输入 其他人可以使用MCP；预期 其他人可以使用MCP；实际 无凭据通用包、两类客户端与本人令牌流程齐全；异机环境限制单列。。证据 live-results.json；synthetic-results.json；browser-native.json；stdio-results.json

### P02 · 已实现 · MCP介绍详细

来源：T-INSIGHTS-MCP-PORTAL-20261030-01 / `request_snapshot`；完整原文SHA256 `e77269c0023755f364d6925428a499d342b101f0c06bc6f73ed97663879d0311`。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

实际：完整指南11工具所有参数直接与真实schema相等。
差缺：本条未确认实现差缺。
证据：live-results.json；synthetic-results.json；browser-native.json；stdio-results.json

- Unconditional / Passed：输入 MCP介绍详细；预期 MCP介绍详细；实际 完整指南11工具所有参数直接与真实schema相等。。证据 live-results.json；synthetic-results.json；browser-native.json；stdio-results.json

### P03 · 部分实现 · 按MCP本身协议制作文档或程序

来源：T-INSIGHTS-MCP-PORTAL-20261030-01 / `request_snapshot`；完整原文SHA256 `e77269c0023755f364d6925428a499d342b101f0c06bc6f73ed97663879d0311`。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

实际：HTTP正确；实际保留stdio CLI的数字和ID路径出现两项反例。
差缺：R8-001、R8-002未解决。
证据：live-results.json；synthetic-results.json；browser-native.json；stdio-results.json

- Unconditional / Failed：输入 按MCP本身协议制作文档或程序；预期 按MCP本身协议制作文档或程序；实际 HTTP正确；实际保留stdio CLI的数字和ID路径出现两项反例。。证据 live-results.json；synthetic-results.json；browser-native.json；stdio-results.json

### P04 · 已实现 · 给接收人材料并使其能够接入

来源：T-INSIGHTS-MCP-PORTAL-20261030-01 / `request_snapshot`；完整原文SHA256 `e77269c0023755f364d6925428a499d342b101f0c06bc6f73ed97663879d0311`。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

实际：23文件ZIP校验和/脚本一致；客户端完整分页和中途失败不输出伪完整。
差缺：本条未确认实现差缺。
证据：live-results.json；synthetic-results.json；browser-native.json；stdio-results.json

- Unconditional / Passed：输入 给接收人材料并使其能够接入；预期 给接收人材料并使其能够接入；实际 23文件ZIP校验和/脚本一致；客户端完整分页和中途失败不输出伪完整。。证据 live-results.json；synthetic-results.json；browser-native.json；stdio-results.json

### P05 · 已实现 · 优化并复核token生成服务

来源：T-INSIGHTS-MCP-PORTAL-20261030-01 / `request_snapshot`；完整原文SHA256 `e77269c0023755f364d6925428a499d342b101f0c06bc6f73ed97663879d0311`。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

实际：独立管理员、受限挑战/会话、一次显示、确认撤销、损坏恢复及原生移动交互已检查。
差缺：本条未确认实现差缺。
证据：live-results.json；synthetic-results.json；browser-native.json；stdio-results.json

- Unconditional / Passed：输入 优化并复核token生成服务；预期 优化并复核token生成服务；实际 独立管理员、受限挑战/会话、一次显示、确认撤销、损坏恢复及原生移动交互已检查。。证据 live-results.json；synthetic-results.json；browser-native.json；stdio-results.json

### P06 · 已实现 · 内网开放生成token服务入口

来源：T-INSIGHTS-MCP-PORTAL-20261030-01 / `request_snapshot`；完整原文SHA256 `e77269c0023755f364d6925428a499d342b101f0c06bc6f73ed97663879d0311`。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

实际：3029内网限定IP，真实TLS、Host/Origin保护和防火墙规则一致。
差缺：本条未确认实现差缺。
证据：live-results.json；synthetic-results.json；browser-native.json；stdio-results.json

- Unconditional / Passed：输入 内网开放生成token服务入口；预期 内网开放生成token服务入口；实际 3029内网限定IP，真实TLS、Host/Origin保护和防火墙规则一致。。证据 live-results.json；synthetic-results.json；browser-native.json；stdio-results.json

### P07 · 已实现 · 将协议/介绍/方法放到生成token服务上

来源：T-INSIGHTS-MCP-PORTAL-20261030-01 / `request_snapshot`；完整原文SHA256 `e77269c0023755f364d6925428a499d342b101f0c06bc6f73ed97663879d0311`。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

实际：/guide和七个下载真实200，全部与冻结文件一致。
差缺：本条未确认实现差缺。
证据：live-results.json；synthetic-results.json；browser-native.json；stdio-results.json

- Unconditional / Passed：输入 将协议/介绍/方法放到生成token服务上；预期 将协议/介绍/方法放到生成token服务上；实际 /guide和七个下载真实200，全部与冻结文件一致。。证据 live-results.json；synthetic-results.json；browser-native.json；stdio-results.json

### P08 · 已实现 · 仅需分享整个服务内网链接

来源：T-INSIGHTS-MCP-PORTAL-20261030-01 / `request_snapshot`；完整原文SHA256 `e77269c0023755f364d6925428a499d342b101f0c06bc6f73ed97663879d0311`。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

实际：接入中心包含指南、工具参考、下载和管理员入口；链接不等于数据权限。
差缺：本条未确认实现差缺。
证据：live-results.json；synthetic-results.json；browser-native.json；stdio-results.json

- Unconditional / Passed：输入 仅需分享整个服务内网链接；预期 仅需分享整个服务内网链接；实际 接入中心包含指南、工具参考、下载和管理员入口；链接不等于数据权限。。证据 live-results.json；synthetic-results.json；browser-native.json；stdio-results.json

### P09 · 已实现 · MCP独立会话处理；本会话继续日报，不侵入3030

来源：T-INSIGHTS-MCP-PORTAL-20261030-01 / `request_snapshot`；完整原文SHA256 `e77269c0023755f364d6925428a499d342b101f0c06bc6f73ed97663879d0311`。

> 开一个新会话处理MCP相关事宜，本会话继续完成客诉日报看板

实际：原日报澄清明确MCP已由新会话处理；本轮仅MCP审查和round8留证，保护PID不变。
差缺：本条未确认实现差缺。
证据：original-sources.json；start.json；end.json

- Unconditional / Passed：输入 MCP独立会话处理；本会话继续日报，不侵入3030；预期 MCP独立会话处理；本会话继续日报，不侵入3030；实际 原日报澄清明确MCP已由新会话处理；本轮仅MCP审查和round8留证，保护PID不变。。证据 original-sources.json；start.json；end.json

### P10 · 已实现 · 继续既有范围

来源：T-INSIGHTS-MCP-PORTAL-20261030-01 / `request_snapshot`；完整原文SHA256 `e77269c0023755f364d6925428a499d342b101f0c06bc6f73ed97663879d0311`。

> 继续

实际：没有新增管理员、生产读取、数据库连接或正式批准。
差缺：本条未确认实现差缺。
证据：original-sources.json；runtime-boundaries.json

- Unconditional / Passed：输入 继续既有范围；预期 继续既有范围；实际 没有新增管理员、生产读取、数据库连接或正式批准。。证据 original-sources.json；runtime-boundaries.json

### P11 · 已实现 · “继续”沿用本人发放的单管理员边界

来源：T-INSIGHTS-MCP-PORTAL-20261030-01 / `clarification:r1.e1`；完整原文SHA256 `7c9691192f1b73408bbe4c0cb6d00db94375ca9d8fce0a0d5985e7a5178f083f`。

> 继续

实际：真实答复只有继续；按既有“我下发”执行，不伪造选择多管理员。访客公开只读，独立管理员才能发放/撤销。
差缺：本条未确认实现差缺。
证据：original-sources.json；synthetic-results.json#/desk；C-tests.log

- Met / Passed：输入 有效管理员/Origin/CSRF；预期 可发放/确认撤销；实际 新原生浏览器和ASGI均成功。证据 browser-native.json；synthetic-results.json
- NotMet / Passed：输入 匿名/Bearer替代会话/Origin缺失或null/CSRF错误；预期 401或403且授权文件不变；实际 49测试及新合成均拒绝。证据 C-tests.log；synthetic-results.json

### R1-01 · 部分实现 · 把管理员账号和密码给本人

来源：T-INSIGHTS-MCP-REPAIR-20261030-01 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

实际：账号owner已有受限配置；父执行者可信上下文说明曾私聊交付随机初始口令且未重置。
差缺：本轮无原始私聊凭据消息可回读；没有再次读取/输出口令，不能冒称本轮重新交付验证。
证据：original-sources.json；governance-observed.json

- Unconditional / NotRun：输入 把管理员账号和密码给本人；预期 把管理员账号和密码给本人；实际 账号owner已有受限配置；父执行者可信上下文说明曾私聊交付随机初始口令且未重置。。证据 original-sources.json；governance-observed.json

### R1-02 · 已实现 · 提供登录入口

来源：T-INSIGHTS-MCP-REPAIR-20261030-01 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

实际：https://192.168.10.20:3029/admin/login可达，匿名admin重定向登录。
差缺：本条未确认实现差缺。
证据：live-results.json#/groups/portal；browser-native.json

- Unconditional / Passed：输入 提供登录入口；预期 提供登录入口；实际 https://192.168.10.20:3029/admin/login可达，匿名admin重定向登录。。证据 live-results.json#/groups/portal；browser-native.json

### R1-03 · 已实现 · 登录该账号即可生成token

来源：T-INSIGHTS-MCP-REPAIR-20261030-01 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

实际：原生表单签发一次显示、复制、同名拒绝、撤销、退出均正常；真实owner完整链路为task05工程证据。
差缺：本条未确认实现差缺。
证据：browser-native.json；synthetic-results.json#/desk；C-tests.log

- Met / Passed：输入 正确登录后提交合法64字符新身份；预期 生成并只显示一次；实际 原生POST200；GET重载无token；复制相同。证据 browser-native.json
- NotMet / Passed：输入 匿名、错误口令、CSRF/Origin无效、同名身份；预期 拒绝且不签发替代令牌；实际 匿名401；错误口令401；CSRF/Origin403；同名400。证据 C-tests.log；synthetic-results.json；browser-native.json

### R1-04 · 已实现 · 明确开始多轮审查

来源：T-INSIGHTS-MCP-REPAIR-20261030-01 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 开始审查

实际：本轮按真实开始/重启授权技术审查；机器Offer拒绝不被隐去。
差缺：本条未确认实现差缺。
证据：original-sources.json；stdio-results.json；governance-observed.json

- Unconditional / Passed：输入 明确开始多轮审查；预期 明确开始多轮审查；实际 本轮按真实开始/重启授权技术审查；机器Offer拒绝不被隐去。。证据 original-sources.json；stdio-results.json；governance-observed.json

### R1-05 · 部分实现 · 发现问题须修复并复验，直到同版连续两轮完整无问题

来源：T-INSIGHTS-MCP-REPAIR-20261030-01 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。

实际：本轮发现2项新问题，已完整留证并交父执行者后续返修；本轮只读，不修改产品。
差缺：R8-001/R8-002待返修；未来同版第二轮尚未发生，不得编造Met或审查通过。
证据：stdio-results.json；synthetic-results.json；governance-observed.json

- Met / NotRun：输入 未来同版两轮完整无问题；预期 才可结束并由官方机制判定；实际 NotRun：本轮发现问题，未达前提。证据 governance-observed.json
- NotMet / Passed：输入 当前发现R8-001/R8-002；预期 不得声称审查通过；先返修复验；实际 报告非干净，正式记录不修改。证据 stdio-results.json；governance-observed.json

### R1-06 · 已实现 · 审查选择不影响现有登录与生成令牌

来源：T-INSIGHTS-MCP-REPAIR-20261030-01 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。

实际：审查未停服务、未重置真实管理员或变更真实授权文件；本轮合成表单可用。
差缺：本条未确认实现差缺。
证据：start.json；end.json；browser-native.json

- Unconditional / Passed：输入 审查选择不影响现有登录与生成令牌；预期 审查选择不影响现有登录与生成令牌；实际 审查未停服务、未重置真实管理员或变更真实授权文件；本轮合成表单可用。。证据 start.json；end.json；browser-native.json

### R2-01 · 部分实现 · 把管理员账号和密码给本人

来源：T-INSIGHTS-MCP-REPAIR-20261030-02 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

实际：账号owner已有受限配置；父执行者可信上下文说明曾私聊交付随机初始口令且未重置。
差缺：本轮无原始私聊凭据消息可回读；没有再次读取/输出口令，不能冒称本轮重新交付验证。
证据：original-sources.json；governance-observed.json

- Unconditional / NotRun：输入 把管理员账号和密码给本人；预期 把管理员账号和密码给本人；实际 账号owner已有受限配置；父执行者可信上下文说明曾私聊交付随机初始口令且未重置。。证据 original-sources.json；governance-observed.json

### R2-02 · 已实现 · 提供登录入口

来源：T-INSIGHTS-MCP-REPAIR-20261030-02 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

实际：https://192.168.10.20:3029/admin/login可达，匿名admin重定向登录。
差缺：本条未确认实现差缺。
证据：live-results.json#/groups/portal；browser-native.json

- Unconditional / Passed：输入 提供登录入口；预期 提供登录入口；实际 https://192.168.10.20:3029/admin/login可达，匿名admin重定向登录。。证据 live-results.json#/groups/portal；browser-native.json

### R2-03 · 已实现 · 登录该账号即可生成token

来源：T-INSIGHTS-MCP-REPAIR-20261030-02 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

实际：原生表单签发一次显示、复制、同名拒绝、撤销、退出均正常；真实owner完整链路为task05工程证据。
差缺：本条未确认实现差缺。
证据：browser-native.json；synthetic-results.json#/desk；C-tests.log

- Met / Passed：输入 正确登录后提交合法64字符新身份；预期 生成并只显示一次；实际 原生POST200；GET重载无token；复制相同。证据 browser-native.json
- NotMet / Passed：输入 匿名、错误口令、CSRF/Origin无效、同名身份；预期 拒绝且不签发替代令牌；实际 匿名401；错误口令401；CSRF/Origin403；同名400。证据 C-tests.log；synthetic-results.json；browser-native.json

### R2-04 · 已实现 · 明确开始多轮审查

来源：T-INSIGHTS-MCP-REPAIR-20261030-02 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 开始审查

实际：本轮按真实开始/重启授权技术审查；机器Offer拒绝不被隐去。
差缺：本条未确认实现差缺。
证据：original-sources.json；stdio-results.json；governance-observed.json

- Unconditional / Passed：输入 明确开始多轮审查；预期 明确开始多轮审查；实际 本轮按真实开始/重启授权技术审查；机器Offer拒绝不被隐去。。证据 original-sources.json；stdio-results.json；governance-observed.json

### R2-05 · 部分实现 · 发现问题须修复并复验，直到同版连续两轮完整无问题

来源：T-INSIGHTS-MCP-REPAIR-20261030-02 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。

实际：本轮发现2项新问题，已完整留证并交父执行者后续返修；本轮只读，不修改产品。
差缺：R8-001/R8-002待返修；未来同版第二轮尚未发生，不得编造Met或审查通过。
证据：stdio-results.json；synthetic-results.json；governance-observed.json

- Met / NotRun：输入 未来同版两轮完整无问题；预期 才可结束并由官方机制判定；实际 NotRun：本轮发现问题，未达前提。证据 governance-observed.json
- NotMet / Passed：输入 当前发现R8-001/R8-002；预期 不得声称审查通过；先返修复验；实际 报告非干净，正式记录不修改。证据 stdio-results.json；governance-observed.json

### R2-06 · 已实现 · 审查选择不影响现有登录与生成令牌

来源：T-INSIGHTS-MCP-REPAIR-20261030-02 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。

实际：审查未停服务、未重置真实管理员或变更真实授权文件；本轮合成表单可用。
差缺：本条未确认实现差缺。
证据：start.json；end.json；browser-native.json

- Unconditional / Passed：输入 审查选择不影响现有登录与生成令牌；预期 审查选择不影响现有登录与生成令牌；实际 审查未停服务、未重置真实管理员或变更真实授权文件；本轮合成表单可用。。证据 start.json；end.json；browser-native.json

### R3-01 · 部分实现 · 把管理员账号和密码给本人

来源：T-INSIGHTS-MCP-REPAIR-20261030-03 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

实际：账号owner已有受限配置；父执行者可信上下文说明曾私聊交付随机初始口令且未重置。
差缺：本轮无原始私聊凭据消息可回读；没有再次读取/输出口令，不能冒称本轮重新交付验证。
证据：original-sources.json；governance-observed.json

- Unconditional / NotRun：输入 把管理员账号和密码给本人；预期 把管理员账号和密码给本人；实际 账号owner已有受限配置；父执行者可信上下文说明曾私聊交付随机初始口令且未重置。。证据 original-sources.json；governance-observed.json

### R3-02 · 已实现 · 提供登录入口

来源：T-INSIGHTS-MCP-REPAIR-20261030-03 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

实际：https://192.168.10.20:3029/admin/login可达，匿名admin重定向登录。
差缺：本条未确认实现差缺。
证据：live-results.json#/groups/portal；browser-native.json

- Unconditional / Passed：输入 提供登录入口；预期 提供登录入口；实际 https://192.168.10.20:3029/admin/login可达，匿名admin重定向登录。。证据 live-results.json#/groups/portal；browser-native.json

### R3-03 · 已实现 · 登录该账号即可生成token

来源：T-INSIGHTS-MCP-REPAIR-20261030-03 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

实际：原生表单签发一次显示、复制、同名拒绝、撤销、退出均正常；真实owner完整链路为task05工程证据。
差缺：本条未确认实现差缺。
证据：browser-native.json；synthetic-results.json#/desk；C-tests.log

- Met / Passed：输入 正确登录后提交合法64字符新身份；预期 生成并只显示一次；实际 原生POST200；GET重载无token；复制相同。证据 browser-native.json
- NotMet / Passed：输入 匿名、错误口令、CSRF/Origin无效、同名身份；预期 拒绝且不签发替代令牌；实际 匿名401；错误口令401；CSRF/Origin403；同名400。证据 C-tests.log；synthetic-results.json；browser-native.json

### R3-04 · 已实现 · 明确开始多轮审查

来源：T-INSIGHTS-MCP-REPAIR-20261030-03 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 开始审查

实际：本轮按真实开始/重启授权技术审查；机器Offer拒绝不被隐去。
差缺：本条未确认实现差缺。
证据：original-sources.json；stdio-results.json；governance-observed.json

- Unconditional / Passed：输入 明确开始多轮审查；预期 明确开始多轮审查；实际 本轮按真实开始/重启授权技术审查；机器Offer拒绝不被隐去。。证据 original-sources.json；stdio-results.json；governance-observed.json

### R3-05 · 部分实现 · 发现问题须修复并复验，直到同版连续两轮完整无问题

来源：T-INSIGHTS-MCP-REPAIR-20261030-03 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。

实际：本轮发现2项新问题，已完整留证并交父执行者后续返修；本轮只读，不修改产品。
差缺：R8-001/R8-002待返修；未来同版第二轮尚未发生，不得编造Met或审查通过。
证据：stdio-results.json；synthetic-results.json；governance-observed.json

- Met / NotRun：输入 未来同版两轮完整无问题；预期 才可结束并由官方机制判定；实际 NotRun：本轮发现问题，未达前提。证据 governance-observed.json
- NotMet / Passed：输入 当前发现R8-001/R8-002；预期 不得声称审查通过；先返修复验；实际 报告非干净，正式记录不修改。证据 stdio-results.json；governance-observed.json

### R3-06 · 已实现 · 审查选择不影响现有登录与生成令牌

来源：T-INSIGHTS-MCP-REPAIR-20261030-03 / `request_snapshot`；完整原文SHA256 `905df7fe8d6b4cac30c4102bd72cdf1d7920ad58cddbead47bf4e9414c4b2065`。

> 工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。

实际：审查未停服务、未重置真实管理员或变更真实授权文件；本轮合成表单可用。
差缺：本条未确认实现差缺。
证据：start.json；end.json；browser-native.json

- Unconditional / Passed：输入 审查选择不影响现有登录与生成令牌；预期 审查选择不影响现有登录与生成令牌；实际 审查未停服务、未重置真实管理员或变更真实授权文件；本轮合成表单可用。。证据 start.json；end.json；browser-native.json

### R4-01 · 部分实现 · 把管理员账号和密码给本人

来源：T-INSIGHTS-MCP-REPAIR-20261030-04 / `request_snapshot`；完整原文SHA256 `8c2024f1424a393b9810055e65e2575dde74d98ba1f0c771f52fd890dd339d38`。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

实际：账号owner已有受限配置；父执行者可信上下文说明曾私聊交付随机初始口令且未重置。
差缺：本轮无原始私聊凭据消息可回读；没有再次读取/输出口令，不能冒称本轮重新交付验证。
证据：original-sources.json；governance-observed.json

- Unconditional / NotRun：输入 把管理员账号和密码给本人；预期 把管理员账号和密码给本人；实际 账号owner已有受限配置；父执行者可信上下文说明曾私聊交付随机初始口令且未重置。。证据 original-sources.json；governance-observed.json

### R4-02 · 已实现 · 提供登录入口

来源：T-INSIGHTS-MCP-REPAIR-20261030-04 / `request_snapshot`；完整原文SHA256 `8c2024f1424a393b9810055e65e2575dde74d98ba1f0c771f52fd890dd339d38`。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

实际：https://192.168.10.20:3029/admin/login可达，匿名admin重定向登录。
差缺：本条未确认实现差缺。
证据：live-results.json#/groups/portal；browser-native.json

- Unconditional / Passed：输入 提供登录入口；预期 提供登录入口；实际 https://192.168.10.20:3029/admin/login可达，匿名admin重定向登录。。证据 live-results.json#/groups/portal；browser-native.json

### R4-03 · 已实现 · 登录该账号即可生成token

来源：T-INSIGHTS-MCP-REPAIR-20261030-04 / `request_snapshot`；完整原文SHA256 `8c2024f1424a393b9810055e65e2575dde74d98ba1f0c771f52fd890dd339d38`。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

实际：原生表单签发一次显示、复制、同名拒绝、撤销、退出均正常；真实owner完整链路为task05工程证据。
差缺：本条未确认实现差缺。
证据：browser-native.json；synthetic-results.json#/desk；C-tests.log

- Met / Passed：输入 正确登录后提交合法64字符新身份；预期 生成并只显示一次；实际 原生POST200；GET重载无token；复制相同。证据 browser-native.json
- NotMet / Passed：输入 匿名、错误口令、CSRF/Origin无效、同名身份；预期 拒绝且不签发替代令牌；实际 匿名401；错误口令401；CSRF/Origin403；同名400。证据 C-tests.log；synthetic-results.json；browser-native.json

### R4-04 · 已实现 · 明确开始多轮审查

来源：T-INSIGHTS-MCP-REPAIR-20261030-04 / `request_snapshot`；完整原文SHA256 `8c2024f1424a393b9810055e65e2575dde74d98ba1f0c771f52fd890dd339d38`。

> 开始审查

实际：本轮按真实开始/重启授权技术审查；机器Offer拒绝不被隐去。
差缺：本条未确认实现差缺。
证据：original-sources.json；stdio-results.json；governance-observed.json

- Unconditional / Passed：输入 明确开始多轮审查；预期 明确开始多轮审查；实际 本轮按真实开始/重启授权技术审查；机器Offer拒绝不被隐去。。证据 original-sources.json；stdio-results.json；governance-observed.json

### R4-05 · 部分实现 · 发现问题须修复并复验，直到同版连续两轮完整无问题

来源：T-INSIGHTS-MCP-REPAIR-20261030-04 / `request_snapshot`；完整原文SHA256 `8c2024f1424a393b9810055e65e2575dde74d98ba1f0c771f52fd890dd339d38`。

> 工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。

实际：本轮发现2项新问题，已完整留证并交父执行者后续返修；本轮只读，不修改产品。
差缺：R8-001/R8-002待返修；未来同版第二轮尚未发生，不得编造Met或审查通过。
证据：stdio-results.json；synthetic-results.json；governance-observed.json

- Met / NotRun：输入 未来同版两轮完整无问题；预期 才可结束并由官方机制判定；实际 NotRun：本轮发现问题，未达前提。证据 governance-observed.json
- NotMet / Passed：输入 当前发现R8-001/R8-002；预期 不得声称审查通过；先返修复验；实际 报告非干净，正式记录不修改。证据 stdio-results.json；governance-observed.json

### R4-06 · 已实现 · 审查选择不影响现有登录与生成令牌

来源：T-INSIGHTS-MCP-REPAIR-20261030-04 / `request_snapshot`；完整原文SHA256 `8c2024f1424a393b9810055e65e2575dde74d98ba1f0c771f52fd890dd339d38`。

> 工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。

实际：审查未停服务、未重置真实管理员或变更真实授权文件；本轮合成表单可用。
差缺：本条未确认实现差缺。
证据：start.json；end.json；browser-native.json

- Unconditional / Passed：输入 审查选择不影响现有登录与生成令牌；预期 审查选择不影响现有登录与生成令牌；实际 审查未停服务、未重置真实管理员或变更真实授权文件；本轮合成表单可用。。证据 start.json；end.json；browser-native.json

### R4-07 · 已实现 · 拉取最新代码并重启审查

来源：T-INSIGHTS-MCP-REPAIR-20261030-04 / `request_snapshot`；完整原文SHA256 `8c2024f1424a393b9810055e65e2575dde74d98ba1f0c771f52fd890dd339d38`。

> 拉取最新代码并重启审查

实际：上游main为7b63ad65；当前88ef76cc为拉取后连续返修交付。新上下文独立完整审查；冻结中不fetch/改产品。
差缺：本条未确认实现差缺。
证据：git-remote.json；start.json；end.json

- Unconditional / Passed：输入 拉取最新代码并重启审查；预期 拉取最新代码并重启审查；实际 上游main为7b63ad65；当前88ef76cc为拉取后连续返修交付。新上下文独立完整审查；冻结中不fetch/改产品。。证据 git-remote.json；start.json；end.json

### R5-01 · 部分实现 · 把管理员账号和密码给本人

来源：T-INSIGHTS-MCP-REPAIR-20261030-05 / `request_snapshot`；完整原文SHA256 `8c2024f1424a393b9810055e65e2575dde74d98ba1f0c771f52fd890dd339d38`。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

实际：账号owner已有受限配置；父执行者可信上下文说明曾私聊交付随机初始口令且未重置。
差缺：本轮无原始私聊凭据消息可回读；没有再次读取/输出口令，不能冒称本轮重新交付验证。
证据：original-sources.json；governance-observed.json

- Unconditional / NotRun：输入 把管理员账号和密码给本人；预期 把管理员账号和密码给本人；实际 账号owner已有受限配置；父执行者可信上下文说明曾私聊交付随机初始口令且未重置。。证据 original-sources.json；governance-observed.json

### R5-02 · 已实现 · 提供登录入口

来源：T-INSIGHTS-MCP-REPAIR-20261030-05 / `request_snapshot`；完整原文SHA256 `8c2024f1424a393b9810055e65e2575dde74d98ba1f0c771f52fd890dd339d38`。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

实际：https://192.168.10.20:3029/admin/login可达，匿名admin重定向登录。
差缺：本条未确认实现差缺。
证据：live-results.json#/groups/portal；browser-native.json

- Unconditional / Passed：输入 提供登录入口；预期 提供登录入口；实际 https://192.168.10.20:3029/admin/login可达，匿名admin重定向登录。。证据 live-results.json#/groups/portal；browser-native.json

### R5-03 · 已实现 · 登录该账号即可生成token

来源：T-INSIGHTS-MCP-REPAIR-20261030-05 / `request_snapshot`；完整原文SHA256 `8c2024f1424a393b9810055e65e2575dde74d98ba1f0c771f52fd890dd339d38`。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

实际：原生表单签发一次显示、复制、同名拒绝、撤销、退出均正常；真实owner完整链路为task05工程证据。
差缺：本条未确认实现差缺。
证据：browser-native.json；synthetic-results.json#/desk；C-tests.log

- Met / Passed：输入 正确登录后提交合法64字符新身份；预期 生成并只显示一次；实际 原生POST200；GET重载无token；复制相同。证据 browser-native.json
- NotMet / Passed：输入 匿名、错误口令、CSRF/Origin无效、同名身份；预期 拒绝且不签发替代令牌；实际 匿名401；错误口令401；CSRF/Origin403；同名400。证据 C-tests.log；synthetic-results.json；browser-native.json

### R5-04 · 已实现 · 明确开始多轮审查

来源：T-INSIGHTS-MCP-REPAIR-20261030-05 / `request_snapshot`；完整原文SHA256 `8c2024f1424a393b9810055e65e2575dde74d98ba1f0c771f52fd890dd339d38`。

> 开始审查

实际：本轮按真实开始/重启授权技术审查；机器Offer拒绝不被隐去。
差缺：本条未确认实现差缺。
证据：original-sources.json；stdio-results.json；governance-observed.json

- Unconditional / Passed：输入 明确开始多轮审查；预期 明确开始多轮审查；实际 本轮按真实开始/重启授权技术审查；机器Offer拒绝不被隐去。。证据 original-sources.json；stdio-results.json；governance-observed.json

### R5-05 · 部分实现 · 发现问题须修复并复验，直到同版连续两轮完整无问题

来源：T-INSIGHTS-MCP-REPAIR-20261030-05 / `request_snapshot`；完整原文SHA256 `8c2024f1424a393b9810055e65e2575dde74d98ba1f0c771f52fd890dd339d38`。

> 工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。

实际：本轮发现2项新问题，已完整留证并交父执行者后续返修；本轮只读，不修改产品。
差缺：R8-001/R8-002待返修；未来同版第二轮尚未发生，不得编造Met或审查通过。
证据：stdio-results.json；synthetic-results.json；governance-observed.json

- Met / NotRun：输入 未来同版两轮完整无问题；预期 才可结束并由官方机制判定；实际 NotRun：本轮发现问题，未达前提。证据 governance-observed.json
- NotMet / Passed：输入 当前发现R8-001/R8-002；预期 不得声称审查通过；先返修复验；实际 报告非干净，正式记录不修改。证据 stdio-results.json；governance-observed.json

### R5-06 · 已实现 · 审查选择不影响现有登录与生成令牌

来源：T-INSIGHTS-MCP-REPAIR-20261030-05 / `request_snapshot`；完整原文SHA256 `8c2024f1424a393b9810055e65e2575dde74d98ba1f0c771f52fd890dd339d38`。

> 工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。

实际：审查未停服务、未重置真实管理员或变更真实授权文件；本轮合成表单可用。
差缺：本条未确认实现差缺。
证据：start.json；end.json；browser-native.json

- Unconditional / Passed：输入 审查选择不影响现有登录与生成令牌；预期 审查选择不影响现有登录与生成令牌；实际 审查未停服务、未重置真实管理员或变更真实授权文件；本轮合成表单可用。。证据 start.json；end.json；browser-native.json

### R5-07 · 已实现 · 拉取最新代码并重启审查

来源：T-INSIGHTS-MCP-REPAIR-20261030-05 / `request_snapshot`；完整原文SHA256 `8c2024f1424a393b9810055e65e2575dde74d98ba1f0c771f52fd890dd339d38`。

> 拉取最新代码并重启审查

实际：上游main为7b63ad65；当前88ef76cc为拉取后连续返修交付。新上下文独立完整审查；冻结中不fetch/改产品。
差缺：本条未确认实现差缺。
证据：git-remote.json；start.json；end.json

- Unconditional / Passed：输入 拉取最新代码并重启审查；预期 拉取最新代码并重启审查；实际 上游main为7b63ad65；当前88ef76cc为拉取后连续返修交付。新上下文独立完整审查；冻结中不fetch/改产品。。证据 git-remote.json；start.json；end.json

### D09 · 部分实现 · MCP门户与独立分工的原始指令

来源：T-INSIGHTS-DAILY-20261030-01 / `request_snapshot`；完整原文SHA256 `f136041515b0fc751dc801e3b229702bb338403f61eac1ac3aedecefaeaabe6e`。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

实际：与门户后续原话分别绑定；门户/说明/发放已检查，stdio协议缺陷保留。
差缺：R8-001/R8-002
证据：original-sources.json；live-results.json；stdio-results.json；start.json；end.json

- Unconditional / NotRun：输入 MCP门户与独立分工的原始指令；预期 MCP门户与独立分工的原始指令；实际 与门户后续原话分别绑定；门户/说明/发放已检查，stdio协议缺陷保留。。证据 original-sources.json；live-results.json；stdio-results.json；start.json；end.json

### D10 · 已实现 · MCP门户与独立分工的原始指令

来源：T-INSIGHTS-DAILY-20261030-01 / `request_snapshot`；完整原文SHA256 `f136041515b0fc751dc801e3b229702bb338403f61eac1ac3aedecefaeaabe6e`。

> 开一个新会话处理MCP相关事宜，本会话继续完成客诉日报看板

实际：与门户后续原话分别绑定；门户/说明/发放已检查，stdio协议缺陷保留。
差缺：本条未确认实现差缺。
证据：original-sources.json；live-results.json；stdio-results.json；start.json；end.json

- Unconditional / Passed：输入 MCP门户与独立分工的原始指令；预期 MCP门户与独立分工的原始指令；实际 与门户后续原话分别绑定；门户/说明/发放已检查，stdio协议缺陷保留。。证据 original-sources.json；live-results.json；stdio-results.json；start.json；end.json

### D11 · 已实现 · 日报范围继续；MCP由新会话处理的真实澄清

来源：T-INSIGHTS-DAILY-20261030-01 / `clarification:r1.e1`；完整原文SHA256 `6d9a497fa5f35f107ccf890a0dce28831417318aa89e12f74d17bb1cc42de0d8`。

> 按此范围继续（推荐）

实际：原问题明确MCP独立分工；本轮未改日报或AICS。
差缺：本条未确认实现差缺。
证据：original-sources.json；start.json；end.json

- Unconditional / Passed：输入 日报范围继续；MCP由新会话处理的真实澄清；预期 日报范围继续；MCP由新会话处理的真实澄清；实际 原问题明确MCP独立分工；本轮未改日报或AICS。。证据 original-sources.json；start.json；end.json

## 未实现与部分实现分列

未实现：本轮未确认完全缺失的产品功能；已实现部分中的确认缺陷见R8-001/R8-002。

|条目|类型|差缺|
|---|---|---|
|F02|ConditionalExternal|本轮禁止连接源库；不能把准备配置等同已完成生产连接验收。|
|F04|Product|stdio数字原值和整数ID处理有缺陷。|
|F07|ExternalAcceptance|已实现远程服务能力；接收方机器的路由、CA安装、本人配置仍须在该机器验收。|
|H03|Product|R8-001/R8-002|
|H07|ConditionalExternal|生产连通后的实际切换/当前线上一致性未执行；没有当前生产权限。|
|D04|ExternalEvidenceLimit|禁止生产连接，不能把MCP/API同副本一致当作当前线上一致。|
|P03|Product|R8-001、R8-002未解决。|
|R1-01|HistoricalEvidenceLimit|本轮无原始私聊凭据消息可回读；没有再次读取/输出口令，不能冒称本轮重新交付验证。|
|R1-05|ReviewProcess|R8-001/R8-002待返修；未来同版第二轮尚未发生，不得编造Met或审查通过。|
|R2-01|HistoricalEvidenceLimit|本轮无原始私聊凭据消息可回读；没有再次读取/输出口令，不能冒称本轮重新交付验证。|
|R2-05|ReviewProcess|R8-001/R8-002待返修；未来同版第二轮尚未发生，不得编造Met或审查通过。|
|R3-01|HistoricalEvidenceLimit|本轮无原始私聊凭据消息可回读；没有再次读取/输出口令，不能冒称本轮重新交付验证。|
|R3-05|ReviewProcess|R8-001/R8-002待返修；未来同版第二轮尚未发生，不得编造Met或审查通过。|
|R4-01|HistoricalEvidenceLimit|本轮无原始私聊凭据消息可回读；没有再次读取/输出口令，不能冒称本轮重新交付验证。|
|R4-05|ReviewProcess|R8-001/R8-002待返修；未来同版第二轮尚未发生，不得编造Met或审查通过。|
|R5-01|HistoricalEvidenceLimit|本轮无原始私聊凭据消息可回读；没有再次读取/输出口令，不能冒称本轮重新交付验证。|
|R5-05|ReviewProcess|R8-001/R8-002待返修；未来同版第二轮尚未发生，不得编造Met或审查通过。|
|D09|Scope|R8-001/R8-002|

## 历史发现在本版的独立处置核对

原R1/R2/R3/R5问题原件已读取，R7三个确认项与修复记录已读。以下Fixed仅绑定原问题的明确复现路径及本冻结版本；不会据此断言相同主题在stdio等另一传输上也无缺陷。R3-04/R7-003的复发事实保留。

|ID|本版处置|本轮理由/证据|
|---|---|---|
|R1-01|Fixed|挑战刷新复用、每peer限额与过期恢复；当前49测试重新通过。 证据：C-tests.log；D-tests.log|
|R1-02|Fixed|新ASGI损坏元数据仍提供撤销并保留原损坏文件。 证据：synthetic-results.json#/desk|
|R1-03|Fixed|原HTTP错误类型/额外参数路径已修，187非法输入后端零调用；stdio新精度问题另列R8-001。 证据：synthetic-results.json#/parameters；C-tests.log|
|R1-04|Fixed|未知工具顶层-32602/id保留，49回归重新通过。 证据：C-tests.log；D-tests.log|
|R2-01|Fixed|NativeJSONArguments保持字符串原值；完整有效参数包含null/[]/{}/引号，49逐字保持测试重跑。 证据：synthetic-results.json#/parameters；C-tests.log|
|R2-02|Fixed|真实Windows Users可读合成父目录下首字节前已移除继承；写入/flush/ACL失败清理49测试通过。 证据：synthetic-results.json#/clients；C-tests.log|
|R2-03|Fixed|原HTTP非法信封-32600、解析-32700、方法/参数错误分层均49项覆盖；不误报stdio新ID问题已被该HTTP修复覆盖。 证据：C-tests.log；D-tests.log|
|R3-01|Fixed|单快照凭据/版本绑定、轮换会话失效当前49测试通过。 证据：C-tests.log；D-tests.log|
|R3-02|Fixed|原HTTP请求ID路径已修；新HTTP整数表示/非法fraction/bool对照通过。stdio同类路径仍在R8-002单独登记。 证据：synthetic-results.json#/parameters/request_id_http_counterparts；C-tests.log|
|R3-03|Fixed|全部五工具显式空cursor先拒绝；五工具同筛选允许/变筛选422/版本409/来源422新对照通过。 证据：C-tests.log；readmodel-results.json|
|R3-04|Fixed|曾在R7复发，当前operator-handoff确指task05/report和results；03/04明确历史。当前报告内容49测试/17组与实际相符。 证据：documentation-observed.json；C-tests.log；live-results.json|
|R5-001|Fixed|同peer成功/失败KDF竞态测试本版C/D均通过，失败返回401。 证据：C-tests.log；D-tests.log|
|R5-002|Fixed|原HTTP高精度fraction反例拒绝，1.0允许；本轮同值真HTTPS控制再次成立；stdio新路径另列R8-001。 证据：live-results.json#/groups/raw_number_precision；C-tests.log|
|R5-003|Fixed|首页mcp-client.json示例可被JSON解析，C/D49重跑通过。 证据：C-tests.log；D-tests.log|
|R5-004|Fixed|新原生浏览器无策略覆写完成签发/撤销/退出，same-origin保留；新ASGI缺失/null/外源Origin均拒绝。 证据：browser-native.json；synthetic-results.json#/desk|
|R5-005|Fixed|360px真实DOM长身份不撑宽；表格在311px容器内横向滚动，撤销可操作。 证据：browser-native.json|
|R7-001|Fixed|新长身份签发/同名错误/撤销alert均311=311，document/body345=345。 证据：browser-native.json；mobile-duplicate.png；mobile-revoked.png|
|R7-002|Fixed|低配额假时钟跨工具、隔离身份、重发保留、窗口恢复与24并发仅5后端；实际guide6000/60。 证据：synthetic-results.json#/rate；live-results.json#/groups/guide_resource|
|R7-003|Fixed|当前交接链接task05，旧03/04为历史，与R3-04复发关系保留。 证据：documentation-observed.json|

## 真实限制、正式状态与失败留存

- 另一台内网电脑的路由、CA安装、本人客户端未实测；本机真实IP/TLS不能替代。
- 历史私聊随机owner口令交付无原始消息可重新读取；不重复交付或输出秘密，不称本轮重验。
- 线上实时完整性没有重验；版本24/DEGRADED为历史副本，生产连接禁止。
- 当前independent-review/security-privacy-review与用户决定Pending；历史其他对象Gate回答不转移到当前版本。
- 原父Deferred使官方Offer登记拒绝；本轮仅留真实技术审查证据，不改旧阶段，不伪造ManagedByParent或官方Passed。
- 本轮2项问题未修复，未来同版第二轮前提未成立；该未来会话条件不是本轮产品领域漏查。
- 真实owner签发/使用/撤销链路引用本冻结task05的17组工程结果；本轮独立使用合成管理员和原生浏览器，不运行会签发真实token的verify脚本。
- 首次C/D回归漏设TEMP/TMP，既有测试的默认TemporaryDirectory写入系统TEMP合成临时文件；测试管理器正常结束清理，随机路径未留存，不声称逐路径事后核验。已保留原日志并在round8内重定向TEMP/TMP复跑相同49项；此偏差不隐去。

scope_exclusions：3030日报/UID/图表/附件预览、采集时效改造、AICS、数据库结构及生产同步操作不属于本独立MCP审查；读取daily全文为追溯MCP原话，不对日报验收。

本轮两项夹具失败保留：初版stdio探针等待非法fraction ID超时，已保留stdio-first-run.json，随后改成逐例记录无响应；首版HTTPS探针把SDK带前缀ToolError文字当字典，发生TypeError，live-first-failure.json保留，修正探针解析后17组通过。读取SDK旧路径session.py不存在的命令输出也记录在failure-notes.json。没有删除失败、修改产品来迎合探针或把首次失败说成全部一次通过。

正式原父Portal和当前task05的after.json均保持Deferred、user_decision=Pending；原父Deferred使官方Offer登记拒绝。真实技术审查授权与证据可以留存，但不能把本报告称官方Round/Passed，也不能伪造Gate或ManagedByParent。历史其他对象的Gate答复不构成当前版本批准。

完整JSON台账、所有条件对照、19个历史处置、16领域与证据索引见results.json。2项确认问题未修复，本轮连续无问题计数不能增加。
