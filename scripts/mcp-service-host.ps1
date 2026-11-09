param(
    [Parameter(Mandatory=$true)][ValidateSet('mcp','desk')][string]$Service,
    [Parameter(Mandatory=$true)][string]$Config
)
$ErrorActionPreference = 'Stop'
$serviceRoot = [IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
$serviceConfig = [IO.Path]::GetFullPath($Config)
$expectedConfig = Join-Path $serviceRoot '.secrets\production.json'
if ($serviceConfig -ne $expectedConfig) { throw 'Only the existing isolated profile is allowed.' }
$profile = Get-Content -LiteralPath $serviceConfig -Raw | ConvertFrom-Json
if ($profile.allow_production_read -ne $false) { throw 'Production reads must remain isolated.' }
$servicePython = Join-Path $serviceRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $servicePython -PathType Leaf)) { throw 'Project Python is missing.' }
$serviceRuntime = Join-Path $serviceRoot '.runtime'
$serviceOut = Join-Path $serviceRuntime ($Service + '.log')
$serviceErr = Join-Path $serviceRuntime ($Service + '.err.log')
$serviceJournal = Join-Path $serviceRuntime ($Service + '-host.jsonl')
$serviceState = Join-Path $serviceRuntime ($Service + '-host.json')
$servicePort = if ($Service -eq 'mcp') { 3037 } else { 3029 }
$utf8 = New-Object System.Text.UTF8Encoding($false)
foreach ($value in @($servicePython,$serviceConfig,$serviceOut,$serviceErr)) {
    if ($value.IndexOfAny([char[]]'"%&|<>^!') -ge 0) { throw 'Unsupported command path characters.' }
}
function Write-ServiceEvent([string]$Event, [hashtable]$Details) {
    $record = @{ at=[DateTimeOffset]::UtcNow.ToString('o'); service=$Service; event=$Event; host_pid=$PID }
    foreach ($key in $Details.Keys) { $record[$key] = $Details[$key] }
    [IO.File]::AppendAllText($serviceJournal, (($record | ConvertTo-Json -Depth 5 -Compress) + [Environment]::NewLine), $utf8)
    $temporaryState = $serviceState + '.tmp-' + $PID
    [IO.File]::WriteAllText($temporaryState, ($record | ConvertTo-Json -Depth 5), $utf8)
    if (Test-Path -LiteralPath $serviceState) {
        [IO.File]::Replace($temporaryState, $serviceState, [NullString]::Value)
    } else {
        [IO.File]::Move($temporaryState, $serviceState)
    }
}
$serviceMutex = New-Object Threading.Mutex($false, ('Global\ComplaintInsights-' + $Service + '-Host'))
$mutexHeld = $false
try {
    try { $mutexHeld = $serviceMutex.WaitOne(0) }
    catch [Threading.AbandonedMutexException] { $mutexHeld = $true }
    if (-not $mutexHeld) { exit 0 }
    Write-ServiceEvent 'host_started' @{ account=[Security.Principal.WindowsIdentity]::GetCurrent().Name; port=$servicePort }
    $env:PYTHONUNBUFFERED = '1'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    while ($true) {
        $existing = @(Get-NetTCPConnection -State Listen -LocalPort $servicePort -ErrorAction SilentlyContinue)
        if ($existing.Count -gt 0) {
            Write-ServiceEvent 'listener_already_present' @{ listener_pid=$existing[0].OwningProcess; port=$servicePort; retry_after_seconds=10 }
            Start-Sleep -Seconds 10
            continue
        }
        $worker = New-Object Diagnostics.Process
        $worker.StartInfo = New-Object Diagnostics.ProcessStartInfo
        $worker.StartInfo.FileName = $env:ComSpec
        $worker.StartInfo.Arguments = '/d /s /c ""' + $servicePython + '" -m insights.cli ' + $Service + ' --config "' + $serviceConfig + '" 1>> "' + $serviceOut + '" 2>> "' + $serviceErr + '""'
        $worker.StartInfo.WorkingDirectory = $serviceRoot
        $worker.StartInfo.UseShellExecute = $false
        $worker.StartInfo.CreateNoWindow = $true
        $worker.StartInfo.ErrorDialog = $false
        try {
            if (-not $worker.Start()) { throw 'Worker creation failed.' }
            Write-ServiceEvent 'worker_started' @{ wrapper_pid=$worker.Id; port=$servicePort }
            $worker.WaitForExit()
            Write-ServiceEvent 'worker_exited' @{ wrapper_pid=$worker.Id; exit_code=$worker.ExitCode; retry_after_seconds=10 }
        } catch {
            Write-ServiceEvent 'worker_start_failed' @{ error_type=$_.Exception.GetType().Name; retry_after_seconds=10 }
        } finally {
            $worker.Dispose()
        }
        Start-Sleep -Seconds 10
    }
} catch {
    Write-ServiceEvent 'host_failed' @{ error_type=$_.Exception.GetType().Name }
    exit 1
} finally {
    if ($mutexHeld) { $serviceMutex.ReleaseMutex() }
    $serviceMutex.Dispose()
}
