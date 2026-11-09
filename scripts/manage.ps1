param(
    [ValidateSet('Start','Stop','Status')][string]$Action = 'Status',
    [ValidateSet('All','serve','watch','mcp','desk','board')][string]$Service = 'All',
    [string]$Config = ''
)
$ErrorActionPreference = 'Stop'
$insightsRoot = Split-Path -Parent $PSScriptRoot
$insightsPython = Join-Path $insightsRoot '.venv\Scripts\python.exe'
if (-not $Config) { $Config = Join-Path $insightsRoot '.secrets\local.json' }
$Config = [System.IO.Path]::GetFullPath($Config)
$insightsRuntime = Join-Path $insightsRoot '.runtime'
$insightsPidFile = Join-Path $insightsRuntime 'processes.json'
$insightsProcesses = @{}
if (Test-Path -LiteralPath $insightsPidFile) {
    $storedProcesses = Get-Content -LiteralPath $insightsPidFile -Raw | ConvertFrom-Json
    foreach ($entry in $storedProcesses.PSObject.Properties) { $insightsProcesses[$entry.Name] = $entry.Value }
}
function Get-InsightsProcess([string]$Kind) {
    if (-not $insightsProcesses.ContainsKey($Kind)) { return $null }
    $record = $insightsProcesses[$Kind]
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$($record.process_id)" -ErrorAction SilentlyContinue
    if ($process -and $process.CommandLine -like "*$insightsRoot*" -and $process.CommandLine -like "*-m insights.cli $Kind*") { return $process }
    return $null
}
if ($Action -eq 'Start') {
    $insightsKinds = @('serve','watch')
    if (Test-Path -LiteralPath (Join-Path $insightsRoot '.secrets\mcp-server.json')) { $insightsKinds += 'mcp' }
    $insightsKinds += 'desk'
    $insightsKinds += 'board'
    foreach ($kind in $insightsKinds) {
        if ($Service -ne 'All' -and $kind -ne $Service) { continue }
        if ($kind -eq 'watch') {
            $profile = Get-Content -LiteralPath $Config -Raw | ConvertFrom-Json
            if ($profile.environment -eq 'production' -and -not $profile.allow_production_read) {
                if ($Service -eq 'watch') { throw 'Production reads are isolated in this profile. The collector was not started.' }
                Write-Warning 'Production reads are isolated; skipping watch.'
                continue
            }
        }
        if (Get-InsightsProcess $kind) {
            if ($insightsProcesses[$kind].config -ne $Config) { throw 'A different profile is running. Stop this project before changing profiles.' }
            continue
        }
        $logPath = Join-Path $insightsRuntime "$kind.log"
        $errorPath = Join-Path $insightsRuntime "$kind.err.log"
        $process = Start-Process -FilePath $insightsPython -ArgumentList @('-m','insights.cli',$kind,'--config',('"' + $Config + '"')) -WorkingDirectory $insightsRoot -WindowStyle Hidden -RedirectStandardOutput $logPath -RedirectStandardError $errorPath -PassThru
        $insightsProcesses[$kind] = @{ process_id=$process.Id; config=$Config; started_at=[DateTimeOffset]::UtcNow.ToString('o') }
    }
    $insightsProcesses | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $insightsPidFile -Encoding UTF8
}
elseif ($Action -eq 'Stop') {
    foreach ($kind in @('board','desk','mcp','watch','serve')) {
        if ($Service -ne 'All' -and $kind -ne $Service) { continue }
        $process = Get-InsightsProcess $kind
        if ($process) {
            # Windows venv Python can have a child interpreter. Kill only the verified
            # project process tree so a hidden child cannot retain the port.
            & taskkill.exe /PID $process.ProcessId /T /F | Out-Null
        }
    }
}
$state = foreach ($kind in @('serve','watch','mcp','desk','board')) {
    $process = Get-InsightsProcess $kind
    [pscustomobject]@{ service=$kind; running=[bool]$process; process_id=if ($process) { $process.ProcessId } else { $null } }
}
$state | ConvertTo-Json -Compress
