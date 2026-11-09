# 表格排序和日志 ZIP 使用说明

## 页面操作

打开 http://127.0.0.1:3030/ ，页面保持白色主题。

1. 在原信明细的“优先排序”中选择“有 UID 优先”“有日志优先”“有图片优先”或“有其他文件优先”。默认 UID；切换回第一页，保留筛选。各选项将对应有内容的邮件放前面，其余证据和收件时间作稳定次序。
2. 点击领域，再点击主问题和具体子问题。具体子问题行右侧显示日志数、涉及邮件数和“下载该子组全部日志”入口。
3. 下载的 ZIP 包含这个具体子问题的全部日志，不只当前页，也不随搜索结果缩减。无日志时显示“该子问题暂无日志”；未选具体子问题时提示先选择。
4. UID 位于第一列；邮件发件邮箱和送达邮箱仍在第二列。时间/内部主键从列表列中删除，详情及搜索仍保留追溯能力。

## 压缩包内容

目录形如 `mail_<邮件内部ID>/attachment_<附件ID>_<清洗后的原文件名>`，相同文件名不会相互覆盖。`_manifest.json` 列出报告日期、源快照摘要、子问题、邮件/文件数量及每个原件的文件名、字节数和 SHA-256。

ZIP 原件与已归档日志字节一致；不额外加入邮件正文、邮箱列表、UID 列表或服务配置。原日志自身已有的内容原样保留。

当前可下载 35 个子问题包、86 个日志。示例：更新安装与启动阻断 → 登录或账号验证失败，6 个日志/3 封来信，已实际浏览器下载核验。

## 实现与运维契约

- `insights/log_archive.py` 在日报读取模型构建阶段生成 ZIP，临时文件校验后原子替换。没有日志不生成；原件缺失或摘要不符拒绝构建完整包。页面下载不扫描数据库、不读取 IMAP、不现场压缩。
- 读取产物：`.runtime/daily-reports/2026-10-29/archives/<64位ID>.zip`；报告的 `subthemes[].log_archive` 和 `log_archives` 为唯一资源索引。
- 下载接口：`GET /log-archive/{archive_id}?v={report_sha256}`，允许 HEAD。仅允许当前报告中 ready 的固定 64 位 ID，不接受文件路径。必须携带当前完整报告 SHA；旧页面版本返回 409，应刷新页面。
- 能力 `daily_log_archive`，独立权限 `insights.attachments.logs.export`，完整父链为 `insights.attachments.read` → `insights.mail.read` → `insights.read` → `insights`。继承已有本机身份、客户端、Host 和 Origin 边界；权限缺失返回 403。
- Feature：`INSIGHTS_DAILY_LOG_ARCHIVE_ENABLED`，默认 `1`；关闭时 data.json 的 `features.daily_log_archive` 提供禁用原因，接口拒绝 503。仅修改看板进程环境后按本项目既有管理脚本重启 board。
- 审计动作 `log-archive.read`，风险 Medium、范围 RESOURCE；记录身份、资源 ID、HTTP 结果和耗时，不记录日志内容或查询正文。
- 3030 只监听 `127.0.0.1`。生产读取保持关闭，watch 不运行；不要用 `All` 或启动采集进程来重启页面。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/manage.ps1 -Action Stop -Service board
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/manage.ps1 -Action Start -Service board -Config .secrets/local.json
```

当前报告 SHA-256：`b2658daf25058d0ce07ee620d60266039998b5c767ddd0d81721698b3de93760`。源快照冻结于 2026-10-30 01:13:42 +08:00，未宣称当前生产完整或实时。

## 验证及回退

工程核验见 [acceptance.md](../verification/acceptance.md)：106 项测试、634 封全量排序、35 包/86 个日志字节与归属、实际浏览器下载及生产隔离。用户决定 Pending；本版本正式安全隐私门禁 Pending，工程结果如实保存 Deferred。

治理包活动查询校验仍报 S4/S5 不一致，已用官方入口重建复验且保留两次失败日志；后续需修复治理工具的阶段绑定，再重新核验，不得将本轮产品测试通过等同于治理校验通过。

本轮 before 副本位于 `.runtime/daily-table-20261030/before/`。回退需成套恢复 board/report/assets 和对应报告；`capabilities.py` 同时有 MCP 会话修改，禁止整文件覆盖，必须只回退本轮 `daily_log_archive` 能力和 export 权限。保留所有邮件和附件原件。MCP 门户、内网入口与 token 文档由独立会话负责。
