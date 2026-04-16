# C# Patterns

Load this reference when the task requires more than a trivial .NET script. It provides reusable idioms for async code, LINQ, configuration, Excel output, and COM interop.

Pair with [../builders/csharp-builder.md](../builders/csharp-builder.md) for routing context and with [../rules/security-baseline.md](../rules/security-baseline.md) when the code handles secrets, external input, or file operations.

---

## 1. Program Skeleton (Top-Level Statements, .NET 6+)

```csharp
// Program.cs
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

var config = new ConfigurationBuilder()
    .AddEnvironmentVariables()
    .AddJsonFile("appsettings.json", optional: true)
    .Build();

var services = new ServiceCollection()
    .AddLogging(b => b.AddConsole())
    .AddSingleton<IConfiguration>(config)
    .AddSingleton<ReportService>()
    .BuildServiceProvider();

var logger = services.GetRequiredService<ILogger<Program>>();
try
{
    var service = services.GetRequiredService<ReportService>();
    await service.RunAsync(CancellationToken.None);
}
catch (Exception ex)
{
    logger.LogError(ex, "Unhandled exception");
    return 1;
}
return 0;
```

---

## 2. Async/Await with CancellationToken

Pass `CancellationToken` through the entire call chain. Wire it to `Console.CancelKeyPress` for CLI tools.

```csharp
using var cts = new CancellationTokenSource();
Console.CancelKeyPress += (_, e) =>
{
    e.Cancel = true;
    cts.Cancel();
};

async Task<string> FetchAsync(string url, CancellationToken ct)
{
    using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(30) };
    var response = await client.GetAsync(url, ct);
    response.EnsureSuccessStatusCode();
    return await response.Content.ReadAsStringAsync(ct);
}
```

---

## 3. LINQ Idioms

```csharp
// Filter, transform, group in a pipeline
var invoicesByRegion = invoices
    .Where(i => i.Amount > 0 && i.Date >= cutoff)
    .GroupBy(i => i.Region)
    .Select(g => new
    {
        Region  = g.Key,
        Total   = g.Sum(i => i.Amount),
        Count   = g.Count(),
        Average = g.Average(i => i.Amount),
    })
    .OrderByDescending(r => r.Total)
    .ToList();

// First-or-default with null guard
var latest = invoices
    .Where(i => i.Region == "West")
    .MaxBy(i => i.Date);
if (latest is null) return;
```

---

## 4. CSV Reading (built-in, no dependency)

```csharp
using System.Globalization;

record InvoiceRow(string Id, string Region, decimal Amount, DateTime Date);

static IEnumerable<InvoiceRow> ReadCsv(string path)
{
    using var reader = new StreamReader(path);
    reader.ReadLine(); // skip header
    while (reader.ReadLine() is { } line)
    {
        var cols = line.Split(',');
        if (cols.Length < 4) continue;
        yield return new InvoiceRow(
            Id:     cols[0].Trim(),
            Region: cols[1].Trim(),
            Amount: decimal.Parse(cols[2], CultureInfo.InvariantCulture),
            Date:   DateTime.Parse(cols[3], CultureInfo.InvariantCulture)
        );
    }
}
```

---

## 5. Excel Output with EPPlus

```csharp
// dotnet add package EPPlus
using OfficeOpenXml;
using OfficeOpenXml.Style;

ExcelPackage.LicenseContext = LicenseContext.NonCommercial;

static void WriteExcel(string path, IEnumerable<InvoiceRow> rows)
{
    using var pkg = new ExcelPackage();
    var ws = pkg.Workbook.Worksheets.Add("Report");

    // Header row
    ws.Cells[1, 1].Value = "ID";
    ws.Cells[1, 2].Value = "Region";
    ws.Cells[1, 3].Value = "Amount";
    ws.Cells[1, 4].Value = "Date";
    using (var r = ws.Cells[1, 1, 1, 4])
    {
        r.Style.Font.Bold = true;
        r.Style.Fill.PatternType = ExcelFillStyle.Solid;
        r.Style.Fill.BackgroundColor.SetColor(System.Drawing.Color.FromArgb(37, 99, 235));
        r.Style.Font.Color.SetColor(System.Drawing.Color.White);
    }

    // Data rows
    int row = 2;
    foreach (var inv in rows)
    {
        ws.Cells[row, 1].Value = inv.Id;
        ws.Cells[row, 2].Value = inv.Region;
        ws.Cells[row, 3].Value = (double)inv.Amount;
        ws.Cells[row, 4].Value = inv.Date;
        ws.Cells[row, 4].Style.Numberformat.Format = "yyyy-mm-dd";
        row++;
    }

    ws.Cells[ws.Dimension.Address].AutoFitColumns();
    ws.View.FreezePanes(2, 1);

    pkg.SaveAs(new FileInfo(path));
}
```

---

## 6. Secrets from IConfiguration / Environment

```csharp
// In appsettings.json: store non-secret config only
// Secrets come from environment or user-secrets

string apiKey = config["ApiKey"]
    ?? throw new InvalidOperationException("ApiKey environment variable is required.");

// For user-secrets in dev: dotnet user-secrets set "ApiKey" "dev-key"
```

---

## 7. COM Release Guard (Office Interop)

Always release COM objects in a `finally` block to prevent Excel hanging in the process list.

```csharp
using System.Runtime.InteropServices;

Excel.Application? excel = null;
Excel.Workbook?    wb    = null;
try
{
    excel = new Excel.Application { Visible = false };
    wb    = excel.Workbooks.Open(filePath);
    // ... work ...
}
finally
{
    wb?.Close(false);
    if (wb    != null) Marshal.ReleaseComObject(wb);
    excel?.Quit();
    if (excel != null) Marshal.ReleaseComObject(excel);
}
```

---

## 8. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| `async void` method | Exceptions are unobservable | `async Task` always (except event handlers) |
| `Task.Result` or `.Wait()` | Deadlocks in ASP.NET context | `await` throughout |
| `new HttpClient()` in a loop | Socket exhaustion | `IHttpClientFactory` or a single static `HttpClient` |
| Hard-coded connection strings | Credential leak in source | `IConfiguration` + environment variables |
| `catch (Exception) {}` | Silently swallows all errors | Catch specific types; log and rethrow |
| `string.Format` with user input for SQL | SQL injection | Always parameterized queries |
| Forgetting `Marshal.ReleaseComObject` | Excel process never exits | Wrap in `try/finally` with explicit release |
| Missing `using` on streams | File handles leak | `using var stream = new FileStream(...)` |
