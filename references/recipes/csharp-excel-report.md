# Recipe: C# CSV to Formatted Excel Report

Complete .NET 8 console app that reads one or more CSV files and generates a formatted `.xlsx` report using EPPlus — frozen header, bold fill, auto-width columns, and a per-sheet summary row.

Pair with [../builders/csharp-builder.md](../builders/csharp-builder.md) and [../patterns/csharp-patterns.md](../patterns/csharp-patterns.md).

---

## What It Does

1. Reads every CSV file in a source folder.
2. Merges rows into a single in-memory collection.
3. Writes a formatted Excel workbook with one sheet per source file plus a `Summary` sheet.
4. Formats each sheet with a frozen header, blue bold header fill, and auto-width columns.
5. Adds a total row at the bottom of each sheet.

---

## Setup

```bash
dotnet new console -n CsvToExcel -f net8.0
cd CsvToExcel
dotnet add package EPPlus --version 7.3.0
```

---

## CsvToExcel.csproj

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="EPPlus" Version="7.3.0" />
  </ItemGroup>
</Project>
```

---

## Program.cs

```csharp
using System.Globalization;
using OfficeOpenXml;
using OfficeOpenXml.Style;

// ---- Configuration ----
const string SourceDir  = "data";
const string OutputPath = "report.xlsx";
const int    AmountCol  = 3;   // 1-based column index for the numeric column to total

ExcelPackage.LicenseContext = LicenseContext.NonCommercial;

if (!Directory.Exists(SourceDir))
{
    Console.Error.WriteLine($"Source folder not found: {SourceDir}");
    return 1;
}

var csvFiles = Directory.GetFiles(SourceDir, "*.csv");
if (csvFiles.Length == 0) { Console.Error.WriteLine("No CSV files found."); return 1; }

using var pkg = new ExcelPackage();
var allRows   = new List<string[]>();

foreach (var csvPath in csvFiles.OrderBy(f => f))
{
    var lines = File.ReadAllLines(csvPath).Select(l => l.Trim()).Where(l => l.Length > 0).ToArray();
    if (lines.Length < 2) continue;

    var headers  = SplitCsv(lines[0]);
    var dataRows = lines[1..].Select(SplitCsv).ToList();

    // Per-file sheet
    var sheetName = Path.GetFileNameWithoutExtension(csvPath)[..Math.Min(31, Path.GetFileNameWithoutExtension(csvPath).Length)];
    var ws = pkg.Workbook.Worksheets.Add(sheetName);
    WriteSheet(ws, headers, dataRows, AmountCol);

    allRows.AddRange(dataRows);
    Console.WriteLine($"Added sheet: {sheetName} ({dataRows.Count} rows)");
}

// Summary sheet
if (pkg.Workbook.Worksheets.Count > 0)
{
    var firstWs  = pkg.Workbook.Worksheets[0];
    var headers  = Enumerable.Range(1, firstWs.Dimension.Columns)
                             .Select(c => firstWs.Cells[1, c].Text).ToArray();
    var sumSheet = pkg.Workbook.Worksheets.Add("Summary");
    WriteSheet(sumSheet, headers, allRows, AmountCol);
}

var tmp = OutputPath + ".tmp";
pkg.SaveAs(new FileInfo(tmp));
File.Move(tmp, OutputPath, overwrite: true);
Console.WriteLine($"\nReport written: {OutputPath} ({pkg.Workbook.Worksheets.Count} sheets)");
return 0;

// ---- Helpers ----

static void WriteSheet(ExcelWorksheet ws, string[] headers, List<string[]> rows, int amountCol)
{
    // Header row
    for (int c = 0; c < headers.Length; c++)
        ws.Cells[1, c + 1].Value = headers[c];

    using (var r = ws.Cells[1, 1, 1, headers.Length])
    {
        r.Style.Font.Bold = true;
        r.Style.Fill.PatternType = ExcelFillStyle.Solid;
        r.Style.Fill.BackgroundColor.SetColor(System.Drawing.Color.FromArgb(37, 99, 235));
        r.Style.Font.Color.SetColor(System.Drawing.Color.White);
    }

    // Data rows
    for (int i = 0; i < rows.Count; i++)
    {
        var row = rows[i];
        for (int c = 0; c < headers.Length && c < row.Length; c++)
        {
            if (c == amountCol - 1 &&
                double.TryParse(row[c], NumberStyles.Any, CultureInfo.InvariantCulture, out var n))
                ws.Cells[i + 2, c + 1].Value = n;
            else
                ws.Cells[i + 2, c + 1].Value = row[c];
        }
    }

    // Total row (for numeric amount column)
    int lastDataRow = rows.Count + 1;
    int totalRow    = lastDataRow + 1;
    ws.Cells[totalRow, 1].Value = "TOTAL";
    ws.Cells[totalRow, 1].Style.Font.Bold = true;
    ws.Cells[totalRow, amountCol].Formula  = $"SUM({ws.Cells[2, amountCol].Address}:{ws.Cells[lastDataRow, amountCol].Address})";
    ws.Cells[totalRow, amountCol].Style.Font.Bold = true;

    // Freeze and auto-width
    ws.View.FreezePanes(2, 1);
    ws.Cells[ws.Dimension.Address].AutoFitColumns();
}

static string[] SplitCsv(string line) =>
    line.Split(',').Select(f => f.Trim().Trim('"')).ToArray();
```

---

## Run

```bash
# Put CSV files in a data/ folder, then:
dotnet run

# Or after build:
dotnet build -c Release
./bin/Release/net8.0/CsvToExcel
```

---

## Validation

- Open `report.xlsx` — every CSV file should have its own tab plus a `Summary` tab.
- Check the header row is blue and bold.
- Check the `TOTAL` row at the bottom of each sheet.
- Row count per sheet should match source CSV row count (excluding header).

---

## Edge Cases

| Case | Behavior |
|---|---|
| CSV with no data rows | Sheet is created with header only — no TOTAL row |
| Amount column not numeric | Cell is written as text — TOTAL row will show `#VALUE!` |
| Sheet name > 31 chars | Truncated to 31 chars (Excel limit) |
| Existing `report.xlsx` open in Excel | Atomic write to `.tmp` then rename — fails only if `.xlsx` is locked |
