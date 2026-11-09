# 客诉 MCP 接入与使用指南

面向：接收人、客户端开发者与发放管理员。文档版本：2026-10-30。工具参数参考由实际 `tools/list` schema 生成，完整原始 schema 随包交付。协议说明固定针对本服务已验证的 `2025-11-25` 版本，不能理解为支持未来全部 MCP 版本。

## 1. 服务与数据边界 {#overview}

|项目|当前配置|
|---|---|
|分享入口|@@PORTAL@@|
|MCP endpoint|@@ENDPOINT@@|
|允许网段|@@NETWORKS@@|
|传输|Streamable HTTP，HTTPS，JSON-RPC 2.0|
|响应模式|无状态、JSON响应，不分配Mcp-Session-Id|
|已验证协商版本|2025-11-25|
|推荐显式来源|production-ai-customer|
|数据时效|历史本地副本，生产采集已暂停；以get_sync_status返回的快照和最近同步时间为准|

服务包含11个只读工具及 `complaint-insights://guide` JSON资源。无写入工具、任意SQL、生产控制、邮件发送或模型调用工具。读取已发布的本地分析副本，不会因为查询而启动生产采集。不存在通过浏览器链接直接获得客诉数据的功能。

`production-ai-customer` 是历史生产数据的本地副本命名空间，名称不表示实时直连生产。`development-local` 是另一份开发数据，日期覆盖和数量不同。不要把两份来源混成一份报告。服务返回的 `schedule` 是配置周期，不能证明当前采集器在运行。`status` 为上次同步记录状态，也不等于实时连接状态。

## 2. 身份、令牌与使用约定 {#identity}

|身份|可执行动作|权限边界|
|---|---|---|
|普通内网访客|阅读指南、下载CA公钥/schema/无凭据客户端包|不能查看已发放身份、生成令牌、撤销令牌或读取客诉数据|
|MCP接收人|本人Bearer调用全部11个只读工具|Bearer不授予管理员登录能力；所有有效令牌具有相同的只读工具和已发布来源范围|
|唯一发放管理员|独立口令登录，按接收人发放、确认撤销、退出|管理凭据与MCP令牌分离；不提供再次显示旧令牌的功能|

管理员通过受控渠道发给每位接收人独立令牌。令牌没有自动到期时间，直到管理员撤销。遗失或泄漏后联系管理员撤销并重新发放。撤销对后续HTTP请求生效，已开始执行的只读请求不作强制取消。可以撤销最后一枚令牌，此时全部MCP访问被拒绝，管理员仍可登录重新发放。

令牌相当于该数据范围的读取凭据。只在 `Authorization: Bearer <本人的令牌>` 请求头中发送；不要放入URL、截图、共享文档、公开仓库或聊天提示词。不要转发其他人的配置文件。客户端输出的邮件和源行包含业务数据，按组织既有数据制度保管和使用；本服务未新增数据外发或转授权许可。

管理员口令、会话Cookie、MCP Bearer是三类不同凭据，不能互相代用。独立接收人身份用于分发、审计和撤销，不等同于字段级或来源级隔离。`get_capabilities` 返回的权限父链和enabled是能力目录，不能把目录中的 `token.issue` 当作MCP可调用工具。

## 3. TLS、CA与首次信任 {#tls}

1. 首次接入前，通过管理员的可信渠道取得 `mcp-ca.crt`，并核对文件SHA-256：`@@CA_SHA@@`。
2. 客户端使用包内CA公钥验证证书、证书链和内网IP。不能使用 `verify=False`、`-k` 或全局关闭TLS校验。
3. 浏览器打开3029前，需要在接收方电脑信任该CA。仅下载同一个尚未信任的HTTPS站点上的CA不能独立证明CA身份；首次文件与指纹应由管理员另行提供。
4. 如组织允许安装用户级根证书，Windows接收人可先核对指纹，再运行下面的命令。Python示例只加载指定CA文件，不要求修改系统证书库。

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath .\mcp-ca.crt
certutil.exe -user -addstore Root .\mcp-ca.crt
Test-NetConnection 10.8.61.200 -Port 3029
Test-NetConnection 10.8.61.200 -Port 3037
```

当前证书有效期结束：`@@CERT_EXPIRY@@`。CA文件SHA-256与服务器叶证书SHA-256不同，不要比较错对象。服务器证书信息与允许网段见 `mcp-endpoint.json`。使用内网IP访问，不能擅自替换为localhost、127.0.0.1或不在证书SAN里的主机名；这两个回环地址在接收方电脑指向接收方自己。

## 4. 快速开始：Python客户端 {#quickstart}

下载并解压 `mcp-client-kit.zip`，在解压目录执行。使用Python 3.11或更高版本；示例已在服务端Python 3.13环境验证。文件 `mcp-client.example.json` 不含有效令牌；`--configure` 以不回显方式读取管理员发给你的令牌。客户端先保护新建的空配置文件，再写入令牌，Windows仅当前用户和系统可读；写入或权限设置失败会清理本次新建文件，已有配置不会覆盖。请把配置与CA放在同一解压目录；需要迁移时同步处理相对 `ca_file` 路径。

```powershell
python .\mcp_client.py --config .\mcp-client.json --configure
python .\mcp_protocol_client.py --config .\mcp-client.json --list-tools
python .\mcp_protocol_client.py get_sync_status --config .\mcp-client.json
python .\mcp_protocol_client.py get_data_guide --config .\mcp-client.json
python .\mcp_protocol_client.py query_daily_statistics --config .\mcp-client.json --arguments-file .\queries\daily.json
python .\mcp_workflow.py --config .\mcp-client.json --start 2026-10-29 --end 2026-10-30
```

`mcp_protocol_client.py` 与 `mcp_workflow.py` 仅用Python标准库，无额外安装依赖。前者完整执行initialize、initialized通知及工具请求；后者运行11工具接入流程，从真实列表取得邮件和原始记录ID，只输出检查结果与版本，不输出客户内容。所选日期为空时，会明确报告依赖真实记录的步骤未执行，不制造示例数据。

SDK客户端需要安装随包锁定的依赖。需要完整分页时使用 `--all-pages`，它输出 `pages` 数组；只有 `complete=true` 才表示遍历结束。工具错误、版本变化、重复游标或超过页数上限时不会输出伪完整汇总。

```powershell
python -m pip install -r .\client-dependencies.txt
python .\mcp_client.py --config .\mcp-client.json --list-tools
python .\mcp_client.py list_mails --config .\mcp-client.json --arguments-file .\queries\mails.json --all-pages
python .\mcp_client.py query_daily_statistics --config .\mcp-client.json --arguments-file .\queries\daily.json --all-pages
```

退出码0为成功，1为连接、工具或配置失败。SDK客户端保留工具错误 `content`；标准库最小示例只报告错误类型，不打印服务器异常正文。排错可使用下文的原生JSON-RPC响应及 `X-Request-ID`，不要提交Bearer值。

其它MCP软件必须支持远程Streamable HTTP、自定义Authorization请求头、私有CA及2025-11-25协商。随包 `mcp-client-config.example.json` 仅演示常见 `mcpServers/url/headers` 配置结构，具体软件的字段由该软件决定。仅支持OAuth登录、不能配置Bearer或私有CA的软件不能直接使用本入口；本服务没有OAuth发现、动态注册或授权码端点。

## 5. 原生MCP协议交互 {#protocol}

单一 endpoint 接收HTTP POST。每次请求携带Bearer，`Content-Type: application/json`，并在 `Accept` 中同时声明 `application/json, text/event-stream`。初始化后携带协商得到的 `MCP-Protocol-Version`。本服务配置为JSON响应，无需维持会话ID；GET不提供SSE监听，DELETE不提供会话删除，返回405。它不是旧式 `/sse` 加消息端点的HTTP+SSE传输。

### 5.1 初始化与就绪通知

首次发出JSON-RPC请求，id为本连接序列内唯一整数或字符串。以下是请求体示例，真实Bearer只放在HTTP头中。

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"my-intranet-client","version":"1.0.0"}}}
```

读取响应 `result.protocolVersion`、`result.capabilities` 与 `result.serverInfo`。若不支持返回版本，应断开。本服务实际返回 `tools.listChanged=false`、`resources.subscribe=false/listChanged=false`，还含SDK声明的prompts能力；`prompts/list` 当前为空，没有业务提示模板。只有已协商能力可使用，不能从SDK名称推断任意可选功能已实现。

初始化成功后发送无id通知，成功HTTP响应为202且空正文；不要对空正文调用JSON解析。

```json
{"jsonrpc":"2.0","method":"notifications/initialized"}
```

### 5.2 发现、调用与结构化结果

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_sync_status","arguments":{"source_id":"production-ai-customer"}}}
```

上面两行表示两次单独POST，不是JSON数组，也不是一份JSON请求体。本服务的工具目录当前一次返回11个工具，无 `nextCursor`；工具内的业务分页使用 `next_cursor`，两者不能混淆。

请求 `id` 必须为字符串或整数，不能为null、布尔、数组或对象；数字表示 `1.0`、`1e3` 按等值整数处理，小数部分不为零时拒绝。数值ID最多4300位，单个请求体上限128KiB。通知省略id，成功接收返回202空体；客户端错误响应的id=null与请求规则不同。

每个工具包含name、description、inputSchema、outputSchema与只读注解。按照JSON Schema传真实JSON类型：布尔用true/false，整数不要改成字符串，mail_pk则必须是字符串。日期使用有效的YYYY-MM-DD字符串。所有工具拒绝未声明的额外参数；参数校验失败不会进入数据查询。成功结果在 `result.structuredContent`，同时提供 `result.content` 文本内容以供兼容；工具执行失败检查 `result.isError=true`，不能只根据HTTP200判断成功。调用不存在的工具返回顶层JSON-RPC `error.code=-32602`。

字符串值保持原值，不再作为JSON二次解析。例如字符串 `"null"` 不等于JSON空值 `null`；不存在的来源或无效游标会报业务错误，不会据此静默回退到默认来源或第一页。可空参数只有省略或传实际JSON `null` 才采用相应默认行为。

资源请求示例：`resources/list`，或 `resources/read` 参数 `{"uri":"complaint-insights://guide"}`。该资源返回静态使用口径；需要当前默认来源信息时调用 `get_data_guide`。

本服务只提供手工发放的独立Bearer，不实现MCP OAuth授权框架中的受保护资源发现、authorization_servers、动态客户端注册或刷新令牌。401中的 `WWW-Authenticate: Bearer realm="complaint-insights"` 是Bearer认证提示。不能把令牌管理页伪装成标准OAuth授权服务器。

## 6. 按需求选择工具 {#selection}

|需求|调用顺序|注意事项|
|---|---|---|
|确认来源与时效|get_data_guide → get_sync_status → get_capabilities|明确source_id、data_version、last_sync_at，勿把历史副本称为实时生产|
|了解分类树与候选状态|list_taxonomy|使用ID筛选，不用分类名称代替ID；不传status返回所有源状态|
|统计每天与三级分类的问题|query_daily_statistics(level=3)|明确primary/all_issues与direction；遍历全部页后分析|
|追溯某类客诉|list_mails → get_mail_detail|先窄日期与分类定位，再按mail_pk取正文和AI证据|
|按日与分类组织分析材料|query_daily_statistics → get_report_context|后者仅当前页材料，无周期总数；需要正文才include_body=true|
|查看附件、候选、提案、孤立AI与归档|list_source_tables → list_source_records → get_source_record|原始表用于追溯；附件只返回元数据，不下载或预览文件本体|
|遍历全量副本|按来源逐表list_source_records并分页|include_payload=true才含完整行；删除副本需include_deleted=true；没有任意SQL|

## 7. 数据口径、字段与分页 {#counting}

所有业务日期是Asia/Shanghai（北京时间），`start` 包含、`end` 不包含，即 `[start,end)`。查询2026-10-29这一天，传start=2026-10-29、end=2026-10-30。两端同时存在时start必须早于end；list_mails可只传一端，无两端则不加日期限制。业务日为空的邮件在无日期筛选的明细中仍可返回，不纳入按日汇总。

`primary`：每封邮件一个主分类；`all_issues`：同封邮件可有多个问题、跨多个分类，同一父级内部按邮件去重。跨分类、跨层级相加不能得到唯一邮件总量。`mail_count` 是当前分类桶的邮件数，`issue_count` 是问题计数，`pending_mail_count` 是待判断邮件数（它是mail_count的子集，不能额外加一次）。`PEND` 为待判断，不是已确认的具体客诉类型。统计采用本项目的AI分类规则，不自动采用人工覆盖。

精确实现：primary的issue_count为analysis_state=DONE且issue_type_id非空的邮件数，并非同一邮件的全部问题点数；all_issues的issue_count对源绑定ID非空、或DONE且问题类型非空的有效问题行计数。all_issues的mail_count在每个日期/方向/邮箱/分类桶内按mail_pk去重，跨邮箱和方向汇总是桶计数相加，不做会话、UID或发件人去重。pending_mail_count对应analysis_state不等于DONE的邮件数。

方向枚举严格区分大小写：RECEIVED（来信）、SENT（发信）、EXCLUDED（按规则排除）、ALL（不按方向筛选）。统计与报告材料默认RECEIVED，list_mails默认ALL，两种默认值不同。`mailbox` 为副本记录的邮箱字段精确匹配，不是模糊搜索；只有日统计和邮件列表支持该参数，get_report_context不支持邮箱筛选。

|字段|含义|
|---|---|
|mail_pk|源messages.id，按十进制字符串传；不是Message-ID或InboundMail.id。有效数值1至9223372036854775807|
|inbound_mail_id / ai_artifact_id|业务InboundMail.id / MailAiArtifact.id，不能拿来替代mail_pk|
|category_ai / category_normalized|AI原始建议 / AI流水线归一分类，不是人工覆盖|
|level_one / level_two / issue_type_id|一、二、三级分类ID；源名称先从list_taxonomy查|
|record_key / payload|原始表主键转文本 / 完整源行；record_key按文本排序，不是数值排序|
|meta|source_id、data_version、同步状态与快照时间等；用于限定这页数据的来源和版本|

列表结果一般为 `meta + items + next_cursor`；get_report_context为 `meta + days + next_cursor`。首页省略cursor或传JSON null，显式空字符串会被拒绝。保留所有原参数，只更新cursor，原样回传上页非空next_cursor，直到null。游标绑定来源、工具、筛选与数据版本；不能跨工具、改日期/分类/正文选项后复用，不能自行解码拼装。页大小limit可改变，但建议保持一致。

遇到DATA_VERSION_CHANGED/后端409，必须丢弃旧页，从无cursor首页重新查询，不能拼接新旧版本。普通SQL之外，MCP没有固定多工具事务快照；组合多个工具时也应核对meta.data_version。多页材料中的同一邮件在all_issues不同分类下重复出现，不能按出现次数作为邮件总数。

默认页大小与上限见逐工具表。taxonomy=100/1000，daily=200/1000，mails=30/200，report_context=20/100，source_records=20/50。输出Schema是开放对象，细节以真实响应字段为准，不虚构未实现的必填输出结构。

## 8. 全部11个工具参数参考 {#tools}

下列每个参数的必填、默认、类型、枚举和约束直接取自本次真实发现的inputSchema。只有Schema允许null的参数才可传null；省略非必填参数使用表中默认值。明确传source_id才能避免服务默认值将来变化导致选错来源。日期、ID含义和组合约束同时适用。只传文档列出的字段。

@@TOOLS@@

## 9. 原始表枚举与用途 {#tables}

table只接受以下14个大小写精确的固定名称。空表是合法查询结果；孤立AI和归档行不自动计入当前邮件总数。`include_deleted=true` 查询本地保留的删除副本，不是删除数据的动作。

@@TABLES@@

## 10. 错误与排查 {#errors}

先区分三层：TCP/TLS失败没有JSON-RPC响应；HTTP鉴权或传输错误有4xx/5xx；工具业务错误会以HTTP200包裹 `isError=true`。JSON-RPC顶层error与工具isError不能互换。

|现象或错误|含义与处理|
|---|---|
|证书校验失败/超时/连接拒绝|核对接收方10.8内网路由、两个端口、防火墙、CA指纹、证书有效期与SAN；不关闭TLS|
|HTTP401 VALID_MCP_BEARER_REQUIRED|令牌缺失、无效、已撤销，或配置失效关闭。联系发放管理员，不重试旧令牌|
|HTTP403 NETWORK_DENIED / HTTPS_REQUIRED|实际TCP来源不在允许网段或请求不是HTTPS；伪造代理头不能放行|
|HTTP400/406/415/413|检查JSON-RPC正文、协议版本、Accept、Content-Type及请求体大小；MCP请求体上限131072字节|
|HTTP405|方法不支持。本服务无GET SSE流或DELETE会话终止，使用POST /mcp|
|JSON-RPC -32700/-32600/-32601/-32602|JSON解析、请求结构、未知协议方法、未知工具或协议参数错误；已知工具的业务参数校验失败返回isError|
|工具INVALID_ARGUMENT，未调用后端|输入不符合公布的inputSchema，包括错误JSON类型、无效日期、额外参数或范围/枚举错误；按工具参考修正|
|工具INVALID_ARGUMENT，后端422|日期、枚举、分类长度、数值范围、游标归属错误；修正输入|
|工具NOT_FOUND，后端404|来源或邮件不存在，先查来源状态与列表|
|工具MAIL_ARCHIVED，后端410|旧主键已归档，查imap_reconcile_archive或新的当前邮件主键|
|工具DATA_VERSION_CHANGED，后端409|丢弃全部旧页，从首页重查，不拼接版本|
|工具RECORD_NOT_FOUND|所选表/record_key无当前行；追溯删除副本需显式include_deleted=true|
|工具DATA_UNAVAILABLE，后端503|本地副本不可用或来源未发布，联系维护者；不是自动恢复生产采集的指令|
|工具BACKEND_AUTH_FAILED / BACKEND_ERROR / BACKEND_UNAVAILABLE|服务器内部只读API凭据、连接、超时或响应异常；联系维护者并提供X-Request-ID，不提供Bearer|
|管理页401/403/421/429/503|分别检查独立管理员登录、同源CSRF、Host、登录限速、配置完整性；MCP Bearer不能代替管理员会话|

管理员登录连续5次失败后，同一实际TCP来源在15分钟窗口内受限。会话空闲20分钟、最长8小时，退出、服务重启或管理员凭据更换会失效。密码配置缺失或损坏时管理关闭，公开指南仍可阅读。令牌文件缺失/无效/重复/空值时MCP拒绝认证，不回退恢复启动时的旧令牌。

登录表单挑战有效10分钟；同一浏览器重载复用尚未使用的挑战。同一实际TCP来源最多保留8个有效挑战，并限制每分钟新建30个，清除Cookie不能绕过；达到限制返回429。共享出口的用户共用该来源限额。发放元数据损坏时停止新发放，管理员仍可登录并在管理页撤销有效身份；授权令牌文件本身损坏时管理和MCP认证均关闭。

## 11. 交接与验证清单 {#handoff}

1. 发放管理员给接收人分享3029入口；经可信渠道提供CA公钥及指纹；单独创建并交付该接收人的令牌。无需发送管理员口令、服务器私钥或任何SQL/API凭据。
2. 接收人核对CA、连通3029/3037，解压通用包、交互配置本人令牌，先运行原生tools/list，再运行get_sync_status确认source_id和数据版本。
3. 执行mcp_workflow.py；看到全部11项成功后，再按实际需求查询。无数据导致的跳过要换有数据区间复验，不能标为11项全部通过。
4. 分页查询直到next_cursor=null，核对相同来源/版本。统计明确日期范围、方向和scope；报告中记录来源、快照、数据版本及历史副本限制。
5. 接收人离岗或令牌泄漏时，管理员确认身份后撤销；接收人旧令牌后续请求应401。新令牌单独重新交付，不复用其他人的身份。

包内SHA256SUMS校验下载后文件完整性，但从同一入口拿到的校验和不能代替首次CA的可信渠道核对。维护者更改工具或服务后必须重新从运行中tools/list构建材料并复验，不能只改说明里的版本号。

服务端经内网IP的HTTPS验证不代表另一台电脑路由已经验收。接收方仍须在其电脑执行上述检查，特别是CA安装、端口路由及本人令牌。

## 12. 官方协议来源与实现依据 {#sources}

本服务协议依据以下固定版本官方文档；参数、数据范围、默认值和限制依据本服务实际schema与实现。这里不声称已实现完整OAuth或全部MCP可选特性。

- [MCP 2025-11-25 Base Protocol](https://modelcontextprotocol.io/specification/2025-11-25/basic)
- [MCP 2025-11-25 Transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
- [MCP 2025-11-25 Lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)
- [MCP 2025-11-25 Tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)
- [MCP 2025-11-25 Authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)

本项目实现：insights/mcp_server.py、insights/mcp_http.py、insights/api.py、insights/datasets.py、insights/token_desk.py。下载tools-schema.json可核对本次原始发现结果。schema不是数据快照；实际数据版本由每次查询返回。
