# 日期看板与每日生成交接

## 使用

- 看板：http://192.168.10.20:3030/；同机：http://127.0.0.1:3030/。默认北京时间今天；日期未生成显示“日报未生成”。日期框、“今天”、“已生成日报”与URL date可切换。
- 10月29日历史入口：http://192.168.10.20:3030/?date=2026-10-29 。原634封、405附件、35 ZIP保持不变，报告指纹`b2658daf25058d0ce07ee620d60266039998b5c767ddd0d81721698b3de93760`。
- 调用`$complaint-daily-report`；已安装到`C:/Users/Administrator/.codex/skills/complaint-daily-report/`。当前运行已读取入口并实际执行其脚本，不仅保存提示词。
- 自动化“每日客诉日报生成”（automation-2）已ACTIVE，kind=heartbeat，绑定当前会话`01a1866c-6ec4-7f83-9aa8-f75c67aebcf8`。每天北京时间00:30生成前一天；系统China Standard Time与客户端Asia/Shanghai一致，配置已由工具创建并回读。尚未到第一次计划运行时间，不声称已经自动生成新日报。

## Skill内容

|路径|用途|
|---|---|
|SKILL.md|执行入口、授权边界和完整流程|
|references/final-standard.md|逐封摘要、业务主类粒度、残余复核、UID真实会话、邮箱/译文/附件/ZIP、统计与最终页面标准|
|references/source-map.md|指定Cursor原话与本会话历次纠偏的可追溯映射|
|references/execution.md|实际准备、阅读、下载、生成、发布和页面验收方法|
|references/review-contract.md|绑定快照的逐封审阅、分组/残余质量检查与本日总结契约|
|assets/baseline-main-groups.json|16业务主类的基准定义，非固定配额|
|assets/quality-baseline.json|10月29日回归指纹、计数、配色与模块/列顺序|
|scripts/run_daily.py|使用项目解释器调用维护中的日期化生成器|
|scripts/read_packet.py|完整集合分页、正文分段和必要会话读取，显式提示未读完的大正文|
|agents/openai.yaml|可发现的UI介绍与调用提示|

Skill不包含真实邮件、UID、附件或凭据。上下文压缩后重新读入口和规定参考文件，不能依赖聊天记忆替代持久标准。历史数字仅作回归，不硬套未来日报。

## 数据和发布

新工作目录默认`.runtime/daily-work/YYYY-MM-DD/`；准备只通过reader访问15433本地分析库，事务read-only/repeatable-read。完整source、逐封review、quality、原件与ZIP均保留。机器负责集合、来源、计数、字节和引用校验；Agent负责逐封语义及全部主组/残余复核。质量未通过不发布。

正式报告目录`.runtime/daily-reports/YYYY-MM-DD/`原子出现后，3030自动可读，无每日代码改动或重启。已有同日默认不可覆盖，相同字节发布幂等。

## 当前阻塞与未验证项

- 当前生产读取关闭，watch停止；本地production-ai-customer副本DEGRADED，数据版本24，消息水位北京时间2026-10-30 01:13:42，辅助水位01:14:02。新日完整生成须等待人在另一个明确授权任务中恢复采集并达到READY和日终水位；本轮不恢复生产、不改状态强行通过。
- 已实际验证日期/生成/内网/附件相关37项测试、日志ZIP3项测试、两个地址的缺报/历史/详情/图片/文本/PDF/ZIP、634封完整索引分页和最长正文30714字符完整分段、真实浏览器交互。没有从另一台电脑实测。
- 没有实际等到定时触发，没有在现有DEGRADED副本上发布新日。完整新日真实语义生成效果需待真实数据到齐；不以结构校验宣称所有未来语义必然正确。未做独立forward-testing子Agent或多轮对抗性审查，未做移动视口实测。
- 机器和Codex桌面应用须运行；应用繁忙或机器休眠会影响实际触发/完成时间。调度机制与本地运行条件依据[OpenAI官方说明](https://developers.openai.com/training/walkthroughs/scheduled-tasks)。

## 验证与恢复材料

私有证据位于`.runtime/daily-automation-20261030/verification.json`、`browser-verification.json`、`local-source-status.json`、`automation.json`、`installed-skill-manifest.json`及测试日志。today-empty.jpg/history-date.jpg为实际截图，不进入GitHub。源业务文件回滚及运行观察见runtime-change.md；生产隔离保留。
