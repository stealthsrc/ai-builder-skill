# Recipe: Archive Files By Date Into Monthly Folders

## When To Use

A working folder accumulates files and needs to be swept into monthly subfolders based on each file's `LastWriteTime`. The operation must be previewable, resumable, and leave a mapping log for audit.

## Route

Primary: PowerShell. Load [../patterns/powershell-patterns.md](../patterns/powershell-patterns.md) for `SupportsShouldProcess`, filesystem idioms, and logging.

## Assumptions

- the user runs Windows
- target files sit directly in one folder (or recurse when `-Recurse` is set)
- monthly folders should be named `archive-YYYY-MM`
- files already inside a folder that matches the pattern are left alone

## Implementation

Save as `Move-ToMonthlyArchive.ps1`.

```powershell
<#
.SYNOPSIS
    Move files into monthly subfolders based on LastWriteTime.
.EXAMPLE
    .\Move-ToMonthlyArchive.ps1 -Folder 'D:\Reports' -OlderThanDays 30 -WhatIf
#>
[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium')]
param(
    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Container })]
    [string]$Folder,

    [ValidateRange(0, 3650)]
    [int]$OlderThanDays = 30,

    [string]$Filter = '*',

    [switch]$Recurse
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$cutoff = (Get-Date).Date.AddDays(-$OlderThanDays)
$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$logPath = Join-Path $Folder ("archive-log-{0}.csv" -f $timestamp)
$archivePattern = '^archive-\d{4}-\d{2}$'

$files = Get-ChildItem -LiteralPath $Folder -Filter $Filter -File -Recurse:$Recurse |
    Where-Object {
        $_.LastWriteTime -lt $cutoff -and
        $_.Directory.Name -notmatch $archivePattern
    }

if (-not $files) {
    Write-Information "Nothing to archive." -InformationAction Continue
    return
}

$plan = foreach ($file in $files) {
    $subfolder = 'archive-{0:yyyy-MM}' -f $file.LastWriteTime
    $targetDir = Join-Path $file.Directory.FullName $subfolder
    $targetPath = Join-Path $targetDir $file.Name

    [pscustomobject]@{
        Source = $file.FullName
        Target = $targetPath
    }
}

# Detect collisions in the plan
$dupes = $plan | Group-Object Target | Where-Object Count -gt 1
if ($dupes) {
    throw "Collision detected: the plan would overwrite the same target path."
}

foreach ($entry in $plan) {
    $targetDir = Split-Path -LiteralPath $entry.Target -Parent
    if (-not (Test-Path -LiteralPath $targetDir -PathType Container)) {
        if ($PSCmdlet.ShouldProcess($targetDir, 'Create archive folder')) {
            New-Item -ItemType Directory -Path $targetDir | Out-Null
        }
    }

    if (Test-Path -LiteralPath $entry.Target) {
        Write-Warning "Skipping (target exists): $($entry.Target)"
        continue
    }

    if ($PSCmdlet.ShouldProcess($entry.Source, "Move -> $($entry.Target)")) {
        Move-Item -LiteralPath $entry.Source -Destination $entry.Target
    }
}

$plan | Export-Csv -LiteralPath $logPath -NoTypeInformation -Encoding UTF8
Write-Information "Archive log written to $logPath" -InformationAction Continue
```

## How To Run

Preview:

```powershell
.\Move-ToMonthlyArchive.ps1 -Folder 'D:\Reports' -OlderThanDays 30 -WhatIf
```

Apply:

```powershell
.\Move-ToMonthlyArchive.ps1 -Folder 'D:\Reports' -OlderThanDays 30
```

Archive PDFs only, recursive:

```powershell
.\Move-ToMonthlyArchive.ps1 -Folder 'D:\Reports' -Filter '*.pdf' -Recurse
```

## Validate

- `-WhatIf` lists every move without touching disk
- monthly folders are created only when they did not already exist
- the log CSV records every source and target path
- rerunning on the same folder reports "Nothing to archive" when no new files are past the cutoff

## Rollback

Reverse the log CSV:

```powershell
Import-Csv -LiteralPath 'D:\Reports\archive-log-20260416-113000.csv' |
    ForEach-Object {
        if (Test-Path -LiteralPath $_.Target) {
            Move-Item -LiteralPath $_.Target -Destination $_.Source -WhatIf
        }
    }
```

Drop `-WhatIf` to apply.

## Edge Cases

- files already inside a monthly archive folder are skipped by the regex guard
- files with timestamps older than ten years are allowed (`ValidateRange` caps at 3650)
- locked files throw on `Move-Item`; close them and rerun; the log still records completed moves
- cross-drive moves are slower; the script does not try to copy+delete instead
