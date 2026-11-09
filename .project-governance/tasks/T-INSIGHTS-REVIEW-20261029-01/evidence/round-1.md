第 1 轮完整审查完成，确认 **3 项问题**。本轮不能计为无问题轮次。

审查者：`review_one`。正式开始：`2026-10-29T10:49:30Z`；独立实体探针结束：`2026-10-29T10:57:02.707358Z`。此后仅补读原始治理问答、运行 4 项规则/网络边界测试并整理结论。

基线为 59 文件清单，SHA256：`19c303af688be7bdbba39b1e3d8a179e7d0e3f982e5a1c4567f6754749ef1971`。核对时仅 `LG_project_docs/README.md` 摘要不同，主线程已确认系正式初始化工具自动生成目录；其余 58 文件一致。实体审查期间未修改交付业务文件。

**确认问题**

| ID | 严重度 / 来源 | 复现、预期与实际 | 位置与证据 |
|---|---|---|---|
| F-R1-ROOT-01 | 中；主线程发现，本审查者复核代码和实体证据 | 分类目录文件丢失或 JSON 无效。预期失败可见，状态 `DEGRADED` 并记录失败；实际 `load_static` 在异常处理外抛出，来源仍 `READY`、错误码为空，最近运行仍显示成功。旧数据和版本未变化。 | `insights/syncer.py:118`、`:119`、`:204`；`.project-governance/tasks/T-INSIGHTS-REVIEW-20261029-01/evidence/root-round1-probes.json:16` |
| F-R1-ROOT-02 | 高；主线程发现，本审查者复核代码和配置证据 | 在源 DSN 追加 `hostaddr=192.168.10.155`，或在目标 DSN 追加非回环 `hostaddr`，只运行配置校验。预期在连接前拒绝；实际校验通过，源身份摘要不变，且默认生产读取仍为关闭。`host` 与实际 libpq 目的地址脱离，绕过目的地址约束。探针没有连接这些地址。 | `insights/config.py:33`、`:75`、`:83`、`:96`；同上证据文件 `:33` |
| F-R1-REVIEW-01 | 低；本独立审查者发现并复现 | 接收方按手册使用 Python 3.10 安装固定客户端依赖。预期能安装；实际 `httpx2==2.16.0` 要求 Python `>=3.11`，pip 解析退出 1。当前 Python 3.13 服务正常，但交接说明承诺的环境不能使用。 | `release/mcp-handoff.md:52`、`client-dependencies.txt:2`；`.runtime/review-one-results.json:117` |

F-R1-REVIEW-01 实际命令：

```powershell
.venv\Scripts\python.exe -m pip install --dry-run --ignore-installed --python-version 3.10 --only-binary=:all: --no-deps --target .runtime/review-one-python310 httpx2==2.16.0
```

实际输出包含 `Requires-Python >=3.11`、`No matching distribution found for httpx2==2.16.0`，退出码 `1`。本地已安装包的 METADATA 同样声明 `Requires-Python: >=3.11`。

**原文逐条覆盖**

本轮重新独立读取了完整 `survey.md`、`mcp-steering.md`，以及原任务 `before.json` 中的完整 `request_snapshot` 和真实澄清问答，没有以派生验收清单代替。

来源简称：

- S1：`discovery/survey.md:9`，原始完整目标句。
- S2：`discovery/survey.md:13`，“暂时不考虑人工分类”。
- S3：`discovery/survey.md:17`，没有生产重启权限。
- S4：`discovery/survey.md:21`，先用开发数据建立本地库，后续快速接生产。
- M1：`discovery/mcp-steering.md:5`，查询不同数据。
- M2：`discovery/mcp-steering.md:7`，MCP、说明、交接、按需调用。
- M3：`discovery/mcp-steering.md:17`、`:21`，其他内网电脑 Agent 直接远程调用。

| 编号 | 原文要求拆分 | 状态 | 核对与证据 |
|---|---|---|---|
| R01 | S1 独立客诉看板目标；S4 本期先交付数据底座 | 本期已实现 | 独立目录、数据库实例、查询模型和接口存在；UI、自动周报按真实范围留待后续。`README.md:3` |
| R02 | S1/S4 数据进入这台机器的独立 PostgreSQL | 已实现 | 真实监听 `127.0.0.1:15433`；只读 SQL 查询到独立分析库 53,119 条当前邮件事实。`.runtime/review-one-results.json:97` |
| R03 | S4 先使用本地开发数据 | 已实现 | 实际来源 `development-local`；十四张表直接从开发源只读快照与副本逐行 SHA256 比对一致。结果文件 `:5` |
| R04 | S1 获取全部原始邮件 | 已实现 | 53,119 条 `messages` 与目标内容一致；完整原文和 JSON 有按单封及源记录查询入口。`api.py:294`、`:199` |
| R05 | S1 获取分类数据 | 已实现 | 三份静态目录、动态候选与注册数据进入分类模型；十四表目录覆盖候选、提案、支持、别名和生命周期。`catalog.py:10`、`:45`；`source.py:22` |
| R06 | S1 先按日期整理 | 已实现 | 北京时间日期模型、含首尾范围规则；混合历史偏移规则测试通过。`time_rules.py:46`；本轮 4 项补充测试 |
| R07 | S1 再按分类归类 | 已实现 | 主分类及多问题分类、1/2/3 级预计算统计；实际当前主分类/绑定与目录层级不一致数均为 0。`projection.py:97` |
| R08 | S1 日期→分类→原始邮件整合 | 已实现 | `get_report_context` 对应日期→分类→邮件；隔离反例核对 ACC、PAY、PEND 的统计、列表、上下文集合一致。结果文件 `:81` |
| R09 | S1 供其他 Agent 分析、形成周报材料 | 已实现数据准备 | 提供完整统计、按需证据及组织后的材料；不把分页上下文冒充周期总量。`mcp_server.py:35`、`:177`；自动生成周报不在本期 |
| R10 | S1 实时增量增加 | 已实现轮询语义 | 30 秒事件轮询、60 秒辅助对账、3600 秒完整对账已实现并明确延迟边界；没有虚称完整历史 CDC。`syncer.py:138`、`:211` |
| R11 | 增量更新及关联变化 | 已实现 | 独立反例修改 `InboundMail.sourcePk`，旧邮件转未分析、新邮件继承 AI；两端事实均更新。结果文件 `:77` |
| R12 | 删除同步与旧副本追溯 | 已实现 | 删除后当前事实消失，重新插入相同主键后取消墓碑并更新日期桶。结果文件 `:80`；`syncer.py:85` |
| R13 | 迟提交、恢复后增量可继续 | 已实现 | 邮件和 AI 在不同事务乱序提交，使用新 Settings/新调用模拟 worker 恢复，迟提交邮件及 AI 均补齐。结果文件 `:83` |
| R14 | 日志截断、无事件变化仍可恢复 | 已实现当前状态对账 | 隔离库停用事件触发后修改源，再清空日志，完整对账恢复实际内容。结果文件 `:84` |
| R15 | 断线不破坏已发布数据 | 已实现常见连接故障；部分失败状态有缺陷 | 实际连接故障得到 `DEGRADED/ConnectionTimeout`，水位和版本不变，旧 API 可读，重试恢复 `READY`；目录加载失败遗漏为 F-R1-ROOT-01。结果文件 `:78`、`:113` |
| R16 | 提供访问数据库的接口 | 已实现 | HTTP 固定查询和独立 SQL 只读账号可用；API 查询不访问源库。`api.py:108`；`db.py:23` |
| R17 | S2 暂不考虑人工分类 | 已实现 | 不读取人工覆盖表；仅采用 AI 绑定；人工来源排除和未完成分析保留 PEND 的本轮规则测试通过。`model.py:47`、`:52`、`:61` |
| R18 | S3 不授权生产重启 | 已遵守 | 本轮没有生产连接或重启；交付无生产管理工具。`production-switch.md:3`、`mcp_server.py:51` |
| R19 | S4 后续生产连接接通后快速切换 | 部分实现 | 独立来源标识、TLS 指纹、默认关闭模板、预检/全量/切换/回退说明齐备；实际目的地址约束有 F-R1-ROOT-02。`production-switch.md:5`；`config.py:64` |
| R20 | M1 查询不同类型数据 | 已实现 | 所有十四表通过真实 HTTPS MCP 分别查询；非空表进一步调用单记录工具，空表正确返回空。结果文件 `:90` |
| R21 | M2 工具以 MCP 形式构建 | 已实现 | 标准 MCP 发现、结构化输入输出、只读注解、资源读取实际成功。`mcp_server.py:108`；结果文件 `:90` |
| R22 | M2 给出使用说明 | 已实现 | 工具指南、每类工具用途、参数/口径、分页/错误及示例齐备；真实调用验证与接口一致。`mcp-handoff.md:68` |
| R23 | M2 方便交接如何使用工具 | 部分实现 | 私有交接包 11 文件完整，无 SQL 凭据/私钥；客户端及 CA 齐备；Python 环境下限说明存在 F-R1-REVIEW-01。结果文件 `:91` |
| R24 | M2 按需调用所需数据 | 已实现 | 列表默认不读正文、源记录默认不读 payload，选中后再取全文；各分页接口实际遍历并拒绝篡改游标。`api.py:199`、`:251`；结果文件 `:82` |
| R25 | M3 其他内网电脑 Agent 直接调用 | 入口已实现；跨电脑环境未实测 | 真实监听 `192.168.10.20:3037`，客户端无需源库/SQL 连接；同机通过内网地址完成标准远程协议调用。另一台电脑实际路由和客户端验收明确保留。`mcp-handoff.md:171` |
| R26 | M3 HTTPS、认证、内网范围 | 已实现 | TLS1.3、真实证书指纹、错误主机名拒绝；缺失/错误令牌 401，Host/Origin 拒绝，超大请求 413。结果文件 `:85`、`:89` |
| R27 | M3 不能通过代理头伪造内网来源 | 已实现 | 本轮网络边界测试确认外部 TCP 地址即使带 `X-Forwarded-For/Proto` 仍 403；明文拒绝、允许网段与正确令牌放行。`mcp_http.py:69`；`tests/test_mcp.py:86` |
| R28 | SQL/API 权限隔离 | 已实现当前运行配置 | 实际 reader 为非超级用户、无建库/建角色/复制/BYPASSRLS 权限，无原始 schema 使用权、无事实表 INSERT 权限。结果文件 `:103` |
| R29 | 查询版本、完整分页与一致快照 | 已实现 | 五类分页实际遍历并拒绝篡改；SQL REPEATABLE READ 跨新版本发布仍保持旧快照，退出后新连接看到新数据。结果文件 `:79`、`:82` |
| R30 | 归档不重复统计、附件范围明确 | 已实现 | 归档仅在源镜像/归档视图追溯，事实由当前 messages 投影；附件元数据全部核对 21,974 条，不声称复制文件本体。`projection.py:65`、`datasets.py:11` |
| R31 | 运行与故障交接 | 已实现，受已列问题约束 | 三进程真实运行；生命周期、故障表、证书和令牌维护、启动恢复说明齐备；没有假称注册开机任务。`manage.ps1:18`；`mcp-handoff.md:143` |
| R32 | 凭据和业务内容不进入公开交接/审计 | 已实现所检查范围 | ZIP 条目白名单及实际配置字段检查通过，无数据库凭据/私钥；实现审计不记录工具参数/邮件正文。`build_mcp_handoff.py:12`、`mcp_server.py:125` |

**11 个 MCP 工具逐个核对**

| 工具 | 本轮真实协议验证 |
|---|---|
| `get_data_guide` | 成功；十四表目录、口径与边界存在 |
| `get_sync_status` | 成功；来源为 `development-local` |
| `get_capabilities` | 成功；能力和权限目录可读 |
| `list_taxonomy` | 成功；一级目录及分页 schema 可读 |
| `query_daily_statistics` | 成功；多问题、二级分类、日期范围 |
| `list_mails` | 成功；日期筛选、小页默认不加载正文 |
| `get_mail_detail` | 成功；真实列表主键、原始行与 AI 行 |
| `get_report_context` | 成功；多问题、正文显式请求 |
| `list_source_tables` | 成功；十四张业务表 |
| `list_source_records` | 十四表分别成功；默认不返回 payload |
| `get_source_record` | 所有非空表取选中主键成功；完整 payload 存在 |

另验证错误分支：非法邮件路径、非法表名、倒置日期、超限页大小均返回 MCP 工具错误；资源 `complaint-insights://guide` 可读。

**实际证据**

- 独立探针：[review_one_probes.py](D:/LFEN_project/dev_project/complaint-insights/.runtime/review_one_probes.py)
- 全部成功探针结果：[review-one-results.json](D:/LFEN_project/dev_project/complaint-insights/.runtime/review-one-results.json)
- 执行：`.venv\Scripts\python.exe -X utf8 .runtime/review_one_probes.py`，最终退出码 `0`。
- 本轮另运行 4 项人工排除、未完成分类、历史日期与网络伪造边界测试，`Ran 4 tests ... OK`。
- 初次自写探针出现两类探针错误：SQL 表达式转换括号、驱动异常类预期过窄。均仅修正 `.runtime` 探针后重跑通过，没有当作产品缺陷。
- 真实源数据未写入；隔离源/目标随机测试库仅位于新实例 15433，执行后销毁。

**限制与范围**

- 未在另一台内网电脑执行真实路由及客户端验收；本轮覆盖服务端机制、真实内网地址 HTTPS 和可交接客户端，不把同机调用冒充跨电脑验收。
- 生产网络、认证、证书、负载及切换未执行，符合本期范围和无重启授权。
- UI、自动周报、附件文件本体不在本期。
- 全量内容核对按既有同步契约排除 `messages.last_fetched_at` 运行心跳；其余十四表字段逐行核对。
- 未对不可访问的外部环境猜报缺陷。3 项确认问题仍待修复，本轮连续无问题计数为 0。
