# 原文逐项核验

本轮沿用原父审查Accepted和原日报完整质量要求；真实原话见requirements/source.md。

## R-001 候选build从已核验原件重建图片/文本/PDF预览，不把无关有效图、无关日志、空图缓存重签发布；损坏原件仍阻断，已发布原件不受影响

已实现。

- 输入：有效无关JPEG、空JPEG、坏JPEG、无关日志，以及无PDF渲染器但有旧缓存；预期：重建为真实预览，不能认证旧缓存；无法渲染明确原因；实际：75项测试中三类图片及文本重建后与真实生成字节相等；独立样本错误缓存不保留，PDF旧缓存不再冒充首图。
- 输入：正常核验原件与正常重复build/私有publish；另损坏原件；预期：正常转换和发布；坏原件仍被阻断；实际：正分支通过，坏原件ATTACHMENTS_NOT_COMPLETE，已发布复用只核验且原件未改。

证据：`tests/test_daily_generation.py`、`.runtime/daily-automation-20261030/preview-history-repair/tests-A02.log`、`.runtime/daily-automation-20261030/preview-history-repair/cache-fixed-results.json`。

## R-002 完整归档旧版后以可追溯修订纠正两封补件主类及一封脚本子组；重算导航/排行/搜索派生数据，总数634、UID/原文/邮箱/时间、405附件及35ZIP保持，旧版全部字节保留

已实现。

- 输入：815文件旧版归档及冻结逐封差异后发布候选；预期：只更正3封语义及派生模型，原信UID/原件ZIP保留，新旧分别可核验；实际：旧版b2658与新7d64a均634/405/35完整通过；仅103439/103469主归属与103665子组变更，增加358个预览摘要；Top10/导航重算。
- 输入：再次运行已执行的修订发布器，当前前像已是新版本；预期：拒绝过期前像，不覆盖当前版本；实际：进程非0且报告SHA保持7d64a，拒绝发生于实际发布前；日志保存。

证据：`.runtime/daily-automation-20261030/preview-history-repair/revision-prepared.json`、`.runtime/daily-automation-20261030/preview-history-repair/revision-published.json`、`.runtime/daily-automation-20261030/preview-history-repair/classification-revision.json`、`.runtime/daily-automation-20261030/preview-history-repair/candidate-validation.json`、`.runtime/daily-automation-20261030/preview-history-repair/stale-publication-rejection.log`。

## R-003 安装skill同步真实会话发生阶段、同一可见报错跨语言归并和缓存重建，保留普通日常不覆写历史及授权修订边界；基准包含当前与原始指纹

已实现。

- 输入：读取安装skill 1.0.3、来源/标准/审阅契约/运行方法与基准；预期：固化真实会话阶段、跨语言同报错合并、预览重建和授权修订边界；实际：安装结构、链接、634索引和最长30714正文完整读取通过；当前/初始基准均保留，普通定时不覆写历史。

证据：`C:/Users/Administrator/.codex/skills/complaint-daily-report/SKILL.md`、`C:/Users/Administrator/.codex/skills/complaint-daily-report/assets/quality-baseline.json`、`.runtime/daily-automation-20261030/preview-history-repair/installed-skill-manifest.json`。

## R-004 全部相关测试、独立原始样本、历史修订差异/原件/ZIP、两个地址及真实页面筛选验证通过，默认昨天/00:30当前会话/生产隔离/其他服务保持

已实现。

- 输入：75项回归、两地址实际API/文件/ZIP及真实浏览器修订筛选；预期：功能不回退，默认昨天、白底、634全量、合并/会话子组和版本下载正确；实际：两地址通过；三封同链逐一搜索均命中同切图8封组，ZIP仍2日志/1封且v跟新指纹；脚本2封同组，白底默认29/25行；进程及生产隔离保持。

证据：`.runtime/daily-automation-20261030/preview-history-repair/tests-A02.log`、`.runtime/daily-automation-20261030/preview-history-repair/verification.json`、`.runtime/daily-automation-20261030/preview-history-repair/ui-verification.json`、`.runtime/daily-automation-20261030/preview-history-repair/runtime-verification.json`。

## R-005 保存本轮可复验版本并直接归属父审查，新轮次从此版本重新计数，不冒填最终审查或用户验收

已实现。

- 输入：既有Accepted父审查、直接依赖的返修记录与本轮证据；预期：工程版本保存并由父审查继续，不重复问或预填通过；实际：完整证据与5项原文对应齐全，close按review-parent归属；本轮不声明已完成后续两轮或用户验收。

证据：`LG_project_docs/requirements/T-INSIGHTS-DAILY-REPAIR-20261030-03/release/handoff.md`、`.runtime/daily-automation-20261030/review-authorization.json`。

限制：新真实业务日和首次00:30尚未执行；本地副本DEGRADED时不生成新日；没有恢复生产或连接真实IMAP；既有API元数据未热部署，其他服务未重启；父审查仍需新版本连续两轮完整无问题。
