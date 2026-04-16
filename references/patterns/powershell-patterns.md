# PowerShell Patterns

Load this reference when the task requires more than a trivial one-liner. It provides reusable idioms and anti-patterns for safe, maintainable Windows-native automation.

Pair with [../builders/powershell-builder.md](../builders/powershell-builder.md) for routing context and with [../rules/security-baseline.md](../rules/security-baseline.md) when the script touches external files, credentials, or destructive actions.

---

## 1. Script Skeleton

Every non-trivial script should start with `Set-StrictMode`, a strict `$ErrorActionPreference`, and a typed `param()` block. This turns silent failures into loud ones.

```powershell
<#
.SYNOPSIS
    Short one-liner describing the script.
.DESCRIPTION
    Longer description. What it does, what it touches, what it produces.
.EXAMPLE
    .\Clean-Reports.ps1 -SourceFolder 'D:\Reports' -Archive
#>
[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium')]
param(
    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Container })]
    [string]$SourceFolder,

    [Parameter()]
    [ValidatePattern('^[A-Za-z0-9_\-]+$')]
    [string]$Prefix = 'report',

    [switch]$Archive
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$InformationPreference = 'Continue'

# ... script body ...
```

---

## 2. Real `-WhatIf` and `-Confirm` via `SupportsShouldProcess`

Never invent a manual `-DryRun` switch when PowerShell has a built-in one. With `SupportsShouldProcess = $true`, `$PSCmdlet.ShouldProcess` handles both `-WhatIf` (preview) and `-Confirm` (interactive approval) for free.

```powershell
function Remove-StaleFile {
    [CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [System.IO.FileInfo]$File
    )
    process {
        if ($PSCmdlet.ShouldProcess($File.FullName, 'Remove file')) {
            Remove-Item -LiteralPath $File.FullName -Force
        }
    }
}
```

Users can now call `Remove-StaleFile -WhatIf` to preview or `-Confirm` to gate every delete.

---

## 3. Parameter Validation Attributes

Validate inputs at the parameter boundary, not in the function body.

```powershell
param(
    [ValidateSet('Daily', 'Weekly', 'Monthly')]
    [string]$Cadence,

    [ValidateRange(1, 365)]
    [int]$RetentionDays = 30,

    [ValidatePattern('^[A-Za-z0-9_\-\. ]+$')]
    [string]$FileNameSafeChars,

    [ValidateScript({ $_.Length -gt 0 -and $_.Length -le 255 })]
    [string]$Label
)
```

---

## 4. `try` / `catch` / `finally` With COM Release

When automating Excel, Word, or Outlook through COM, always wrap the work in `try` / `finally` and explicitly release the COM objects. Otherwise the host process stays resident.

```powershell
function Export-WorkbookToPdf {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$WorkbookPath,
        [Parameter(Mandatory)][string]$OutputPdf
    )

    $excel   = $null
    $books   = $null
    $book    = $null
    try {
        $excel = New-Object -ComObject Excel.Application
        $excel.Visible = $false
        $excel.DisplayAlerts = $false

        $books = $excel.Workbooks
        $book  = $books.Open($WorkbookPath, 0, $true)  # read-only

        $book.ExportAsFixedFormat(0, $OutputPdf)   # 0 = xlTypePDF
    }
    finally {
        if ($book)  { $book.Close($false);  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($book) }
        if ($books) { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($books) }
        if ($excel) { $excel.Quit();        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($excel) }
        [GC]::Collect()
        [GC]::WaitForPendingFinalizers()
    }
}
```

---

## 5. Splatting For Readable Calls

Long command calls with many parameters become unreadable. Splat a hashtable instead.

```powershell
$params = @{
    LiteralPath = $source
    Destination = $destination
    Recurse     = $true
    Force       = $false
    ErrorAction = 'Stop'
}
Copy-Item @params
```

---

## 6. Pipeline Function Skeleton

Functions that process a stream of input should use `Begin` / `Process` / `End`. Initialize once, process each item, finalize once.

```powershell
function ConvertTo-CleanedName {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [string]$Name
    )
    begin {
        $invalid = [IO.Path]::GetInvalidFileNameChars()
    }
    process {
        $out = $Name
        foreach ($ch in $invalid) {
            $out = $out.Replace($ch, '_')
        }
        $out
    }
}

Get-ChildItem -LiteralPath $src -File |
    ForEach-Object { $_ | Rename-Item -NewName ($_.Name | ConvertTo-CleanedName) -WhatIf }
```

---

## 7. Logging Without A Module

Use `Write-Verbose` and `Write-Information` for progress. Use `Write-Error` with `-ErrorAction Stop` for failures. Avoid `Write-Host` in library code.

```powershell
[CmdletBinding()]
param()

Write-Information "Starting cleanup..." -InformationAction Continue
Write-Verbose    "Source folder resolved to $source"

try {
    # work
}
catch {
    Write-Error "Cleanup failed: $($_.Exception.Message)" -ErrorAction Stop
}
```

For durable logs, wrap a script in `Start-Transcript` / `Stop-Transcript`:

```powershell
$log = Join-Path $PSScriptRoot ("run-{0:yyyyMMdd-HHmmss}.log" -f (Get-Date))
Start-Transcript -Path $log -Append | Out-Null
try {
    # work
}
finally {
    Stop-Transcript | Out-Null
}
```

---

## 8. Filesystem Idioms

Always use `-LiteralPath` when the path might contain brackets or wildcards. Build paths with `Join-Path`. Never concatenate with `+`.

```powershell
$archive = Join-Path -Path $root -ChildPath ('archive-{0:yyyy-MM}' -f (Get-Date))

if (-not (Test-Path -LiteralPath $archive -PathType Container)) {
    New-Item -ItemType Directory -Path $archive | Out-Null
}

Get-ChildItem -LiteralPath $source -Filter '*.pdf' -File |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } |
    ForEach-Object {
        $dest = Join-Path $archive $_.Name
        Move-Item -LiteralPath $_.FullName -Destination $dest -WhatIf
    }
```

Remove the `-WhatIf` only once the preview is correct.

---

## 9. Safe External Command Execution

Prefer native cmdlets over shelling out. When you must call an external tool, pass arguments as an array and avoid `Invoke-Expression` entirely.

```powershell
# Bad:  Invoke-Expression "git log --since $from"
# Good:
$args = @('log', '--since', $from, '--pretty=format:%h %s')
& git @args
```

`&` with an array passes each element as its own argument. No shell parsing, no injection.

---

## 10. HTTPS Requests With Explicit TLS and Retry

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$attempt = 0
$max     = 3
while ($true) {
    try {
        $response = Invoke-RestMethod -Uri $url -Method Get -TimeoutSec 30
        break
    }
    catch {
        $attempt++
        if ($attempt -ge $max) { throw }
        Start-Sleep -Seconds ([Math]::Pow(2, $attempt))
    }
}
```

For secrets, use `SecretManagement` (`Get-Secret`) or environment variables. Never bake a credential into the script.

---

## 11. Anti-Patterns With Fixes

| Anti-pattern | Why it hurts | Fix |
|---|---|---|
| `Invoke-Expression $userInput` | arbitrary code execution | use `&` with an argument array, or `Start-Process -ArgumentList @(...)` |
| `Get-ChildItem *` without `-File` / `-Filter` | pulls too much, slow and ambiguous | add `-File`, `-Filter`, or `-Include` |
| Assuming admin privileges | script fails silently for standard users | detect with `[Security.Principal.WindowsPrincipal]` and fail loudly |
| Path concatenation with `+` | breaks on trailing slashes, spaces | use `Join-Path` |
| No `-LiteralPath` on user-supplied paths | glob characters break the path | always use `-LiteralPath` for dynamic paths |
| Custom `-DryRun` switch | reinvents a built-in | declare `SupportsShouldProcess` and call `ShouldProcess` |
| `Write-Host` everywhere | output cannot be captured or piped | use `Write-Verbose` / `Write-Information` / return objects |
| Forgotten COM release | Excel / Word keeps running | `Release-ComObject` in a `finally`, then `GC::Collect` |
| `$ErrorActionPreference` default | silent failures | set to `'Stop'` in non-trivial scripts |
| Hardcoded credentials | secret leak | `Get-Secret` / `$env:VAR` / `Import-Clixml` protected file |

---

## Related

- Recipe: [../recipes/bulk-rename-safe.md](../recipes/bulk-rename-safe.md)
- Recipe: [../recipes/archive-by-date.md](../recipes/archive-by-date.md)
- Recipe: [../recipes/outlook-send-confirmed.md](../recipes/outlook-send-confirmed.md)
- Safety: [../rules/security-baseline.md](../rules/security-baseline.md)
