# 日报看板维护与交接

## 入口与边界

在这台电脑访问 [http://127.0.0.1:3030/](http://127.0.0.1:3030/)。日报是独立 Python 单页服务，不是原 AICS 的 Next.js 开发服务。3030仅监听回环，身份边界为本机操作者及 Host/Origin 检查；页面和接口只读。不要对外开放3030，也不要使用 `Start -Service All` 恢复生产采集。

当前报告日期2026-10-29，数据源production-ai-customer，本地副本版本24；生产库持续隔离。当前 MCP 新版接入说明、令牌发放门户及内网开放由独立会话“MCP 内网接入、使用说明与令牌管理”处理，ID `01a188de-a98f-7c02-802b-4c218caf7651`。

## 页面使用

1. 顶部阅读结论和六项指标。Top10按业务问题类型汇总，点击行即可筛选该类客诉原信。领域和主类标签包含全部相关来信；下钻后选择具体故障。
2. 搜索支持摘要、原文、译文、邮箱和 UID。用 `#103269` 精确定位邮件主键。点击小时柱筛选对应北京时间时段；“重置筛选”返回全部634封。
3. 表格中的“发”为发件邮箱，“达”为实际采集邮箱。详情内另有原始To显示名/地址和Cc。主题、正文的原译按钮分别切换；侧栏按钮同样独立。
4. 图片、日志或其他文件列展示首个文件，点击后进入侧栏附件区，可切换该邮件的所有附件。图片/HEIC转为惰性JPEG，日志限256KB，视频使用原件，PDF预览首页；完整内容用“下载原文件”。密钥和签名不执行。
5. UID多账号时列出主账号、误建账号等角色，不选单一值。展开“UID识别依据”查看原文证据和真实RFC关联；展开“复核元数据”查看原分类、旧摘要和历次归类依据。

## 文件与读取链

- `.runtime/cursor-verification-20261030/frozen-source.json`：不可改写的本地源快照。
- `mail-review-a/b/c.json`：634封初次逐封审阅；`theme-review-overrides.json`、`theme-hierarchy-review.json`：保留历史细分修正。
- `main-groups-review.json`：业务主类定义与细类映射；`reclassify-b/c.json`、`conversation-classification-review.json`：111封疑难邮件的附件/会话证据；`classification-decisions.json`：本次主审合并及冲突裁决。各文件均有来源摘要绑定，不直接修改审阅者原文件。
- `uid-review.json`、`uid-full-context.json`、`uid-conversation-text.json`：UID与历史邮件头/原文证据。业务问题组、同发件人或同UID本身都不是会话关系。
- `.runtime/daily-reports/2026-10-29/report.json`：原子生成的读取模型，包含634封摘要、原文、译文、证据、分类和附件清单。页面请求不访问数据库或IMAP。
- 同目录 `attachments/`：固定数字ID命名的原件`.bin`和预览；manifest保存来源身份、大小与内容摘要。PDF首页渲染使用PATH中已有的Poppler `pdftoppm`，最长20秒、首页最长边1600像素。没有渲染器时保留原件并明确提示下载。

## 管理命令

以下命令在 `D:\LFEN_project\dev_project\complaint-insights` 执行，只管理本项目board进程：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\manage.ps1 -Action Status -Service board
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\manage.ps1 -Action Stop -Service board
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\manage.ps1 -Action Start -Service board -Config .secrets\local.json
```

重建同一冻结来源的报告，不会连接生产；须保留全部已绑定审阅文件和附件manifest：

```powershell
$env:PYTHONUTF8='1'
.venv\Scripts\python.exe -m insights.daily_report
.venv\Scripts\python.exe -m unittest tests.test_daily_report -v
node --check assets/daily-board.js
```

服务会在报告时间戳变化后读取新模型；页面需刷新。已打开侧栏的报告版本不一致时会提示重载。代码变更则只重启board。运行日志为`.runtime/board.err.log`，仅记动作/状态/耗时，不记录查询词或邮件正文。

## 只读接口

|路径|用途|
|---|---|
|`GET /data.json`|概览、统计、主类/子类/领域和表格数据；不直接返回全文body、审阅metadata字段|
|`GET /mail/{mail_pk}`|仅查询本日报内邮件的完整原文、译文、收发邮箱、UID、审阅元数据与所有附件|
|`GET /file/{id}/preview`|固定允许ID的图片、日志或PDF首页预览|
|`GET /file/{id}?download=1`|下载本地已校验原件|

这些是本机看板接口；给其他内网Agent使用的协议入口是独立MCP服务。不要把3030接口当MCP转交他人。

## 后续生产恢复

不得因看板已经可用而取消生产隔离。恢复连接、数据库重启、采集排程及源副本一致性复核均需按用户后续授权处理。未来日报需冻结新的日期范围和版本、补齐逐封审阅及来源摘要绑定，再生成新读取模型；当前程序和当前报告不证明后续日期已自动完成AI归类。

验收证据和未验项见 [acceptance.md](../verification/acceptance.md)。原始邮件、IMAP配置和客户附件保留在受限本地目录，不随公共交接文档打包。
