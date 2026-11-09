# 客诉数据底座审查返修

记录时间：2026-10-29 19:03（Asia/Shanghai）。任务：T-INSIGHTS-REVIEW-20261029-01。

## 变更

- `insights/syncer.py`：把静态分类文件加载纳入已有失败处理。缺文件或无效 JSON 会记录 `DEGRADED`、错误码与失败运行，保留已发布数据、版本和水位；下一次成功恢复 `READY`。
- `insights/config.py`：在创建连接前拒绝 URL 的 `hostaddr/service` 以及进程环境的 `PGHOSTADDR/PGSERVICE`，防止 libpq 将实际目的地址替换到已验证的 host 之外。使用显式主机地址连接。
- `tests/test_rules.py`、`tests/test_integration.py`：增加目的地址覆盖与分类文件失败/恢复的三项回归测试，实际数据库夹具只创建在新实例 15433。
- `README.md`、原需求 `release/mcp-handoff.md`：Python 最低版本改为 3.11，与固定客户端依赖一致。
- `.secrets/mcp-handoff.zip`：使用现有凭据重新打包最新手册；未改变令牌或私钥。私有包不纳入公开文件清单。
- `LG_project_docs/requirements/T-INSIGHTS-REVIEW-20261029-01/`、`.project-governance/`：保存真实授权、原始预审反例、验证与后续完整审查报告。`LG_project_docs/README.md` 由任务初始化工具更新索引。

## 实际验证

- `python -m unittest discover -s tests -v`：50 项通过，17.662 秒；日志 `.runtime/unittest-review-fixes.log`。
- 本项目三个进程停止后重新启动，加载修复代码；未操作原业务服务和生产服务器。
- 内网 IP 的真实 HTTPS MCP：严格校验证书，发现 11 个工具，同步来源 `development-local`，状态 `READY`。
- 新交接包 11 个文件，手册已写 Python 3.11+；包摘要见本任务 `verification/fix-results.json`。
- 十四表逐行内容核对、增量乱序提交、断线恢复、五类分页和全部工具的第一轮独立证据见 `evidence/round-1-results.json`。

第一轮发现三项问题，不能计为无问题轮次。后续完整审查的实际结果单独记录，不能用本次普通回归代替。

## 未执行

未接入生产、未重启生产 PostgreSQL、未在另一台内网电脑执行路由及客户端验收。当前仍为开发数据副本。
