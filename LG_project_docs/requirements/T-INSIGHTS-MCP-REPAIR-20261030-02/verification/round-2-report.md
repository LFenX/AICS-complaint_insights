第二轮独立只读对抗性审查完成：确认3项问题（R2-01、R2-02、R2-03），本轮不计为干净轮次，连续计数0。约定产品审查面完整；验证分工与外部限制均在下文明确，不替代正式人类门禁。

审查项目：D:/LFEN_project/dev_project/complaint-insights；当前交付：T-INSIGHTS-MCP-REPAIR-20261030-01；无Git。开始：2026-10-29T19:52:03.031470+00:00；结束：2026-10-29T20:06:09.610942+00:00。开始与结束45文件哈希全部匹配，清单自身未变化。版本SHA256：d5824b26cb3b4ef46360ff83047250be6190c3feb6aaf171b62710fbb670ed7c；正式subject_sha256：54320013394c6bd06bbe598bdbca6aae785cac5c979b180b7d929ba18e9d3b97，本轮通过官方只读get_approval_subject.py核对。

首先独立读取父/返修before.json完整request_snapshot、唯一澄清原问题/推荐默认/真实回答及scope/authority，并读survey中的既有完整权限原话。之后才读取第一轮报告和fixes.json，没有把其结论当成本轮前提。下列quote保留同来源完整原句；细拆不截掉限定词。



U01｜MCP供其他人使用｜部分实现

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

来源：portal.request_snapshot。证据：L07；L08；L13；L14；L15；R2-01；R2-02。客户端凭据保护和部分字符串参数仍有缺陷；异机路由为已声明外部限制



U02｜提供详细介绍｜已实现

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

来源：portal.request_snapshot。证据：document-checks.json；L06；L07。指南覆盖协议/身份/TLS/全部参数/枚举/分页/来源/统计/错误/交接；所有11段inputSchema逐对象等于真实发现



U03｜按MCP本身协议制作文档或程序｜部分实现

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

来源：portal.request_snapshot。证据：F17；F18；F20；F21；F22；protocol-edges.json；R2-01；R2-03。合法字符串被二次解析；非法JSON-RPC信封错误码不符合规范



U04｜接收人拿到材料能够使用MCP｜部分实现

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

来源：portal.request_snapshot。证据：L13；L14；L15；C01；C02。正常接入成功；Windows首次凭据写入与写入异常存在泄漏窗口



U05｜优化并复核token生成服务｜已实现，本轮新问题在MCP及接收客户端

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

来源：portal.request_snapshot。证据：F01-F16；existing-tests.log；verification/results.json。本轮未确认新的门户发放/撤销缺陷；完整审查结果仍未通过



U06｜在内网开放token服务入口｜已实现，外部限制保留

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

来源：portal.request_snapshot。证据：L01-L06；deployment-listeners-end.json；deployment-firewall.json。3029为10.8.61.200 HTTPS，允许10.8.0.0/16；另一台电脑未实测



U07｜将MCP使用协议和介绍方法放在token服务｜已实现

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

来源：portal.request_snapshot。证据：L03；L06；document-checks.json。/guide及7项公开下载与当前发布文件逐字节一致



U08｜可直接分享整个服务的内网链接｜部分实现

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

来源：portal.request_snapshot。证据：L03；L06；L13；R2-02。一个入口提供全部接入材料；接收客户端凭据失败恢复仍需修复



U09｜MCP独立会话；日报看板继续在原会话｜已遵守

> 开一个新会话处理MCP相关事宜，本会话继续完成客诉日报看板

来源：portal.request_snapshot。证据：当前聊天工作目录 complaint-insights-mcp；deployment-listeners-end.json；deployment-processes.json。本轮未操作日报、3030、3036、数据库、附件、AICS或历史治理；本轮不能重新证明历史新会话创建事件



U10｜继续已授权的MCP范围｜已遵守

> 继续

来源：portal.request_snapshot。证据：T-INSIGHTS-MCP-PORTAL-20261030-01-original.json authority；本轮工具记录。没有从继续推导额外管理员、OAuth、生产读取或人类门禁批准



U11｜简单权限发放网页、生成访问token｜已实现

> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

来源：portal.discovery/survey.md 既有权限原话，原来源T-INSIGHTS-DAILY-20261030-01/before.json。证据：F08-F16；verification/results.json real_owner_issue_use_revoke_and_logout。本轮真实管理员链路由根执行者先行验证，审查者以隔离夹具独立复核



U12｜虽为内网，必须由本人下发token才能访问MCP｜已实现

> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

来源：portal.discovery/survey.md 既有权限原话。证据：L05；F02；F12；F15。匿名MCP401；接收人Bearer不能管理；撤销和损坏均拒绝后续访问



U13｜3029端口及原localhost约束的后续演进｜已实现

> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

来源：portal.discovery/survey.md 既有权限原话。证据：L01；L03；deployment-listeners-end.json。后续同一用户明确要求内网开放，现只绑定10.8.61.200:3029；没有同时宣称仍只监听localhost



U14｜普通内网访客只能阅读文档、下载无凭据客户端｜已实现

> 令牌发放保留哪种管理员范围？普通内网访客均只能阅读文档、下载无凭据客户端；只有登录管理员才能生成或撤销 MCP 令牌。

来源：portal.clarification:r1.e1.question。证据：F02；L03；L05；L13。匿名可读公开材料、管理拒绝；包不包含本次允许读取的接收人Bearer/私钥/数据库URL；初始管理员口令由根已有验证器扫描，本审查未读取



U15｜只有登录管理员才能生成或撤销MCP令牌｜已实现

> 令牌发放保留哪种管理员范围？普通内网访客均只能阅读文档、下载无凭据客户端；只有登录管理员才能生成或撤销 MCP 令牌。

来源：portal.clarification:r1.e1.question。证据：F02；F08-F16；verification/results.json。独立凭据、会话、同源Origin、CSRF、确认撤销与状态恢复均有正反例



U16｜沿用推荐的唯一所有者，不新增管理员｜已遵守

> 继续

来源：portal.clarification:r1.e1.answer。证据：token_desk.py configure_admin/_admin；F08；operator-handoff.md。回答仅为继续；唯一所有者依据原“需要我下发”及推荐默认，不声称用户选了多个管理员



U17｜把管理员账号密码给用户｜交付事实有来源，本审查未读取口令

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

来源：repair.request_snapshot。证据：根执行者同一私聊确认；operator-handoff.md；verification/results.json。根执行者确认在本次私聊审查开始前交付owner/口令/登录入口；精确原消息时间不可查。未把此转述冒充本审查亲见口令



U18｜提供登录入口｜已实现

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

来源：repair.request_snapshot。证据：L03；operator-handoff.md。https://10.8.61.200:3029/admin/login；真实正常表单和独立管理员登录均有证据



U19｜登录该账号即可生成token｜已实现

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

来源：repair.request_snapshot。证据：F08；F10；F11；F12；verification/results.json real_owner_issue_use_revoke_and_logout。正常管理可签发；无效会话/CSRF/损坏授权拒绝，元数据损坏只保留撤销



U20｜多轮审查发现问题修复复验，直至同版本连续两轮完整无问题｜本轮执行完整，发现问题待返修

> 工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。

来源：repair.request_snapshot。证据：fixture-results.json；client-results.json；protocol-edges.json；hash-start.json；hash-end.json。本轮3项确认问题，连续干净计数为0；未替代正式人类门禁或用户验收



U21｜明确开始审查｜已遵守

> 开始审查

来源：repair.request_snapshot。证据：repair.request_snapshot；当前委派消息。同范围审查获授权；没有重复要求授权或执行真实管理员变更



确认问题：



R2-01（P2）合法字符串null在Schema校验后被SDK二次解析为None，清除来源、筛选或游标

位置：insights/mcp_server.py:78-87；MCP 2.3.0 utilities/func_metadata.py:228-265；insights/api.py:251-284。

输入：{"tool": "list_mails", "arguments": {"source_id": "null", "mailbox": "null", "cursor": "null"}}。

预期：符合公布Schema的字符串应保持原值；不存在的来源/无效游标可以返回相应业务错误，但不能静默当作省略参数

实际：HTTP200且isError=false；FakeAPI收到source_id=None、mailbox=None、cursor=None。另level_one="null"被转换为None。真实ReadAPI会省略None并选用默认来源，后端不添加对应筛选。

影响：查询成功但查询对象或范围发生变化；无效游标null被当作首页而非报错。

对照：record_key="null"、mailbox="true"、mailbox="123"与带引号字符串保持原值；错误JSON类型被Schema正确拒绝，见F18。

证据：fixture_review.py；fixture-results.json F19-literal-string-0/1。



R2-02（P2）Windows客户端在设置受限ACL前写入Bearer，写入异常遗留可读凭据文件

位置：scripts/mcp_client.py:26-37；下载包mcp_client.py同字节副本；client-guide.md第4节受限配置承诺。

输入："合成父目录仅在scratch授予BUILTIN Users继承读取；下载客户端configure输入合成令牌。正常json.dump前观察ACL；另在json.dump完成写入后注入OSError。"。

预期：第一个凭据字节写入前已建立受限访问；任何写入或保护失败不留下含Bearer的配置。

实际：正常写入阶段Users仍有继承读取，成功后才由icacls移除。json.dump抛OSError时文件仍存在，包含完整合成令牌，Users继承读取仍存在。

影响：配置位于允许其他账户读取的目录时，正常首次写入存在泄漏窗口；磁盘/编码/写入异常后泄漏持续。当前try仅包住ACL设置，未包住凭据创建/序列化。

对照：正常结束后Users访问已移除；仅合成数据，结束已删除合成令牌配置文件。未读取或写入真实接收人配置。

证据：client_review.py；client-results.json C01/C02。



R2-03（P3）非法JSON-RPC信封被错误归类为Invalid params -32602

位置：insights/mcp_http.py:142使用锁定SDK默认传输；requirements.txt mcp==2.3.0；MCP 2.3.0 server/streamable_http.py:587-597。

输入：["[]", "{\"jsonrpc\":\"1.0\",\"id\":1,\"method\":\"tools/list\"}", "{\"jsonrpc\":\"2.0\",\"id\":3,\"method\":123}", "{}", "null"]。

预期：能解析JSON但不是有效JSON-RPC Request的输入返回-32600 Invalid Request；解析错误为-32700，方法参数错误才为-32602。

实际：以上均HTTP400、id=null、error.code=-32602。

影响：与本服务文档及JSON-RPC2.0错误分类不符，调用方无法按错误码区分信封/版本结构错误和方法参数错误。

对照：破损JSON "{" 返回-32700；未知协议方法返回-32601且保留id；tools/call缺少name返回-32602且保留id；未知工具当前正确返回-32602。

证据：fixture-results.json F22-batch/F22-bad-envelope；protocol-edges.json。



完整范围及真实验证：

权限/状态：匿名与Bearer均不能管理；实际peer而非代理头、HTTP/HTTPS、Host后缀、opaque/cross-port Origin；单次且peer绑定的10分钟挑战、清Cookie来源上限/恢复；5次失败窗口及代理伪装；Secure/HttpOnly/Strict Cookie；缺失Origin、错误类型、重复CSRF、超限表单；成功签发只显示一次、重复身份、显式确认撤销；空闲/绝对会话/退出/凭据轮换由30项现有测试与新增夹具共同覆盖。

存储：合法JSON但元数据值类型损坏仍可网页撤销且停止签发；重复授权JSON键全部拒绝并可恢复；最后令牌撤销后可独立登录重发；签发授权提交失败不授权、撤销元数据提交失败仍生效；5个跨进程撤销和8个签发混合并发无丢写。所有永久夹具文件仅在scratch。

原生协议：2025-11-25 initialize→initialized HTTP202空正文→tools/list 11；无会话头、GET/DELETE405、超限体413、错误版本400、Accept拒绝；日期/整数/大小写枚举/额外字段/无效ID错误不查询；未知工具及方法错误分层；资源guide含14表；新合法字符串反例和非法信封反例产生R2-01/R2-03。

真实工具：L08独立只读调用全部11工具，L09对14表读取当前/删除元数据，非空表按真实record_key取同记录核对；11表有行、3张空表保留为空，不制造数据。数据来源production-ai-customer、版本24、历史状态DEGRADED。只记录工具名、数量、状态和版本；正文、客户payload、实际ID和秘密始终只在内存。

材料和客户端：7公开下载与发布字节相同；23文件ZIP逐内部SHA256SUMS校验，当前脚本与产品同字节；8查询示例均显式生产历史副本来源；11段指南inputSchema与真实tools/list逐对象相同；指南/离线材料链接无损坏。下载SDK用limit1000完整遍历分类4页，同版本且末页cursor=null；标准库工作流11工具无跳过。独立合成transport验证变版、重复游标、页数上限均拒绝伪完整，正常分页complete=true。新Windows ACL/写入失败反例产生R2-02。

部署/保护：3029/3037实际监听10.8.61.200，3036/15433/3030回环；防火墙为Domain/Private、以太网、10.8.0.0/16、精确本机地址/端口。现场无watch；production.json仅输出allow_production_read=false及target_reader_url的127.0.0.1:15433；未打印完整配置。根部署证据中3030/3036/15433 PID前后不变，本轮起末读取监听PID一致；未重启任何服务。没有连接源10.8.45.155:5432或任何数据库，没有采集、日报/附件/AICS/历史任务操作。

已复查前轮：R1-01通过F05/F06与现有刷新测试；R1-02通过F11合法JSON损坏形态及现有损坏网页测试；R1-03原错误类型、日期和额外参数拒绝已成立，但R2-01显示合法值在下游仍被改写；R1-04通过F20未知工具顶层-32602。前轮四项原反例已修复，不因其修复就忽略本轮新问题。



疑似误报与夹具失败：



N01｜F21曾预期text/plain必须415，实际400｜NotAnIssue。固定版传输没有要求该输入必须415；请求体同时为无效信封{}。安全中间件已以4xx拒绝，没有错误请求进入后端。不能把本夹具过窄预期作为产品问题。证据：fixture-results.json F21；https://modelcontextprotocol.io/specification/2025-11-25/basic/transports。



N02｜L03首次将HTTP头名当作区分大小写，no-store判定失败｜NotAnIssue。HTTP头名不区分大小写；夹具统一小写后所有实际响应no-store，live-run.log保留原失败、live-run-retry.log保留复验。证据：live-run.log；live-run-retry.log；live-results.json L03。



N03｜首次SDK分类分页limit=1且max_pages=1000触发页数上限｜NotAnIssue。历史分类超过1000项，客户端按契约拒绝输出不完整汇总。改用公开允许的limit=1000后4页完整且同版本；没有修改产品代码。证据：live-run.log；live-results.json L14；client-results.json C03-pagination-page-bound。



N04｜ACL夹具初次以stream.name当路径，后子PowerShell模块加载失败｜HarnessFailure。stream.name是文件描述符；修正路径后子PowerShell受继承模块路径影响。最终直接用本机icacls读取ACL完成独立复现。三份原失败日志均保留，未把夹具异常当产品缺陷。证据：client-run.log；client-run-retry.log；client-run-retry2.log；client-results.json。



正式已声明的外部限制：

- 另一台内网电脑的实际路由、CA安装和本人客户端接入未实测，原交付已明确声明；当前只证明本机经内网IP严格CA。

- independent-review、security-privacy-review正式人类门禁与user_decision仍Pending；本审查不能代为批准。

- 父工程结果Deferred使官方adversarial_review.py拒绝Offer，失败已由根保留；本轮不写治理记录，不声明机器Passed或ManagedByParent。



本轮实际验证分工和未亲自执行的操作：

- 审查者新增执行：全部隔离反例、现有30测试、严格CA公开与MCP只读、11工具14表、真实SDK4页分类遍历、下载工作流11工具、仅允许字段的生产配置核查、监听/防火墙只读。

- 真实唯一管理员登录→签发→调用→撤销→退出由根执行者在本轮开始前按当前版本重跑，证据verification/results.json的13checks和.runtime/mcp-portal-repair-live-A02.log；本审查读取并与验证器实现核对，另以独立合成凭据测试管理全链路。审查者没有真实签发/撤销。

- 管理员账号口令私聊交付由根执行者确认；审查者按约束未读取初始口令，精确原消息时间不可查。报告不包含口令。

- 服务端破坏性故障、凭据轮换、挑战耗尽和并发写入仅在scratch夹具执行；没有在真实服务故障注入。

- 本轮读取现有430/1440预览图、当前HTML/CSS/JS与布局证据；未新增真实管理员浏览器交互或未来浏览器矩阵，此类矩阵不在已约定范围。



没有隐藏的必查产品路径：unreviewed_required_product_items=[]。这表示本轮对约定审查面已作实现、隔离反例或明确当前证据分工核对；不表示真实服务器破坏性故障、另一台电脑或正式人类门禁已执行。三项产品缺陷仍未解决，本轮不能通过或算作连续干净轮。

协议判定来源：[MCP 2025-11-25 Transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)；[Lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)；[Tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)；[JSON-RPC 2.0 §4/§5.1](https://www.jsonrpc.org/specification)。R2-03依据JSON-RPC明确区分-32600与-32602；R2-01/R2-02依据实际公开Schema和凭据保护承诺及本机可复现观察，不以依赖默认行为作合规凭证。

全部本轮证据：hash-start.json；hash-end.json；fixture_review.py；fixture-results.json；fixture-run.log；client_review.py；client-results.json；client-run-retry2.log；live_review.py；live-results.json；live-run.log；live-run-retry.log；existing-tests.log；document-checks.json；protocol-edges.json；deployment-listeners-end.json；deployment-firewall.json；deployment-processes.json；server-credential-acls.json。report.md和results.json仅写本轮scratch，不写产品、服务配置、真实凭据、治理记录或任何人类批准。
