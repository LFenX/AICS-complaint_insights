# 管理员与维护交接

分享入口：https://192.168.10.20:3029/ 。管理员登录：https://192.168.10.20:3029/admin/login 。MCP：https://192.168.10.20:3037/mcp 。3029与3037均仅监听该内网IP，允许实际TCP来源192.168.10.0/24，HTTPS私有CA。

## 所有者登录与发放

唯一管理员名称为owner。初始随机口令只保存在服务器受限文件 `D:\LFEN_project\dev_project\complaint-insights\.secrets\token-desk-initial.json`。该文件没有HTTP下载路由，也未进入公开客户端包；管理员口令不能作为MCP Bearer使用。用户2026-10-30在当前私有聊天明确请求管理员账号、密码与登录入口，管理员初始口令仅在该聊天交付给用户，不写入本交接文档、公共输出或日志。

首次在接收方浏览器打开前，核对并信任管理员提供的CA公钥。文件SHA256为 `b65f85f59835a8277c254a6f41861f7f02ce9302e02c1fa9098dba71e3460d3f`。证书DER指纹为 `6ae4dee46fcebdf1c2d2137973a8c655b871b216aaf6fecb9e6a9ccae053c879`，不要混淆两种对象。

登录后进入令牌管理，为每位接收人填写独立身份（如analyst-wang）并生成。新令牌只显示一次，立即复制并单独交付给该接收人；分享给所有人的ZIP始终不含任何有效令牌。撤销时勾选该身份的确认框。可以撤销最后一枚令牌；MCP会拒绝全部访问，管理员仍可独立登录发放。

元数据文件损坏或不可读时，网页停止发放并提示故障，但继续从授权文件列出有效身份、提供CSRF保护的撤销表单；不得以重建空元数据覆盖原文件。授权文件自身损坏时认证与管理均关闭。登录表单按实际TCP来源限额：最多8个有效挑战、每分钟30次新建；有效Cookie重载复用挑战，10分钟后过期。该限额同样作用于共享同一出口的浏览器。

如需更换管理员口令，在服务器当前受限Windows账户的PowerShell运行以下命令。口令交互不回显，至少16字符；旧管理会话立即失效，不改变接收人的MCP令牌。

```powershell
Set-Location 'D:\LFEN_project\dev_project\complaint-insights'
.venv\Scripts\python.exe scripts/token_desk_admin.py --reset --interactive --username owner
```

不带reset时不会覆盖既有管理员。没有远程重置口令、注册额外管理员或匿名申请签发接口。新增管理员属于后续明确授权范围。

## 精确运行命令

只管理本项目对应服务；manage.ps1会核对进程路径和命令行，隐藏窗口启动。当前生产配置保持allow_production_read=false，watch保持停止。不要运行bootstrap、sync或watch来恢复采集。本任务不管理3030和回环3036。

```powershell
Set-Location 'D:\LFEN_project\dev_project\complaint-insights'
powershell.exe -NoProfile -NonInteractive -File scripts/manage.ps1 -Action Status
powershell.exe -NoProfile -NonInteractive -File scripts/manage.ps1 -Action Start -Service desk -Config '.secrets\production.json'
powershell.exe -NoProfile -NonInteractive -File scripts/manage.ps1 -Action Start -Service mcp -Config '.secrets\production.json'
powershell.exe -NoProfile -NonInteractive -File scripts/mcp-firewall.ps1 -Action Status -Service Portal
```

重启时先对相同Service执行Stop，再Start。重启desk使管理会话和登录挑战失效，不改变已发放的MCP令牌。发放与撤销无需重启MCP；鉴权每次读取当前令牌文件，配置异常则拒绝全部认证。

工具按身份对全部工具合并限频，默认6000次/60秒滑动窗口。HTTP私有配置 `.secrets/mcp-server.json` 可设 `tool_calls_per_minute` 为1至60000的整数，修改后仅重启mcp生效；没有禁用值。stdio使用默认配额。`get_data_guide.tool_rate_limit` 返回当前实际配额。超过配额在读取后端前返回 `isError=true`，错误内容含 `TOOL_RATE_LIMITED` 与 `retry_after_seconds`；等待后重试，完整分页重新运行从首页开始，版本冲突必须丢弃旧页，不能发布半结果。相同身份重新发放令牌不重置当前进程的窗口；重启MCP后窗口重新计数。

防火墙规则 `ComplaintInsights-Portal-3029` 只在Domain/Private配置文件中对192.168.10.20:3029、以太网接口、192.168.10.0/24放行。3037规则保持独立。未添加开机任务；电脑重启后应先确认本地副本与回环查询API由其维护者正常运行，再按上述命令启动两个服务。

## 重建材料与验证

工具签名或文档更改后，从运行中的MCP获取tools/list的result，保存为UTF-8 JSON，执行构建。构建只读取公开文档、模板、CA和schema，不读取凭据。

```powershell
.venv\Scripts\python.exe scripts/mcp_protocol_client.py --config .secrets/mcp-client.json --list-tools | Set-Content -Encoding utf8 -LiteralPath .runtime/mcp-portal-survey/tools-list-live.json
.venv\Scripts\python.exe scripts/build_mcp_handoff.py --schema-file .runtime/mcp-portal-survey/tools-list-live.json --replace-legacy-private-archive
.venv\Scripts\python.exe -m unittest tests.test_token_desk tests.test_mcp -v
.venv\Scripts\python.exe scripts/mcp_portal_verify.py
```

上面的Set-Content明确写UTF-8，构建器同时接受UTF-8有BOM与无BOM。schema仅包含工具定义，不含Bearer或客户数据。兼容入口scripts/verify_mcp.py现调用本次验证器，不再覆盖foundation历史结果。

真实验证器在当前服务器通过内网IP执行。会使用受限初始管理员文件，生成临时验证身份、验证MCP读取并在finally撤销，扫描公开包与运行日志不得出现真实秘密。用户改为自定口令并删除初始文件后，不应重新创建随机管理员来跑验证；人工登录验证管理链路，或在受限环境调整验证凭据输入方式。

当前工程证据见 [第六次返修验证报告](../../T-INSIGHTS-MCP-REPAIR-20261030-06/verification/report.md) 与同目录 `results.json`；检查数量、实际版本及未验项以该次保存结果为准。冻结清单由服务器上该任务正式 `after.json.source_snapshot.file_manifest` 指向，不把仓库内缺失的清单链接当作证据。此前返修及初版测试均为历史证据。验证范围包括11工具、14表入口、原始记录、签发/使用/撤销、材料与客户端完整分页，以及本机可选stdio脚本的原始数值/ID与错误恢复。3张原始空表的空结果保留为合法事实。数据为production-ai-customer历史本地副本；数据版本、DEGRADED状态和同步时间以本次实际报告为准，不宣称与线上实时一致。

## 日志、限制与回滚

日志位于.runtime/desk.err.log和.runtime/mcp.err.log，只有身份标签、动作、状态、请求标识、耗时等，不记录口令、Cookie、CSRF、Bearer、正文或表单。客户端报错时提供X-Request-ID，不提供令牌。

代码与公开配置备份位于.runtime/mcp-portal-backup，未备份秘密。故障时先关闭Portal规则并停止desk：

```powershell
powershell.exe -NoProfile -NonInteractive -File scripts/mcp-firewall.ps1 -Action Disable -Service Portal
powershell.exe -NoProfile -NonInteractive -File scripts/manage.ps1 -Action Stop -Service desk -Config '.secrets\production.json'
```

如恢复旧token_desk代码，只能按旧配置回环运行，禁止把旧无登录发放页暴露内网。不能为了回滚恢复已撤销令牌的旧mcp-server.json。MCP可以独立停止/恢复代码，不触碰生产、回环API、3030或其它项目进程。

正式independent-review与security-privacy-review未取得真实最终决定；用户验收Pending。工程测试通过不表示两轮对抗性审查通过，旧review和Cursor历史未改写。接收方另一台电脑的实际路由、CA安装和本人客户端仍须在该电脑按门户指南验证。
