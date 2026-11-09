# MCP与门户独立运行维护

生效日期：2026-11-01。当前由Windows任务计划程序托管，取代原普通后台进程运行方式。旧版本交接中的“未添加开机任务”和普通manage.ps1流程是历史运行方式。

|服务|入口|计划任务|
|---|---|---|
|MCP|https://10.8.61.200:3037/mcp|ComplaintInsights-MCP-3037|
|门户|https://10.8.61.200:3029/|ComplaintInsights-Portal-3029|

两个任务使用当前Windows账户、S4U和Limited权限，不保存账户密码，不增加SYSTEM权限。任务执行时长不限、允许电池运行、忽略重复实例；开机20秒后启动，每分钟重复触发检查托管器，运行中不重复启动。

scripts/mcp-service-host.ps1仅接受mcp或desk以及现有隔离production.json。服务退出后等待10秒再启动。全局互斥避免重复托管；端口已有监听时只记录并等待，不终止未知进程。

实际托管父链为powershell.exe → svchost.exe → services.exe → wininit.exe。无需保持ChatGPT打开。整机重启和注销没有为本次验证实际执行。

## 状态和启动

~~~powershell
Get-ScheduledTask -TaskName 'ComplaintInsights-MCP-3037','ComplaintInsights-Portal-3029'
Get-ScheduledTaskInfo -TaskName 'ComplaintInsights-MCP-3037'
Get-ScheduledTaskInfo -TaskName 'ComplaintInsights-Portal-3029'
Enable-ScheduledTask -TaskName 'ComplaintInsights-MCP-3037' | Out-Null
Enable-ScheduledTask -TaskName 'ComplaintInsights-Portal-3029' | Out-Null
Start-ScheduledTask -TaskName 'ComplaintInsights-MCP-3037'
Start-ScheduledTask -TaskName 'ComplaintInsights-Portal-3029'
~~~

State=Running表示常驻托管器运行，LastTaskResult=267009（0x41301）表示任务仍在运行。

旧.runtime/processes.json中的mcp/desk PID是普通后台时代的历史值。以计划任务、实际端口和*-host.json为准，不使用manage.ps1 -Service All操作这些任务或其它服务。

## 维护停用与回滚

计划维护时，先禁用对应任务自动触发，再停止该任务。只停止而不禁用会在下次一分钟触发时恢复。停止后必须检查对应3029或3037端口是否释放。如果仍有监听，维护者应核验具体PID、命令行中的项目根和insights.cli服务名后，仅结束该服务进程，不停止未知进程或其它项目。

完整撤销本次托管时，仅注销上表两个任务；不得恢复旧令牌存储或更改其它任务。重新启用使用上面的Enable/Start命令。完整停用/注销回滚未在本次演练。

## 日志与调查

- .runtime/mcp.err.log、desk.err.log：继续追加的应用日志。
- .runtime/mcp-host.jsonl、desk-host.jsonl：UTC时间、托管PID、worker wrapper PID、退出码、自动恢复事件。
- .runtime/mcp-host.json、desk-host.json：最近的托管状态。
- Windows任务计划程序Operational：任务启动与结束事件。
- 本任务verification/before/：完整保全的旧日志和进程记录。

原停止日志没有退出时间、退出码或进程终止审计，不能确证直接触发原因。连接重置回调异常不等同于进程退出。已确认的运维缺口是原普通后台模式没有独立托管和自动恢复。

本次两个服务分别完成受控终止后的自动恢复；MCP自有worker退出码-1已记录，11.81秒自动恢复。原密钥、管理员和生产配置哈希不变，3030/3036/15433进程不变，采集仍停止。

首次托管器的Windows PowerShell状态文件兼容问题及其修正记录保留在verification目录，不隐藏失败。
