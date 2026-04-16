[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)]
    [string]$FolderPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$resolvedFolder = (Resolve-Path -LiteralPath $FolderPath).Path
$pattern = '(?<year>20\d{2})[-_ ]?(?<month>\d{2})[-_ ]?(?<day>\d{2})'

Get-ChildItem -LiteralPath $resolvedFolder -Filter *.pdf -File | ForEach-Object {
    $match = [regex]::Match($_.BaseName, $pattern)
    if (-not $match.Success) {
        Write-Host "Skipping '$($_.Name)' because no date was found."
        return
    }

    $datePrefix = "{0}-{1}-{2}" -f $match.Groups["year"].Value, $match.Groups["month"].Value, $match.Groups["day"].Value
    $newName = "{0}_{1}" -f $datePrefix, $_.Name

    if ($_.Name -eq $newName) {
        Write-Host "Skipping '$($_.Name)' because it is already normalized."
        return
    }

    if ($PSCmdlet.ShouldProcess($_.FullName, "Rename to $newName")) {
        Rename-Item -LiteralPath $_.FullName -NewName $newName
    }
}
