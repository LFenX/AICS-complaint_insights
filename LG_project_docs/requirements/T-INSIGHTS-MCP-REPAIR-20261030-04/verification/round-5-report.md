# 第5轮独立只读对抗性审查

结论：完成约定范围审查，确认5项问题（P1×1、P2×3、P3×1），本轮不是干净轮次，连续计数0。coverage=Complete。未修改产品或96项冻结交付。

时间：2026-10-29T21:39:28.817254+00:00 → 2026-10-29T22:01:23.562918+00:00。当前Git：7b63ad65b66a94084db8a40a43838929eabcbb07；origin/main同提交。交付版本：dde52278607189a7306d330eda6cda2275b57b209a751915069db4a0f6eea613。

起末核对：96文件（88 Git受控+8公开材料）全部匹配冻结清单；Git起末status为空；version_unchanged=True。见baseline-start.json、baseline-end.json。此绑定是当前Git交付，不是旧D盘工程subject，也不是正式人类Gate。

## 审查输入与方法

亲自完整读取run-governed-product-workflow/SKILL.md、commands/verify.md，及原门户before.json的request_snapshot、唯一澄清问答/默认、requirement_items、authority/scope；亲自读survey既有完整权限原话，再读第三次返修before.json完整账号口令/多轮原始请求，最后核对session.json中“拉取最新代码并重启审查”。先写independent-plan.json、形成新反例，再读前三轮原报告和fixes。未以派生清单或实施者通过结论代替原文。

完整阅读当前token_desk.py、mcp_tokens.py、mcp_http.py、mcp_server.py、门户JS/CSS、公开构建器/3客户端/管理员/防火墙/manage脚本、指南模板/生成指南/Schema/交接；必要依赖capabilities、datasets、config、API分页、db只读设置、projection统计与initialize视图源码仅只读。没有执行数据库、生产、watch、bootstrap、sync、mcp_portal_verify.py或真实管理员变更。

## 已确认问题

### R5-001 · P2 · 同一peer并发成功/失败登录使失败请求抛KeyError并返回500

位置：insights/token_desk.py:357；insights/token_desk.py:360

复现：两个浏览器客户端共享合成实际peer；错误密码认证在工作线程内等待；另一个正确认证先返回303并删除failures[peer]；随后释放错误认证。

预期：正确认证303；错误认证401并提供新挑战和重试表单；失败计数仍可核对。

实际：正确303、有效会话200；错误500且无重试表单。独立根夹具确认KeyError；授权文件未改变。

影响：并发使用同一出口时失败登录不能正常反馈/重试；失败窗口共享状态存在竞态。

证据：concurrent-login.json；concurrent_login.py；../restart-20261030/root-concurrent-login.json

### R5-002 · P2 · 工具数字参数先经二进制浮点舍入，违反严格原值schema

位置：insights/mcp_http.py:168；insights/mcp_server.py:85

复现：原始HTTP tools/call list_mails，分别传limit数值字面量1.00000000000000001、200.00000000000000001、0.99999999999999999；与1.0及1.5控制对照。

预期：数学值非整数或低于最小值应isError且后端零调用；1.0作为整数值可成功。

实际：三个反例均HTTP200/isError=false且调用FakeAPI，参数变为1、200、1；1.0成功和1.5拒绝控制成立。

影响：公开整数/范围契约与实际接受值不一致；原始查询参数被隐式改写。id有Decimal保护，arguments无对应保护。

证据：numeric-schema.json；numeric_schema.py

依据：[json-schema.org](https://json-schema.org/understanding-json-schema/reference/numeric)；[modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-11-25/basic)

### R5-003 · P3 · 首页标为mcp-client.json的配置片段不是有效JSON，且未标示伪代码

位置：insights/token_desk.py:134

复现：提取首页snippet代码文本，交给JSON解析器。

预期：文件示例使用带引号的占位字符串，或清楚注明只是不可直接使用的配置示意。

实际：bearer_token值只有/* 管理员发给你本人的令牌 */，缺少JSON值；JSONDecodeError，首页无配置示意标注。

影响：首次接入者照首屏配置文件示例替换/创建文件时得到非法JSON。下载模板与configure正确，范围仅首页说明。

证据：new-management.json；new_management.py

### R5-004 · P1 · no-referrer与严格Origin校验冲突，浏览器原生管理表单全部403

位置：insights/token_desk.py:481；insights/token_desk.py:477；insights/token_desk.py:188

复现：使用当前响应Referrer-Policy:no-referrer的原生POST表单。Fetch算法将非cors导航POST的Origin设为null；正确凭据/挑战或有效会话+CSRF均被当前Origin边界拒绝。

预期：同源浏览器能正常登录、签发、确认撤销和退出；跨源与不可信Origin继续拒绝。

实际：根真实浏览器POST/issue记录Origin:null、403；本独立当前代码对照中正常Origin登录303，相同挑战Origin:null403，已登录的issue/revoke/logout同样403，授权字节未变。根仅将UI夹具响应header改same-origin后，浏览器登录303、签发200。

影响：用户要求的网页登录后生成token在标准浏览器表单路径上被阻断。手工设置Origin的HTTP测试不能覆盖此交互。

证据：origin-policy.json；origin_policy.py；../restart-20261030/original-form-origin-failure.log；../restart-20261030/preview.py；../restart-20261030/same-origin-positive-control.log

依据：[fetch.spec.whatwg.org](https://fetch.spec.whatwg.org/#append-a-request-origin-header)；[developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy#effect_on_the_origin_header)

### R5-005 · P2 · 合法长身份撑宽管理网格，移动端发放输入框与撤销列初始被裁切

位置：assets/token-desk.css:152；assets/token-desk.css:176；assets/token-desk.css:17

复现：在430px浏览器视口展示含一个合法64字符身份的当前管理页；不进行定位器自动滚动前观察发放区和身份表。

预期：发放表单适配可用415px宽度；长身份在明确可滚动表格容器中显示，操作列可发现，不把整页网格撑宽。

实际：table宽775.609px，撤销summary初始x728.609超出415px内容区；table wrapper overflow:visible且html clip；截图显示发放输入框也越出屏幕。定位器点击可自动滚动使summary到x364并展开，因此不是完全不能撤销。

影响：单个合法身份使移动管理布局破坏，输入字段和关键操作初始被裁切；横向位置变化后左右内容难以同时核对。

证据：../restart-20261030/root-browser-evidence.json；../restart-20261030/admin-long-identity-mobile-7b63ad6.png；../restart-20261030/admin-clipped-form-mobile-7b63ad6.png；../restart-20261030/admin-revoke-long-mobile-7b63ad6.png

## 全部原文逐条对照

每项quote保留同来源完整原句；同一句多要求独立拆条。完整source_sha256、限定上下文、条件编号、正反输入/预期/实际/result及证据在results.json.requirements；原文未被改写。

### O01 · 提供可交给其他接收人的详细MCP介绍

来源：portal:request_snapshot。状态：部分实现。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

详细指南、11工具与14表、全部schema和客户端齐全；首页配置片段R5-003需修正。

证据：materials.json；live-results.json；R5-003

### O02 · 说明与程序依照MCP原生协议

来源：portal:request_snapshot。状态：部分实现。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

固定2025-11-25初始化/通知/资源/错误分层通过，严格数字原值仍R5-002。

证据：test_mcp.log；synthetic-results.json；R5-002

### O03 · 接收人据此能完成接入并使用全部只读工具

来源：portal:request_snapshot。状态：部分实现。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

现有Bearer的11工具、3类客户端、完整分页和正文可用；新接收人依赖的浏览器发放被R5-004阻断。

证据：live-results.json；client-results.json；body-proof.json；R5-004

### O04 · 优化并复核令牌生成服务

来源：portal:request_snapshot。状态：部分实现。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

独立认证/权限隔离/轮换/会话/CSRF/限额/存储并发已复核；R5-001与R5-004未解决。 移动长身份布局另见R5-005。

证据：test_token_desk.log；synthetic-results.json；new-management.json；R5-001；R5-004；R5-005

### O05 · 内网提供令牌服务入口

来源：portal:request_snapshot。状态：已实现。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

实际3029/3037监听10.8.61.200，当前代码保留HTTPS及实际peer限制；新版门户以隔离夹具验证，运行3029仍是旧UI。

证据：listeners.json；extra-live.json；test_token_desk.log

### O06 · 把MCP协议、介绍和接入方法放于发放服务

来源：portal:request_snapshot。状态：已实现。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

当前同一门户路由提供在线完整指南和7项公开下载，23项通用包一致。

证据：live-results.json；materials.json

### O07 · 接收人使用一个内网链接阅读、下载并找到接入路径

来源：portal:request_snapshot。状态：部分实现。

> 另外MCP工具后续我会给其他人使用，MCP工具的介绍需要比较详细，请按照MCP本身的协议来制作文档或者程序，后续我会给其他要用该MCP的人，让他们能够使用我的MCP，另外MCP token生成所运行的服务你也需要优化并复核一下，然后在内网开放该服务入口（生成token的服务），然后请将该MCP的使用协议介绍方法等，放置在生成token的服务上，后面我会直接给其他需要用到该MCP的人整个服务的内网链接，这样省事很多

一个链接可阅读、下载和找到接入路径；原生管理员表单被R5-004阻断。 移动长身份布局另见R5-005。

证据：live-results.json；materials.json；R5-004；R5-005

### O08 · 本审查只处理MCP，不干涉日报及排除服务

来源：portal:request_snapshot。状态：已遵守。

> 开一个新会话处理MCP相关事宜，本会话继续完成客诉日报看板

仅MCP审查及round5证据；未修改/重启日报、3030/3036/15433、附件、AICS、源生产或旧治理。

证据：baseline-start.json；baseline-end.json；production-boundary.json

### O09 · 沿用已有MCP授权和单一所有者权限，不扩大管理员

来源：portal:request_snapshot。状态：已遵守。

> 继续

继续只沿用所有者发放和MCP范围；未新增管理员/OAuth/生产操作或代批人类门禁。

证据：independent-plan.json

### O10 · MCP使用必须拥有所有者下发的独立令牌

来源：survey:existing_authority。状态：已实现。

> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

真实有效Bearer读取，匿名/错误Bearer401；合成撤销和损坏配置失效关闭均通过。

证据：live-results.json；extra-live.json；test_mcp.log；test_token_desk.log

条件：存在有效MCP Bearer才授予数据读取；无效、撤销或缺失时拒绝

|分支|输入|预期|实际|结果|
|---|---|---|---|---|
|Met|有效现有Bearer；合成新发/重发Bearer|11工具读取成功|真实11工具与撤销后重发恢复成功|Passed|
|NotMet|匿名、错误、撤销、损坏/丢失token配置|拒绝；不回退启动令牌|真实匿名/错误401；合成全部失效关闭|Passed|

### O11 · 门户使用3029；后续明确内网开放覆盖原localhost绑定

来源：survey:existing_authority。状态：已实现。

> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

3029当前指定内网IP开放；当前源码+隔离正反验证HTTPS/实际peer/Host/Origin及代理头无效，另一电脑路由/CA保留外部限制。

证据：listeners.json；test_mcp.log；test_token_desk.log；extra-live.json

条件：属于指定内网实际TCP peer且HTTPS/Host正确才允许；伪造代理头无效

|分支|输入|预期|实际|结果|
|---|---|---|---|---|
|Met|指定内网实际TCP peer+HTTPS+正确Host|入口可读|真实严格CA HTTPS成功；合成200|Passed|
|NotMet|HTTP、公网peer、错Host/Origin、伪造X-Forwarded-*|不放行|合成403/421；真实错Origin403/Host421|Passed|

### O12 · 结合提问、推荐默认和survey：唯一独立owner，访客只读文档；登录管理员才能发放/撤销

来源：portal:clarification:r1.e1。状态：部分实现。

> 继续

唯一owner和管理/MCP身份隔离成立；合法原生浏览器管理遭R5-004拒绝。

证据：test_token_desk.log；new-management.json；origin-policy.json；R5-004

条件：独立管理员会话及同源CSRF有效才允许管理；匿名、MCP Bearer、跨会话、失效会话等拒绝

|分支|输入|预期|实际|结果|
|---|---|---|---|---|
|Met|合成唯一管理员、有效会话/CSRF、手工正常同源Origin|签发/撤销成功|303登录、200一次显示、303撤销，底层逻辑通过|Passed|
|Met|同源真实浏览器原生表单；正确独立凭据或会话/CSRF|正常登录或管理提交|no-referrer使Origin:null；403（R5-004）|Failed|
|NotMet|无会话、仅MCP Bearer、失效会话、错误/缺失/跨会话CSRF或跨Origin|拒绝且授权不变|当前隔离正反与真实匿名拒绝；未发现越权|Passed|

### O13 · 提供唯一管理员账号；原交付为owner，本轮核对唯一凭据机制

来源：repair:request_snapshot。状态：已实现（历史交付分工）。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

原交付账号owner及唯一管理员机制可核对；本轮不重新读取真实管理员凭据。

证据：../AICS-database-MCP/LG_project_docs/requirements/T-INSIGHTS-MCP-PORTAL-20261030-01/release/operator-handoff.md；test_token_desk.log

### O14 · 有效管理员登录后能生成并交付可用令牌

来源：repair:request_snapshot。状态：部分实现。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

合成管理员带正常Origin可登录签发、一次显示并撤销；原生浏览器受R5-004阻断。

证据：new-management.json；origin-policy.json；R5-004

条件：有效管理员登录后带CSRF签发成功；未登录与无效凭据拒绝

|分支|输入|预期|实际|结果|
|---|---|---|---|---|
|Met|合成唯一管理员、有效会话/CSRF、手工正常同源Origin|签发/撤销成功|303登录、200一次显示、303撤销，底层逻辑通过|Passed|
|Met|同源真实浏览器原生表单；正确独立凭据或会话/CSRF|正常登录或管理提交|no-referrer使Origin:null；403（R5-004）|Failed|
|NotMet|无会话、仅MCP Bearer、失效会话、错误/缺失/跨会话CSRF或跨Origin|拒绝且授权不变|当前隔离正反与真实匿名拒绝；未发现越权|Passed|

### O15 · 已授权多轮完整对抗审查、返修、复验，同版连续两轮零问题才结束

来源：repair:request_snapshot。状态：部分实现。

> 工程结果已保存。依据 [run-governed-product-workflow](C:/Users/Administrator/.codex/skills/run-governed-product-workflow/SKILL.md)「工程完成并保存结果后，必须主动询问用户是否启动对抗性审查」，是否启动多轮审查？发现问题将修复并复验，直至同一版本连续两轮完整审查无问题；此选择不影响现在登录和生成令牌。

已按授权进行本轮完整审查并保存反例；本轮有问题，必须返修并以新版本重启计数，不能声明两轮收敛。

证据：report.md；results.json

条件：同版、完整、零确认且无未决问题方可计干净；发现问题/缺口/漂移归零

|分支|输入|预期|实际|结果|
|---|---|---|---|---|
|Met|同版+完整+连续两轮零问题|才可标审查通过|本轮不满足前提，未伪造此正向事实|NotRun|
|NotMet|本轮有5项已确认问题|连续计数归零，不结束|计数0，保持返修/后续完整复审|Passed|

### O16 · 实际开展审查，正式人类Gate和用户验收不代批

来源：repair:request_snapshot。状态：已实现。

> 开始审查

实际重新读取原话、构造新反例、执行完整范围审查；不自批正式独立/安全门禁或用户验收。

证据：independent-plan.json；results.json

### O17 · 当前最新Git与96文件材料绑定，旧版本轮次不计数

来源：session:request_snapshot。状态：已实现。

> 拉取最新代码并重启审查

origin/main、HEAD及96项起末hash绑定当前最新7b63ad65；旧D版及前轮不计干净。

证据：baseline-start.json；baseline-end.json；../restart-20261030/session.json

### O18 · 交付管理员口令；仅引用真实历史交付分工，不重新读取或公开秘密

来源：repair:request_snapshot。状态：已实现（历史交付分工）。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

既有工程记录记载口令仅在用户私聊交付；本轮不读真实initial/admin秘密，不重新显示或落盘口令。用户接收及验收由真实原消息/用户决定保留。

证据：../AICS-database-MCP/LG_project_docs/requirements/T-INSIGHTS-MCP-REPAIR-20261030-03/verification/report.md

### O19 · 提供可直接到达的管理员登录入口

来源：repair:request_snapshot。状态：部分实现。

> 把管理员账号密码给我，然后给一个登录入口，登录该账号即可生成token

/admin/login入口可达，独立口令表单存在；浏览器正常提交因R5-004无法登录。

证据：new-management.json；origin-policy.json；R5-004

### O20 · 提供简单权限发放网页，能生成访问令牌

来源：survey:existing_authority。状态：部分实现。

> 另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，

新管理页面的发放、确认撤销、一次显示等逻辑通过隔离测试；原生浏览器提交受R5-004影响。 移动长身份布局另见R5-005。

证据：new-management.json；test_token_desk.log；R5-004；R5-005

条件：登录唯一管理员并通过同源CSRF才签发；其它身份拒绝

|分支|输入|预期|实际|结果|
|---|---|---|---|---|
|Met|合成唯一管理员、有效会话/CSRF、手工正常同源Origin|签发/撤销成功|303登录、200一次显示、303撤销，底层逻辑通过|Passed|
|Met|同源真实浏览器原生表单；正确独立凭据或会话/CSRF|正常登录或管理提交|no-referrer使Origin:null；403（R5-004）|Failed|
|NotMet|无会话、仅MCP Bearer、失效会话、错误/缺失/跨会话CSRF或跨Origin|拒绝且授权不变|当前隔离正反与真实匿名拒绝；未发现越权|Passed|

## 必需范围完成情况

|范围|状态|证据|
|---|---|---|
|S01 原始需求/澄清/权限/版本穷举|Complete|independent-plan.json；baseline-start.json；baseline-end.json|
|S02 单一owner、独立认证、轮换、会话、退出|Complete|test_token_desk.log；new-management.json；concurrent-login.json；origin-policy.json|
|S03 HTTPS、actual peer、Host、Origin、代理头、CSRF、Bearer隔离|Complete|test_token_desk.log；test_mcp.log；extra-live.json；origin-policy.json|
|S04 挑战活跃/每分钟上限、失败窗口、时效恢复、登录并发|Complete|test_token_desk.log；new-management.json；concurrent-login.json|
|S05 一次显示、刷新/关闭、确认撤销、最后一枚、恢复|Complete|test_token_desk.log；new-management.json|
|S06 授权/元数据原子提交、线程/跨进程并发、故障恢复/残留|Complete|test_token_desk.log；synthetic-results.json|
|S07 固定MCP初始化/通知/资源、11工具schema原值、分层错误、只读|Complete|test_mcp.log；synthetic-results.json；numeric-schema.json；live-results.json|
|S08 14表raw payload、完整分页、统计primary/all_issues、正文、来源/版本|Complete|live-results.json；extra-live.json；all-issues.json；pagination-api.json；body-proof.json|
|S09 在线指南、7下载、23包、参数/Schema/材料一致及秘密隔离|Complete|live-results.json；materials.json；new-management.json|
|S10 下载SDK/stdlib/workflow、Windows真实ACL、失败残留、分页恢复|Complete|client-results.json；test_mcp.log|
|S11 新版首页/导航/登录重试/管理筛选/撤销弹层/一次提示/暗色移动/指南折叠复制|Complete|new-management.json；materials.json；../restart-20261030/original-form-origin-failure.log；../restart-20261030/root-browser-evidence.json；../restart-20261030/same-origin-positive-control.log|
|S12 实际监听/生产隔离及部署分工|Complete|listeners.json；production-boundary.json；../restart-20261030/session.json|

## 实际验证及分工

|验证组|数量/结果|证据|
|---|---|---|
|现有MCP回归|20 / Passed|test_mcp.log|
|现有门户回归|21 / Passed|test_token_desk.log|
|新增存储/协议/错误映射|83 / 83通过，0失败|synthetic-results.json|
|真实MCP与当前公开材料|99 / 99通过，0失败|live-results.json|
|下载客户端/ACL/恢复|17 / 17通过，0失败|client-results.json|
|all_issues口径|4 / 4通过，0失败|all-issues.json|
|五分页API版本/过滤绑定|5 / 5通过，0失败|pagination-api.json|
|当前新管理逻辑|18 / 18通过，0失败|new-management.json|
|材料生成/引用一致|10 / 10通过，0失败|materials.json|
|补充真实表/鉴权/TLS|22 / 22通过，0失败|extra-live.json|
|明确真实正文字段|7 / 7通过，0失败|body-proof.json|

这些是不同粒度的检查组/断言，不与41个unittest直接合并宣称测试总量。live.py早期body_text弱断言由body-proof.json的明确字段证据取代。反例结果另列findings，不以正向组通过掩盖。

真实3037通过专用CA，11工具与14表（11表有行、3表合法空），原始payload/get_source_record逐对象相同；taxonomy完整25页3370项；限定2026-10-29 RECEIVED邮件4页634封、context7页634封；primary三级mail/issue/pending逐桶与完整邮件独立重算相同；all_issues完整context8页673次出现/634封，31个二级桶去重数与daily相同，11个一级分类完整list_mails逐桶相同。所有观察data_version=24、来源production-ai-customer、历史快照状态DEGRADED。没有据此宣称当前生产实时或全历史数据已审计。

当前公开ASGI入口7项下载逐字节一致，ZIP23项、内外相关校验和、所有脚本和实际Schema一致；11完整schema和参数表由当前生成器逐对象核对。下载SDK真实4页634封、stdlib初始化和workflow全11工具成功。Windows真实ACL在Users可读父目录下首字节前已无继承/Users读取，仅2个ACE；ACL、部分写和fsync失败新文件清理。

新版浏览器由/root亲自操作，本人读取固定日志、root-browser-evidence.json和截图。原no-referrer失败保存于original-form-origin-failure.log；仅UI夹具header改same-origin的正向控制证明登录303、发放200、一次令牌复制/关闭。11 schema初始折叠、真实展开和复制变“已复制”；实际深色rgb(9,9,11)。移动合法长身份布局已明确列R5-005，不隐藏为通过。HTTPS/peer/cookie重写的HTTP夹具只证明UI，不作为真实TLS/管理员安全证据。

先前私聊交付记录；本轮未重复读取/重登真实口令。root当前压缩上下文不能提供精确消息时间，未补造；引用已存operator-handoff及原工程报告作为历史分工，用户验收Pending。

## 既有发现处置

前三轮11个具体反例（R1-01至04、R2-01至03、R3-01至04）在当前原测试及新增对照中按原输入复验通过，登记Fixed仅指对应旧复现路径；R1-03同一契约仍有本轮新精度反例R5-002。未把旧Fixed或41项回归通过当本轮预设结论。完整prior_resolutions见results.json。

## NotAnIssue与证据限制

- N5-01：430视口根scrollWidth较clientWidth多8px。html明确overflow-x:clip，尚无全页横向滚动；代码块内横向滚动为有意可用行为。不能仅凭scrollWidth判整页故障。
- N5-02：3张原始表为空，get_source_record无可用真实ID。空表是已公布合法结果；14表查询已执行，3空表非existent key返回RECORD_NOT_FOUND。未伪造记录或跳过原表入口。
- N5-03：资源guide不含default_source。指南明确资源为静态使用口径；get_data_guide才返回当前default_source；两者去除该字段逐对象相等。
- N5-04：旧3029与当前Git门户UI不同。用户要求拉取新代码重审；新UI使用本版隔离夹具，真实3037核心有字节一致支持；没有将旧UI或旧截图冒称当前新版证据。
- N5-05：移动指南clientWidth415/scrollWidth511。root实际检查差异来自pre内部代码宽度且overflow:auto，普通段落/列表inline code未溢出；不是本轮管理网格裁剪问题。

## 夹具失败及修正

- FX5-01：最初start.py按字面\n\n拆分request导致IndexError。仅修正round5夹具将存档换行表达归一后拆条；原JSON未改，真实source_sha256仍对原文完整值计算。
- FX5-02：两次只读命令遗漏repo workdir，读取文档/rg路径未找到。用已确认Git工作目录/绝对路径重新完整读取；没有因此跳过范围。
- FX5-03：嵌套Windows PowerShell 5.1因继承模块路径无法加载Get-Acl。保留client-acl-fixture-failure.log，改用当前pwsh执行原生ACL只读；随后真实icacls与首字节前ACL检查17组全过。
- FX5-04：live.py初始正文对照用了body_text/.get弱断言。未将弱断言作为正文证明；独立读取真实view字段后新增body-proof.json，以明确字段存在及原值对照7/7取代该断言。

## 外部限制与门禁

- 另一内网电脑路由、CA安装和真实接收人环境未实测，保留原已声明边界。
- 真实3029仍为旧门户UI；本轮新UI不以它作证。根UI夹具只用于界面交互，HTTPS/peer/cookie的适配不是安全验收。
- 本轮未读取真实initial/admin/server/registry/agent秘密，未真实登录/发放/撤销。现有Bearer仅在内存供真实3037只读，真实ID/正文/payload不落盘。
- 正式independent-review、security-privacy-review与user_acceptance均Pending；原Deferred导致官方Offer登记拒绝保持，不写机器Passed/ManagedByParent或旧D subject作为本轮绑定。
- 真实数据验证限定一日及表入口/有限原始记录；不进行全历史数据审计。all_issues三级仅用8个桶作运行交叉核对，完整统计逻辑以当前SQL逐行审读补充，不声称全库数据正确。

所有确认问题仍Open；本轮只读审查不修复。正式人类门禁和用户验收Pending。下一步是同范围返修、保存新交付，再以新版本从0开始完整复审；不能用本轮或旧D版累计干净轮次。
