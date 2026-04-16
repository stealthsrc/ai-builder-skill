# Recipe: Outlook Send With Human Confirmation

## When To Use

The automation needs to send Outlook emails but must not send silently. The user must review each draft, or approve a batch with an explicit confirmation string.

## Route

- VBA when the mail flow lives inside an Excel or Word macro.
- PowerShell when the trigger is an operational script on Windows.

Load [../patterns/vba-patterns.md](../patterns/vba-patterns.md) or [../patterns/powershell-patterns.md](../patterns/powershell-patterns.md).

Always load [../rules/security-baseline.md](../rules/security-baseline.md) because email sends are high-impact.

## Assumptions

- the user runs Outlook desktop on Windows with a configured profile
- the sender account has permission to send
- the recipient list is short enough for manual review, or batched with an explicit approval

## VBA Implementation

Paste into a standard module of an `.xlsm` workbook.

```vba
Option Explicit

' ---- Configuration ----
Private Const CONFIRM_TOKEN As String = "SEND-20260416"   ' change for each batch
Private Const RECIPIENT_SHEET As String = "Recipients"
Private Const COL_TO As Long = 1
Private Const COL_SUBJECT As Long = 2
Private Const COL_BODY As Long = 3
Private Const COL_STATUS As Long = 4

Public Sub DraftBatch()
    ProcessBatch send:=False
End Sub

Public Sub SendBatchWithToken(ByVal token As String)
    If token <> CONFIRM_TOKEN Then
        MsgBox "Refusing to send: token mismatch.", vbCritical
        Exit Sub
    End If
    ProcessBatch send:=True
End Sub

Private Sub ProcessBatch(ByVal send As Boolean)
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(RECIPIENT_SHEET)

    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, COL_TO).End(xlUp).Row

    Dim olApp As Object
    Set olApp = CreateObject("Outlook.Application")

    Dim r As Long
    For r = 2 To lastRow
        Dim toAddr As String, subj As String, body As String
        toAddr = Trim$(CStr(ws.Cells(r, COL_TO).Value2))
        subj = Trim$(CStr(ws.Cells(r, COL_SUBJECT).Value2))
        body = CStr(ws.Cells(r, COL_BODY).Value2)

        If Len(toAddr) = 0 Or Len(subj) = 0 Then
            ws.Cells(r, COL_STATUS).Value = "SKIPPED (missing to/subject)"
        Else
            Dim msg As Object
            Set msg = olApp.CreateItem(0)                 ' olMailItem
            With msg
                .To = toAddr
                .Subject = subj
                .Body = body
            End With
            If send Then
                msg.Send
                ws.Cells(r, COL_STATUS).Value = "SENT " & Format$(Now, "yyyy-mm-dd hh:nn")
            Else
                msg.Display                                ' user reviews, can close to discard
                ws.Cells(r, COL_STATUS).Value = "DRAFTED " & Format$(Now, "yyyy-mm-dd hh:nn")
            End If
        End If
    Next r

    MsgBox "Batch complete.", vbInformation
End Sub
```

**How to run safely:**

1. Populate the `Recipients` sheet with `To`, `Subject`, `Body`, `Status`.
2. Run `DraftBatch` first. Outlook opens every mail item for review.
3. Close the drafts you do not want.
4. When satisfied, call `SendBatchWithToken "SEND-20260416"` from the Immediate window (`Ctrl+G`) with the current token value.

The token rotation forces the user to edit the constant intentionally for every batch, which prevents accidental reruns.

## PowerShell Implementation

```powershell
<#
.SYNOPSIS
    Draft or send an Outlook batch from a CSV. Defaults to draft-only.
.EXAMPLE
    .\Send-Outlook.ps1 -Csv 'D:\mail\batch.csv'
    .\Send-Outlook.ps1 -Csv 'D:\mail\batch.csv' -Send -ConfirmToken 'SEND-20260416'
#>
[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
param(
    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string]$Csv,

    [string]$ConfirmToken,
    [switch]$Send
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$expectedToken = 'SEND-20260416'

if ($Send -and $ConfirmToken -ne $expectedToken) {
    throw "Refusing to send without the current ConfirmToken."
}

$rows = Import-Csv -LiteralPath $Csv
$outlook = New-Object -ComObject Outlook.Application
try {
    foreach ($row in $rows) {
        if (-not $row.To -or -not $row.Subject) { continue }

        $mail = $outlook.CreateItem(0)
        $mail.To = $row.To
        $mail.Subject = $row.Subject
        $mail.Body = $row.Body

        if ($Send) {
            if ($PSCmdlet.ShouldProcess($row.To, "Send mail: $($row.Subject)")) {
                $mail.Send()
            }
        } else {
            $mail.Display()
        }
    }
}
finally {
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($outlook)
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
```

Preview mode:

```powershell
.\Send-Outlook.ps1 -Csv 'D:\mail\batch.csv'
```

Send mode with explicit token:

```powershell
.\Send-Outlook.ps1 -Csv 'D:\mail\batch.csv' -Send -ConfirmToken 'SEND-20260416' -Confirm
```

## Validate

- draft mode opens one Outlook window per recipient
- send mode sends only when `-ConfirmToken` matches
- the status column or log records every action with a timestamp

## Rollback

- draft mode does not need rollback; close the drafts to discard
- for a bad send, contact the recipient; Outlook "Recall This Message" only works within the same Exchange org and often fails

## Edge Cases

- the Outlook profile is not signed in: `CreateItem` throws; surface a clear error
- attachments: add `$mail.Attachments.Add($path)` with `Test-Path -LiteralPath $path` before
- HTML body: set `$mail.HTMLBody` instead of `$mail.Body`; never interpolate user data into HTML without escaping
