# 后续切换生产来源

本期没有执行生产连接或重启。生产 `10.8.45.155:5432/ai_complaint_mail` 的监听、凭据及证书交付由用户与生产 agent 完成；本文不构成重启授权。

1. 将生产 `connection.env` 和 `server.crt` 通过安全渠道交付到 `.secrets/production/`，不得写入普通文档、日志或 Git。
2. 核验服务器证书 SHA256：`7D:A9:1C:FC:69:FA:95:69:AF:3E:FA:BF:10:B8:37:88:70:6F:4B:14:8E:70:44:41:03:BA:7F:D6:7A:64:52:6F`。指纹来源为用户提供的生产回执，接入时必须与实际文件比对。
3. 从 `config/production.example.json` 创建私有 `.secrets/production.json`。复用独立目标库连接；源账号使用 `complaint_analytics_ro`，填入密码的 URL 编码值及实际证书绝对路径。启用 `sslmode=verify-full`，保留该信任锚摘要。
4. 保持 `source_id=production-ai-customer`，不要把开发标识的 DSN 改成生产地址；命名空间、镜像、统计和水位分别隔离。
5. 获准进行生产只读接入后，将私有配置的 `allow_production_read` 设为 `true`。只表示允许采集读取，不授予任何生产写入或重启权限。
6. 执行预检和首次完整同步：

```powershell
Set-Location 'D:\LFEN_project\dev_project\complaint-insights'
.venv\Scripts\python.exe -m insights.cli preflight --config .secrets/production.json
.venv\Scripts\python.exe -m insights.cli sync --config .secrets/production.json
```

7. 核对生产实际来源 IP、TLS、只读状态、列契约、分类文件版本与导入数量。生产期间数据增长，因此以同一只读源快照和发布批次验证，不把先前回执的 58,021 当作永远固定数量。
8. 冻结目录与当前三个文件摘要不一致时，先取得生产文件并为该来源配置独立 `catalog_dir`；不要静默沿用开发目录。数据库动态目录始终按来源同步。
9. 确认新来源状态 `READY` 后切换常驻进程：

```powershell
powershell.exe -NoProfile -NonInteractive -File scripts/manage.ps1 -Action Stop
powershell.exe -NoProfile -NonInteractive -File scripts/manage.ps1 -Action Start -Config 'D:\LFEN_project\dev_project\complaint-insights\.secrets\production.json'
```

10. API 默认来源随配置切换；SQL/HTTP/MCP 查询必须明确生产来源标识。分析 agent 的私有 `agent.json` 中同步更新 `source_id` 和本次选择的 API Token，随后重启 MCP，让适配层加载新的本地 API 凭据；MCP 自身的访问令牌独立，不用 API Token 替代。同步更新交接配置中的默认来源和参数示例，重建 `.secrets/mcp-handoff.zip`。开发数据仍保留，可通过显式 `source_id=development-local` 单独查询。

接口、日期模型和后续看板不需要随源切换重写。回退时先停止本项目进程，再以开发私有配置启动；不操作生产服务器或删除任一来源的数据。

尚未验证：真实生产网络、证书与 SCRAM 认证、生产只读权限、生产源负载和实际数据延迟。辅助表默认 60 秒内容指纹对账，完整对账默认 3600 秒；生产数据规模增长后应根据实测调整，不宣称当前开发测量代表生产表现。
