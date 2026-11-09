# 客诉日报修复与重分类

时间：2026-10-30T04:18:21.510763+08:00，任务T-INSIGHTS-DAILY-20261030-01。报告版本：d9c9f818a6b727321257b8d67d39eba9dc1bb62f11ed5eb49481cdba6f1b7a21。

- 修改insights/source.py、syncer.py：分页读取全部新事件后再推进checkpoint，避免全局日志尾号导致新分类漏采；隔离反例验证通过。
- 修改insights/mcp_http.py的令牌读取失效处理；后续MCP文件由独立会话接续，未覆盖其并行变更。
- 新增/完善insights/attachment_fetcher.py、attachment_preview.py、daily_report.py、daily_board.py与assets/daily-board.html/css/js、echarts本地资源，维护相关能力注册、tests/test_daily_report.py、测试与依赖锁定文件。只读IMAP下载405原件，校验来源身份及摘要；PDF使用现有Poppler离线首页渲染。
- scripts/manage.ps1增加生产隔离watch保护及board管理；.secrets/production.json禁止生产读取，保留独立备份；.secrets/mail-service.json受限存储邮件服务参数，不在日志复制凭据。
- 主层137收敛为16，具体故障保留子类；111封专项重核恢复103封，HTML-only、To显示名、UID多角色、错标图片、PDF白页和译文来源已修复。原审阅文件与失败截图保留，最终裁决另存。
- LG_project_docs/requirements/T-INSIGHTS-DAILY-20261030-01下维护原文、PRD、控件SPEC、逐条覆盖、验收证据及交接；.project-governance记录真实失败、重试与结果；.runtime保存受限客户数据和证明，不作为公开附件分发。

验证：92项完整测试通过（34.300秒）；634封详情逐字段HTTP核对；405附件读取/预览/Range校验；浏览器10排行、16主类、全部领域、分页634唯一ID、分时79封、UID/邮箱、独立原译、图片/HEIC/日志/视频/PDF通过；JS语法通过。性能单次概览0.0316秒、3,756,181字节，未做压力测试。

未验：生产源当前完整性、持续一小时时效、历史01:00前收齐；当前版本安全隐私门禁正式通过；同版连续两轮完整对抗审查。用户验收Pending。MCP新版门户和内网服务由01a188de-a98f-7c02-802b-4c218caf7651负责，未代其宣告完成。原AICS代码、生产库、邮件状态未修改，未发送邮件。

目录没有Git仓库，保留before业务文件副本和最终SHA；未声称Git范围对账通过。原AICS AOCI完整索引未成功加载，本任务未修改原AICS受管对象；独立项目没有AOCI索引，不生成正式认知条目。

正式治理附记：revision16修订后的活动条款查询复现检查仍返回不一致，未标为通过；失败保存在`.runtime/cursor-verification-20261030/governance-validation.txt`。本地业务版本与上述实际测试证据不变，按真实未完成结果留档，不修改Skill脚本或缓存绕过检查。
