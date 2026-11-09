# Task Review: T-INSIGHTS-REPAIR-20261029-02

- Objective: 修复第二轮确认的连接串隐式主机、端口和数据库名校验缺陷
- Contract revision: 3
- Contract state: Frozen
- Depends on: T-INSIGHTS-REVIEW-20261029-01

## Acceptance criteria

- 省略主机、端口或数据库名的连接串在建立连接前被拒绝，PGHOST、PGPORT、PGDATABASE 不能代替这三项
- 已写明主机、端口和数据库名的连接串，在上述环境变量指向其他地址时身份保持为连接串中的值
- 既有 hostaddr 与 service 拒绝仍然有效，当前显式本地配置的规则测试通过

## Outcome

No engineering result recorded.

## Proof validation

活动记录；尚未进行终态证明校验
