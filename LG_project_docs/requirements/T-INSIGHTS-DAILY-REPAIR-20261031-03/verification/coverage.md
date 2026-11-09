# 原文逐项核验

原话与Accepted范围见requirements/source.md；继承原日报全部质量标准，本次只修复第05轮两项确认问题。

## R-001 4封UID按完整原文补current/primary角色及真实引用传播，数值/支持状态/分类/计数/源字段/资源不变；815文件完整归档，候选来源及有限差异校验后原子切换，新SHA仅作确定旧格式兼容，安装skill基准同步

已实现。

- 输入：四封完整current/main语境、真实RFC闭包与829de9当前正式815文件。预期：仅纠正4封角色与来源元数据，完整归档后核验原文/数字/状态/分类/统计/资源并原子切换，skill基准对应新SHA。实际：四封UID等于独立原文提案，其他630封不变；单值140/冲突7/待核验5，634/405/358/35保持；829de9全部815文件按SHA保留，新c5150286候选/正式及坏预览拒绝核验通过。
- 输入：对已完成的新c5150286正式目录再次运行只接受829de9前像的单次修订发布器。预期：在替换前拒绝过期前像，不修改已发布版本或历史。实际：非0退出且正式SHA保持c5150286，失败发生于任何候选预览或正式替换之前，日志留存。

证据：`.runtime/daily-automation-20261030/publication-repair/uid-revision.json`、`.runtime/daily-automation-20261030/publication-repair/revision-published.json`、`.runtime/daily-automation-20261030/publication-repair/uid-http-verification.json`、`.runtime/daily-automation-20261030/publication-repair/stale-publication-rejection.log`、`.runtime/daily-automation-20261030/review-05/role-proposals.json`。

## R-002 首次发布必须拒绝缺失、错快照、非ready或身份未核验的附件清单；完整合法输入及零附件输入正常发布和复用

已实现。

- 输入：完整9封/2附件候选与现有零附件正例。预期：合法首发published，同字节复用already_published；完整证据与正式字节保持。实际：离线正常首发/复用通过且全部字节不变；78项回归包含零附件合法首发/复用正例。
- 输入：build后清单缺失、错source、false/非布尔identity、非ready、缺文件项、错摘要或非法JSON，共8例。预期：阻断首发，日期不可见、不写成功状态，候选不被修改。实际：8例全部GenerationBlocked，无正式日期、成功状态或暂存残留，候选原字节保持。

证据：`.runtime/daily-automation-20261030/publication-repair/tests-A01.json`、`.runtime/daily-automation-20261030/publication-repair/tests-A01.log`、`.runtime/daily-automation-20261030/publication-repair/publication-verification.json`。

## R-003 复制后的私有暂存目录再次执行同一完整校验；复制中证据漂移不得变成可见正式日期或成功状态，保持失败清理、原候选和既有历史字节

已实现。

- 输入：完整证据复制至实际私有reports根的暂存目录。预期：完整校验通过再原子rename，正常报告可用。实际：正常发布published、审计validated、复用already_published通过，正式报告全字节不变。
- 输入：在copytree返回后删除manifest、错绑source或撤回identity，共3例。预期：暂存完整校验拒绝，正式日期不可见、不写成功状态、清理唯一私有暂存，原候选保持。实际：3例全部阻断，未留下正式目录或staging，候选和真实当前报告均未改；相关回归也逐项通过。

证据：`.runtime/daily-automation-20261030/publication-repair/publication-verification.json`、`.runtime/daily-automation-20261030/publication-repair/tests-A01.log`。

## R-004 原反例及新的暂存漂移正反、全部相关回归与当前正式报告资源核验通过；保存可核对的新版本、原文覆盖、真实失败及未验限制，归属父审查

已实现。

- 输入：78项回归、11反例及正常分支、安装skill、14封双地址详情、HTTP与真实GUI、来源及版本清单。预期：保存真实验证、逐项覆盖与新版本归父会话，不冒填首次真实调度/新日报/用户验收或两轮通过。实际：78项0失败/错误/跳过，临时目录无残留；安装10文件/634索引/30714最长正文续页、双地址详情/图片日志PDF/ZIP和日期版本边界通过；GUI当前/主角色可见，重置634/140，默认昨天30日缺报；来源与差异、已知限制和交接已保存。

证据：`.runtime/daily-automation-20261030/publication-repair/verification.json`、`.runtime/daily-automation-20261030/publication-repair/ui-verification.json`、`.runtime/daily-automation-20261030/publication-repair/delivery-manifest.json`、`LG_project_docs/requirements/T-INSIGHTS-DAILY-REPAIR-20261031-03/release/handoff.md`。

限制：10/30真实日报未生成；最近一次本地15433 reader只读连接超时，本次未重测或恢复。生产继续隔离；首次真实00:30触发/成功结果、当前线上全量一致和持续一小时时效未验证。旧API元数据未热部署。当前是工程修复结果，不代表用户最终验收或同版连续两轮通过。
