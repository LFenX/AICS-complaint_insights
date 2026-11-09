# 隐式数据库目的地勘察

用户原话：先把修复做了呗

## 相关位置

- `insights/config.py` 的 `connection_identity` 与 `Settings.validate`
- `tests/test_rules.py` 已有 `hostaddr` / `PGHOSTADDR` / `PGSERVICE` 拒绝用例
- 第二轮证据：`.project-governance/tasks/T-INSIGHTS-REVIEW-20261029-01/evidence/round-2-results.json` 的 `R2-01`
- 复现探针：同目录 `round-2-probe.py` 的 `destination_environment`

## 现有实现

`conninfo_to_dict` 只返回连接串里写明的参数。主机、端口或数据库名被省略时，字典里没有对应键。`connection_identity` 再用 `localhost`、`5432` 和空库名补齐，并据此做回环、端口、来源隔离和生产门禁判断。

libpq 在参数省略时改用 `PGHOST`、`PGPORT`、`PGDATABASE`。探针在隔离库上复现：校验身份是 `localhost:5432`，实际连接是环境变量给出的地址。离线用例里，指向 `203.0.113.1:6543` 的环境变量仍能通过校验。

已显式写出主机、端口和数据库名时，libpq 使用连接串，不用上述环境默认值。当前 `.secrets/local.json` 和 `config/production.example.json` 的 URL 都带这三项。`hostaddr`、`service`、`PGHOSTADDR`、`PGSERVICE` 已在连接前拒绝。

## 既有约定

目的地必须和来源身份绑定，生产读取默认关闭，目标库固定为回环 `15433` 上的 `complaint_insights`。测试用 `Settings.load()` 和 `assertRaisesRegex`，不连接被拒绝的地址。

## 分歧点

没有未决分歧。第二轮已选定：拒绝缺少主机、端口或数据库名的连接串，保留现有 `hostaddr` / `service` 拒绝；不解析并固化全部 libpq 环境默认值。生产监听变更不在本次修复内。
