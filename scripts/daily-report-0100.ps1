# Daily 01:00 Beijing-time launcher. The run must finish without asking the user.
param(
    [string]$Date = ''
)
$ErrorActionPreference = 'Continue'
$projectRoot = 'D:\LFEN_project\dev_project\complaint-insights'
$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
$policy = Join-Path $projectRoot 'scripts\daily-report-unattended-policy.json'
$logDir = Join-Path $projectRoot '.runtime\daily-schedule'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$log = Join-Path $logDir ("run-{0}.log" -f $stamp)
function Write-Log([string]$Message) {
    Add-Content -LiteralPath $log -Value ('{0} {1}' -f (Get-Date).ToString('o'), $Message) -Encoding utf8
}
Set-Location -LiteralPath $projectRoot
if (-not $Date) {
    $Date = & $python -c "from datetime import datetime, timedelta; from zoneinfo import ZoneInfo; print((datetime.now(ZoneInfo('Asia/Shanghai')).date()-timedelta(days=1)).isoformat())"
}
Write-Log "daily-report-0100 start date=$Date"
if (Test-Path -LiteralPath (Join-Path $projectRoot ".runtime\daily-reports\$Date\report.json")) {
    Write-Log "published report exists; verifying the stored evidence without a new capture or local freeze"
    & $python -m insights.daily_generation prepare --date $Date *>> $log
    $verifyCode = $LASTEXITCODE
    Write-Log "published verify exit $verifyCode"
    exit $verifyCode
}
if (Get-Command docker -ErrorAction SilentlyContinue) {
    $running = docker inspect complaint-insights-postgres --format '{{.State.Running}}' 2>$null
    if ($running -ne 'true') {
        Write-Log 'starting Docker Desktop and local analytics container'
        $desktop = 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
        if (Test-Path -LiteralPath $desktop) { Start-Process -FilePath $desktop | Out-Null }
        for ($i = 0; $i -lt 40; $i++) {
            docker info --format '{{.ServerVersion}}' 1>$null 2>$null
            if ($LASTEXITCODE -eq 0) { break }
            Start-Sleep -Seconds 3
        }
        docker start complaint-insights-postgres 1>>$log 2>&1
    }
}
Write-Log 'capturing the closed day from production; local replica freeze is not used'
& $python (Join-Path $projectRoot 'scripts\capture_fresh_closed_day.py') --date $Date *>> $log
$captureCode = $LASTEXITCODE
Write-Log "production capture exit $captureCode"
if ($captureCode -ne 0) {
    Write-Log 'fresh production capture failed; the report stays unpublished'
    exit $captureCode
}
$wake = Join-Path $logDir 'session-wake.json'
$prompt = "你在本机这个 Cursor 会话里无人值守地生成客诉日报，禁止向用户提问。先读 $policy 。项目根 $projectRoot 。目标日期是 $Date 。source.json 已由生产库只读补采写好。不要再连生产库，不要运行 freeze_covered_local_day.py，不要调用 agent 命令行，不要改 allow_production_read，不要启动 watch，不要推进全局水位。已有正式报告就核验后停止，不覆盖。附件原件若已不在补采到的 IMAP 邮件里，只跳过该文件、保留邮件，并按策略写入 attachment-exceptions.json，然后继续。逐封阅读、看实际图片和工单截图、沿用最近已发布子问题名，build、check、publish。完成后核验 http://127.0.0.1:3030/?date=$Date 。失败只记录精确缺口，不要说已生成。"
@{ date = $Date; written_at = (Get-Date).ToString('o'); prompt = $prompt } | ConvertTo-Json -Compress | Set-Content -LiteralPath $wake -Encoding utf8
Write-Log "production capture is ready for the open Cursor session; wake file $wake"
exit 0
