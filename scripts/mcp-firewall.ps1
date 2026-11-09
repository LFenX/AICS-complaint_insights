param(
    [ValidateSet('Enable','Disable','Status')][string]$Action='Status',
    [ValidateSet('MCP','Portal')][string]$Service='MCP'
)
$ErrorActionPreference='Stop'
$insightsMcpRoot=Split-Path -Parent $PSScriptRoot
$insightsMcpConfig=Get-Content -LiteralPath (Join-Path $insightsMcpRoot '.secrets\mcp-server.json') -Raw | ConvertFrom-Json
$insightsMcpListenPort=if ($Service -eq 'Portal') { 3029 } else { $insightsMcpConfig.port }
$insightsMcpRuleName='ComplaintInsights-' + $Service + '-' + $insightsMcpListenPort
$insightsMcpOwner='Owner=' + $insightsMcpRoot
$insightsMcpRule=Get-NetFirewallRule -Name $insightsMcpRuleName -ErrorAction SilentlyContinue
if ($insightsMcpRule -and $insightsMcpRule.Description -ne $insightsMcpOwner) { throw 'Firewall rule name belongs to another owner' }
if ($Action -eq 'Enable') {
    if ($insightsMcpRule) { Enable-NetFirewallRule -Name $insightsMcpRuleName | Out-Null }
    else {
        $insightsMcpInterface=(Get-NetIPAddress -AddressFamily IPv4 -IPAddress $insightsMcpConfig.host).InterfaceAlias
        New-NetFirewallRule -Name $insightsMcpRuleName -DisplayName ('Complaint Insights ' + $Service + ' (HTTPS)') -Group 'ComplaintInsights' -Description $insightsMcpOwner -Direction Inbound -Action Allow -Enabled True -Protocol TCP -LocalPort $insightsMcpListenPort -LocalAddress $insightsMcpConfig.host -RemoteAddress $insightsMcpConfig.allowed_networks -Profile Domain,Private -InterfaceAlias $insightsMcpInterface | Out-Null
    }
}
elseif ($Action -eq 'Disable' -and $insightsMcpRule) { Disable-NetFirewallRule -Name $insightsMcpRuleName | Out-Null }
$insightsMcpRule=Get-NetFirewallRule -Name $insightsMcpRuleName -ErrorAction SilentlyContinue
if ($insightsMcpRule) {
    $insightsMcpPorts=$insightsMcpRule | Get-NetFirewallPortFilter
    $insightsMcpAddresses=$insightsMcpRule | Get-NetFirewallAddressFilter
    [pscustomobject]@{name=$insightsMcpRule.Name;enabled=[string]$insightsMcpRule.Enabled;profile=[string]$insightsMcpRule.Profile;local_port=$insightsMcpPorts.LocalPort;local_address=$insightsMcpAddresses.LocalAddress;remote_address=$insightsMcpAddresses.RemoteAddress} | ConvertTo-Json -Compress
} else { Write-Output '{"configured":false}' }
