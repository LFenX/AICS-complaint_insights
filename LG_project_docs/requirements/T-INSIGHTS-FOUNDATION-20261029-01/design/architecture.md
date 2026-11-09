# 数据、权限与运行契约

本期唯一计划与授权见 `.project-governance/tasks/T-INSIGHTS-FOUNDATION-20261029-01/before.json`；本文件说明最终技术设计，不建立第二份执行计划。

## 模块所有权

- `config/db`：私有配置、源身份、连接、只读与证书约束；禁止源写入。
- `source`：十四张业务表的白名单及必要列、两类事件的只读适配。
- `syncer`：一致源快照、目标镜像、来源锁、事件水位、内容对账、原子发布与失败状态。
- `catalog/model/time_rules/projection`：分类定义、源到分析事实的变换、时间归一和预计算统计；不负责网络。
- `api/capabilities`：固定查询、Bearer 身份、来源参数校验、能力与权限目录、游标版本及脱敏审计；不访问源库。
- `initialize`：只在独立目标实例安装增量迁移和最小权限角色；迁移已应用后摘要不符即拒绝。
- `cli/manage`：入口组装、容器及本项目进程生命周期；不修改其他服务。

## 数据字典与追溯

| 业务项 | 物理来源 | 分析字段 / 查询 |
|---|---|---|
| 原始邮件身份 | `messages.id` | `mail_fact.mail_pk`；按 `source_id` 隔离 |
| 邮箱 | `messages.mailbox_id -> mailboxes.id/email` | `mail_fact.mailbox` |
| 日期 | `internal_date/date_header/first_seen_at` | `received_at/business_date/time_shift_hours`；与源适配层相同的单行及全局回退补偿 |
| 原文和头 | `messages` 完整 JSON | `v_mail_details.raw_record/body_plain_text/body_html/date_header/...` |
| AI 关联 | `InboundMail.sourcePk/id -> MailAiArtifact.inboundMailId` | `inbound_mail_id/ai_artifact_id` |
| 原始及归一分类 | `MailAiArtifact.categoryAi/category/categorySource` | `category_ai/category_normalized/level_one/level_two`；不叠人工表 |
| 三级和多问题 | `taxonomyGroupId/issueTypeId/MailIssueBinding` | `issue_type_id/mail_issue`；一个有效主绑定，其余保持其他问题 |
| 未分析状态 | 缺 AI 或 `analysisState != DONE` | 保留邮件和原始建议，最终分类汇总进入 `PEND` |
| 中文摘要及译文 | `summaryZh/bodyTranslated` | `summary_zh/body_translated`，不生成新摘要 |
| 目录 | 三份冻结 JSON + `TaxonomyCandidate/IssueTypeRegistry` | `taxonomy/catalog_files`，原始候选与别名仍在镜像 |
| 归档 | `imap_reconcile_archive` | `v_archives`，不额外增加当前邮件数 |
| 周期统计 | 本地 typed facts | `daily_category`，按范围与分类深度预计算去重邮件数 |
| 版本与新鲜度 | 原子目标提交 | `v_sync_status.data_version/source_snapshot_at/last_*` |

辅助表对账不依赖 `updatedAt`，因此能覆盖无该字段的支持关系及删除。JSON 镜像保留新增字段；必要列缺失时拒绝发布，旧数据保持可读。

## 安全与隐私

数据所有者通过当前聊天明确授权将开发邮件及 AI 数据复制到该设备，用于独立分析，随后明确要求其他内网电脑的 Agent 远程调用 MCP。源数据包含邮件正文、邮箱与附件元数据；允许持有独立 MCP 令牌的内网客户端读取，实际验证尚未由另一台电脑发起，没有向第三方模型发送数据。未知的生产可达性、凭据和证书不作为已通过事实。

数据库与 API 仅绑定回环地址。容器、卷、配置和进程独立；私有目录使用当前用户/SYSTEM ACL。`insights_sync` 仅在独立目标库内写入，`insights_reader` 只能读分析表和受控视图。API 使用独立 Token，写操作没有路由；业务查询使用参数绑定，schema 与表来自固定白名单。权限完整父链、动作、风险与作用域由 `capabilities.py` 定义；来源即资源边界。

API 审计仅记请求 ID、路由模板、方法、状态及耗时，不记录 Token、查询参数、邮件正文或发件人。同步失败只保存 SQLSTATE/异常类，不将源数据放入错误账本。API 不返回 owner/writer/source 连接的值；分析 agent 的交付凭据单独输出，避免误传完整配置。

源镜像保留删除标记、归档和历史定位；默认查询剔除删除行。物理删除策略未作为本期自动行为，不能把副本状态同步称为数据擦除。

工程安全检查证据与正式 `security-privacy-review` 决定分开。测试成功不能代替用户审查、验收或生产授权。

## MCP 适配与内网入口

`mcp_server.py` 只负责工具输入/输出与本地 API 适配；日期、分类、权限目录、参数绑定与版本游标继续由既有 API 和读取模型负责。`datasets.py` 定义十四类原始资料的固定目录，`source-records` 使用受控分析视图，不接受任意 SQL。默认不取 payload，需要时按记录或小页读取完整源 JSON。

`mcp_http.py` 在 SDK 协议处理前核验 HTTPS、真实 TCP 来源网段和独立 Bearer 身份；不信任代理来源头。SDK 同时限制 Host/Origin。服务仅绑定 `192.168.10.20:3037`，允许 `192.168.10.0/24`；Windows 防火墙规则仅该 IP/端口与 Domain/Private 配置文件。MCP 不开放 PostgreSQL 和底层 API 到内网。

MCP 11 个工具均声明只读，并记录身份、工具名、状态与耗时；HTTP 层另有请求 ID。所有身份当前拥有同一副本的只读范围，没有按邮箱的数据隔离。独立 MCP 令牌和 TLS 私钥保存在受限 `.secrets`，交接包仅含 MCP 只读令牌、公开 CA、客户端和说明，没有任何数据库凭据或私钥。

## 兼容、运行和回滚

源固定命名空间绑定连接身份，不把密码纳入身份摘要；同库换密码无需重建来源。切换主机/数据库/schema 必须新建来源标识。生产必须显式开启读取、核对信任锚指纹并使用 `verify-full`，模板默认关闭。

失败事务整体回滚，不前移事件/版本/对账水位；副本状态 `DEGRADED` 与上一份成功数据同时保留。初次导入、周期完整对账、无事件辅助对账、事件正常增量均用同一提交机制。

回滚仅停止经确认归属的本项目进程和容器；保留数据卷。测试库只在该独立实例中以随机 `complaint_insights_*test_*` 名称创建、销毁；禁止对现有开发源运行破坏性验证。
