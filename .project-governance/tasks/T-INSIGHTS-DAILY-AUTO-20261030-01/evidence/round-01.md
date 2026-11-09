# 首轮独立对抗性审查：发现轮

- 审查者：`/root/adversarial_initial`，新启动的只读审查子 Agent。
- 审查时间：2026-10-30；采用实际执行时区时间，详细时间见 JSON 证据。
- 起始交付 subject：`b31680b5864baecf391187fda7a4d498da3e2d5dd1ecfa00ad584d96d5e6eb3b`。
- 工程根：`D:/LFEN_project/dev_project/complaint-insights`。
- 结论：确认 4 项缺陷。另有默认日期需求在本轮被真实用户澄清，实施者正修改交付；本轮不能计为同版干净轮。未向正式日报目录发布合成数据。

## 原文与边界

独立完整读取以下原件后再形成检查项，没有把任务卡或完成清单作为唯一依据：

1. `LG_project_docs/requirements/T-INSIGHTS-DAILY-AUTO-20261030-01/requirements/source.md`：日期可改、默认日期、缺报整页状态、原主题、汇总安装 skill、每日 00:30 生成前日、质量对齐已满意的 10 月 29 日版、优先本会话。
2. `LG_project_docs/requirements/T-INSIGHTS-DAILY-20261030-01/requirements/source.md`：用户指定 Cursor 会话恢复的全部日报要求。
3. 同目录 `requirements/steering.md`：UID/收发邮箱、HTML2 视觉、主问题收敛/子问题细分、源分类只作参考、MCP 分会话的明确修订。
4. `.runtime/daily-automation-20261030/default-date-steering.json`：用户最新原话“今天展示就是昨天的日报，所以默认今天展示昨天的，而不是今天展示今天的”。这是对初始“默认今天”口径的后续覆盖。

用户授权范围是本地日期看板、日报生成方法与安装 skill、00:30 本会话自动化。MCP/令牌台、生产维护、恢复采集不属于本次。未读取任何真实凭据，未连接数据库，未连接生产，未启停服务，未改自动化、业务代码或既有日报。仅在指定私有 review-initial 目录及 TemporaryDirectory 写入审查证据；所有 publish 反例均指向 TemporaryDirectory 的 isolated-published。

## 确认问题

### ADV-INIT-01：相同子问题 ID 的不同名称和表现被静默合并

- 位置：`insights/daily_generation.py:assemble` 调用 `insights/daily_report.py:main_read_model`；后者 children 的 `setdefault` 没有校验既有 `name` 与本封 `subtheme_name` 一致。
- 条件：同一主类下两封分别有“启动黑屏”和“登录授权报错”的独立原文、摘要与依据，但 Agent 输出意外复用了 `sub_id=entry-black-screen`。其 `sub_name` 不同，主组复核明确声明应保留独立子标签。
- 预期：拒绝存在身份冲突的审阅输入，要求修订子问题 ID；不能正式发布已经相互矛盾的读取模型。
- 实际：`assemble` 和 `publish` 都成功。两封记录各自保留不同 subtheme_name，但 `report.subthemes` 只有一个子问题，名称取第一封“启动黑屏”，邮件集合同时包含两种错误。
- 影响：将不同错误静默混入同一子问题，子问题统计和日志 ZIP 随错误 ID 一同聚合，违背“很多是不一样的错误却放到了一起”的明确纠偏。
- 复现：运行本目录 `probe.py`，查看 `probe-results.json` 的 `same_sub_id_different_sub_names`。该文件保留了缺陷修复前的实际 build/publish 结果；不得用返修后重跑覆盖它。

### ADV-INIT-02：领域 ID 与领域名称冲突可正式发布

- 位置：`insights/daily_report.py:main_read_model` 中 domains 的 `setdefault`；新生成器没有在入口约束 domain_id 与 domain_name 的身份关系。
- 条件：两个不同主组都使用 `domain_id=entry-update`，分别声明 domain_name 为“进入游戏与更新”和“付费与账号”。两个名称本身均在允许名单中。
- 预期：同一个领域 ID 必须唯一映射到相同名称与配色，冲突应阻断。
- 实际：`assemble` 和 `publish` 成功。domains 列表只保留第一组名称与颜色，第二组记录/主题仍标“付费与账号”，却被归入 entry-update 的领域筛选与数量。
- 影响：导航、领域占比、颜色和邮件文字相互矛盾，跨领域数据被静默合计；审查用 group count 闭合仍全绿。
- 证据：`probe.py` 与 `probe-results.json` 的 `same_domain_id_different_domain_names`。

### ADV-INIT-03：日期重新载入后，每页数量控件与实际行数不一致

- 位置：`assets/daily-board.js:loadReport` 重置 state 时未处理 pageSize；`shell` 重建 #page-size 固定默认 25；`renderTable` 按旧 state.pageSize 切片。
- 实际操作：在独立隐藏浏览器打开 10 月 29 日报告，将“每页邮件数量”设为 100，再通过“已生成日报”下拉选择同一日期重新加载。
- 预期：要么重置控件和数据为 25，要么保持控件和数据均为 100。
- 实际：重载前 `{pageSize:'100',rows:100,range:'第 1–100 封 · 共 634 封'}`；重载后 `{pageSize:'25',rows:100,range:'第 1–100 封 · 共 634 封'}`。
- 影响：显示的分页设置和实际分页不一致；用户随后翻页时继续按旧 100 计算。跨日期同样走此重建路径。
- 证据：`browser-results.json`、`page-size-mismatch.jpg`。浏览器仅操作本轮新建的隐藏标签页，已关闭，没有操作用户原标签页。

### ADV-INIT-04：新增本地日报生成能力状态错误地显示启用

- 位置：`insights/capabilities.py` 新注册 daily_generation；`insights/api.py:/v1/capabilities` 对全部能力仅用 `data_version>0` 判断启用状态。
- 条件：`INSIGHTS_DAILY_GENERATION_ENABLED=0`，合成状态 `DEGRADED,data_version=1`。
- 预期：生成能力不应声称可执行，应有明确的禁用原因；若该状态接口只描述远端可调用能力，应明确本地生成不属于远程可调用范围。
- 实际：返回 `daily_generation.enabled=true,disabled_reason=null`，而 CLI 对该 feature flag 明确返回 DAILY_GENERATION_DISABLED。
- 影响：新增能力的对外发现状态与实际执行不一致。不是执行越权，HTTP/MCP 没有新增生成写入路由。
- 证据：`capability-probe.py`、`capability-results.json`。仅使用纯合成 Settings、MagicMock 和 endpoint 函数，未加载任何配置文件、未连接任何数据库。

## 原文逐项覆盖

下表是根据上述完整原件独立拆分的检查结果。历史要求的当前适用解释遵循最后的真实修订；早期“过细三级为主导航”等方案不覆盖后续收敛指令。

|编号|原文要求/最后修订的含义|状态及本轮证据|
|---|---|---|
|R01|日期可以更改；最新澄清默认上一自然日的数据所属日期|部分实现：原交付默认当日；真实澄清已收到，父 Agent 正修改，不把修改中版本声称已验证|
|R02|所选日期无报告时整个内容区显示日报未生成|已实现：test_daily_dates 的缺报、日期隔离和错误模型对照；JS renderStatus 保留日期入口并重建整个 main|
|R03|保留既有主题、白色背景、配色及全宽|已实现：实际浏览器 body 背景 rgb(255,255,255)，CSS 明确 light/100% 宽；没有导入参考 mock 数据|
|R04|date URL、历史选择及快速日期切换保持正确状态|部分实现：日期 API、版本隔离和 JS loadGeneration/AbortController 已检查；发现 ADV-INIT-03 分页控件状态不一致|
|R05|3030 显示单页 HTML，已有内网边界不扩展|已实现：daily_board 独立文件读取，没有 HTTP 中的新 DB 查询；test_daily_network 全路径 Host/Origin/真实 peer/只读动词检查通过|
|R06|将历次满意版方法完整汇总成 skill 并安装|已实现但需返修：安装目录有 SKILL.md、4 份 references、2 份 assets、2 脚本和 agents/openai.yaml；旧默认今天口径需随 R01 同步，父 Agent 已知|
|R07|每天最终改为 00:30，生成上一自然日|已配置：automation-2 为 ACTIVE heartbeat，BYHOUR=0/BYMINUTE=30/BYSECOND=0；prompt 及 run_daily.prepare 使用执行时 Shanghai 前一天|
|R08|优先发送到本会话，靠持久工作流保证质量|已配置：target_thread_id=01a1866c-6ec4-7f83-9aa8-f75c67aebcf8；prompt 要求加载已安装 skill，全读标准和方法；不只依赖会话摘要|
|R09|生产库保持隔离；采集小批、复杂分析本地完成|已实现：新生成器仅 target_connection(reader=True)，没有 source_connection/watch；执行契约明确不恢复生产采集；没有本轮真实数据库操作|
|R10|完整 RECEIVED 自然日，非最近24小时；未齐不能充作0|已实现：export-probe.py 的 READY 完整成功，DEGRADED 与旧辅助水位在读邮件前阻断；joined_mail_missing 拒绝；既有零封/闭日对照测试通过|
|R11|逐封过所有邮件、不遗漏，源无摘要自己补|已实现：集合/重复/未审阅/空摘要/空依据均有拒绝测试；skill 强制分页全读，而不是关键词分类；结构检查不宣称已证明语义|
|R12|结合摘要正文自归纳，原三级只参考|已实现：review-contract 的逐封语义创作与引文；assemble 不以源分类作聚合键，original_classification 另存|
|R13|同错误合并，不同错误分开；主层不能太细|部分实现：skill 明确业务主层与具体子层，20封是粒度预期而非配额；ADV-INIT-01/02 表明身份冲突缺少阻断|
|R14|不能大量错误标无法归类，能定位跟进应回到具体问题|已实现为生成规则：unknown 必须逐封复核 subject/plain_and_html/attachments/real_conversation，有具体 reason；跟进状态与主问题分开；不会仅以缺根因拒绝定位|
|R15|每封分析和修订依据持久化，可二次总结审查|已实现：report.records.metadata 的源身份/SHA/版本/审阅者/完整decision/evidence_refs；publish 同目录保存 source/review/quality|
|R16|Top10、邮件封数/占比、增长对照，有依据总结|已实现：rank_count 用 complaint 封数、分母全量，main_read_model/audit 均校验；实际 Top1 107；statistics 的前日/前7日均未舍入与缺失/0基数测试通过|
|R17|跟进、补件、咨询、已解决有正确口径；不把邮件数当玩家/事故数|已实现为规则与显示：scope/mail_status 独立，非客诉类别不得 enter rank；method/页面说明明确一次主计数|
|R18|UID独立列，结构化字段候选结合原文；必要时真实会话补证|已实现：实际9列 UID 第一；直接原文/RFC 引文路径校验；同发件人、thread_id、跨邮箱、参与者不符及伪引文拒绝用例通过|
|R19|多账号/冲突不任取单值；证据不是持有人验证|已实现：reviewed_uid 约束多值 state，不允许冲突选择；角色必须有引文候选；skill/详情明确文本证据边界|
|R20|发件与实际送达均有记录，原To/Cc单独保留|已实现：assemble 与 uid_evidence 绑定 from_address/mailbox；表格两者独立；详情 recipients_original/cc 单独显示|
|R21|主题、正文原译独立切换|已实现：实际只点主题原文后，主题=原文/正文=译文，写入 ui-regression-results.json；源译与Agent补译标来源|
|R22|HTML-only不当空信，邮件HTML不执行|已实现：TextHTML 提取可见文本，忽略script/style；现有测试和真实合成第二封覆盖；渲染文本经过 esc/textContent|
|R23|图片/log/其他文件有独立表列，首个真实预览，侧栏全量|已实现：实际9列表头完整；prepare_files 真实字节、魔数、摘要，图片/PDF/文本/视频/不可预览格式不同状态；既有附件下载/预览测试通过|
|R24|保留全部附件，下载器只读且校验来源身份|已实现：IMAPS EXAMINE/BODY.PEEK、UIDVALIDITY/Message-ID/MIME摘要；测试证实只读/重试缓存；不执行实际外部IMAP连接|
|R25|子问题日志ZIP在筛选组件，覆盖子组全部日志|已实现：实际选“启动加载停滞”有2日志/2信，搜索成0行后 ZIP href 不变；date/v相同，未受搜索/当前页影响；ZIP原件/manifest/路径测试通过|
|R26|去掉时间、PK专列，UID/log/image/其他文件有的优先|已实现：实际9列，无时间和PK专列；compareEvidence 的4种布尔证据优先和稳定兜底；时间PK仍在详情/搜索元数据|
|R27|搜索筛选行更新，领域/主/子/口径/分页/重置可用|部分实现：实际Top1对应complaint筛107；搜索可变0，子组ZIP仍全量；ADV-INIT-03分页设置不同步|
|R28|去掉长资产说明与工程页尾，底部自然间距|已实现：当前 shell 不再输出指定长资产定义与工程 footer；workspace padding-bottom20px，无宽大页尾区|
|R29|后三补充指标与15日/分时两图下移底部|已实现：实际 DOM 顺序 HEADER→日报结论→核心指标→问题排行→原信明细→补充指标→来信趋势与时段；CSS 有窄屏堆叠|
|R30|当日结论与处理建议有价值且对齐10月29质量|已实现为生成契约：editorial summary/attention/evidence_mail_ids 必填且绑定本日；skill 要求逐项语义复核，不用10/29文案代填新日；未来真实日报仍须实际执行本流程|
|R31|日报完整检查、原子发布、幂等且不破坏既有历史|已实现：原子临时目录rename；空报告/损坏/漏审/错SHA拒绝；合成正常publish、相同重复publish与旧日拒绝覆盖测试通过；但 ADV-INIT-01/02 的矛盾输入能发布，须修复|
|R32|新能力注册、权限/状态/审计同步|部分实现：daily_generation注册独立权限父链，无远端写路由，日志metadata-only；ADV-INIT-04 enabled/disabled_reason与实际flag相悖|
|R33|MCP相关另会话，不由本任务扩大访问|符合边界：本轮只读 capabilities 元数据的合成函数，不启停服务或调整MCP/令牌台、网络配置|

## 实际运行验证

1. 独立执行 `python -m unittest tests.test_daily_dates tests.test_daily_generation tests.test_daily_network tests.test_daily_report tests.test_log_archive -v`：40 项全部通过，进程退出 0。该结果只代表已有自动化检查，未覆盖上述新增反例。
2. `probe.py`：两种分类身份冲突均得到 validated 与 published。候选文件仅存在于 TemporaryDirectory，已随测试清理。
3. `export-probe.py`：用本地只读事务 double 走真实 export_snapshot 逻辑，不使用连接 URL。READY 成功且覆盖2封；DEGRADED、旧 auxiliary watermark、raw join漏封分别按预期阻断。详细实际查询次序保存在 export-results.json。
4. `capability-probe.py`：用纯合成配置与MagicMock，确认关闭feature仍显示enabled。
5. 实际浏览器：确认白底、布局顺序、UID第一九列、Top1筛107、子组ZIP无临时筛选限制、主题原文与正文译文独立；确认分页错误。浏览器证据是实际DOM和截图，没有读取应用内部私有状态或用 evaluate 触发业务动作。
6. 静态逐文件检查：daily_board.py、daily_generation.py、daily_report.py相关公共函数、daily-board.js/css、db/config初始化读取模型SQL、安装skill全部工作流文件及automation-2.toml。

## 尚未验证与不能据此宣称的事项

- 本轮没有真实健康副本的 SQL 冻结集成测试；只读事务 double 与已有程序检查不能证明 PostgreSQL 运行时性能或真实数据库权限。生产隔离和禁止凭据读取边界保持。
- 00:30 实际调度时间尚未到，不能声称调度已真实生成新日报。本轮确认保存的ACTIVE时间规则、当前thread绑定和执行prompt；不修改时间制造假触发。
- 本轮没有为新一天人工代写完整真实语义裁决，也没有重新审完634封历史邮件；此轮审查对象是新的生成工作流/安装skill及日期界面，历史分类语义不能凭结构检查证明绝对正确。
- 本轮没有从另一台内网电脑测试；已有localhost实际浏览器与合成peer边界检查不能代替远端设备实测。
- 本轮没有进行移动端实际渲染截图、真实未来跨日边界测试，或全部浏览器键盘无障碍测试。
- 日期新澄清和后续修复未稳定，不能把目前混合时间点证据绑定成“同一最终交付完整干净轮”。完成修复并保存新交付后，必须重新独立覆盖并计数。

以上限制和四项缺陷均已向父 Agent 提交。本文保留首次发现时的实际观察，不使用后来的修复状态反写本轮为无问题。
