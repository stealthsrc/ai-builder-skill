[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)]
    [string]$Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$resolved = (Resolve-Path -LiteralPath $Path).Path

if ($PSCmdlet.ShouldProcess($resolved, "Inspect item")) {
    Get-Item -LiteralPath $resolved | Select-Object FullName, Length, LastWriteTime
}
