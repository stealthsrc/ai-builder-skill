# Visual Basic .NET Patterns

Load this reference when the task requires more than a trivial VB.NET program. It provides reusable idioms for Windows Forms, ADO.NET data access, file I/O, and Office interop.

Pair with [../builders/vb-net-builder.md](../builders/vb-net-builder.md) for routing context and with [../rules/security-baseline.md](../rules/security-baseline.md) when the code handles secrets, database access, or file operations.

---

## 1. Module Skeleton (Console App)

```vb
' Program.vb
Option Strict On
Option Explicit On

Imports System.IO
Imports Microsoft.Extensions.Configuration

Module Program
    ' ---- Configuration ----
    Private ReadOnly Config As IConfiguration = New ConfigurationBuilder() _
        .AddEnvironmentVariables() _
        .AddJsonFile("appsettings.json", optional:=True) _
        .Build()

    Sub Main(args As String())
        Try
            Run(args)
        Catch ex As Exception
            Console.Error.WriteLine($"[ERROR] {ex.Message}")
            Environment.Exit(1)
        End Try
    End Sub

    Private Sub Run(args As String())
        Dim inputPath As String = If(args.Length > 0, args(0), "input.csv")
        If Not File.Exists(inputPath) Then
            Throw New FileNotFoundException($"Input file not found: {inputPath}")
        End If
        ' ... work ...
        Console.WriteLine("Done.")
    End Sub
End Module
```

---

## 2. Windows Forms Event Handler Pattern

```vb
' InvoiceForm.vb
Option Strict On

Public Class InvoiceForm
    ' ---- State ----
    Private _invoices As New List(Of Invoice)

    ' ---- Event Handlers ----
    Private Async Sub BtnLoad_Click(sender As Object, e As EventArgs) Handles BtnLoad.Click
        BtnLoad.Enabled = False
        LblStatus.Text  = "Loading..."
        Try
            _invoices = Await Task.Run(Function() LoadCsvAsync(TxtPath.Text))
            DgvInvoices.DataSource = _invoices
            LblStatus.Text = $"Loaded {_invoices.Count} rows."
        Catch ex As Exception
            MessageBox.Show($"Error: {ex.Message}", "Load Failed", MessageBoxButtons.OK, MessageBoxIcon.Error)
            LblStatus.Text = "Load failed."
        Finally
            BtnLoad.Enabled = True
        End Try
    End Sub

    Private Sub BtnExport_Click(sender As Object, e As EventArgs) Handles BtnExport.Click
        Using dlg As New SaveFileDialog() With {.Filter = "CSV files|*.csv", .FileName = "export.csv"}
            If dlg.ShowDialog() = DialogResult.OK Then
                WriteCsv(dlg.FileName, _invoices)
                LblStatus.Text = $"Exported to {dlg.FileName}"
            End If
        End Using
    End Sub
End Class
```

---

## 3. ADO.NET Safe Parameterized Query

```vb
Imports System.Data.SqlClient

Function GetInvoicesByRegion(connectionString As String, region As String) As DataTable
    Dim result As New DataTable()
    ' ✓ Parameterized — never string concatenation
    Dim sql As String = "SELECT id, region, amount FROM invoices WHERE region = @region"
    Using conn As New SqlConnection(connectionString)
        Using cmd As New SqlCommand(sql, conn)
            cmd.Parameters.AddWithValue("@region", region)
            conn.Open()
            Using adapter As New SqlDataAdapter(cmd)
                adapter.Fill(result)
            End Using
        End Using
    End Using
    Return result
End Function
```

---

## 4. CSV Read and Write

```vb
Imports Microsoft.VisualBasic.FileIO

Function ReadCsv(path As String) As List(Of Invoice)
    Dim result As New List(Of Invoice)
    Using parser As New TextFieldParser(path)
        parser.TextFieldType = FieldType.Delimited
        parser.SetDelimiters(",")
        parser.HasFieldsEnclosedInQuotes = True
        parser.ReadLine() ' skip header
        While Not parser.EndOfData
            Dim cols = parser.ReadFields()
            If cols IsNot Nothing AndAlso cols.Length >= 3 Then
                result.Add(New Invoice With {
                    .Id     = cols(0).Trim(),
                    .Region = cols(1).Trim(),
                    .Amount = Decimal.Parse(cols(2))
                })
            End If
        End While
    End Using
    Return result
End Function

Sub WriteCsv(path As String, invoices As IEnumerable(Of Invoice))
    Using writer As New StreamWriter(path, False, System.Text.Encoding.UTF8)
        writer.WriteLine("id,region,amount")
        For Each inv In invoices
            writer.WriteLine($"{inv.Id},{inv.Region},{inv.Amount}")
        Next
    End Using
End Sub
```

---

## 5. COM Release Guard (Office Interop)

```vb
Imports System.Runtime.InteropServices
Imports Excel = Microsoft.Office.Interop.Excel

Sub ExportToExcel(rows As List(Of Invoice), path As String)
    Dim excel As Excel.Application = Nothing
    Dim wb    As Excel.Workbook    = Nothing
    Try
        excel = New Excel.Application With {.Visible = False}
        wb = excel.Workbooks.Add()
        Dim ws As Excel.Worksheet = CType(wb.Sheets(1), Excel.Worksheet)
        ' ... populate ws ...
        wb.SaveAs(path)
    Finally
        If wb IsNot Nothing Then
            wb.Close(False)
            Marshal.ReleaseComObject(wb)
        End If
        If excel IsNot Nothing Then
            excel.Quit()
            Marshal.ReleaseComObject(excel)
        End If
    End Try
End Sub
```

---

## 6. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| Missing `Option Strict On` | Silent type coercion; late binding surprises | Always `Option Strict On` |
| String concatenation in SQL | SQL injection | `SqlCommand` with `Parameters.AddWithValue` |
| `On Error Resume Next` | Silently swallows all errors | `Try`/`Catch` with specific exception types |
| Forgetting `Marshal.ReleaseComObject` | Office process hangs | `Try`/`Finally` with explicit release |
| `MsgBox` for all feedback | Blocks automation, ugly in CI | `Console.WriteLine` for CLI, status labels for forms |
| `My.Settings` for secrets | Settings file may be committed | `Environment.GetEnvironmentVariable` |
| Late binding (`Dim obj As Object`) | No IntelliSense, runtime errors | Strong typing with specific COM interface types |
