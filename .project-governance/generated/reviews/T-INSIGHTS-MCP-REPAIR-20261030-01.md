# Task Review: T-INSIGHTS-MCP-REPAIR-20261030-01

- Objective: 修复已授权MCP审查发现并验证当前交付
- Contract revision: 2
- Contract state: Frozen
- Depends on: T-INSIGHTS-MCP-PORTAL-20261030-01

## Acceptance criteria

- 同一匿名来源重复刷新或清除Cookie不能耗尽另一来源登录页；限制有期限且不扩大登录权限
- registry损坏时独立管理员可在网页列出有效身份和撤销，发放仍拒绝；授权文件损坏保持全部拒绝
- 工具调用执行前按公布JSON Schema验证类型/日期/额外参数；无效输入不查询后端，未知工具为JSON-RPC -32602
- 全部单测、真实TLS签发查询撤销、11工具14表和接收人客户端验证通过；只重启3029/3037，生产读取关闭
- 原话全部覆盖，保存版本摘要和真实限制；不把普通测试或开始审查冒充正式人工门禁批准

## Outcome

- Status: Deferred
- User decision: 待用户验收
- Adversarial review: {'status': 'NotApplicable', 'clean_streak': 0, 'rounds': 0, 'open_findings': [], 'current_delivery': {'task_id': 'T-INSIGHTS-MCP-REPAIR-20261030-01', 'subject_sha256': '54320013394c6bd06bbe598bdbca6aae785cac5c979b180b7d929ba18e9d3b97'}}
- Revision: 1

## Established facts

- 四项缺陷修复并验证，45文件版本已固定；正式人类门禁Pending及后续完整审查待完成

## Actual changes

- 按来源限额和复用挑战；元数据故障保留网页撤销；SDK转换前JSON Schema校验；未知工具顶层-32602；公共指南和无凭据包同步更新

## Verification

- Passed: 30项单测和契约测试通过
- Passed: 严格CA真实内网13检查、11工具14表、22页和登录签发使用撤销退出通过

## Evidence

- LG_project_docs/requirements/T-INSIGHTS-MCP-REPAIR-20261030-01/verification/coverage.json

## Incomplete items

- 正式人类门禁Pending; reason=independent-review与security-privacy-review没有真实通过决定; impact=工程已验证，正式Gate不可标为通过; owner=用户或有权审查者; reentry=对当前交付给出真实可核对决定
- 异机路径未实测; reason=另一内网电脑路由和CA安装未测试; impact=仅本机经内网IP严格CA已验证; owner=接收人; reentry=另一电脑按公开指南复验
- 修复版后续审查进行中及机器登记受限; reason=父Deferred导致Offer拒绝；当前返修已验证，独立后续轮次尚未完成; impact=不能宣称官方审查Passed或两轮收敛; owner=当前任务执行者; reentry=完成同版本两轮真实完整审查；官方登记仍需合法父工程前置状态，不绕过门禁

## Legacy issues


## Decisions


## Next tasks


## Terminal artifact manifest

- T-INSIGHTS-MCP-REPAIR-20261030-01-before / TaskContract / Create/Revise / Created
- T-INSIGHTS-MCP-REPAIR-20261030-01-run / RunLedger / Create/Revise / Created
- T-INSIGHTS-MCP-REPAIR-20261030-01-after / TaskOutcome / Create/Revise / Created
- T-INSIGHTS-MCP-REPAIR-20261030-01-prd / AuthorityAsset / Create/Revise / Created
- T-INSIGHTS-MCP-REPAIR-20261030-01-tds / AuthorityAsset / Create/Revise / Created
- T-INSIGHTS-MCP-REPAIR-20261030-01-ver / AuthorityAsset / Create/Revise / Created
- T-INSIGHTS-MCP-REPAIR-20261030-01-rcr / DerivedView / Generate / Generated
- T-INSIGHTS-MCP-REPAIR-20261030-01-rlc / AuthorityAsset / Create/Revise / Created

## Amendments

- r1→r2 requirement_items: 按真实结果交代：账号入口和开始指令Covered；连续两轮仍进行中，R-02 Deferred，不伪造完成 (basis: LG_project_docs/requirements/T-INSIGHTS-MCP-REPAIR-20261030-01/verification/coverage.json)

## Proof validation

当前契约记录校验通过（不替代人的验收）
