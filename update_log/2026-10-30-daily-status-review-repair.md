# 日报状态口径、读包及已发布证据返修

保存材料时间：2026-10-30T12:19:34.174826+00:00。任务T-INSIGHTS-DAILY-REPAIR-20261030-02，直接依赖T-INSIGHTS-DAILY-AUTO-20261030-01，复用其实际Accepted审查授权。

四项确认问题均修复：显式非客诉状态与scope冲突由共用规则在build/check阻断；读取器对超长主题/元数据返回有界标识和完整字段续页；重复发布及prepare校验实际正式目录，包含原件/预览/ZIP及source/review/quality/附件manifest绑定；check对照原始subject/recipients_original/cc/收件时间而允许展示to投影。安装skill升1.0.2，运行方法和语义责任同步。

实际验证：73项测试；独立原始合成样本7封、1封历史会话及4附件重新生成、隔离发布/幂等/损坏阻断；32k主题/25k元数据/28k正文完整重组；历史634封/405附件/35ZIP全量原件与预览核验，原报告SHA未改；两个3030地址默认昨天、详情/图片/文本/PDF/ZIP及日期版本错误通过。日期UI未再变更，前一返修的真实白底/UID首列9列/昨天快捷/100重载25截图继续有效。

未重启任何服务，3030监听PID210888与其他服务PID均保持；生产false、watch停。automation-2回读保持ACTIVE、00:30、当前会话，未新建自动化。没有真实生产访问/IMAP、新日期发布、真实定时触发或Git推送。

失败证据保留：首次测试误写不存在模块；隔离验证器把assemble摘要当报告；新增PDF预览核验误用文件名，按既有id.pdf.jpg约定修正后历史全量通过。另目录级write-guard拒绝没有导致写入，改核对范围内具体文件后允许。

回滚：本轮before目录保留生成器/测试及完整安装skill前像，新读包测试有完整差异；按局部反向补丁恢复，不触碰历史数据。保存版本不等于最终审查或用户验收，通过官方close归属父审查后继续同版两轮完整审查。

涉及：insights/daily_generation.py、tests/test_daily_generation.py、tests/test_daily_skill_reader.py、安装complaint-daily-report/SKILL.md与references/final-standard.md、execution.md、review-contract.md及scripts/read_packet.py；本任务原文/验证/交接/私有证据与治理记录。未改变项目结构、服务端口、历史日报与调度。
