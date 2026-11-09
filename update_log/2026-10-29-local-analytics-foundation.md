# 2026-10-29 本地独立客诉分析底座

开始记录：2026-10-29 16:27（Asia/Shanghai）；最终核验时间见 `verification/results.json`。

## 原因与范围

按用户“先用本地开发数据推进本地的数据库建立”的指令，先交付独立数据存储、日期分类读取模型和 agent 查询接口，预留生产配置。本次创建 `D:/LFEN_project/dev_project/complaint-insights`，没有重写原项目结构、修改源库或操作生产。

## 涉及文件和资源

- `insights/`：配置、只读源适配、镜像与增量、分类和时间规则、读取模型、API/权限、初始化和入口。
- `sql/001_foundation.sql`：独立目标库增量迁移；应用后摘要校验，未修改既有迁移。
- `assets/taxonomy/`：原部署三份分类 JSON 的逐字节副本。
- `deploy/compose.yml`、`config/production.example.json`：隔离 PostgreSQL 与默认禁止生产读取的模板。
- `scripts/`：本项目进程管理、只读 agent 客户端和全量验证器。
- `tests/`：规则及隔离 PostgreSQL/接口测试。
- `requirements.txt`、`dev-dependencies.txt`、`requirements.lock`：可复现依赖；依赖安装于独立虚拟环境。
- `README.md`、`LG_project_docs/`、`.project-governance/`：运行、设计、切源、原文覆盖、证据和流程记录。
- Docker 容器 `complaint-insights-postgres`、卷 `complaint-insights-pgdata`、回环端口 15433/3036；后台 API 与 30 秒同步进程。
- 私有凭据和运行日志只保存到忽略目录，不将其内容写入本日志。

## 实际验证

- 源读取预检 `transaction_read_only=on`，十四张业务表契约检查通过。
- 完整导入 185,828 条源业务记录，其中原始邮件 53,119 封、AI 产物 35,544 行、问题绑定 18,396 行；原始邮件、主归属及日期汇总对齐。
- 38 项单元与隔离 PostgreSQL 集成测试通过。实际创建和销毁的测试库仅在新实例内，未使用原项目 `.env` 的数据库做破坏性测试。
- 十四表全量源目标 SHA256 内容比较通过，实际 HTTP/鉴权及全文读取通过。
- 本项目 API/worker 停止、端口释放、重新启动及水位续传已实际验证；数据库卷保持。
- 生产连接、生产证书/SCRAM/权限及生产负载：未执行。看板 UI、自动周报、附件文件传输：不在本期范围。

## 失败与修正

- 任务初始化第一次被原话覆盖检查拒绝：拆分引用未覆盖机器识别的完整原句；保留完整原句后重试成功，没有伪造用户回答。
- 首次计划检索发生阶段与动作不匹配，按工具合同调整到 S4；状态保持现状比较明确登记 O0，并登记必需安全隐私门禁。
- 验证上下文被文档目录检查拒绝：本任务新增 `requirements-dev.txt` 被识别为根目录产品文档。仅将该开发依赖清单改为 `dev-dependencies.txt` 后通过；失败与重试已进入账本。
- Starlette 测试客户端报告 httpx 兼容层弃用提示，38 项测试仍通过；这是测试依赖提示，不是运行时异常。

## 工程与人的决定

本地工程与测试已完成，服务运行中。安全隐私门禁和用户验收与自动验证分开记录，尚未收到用户通过决定，不标为已验收。生产重启未获授权，本期没有执行。

原项目受 AOCI 管理的业务文件没有发生本任务修改；独立新项目未建立正式 AOCI 索引，不冒称完成该新项目的 AOCI 全库认知或维护。

## MCP 远程查询补充（2026-10-29，验证时间见 mcp-results.json）

- 用户原话与真实远程调用选择保存在 `discovery/mcp-steering.md`。该回复没有批准安全隐私门禁。
- 新增 `insights/datasets.py`、`mcp_server.py`、`mcp_http.py`；API 增加固定白名单的源资料目录与分页查询，权限/能力目录同步。
- 新增 MCP 客户端、TLS/令牌准备、远程防火墙、交接打包和真实协议验证脚本。进程管理增加单服务控制；新增配置、公开 CA、参数示例和中文交接手册。没有修改既有 SQL migration。
- 通过官方 SDK 文档和 PyPI/实际包索引核验后固定 `mcp==2.3.0`，增加 `client-dependencies.txt` 并重新生成 UTF-8 `requirements.lock`；依赖仅安装到本项目虚拟环境。
- 启动本项目 HTTPS MCP `192.168.10.20:3037`；新增本项目所有的 `ComplaintInsights-MCP-3037` Windows 防火墙规则，仅该内网 IP/端口、`192.168.10.0/24`、Domain/Private。数据库和 API 保持回环监听，生产无操作。
- 47 项单元/隔离 PostgreSQL/MCP 契约测试通过；严格 TLS 下发现 11 个只读工具并实际调用 26 次，十四类资料与只读 SQL 逐类核对通过。旧版 initialize、错误令牌/Host/Origin、来源和明文限制、资源读取、stdio 调试入口通过验证。
- 交接 ZIP 实际解压后运行随包客户端，发现 11 个工具。包有独立 MCP 只读令牌，未包含任何数据库凭据或私钥；仅保存在受限 `.secrets` 中。
- 首次 TLS 连接失败，原因为证书缺 SKI/AKI；补齐扩展并保持密钥和令牌后重试成功。失败证书与摘要保留在受限 `.runtime/tls-before-repair/`，未关闭 TLS 校验。
- 治理范围修订触发澄清重开，取得用户真实回答后经正式 Amendment 解决。历史阶段查询保留原字节迁入 query-history，官方重建索引校验通过；不是改写历史摘要来伪造当前查询。
- 文档补充过程中一次 patch 因空 hunk 被拒绝，工具确认零修改；删除空 hunk 后重试成功。
- 尚未由另一台电脑进行路由/客户端验收；生产连接和负载未验证；安全隐私 Gate、用户验收和可选多轮对抗性审查没有通过记录。
