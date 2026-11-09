# 独立客诉分析数据底座

独立 PostgreSQL 保存邮件和 AI 分类副本，按北京时间日期、分类整理，供 agent 通过 MCP 按需查询。已提供独立客诉日报看板与每日生成 skill；当前生产采集保持隔离，历史副本不代表实时生产数据。

| 服务 | 地址 / 标识 |
|---|---|
| PostgreSQL | `127.0.0.1:15433/complaint_insights` |
| 查询 API | `http://127.0.0.1:3036` |
| 内网 MCP | `https://10.8.61.200:3037/mcp`，HTTPS + 独立 Bearer 令牌 |
| MCP 接入与令牌门户 | `https://10.8.61.200:3029/`，公开说明下载；独立管理员登录后发放/撤销 |
| 客诉日报看板 | `http://10.8.61.200:3030/`，同机 `http://127.0.0.1:3030/` |
| MCP 接收人推荐来源 | `production-ai-customer`，历史本地副本；采集已暂停，先查同步状态 |
| 开发来源标识 | `development-local` |
| 数据库容器 / 卷 | `complaint-insights-postgres` / `complaint-insights-pgdata` |
| 同步周期 | 邮件和 AI 事件 30 秒；辅助表内容对账 60 秒；完整对账 3600 秒 |

## 运行

首次准备（需要 Docker Desktop、Python 3.11+；已交付环境使用 Python 3.13）：

```powershell
Set-Location 'D:\LFEN_project\dev_project\complaint-insights'
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m insights.cli bootstrap --original-project 'D:\LFEN_project\dev_project\AI客诉系统'
.venv\Scripts\python.exe -m insights.cli sync
powershell.exe -NoProfile -NonInteractive -File scripts/manage.ps1 -Action Start
```

`bootstrap` 仅接受回环地址的开发邮件源。它读取源项目的邮件数据库连接，创建新实例、独立角色和私有配置；不迁移、不写入源库，不改变源项目。缓存中已有 `postgres:17-alpine` 时使用现有镜像，不拉取镜像。

查看或停止本项目的 API 与同步进程：

```powershell
powershell.exe -NoProfile -NonInteractive -File scripts/manage.ps1 -Action Status
powershell.exe -NoProfile -NonInteractive -File scripts/manage.ps1 -Action Stop
```

停止脚本仅结束经路径和命令行核验的本项目进程树，保留数据库及卷。电脑重启后，先运行 Docker Desktop，再执行 `Start`；本期没有注册 Windows 开机任务。持久水位支持进程恢复，不依赖进程内缓存。

## 给分析 agent 的入口

其他内网电脑使用 [MCP 接入中心](https://10.8.61.200:3029/)。当前 [完整指南](LG_project_docs/requirements/T-INSIGHTS-MCP-PORTAL-20261030-01/release/client-guide.md) 覆盖协议、TLS/CA、全部11工具、14表、参数、分页、错误、计数与选源。门户下载的通用包不包含令牌；`.secrets/mcp-handoff.zip` 也已替换为同一无凭据包。管理员须按接收人单独发放令牌，不能转发现有接收人的私有配置。旧foundation交接说明属于历史版本，以本节和当前门户为准。

3029入口只在 `10.8.61.200` 上以HTTPS运行，实际TCP来源限制为 `10.8.0.0/16`。普通访客只能阅读和下载；MCP Bearer不能登录管理员页面。唯一管理员初始凭据保存在服务器受限 `.secrets/token-desk-initial.json`，不进入客户端包或日志。运维与回滚见 [管理员交接](LG_project_docs/requirements/T-INSIGHTS-MCP-PORTAL-20261030-01/release/operator-handoff.md)。

同机 SQL/HTTP 分析使用下面的入口：

仅交付 `.secrets/agent.json` 给有权分析该数据的 agent。该文件只包含只读数据库连接、API Token、来源标识和地址；不要分发包含源库、数据库所有者和同步写入凭据的 `local.json`。私有目录已限制为当前 Windows 用户与 SYSTEM 访问，凭据不进入 Git 或验证证据。

无需额外依赖的客户端：

```powershell
.venv\Scripts\python.exe scripts/agent_client.py status
.venv\Scripts\python.exe scripts/agent_client.py taxonomy --limit 100
.venv\Scripts\python.exe scripts/agent_client.py daily --start 2026-10-15 --end 2026-10-23 --level 1
.venv\Scripts\python.exe scripts/agent_client.py mails --start 2026-10-15 --end 2026-10-23 --direction RECEIVED --limit 20
.venv\Scripts\python.exe scripts/agent_client.py mail --mail-pk 1 --include-raw
.venv\Scripts\python.exe scripts/agent_client.py report-context --start 2026-10-15 --end 2026-10-23 --include-body --limit 20
```

`mail-pk` 必须取实际列表返回值；示例的 `1` 不保证存在。日期范围为 **`[start,end)`**，`end` 不包含；业务时区为 `Asia/Shanghai`。开发数据最新日期以同步状态或 SQL 为准，不能当作当前生产数据。

HTTP 请求携带 `Authorization: Bearer <agent.json 中的 api_token>`。所有已注册端点均鉴权，包括健康与 OpenAPI；未授权返回 401。接口：

| 路径 | 内容 |
|---|---|
| `/health` | 数据库连接健康 |
| `/openapi.json` | 可供 agent 读取的完整 API 契约 |
| `/v1/capabilities` | 能力、权限父链、启用状态和禁用原因 |
| `/v1/sync/status` | 来源、版本、最近同步/对账时间、失败代码及同步调度 |
| `/v1/taxonomy` | 冻结及动态分类，包含候选、待审、归档等源状态；分页 |
| `/v1/daily` | 按日期和 1/2/3 级分类汇总；分页 |
| `/v1/mails` | 邮件元数据、AI 分类与摘要；不默认加载正文；分页 |
| `/v1/mails/{mail_pk}` | 原文、译文、问题绑定、附件元数据；`include_raw=true` 返回完整源行和 AI 行 |
| `/v1/report-context` | 按日期、分类组织当前页邮件；`include_body=true` 包含原文与译文 |
| `/v1/source-tables` | 十四类源资料、用途与主键目录 |
| `/v1/source-records` | 固定表白名单的分页源副本；显式请求 payload 和删除标记 |

先用 `/v1/daily` 获取周期内完整统计，再分页取原文证据。上下文页不是完整周报，也不以抽样页的邮件数冒充总量。`direction=ALL` 可取包含发件、草稿与删除文件夹在内的全部当前源行；日汇总与报告上下文默认 `RECEIVED`。

`scope=primary` 中每封邮件只有一个主归属；`scope=all_issues` 保留多问题归属。父级汇总预先按邮件去重；跨不同分类直接相加仍存在交叉。`PEND` 保留待分析/未判断数据。人工覆盖表没有读取入口。`category_ai` 与 `category_normalized` 分别保存原始 AI 建议和流水线归一结果，不能因两者不同就视为人工分类。

所有分页返回 `meta.data_version` 和 `next_cursor`。数据版本变化时旧游标返回 409，客户端必须重新查询；游标不能静默跨版本拼接。需要长时间读取完整周期时，使用下面的只读 SQL 快照。超出 JavaScript 安全范围的整数通过 HTTP 以字符串返回。

## 客诉日报与每日生成

看板默认选择北京时间前一自然日（例如10月30日打开显示10月29日日报），日期框与标题标注邮件所属日期；“昨天”可返回默认日期。所选日期未生成时显示“日报未生成”，可通过日期框或“已生成日报”切换。历史链接如 `http://10.8.61.200:3030/?date=2026-10-29`。页面继续使用既有白底、配色和布局，详情、附件预览/下载及子问题日志ZIP按相同日期和报告版本读取。

日常方法已安装为 `$complaint-daily-report`，入口在 `C:/Users/Administrator/.codex/skills/complaint-daily-report/SKILL.md`；配套标准、来源索引、审阅契约、基准主类和可执行脚本同目录保存。当前会话的“每日客诉日报生成”自动化每天北京时间00:30调用该skill生成前一天，电脑和Codex桌面应用须运行。

日期化生成入口为 `python -m insights.daily_generation --help`，支持prepare/build/check/publish；只读本地15433副本、逐封语义审阅、完整性校验后原子发布，日常生成无需重启3030。已发布日期默认不可覆盖。源未覆盖日终、DEGRADED、漏审或附件缺失时停止发布，保留运行状态与缺口，不使用历史或模拟数据替代。

使用与验证记录见 [本轮交接](LG_project_docs/requirements/T-INSIGHTS-DAILY-AUTO-20261030-01/release/handoff.md)。MCP令牌服务由独立会话维护，日报生成不修改其配置。

## SQL 访问

只读连接保存在 `.secrets/agent.json` 的 `readonly_database_url`，角色为 `insights_reader`。该角色只能读取 `analysis`，不能写入、创建对象或直接访问物理镜像。使用视图读取完整原始数据，包括源端删除标记和归档快照。

```sql
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY;

SELECT source_id, data_version, last_sync_at, status
FROM analysis.v_sync_status
WHERE source_id = 'development-local';

SELECT business_date, level_one, sum(mail_count) AS mail_count,
       sum(pending_mail_count) AS pending_mail_count
FROM analysis.daily_category
WHERE source_id = 'development-local'
  AND scope = 'primary' AND category_depth = 1 AND direction = 'RECEIVED'
  AND business_date >= DATE '2026-10-15' AND business_date < DATE '2026-10-23'
GROUP BY business_date, level_one
ORDER BY business_date, level_one;

SELECT mail_pk, business_date, category_ai, category_normalized,
       summary_zh, body_plain_text, body_translated
FROM analysis.v_mail_details
WHERE source_id = 'development-local'
  AND business_date >= DATE '2026-10-15' AND business_date < DATE '2026-10-23'
ORDER BY business_date, mail_pk;

COMMIT;
```

`analysis.v_source_records` 提供十四张源业务表的完整 JSON 副本，字段为 `source_id/source_domain/source_table/record_key/payload/synced_at/deleted_at`。它还保留未能挂到当前邮件的 AI 行和归档资料，便于对账；统计只计当前 `mail_fact`。附件文件本体未复制，`local_path` 仍是源端路径。

## 生产接入准备

完整步骤见 [生产来源切换](LG_project_docs/requirements/T-INSIGHTS-FOUNDATION-20261029-01/release/production-switch.md)。配置模板为 `config/production.example.json`，默认禁止生产读取。开发与生产使用不同 `source_id` 和独立水位，邮件主键相同也不会混合。更改已绑定来源的主机、端口、数据库或 schema 会被拒绝，不能覆盖开发身份来冒充生产数据。

## 同步边界

- 正常日志覆盖的变化按 30 秒轮询读取，辅助表变化按 60 秒内容指纹对账；还需叠加同步耗时和源 AI 处理延迟，不承诺固定秒数内必达。
- 有界日志尾部重读处理近期乱序提交；更早迟提交、日志清理和无事件变化由完整对账保证当前状态最终一致。这不是保留所有历史变化的 CDC。
- 首次完整导入使用源只读一致快照；目标镜像、分类、汇总和水位原子发布。失败保留上一份可查询数据，状态标记 `DEGRADED`，下一轮重试。
- 镜像保留删除标记和归档快照；删除行不计入当前邮件。源端删除不等于副本物理擦除。本期不自动清理原始镜像、归档和运行账本，后续保留策略由数据所有者确定。
- API 仅查询独立库，不在请求中访问业务源库或重建全量数据。

验证记录见 `LG_project_docs/requirements/T-INSIGHTS-FOUNDATION-20261029-01/verification/`；任务日志见 `update_log/`。
