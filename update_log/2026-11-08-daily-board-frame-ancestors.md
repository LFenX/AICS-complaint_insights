# 客诉日报允许指定父页面内嵌

时间：2026-11-08T17:41:47+08:00。只改日报 Web 服务。AICS、MCP、采集和生成进程未重启。

你的需求已经描述的非常清楚了，并且和项目现状一致，本次跳过向你提问的阶段。

## 变更文件

- `insights/daily_board.py`：新增可选 `frame_ancestor_origins`。未配置或空列表时，主页面 CSP 仍是 `frame-ancestors 'none'`。配置后只把精确来源写入 `frame-ancestors`。来源必须是单个 http/https origin；`*`、路径、查询、片段、用户信息、IPv6 和非法端口会在启动前报错。浏览器默认端口会折叠成同一个 origin，`http://10.8.45.155:80` 与 `http://10.8.45.155` 相同，`http://10.8.45.155:3025` 仍然不同。Host、客户端网段、只读方法和权限检查保持原样。允许的父页面 Origin 只是额外的精确匹配，不代替网段校验，也不增加 CORS 响应头。`Cross-Origin-Resource-Policy` 保持 `same-origin`。附件下载仍使用 `default-src 'none'; sandbox`。没有 `X-Frame-Options`，也没有第二条 CSP。
- `insights/capabilities.py`：日报和日志包的审计说明改为“Origin 缺省、与 Host 相同，或精确命中已配置的父页面来源”。
- `config/daily-board.example.json`：补充空的 `frame_ancestor_origins`，示例本身不允许内嵌。
- `.secrets/daily-board.json`：当前部署加入 `http://10.8.45.155`。没有加入 `http://10.8.45.155:3025`。
- `tests/test_daily_network.py`：覆盖未配置、空列表、已配置、默认端口、其他端口、通配符和非法来源，以及网段、Host、只读、附件 sandbox 和单条 CSP。

## 配置

`.secrets/daily-board.json` 在原有 `lan_host` 和 `allowed_networks` 之外增加：

```json
"frame_ancestor_origins": [
  "http://10.8.45.155",
  "http://127.0.0.1",
  "http://localhost",
  "http://10.8.61.200"
]
```

本机默认 80 端口之外，本地 AICS 开发服务 `3016` 也已加入：`http://127.0.0.1:3016`、`http://localhost:3016`、`http://10.8.61.200:3016`。`http://10.8.61.200:3017` 和其他未列出的端口仍然是不同来源。

省略该字段或使用空数组时，行为与升级前相同，继续禁止内嵌。

## 实际验证

- `tests.test_daily_network`、`tests.test_daily_dates`、`tests.test_daily_report.DailyBoundaryTests`、`tests.test_log_archive`：28 项通过。
- 隔离浏览器试验：`Cross-Origin-Resource-Policy: same-origin` 配合 `frame-ancestors http://127.0.0.1:8765` 时，父页面能载入子文档；父页面换成 `http://127.0.0.1:8766` 时，iframe 停在 `chrome-error://chromewebdata/`。没有关闭浏览器安全检查。
- 隔离日报进程只监听 `127.0.0.1:3030`，父页面白名单只有 `http://127.0.0.1:8765`，读取现有本地报告。`http://127.0.0.1:8765` 内嵌后渲染了 2026-11-07 日报；`http://127.0.0.1:8766` 被浏览器阻止。
- 生产进程切换只处理了当时占用 3030 的日报进程。进程记录里的旧 PID 已经不在，实际停止的是命令行为 `insights.cli board` 的 PID 45144。随后只用 `scripts/manage.ps1 -Action Start -Service board` 启动。当前监听是 `127.0.0.1:3030` 和 `10.8.61.200:3030`，子进程 12912。3029、3036、3037 的监听进程没有变化。
- 生产响应：主页面 CSP 为原有指令加上 `frame-ancestors http://10.8.45.155`；没有 `X-Frame-Options`，没有 `Access-Control-Allow-Origin`，`Cross-Origin-Resource-Policy` 为 `same-origin`。`Origin: http://10.8.45.155` 返回 200，`Origin: http://10.8.45.155:3025` 返回 403。`POST /data.json` 返回 405。
- 浏览器直接打开生产日报：日历从 2026-11-07 切到 2026-11-01，搜索邮件编号，打开原信正文。PDF 首页预览为 1132×1600 图片，下载得到 `%PDF-1.4` 且 CSP 为 sandbox。回到 2026-11-07 后，图片预览为 1800×1012，文本预览载入 260217 字符，视频 `readyState` 为 4，Range 请求返回 206 和 MP4 `ftyp`，CSP 仍是 sandbox。
- 生产配置生效后，`http://127.0.0.1:8765` 再内嵌 `http://127.0.0.1:3030/` 被浏览器阻止。
- 随后按要求加入本机来源并只重启 board。浏览器从 `http://127.0.0.1/parent.html` 内嵌，子页面载入 2026-11-07 日报，25 行原信。预览页同时可由 `http://localhost/parent.html` 和 `http://10.8.61.200/parent.html` 打开。

## 未验证

- AICS 生产页面尚未接入，真实生产内嵌联调未做，不能标为通过。
- 没有另找一台 10.8.0.0/16 以外的客户机重复网段拒绝；该拒绝由自动化测试覆盖。
- 没有修改或重启 AICS、MCP、采集和日报生成进程，也没有对它们做本次变更的回归。

## 升级步骤

本次升级已经完成，步骤如下，供复核：

1. 更新日报代码和 `.secrets/daily-board.json`。
2. 确认占用 3030 的进程命令行是 `insights.cli board` 后，只停止该进程树。
3. 运行 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\manage.ps1 -Action Start -Service board`。
4. 核对启动日志中的 `frame_ancestor_origins` 只有 `http://10.8.45.155`，并且 3029、3036、3037 仍由原进程监听。

## 回滚

只操作 3030 日报服务。

- 保留新代码、只关闭内嵌：从 `.secrets/daily-board.json` 删除 `frame_ancestor_origins`，按上面的方式只重启 board。主页面会回到 `frame-ancestors 'none'`。
- 连代码一起退回：先删除该配置项，再恢复本次变更的代码和测试，然后只重启 board。旧代码遇到未知配置项会拒绝启动，所以不能在配置仍含该字段时退回旧代码。

用户验收仍为 Pending。
