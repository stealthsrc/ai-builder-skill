Attribute VB_Name = "CleanInvoices"
Option Explicit

Public Sub CleanInvoiceSheet()
    Const TARGET_SHEET As String = "Invoices"
    Const HEADER_ROW As Long = 1
    Const INVOICE_COLUMN As String = "A"
    Const FIRST_DATA_ROW As Long = 2

    Dim ws As Worksheet
    Dim lastRow As Long
    Dim rowIndex As Long
    Dim cellValue As String
    Dim seen As Object

    Application.ScreenUpdating = False
    Application.EnableEvents = False

    On Error GoTo CleanFail

    Set ws = ThisWorkbook.Worksheets(TARGET_SHEET)
    lastRow = ws.Cells(ws.Rows.Count, INVOICE_COLUMN).End(xlUp).Row
    Set seen = CreateObject("Scripting.Dictionary")

    ws.Range(INVOICE_COLUMN & FIRST_DATA_ROW & ":" & INVOICE_COLUMN & lastRow).Interior.Pattern = xlNone

    For rowIndex = lastRow To FIRST_DATA_ROW Step -1
        cellValue = Trim$(CStr(ws.Cells(rowIndex, INVOICE_COLUMN).Value))

        If Len(cellValue) = 0 Then
            ws.Rows(rowIndex).Delete
        Else
            ws.Cells(rowIndex, INVOICE_COLUMN).Value = cellValue

            If seen.Exists(UCase$(cellValue)) Then
                ws.Cells(rowIndex, INVOICE_COLUMN).Interior.Color = RGB(255, 230, 153)
                ws.Cells(seen(UCase$(cellValue)), INVOICE_COLUMN).Interior.Color = RGB(255, 230, 153)
            Else
                seen.Add UCase$(cellValue), rowIndex
            End If
        End If
    Next rowIndex

    ws.Rows(HEADER_ROW).Font.Bold = True
    ws.Columns(INVOICE_COLUMN).AutoFit

CleanExit:
    Application.ScreenUpdating = True
    Application.EnableEvents = True
    Exit Sub

CleanFail:
    MsgBox "Invoice cleanup failed: " & Err.Description, vbExclamation
    Resume CleanExit
End Sub
