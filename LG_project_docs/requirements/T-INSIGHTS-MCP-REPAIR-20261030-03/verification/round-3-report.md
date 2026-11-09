第3轮独立只读对抗性审查：确认4项问题，本轮不是干净轮次。原始基线的约定产品范围已逐条检查；末次发现外部版本漂移，当前混合工作树未完成重新定版与整轮复验，coverage=Incomplete。

项目：D:\LFEN_project\dev_project\complaint-insights。交付任务：T-INSIGHTS-MCP-REPAIR-20261030-02。开始：2026-10-29T20:16:19.182808+00:00；结束：2026-10-29T20:40:40.677703+00:00。
起始工程版本SHA256：974965546ff8c800f6aea4ec1355b5c2443f5a1646345fdbd28d441a66b06930。已保存工程正式subject_sha256：770988aa2d3d135cd795851cc84784e8f137f5ca7873933515b505ad0a05c369，已执行官方只读get_approval_subject.py核对。46文件中45项起末匹配，insights/capabilities.py漂移；起末全部匹配标志：False。逐文件起末hash见final-snapshot.json，原始首次末检见final-snapshot-first.json。

版本漂移：{"path": "insights/capabilities.py", "start_sha256": "72f11bacf9d0343e6bb4691d9bae166fc6770d53639917188b1ca25ba25ec2cb", "end_sha256": "4ba56d2776ec1028b02002878f9ffe88c59bc3acd29687db16c975cfbfc92b60", "observed_file_last_write_utc": "2026-10-29T20:34:39.1355727Z", "content_delta": "新增insights.attachments.logs.export权限与daily_log_archive能力；原MCP token_issue/revoke条目未改。末次已完整阅读新文件，但未重新定版或复验全部新工作树。", "mutation_source": "非本轮工具发起；根确认也未编辑该产品文件；未独立确认具体外部执行者。"}

先亲自读取两份before.json的完整request_snapshot、clarification、scope、authority，以及原survey的既有权限原话；先形成review-plan.json和自创反例，再读取fixes.json/前轮报告。父审查者提出的同一凭据竞态也在本轮独立原始计划中，实际使用自己的合成文件复现，没有依赖父证据代验。

原文逐条覆盖（quote保留同来源完整原句及限定）：

U01｜供其他人使用｜部分实现

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

来源：portal.request_snapshot。证据：live-results.json；client-results.json；R3-02；R3-03。正常11工具与下载客户端能用；非法ID与空游标仍存在协议/查询范围缺陷。


U02｜提供详细介绍｜已实现

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

来源：portal.request_snapshot。证据：live-results.json:all_documented_tools；additional-live-controls.json。指南全文、11个完整inputSchema、14表、TLS/认证/来源/计数/分页/错误/交接齐全；公共材料与真实schema一致。维护交接当前统计另列R3-04。


U03｜按MCP本身协议制作文档或程序｜部分实现

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

来源：portal.request_snapshot。证据：synthetic-results.json；live-results.json；protocol-id-additional.json；R3-02。正常原生2025-11-25、通知、资源与工具成功；含非法ID的请求被当作通知返回202空体，整数值数值表示1.0/1e3也被丢弃。

条件对照：{"input": "合法整数/字符串ID，2025-11-25头", "expected": "200结果保留ID", "actual": "0、字符串、大整数均200且同ID同类型", "result": "Passed"}
条件对照：{"input": "id=true/null/1.5/[]/{}", "expected": "非法信封-32600", "actual": "202空体", "result": "Failed"}
条件对照：{"input": "notifications/initialized无ID", "expected": "202空体", "actual": "202空体", "result": "Passed"}
条件对照：{"input": "协议头2999-01-01", "expected": "HTTP400", "actual": "HTTP400", "result": "Passed"}

U04｜接收人拿到材料能够使用MCP｜部分实现

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

来源：portal.request_snapshot。证据：live-results.json:downloaded_sdk_full_pagination；client-results.json；R3-03。无凭据ZIP、标准库与SDK正常接入成立；完整邮件遍历成功，空字符串游标会静默回首页。异机限制已明示。


U05｜优化并复核token生成服务｜部分实现

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

来源：portal.request_snapshot。证据：synthetic-results.json；existing-tests.log；R3-01。独立认证/会话/CSRF、限速、原子存储、并发及失败恢复成立；管理员凭据更换存在双读竞态。


U06｜在内网开放token服务入口｜已实现，异机限制保留

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

来源：portal.request_snapshot。证据：live-results.json；listeners-observed.json；firewall-observed.json；tls-observed.json。3029/3037仅绑定10.8.61.200，实际10.8私网及严格CA可达；规则仅Domain/Private、指定地址/端口/以太网/10.8.0.0/16。


U07｜将使用协议、介绍及方法放在token服务｜已实现

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

来源：portal.request_snapshot。证据：live-results.json:download_exact_file；live-results.json:full_guide_html。/guide与7项公开下载200；发布字节逐一相同，在线HTML等于完整指南渲染，完整原生协议与运行方法可读。


U08｜单一内网链接分享全部接入材料｜已实现，已声明外部限制保留

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

来源：portal.request_snapshot。证据：live-results.json；additional-live-controls.json。首页统一入口链接到指南、CA、schema、无凭据客户端和管理登录；离线/在线引用无坏锚点；首次CA信任需可信渠道，未将单一URL误称自动授权。


U09｜MCP在独立聊天；原聊天继续日报｜本轮已遵守；历史创建由原交付分工证明

> 开一个新会话处理MCP相关事宜，本会话继续完成客诉日报看板

来源：portal.request_snapshot。证据：review-plan.json；listeners-observed.json；service-processes-observed.json。当前MCP scratch/独立审查上下文；本轮不创建或发送其它聊天消息，不修改/重启日报、API、数据库或附件。历史创建事件不是本轮重演的动作。


U10｜继续原已授权MCP范围｜已遵守

> 继续

来源：portal.request_snapshot。证据：review-plan.json；subject-observed.json。原继续指令未解释成新增管理员、OAuth、生产读取、正式门禁或验收批准。


U11｜简单网页发放访问token｜已实现

> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

来源：portal.discovery/survey.md:既有权限原话。证据：synthetic-results.json:full_admin_control；LG_project_docs/requirements/T-INSIGHTS-MCP-REPAIR-20261030-02/verification/results.json。合成独立管理员登录后网页签发；根按当前版本执行真实签发/使用/撤销/退出15组验证，本轮核对其脚本和日志，不真实签发。


U12｜虽然内网，必须经本人下发的token才能实际访问MCP｜已实现，凭据重置竞态另列

> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

来源：portal.discovery/survey.md:既有权限原话。证据：synthetic-results.json；live-results.json:mcp_http_boundary；R3-01。真实无令牌/错误令牌401，持现有Bearer真实只读成功；合成撤销最后一枚后拒绝、重发后恢复；管理员口令不当Bearer、接收人Bearer不管理。

条件对照：{"input": "内网+有效现有Bearer", "expected": "只读工具成功", "actual": "11工具/14表成功", "result": "Passed"}
条件对照：{"input": "同内网无Bearer或错误Bearer", "expected": "401", "actual": "401", "result": "Passed"}

U13｜3029端口；localhost限制的后续演进｜已实现

> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

来源：portal.discovery/survey.md:既有权限原话。证据：listeners-observed.json；tls-observed.json；portal.request_snapshot。当前3029仅绑定指定私网IP；后续同一用户明确要求内网开放，覆盖旧localhost-only约束；未同时声称只监听localhost。


U14｜匿名访客仅阅读文档和下载无凭据客户端｜已实现

> 令牌发放保留哪种管理员范围？普通内网访客均只能阅读文档、下载无凭据客户端；只有登录管理员才能生成或撤销 MCP 令牌。

来源：portal.clarification:r1.e1.question。证据：synthetic-results.json:roles_control；live-results.json；client-results.json。匿名文档/下载200，匿名admin重定向、Bearer无管理会话401；ZIP不含现有真实Bearer/私钥/数据库URI。管理员初始口令及后端秘密扫描由根真实验证器证据核对。

条件对照：{"input": "匿名访客读取指南与下载", "expected": "200且无有效凭据", "actual": "7项下载200且内容扫描通过", "result": "Passed"}
条件对照：{"input": "匿名或MCP Bearer尝试管理", "expected": "无法发放撤销/查看身份", "actual": "合成401与真实/admin303", "result": "Passed"}
条件对照：{"input": "合成管理员独立登录", "expected": "进入管理", "actual": "200", "result": "Passed"}

U15｜只有登录管理员才能生成或撤销MCP令牌｜部分实现

> 令牌发放保留哪种管理员范围？普通内网访客均只能阅读文档、下载无凭据客户端；只有登录管理员才能生成或撤销 MCP 令牌。

来源：portal.clarification:r1.e1.question。证据：synthetic-results.json；R3-01；LG_project_docs/requirements/T-INSIGHTS-MCP-REPAIR-20261030-02/verification/results.json。正常独立登录、同源CSRF及确认撤销门槛成立；轮换竞态允许旧密码获得绑定新凭据版本的管理会话。

条件对照：{"input": "合成正确登录+同源CSRF+撤销确认", "expected": "签发200、撤销303", "actual": "200/303", "result": "Passed"}
条件对照：{"input": "无管理会话、错误CSRF/Origin、不确认撤销", "expected": "拒绝", "actual": "401/403/400", "result": "Passed"}
条件对照：{"input": "读取旧凭据后、读取摘要前更换凭据；旧密码登录", "expected": "不得获得新版本有效会话", "actual": "登录303、管理200", "result": "Failed"}

U16｜沿用唯一所有者默认，没有额外管理员｜已遵守

> 继续

来源：portal.clarification:r1.e1.answer。证据：review-plan.json；insights/token_desk.py:configure_admin/_admin。原问题和推荐默认完整保留；真实回答仅“继续”，原需要本人下发及单一凭据对象支持唯一owner，不声称用户选择了多管理员。


U17｜把管理员账号密码给用户｜由根私聊交付；本轮按分工未读取口令

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

来源：repair02.request_snapshot。证据：parent delegation message；release/operator-handoff.md。根确认在本轮首次审查开始前的私聊commentary已交付owner/初始口令/登录链接，精确原消息时间不可查。本轮没有亲见口令，不把转述冒称直接独立验证；最终自包含交付仍由根完成。


U18｜提供登录入口｜已实现

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

来源：repair02.request_snapshot。证据：live-results.json:anonymous_route；release/operator-handoff.md。https://10.8.61.200:3029/admin/login 严格CA返回200；表单具独立账号/口令输入及登录挑战。


U19｜登录该账号即可生成token｜正常路径已实现；边界缺陷列R3-01

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

来源：repair02.request_snapshot。证据：synthetic-results.json:full_admin_control；LG_project_docs/requirements/T-INSIGHTS-MCP-REPAIR-20261030-02/verification/results.json。本轮以自创凭据独立验证登录→发放→一次显示→确认撤销→最后撤销→重发；真实当前链路由根15组检查并有日志，审查者未真实登录签发。


U20｜发现问题修复复验，直到同版连续两轮完整无问题｜本轮已执行，发现问题待返修；版本漂移，整体多轮目标尚未完成

> 工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。

来源：repair02.request_snapshot。证据：initial-snapshot.json；final-snapshot.json；synthetic-results.json；live-results.json；report.md。本轮4项确认问题，不能计为干净轮次；末次发现capabilities.py在审查期间发生非本轮写入的变更，原始基线范围已检查，但新混合工作树没有完成重新定版与整轮复验。正式人类门禁和user_decision仍Pending，原父Deferred使官方Offer登记失败，未伪造机器Passed或ManagedByParent。


U21｜明确开始审查｜已遵守

> 开始审查

来源：repair02.request_snapshot。证据：review-plan.json；parent delegation message。用户真实“开始审查”授权后执行本轮同范围只读审查；不额外要求重复授权、不扩大生产/发布/权限。


确认问题：

R3-01（P2）管理员校验数据与会话凭据版本来自两次文件读取，轮换竞态可使旧密码创建新版本有效会话

位置：insights/token_desk.py:58-64、225-269。
输入：取得有效登录挑战；_admin的read_object读取旧凭据后，另一维护操作用configure_admin原子替换凭据；随后_admin读取新文件字节求版本hash；以旧密码完成POST登录。
预期：更换后的凭据版本不能给旧密码认证产生持续有效管理会话；同一快照应同时用于校验与版本摘要。
实际：轮换已实际发生，旧密码登录303，后续/admin200；再正常轮换一次后旧会话303，证明普通重置对照有效。
影响：在服务器维护者重置管理员口令的并发窗口内，已掌握旧口令的请求仍可签发/撤销令牌。该行为违背交接与指南的凭据更换使旧管理会话失效承诺。
证据：synthetic_review.py:rotate_after_read；synthetic-results.json:credential_rotation_between_snapshot_reads；synthetic-results.json:normal_credential_rotation_control。

R3-02（P2）带非法ID的请求被SDK联合模型回退为通知；整数值数值表示也丢失请求响应

位置：insights/mcp_http.py:139-196，锁定mcp2.3的原始消息解析边界。
输入：{"method": "tools/list", "id_values": [true, false, null, 1.5, [], {}], "integer_valued_number_representations": ["1.0", "1e3"]}。
预期：布尔/null/非整数/容器ID非法，应-32600；整数值数字请求应按请求处理并返回对应ID；通知只有无ID才可202空体。
实际：合成环境和真实服务非法ID均202空体；合成1.0/1e3也202空体。合法0、字符串、大整数均200且ID保留；客户端result/error响应合法ID及error id=null均202控制正常。。
影响：不满足MCP固定版请求ID与通知结构契约；调用方无法按错误码定位非法信封，合法整数数值表示的请求还会丢失应答。
证据：synthetic-results.json:jsonrpc_id_boundary；live-results.json:live_invalid_request_id；protocol-id-additional.json。

R3-03（P2）五个分页工具的显式空字符串cursor静默选择第一页

位置：insights/mcp_server.py:36（Cursor）；insights/api.py:126-129（既有后端，仅定位不修改）；release/client-guide.template.md:111附近的字符串/默认行为说明。
输入：{"tools": ["list_taxonomy", "list_mails", "query_daily_statistics", "get_report_context", "list_source_records"], "cursor": ""}。
预期：显式字符串不是省略或JSON null；无效游标应INVALID_ARGUMENT，不能成功回到第一页。
实际：五工具均isError=false，structuredContent逐对象等于省略cursor的第一页；非空非法cursor对照全部isError=true。Schema只有maxLength，没有最小长度，既有page_state用if not cursor判断默认页。。
影响：错误客户端分页状态被当作成功查询，重读首页或对不完整/重复页进行分析，且违背当前指南的明确默认/游标承诺。可在MCP边界拒绝空串，无需改变3036。
证据：empty-cursor-independent.json；live-results.json:empty_cursor_boundary；insights/mcp_server.py:Cursor；insights/api.py:page_state。

R3-04（P3）当前维护交接页把旧版验证数量写成当前证据

位置：LG_project_docs/requirements/T-INSIGHTS-MCP-PORTAL-20261030-01/release/operator-handoff.md:55。
输入：读取本交付清单中的维护交接“当前证据”段，并与当前repair02 after.json和verification/results.json核对。
预期：当前交接应指向当前验证结果，或明确25项/12组属于历史版本。
实际：交接仍写“当前证据：25项…真实HTTPS验证12组”；本交付after为36项单测、15组真实检查；本轮又独立重跑36项全部通过。该段没有历史标记。。
影响：维护者无法仅按当前交接确定此版本的验证基线，数字与工程留档不一致。没有观察到由此引发的功能故障，严重度P3。
证据：release/operator-handoff.md:55；LG_project_docs/requirements/T-INSIGHTS-MCP-REPAIR-20261030-02/verification/results.json；.project-governance/tasks/T-INSIGHTS-MCP-REPAIR-20261030-02/after.json；existing-tests.log。

完整审查范围与实际验证：

权限与管理：管理员挑战的实际peer绑定/一次性/600秒等号/8个来源容量/另一peer对照；现有5次失败/900秒窗口、空闲/最长会话、退出与轮换测试；原子双读轮换新反例；真实角色/Host/Origin/HTTPS边界与合成代理头、表单格式/重复值/超限体、会话CSRF和确认撤销；正常签发一次显示、重复身份、最后一枚撤销、重发恢复。
存储：损坏授权文件不覆盖、重复键/重复token/BOM/非字符串拒绝，授权提交失败保留旧图、元数据孤儿不授权、同身份重试可恢复；撤销提交失败不伪装成功、临时文件清理、元数据损坏仍可网页紧急撤销；16项并发签发与8项并发撤销没有丢写；既有跨进程测试重跑通过。真实服务不注入故障。
原生MCP：固定2025-11-25 initialize→initialized(202空体)→tools/list；11工具完整Schema/只读注解/开放输出Schema逐一核对；资源guide、空prompts、无状态GET/DELETE405；未知版本400；全部工具新正向控制、严格类型/范围/日期/枚举/额外参数负向、字符串原值保持及后端零调用；未知方法/工具/缺协议参数/解析/非法信封通过既有36测试逐层核对；新ID家族产生R3-02，未把SDK默认行为当正确性证明。
真实数据：11工具均由当前授权Bearer只读调用；14表全部核对默认元数据与include_deleted/include_payload=true正向；非空表用真实键内存取得完整记录，3张空表保留合法空结果与RECORD_NOT_FOUND控制；显式production/default/null/development来源对照；不记录客户正文、原始payload、实际ID或任何凭据。
分页与计数：分类limit7/1000、单日邮件limit17/200完整遍历结果逐对象相同；真实下载SDK完整邮件分页；primary所有3分类深度×4方向与独立邮件列表推导mail_count/issue_count/pending完全相同；all_issues逐方向校验非负及pending子集，代码和指南共同核对父级去重/跨桶交叉；报告正文false/true、游标正文选项绑定；14表非空次页接续与mailboxes limit1/50全遍历。messages无筛选全量双遍历没有完成，已保留这一夹具设计调整，不冒称全量历史镜像已审计；产品分页控制通过其它独立全遍历和同接口接续核对。
材料与客户端：七公开下载与当前46文件字节相同；23文件ZIP逐内部校验和、全部路径、脚本/依赖副本、8来源示例与无现有真实Bearer/私钥/数据库URI核对；在线指南精确等于完整MD渲染，11段完整inputSchema匹配真实tools/list，离线资源和在线锚点无断链；Windows合成Users可读父目录中首次写入前实际ACL已收紧，whoami/ACL/部分写入/fsync/fdopen故障后无新配置、既有文件不变；分页版本改变/重复游标/页数上限/中途工具错误均不输出伪完整页汇总，成功对照complete=true；后端401/404/409/410/422/503/500均分层且脱敏。
部署与证据：3029/3037精确私网绑定，3030/3036/15433回环；规则Domain/Private、以太网及10.8范围；现场服务进程没有watch；production.json只输出allow_production_read=false与target_reader_url解析出的127.0.0.1:15433；不连接任何数据库。两端严格CA与证书IP校验成功、TLS1.3，叶证书指纹与公开配置一致；现有UI预览亲自查看。36项既有测试本轮重跑通过；根真实15组验证与代码/日志一致。after Deferred、Pending和原机器限制没有伪装通过；维护交接旧计数另列R3-04。

前轮处置复核：

R1-01：原始反例修复已复核；证据：existing-tests.log:test_refresh_and_cookie_clearing_cannot_exhaust_other_peer_login；synthetic-results.json:challenge_capacity_control。

R1-02：原始反例修复已复核；证据：existing-tests.log；synthetic-results.json:bad_metadata_emergency_revoke。

R1-03：原始反例修复已复核；证据：existing-tests.log；synthetic-results.json:tool_schema_boundary。

R1-04：原始反例修复已复核；证据：existing-tests.log:test_raw_http_schema_validation_and_protocol_error_layer。

R2-01：原始反例修复已复核；空串cursor另列R3-03；证据：synthetic-results.json:literal_value_control；live-results.json:business_negative_control。

R2-02：原始反例修复已复核；证据：client-results.json；existing-tests.log。

R2-03：原始非法信封反例已修复；更广ID信封反例R3-02仍失败；证据：existing-tests.log:test_raw_http_schema_validation_and_protocol_error_layer；protocol-id-additional.json。

疑似误报与夹具失败：

N01｜Accept仅application/json仍200不是确认缺陷｜NotAnIssue。固定版要求客户端声明两种Accept，但没有要求服务端对该兼容子集强制406；本服务JSON响应属于Accept允许范围。夹具406预期过窄。 证据：live-results.json:mcp_http_boundary；https://modelcontextprotocol.io/specification/2025-11-25/basic/transports。

N02｜text/plain返回400不必强制415｜NotAnIssue。输入被4xx拒绝；固定传输文档没有要求这一输入必须415。不能把过窄HTTP状态预期计为缺陷。 证据：live-results.json:mcp_http_boundary；https://modelcontextprotocol.io/specification/2025-11-25/basic/transports。

N03｜空mailbox/status/分类参数没有清除过滤｜NotAnIssue。5项真实空串筛选均只返回对应字段等于空串的记录；API对这些字段使用is not None。未新增要求这些空字段必须报错，R3-03限定为cursor的明确承诺。 证据：live-results.json:empty_string_filter_kept；insights/api.py:taxonomy/read_mails。

N04｜3张源表为空不是未实现｜NotAnIssue。真实目录14表；11表有行，3表空结果合法。空表get_source_record使用合成不存在键验证RECORD_NOT_FOUND；未制造当前行。 证据：live-results.json:all_table_query_and_detail。

N05｜error响应id=null不是请求id=null｜NotAnIssue。客户端错误响应与请求结构不同；error id=null真实SDK对照202，修复不得对没有method的响应套用请求ID限制。 证据：protocol-id-additional.json。

H01｜最初读取。scratch尚不存在，进程创建目录错误；已先建立scratch并重试

H02｜拆条计划初次写入。把文本实际换行误作字面\n拆分，引发IndexError；未生成该次文件；改为实际换行重新生成

H03｜synthetic-review.log。最小ASGI成功夹具未实现lifespan，TestClient启动断言失败；补齐纯夹具lifespan后复验。

H04｜synthetic-review-retry1.log。预期所有ID反例都有JSON正文，但实际202空体触发json.loads；保留失败，改为记录空体后得到R3-02。

H05｜live-results-initial.json public_portal。HTTP头名以区分大小写键查找导致假失败；新case统一小写后no-store真实通过。

H06｜live-results-initial.json report_context_control。夹具误写字段body_text，当前视图字段为body_plain_text/body_translated；独立修正字段后false/true对照均通过。

H07｜live_review_initial.py source_records全量messages双遍历。无业务日期筛选的messages双遍历运行超过约300秒，主动只停止本轮两个已核对命令行的审查Python进程；保留62项已完成结果与初始脚本/日志；未停止任何服务。改为14表首/次页连贯性、mailboxes完整遍历与单日邮件完整双遍历；不声称messages全量遍历已经完成。

真实验证分工：

- 本轮亲自：全部46文件产品/文档/测试/证据，原文与澄清、36项测试、自创65隔离观察、20客户端故障检查、真实授权只读11工具/14表、严格CA公开材料、分页计数、部署监听/防火墙/进程；所有实际ID和客户payload仅内存。
- 真实管理员登录→签发→读取→撤销→退出由根在本版本先行执行15组检查，审核者已读验证器全文、当前results和原始摘要日志，另以合成凭据独立验证管理全链路；未运行mcp_portal_verify.py。
- 初始口令私聊交付由根确认，本轮未读取或写出口令，精确原消息时间不可查，不冒称亲见。
- 现有430/1440 UI预览与布局结果亲自查看，当前CSS/JS/HTML完整读取；没有新增真实管理员浏览器交互或全部浏览器矩阵。

已声明外部限制：

- 另一内网电脑路由、CA安装和本人客户端未实测；只证明本机经内网IP严格CA。
- 正式independent-review/security-privacy-review与user_decision仍Pending，本轮不代批。
- 父Deferred导致官方Offer登记拒绝的原失败由根保留；本轮只写scratch，不声称机器Passed/ManagedByParent。

未检查必需产品项：["capabilities.py外部变更后的新混合工作树需重新定版并完成完整一轮；本轮不将原基线测试当作新字节版本已复验"]。原始基线产品范围已用代码、独立合成反例、授权真实只读与明确管理链路证据分工核对；外部改动的新工作树尚未全量复验，不隐去该缺口。不表示另一电脑、真实破坏性故障或人类最终门禁已执行。发现的4项均仍待根返修，不计为连续干净轮，也不声称整体多轮任务完成。

判定使用的外部原始来源：
- [MCP 2025-11-25 Base Protocol](https://modelcontextprotocol.io/specification/2025-11-25/basic)：请求ID须为字符串或整数且不可null，通知无ID；请求与响应限制分开。
- [Transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)：Origin、POST、通知202空体、GET405和协议版本头；Accept客户端要求不能替代不存在的服务端强制拒绝条款。
- [Lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)：初始化与协商；[Tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)：Schema和工具错误分层；[Authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)：核对文档没有冒称完整OAuth。

全部证据路径在本轮scratch；results.json列出逐条原文、条件对照、全部文件阅读清单、实际时间/版本/哈希及证据引用。没有修改治理数组或人类批准。
