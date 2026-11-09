# 第三轮独立只读对抗审查

- 审查者：`/root/adversarial_round03`，新建只读审查子 Agent。
- started_at：`2026-10-30T12:21:59Z`。
- 验证结束：`2026-10-30T12:51:55Z`；报告落盘在验证之后。
- 当前交付：`T-INSIGHTS-DAILY-REPAIR-20261030-02`。
- 交付 completed_at：`2026-10-30T12:20:49.274946Z`，本轮开始晚于交付留档。
- subject_sha256：`7bca1f351e0375a02b8b7432c71f8426b4018fcad32c0c5469c2f38553b4e273`。
- 父任务原文绑定：`ab5e7393462e3376c9e4afc7829f3332da44c9222ce4858279e331b103e3e7cd`。
- 原文条款覆盖：**Complete**；发现 **3 项**，本轮不能计为干净轮次。
- 原文范围内未检查项：无。下文单列生产隔离、首次真实定时触发、旧 API 未热部署及历史语义复读深度的确切限制，不将这些限制包装为真实生成成功。
- 开始和结束核对的 35 项 delivery-manifest 均无漂移；历史报告仍为 `b2658daf25058d0ce07ee620d60266039998b5c767ddd0d81721698b3de93760`。

## 范围、方法与证据身份

仅使用 `D:/LFEN_project/dev_project/complaint-insights`，未读取邻居项目 AOCI，也未修改产品、skill、自动化、正式报告或治理记录。本轮新文件全部在本目录。未连接真实数据库、真实 IMAP 或外部 LLM；未调用 source_connection/watch；未重启服务，未操作 MCP/令牌台，未推送 Git。所有 publish 都显式指向本轮私有 `TemporaryDirectory`，未向真实 `.runtime/daily-reports` 发布。浏览器使用 CUA 新建 hidden IAB 标签；结束时已关闭自建标签。

本轮先独立重读下列完整原文、澄清和标准，再阅读实现并创造前向输入。`independent-judgment.json` 的实际时间 `2026-10-30T12:40:06.336751+00:00` 早于首次读取父 after 历史问题的 `2026-10-30T12:40:23.529039+00:00`。没有把上轮结论作为本轮前提，没有复制上轮报告。

原文来源编号：

| 编号 | 本轮完整重读原件 |
|---|---|
| A | `LG_project_docs/requirements/T-INSIGHTS-DAILY-AUTO-20261030-01/requirements/source.md` |
| B | `LG_project_docs/requirements/T-INSIGHTS-DAILY-20261030-01/requirements/source.md` |
| C | 同需求 `requirements/steering.md`，包括两次视觉参考、全部分类纠偏与 MCP 转交原话 |
| D | 同需求 `prd/daily-report.md`，包括 v2、最终 v3、底部布局、日期及默认日期澄清 |
| E | `LG_project_docs/requirements/T-INSIGHTS-DAILY-REPAIR-20261030-01/requirements/source.md` 与 `.runtime/daily-automation-20261030/default-date-steering.json` |
| F | `LG_project_docs/requirements/T-INSIGHTS-DAILY-REPAIR-20261030-02/requirements/source.md` |
| G | `.runtime/daily-automation-20261030/review-authorization.json` |
| H | 已安装 `complaint-daily-report/SKILL.md`、`agents/openai.yaml`、`references/final-standard.md`、`execution.md`、`review-contract.md`、`source-map.md` 与基准主类/质量资产 |
| V | `run-governed-product-workflow/SKILL.md` 与完整 `commands/verify.md`；CUA 前完整读取 computer-use skill，并遵循工具实时浏览器合同 |

本目录证据简称：

- **VER**：`version-start.json`、`version-end.json`；交付摘要和真实历史指纹。
- **NEW**：`round03_cases.py`、`cases-results.json`、`cases-console.txt`；9 组独立前向案例全部通过。
- **REG**：`run_regression.py`、`regression-results.json`、`regression-console.txt`；53 项测试，0 失败、0 错误、0 跳过；所有临时目录强制位于本轮目录，数据库连接被禁止。
- **WRAP**：`wrapper-prepare.txt`、`wrapper-build.txt`、`wrapper-check.txt`；实际执行已安装 skill 的入口。
- **UI**：`ui-interactions.json`、`ui-expected.json`、`ui-initial.txt`、`ui-initial.png`、`ui-drawer.png`、`ui-missing.png`；真实 3030 页面操作。
- **CACHE**：`preview-cache-counterexample.py`、`preview-cache-results.json`，以及两份持久私有候选目录 `preview-cache-valid-but-unrelated`、`preview-cache-interrupted-empty-jpeg`。
- **SEM**：`semantic-counterexamples.json`、`ui-followup-103439.png`、`ui-script-103108.png`、`ui-script-103665.png`；原信、真实头链、当前读取模型和 CUA 逐图证据。
- **UNKNOWN**：`unknown-reinspection.json`；8 封残余逐项重读结果。
- **OLD**：`historical-findings-read.json`、`prior-finding-probes.py`、`prior-finding-probe-results.json`、`prior-finding-console.txt`；独立判断之后才核对旧问题。

## 实际输入与命令

新日输入由本轮从零撰写，未从最终 report 倒推：2026-10-27 的 11 封原信，含 HTML-only、50,062 字符正文、34,021 字符结构化字段、真实历史 RFC 跟进、未关联同发件人、已解决、咨询、纯建议、空信、多账号角色。Agent 在脚本中逐封写明对象、现象、阶段、状态、摘要、原文引文和归类理由，独立形成 7 个业务定义。该固定小样本不是对未来真实邮件自动分类正确率的证明。

9 个附件使用真实合成字节：日志、PNG、HEIC、PDF、zstd 日志、视频格式说明样本和不支持文档格式。内存 IMAP 模拟 TLS/EXAMINE/BODY.PEEK，未连接服务器。全子组 ZIP 含来自 3 封邮件的 4 个原日志，包含 non_complaint 结案来信，全部成员逐字节匹配原件。

实际主要命令（均在项目根，以项目 Python 执行，设置 `PYTHONDONTWRITEBYTECODE=1`、UTF-8，测试根在本轮目录）：

```powershell
& '.\.venv\Scripts\python.exe' '.runtime/daily-automation-20261030/review-03/round03_cases.py'
& '.\.venv\Scripts\python.exe' '.runtime/daily-automation-20261030/review-03/run_regression.py'
& '.\.venv\Scripts\python.exe' '.runtime/daily-automation-20261030/review-03/preview-cache-counterexample.py'
& '.\.venv\Scripts\python.exe' '.runtime/daily-automation-20261030/review-03/prior-finding-probes.py'
& '.\.venv\Scripts\python.exe' 'C:/Users/Administrator/.codex/skills/complaint-daily-report/scripts/run_daily.py' prepare --date yesterday --work '.runtime/daily-automation-20261030/review-03/wrapper-prepare'
& '.\.venv\Scripts\python.exe' 'C:/Users/Administrator/.codex/skills/complaint-daily-report/scripts/run_daily.py' build --work '.runtime/daily-automation-20261030/review-03/wrapper-work'
& '.\.venv\Scripts\python.exe' 'C:/Users/Administrator/.codex/skills/complaint-daily-report/scripts/run_daily.py' check --report '.runtime/daily-automation-20261030/review-03/wrapper-work/report.json' --snapshot '.runtime/daily-automation-20261030/review-03/wrapper-work/source.json'
```

WRAP 的 prepare 真实返回已发布的 10 月 29 日版本（634/405/35），未连接 reader、未重新生成或改写。build/check 针对本轮新写的 10 月 27 日私有样本，真实返回 11/9/1。publish 的正负分支由 NEW/CACHE 的 Python 接口实际执行，全部使用显式私有临时目录。

初次 NEW 的 205 封冻结反例中，审查脚本把第二次负分支调用写在 mock 之外，先因合成 Settings 无 `validate` 失败，尚未触及数据库。修正审查脚本 mock 范围后完整重跑，9 组通过。初次输出和工作目录保留为 `cases-results-initial.json`、`cases-console-initial.txt`、`forward-work-initial`；未把夹具错误当产品发现。

## 原文逐条穷举状态表

“已实现”表示本轮对应证据支持所述功能或边界；不表示全局无缺陷。“部分实现”逐条列明真实差距。早期 MCP、令牌和生产全量一致性按用户后续原文转交或隔离，不伪报当前完成。

| ID | 原文要求、条件或后续限定 | 状态 | 本轮证据与实际结果 | 缺口 |
|---|---|---|---|---|
| A01 | “首先把这个日期选择器给它做好，然后默认展示今天。”后续 E 明确覆盖默认口径 | 已实现，按最新原话 | UI 可选 10/30；“昨天”回到 10/29；日期框为数据日。NEW/REG 检查北京时间、月/年/闰日边界 | 无；未沿用已被覆盖的默认今天 |
| A02 | “今天没有出来就显示整个页面显示日报未生成，这样好了。” | 已实现 | UI 10/30 缺报时 `#evidence=0`、侧栏为 0，整内容区为“日报未生成”；前进后退仍按所选日 | 无 |
| A03 | “主题风格、颜色配色还是跟原来一致。” | 已实现 | UI 白底 rgb(255,255,255)、全宽 1265/1265；CSS 保持红紫青绿蓝及细边框 | 窄屏堆叠读实现，未调整用户窗口 |
| A04 | “把之前我们所有对日报生成的要求，以及你在上述执行过程中我修改的细节，到最终我们产生这版我满意的这个日报整个的这个工作流汇总成一个 skill，汇总成一个 skill。” | 部分实现 | H 已包含日期、逐封、主子粒度、UID、附件、ZIP、UI、失败和隔离；WRAP 与完整分页独立使用成功 | 实际预览复用存在 R03-PREVIEW-01；历史语义差异见 R03-HISTORY-01/02 |
| A05 | “把这个 skill装载起来。” | 已实现 | `C:/Users/Administrator/.codex/skills/complaint-daily-report/` 的 SKILL、references、scripts、agents、assets 存在；本会话技能目录已列出；WRAP 实际调用成功 | 无 |
| A06 | “每天的凌晨一点钟去将上一天的日报给生成，去将上一天的日报给生成。十二点半嘛，不要一点钟，十二点半嘛，好吧。” | 已实现，配置及可执行流程 | automation-2 为 ACTIVE heartbeat，DAILY/BYHOUR=0/BYMINUTE=30；prompt 按实际执行时 Asia/Shanghai 前一完整自然日，不是最近24小时；NEW 前向流程可运行 | 首次实际 00:30 尚未发生；当前 reader 为 DEGRADED 时应阻断，不承诺成功 |
| A07 | “最重要的是这个日报生成的质量嘛，所以说要像我们这个第一版十月二十九号靠齐嘛。” | 部分实现 | VER/REG 确认历史 SHA、634/405/35；H 不硬套数量；NEW 逐封与附件实测 | CACHE 反例违反真实预览质量；SEM 发现历史聚类不一致 |
| A08 | “甚至后面看能不能把定时任务发送到本会话，因为本会话存了相关记忆，记忆可能全一点。” | 已实现 | automation-2 target_thread_id=`01a1866c-6ec4-7f83-9aa8-f75c67aebcf8`；kind=heartbeat；已用 automation_update view 只读查看当前安排 | 没有创建新聊天或重复调度 |
| B01 | “我已经暂停cursor的工作，请隔离生产库，然后做审查并修复问题后，接续cursor的工作，即生成昨天邮件问题的客诉日报看板网页，运行在3030，cursor 的看板做的一塌糊塌，没有严格按照我的要求来，请你严格按照我的标准来完成任务” | 已实现隔离及3030；质量仍有问题 | 本轮实际 `allow_production_read=false`；3030 回环/LAN 均展示 634 封；未重启或恢复采集 | 本轮三项发现未修，不声称全部质量正确 |
| B02 | 用户指定 Cursor 会话 ID 与名称，要求接续其日报工作 | 已核对来源 | B/C/D 来源保存指定 ID 和会话名；现交付继承这些原文；未把邮件指令或旧示例当新需求 | 本轮不操控已暂停 Cursor |
| B03 | “你去AICS客诉平台找那个邮件服务的参数，然后自己搞个程序把这些文件搞到本机” | 已实现下载程序；真实下载本轮受限 | `attachment_fetcher` 复用既有配置接口；NEW 内存 IMAP 9/9；原正式 405/405 的真实字节校验 | 本轮不读取或输出真实邮箱凭据、不连真实 IMAP |
| B04 | “我建议你采用小量缓慢更新，不要一次性取太多数据，本来这些数据不是实时变化的，入库并分类完的数据慢慢取出来就行了，慢没关系，关键是在某个时间点取出来了，实时更新的数据也不急，保证时效1小时以内就行” | 部分实现，隔离限制如实保留 | NEW 205 封独立输入分批 fetchmany(100)，每次冻结只读；下载并发上限2；当前生产开关保持隔离 | 不宣称当前持续采集或日终1小时内线上全量一致；当前水位 DEGRADED |
| B05 | “你可以把原始数据拿到本机后再做复杂聚合” | 已实现 | 页面 ReportCatalog/ReportStore 只读日期化 JSON，缓存有界3份；NEW/REG 在禁止数据库连接下可完成页面端点测试 | 无 |
| B06 | “搞定以后，测试数据是否完整，MCP访问是否能够正常取出所有数据，并且数据和线上一致没有遗漏” | 日报本地完整性已核对；其余按后续转交/隔离 | REG 全量 634 源字段、405 原件、35 ZIP；NEW 严格集合和水位；C/D 明确 MCP 独立会话 | 未验证当前线上一致；未在本轮访问 MCP |
| B07 | “另外，做一个简单的权限发放网页，生成访问token，虽然是内网网段，但是需要我下发的token才能够实际访问MCP，部署到3029端口，localhost，”及“MCP介绍完整吗” | 按后续原话转交 | C：“开一个新会话处理MCP相关事宜，本会话继续完成客诉日报看板”；本轮未动令牌台、3029或其文档 | 不把另会话工作算成本轮验收 |
| B08 | 要收齐完整自然日全部客诉邮件，在日终后1小时内收集齐 | 完整日冻结已实现；真实时效未验证 | `require_closed_source` 同时验证 READY、message/aux 日终水位；低水位/DEGRADED/数据缺失与真实0封对照；NEW/REG | 隔离状态下不恢复生产来满足时效，也不把失败当0封 |
| B09 | “分析系统给出的分类（主要是三级分类）结合系统给出的分类，你再每一篇都过一遍”及“上面的系统分类可以作为一个参考，特别是三级问题组分类” | 已实现契约与前向行为 | NEW 每封先读原文写决定，source classification 仅复查字段；H 明确禁止原组聚合；源分类未进入主聚合键 | 机器结构校验不能证明全部真实历史语义；SEM 已找到反例 |
| B10 | “注意，你需要过每一篇邮件，不要遗漏”及“这样的总结才是全面的，有依据的” | 覆盖/来源已实现，语义有发现 | REG 634 个源 PK/记录字段闭合；UI 7页100/最后34封，总634且无重复；NEW 11封逐封阅读、遗漏/重复/漏引文负分支拒绝 | 原历史未重新逐封全文重作634次语义裁决，未据此宣称全量语义正确 |
| B11 | “总结出更加具体的问题汇总，因为系统的分类可能太聚合，也可能太分散，你需要找到一个平衡，让研发运营能够看得懂的问题描述颗粒度” | 部分实现 | 全16主组定义与全部子组导航逐组核对；NEW 7业务定义、发生阶段及具体子表现独立保存 | SEM 的同问题跨主类和同错误双子ID不符合要求 |
| B12 | “首先总结top10客诉问题，以及一个总结度高，有参考价值的总结” | 部分实现 | UI Top10可点击、数量/分母正确；新样本按实际6封客诉、不凑10类；editorial 原文绑定 | 两封跟进错主类影响当前历史分组；缓存错误会误导复核 |
| B13 | “还有各种问题的上报数量占比图等等” | 已实现 | 主类/子组/领域计数及share全量校验；UI 领域条、排行量级与15日/24小时 SVG 图；24小时加总634 | 无 |
| B14 | “来让你做出来的客诉舆情日报有说服力，总结到位，不遗漏，不偏颇” | 部分实现 | 口径保留邮件≠玩家/事故、引用≠新反馈、根因不确定；NEW 结案/咨询/建议不入榜 | 历史语义与预览问题见三项发现 |
| B15 | “每篇邮件的分析要储存元数据，不要丢失，以便二次总结或者审查时可以查看” | 已实现 | 正式 source/审阅元数据保留 PK、namespace、版本、正文/SHA、原分类及修订；NEW 保留 source.json/review.json/quality.json/report.json | 已保存元数据本身不等于结论正确 |
| B16 | “每一个问题组都能够在看板看到原始邮件和邮箱信息，方便我复查详细情况）定位相应邮件，这些信息可以放到叠加面板中展开查看” | 已实现 | UI 领域→主→子过滤、详情、To/Cc、完整原文、源分类和UID证据；身份/版本 API 全部实测 | 无 |
| B17 | “记得把今天相比之前客诉来信数量上的增长率提一嘴” | 已实现 | UI 日环比+144.8%、前7均值+108.9%；原数平均2124/7；NEW 前日0与缺基线均为不可比较，非0%/Infinity | 无 |
| B18 | “你可以先开始对已有邮件做处理，后续更再对增量做处理” | 已实现稳定冻结/重用 | 已发布日报校验后复用；冻结已有source不重取；未发布工作可续接；NEW 私有发布与失败恢复成对验证 | 当前不恢复生产增量 |
| B19 | “图表要做出那种专业好看的，选择图表生成工具时要考虑丰富性和美观性” | 已实现 | 本地 ECharts、SVG、领域色与参考2一致，24小时柱可点击，趋势基线标注 | 审美由用户决定，本轮不补造用户验收 |
| B20 | “你要把识别出来的UID字段加一列放进去这也很重要” | 已实现 | UI第一列UID/依据；文本支持、会话支持、多账号、未找到状态与详情保留 | 无 |
| B21 | “我记得有专门的统计字段能够识别出UID的，不只是在摘要中” | 已实现 | H 先看结构化候选再核原文；NEW ai_fields 候选99999999不被自动确认为UID；真实原文值显示，候选与文本证据分开 | 无 |
| B22 | “不要用画布，直接出一个html单页网页程序吧，根据我之前的需求来做” | 已实现 | assets/daily-board.html/css/js 与既有3030读取服务；无新增Next服务、前端CDN或ChatGPT画布 | 无 |
| B23 | “系统没有出摘要你自己出，不允许出现没有摘要的邮件” | 已实现 | 历史634/634摘要、134封源缺摘要已补；NEW 源摘要全空仍有11封独立中文摘要，空摘要负分支阻断 | 无 |
| B24 | “log和图片以及其他文档我不是说也要加到数据表格中吗，你忘了？” | 已实现展示 | UI9列含图片、日志/文本、其他文件；真实图片、日志、PDF、HEIC、MOV、PGP元数据/下载已操作 | 未来候选错误缓存为 R03-PREVIEW-01 |
| B25 | “我记得主题和正文还有翻译的，在生产库里面，所以你最好把翻译也加上，然后提供切换原文和译文的按钮在这两列中” | 已实现 | UI主题原文与正文译文可同时保持；侧栏改为主题译文/正文原文不污染列表；源译文与review-agent有来源标记 | 无 |
| B26 | “log和图片要预览，一张或者一个文件预览就行，点击后打开侧边栏展示所有” | 部分实现 | 历史真实首图/日志与5个附件侧栏已实测；PDF首页1280×1600，HEIC1800×830；视频保留播放控件及编码说明 | 已存在的错误预览会被未来build重签，R03-PREVIEW-01 |
| B27 | “横跨整个屏幕，不要居中，占满屏幕” | 已实现 | UI main宽=viewport=1265；CSS width100%，无居中max-width上限 | 无 |
| B28 | “UID可以从整个会话视角去找，只从本封邮件找可能没有但是看该邮件对应的会话就能够看到” | 已实现，有真实边界 | NEW 102沿唯一RFC历史91借UID成功；同发件人无ref、跨邮箱、错误参与者、重复Message-ID均拒绝；多账号显示空单值及角色 | 不把旧thread/reply_group或相同UID当会话 |
| C01 | “UID的识别存在错误，另外，发件邮箱有记录，送达邮箱也要有记录” | 已实现 | UI表格同时“发/达”；原To显示名在侧栏；NEW 原收件alias与collector分离且各自绑定 | 无 |
| C02 | 结构化UID核对、主账号/误建号分开、不自动择一；业务replyGroupKey不能当会话 | 已实现 | NEW 107两账号角色，主值空；108同sender/thread不继承；uid邮箱与原文引文配对 | 无 |
| C03 | “看板整体风格和配色样式请参照这个来做”及后续“根据最新的这个样式参考来修改吧” | 已实现 | C/D以《日报2.html》替代首参考；白底与红紫青绿；保留全宽、不套1600px上限；不执行参考样例脚本 | 无 |
| C04 | C-019读取失败重试，同一份本地报告重新载入；C-001品牌导航取消 | 已实现，静态/合成故障验证 | JS错误页同URL重试handler；REG损坏模型503；真实正常页无品牌导航；CI仅加载/状态标识 | 未破坏真实服务制造503来点击重试；源码和合成503成对核对 |
| C05 | “为什么会有这多信件无法归类？这明显不合常理，cursor原来的分类根本没有这么散，很多都能够定位” | 已实现方法；残余逐项核对 | H 明确功能可定位不要求根因；UNKNOWN 的8封全文为空/仅UID或日志、无可确认现象；NEW补件102/110归启动而非unknown | 未凭日志中的多个底层错误虚构玩家症状 |
| C06 | “另外为什么这个主题变成暗色了，改成白色北京” | 已实现 | UI白底；meta color-scheme=light；CSS固定light，无dark覆盖 | 无 |
| C07 | “而且按理来说，top10客诉每一个类别的体谅应该都不会低于20封的，你这个top10非常散”“总结一句话就是搞的太细了” | 主层已实现；具体一致性有发现 | 历史Top10 107/96/55/54/51/39/36/34/33/25；NEW11封不硬凑20，主层业务能力、具体表现保留子层 | R03-HISTORY-01/02 |
| C08 | “不要用原始问题组呀，cursor会话里面我都说了要自己根据摘要总结归类，很多其实是一种错误，很多是不一样的错误却放到了一起” | 部分实现 | 主聚合键是review main/sub，原三级只复查；同ID异名负例阻断，不同具体表现独立子ID | 同一脚本初始化弹窗仍双子ID；同切图跟进仍跨父组，SEM |
| C09 | “一些布局和细节（比如表格样式）要针对我刚刚说的需求做适配但是整体审美风格反正就是参照那个文档” | 已实现 | 9列表、收发堆叠、译文按钮、附件预览、标签化筛选、自然页尾；截图留存 | 无 |
| C10 | MCP说明、协议、token优化、内网开放，以及“开一个新会话处理MCP相关事宜，本会话继续完成客诉日报看板” | 按后续原话转交 | 独立会话ID存于C；本轮不把令牌/MCP工作混入日报验收，不增权或开端口 | 不重复审其上线 |
| C11 | 视觉HTML含mock正文/附件/UID；只取视觉不把示例当业务事实或执行其脚本 | 已实现 | 原报告与真实冻结源逐封字段匹配；NEW从自写原信前向生成；安全HTML解析去script/style；页面esc | 无 |
| D01 | 10月29日北京时间全天634封RECEIVED，一封一主组，次问题另列 | 已实现集合和计数 | REG全量来源、统计、主/子/领域闭合；UI分页全集=源PK集，634唯一 | 分类语义有SEM发现 |
| D02 | 区分本封负面反馈、纯咨询/已解决、信息不足；封数不称玩家数/新增事故，不推定根因 | 已实现契约与口径 | NEW complaint6/non_complaint4/unclear1；真实UI68非客诉、8残余；R02-01新对照验证四非客诉状态不得入投诉 | 无 |
| D03 | 保存中文摘要、具体主题、依据、原分类、源主键、版本、审查者及内容摘要 | 已实现 | metadata及source/review保留；REG全文/收发/subject/原To/Cc/时间逐封绑定；详情可查 | 不宣称结构字段能证明语义正确 |
| D04 | 标题→结论→顶部三核心指标→领域及Top10→原信表格/分页→后三指标→两图 | 已实现 | UI region顺序严格为日报结论、核心指标、问题排行、原信明细、补充指标、来信趋势与时段；顶部无多余三项 | 无 |
| D05 | 小屏堆叠；小时点击筛选并返回明细 | 已实现 | CSS max700时kpis/charts单列；UI实际点击15时柱得到36封，显示15:00–16:00并回到明细 | 小屏仅源码审查，未改动窗口尺寸 |
| D06 | 图片/日志真实字节、HEIC离线预览、PDF首页与全原件、视频播放或明示格式、其他安全下载 | 部分实现 | NEW全类型真实合成与端点；UI PDF/HEIC/MOV/签名元数据正确；405原件与35ZIP全量核验 | 候选缓存缺真实性/恢复验证，R03-PREVIEW-01 |
| D07 | 下载只读TLS、EXAMINE、BODY.PEEK；核对UIDVALIDITY、Message-ID、MIME、内容摘要；限定冻结清单，不改库或邮件状态 | 已实现可运行边界 | NEW记录TLS、readonly=True、UID RFC822.SIZE与BODY.PEEK；9/9，重复运行0连接；错误Message-ID/大小拒绝；REG覆盖UIDVALIDITY | 真实IMAP不在本轮授权验证范围 |
| D08 | 只读报告、固定allowlist、Host/Origin/真实客户端、禁止代理头绕过/路径穿越/HTML主动执行 | 已实现 | NEW/REG 200/400/403/404/405/409/503正负分支；未知ID及source/review路由404；CSP/nosniff/no-store；伪造XFF不放行 | 无 |
| D09 | 3030回环限制已由后续用户批准的内网边界覆盖，沿用现有边界不重开 | 已实现 | CUA127.0.0.1与192.168.10.20均634；NEW显式RFC1918允许网段与外部拒绝；未改绑定 | 无 |
| D10 | 保留文件结构和命名，仅职责明确适配器；不引Next或外部前端CDN | 已实现 | 读取现有insights/assets模块；浏览器资源同源；本轮不改产品结构 | 无 |
| D11 | UID仅本封或同采集邮箱、唯一真实RFC链、参与者范围支持，多角色/历史冲突不选单值 | 已实现已测边界 | NEW直接/历史/同sender无ref/跨箱/错误参与者/重复ID成对输入；正文与主题引文确切匹配 | 未把文本支持说成账号持有人核验 |
| D12 | HTML-only参与摘要、全文、译文和归类；plain空不算整封空；源缺译文说明来源 | 已实现 | NEW101从HTML提取设备空间描述，去script；新补译标review-agent；UI未翻译状态、原译独立 | 无 |
| D13 | 线上一致性、持续时效和安全门禁未验不能据此恢复生产；需求方验收Pending | 已如实保留 | allow_production_read=false；root新只读水位证据DEGRADED；未重启任何服务；审查启动Accepted不被当产品验收 | 不宣称线上全量相同或用户已通过 |
| D14 | 最终16业务主类、12可榜为基准；具体故障和原修订保留，rank用complaint_count、导航用count | 已实现机制；历史语义有缺陷 | 全16主组定义/全部子组导航核对，REG计数/分母/排行；NEW source原组与main无关，不硬套16/12 | R03-HISTORY-01/02 |
| D15 | 626/634已归类、8真实残余；跟进/补件与可归类分开，未知根因不阻止功能归类 | 数量/方法已实现 | VER/REG626/8；UNKNOWN逐项核对；NEW102/110具真实问题证据被归类 | 已定位跟进也存在错父组，R03-HISTORY-01 |
| D16 | “请将图中叉掉的部分下移到底部”，不隐藏/删模块、不丢小时筛选和下载 | 已实现 | UI 3补充指标与2图均在分页之后，小时筛选及ZIP实际工作 | 无 |
| E01 | “今天展示就是昨天的日报，所以默认今天展示昨天的，而不是今天展示今天的” | 已实现，覆盖A/D旧今天口径 | 无date页面默认10/29；标题/日期框显示数据日；昨天按钮回默认；REG月年闰日/缺默认日不回退 | 无 |
| E02 | 显式日期仍是数据日；缺报整页、URL保留、切日清筛选/缓存/侧栏、旧异步不得回填 | 已实现 | UI10/30空页、昨天回634且25行、back/forward正确、快速28→29最终634/25/无侧栏；JS generation+abort、detailCache.clear | 未注入网络延迟；实际快速切换及代际守卫源码均核对 |
| H01 | “去掉时间，主键这个列…有没有uid…日志…图片…其他文件分别排序，有的放前面”“UID放第一列” | 已实现 | UI确为9列，UID第一，无时间/PK专列；四排序首25条与独立比较器全部一致；时间/PK在详情，#103804可搜索 | 无 |
| H02 | 默认UID→日志→图片→其他；各证据优先，其余固定兜底，时间/PK稳定排序，非UID数值排序 | 已实现 | UI四模式行ID分别与原报告离线独立比较；634全分页无遗漏/重复；NEW evidence_presence计算 | 无 |
| H03 | “子问题组的log日志批量下载zip入口…和上面的筛选问题组组件结合”及全子组不受搜索/页/小时/口径影响 | 已实现 | UI子问题工具条：无日志明确禁用；有2日志时搜索到0封仍同一日期/版本/allowlist链接；NEW ZIP含3封4日志，含non_complaint；REG35包全成员 | 无 |
| H04 | 无日志或有日志未校验时禁用说明，ZIP含manifest/mail/attachment/原名/大小/SHA，固定ID与版本 | 已实现 | NEW/REG缺日志/损坏日志/未校验正负分支、全成员摘要和安全名称；ZIP缺v/旧v409、未知ID404；权限/Feature关闭拒绝 | 无 |
| H05 | “底部空白太多了，压缩”“这个话去掉”及长资产组说明删除 | 已实现 | CSS workspace页尾20px；真实DOM在图后结束，无工程页尾和长资产定义块；来源指纹在口径/详情 | 无 |
| H06 | “搜索和筛选这一行组件是不是没有更新？更新一下” | 已实现 | UI有标签的搜索、口径、主问题、证据排序、重置；领域→主→子、口径三状态实测 | 无 |
| H07 | 搜索主题、完整正文、摘要、邮箱、UID、邮件编号 | 已实现 | UI6查询全部与原数据集合一致，包括正文200字预览之后独有`up before season 2 or m`；精确PK、UID、发件、送达、中文描述 | 无 |
| H08 | 翻译主题/正文独立，侧栏不污染列表 | 已实现 | UI列表subject:original/body:translated，侧栏drawerSubject:translated/drawerBody:original，返回列表不变 | 无 |
| H09 | 同一只读repeatable-read事务冻结状态、邮件、附件、分类和15日；完整分页和PK严格覆盖 | 已实现可执行契约 | NEW205封从原始合成输入冻结，fetchmany100完整取到末尾、count核对；db.target_connection独立mock验证reader URL、只读及REPEATABLE_READ；无写SQL | 未连接当前真实reader，该项使用内存事务适配与真实代码执行 |
| H10 | READY且message/aux均覆盖日终才能生成；缺数据不能假报0；真实0封也有完整水位证明 | 已实现 | NEW两种水位日终前、空水位、DEGRADED均阻断；合格0封及非0封正分支；REG零邮件组装与发布 | 当前真实水位DEGRADED，下一新真实日不得假报生成 |
| H11 | 全部邮件的源摘要、HTML、必要RFC、结构化字段完整分页；长字段必须续读到末尾 | 已实现 | NEW11封按batch索引到next_offset=null，再逐个required_followups字段到末尾，正文50062/AI34021完整恢复；OLD新长主题与metadata分页实际恢复 | 无 |
| H12 | 全部主组与全部unknown复核，逐封source/review/quality绑定，不以脚本绿灯代替语义 | 部分实现 | NEW全部11封、7定义、1unknown语义创作/横向复核；正式16主组和全部子组结构及8残余重读；本轮确实找到语义反例 | 历史634封未重新逐封全文裁决，不据此宣布其每条语义正确 |
| H13 | 已发布复用必须检查正式目录原件/预览/ZIP/source/review/quality，不覆写/重算历史 | 已实现复用检查；构建缓存另有缺陷 | WRAP真实历史校验复用；OLD新输入删除正式原件、ZIP、review、quality、manifest全部拒绝，恢复后already_published | CACHE是在候选build时重签，区别于复用正式目录校验已修的R02-03 |
| H14 | 日报按日期原子发布完整目录，发布后页面自动发现，无需每天改代码或重启 | 已实现 | NEW私有目录publish→already_published，拷贝检查与冲突保护；REG缺报后目录出现自动发现；真实服务未重启 | 新真实日期尚未发布；未作成功宣称 |
| H15 | Feature/权限完整父链、风险/作用域/动作/审计、服务端身份/资源校验、状态/禁用原因 | 源码及合成已实现，运行部署限制保留 | capabilities父链、daily_generation local_os_operator_only、环境关闭/副本未齐禁用；NEW/REG权限/Feature/审计；生成无HTTP/MCP写入口 | 旧API进程启动早于新metadata；本轮未热部署，不声称运行API已更新 |
| H16 | 定时通知同原因未变化保持安静，成功/新失败/状态变化/需用户处理再报告，不重复调度 | 已实现配置 | automation-2实际prompt写明上述条件、ACTIVE、heartbeat、当前会话；只读view成功；未新增自动化 | 首次实际触发/通知尚未发生 |
| F01 | 同范围审查返修、保留全部历史纠偏，默认昨天，不新开审查或伪造最终验收 | 已遵守 | 本轮只读，不修复、不动父after；独立判断后才读旧问题；当前摘要与授权原件一致 | 返修由root后续任务负责 |
| G01 | 用户真实回答“启动多轮对抗性审查”，同版连续两轮完整无问题才通过 | 已遵守 | G真实原件、父Offer/Accepted存在；本轮新执行者、新开始时间、新报告；三项发现使干净计数为0 | 未预设通过，不把53项通过算审查通过 |

## 全部确认发现

### R03-PREVIEW-01 — P1：错误预览缓存被重新签名并发布

位置：`insights/attachment_preview.py:94`、`:106`、`:126` 仅以 `dest.is_file()` 复用图片/日志/PDF预览；`insights/daily_generation.py:315` 随后为现有预览重新计算 `preview_sha256`。`audit_report` 只比较新签摘要，无法发现缓存不是从当前原件生成。

复现条件：某次中断留下空 JPEG，或工作目录已有其他邮件/旧运行的预览文件；原附件 `.bin` 和已验证 manifest 完全正确。重新执行 build，不能信任“缓存存在”代表真实预览。

本轮独立复现：

1. 在本轮 11 封/9附件的私有 work 副本中，所有原件 SHA 保持不变。
2. 第一组把本来全红的 PNG 对应 JPEG 改成可正常解码的全蓝 JPEG，把真实 `round03 launch evidence` 日志预览改成完全无关文字。
3. 第二组把该 JPEG 截成 0 字节，模拟预览写入中断。
4. 两组 `assemble` 均返回 `validated`，`ready=true`、`preview_type=image`，错误缓存 SHA 被重新签入 report；两组私有 `publish` 均返回 `published`。
5. 第一组原图RGB均值 `[255,0,0]`、被发布预览 `[0,0,254]`；第二组 JPEG 不能解码，但同样发布成功。

预期：基于当前已验证原件重新生成预览，或检测到来源/转换身份/内容不成立而阻断。实际：错误图片、无关日志和不可用图片被当作经过校验的证据发布。

影响：下次新日构建或失败恢复会静默发布错误证据；新摘要只能证明错误缓存自洽，不能证明来源。违反真实字节预览、失败恢复、发布完整性和质量不得退回的要求。CLI拒绝写已发布目录并不能解决候选目录中的此问题。

证据：CACHE。root先提供了缓存边界方向；本轮未读取root探针，使用自己先前独立编写的原信和附件另写脚本、独立执行。该来源关系已保留，不冒充无人提示的发现。

### R03-HISTORY-01 — P2：同一真实会话的切图故障补件被改送启动主类

位置：正式 `2026-10-29/report.json` 的 `records[id=103426/103439/103469]`、对应 `themes`/`subthemes`；原冻结 `source.json` 中同三封邮件的原文与头链。原件 SHA 全程未改。

- 103426 原文明确说加载10%、全息模拟任务和 **map transitions freeze at 10%**；本次主问题为 `main:performance-controls`，子组 `main:performance-controls:complaint:scene-loading-stuck`。其basis明确“主组按明确切图环节，未断言首次启动”。
- 103439 是同采集邮箱、唯一 In-Reply-To 指向103426的真实回复，正文仅引用原信并补图，没有新增“启动阶段”文字；103469继续引用103439/103426并补同SHA截图/录像。
- 103439、103469却在 `main:update-launch`，子组后缀仍为同一个 `complaint:scene-loading-stuck`；summary/basis也仍写“切换地图”。
- CUA已查看103439截图，属于通用10%加载画面，不能据此推翻原信已明确的地图切换阶段。真实头链和源正文已在SEM保存。

预期：本封无新独立现象时，依据已证实的原问题与发生阶段归回同一主类；补图只是状态，不改变业务问题。实际：同一链拆成运行性能1封、启动阻断2封，当前主/子筛选不能完整看到这个问题的全部来信，并把2封计入不对应的主类。

影响：主类路由、Top10主类数量与子问题聚合不一致。此处“跟进不等于unknown”做到了，但“回归可证实原问题”仍不成立。

证据：SEM、CUA截图；103439/103469 References/In-Reply-To 逐字指向前一真实Message-ID，不是以同发件人推断会话。

边界：这是冻结历史报告本来存在、当前页面仍呈现的内容缺陷，非本轮改坏。不能为消除发现覆盖历史原件或改其SHA；后续处置需要可追溯修订或明确记录历史基准的例外边界。本轮没有修复。

### R03-HISTORY-02 — P2：同一脚本初始化错误按显示语言分成两个子问题

位置：正式 `2026-10-29/report.json` 的103108、103665及两个子组。

- 103108 / 附件60159：启动页英文弹窗 `Game scripts failed to initialize. Please restart the game or use Repair.`；子ID为 `main:update-launch:complaint:startup-script-init-failed`，1封。
- 103665 / 附件60414：同一启动画面、同一弹窗的日文“ゲームスクリプトの初期化に失敗しました”，同样要求重启或修复；子ID为 `main:update-launch:complaint:script-initialization-failed`，1封。
- 本轮分别在 CUA 中逐图看到了两张真实图片。业务主类同为启动阻断；差别是语言和设备，不是不同故障现象或处理方向。

预期：同一明确可见错误合为一个稳定子问题，语言/设备留元数据，子问题计数2封。实际：工具条显示“启动时提示游戏脚本初始化失败 · 1”和“启动游戏脚本初始化失败 · 1”两个入口。

影响：同问题规模被拆散、导航重复，违背“很多其实是一种错误”应合并的原话。此项不是旧报告同ID逐封标签别名的兼容问题：这里是两个不同子ID，精确SHA的别名兼容不解决它。

证据：SEM及两张CUA截图。边界同上：不得直接覆盖不可变历史。

## 历史问题处置：先独立判断，再读取父 after

父 after 读取时间晚于独立判断，原件摘要保存在 OLD。本轮不读取或复制上轮报告凑覆盖，使用新的对照输入复验。

| 历史ID | 本轮处置 | 当前交付的新实际证据 |
|---|---|---|
| ADV-INIT-01 | Fixed，维持原已修结论 | NEW合法主/子身份可建；同主组同sub_id异名真实拒绝 `SUBGROUP_IDENTITY_CONFLICT:111`；REG导航label/parent漂移拒绝 |
| ADV-INIT-02 | Fixed，维持原已修结论 | NEW同domain_id异名拒绝 `DOMAIN_IDENTITY_CONFLICT:entry`，不同合法领域可导航；REG配色/标签关系校验 |
| ADV-INIT-03 | Fixed，维持原已修结论 | UI先改100并读完7页，再选缺日报/昨天，真实恢复25行；控件和实际一致 |
| ADV-INIT-04 | Fixed（源码与合成端点；部署限制保留） | NEW关闭开关/DEGRADED/低水位均disabled，合格水位enabled且local_os_operator_only；REG实际API合成状态分支通过；未把旧运行进程说成已更新 |
| R02-01 | **Fixed**，绑定7bca1交付 | OLD对resolved/inquiry/notice/suggestion逐一实际调用：non_complaint放行、complaint全部拒绝 `NON_COMPLAINT_STATUS_SCOPE_CONFLICT`；NEW完整报告已解决/咨询/建议不入榜；REG build/check两处均覆盖 |
| R02-02 | **Fixed**，绑定7bca1交付 | OLD新写600001原信，超长Unicode主题与超长源摘要；index/batch预算1000仅返回稳定ID及明确subject/metadata续读；主题210000字符/53页、metadata32265字符/9页完整恢复；NEW长正文与AI字段也完整分页 |
| R02-03 | **Fixed**，绑定7bca1交付 | OLD私有正式目录分别删除原件、ZIP、review、quality、manifest，完全相同report的再次publish全部blocked；恢复后already_published。NEW正式预览变字节同样blocked。R03-PREVIEW-01发生于候选build重签，不能用本项已修抵消 |
| R02-04 | **Fixed**，绑定7bca1交付 | OLD新报告分别改subject、recipients_original、cc、同小时at，`check --snapshot`语义入口均拒绝 `REPORT_SOURCE_HEADER_MISMATCH`；仅展示to投影改变仍允许；真实历史原To绑定检查通过 |

本轮未决项就是上述3项新发现；没有用“实施者说已修”替代Fixed证据。

## 历史发现的逐封预期修订字段（仅给出审查预期，不授权或执行历史写入）

root要求补充具体修订字段。本节给出可核对的内容预期；采用何种版本化历史修订载体、是否发布及权限边界由root按原授权判断。本轮未改任何正式原件，也未把两项标记为已解决。

### R03-HISTORY-01

| mail_pk | 预期直接字段 | 保留字段与原始证据 | 附件 |
|---|---|---|---|
| 103426 | 无需修改；它提供已明确“地图切换”的原主问题与同链基准 | `main_id=performance-controls`、`theme_id=main:performance-controls`、`theme_name=画面、操作与运行性能`、`domain_id=gameplay-events`、`domain_name=玩法与活动`、`subtheme_id=main:performance-controls:complaint:scene-loading-stuck`、`subtheme_name=切换地图或家园时加载冻结` | 无 |
| 103439 | `main_id: update-launch → performance-controls`；`theme_id: main:update-launch → main:performance-controls`；`theme_name: 更新安装与启动阻断 → 画面、操作与运行性能`；`domain_id: entry-update → gameplay-events`；`domain_name: 进入游戏与更新 → 玩法与活动`；`subtheme_id: main:update-launch:complaint:scene-loading-stuck → main:performance-controls:complaint:scene-loading-stuck` | `scope=complaint`、`mail_status=materials`、`identified=true`、`concrete=true`、相同子问题名称、summary/原文/原To/Cc/时间/UID/原分类/附件身份不变；新修订依据记录真实103426→103439链与未新增启动阶段证据，原decision留为历史 | 60278：JPG |
| 103469 | 与103439相同的6项直接字段映射 | 同上，新增修订依据记103426→103439→103469链及同SHA补图；不把补件改为新事故 | 60297：同SHA JPG；60298：MP4 |

派生变化必须重新计算并以新版本保存：启动阻断 `count/rank_count 107→105`，运行性能 `54→56`；领域进入游戏与更新 `237→235`、玩法与活动 `203→205`；运行性能下 `scene-loading-stuck 6→8`，启动下该子组2封变0并移除空组；总邮件634、客诉总数558、附件405、已归类626/残余8不变。运行性能56将排在账号55之前；Top10的顺序、share、rank_share、mail_ids、scope_counts、search_text和新修订元数据须由最终读取模型重算，不手工改一个数字。

**日志ZIP影响：**这三封均无日志。目标子组现有ZIP `9670a023baa31ca3f5c50a2198bd37e7d1abc2fcd343baceed56f08c81eb2c82` 仅有103405的60254/60255两个日志，`file_count=2/mail_count=1`，两封无日志补件加入不改变该ZIP的原件成员、字节或计数。在源快照SHA、子ID/名称不变的前提下该ZIP摘要/ID应保持；新报告版本的下载URL `v` 必须跟随新报告。原启动子组原本 `log_archive=null`。

### R03-HISTORY-02

采用**已有**103108子ID作归并目标，避免另造新命名：`main:update-launch:complaint:startup-script-init-failed` / “启动时提示游戏脚本初始化失败”。这一目标是审查建议；另一已有ID同样可作为稳定规范值，关键是两封只落同一个子问题且保留语言/设备差异。

| mail_pk | 预期直接字段 | 保留字段 | 附件/ZIP |
|---|---|---|---|
| 103108 | 子ID/名已是上述目标，直接字段无需改 | `mail_status=materials`、主类/领域/scope、英文原图与旧裁决完整保留 | 60159：PNG；无日志，无ZIP |
| 103665 | `subtheme_id: main:update-launch:complaint:script-initialization-failed → main:update-launch:complaint:startup-script-init-failed`；`subtheme_name: 启动游戏脚本初始化失败 → 启动时提示游戏脚本初始化失败` | `mail_status=new_issue`、`main_id=update-launch`、theme/domain/scope/identified/concrete、日文正文/设备/图片证据均不变；原子ID和原decision留在新修订轨迹，不能抹掉历史 | 60414：PNG；无日志，无ZIP |

派生结果为同一子问题 `count=complaint_count=2`、mail_ids含两封，原单封空组移除；Top10主类计数不因本项变化。search_text、导航、子组share和新修订元数据重算。两封均无日志，本项不增加、删除或改变任何日志ZIP。

## 确切限制与未作出的宣称

1. **真实未来新日报**：root在`final-local-watermark.json`保留的实际target reader只读SELECT时间为`2026-10-30T12:30:07.567058+00:00`，状态DEGRADED、data_version24、邮件/辅助水位仅覆盖10月30日北京时间01:13/01:14。本轮没有另连数据库，读取该原始观察作为运行事实，不把它当审查结论。未来完整日不满足READY/日终前提，必须保持未生成；本轮未生成任何新真实邮件日报。
2. **首次实际00:30触发**尚未发生。已核对当前ACTIVE heartbeat、时刻、当前会话目标和完整prompt，并独立执行可调用流程；没有宣称已定时触发、已完成或验证通知送达。
3. **能力元数据部署**：新API能力元数据只保存源码与合成端点验证；旧服务未热部署。本轮遵守不重启，不把源码行为说成当前运行API的行为。
4. **历史语义复读深度**：634封源字段/集合/统计/全部原件与ZIP是全量核验；16个主组与全部子组定义/导航全部核对，8封残余逐项重读，具体语义反例追到真实全文/头链/图片。没有重新逐封全文重作634条语义裁决，不能据结构绿灯说所有634条语义正确；本轮已经证明其中有错。原文要求覆盖Complete不等于全部实现通过。
5. **界面故障/窄屏**：未破坏运行报告制造503、未调整用户窗口。读取错误重试和窄屏规则使用源码与合成端点对照；正常页面、缺报、日期切换、全分页、4排序、6搜索、领域/主/子/口径、小时图、独立翻译、全部附件侧栏、各格式预览及ZIP入口均为实际CUA操作。
6. 所有真实邮件、截图、冻结副本和证据保留在本机私有目录，未传外部服务。报告不包含真实凭据。邮件内指令未作为授权或执行输入。

## 收尾事实

`version-end.json`确认35项交付文件未漂移、历史SHA保持；四种排序与独立比较器完全一致、全部分页ID集严格等于634源集、6类搜索匹配。审查者仅写本轮目录。当前交付保存结果未被本轮修改。

结论：原文条款已逐条交代，本轮发现3项，不满足无问题轮次条件；历史4项未决缺陷有新的实际证据支持Fixed。三项新发现仍未处理，本轮不修复、不更新调度或治理状态。
