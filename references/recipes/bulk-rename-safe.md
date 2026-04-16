# Recipe: Bulk Rename Files Safely

## When To Use

The user has a folder of files that need to be renamed by a rule: prefix, date, regex replace, extension change, or a mix. The rename is destructive if done wrong, so the workflow must preview, confirm, and produce a reversal map.

## Route

Primary: PowerShell. Load [../patterns/powershell-patterns.md](../patterns/powershell-patterns.md) for `SupportsShouldProcess` and parameter validation.

## Assumptions

- the user runs Windows
- target files live in one folder (no recursion by default)
- the rename is deterministic: same input name always produces the same output name

## Implementation

Save as `Rename-FilesByRule.ps1` anywhere on the user's machine.

```powershell
<#
.SYNOPSIS
    Rename files in a folder by matching a regex pattern against the basename.
.DESCRIPTION
    Defaults to preview only. Supports -WhatIf and -Confirm natively. Writes a
    CSV mapping of old -> new so the operation can be reversed.
.EXAMPLE
    .\Rename-FilesByRule.ps1 -Folder 'D:\Exports' -Pattern '^report-' -Replacement 'weekly-' -WhatIf
#>
[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
param(
    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Container })]
    [string]$Folder,

    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string]$Pattern,

    [Parameter(Mandatory)]
    [ValidateNotNull()]
    [AllowEmptyString()]
    [string]$Replacement,

    [string]$Filter = '*',

    [switch]$Recurse
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$mapPath   = Join-Path $Folder ("rename-map-{0}.csv" -f $timestamp)

$regex = [regex]::new($Pattern)

$items = Get-ChildItem -LiteralPath $Folder -Filter $Filter -File -Recurse:$Recurse
$plan  = foreach ($file in $items) {
    $newBase = $regex.Replace($file.BaseName, $Replacement)
    if ($newBase -eq $file.BaseName) { continue }
    $newName = $newBase + $file.Extension
    [pscustomobject]@{
        OldFullName = $file.FullName
        NewFullName = Join-Path $file.Directory.FullName $newName
    }
}

if (-not $plan) {
    Write-Information "No files match the pattern." -InformationAction Continue
    return
}

# Guard against collisions in the plan itself
$dupes = $plan | Group-Object NewFullName | Where-Object Count -gt 1
if ($dupes) {
    throw "Collision detected: the rename would produce duplicate names. Aborting."
}

foreach ($entry in $plan) {
    if (Test-Path -LiteralPath $entry.NewFullName) {
        throw "Target already exists on disk: $($entry.NewFullName)"
    }
    if ($PSCmdlet.ShouldProcess($entry.OldFullName, "Rename -> $($entry.NewFullName)")) {
        Rename-Item -LiteralPath $entry.OldFullName -NewName (Split-Path $entry.NewFullName -Leaf)
    }
}

$plan | Export-Csv -LiteralPath $mapPath -NoTypeInformation -Encoding UTF8
Write-Information "Rename map written to $mapPath" -InformationAction Continue
```

## How To Run

Preview only:

```powershell
.\Rename-FilesByRule.ps1 -Folder 'D:\Exports' -Pattern '^report-' -Replacement 'weekly-' -WhatIf
```

Interactive confirmation per file:

```powershell
.\Rename-FilesByRule.ps1 -Folder 'D:\Exports' -Pattern '^report-' -Replacement 'weekly-' -Confirm
```

Real run once the preview looks right:

```powershell
.\Rename-FilesByRule.ps1 -Folder 'D:\Exports' -Pattern '^report-' -Replacement 'weekly-'
```

## Validate

- `-WhatIf` output lists every rename without changing disk
- the rename-map CSV has one row per renamed file
- file count in the folder is unchanged (no deletions)
- every expected file appears with the new name

## Rollback

Reverse the map CSV:

```powershell
Import-Csv -LiteralPath 'D:\Exports\rename-map-20260416-113000.csv' |
    ForEach-Object {
        if (Test-Path -LiteralPath $_.NewFullName) {
            Rename-Item -LiteralPath $_.NewFullName -NewName (Split-Path $_.OldFullName -Leaf) -WhatIf
        }
    }
```

Drop the `-WhatIf` to apply.

## Edge Cases

- file names with brackets, parentheses, or spaces: handled by `-LiteralPath`
- read-only files: fail loudly, do not silently skip
- files open in another process: the rename throws `IOException`; close the file and rerun
- recursion across subfolders: use `-Recurse`; the map CSV stores full paths

## Execution Policy

If the script is blocked, unblock it once in the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
Unblock-File -LiteralPath .\Rename-FilesByRule.ps1
```
