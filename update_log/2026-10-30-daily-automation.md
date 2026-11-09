# 日期化日报与每日生成skill

变更时间：2026-10-30T17:25:17+08:00（Asia/Shanghai）。任务：T-INSIGHTS-DAILY-AUTO-20261030-01。

## 变更与原因

- insights/daily_board.py：固定报告改为日期目录与有界缓存；默认北京时间今天，缺报与读取错误分开，详情/预览/原件/ZIP按日期和版本隔离；保留原有内网边界、Feature、身份、权限与审计。
- assets/daily-board.js/.css/.html：原生日期框、今天与历史选择、完整未生成状态、URL前进后退与异步代次隔离；原风格和七模块顺序保留；新日报正文总结与关注从本日editorial读取，不复制10月29日。
- insights/daily_generation.py：只读本地冻结、真实RFC引用路径、逐封审阅契约、分组/残余复核、附件与ZIP校验、计数闭合、幂等原子发布；不向HTTP/MCP开放生成写入口。insights/capabilities.py同步生成能力、权限父链与元数据审计定义。
- tests/test_daily_dates.py、test_daily_generation.py：日期/状态/证据边界、完整与失败packet、不可覆盖/同版幂等；相关旧测试保持通过。
- C:/Users/Administrator/.codex/skills/complaint-daily-report/：正式安装10文件skill，完整标准、原文修订映射、契约、两个实用脚本、基准与UI元数据；没有复制客户数据/凭据。
- automation-2“每日客诉日报生成”：工具创建ACTIVE heartbeat并回读，绑定本会话，按系统/客户端北京时间每天00:30生成前一天；未手写定时器文件或重复任务。
- README.md、新需求目录、既有daily-report PRD、治理记录与本日志：补充运行/交接/限制。未改项目命名或原有目录结构，未GitHub推送，未改MCP或原AICS业务。

## 实际验证

- 日期、生成、网络和附件相关37项unittest通过；另3项日志ZIP测试通过，共40项不同测试。JS node --check通过；skill quick_validate通过。
- 已安装脚本实际分页覆盖634条索引，最长正文30714字符分段后逐字重组一致；CLI复用历史日报、阻止未结束的今天，越界work未写文件。已安装10文件与真实邮件/UID指纹扫描无命中。
- 原10月29日SHA未变；634邮件原文/邮箱集合、405原件SHA、35 ZIP的manifest与每个成员实际字节核对通过。
- 回环与10.8.61.200地址：默认今天缺报、历史634封、详情、图片/日志/PDF预览、真实ZIP、非法日期400和版本409全部通过。未从另一台电脑测试。
- 浏览器1280视口：白底、今天空状态无旧表图、历史日期/三个核心指标/模块与9列表、Top10筛107、子问题15封/2日志ZIP入口、无日志禁用、排序选项、原译独立、详情邮箱、18点筛79、快速切日与前进后退通过，控制台无error。未测移动视口。
- 只重启board；serve/mcp/desk父子PID均未变，watch停止且生产读取false。运行与自动化证据保存，尚未实际等到首次定时触发。

## 失败与修正

- 初始化时FP基础要素条数与E04扩展登记不匹配，正式Run前修正并通过校验；没有因此扩大授权。
- 外部skill允许路径误用绝对通配符，守卫明确拒绝后同一复合命令仍初始化了空脚手架。已如实记failure，停止继续写入，经官方Amendment改为同一授权目录前缀并复验通过，新Attempt完成；不隐瞒首次副作用。
- 项目与内置Python均缺PyYAML，quick_validate首次失败；只在本轮私有.runtime/tool-deps装PyYAML6.0.3后验证通过，未改项目venv依赖清单或生产环境。
- 真实本地准备前置检查被DEGRADED状态正确阻断；未改状态绕过。一次内联Python探针引号失败，改为明确脚本local_probe.py并取得只读状态。
- 浏览器首次ZIP探针选到没有日志的子问题，读取不存在链接超时；重新观察确认禁用正确，再选择实际有2日志子问题验证正分支，没有改业务数据。
- 任务阶段切换后旧查询被校验器判为非当前阶段；按官方历史索引流程完整封存旧发布与请求原字节，并使用新阶段查询，不改写旧查询或删失败。

## 限制与恢复

当前本地副本DEGRADED、消息水位2026-10-30 01:13:42北京时间，未来完整日报仍依赖重新授权恢复采集后READY和日终水位。保持未生成，不宣称自动任务已发布新日报。未进行独立forward-testing或多轮对抗审查；没有把结构校验等同语义或用户验收通过。

证据：.runtime/daily-automation-20261030/verification.json、browser-verification.json、automation.json、runtime-verification.json、local-source-status.json、installed-skill-manifest.json、tests-A02.log、log-archive-tests.log及today-empty.jpg/history-date.jpg。私有证据不入GitHub。

回滚：按release/runtime-change.md恢复已备份业务文件并只重启board；停用automation-2并撤回skill调用，保留全部历史报告和生产隔离。README本轮仅新增日报说明及修改顶部范围文字，可按本轮局部反向补丁恢复；未声称其有修改前整文件备份。
