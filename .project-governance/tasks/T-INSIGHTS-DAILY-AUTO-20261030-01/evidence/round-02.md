# 独立对抗审查 ROUND-02

- 审查者：新启动只读 Agent `/root/adversarial_round02`；先自行阅读原文、代码并构造合成输入，再核对首轮问题。没有接受实施者完成清单作为结论。
- 实际开始：2026-10-30T19:46:43.6946923+08:00；报告完成：2026-10-30T12:00:59.763448+00:00。交付完成：2026-10-30T11:45:56.303562Z；本轮开始晚于该时间。
- 当前交付：`T-INSIGHTS-DAILY-REPAIR-20261030-01`，状态 `Implemented`，父任务 `T-INSIGHTS-DAILY-AUTO-20261030-01`；用户决定仍为 `Pending`。
- 交付 subject：`81b9ecc01f3680360a139f86173c27904f5004ebb130a30a85b6e5da664b00ea`。实际运行 `get_approval_subject.py` 返回同值；交付 manifest 的全部 28 项 SHA 与当前文件一致，证据 `identity-prior-freeze-results.json`。
- 范围：日期看板、保留的原信/UID/原译/邮箱/附件/全组 ZIP/排序/筛选/底部布局，通用冻结—审阅—检查—发布，安装 skill 十个文件与自动化配置。工程根为 `D:/LFEN_project/dev_project/complaint-insights`；没有触碰邻接 AI客诉系统。
- 使用技能：`run-governed-product-workflow`（完整读取 verify，按原话逐项核对）、`complaint-daily-report`（完整 skill、全部引用/脚本/配置/资产）、`computer-use`（独立隐藏浏览器标签，只读交互，完成关闭）。

## 结论

本轮覆盖约定范围，确认 4 个问题，不能计为干净轮次。首轮 4 个问题在当前交付中均已独立复验修复。主流程前向执行成功，但不消除失败恢复和输入矛盾的缺口。

本报告只说明本轮实际检查的结果，不声称绝对无缺陷，不代替用户 Acceptance，不批准访问生产或修改正式历史报告。

## 直接读取的原文及适用边界

以下原件均由本 Agent 完整读取，而非只读取派生任务卡或上一轮报告：

1. `LG_project_docs/requirements/T-INSIGHTS-DAILY-AUTO-20261030-01/requirements/source.md`（下称 A）。日期、缺报、保持风格、汇总并安装 skill、最终每天 00:30 生成前日、优先本会话。
2. `LG_project_docs/requirements/T-INSIGHTS-DAILY-20261030-01/requirements/source.md`（下称 D）。Cursor 来源、生产隔离、本地副本、3030、完整逐封分析、Top10、摘要、元数据、邮箱、增长率、UID、附件与原译等。
3. 同需求 `requirements/steering.md`（下称 S）。UID/送达邮箱、两次视觉参考、白底、主层过细和未知过多纠偏、独立归类、MCP 另开会话。
4. `LG_project_docs/requirements/T-INSIGHTS-DAILY-REPAIR-20261030-01/requirements/source.md` 与 `.runtime/daily-automation-20261030/default-date-steering.json`（下称 R）。明确覆盖最初的“默认今天”。
5. 已安装 skill 全部十个文件；并读了它列出的表格/ZIP、筛选和底部布局日志，以核对最终细节。技能是本次被审查交付的一部分，不反过来取代用户原话。

关键条件原句完整保留如下，后表按同句的不同义务拆项：

> A：“请让这个2026年10月29的课书日报这个日期可以被更改，然后默认展示今天的，默认展示今天的。但是今天的日报还没有制作嘛，所以我需要你做一件事情是什么呢？首先把这个日期选择器给它做好，然后默认展示今天。今天没有出来就显示整个页面显示日报未生成，这样好了。主题风格、颜色配色还是跟原来一致。”

> A：“然后每天，就是每个每天的凌晨一点钟起一个这样的定时任务，每天的凌晨一点钟去将上一天的日报给生成，去将上一天的日报给生成。十二点半嘛，不要一点钟，十二点半嘛，好吧。”

> R：“我已经发现了一个问题，就是今天展示的是昨天的日报。今天展示就是昨天的日报，所以默认今天展示昨天的，而不是今天展示今天的，这个要澄清一下，好吧？要不然的话，永远我看到的都是日报未完成的画面，基本上。”

> D：“我需要的细分的一个客诉日报，请你在今天过后1小时内收集齐所有今天（注意今天的日期）的所有客诉邮件，分析系统给出的分类（主要是三级分类）结合系统给出的分类，你再每一篇都过一遍，总结出更加具体的问题汇总，因为系统的分类可能太聚合，也可能太分散，你需要找到一个平衡，让研发运营能够看得懂的问题描述颗粒度（比如有的分类说有bug，这太宽泛，我要的是具体的这类邮件都反馈比如更新后进不去游戏-又有细分的有储存空间不够，下载进度丢失这样，最终我要一个舆情看板，首先总结top10客诉问题，以及一个总结度高，有参考价值的总结，还有各种问题的上报数量占比图等等，结合一些客诉舆情看板的专业手段，来让你做出来的客诉舆情日报有说服力，总结到位，不遗漏，不偏颇”

> D：“UID可以从整个会话视角去找，只从本封邮件找可能没有但是看该邮件对应的会话就能够看到”

> S：“UID只按原字段和真实邮件链保留证据，业务replyGroupKey不能当会话；兼容游戏UID、当前账号UID等语义字段，主账号/误建账号的不同身份分开表示，不自动择一。表格同时展示发件邮箱和实际送达邮箱，原始To/Cc在侧栏保留。”

> S：“不要用原始问题组呀，cursor会话里面我都说了要自己根据摘要总结归类，很多其实是一种错误，很多是不一样的错误却放到了一起”

> S：“开一个新会话处理MCP相关事宜，本会话继续完成客诉日报看板”

原文关于生产一致性、MCP 介绍/令牌服务/3029 的历史诉求，没有被静默视为本轮已验证：MCP 已明确移交独立会话；生产采集既有隔离尚在，不能以旧快照证明当前线上一致或一小时采集目标。这里检查的是既定隔离边界与阻断行为，未重新连接生产。

## 原文逐条覆盖

证据缩写：E1=`identity-prior-freeze-results.json`；E2=`forward-boundary-results.json`；E3=`live-preservation-results.json`；E4=`browser-evidence.json`；E5=`all-details-previews-results.json`；E6=`regression.log`；E7=`synthetic-fetch-results.json`。全部位于本报告同目录。

|ID|原话/来源中的独立义务|判断|实际证据与差异|
|---|---|---|---|
|A01|A 日期“可以被更改”“日期选择器给它做好”|已实现|E4 日期字段、历史日期下拉、前进/后退实际切换；服务按日期独立命名空间。|
|A02|A 最初默认今天，被 R“默认今天展示昨天的，而不是今天展示今天的”覆盖|已实现|两地址默认 2026-10-29，服务器 `default_date` 同值；标题/日期框是邮件所属日期，昨天按钮返回该日；E3/E4。|
|A03|A“今天没有出来就显示整个页面显示日报未生成”|已实现|显式 2026-10-30、无数据日都无原信/侧栏，显示“日报未生成”；未回填更早报告；E3/E4，`missing-today.png`。|
|A04|A“主题风格、颜色配色还是跟原来一致”|已实现|真实浏览器白底、红紫青绿、全宽、9 列和原模块顺序；`default-layout.png`，E4。|
|A05|A“所有对日报生成的要求…我修改的细节…整个工作流汇总成一个 skill”|部分实现|安装十文件覆盖原文与最终修订；本轮前向可用，但有 R02-01/02/03/04 的工作流边界缺口。|
|A06|A“把这个 skill装载起来”|已实现|固定安装路径存在，十文件逐一完整读取；E1 校对十文件交付 SHA，`run_daily.py build/check/prepare` 实际执行。|
|A07|A 每天凌晨“十二点半…上一天的日报”|配置实现，实际未来运行未宣称|`automation-2` 是 ACTIVE heartbeat，DAILY 00:30，prompt 按执行时 Asia/Shanghai 前一完整自然日；系统 China Standard Time UTC+08。未实际触发调度。|
|A08|A“看能不能把定时任务发送到本会话”|已实现配置|`target_thread_id=01a1866c-6ec4-7f83-9aa8-f75c67aebcf8`，与父会话标识一致；prompt 明确本会话接续。未修改调度。|
|A09|A“生成的质量…十月二十九号靠齐”|主流程成立，边界部分实现|634/405/35 历史版本字节与技能基准保持；前向 7 封覆盖同类合并、异类分离、跟进/咨询/残余；4 个确认问题需修复。不能推导未来语义自动正确。|
|D01|D“请隔离生产库，然后做审查并修复问题后，接续cursor的工作”|边界保持|源码只用目标 reader 入口；本轮未读取真实配置、未连接生产、未启动 watch、未启停服务。既有隔离状态证据只作历史事实。|
|D02|D“昨天邮件问题的客诉日报看板网页，运行在3030”|已实现|3030 回环及既定内网两入口实际返回相同已接受报告和静态资源；E3/E4。|
|D03|D“小量缓慢更新…时效1小时以内”|生成侧有界意图实现，采集时效未达成新证明|冻结源码 reader+repeatable-read、`fetchmany(100)`；不扫生产；E1 mock 冻结和源码。隔离下未声称生产采集 SLA；R02-02 是读取预算缺口。|
|D04|D“原始数据拿到本机后再做复杂聚合”|已实现|`export_snapshot` 后 Agent review、聚合/预览/ZIP均在工作目录；E1/E2/E7。|
|D05|D“测试数据是否完整…和线上一致没有遗漏”|本地完整性成立，线上对账明确未验|假 reader 两视图计数 7=7 放行、7≠8 阻断；634 本地历史保持。未访问线上，不将本地校验表述为生产一致。|
|D06|D 长原句中的“今天过后1小时内收集齐所有今天…所有客诉邮件”|完整日与方向口径实现，实际采集受隔离限制|北京时间自然日 RECEIVED；today 未结束拒绝、旧水位/DEGRADED 拒绝；E1/E2/E6。00:30 是触发时间，非保证完成。|
|D07|D“你再每一篇都过一遍”“注意…每一篇邮件，不要遗漏”|主流程实现，长元数据反例部分失败|review 与冻结 PK 精确集合匹配、缺审阅拒绝，7 封+必要历史均已读；长主题会突破预算，见 R02-02。|
|D08|D“系统分类可以作为一个参考，特别是三级问题组分类”及 S“不要用原始问题组”|已实现|独立 main/sub 决策键，不以源三级聚合；原分类只留复查字段。新合成分类未复制旧答案；E2。|
|D09|D 平衡研发/运营可读粒度，S“总结一句话就是搞的太细了”|主流程实现|基准16业务主类；合成黑屏3封同主同子，设备容量、账号关联另主；没有按原始分类凑组；E2。|
|D10|S“很多其实是一种错误，很多是不一样的错误却放到了一起”|主流程实现|101/102不同说法合并；103真实链补件归回；106与黑屏分开。当前同sub ID异名、同domain ID异名拒绝；E1/E2。|
|D11|D“首先总结top10客诉问题”|部分实现|历史Top10 107/96/55/54/51/39/36/34/33/25；新报告按rank_count及全量分母。不足10显示真实类。但状态/scope矛盾可入榜，R02-01。|
|D12|D“一个总结度高，有参考价值的总结…有说服力…不偏颇”|已实现方法与前向例，不保证未来结论|新例按本日7封独立写 summary/attention 并列证据；既有版结论保留；建议与事实、邮件数与玩家/事故数分开；E2/E4。|
|D13|D“各种问题的上报数量占比图”|已实现|领域占比、排行全量分母、15日及24小时图；所有组/子组闭合，24小时=634；E3/E4/E6。|
|D14|D“每篇邮件的分析要储存元数据，不要丢失”|已实现保存；复核完整性仍有缺口|新发布目录保留 source/review/quality、每封snapshot/body/review SHA与依据；634详情metadata与历史完全一致。R02-04是检查原始字段漂移缺口。|
|D15|D“每一个问题组都能够在看板看到原始邮件和邮箱信息…展开查看”|已实现展示；校验部分不足|完整遍历16主组和全部子组；634封详情全部字段与历史原件一致；一封实际展开有完整原信/邮箱；E3/E4/E5。R02-04需加强新报告源校验。|
|D16|D“今天相比之前客诉来信数量上的增长率提一嘴”|已实现|日环比+144.8%、前7日均对比+108.9%；零/缺失基准返回不可比较，未舍入均值计算；E3/E4/E6、`statistics`源码。|
|D17|D“可以先开始对已有邮件做处理，后续更再对增量做处理”|可续接冻结工作，未宣称重开生产增量|prepare 已有冻结source可resume；既有正式报告校验后原样复用。新日期数据不足保持blocked，不以旧日替代。|
|D18|D“图表…专业好看的…丰富性和美观性”|保留最终接受样式|离线ECharts SVG图，截图人工可视核对；小时柱点击18时实际79封；E4。审美判断不以HTTP200替代。|
|D19|D“识别出来的UID字段加一列”及最终“UID放第一列”|已实现|9列表第一列UID/依据，143单值与7多账号冲突分开；详情有证据；E4/E5。|
|D20|D“专门的统计字段…不只是在摘要中”|已实现工作规则|读 ai_fields 与原文字段；结构化UID只能作候选，单值仍须真实正文/主题证据。合成直接文本、多账号和无UID三支均执行。|
|D21|D UID从整个会话视角；S禁止replyGroupKey替代会话|已实现|合成103经唯一RFC链900继承98765432；无真实链、跨采集邮箱、重复Message-ID反例拒绝；E2/E6。|
|D22|S“主账号/误建账号…分开表示，不自动择一”|已实现|105双UID角色original/keep与wrong保留、主值空；UID证据引文每值可追溯；E2。不将UID当PK或IMAP UID。|
|D23|S“发件邮箱有记录，送达邮箱也要有记录”|已实现|表格同时显示from/mailbox；synthetic原To刻意与mailbox不同，输出分别保留；634详情from/mailbox精确一致；E2/E4/E5。|
|D24|S“原始To/Cc在侧栏保留”|展示已实现，审计部分不足|UI优先recipients_original；634原件展示保持。新候选原To能漂移而check仍过，R02-04。旧to展示归一化不要求等于冻结raw。|
|D25|D“不要用画布，直接出一个html单页网页程序”|已实现|本地HTML/CSS/JS单页；图表renderer=svg，未使用Canvas产物；源码与截图。|
|D26|D“系统没有出摘要你自己出，不允许出现没有摘要的邮件”|已实现|历史634均非空、134源缺摘要已补；新7封源摘要均空，本次逐封创作；空摘要反例E6拒绝。|
|D27|D“log和图片以及其他文档…加到数据表格中”|已实现|三独立列，完整附件405原件；E3/E4/E5，前向4附件。|
|D28|D“主题和正文还有翻译…切换原文和译文的按钮在这两列中”|已实现|主题/正文分别切换；详情主题切译不污染列表；源译/补译来源分开，缺译显式提示；E4/E5。|
|D29|D“log和图片要预览，一张或者一个文件预览就行，点击后打开侧边栏展示所有”|已实现当前版本|271图、86文本、1PDF预览文件存在；43视频/4其他下载边界明确；真实类型HTTP206读字节；一封详情5附件显示齐全；E4/E5。|
|D30|D“横跨整个屏幕，不要居中，占满屏幕”|已实现|workspace宽1265等于body可用宽1265，无居中max-width；E4截图。|
|D31|S 最新HTML2替换HTML1，只参考视觉，不引入mock数据|已实现保留|白底配色、紧凑边框、布局与已接受版本一致；报告SHA没有改变；未执行参考HTML脚本。|
|D32|S“为什么会有这多信件无法归类…很多都能够定位”|已实现流程与合成例|7封中真实空信1封残余、103补件已通过真实链定位；全部unknown_rechecks与group_reviews结构必需；历史626/8不变。|
|D33|S“每一个类别…不会低于20封…太细了”|已按限定正确实现|20封是粒度参考不强制数量；合成低量仍真实3/1/1而非凑20；历史Top10与粒度基准相同。|
|D34|S C-019“读取失败重试（重新载入相同本地报告）”|实现与隔离错误分支核对|503错误不伪装未生成；前端data-retry取当前URL日期重载；E6坏报告用例、源码。未制造真实服务故障。|
|D35|S C-001取消品牌导航，“直接报告标题与正文，不留下隐藏导航控件”|已实现|实际DOM模块以hero开始，白底标题日期，无隐藏品牌导航；E4。|
|D36|D/S MCP文档、令牌生成3029、内网入口，以及“开一个新会话处理MCP相关事宜”|明确不在本轮交付验证范围|完整原话已读；后续明确移交覆盖当前范围。本轮未重启serve/mcp/desk、未改其文档/权限；不冒充其验收。|
|S01|最终去掉时间/主键专列，元数据和PK搜索仍保留|已实现|9列没有时间/PK；#103804精确1封、详情含时间PK；E4/E5。|
|S02|最终四种“有的在前”证据排序，UID首列|已实现|真实浏览器每种排序7页，均634唯一ID；逐项与固定优先顺序及时间/PK兜底比较完全相同；E3/E4。|
|S03|最终子问题日志ZIP入口与筛选工具条结合，打包整个子组|已实现原发布版本|“登录或账号验证失败”3封6日志，搜索无结果后入口仍6个且同date/version；本地35ZIP逐成员SHA校验；E3/E4。|
|S04|最终搜索和筛选行更新、主/子/领域/口径/重置/分页有效|已实现|16主组与全部子组UI覆盖及计数闭合、Top10自动complaint、搜索/重置、25/100分页；E3/E4。|
|S05|最终删除长资产定义和页尾工程解释、压缩底部空白|已实现|无旧footer、无重新渲染长定义，workspace底边20px；源码和E4。|
|S06|最终后三指标和两图下移原信/分页之后|已实现|DOM顺序hero→结论→核心3→排行→原信→补充3→两图；E4。|
|W01|闭日冻结须READY、消息与辅助水位覆盖日终，数据不足不是0封|已实现|READY完整假连接允许；DEGRADED/水位不足拒绝；真实零封独立空review由E6验证；E1/E2。|
|W02|一事务读取邮件/附件/分类/基线，冻结与逐封/渲染集合一致|已实现结构检查|`target_connection(reader=True)`源码只读repeatable-read；mock真实export9查询、7=7冻结、7≠8拒绝；review漏封拒绝；E1/E2。|
|W03|有界完整分页、HTML-only与必要历史都读|部分实现|7封及历史完整batch阅读；HTML脚本/style剔除。长主题仍超预算并推进offset，R02-02。|
|W04|每封先总结、再归主/子、全部主组和unknown复核|已实现流程与本例|`author_review.py`显式创作7封依据和组复核；无关键词分类器；E2/E6。机器不能证明未来Agent确实读懂全文。|
|W05|只读IMAPS/TLS、EXAMINE、BODY.PEEK、UIDVALIDITY/Message-ID/MIME摘要|已实现本机代码与mock分支|真实fetcher消费自建EML，mock网络，4/4下载；第二次不再构建连接；调用只有readonly select/UID FETCH/BODY.PEEK/logout；E7。未实际访问邮箱。|
|W06|附件缺失/摘要不符不发布；子组日志全量ZIP|已实现主路径|4附件真字节/来源manifest绑定；合成ZIP3原日志；E6缺失/篡改反例拒绝；E2/E7。但已发布目录重复校验见R02-03。|
|W07|新日期原子发布，日常不改代码/不重启，来源/审阅持久化|已实现主路径|TemporaryDirectory内staging→rename，最终完整四文件/原件/ZIP，遗留staging空；日期发现无需重启E6；从未向正式目录publish。|
|W08|同日已存在校验后复用、不得覆盖历史|部分实现|安装prepare 2026-10-29实际already_published、原报告SHA不变；同字节重复publish正常；但目的原件损坏仍回already_published，R02-03。|
|W09|check须源身份/原信/邮箱与附件ZIP完整可追溯|部分实现|正文/from/mailbox与文件SHA检查存在；原主题与原始To漂移仍validated，R02-04。|
|W10|能力目录、权限完整父链、Feature/身份/资源/审计|已实现当前源码；旧API进程不冒称已热更新|generate→admin→insights；只本机操作者，无HTTP/MCP写路由。5组禁用状态正确；board Host/Origin/peer/read-only/version测试通过；E1/E3/E6。|
|W11|发布后所选日期、缓存/侧栏清空、旧异步不回填|已实现检查|浏览器缺报/昨天/前后退，回到634、25行、空侧栏；源码有AbortController+generation校验；E4。未进行网络调度层的精确乱序注入。|
|W12|通知遵循自动化、不重复调度、不以触发等于成功|已实现配置/运行约定|prompt同原因未变阻塞静默、成功/新失败/变化/需要处理才报告；ACTIVE只一项，未创建重复任务；技能记录阻塞而非假成功。|

## 新发现问题

### R02-01（P2）：显式非客诉状态与scope矛盾仍入榜并发布

**依据。** 安装最终标准明确“已解决/纯致谢、纯咨询/正常申请、商务通知、真正残余不入Top10”，“纯愿望建议不因被放在可榜主类就自动计为客诉”。这也是避免偏颇、真实Top10的组成要求。不是要求脚本理解任意自然语言，而是要求已经声明的受控状态与计数口径保持一致。

**复现。** `verify_forward_and_boundaries.py` 对101分别设四段全新原文：已经修复仅致谢、正常操作咨询无故障、机构营销合作、尚未体验只希望新增功能；`mail_status`依次为`resolved/inquiry/notice/suggestion`，摘要与状态吻合，分类证据来自当前真实subject，UID不再任取旧值。故意把`scope`填成`complaint`，主类仍为可入榜业务类。

**预期/实际。** 预期拒绝矛盾review或明确排除该行rank。实际四组都`validated`、隔离`published`，总rank=5；同样原文仅修正scope为`non_complaint`后正常发布，总rank=4。详见E2 `status-*`与`status-*-correct-scope`成对结果，合成source/review/report均在`cases/`。

**位置。** `insights/daily_generation.py:304`只校验scope/status枚举，315只限制主组是否eligible；`insights/daily_report.py:224`仅用scope累加，255直接当rank。`audit_report`也未交叉校验。

**影响/建议。** 一次字段误填即可把已解决/正常咨询/商务/纯建议公开算入客诉和Top10。为明确非客诉状态建立一致性判据，build与check同时拒绝；mixed/new/follow_up/materials不应被粗暴全禁，仍由逐封语义判断并保留正例。本发现独立复现后与协调者提供的状态探针同向；未直接采纳其结论。

### R02-02（P2）：长主题突破read_packet预算且未安排主题分页

**复现。** 自建冻结packet第一封主题为32005字符，执行安装脚本`read_packet.py --mode batch --max-chars 1000 --limit 1`，输入合法（1000在允许预算内）。

**预期/实际。** 预期返回有界索引元信息，并在required_followups要求完整读subject。实际stdout为32665字符，`subject_length=32005`、`body_present=false`，`next_offset=1`；followups只有body/translation/ai_fields/headers/attachments，没有subject。`long-subject/source.json`及E2 `reader_long_subject`保留输入/输出统计。

**位置。** 安装`script/read_packet.py`的真实路径为`C:/Users/Administrator/.codex/skills/complaint-daily-report/scripts/read_packet.py:36`、56–61；fallback仍调用含完整subject/summary的basic，未对fallback重新预算。

**影响/建议。** 默认18000/最大24000预算同样不足以包住32005主题，宿主截断时仍推进下一封。它不证明已经漏读真实邮件，但直接破坏完整有界阅读契约。按字段分页subject、source summary及其他无界元数据；不能只是截断后静默丢弃。保留普通批次和长正文正例，并校验每个被移出批次的字段有完整续读路径。

### R02-03（P2）：重复publish只核对report字节，不复核已发布完整目录

**复现。** 从正确7封工作目录向TemporaryDirectory发布；把目的目录`attachments/50101.bin`改为`corrupt-after-publication`；保持工作目录和目的report字节完全不变，再调用`publish(work, temp_reports_root)`。

**预期/实际。** 预期检测目的目录附件损坏并阻断，保护不可变历史，要求显式修复。实际返回`status=already_published`，附件数量仍报4、ZIP数量仍报1，未检测目的原件损坏。原始及重复正常分支均执行，E2 `republish-existing-corrupt-original`记录反例。

**位置。** `insights/daily_generation.py:500–512`先audit工作目录，509–512在目的report相同时直接返回，没有audit目的目录。

**影响/建议。** 失败恢复/重试可以报告一个不完整既有版本“复用成功”。对目的目录先验证源/审阅/质量/所有必需附件与ZIP，再判断幂等；损坏时拒绝，不自动覆盖或删除历史。本反例没有损坏任何正式报告，TemporaryDirectory已清理。

### R02-04（P2）：check带snapshot仍接受原始主题和原始To漂移

**复现。** 正常assemble后，在隔离候选report的101行把`subject`换成`Subject from a different mail`，同时把`recipients_original`换成错误地址（也同步备用`to`）。原始source不改。实际运行安装入口`run_daily.py check --report .../cases/report-subject-drift/report.json --snapshot .../source.json`。

**预期/实际。** 预期拒绝原始主题/原始邮件头与冻结证据不一致。实际返回`validated`、退出0；原始字段已变而source SHA仍绑定旧source。E2最后一例及`cases/report-subject-drift/`保留完整文件。

**位置。** `insights/daily_generation.py:477–485`源比对仅检查body/from/mailbox，没有subject/recipients_original/cc等原始头字段。

**边界。** 这里确认的是原始证据校验缺口；没有修改quality以绕过publish绑定，也不声称这个被改候选可以直接发布。旧基准`to`为展示归一化，不要求与冻结raw逐字相同；应检查实际展示优先读取的`recipients_original`。不修改已接受历史报告。

**建议。** 对新增报告校验冻结原始主题与原始头；对历史兼容保留明确投影语义。补正反例：原始字段不同应拒绝，合法旧展示to归一化不应被误拦。

## 小型前向执行记录

这是本轮从新合成邮件出发的实际执行，不是复制原日报分类答案：

1. `create_packet.py`创建2026-10-27的7封完整新邮件、1封必要历史、4个实际附件；原To刻意不同于采集mailbox；HTML-only带script/style，附件含日志与PNG。源SHA=`c790ac20dea24633a8581557c3faaea6e39268845d234e25d2d1b24bea3fe5b4`。
2. 用安装`read_packet.py`完整读day批次与context，均`next_offset=null`，7封源正文和历史原文在工具返回中全部出现；没有未完成正文分页。阅读自建实际附件字节和日志内容。
3. `fetch_synthetic.py`调用真实下载器，但IMAP构造器被mock为消费自建EML；无网络/真实凭据。真实MIME part/SHA和readonly命令路径执行，4/4 ready；重复执行未再次建连接；E7。
4. 本Agent基于已读内容逐封形成`author_review.py`和`forward-work/review.json`，不是关键词分类：101/102不同说法同黑屏；103有真实RFC链900，补件回黑屏并继承UID；104明确纯咨询；105原/误建账号两个角色；106设备容量HTML-only；107真实空信保留残余。完整主组与unknown复核、当日editorial均有依据。
5. 安装`run_daily.py build`与`check`实际成功：7封、4附件、1ZIP，report SHA=`7a4561db1366b9f930aba1186c51c34d8778aebe34eb9ac65b9228ac6be64f8f`。
6. `verify_forward_and_boundaries.py`只向TemporaryDirectory调用真实publish；正常第一次published、第二次already_published；报告目录source/review/quality均保留。TestClient使用同一board代码检查日期/详情/预览/ZIP，3日志成员、会话UID、多账号空单值、HTML可见文本、错误版本409、私有source404均符合预期；E2。Temp发布目录清理，持久证据仍在review-02。
7. `verify_identity_and_prior_fixes.py`额外以fake本地reader调用真实export_snapshot：7=7冻结，7≠8阻断，reader=True、owner=False。事务read_only/repeatable-read由`db.py`源码确认；本测试没有实际连接数据库，不能冒称真DB事务执行。

复现入口（项目根、设置`PYTHONDONTWRITEBYTECODE=1`，均只写review-02或TemporaryDirectory）：

```powershell
& '.venv/Scripts/python.exe' '.runtime/daily-automation-20261030/review-02/create_packet.py'
& '.venv/Scripts/python.exe' '.runtime/daily-automation-20261030/review-02/fetch_synthetic.py'
& '.venv/Scripts/python.exe' '.runtime/daily-automation-20261030/review-02/author_review.py'
& '.venv/Scripts/python.exe' 'C:/Users/Administrator/.codex/skills/complaint-daily-report/scripts/run_daily.py' build --work '.runtime/daily-automation-20261030/review-02/forward-work'
& '.venv/Scripts/python.exe' 'C:/Users/Administrator/.codex/skills/complaint-daily-report/scripts/run_daily.py' check --report '.runtime/daily-automation-20261030/review-02/forward-work/report.json' --snapshot '.runtime/daily-automation-20261030/review-02/forward-work/source.json'
& '.venv/Scripts/python.exe' '.runtime/daily-automation-20261030/review-02/verify_forward_and_boundaries.py'
```

上述执行证明当前方法可运行，并揭示已列反例；不证明未来每一封的语义质量。新Agent仍须真正逐封阅读和复核，不得把布尔字段或脚本通过当作语义证明。

## 首轮4项修复的独立处置

本轮先完成自己的核心阅读/反例/前向，再查看首轮4个ID，用来核对处置；没有从首轮结论反推本轮无问题。

|首轮ID|本轮观察|处置|
|---|---|---|
|ADV-INIT-01 子问题同ID异名静默并组|本轮不同sub_name共用sub_id抛`SUBGROUP_IDENTITY_CONFLICT:102`；正常前向同ID同名合并，真正不同问题分开；E2|Fixed，绑定当前81b9交付|
|ADV-INIT-02 领域同ID异名|自建两个定义共用entry-update但domain_name不同，抛`DOMAIN_IDENTITY_CONFLICT:entry-update`；正常前向同领域一致、跨领域可导航；E1|Fixed，绑定当前81b9交付|
|ADV-INIT-03 日期重载控件25但实际100|浏览器先100完成全部排序，切今日缺报再昨天，控件25且实际25行、1/26；前后退加载完同样25；E4 returnedReady/forwardReady|Fixed，绑定当前81b9交付|
|ADV-INIT-04 生成关闭或副本异常仍enabled|独立调用真实capabilities endpoint，分别开关0、DEGRADED、version0、辅助水位不足、READY完整，前4禁用且原因明确、最后启用；invocation始终local_os_operator_only；E1|Fixed为当前源码；不声称旧API运行进程已热更新|

## 实际验证汇总与限制

- 47项相关测试真实执行，1.389秒，全部通过；范围为daily_generation/dates/report/network/log_archive；日志E6。没有运行连接数据库的integration测试。
- 既有report SHA保持`b2658daf25058d0ce07ee620d60266039998b5c767ddd0d81721698b3de93760`；634封、405原附件（985048369字节）、35ZIP的本地SHA及ZIP每成员实际字节均经audit检查。HTTP没有重复传输近1GB原件。
- 634个真实详情HTTP逐个读回，主题/正文/原译/UID/收发/To/Cc/files/metadata与已接受报告逐项相等；271图片、86文本、1PDF已准备预览存在，43视频与4其他类型各类代表实际返回字节。数据是私有本地证据，未上传或输出到公开服务。
- 浏览器使用新隐藏标签；16主组/全部子组数量、四排序各634唯一ID/7页、搜索、原译独立、详情5附件、小时79封、Top10口径、搜索不改变全组ZIP、缺报/昨天/前后退、内网入口均执行。标签已关闭。一次遍历夹具因主组选择会同步领域而跨域selectOption超时，已记录并在每组前reset后完成；这是夹具修正，不是产品缺陷。
- 当前自动化仅核对配置、线程与系统时区，未等待未来00:30真实运行；不把ACTIVE当成已产新日报。生产隔离下未查询新的真实副本状态，没有验证将来水位充足时的真实新日数据；已知DEGRADED证据是既有记录，不冒称本轮实时探测。
- 没有重新判读634封历史邮件的分类语义；本轮核对的是用户已接受版本的完整保真、通用方法与全新小型前向。历史内容未改变；不据此宣称历史语义已得到第二次逐封重新裁决。
- 真实IMAP、真实生产/本地DB事务、断电/跨进程并发发布、真实移动设备、视频各编码完整播放、浏览器精确网络乱序注入没有执行；相关实现/既有测试与受控反例已阅读，以上环境行为不冒称已实测。未发现需通过真实生产操作才能裁决的本轮代码问题。
- 未修改产品、skill、自动化、正式报告及正式治理before/after/run；测试产物只位于review-02，所有实际publish只指向TemporaryDirectory。未启停任何服务。版本校对以E1及当前subject为准，后续返修必须另起新交付，不能沿用本轮的版本判断。

本轮仍有4个确认问题待修复，连续干净轮计数应归零。后续由父任务记录轮次与返修关系；本Agent未写父治理记录。
