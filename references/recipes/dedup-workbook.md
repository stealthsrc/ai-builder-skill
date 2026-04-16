# Recipe: Dedup Workbook By Key Column

## When To Use

The workbook has duplicate rows by a business key such as invoice id, SKU, order number, or customer email. The user wants a single cleaned sheet, with the duplicates either deleted or moved to a review sheet.

## Route

Primary: VBA (task belongs inside Excel desktop, no external runtime needed).

Load [../patterns/vba-patterns.md](../patterns/vba-patterns.md) for state-save, 2D array, and bottom-up delete.

## Assumptions

- data lives on a single sheet with a header row
- the key column is contiguous and numeric, text, or date
- the user wants to keep the first occurrence and remove the rest
- the file is a macro-enabled workbook (`.xlsm`)

## Implementation

Paste into a standard module. Adjust constants at the top.

```vba
Option Explicit

' ---- Configuration ----
Private Const SOURCE_SHEET_NAME As String = "Invoices"
Private Const DUPLICATE_SHEET_NAME As String = "Duplicates"
Private Const KEY_COLUMN As Long = 2                ' Column B
Private Const HEADER_ROW As Long = 1
Private Const MODE_DELETE As Boolean = False         ' False = move to Duplicates, True = delete

Public Sub DedupByKey()
    Dim wb As Workbook
    Set wb = ThisWorkbook

    Dim src As Worksheet
    Set src = wb.Worksheets(SOURCE_SHEET_NAME)

    Dim prevCalc As XlCalculation
    Dim prevEvents As Boolean
    Dim prevScreen As Boolean
    With Application
        prevCalc = .Calculation: prevEvents = .EnableEvents: prevScreen = .ScreenUpdating
        .Calculation = xlCalculationManual
        .EnableEvents = False
        .ScreenUpdating = False
    End With

    On Error GoTo Cleanup

    Dim lastRow As Long
    lastRow = src.Cells(src.Rows.Count, KEY_COLUMN).End(xlUp).Row
    If lastRow <= HEADER_ROW Then GoTo Cleanup

    Dim seen As Object
    Set seen = CreateObject("Scripting.Dictionary")
    seen.CompareMode = 1                             ' vbTextCompare

    Dim dupSheet As Worksheet
    If Not MODE_DELETE Then Set dupSheet = EnsureDuplicateSheet(wb, src)

    Dim r As Long
    For r = lastRow To HEADER_ROW + 1 Step -1
        Dim key As String
        key = Trim$(CStr(src.Cells(r, KEY_COLUMN).Value2))
        If Len(key) = 0 Then
            ' skip blank keys; leave the row alone
        ElseIf seen.Exists(key) Then
            If MODE_DELETE Then
                src.Rows(r).Delete
            Else
                src.Rows(r).Copy Destination:=dupSheet.Cells(dupSheet.Cells(dupSheet.Rows.Count, 1).End(xlUp).Row + 1, 1)
                src.Rows(r).Delete
            End If
        Else
            seen.Add key, r
        End If
    Next r

Cleanup:
    With Application
        .Calculation = prevCalc: .EnableEvents = prevEvents: .ScreenUpdating = prevScreen
    End With
    If Err.Number <> 0 Then
        MsgBox "DedupByKey failed: " & Err.Number & " - " & Err.Description, vbCritical
    Else
        MsgBox "Dedup complete. " & seen.Count & " unique keys kept.", vbInformation
    End If
End Sub

Private Function EnsureDuplicateSheet(wb As Workbook, src As Worksheet) As Worksheet
    Dim ws As Worksheet
    On Error Resume Next
    Set ws = wb.Worksheets(DUPLICATE_SHEET_NAME)
    On Error GoTo 0
    If ws Is Nothing Then
        Set ws = wb.Worksheets.Add(After:=src)
        ws.Name = DUPLICATE_SHEET_NAME
        src.Rows(HEADER_ROW).Copy Destination:=ws.Cells(1, 1)
    End If
    Set EnsureDuplicateSheet = ws
End Function
```

## Where To Paste

1. Save the workbook as `.xlsm` first.
2. Press `Alt+F11` to open the VBA editor.
3. `Insert` → `Module` and paste the code.
4. Close the editor.
5. Run `Alt+F8` → `DedupByKey` → `Run`.

## Validate

- row count on the source sheet drops by the expected amount
- the `Duplicates` sheet exists and contains every removed row (when `MODE_DELETE = False`)
- the first occurrence of each key remains on the source sheet
- compare total rows before and after: `original - kept = duplicates`

## Rollback

- save a copy of the workbook before running
- `Ctrl+Z` does not undo VBA changes; the copy is the only safe rollback
- if the run fails mid-way, close without saving to discard changes

## Edge Cases

- blank key cells are skipped, not merged
- case sensitivity is off by default (`CompareMode = 1`); flip to `0` for `vbBinaryCompare`
- keys that are numbers stored as text will not match numeric keys; normalize with `CStr` + `Trim`
- tables (`ListObject`) should be converted to a range first, or the code adapted to use `.DataBodyRange`
