Attribute VB_Name = "StarterModule"
Option Explicit

Public Sub RunTask()
    Const TARGET_SHEET As String = "Sheet1"
    Dim ws As Worksheet

    Set ws = ThisWorkbook.Worksheets(TARGET_SHEET)
    MsgBox "Replace this macro body with your workbook logic.", vbInformation
End Sub
