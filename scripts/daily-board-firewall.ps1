param([ValidateSet('Enable','Disable','Status')][string]$Action='Status')
$ErrorActionPreference='Stop'
$insightsBoardRoot=Split-Path -Parent $PSScriptRoot
$insightsBoardRuleName='ComplaintInsights-DailyBoard-3030'
$insightsBoardOwner='Owner=' + $insightsBoardRoot
$insightsBoardRule=Get-NetFirewallRule -Name $insightsBoardRuleName -ErrorAction SilentlyContinue
if ($insightsBoardRule -and $insightsBoardRule.Description -ne $insightsBoardOwner) {
    throw 'Firewall rule name belongs to another owner'
}
if ($Action -eq 'Enable') {
    $insightsBoardPython=Join-Path $insightsBoardRoot '.venv\Scripts\python.exe'
    $insightsBoardConfigPath=Join-Path $insightsBoardRoot '.secrets\daily-board.json'
    # Use the application's own validation, rather than duplicating CIDR rules.
    Push-Location -LiteralPath $insightsBoardRoot
    try {
        $insightsBoardRaw=& $insightsBoardPython -c "from insights.daily_board import BoardNetwork; import json,sys; from pathlib import Path; n=BoardNetwork.load(Path(sys.argv[1])); print(json.dumps({'lan_host':n.lan_host,'allowed_networks':n.allowed_networks}))" $insightsBoardConfigPath
        if ($LASTEXITCODE -ne 0) { throw 'Daily board network configuration is invalid' }
        $insightsBoardConfig=$insightsBoardRaw | ConvertFrom-Json
    } finally { Pop-Location }
    if (-not $insightsBoardConfig.lan_host) { throw 'Explicit LAN configuration is required' }
    $insightsBoardNic=@(Get-NetIPAddress -AddressFamily IPv4 -IPAddress $insightsBoardConfig.lan_host -ErrorAction Stop)
    if ($insightsBoardNic.Count -ne 1) { throw 'LAN address does not resolve to exactly one interface' }
    $insightsBoardParameters=@{
        Name=$insightsBoardRuleName; Direction='Inbound'; Action='Allow'; Enabled='True';
        Protocol='TCP'; LocalPort=3030; LocalAddress=$insightsBoardConfig.lan_host;
        RemoteAddress=$insightsBoardConfig.allowed_networks; Profile=@('Domain','Private');
        InterfaceAlias=$insightsBoardNic[0].InterfaceAlias
    }
    if ($insightsBoardRule) {
        Set-NetFirewallRule @insightsBoardParameters | Out-Null
    } else {
        New-NetFirewallRule @insightsBoardParameters -DisplayName 'Complaint Insights Daily Board (3030)' -Group 'ComplaintInsights' -Description $insightsBoardOwner | Out-Null
    }
} elseif ($Action -eq 'Disable' -and $insightsBoardRule) {
    Disable-NetFirewallRule -Name $insightsBoardRuleName | Out-Null
}
$insightsBoardRule=Get-NetFirewallRule -Name $insightsBoardRuleName -ErrorAction SilentlyContinue
if ($insightsBoardRule) {
    $insightsBoardPort=$insightsBoardRule | Get-NetFirewallPortFilter
    $insightsBoardAddress=$insightsBoardRule | Get-NetFirewallAddressFilter
    [pscustomobject]@{
        name=$insightsBoardRule.Name; enabled=[string]$insightsBoardRule.Enabled; profile=[string]$insightsBoardRule.Profile;
        local_port=$insightsBoardPort.LocalPort; local_address=$insightsBoardAddress.LocalAddress;
        remote_address=$insightsBoardAddress.RemoteAddress
    } | ConvertTo-Json -Compress
} else { Write-Output '{"configured":false}' }
