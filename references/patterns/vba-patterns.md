# VBA Patterns

Load this reference when the task requires more than a trivial macro. It provides reusable idioms and anti-patterns that raise code quality immediately.

Pair with [../builders/vba-builder.md](../builders/vba-builder.md) for routing context and with [../rules/security-baseline.md](../rules/security-baseline.md) when the macro touches email, external files, or destructive actions.

---

## 1. Module Skeleton

Start every standard module with `Option Explicit` and a visible configuration block. Keep all tuneable values at the top so a non-developer can edit them without reading the procedure body.

```vba
Option Explicit

' ---- Configuration ----
Private Const SOURCE_SHEET_NAME As String = "Invoices"
Private Const OUTPUT_SHEET_NAME As String = "Cleaned"
Private Const KEY_COLUMN As Long = 2          ' Column B: invoice id
Private Const HEADER_ROW As Long = 1

Public Sub CleanInvoices()
    Dim wb As Workbook
    Set wb = ThisWorkbook

    Dim src As Worksheet
    Set src = wb.Worksheets(SOURCE_SHEET_NAME)

    ' ... work here ...

    MsgBox "Done.", vbInformation
End Sub
```

No `Dim` without a type. No `Variant` catch-alls unless interacting with a Range array.

---

## 2. Application State Save and Restore

Turning off screen updates, events, or calculation speeds up macros dramatically. Forgetting to restore them leaves Excel in an unusable state. Always wrap the block in a `With` + error handler.

```vba
Public Sub RunHeavyTask()
    Dim prevCalc As XlCalculation
    Dim prevEvents As Boolean
    Dim prevScreen As Boolean

    With Application
        prevCalc = .Calculation
        prevEvents = .EnableEvents
        prevScreen = .ScreenUpdating

        .Calculation = xlCalculationManual
        .EnableEvents = False
        .ScreenUpdating = False
    End With

    On Error GoTo RestoreState

    ' ... heavy work here ...

RestoreState:
    With Application
        .Calculation = prevCalc
        .EnableEvents = prevEvents
        .ScreenUpdating = prevScreen
    End With

    If Err.Number <> 0 Then
        MsgBox "Error " & Err.Number & ": " & Err.Description, vbCritical
    End If
End Sub
```

---

## 3. Work in a 2D Array, Not on Cells

Reading and writing cells one at a time is orders of magnitude slower than transferring the Range to a Variant array, working in memory, and writing it back in one shot.

```vba
Public Sub UpperCaseColumnFast(rng As Range)
    Dim data As Variant
    data = rng.Value2                     ' 2D array for multi-row ranges

    Dim r As Long, c As Long
    For r = LBound(data, 1) To UBound(data, 1)
        For c = LBound(data, 2) To UBound(data, 2)
            If Not IsEmpty(data(r, c)) Then
                data(r, c) = UCase$(CStr(data(r, c)))
            End If
        Next c
    Next r

    rng.Value2 = data
End Sub
```

For single-cell ranges `Value2` returns a scalar, not an array. Guard with `If rng.Count = 1 Then ...`.

---

## 4. Delete Rows Bottom-Up

Deleting rows top-down skips rows because indices shift. Iterate from the last row to the first.

```vba
Public Sub DeleteBlankRows(ws As Worksheet, keyCol As Long)
    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, keyCol).End(xlUp).Row

    Dim r As Long
    For r = lastRow To HEADER_ROW + 1 Step -1
        If Trim$(CStr(ws.Cells(r, keyCol).Value2)) = "" Then
            ws.Rows(r).Delete
        End If
    Next r
End Sub
```

---

## 5. Dedup With Scripting.Dictionary (Late Bound)

Late binding avoids a reference dependency and still gives O(1) lookup.

```vba
Public Function UniqueValues(rng As Range) As Object
    Dim dict As Object
    Set dict = CreateObject("Scripting.Dictionary")
    dict.CompareMode = 1                  ' vbTextCompare

    Dim data As Variant
    data = rng.Value2

    Dim r As Long
    For r = LBound(data, 1) To UBound(data, 1)
        Dim key As String
        key = Trim$(CStr(data(r, 1)))
        If Len(key) > 0 And Not dict.Exists(key) Then
            dict.Add key, r
        End If
    Next r

    Set UniqueValues = dict
End Function
```

---

## 6. Safe Range References

Never use `ActiveSheet`, `Selection`, `.Select`, or `.Activate` in production code. Bind a worksheet object once, then pass it.

```vba
Private Function GetSheet(wb As Workbook, ByVal name As String) As Worksheet
    Dim ws As Worksheet
    On Error Resume Next
    Set ws = wb.Worksheets(name)
    On Error GoTo 0
    If ws Is Nothing Then
        Err.Raise vbObjectError + 1001, , "Sheet not found: " & name
    End If
    Set GetSheet = ws
End Function
```

For ranges, prefer `ws.ListObjects("tbl").DataBodyRange` when the data is in a Table, or compute the last row explicitly with `ws.Cells(ws.Rows.Count, keyCol).End(xlUp).Row`.

---

## 7. Error Handler Skeleton

```vba
Public Sub DoWork()
    On Error GoTo Fail

    ' ... work ...

    Exit Sub

Fail:
    MsgBox "DoWork failed at line " & Erl & vbCrLf & _
           Err.Number & " - " & Err.Description, vbCritical
End Sub
```

Use `Erl` only when line numbers are present; otherwise drop it.

---

## 8. Late Binding for Other Office Apps

Avoid early-bound references unless the environment is tightly controlled. Late binding keeps the file portable across Office versions.

```vba
Public Sub OpenWordDoc(path As String)
    Dim wordApp As Object
    Set wordApp = CreateObject("Word.Application")
    wordApp.Visible = True

    On Error GoTo CleanUp
    wordApp.Documents.Open path
    Exit Sub

CleanUp:
    If Not wordApp Is Nothing Then wordApp.Quit
    Err.Raise Err.Number, , Err.Description
End Sub
```

---

## 9. Outlook Safe Send (Dry-Run First)

Never send automatically on a fresh run. Default to `.Display` so the user confirms.

```vba
Public Sub DraftInvoiceEmail(toAddr As String, subj As String, body As String, _
                             Optional send As Boolean = False)
    Dim olApp As Object, msg As Object
    Set olApp = CreateObject("Outlook.Application")
    Set msg = olApp.CreateItem(0)         ' olMailItem

    With msg
        .To = toAddr
        .Subject = subj
        .Body = body
    End With

    If send Then
        msg.Send
    Else
        msg.Display                       ' user reviews before sending
    End If
End Sub
```

For batch sends, require a hardcoded confirmation like a second argument or a cell value that must equal `"SEND"`.

---

## 10. Anti-Patterns With Fixes

| Anti-pattern | Why it hurts | Fix |
|---|---|---|
| `ActiveSheet.Range("A1").Select` | breaks when user switches sheet | bind `Dim ws As Worksheet: Set ws = wb.Worksheets("Name")` then `ws.Range("A1").Value = ...` |
| Top-down row delete | skips rows | iterate bottom-up with `Step -1` |
| `Dim x, y, z` (no types) | silent `Variant` bugs | declare each with its type |
| Missing `Option Explicit` | typo becomes a new variable | start every module with it |
| `.Value` on huge ranges in a loop | thousands of COM calls | read `.Value2` into a Variant array, process, write back |
| No state restore | leaves Excel broken | save `Calculation`/`EnableEvents`/`ScreenUpdating`, restore in an error handler |
| Hardcoded column letters | break on layout change | use named constants or `ListObject` column references |
| `MsgBox` inside a loop | blocks the macro | accumulate into a string, show once at the end |
| `.Send` without review | spam risk | default to `.Display`, gate `.Send` behind an explicit flag |

---

## Related

- Recipe: [../recipes/dedup-workbook.md](../recipes/dedup-workbook.md)
- Recipe: [../recipes/outlook-send-confirmed.md](../recipes/outlook-send-confirmed.md)
- Safety: [../rules/security-baseline.md](../rules/security-baseline.md)
