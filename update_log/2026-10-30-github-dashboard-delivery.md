# 2026-10-30 看板源码交付与内网访问

记录时间：2026-10-30 05:47（Asia/Shanghai）。

## 变更

- `insights/`、`assets/`、`config/`、`tests/`：保留现有看板、读取模型生成、附件预览及子问题日志ZIP实现和相对路径；22项交付源码摘要记录在 `SOURCE_MANIFEST.json`。
- `insights/daily_board.py`、`insights/capabilities.py`、`tests/test_daily_network.py`：按明确授权增加可选的精确内网地址、双监听、RFC1918访问网段、真实TCP来源、Host/Origin校验和元数据审计。默认仍仅回环；不会通过HTTP请求读取源数据库。
- `config/daily-board.example.json`、`scripts/daily-board-firewall.ps1`：提供无凭据的配置示例与本目录所属的Windows防火墙管理。网络配置存放在被忽略的 `.secrets/daily-board.json`。
- `README.md`、依赖清单、锁定文件、Git忽略和属性：补充独立安装、私有输入、启动、内网访问、关闭和数据范围说明，保留第三方许可。

## 实际验证

- Windows / Python3.13，独立新虚拟环境实际安装依赖成功。
- `python -m unittest discover -s tests -v`：24项通过。
- `python -m pip check`：无依赖冲突。
- `node --check assets/daily-board.js` 与PowerShell解析检查通过。
- 暂存区按Windows CRLF语义检查空白，保留原始源码已有的两条提示：`assets/daily-board.js:231` 末尾空行、`insights/config.py:45` 尾随空格。这两个文件与原始交付SHA完全一致；未把此项记为零告警通过。
- 实际服务的本地/内网地址均完成页面、数据、邮件详情、附件SHA、ZIP CRC、静态资源SHA、非法Host/Origin403、写入405、旧报告版本409验证。
- 生产读取保持关闭，采集进程停止，其他服务PID、配置及启动时刻未变。未从第二台电脑实测，未开展本轮多轮对抗性审查，未把测试结果记为人工安全隐私门禁通过。

## 交付边界

此仓库只保存源码和使用资料；真实邮件、UID证据、附件、读取模型、数据库快照、凭据、证书及运行日志不在提交范围。当前默认日报路径固定为2026-10-29；没有业务输入时数据接口返回503。Git提交和远端SHA以实际仓库历史为准。

## 本机部署与远端证明

内网入口：http://192.168.10.20:3030/；GitHub提交：https://github.com/LFenX/AICS-CCDD/commit/d36486b27f1a9a92edb35aa825df09a8dd0edb5b。实际提交/tree/文件清单复核见`.runtime/github-delivery-20261030/remote-verification.json`；内网验证见`.runtime/github-delivery-20261030/lan-verification.json`。私有配置和真实读取产物只保留在本机。


## 后续安全隐私决定（2026-10-30T14:14:06.678441+08:00）

用户原话：“通过本轮门禁”。本轮security-privacy-review已通过，决定登记为`.project-governance/authority/ACD-INSIGHTS-LAN-20261030-01.json`，原始问题/回答及交付摘要见`LG_project_docs/requirements/T-INSIGHTS-GITHUB-20261030-01/verification/security-gate-decision.json`。22项源码摘要未变，内网HTTP200，634封同版模型可读；另一台电脑仍未实测。此前待审文字及旧Run保留当时历史，不再重复请求相同门禁。整体用户Acceptance及可选多轮审查各自独立。
