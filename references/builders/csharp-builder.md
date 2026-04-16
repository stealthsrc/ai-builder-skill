# C# Builder

Use this reference for Windows desktop apps, .NET automation scripts, ASP.NET Core APIs, Office interop (VSTO), Unity game scripts, and any workflow that benefits from the .NET ecosystem.

## Use It For

- Windows Forms and WPF desktop applications
- .NET console scripts and automation tools
- ASP.NET Core REST APIs and web services
- Excel, Word, and Outlook automation via VSTO or Office Interop
- Unity game scripts (MonoBehaviour, coroutines, ScriptableObjects)
- Cross-platform .NET apps that run on Windows, Linux, and macOS
- COM interop and Windows registry access as a PowerShell alternative
- Maintaining or extending existing C# codebases

## Default Approach

- Target **.NET 8 LTS** unless the user specifies an older version or Unity constraint.
- Use the `dotnet` CLI for project creation, build, and run — no IDE required.
- Use `async`/`await` throughout for I/O-bound operations.
- Load secrets from environment variables or `IConfiguration` — never hard-code credentials.
- Prefer `using` statements for all `IDisposable` resources (streams, database connections, Excel COM objects).

## Project Structure

```
MyTool/
  MyTool.csproj
  Program.cs
  Models/
  Services/
  appsettings.json    ← non-secret config
  .env.example        ← document required env vars
```

For library projects add a `MyTool.Tests/` sibling with `xunit` or `nunit`.

## Quality Bar

- Enable nullable reference types: `<Nullable>enable</Nullable>` in the `.csproj`.
- Use `record` for immutable data objects.
- Use `ILogger<T>` for logging — never `Console.WriteLine` in production code.
- Validate all external inputs (CLI args, API responses, CSV rows) before using them.
- Release COM objects explicitly via `Marshal.ReleaseComObject` to avoid Excel hanging after Office interop.

## What To Deliver

- Provide the exact `dotnet new` command and the `.csproj` file.
- List all NuGet packages and their install commands (`dotnet add package`).
- Provide the exact run command (`dotnet run` or the built executable path).
- Explain `appsettings.json` vs environment variable configuration.
- Mention any SDK prerequisites (e.g., .NET 8 SDK download).

## Deep References

Load these when the task is non-trivial:

- [../patterns/csharp-patterns.md](../patterns/csharp-patterns.md) — program skeleton with top-level statements, LINQ idioms, async/await with `CancellationToken`, Excel via EPPlus, COM release guard, `IConfiguration` for secrets, `using` disposal, anti-patterns.
- [../recipes/csharp-excel-report.md](../recipes/csharp-excel-report.md) — .NET 8 console app that reads CSV files and generates a formatted Excel report using EPPlus.
