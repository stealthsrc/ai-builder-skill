# Visual Basic .NET Builder

Use this reference for Windows Forms desktop applications, .NET automation scripts, and legacy VB.NET codebases that need maintenance or extension.

## Use It For

- Windows Forms (WinForms) desktop applications
- .NET console scripts and automation tools for Windows
- Maintaining and extending existing VB.NET codebases
- Office automation via VSTO or the Office Interop assemblies in .NET
- DataGridView-based data entry and reporting tools
- Migrating VBA macros to a standalone .NET desktop application

## When To Use VB.NET vs C#

- **Use VB.NET** when the existing codebase, team, or customer is already in VB.NET — do not force a rewrite.
- **Use C#** for new .NET projects unless there is a specific reason to stay in VB.NET.
- VB.NET and C# compile to the same IL — they share all .NET libraries and can reference each other's assemblies.

## Default Approach

- Target **.NET 6 LTS or .NET 8 LTS** for new projects; target **.NET Framework 4.8** only if the existing codebase requires it.
- Use `Option Strict On` and `Option Explicit On` at the top of every file — equivalent to `strict: true` in TypeScript.
- Use `Using` blocks for all `IDisposable` resources (streams, database connections, COM objects).
- Load configuration from `app.config`, `appsettings.json`, or environment variables — never hard-code connection strings or API keys.

## Quality Bar

- Never suppress warnings with `#Disable Warning` unless unavoidable legacy interop.
- Use `Try`/`Catch` with specific exception types.
- Prefer `List(Of T)` and `Dictionary(Of TKey, TValue)` over untyped `ArrayList` or `Hashtable`.
- Validate all user input from form controls before use.
- Release COM objects with `Marshal.ReleaseComObject` in a `Finally` block for Office interop.

## What To Deliver

- State whether the project targets .NET (modern) or .NET Framework (legacy).
- Provide the `.vbproj` file or the `dotnet new` command.
- For Windows Forms: describe the form layout and control names alongside the code.
- Provide the exact build and run command (`dotnet run` or Visual Studio setup steps).

## Deep References

Load these when the task is non-trivial:

- [../patterns/vb-net-patterns.md](../patterns/vb-net-patterns.md) — module and class skeleton with `Option Strict On`, Windows Forms event-handler pattern, DataGridView binding, file I/O, ADO.NET safe queries, Office COM release, anti-patterns.
