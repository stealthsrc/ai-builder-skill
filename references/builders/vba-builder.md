# VBA Builder

Use this reference for Office desktop macros and maintenance of existing VBA code.

## Build Safely

- Start modules with `Option Explicit`.
- Prefer direct object references over `Select` and `Activate`.
- Keep configurable worksheet names, ranges, paths, and constants in a visible block near the top.
- Use clear procedure names such as `CleanSalesSheet` or `ExportWeeklyReport`.
- Restore Excel application state when using `ScreenUpdating`, `EnableEvents`, or `Calculation`.

## Structure The Solution

- Use a standard module for normal macros.
- Use worksheet or workbook code modules only for events or when the existing workbook already depends on them.
- Use helper procedures when the logic would otherwise become difficult to follow.
- Prefer late binding for other Office apps or COM objects unless the environment is tightly controlled.

## Tell The User How To Run It

- Explain whether the code belongs in a standard module, a worksheet module, `ThisWorkbook`, or another Office host.
- Tell the user how to open the VBA editor with `Alt+F11`.
- Tell the user when the file must be saved as `.xlsm`, `.docm`, or another macro-enabled format.
- Mention that macro security settings may block execution until macros are enabled.

## Validate And Protect Data

- Recommend testing on a copy of the workbook or document first.
- State what sheets, ranges, files, or messages will be modified.
- When deleting or rewriting data, prefer a preview mode or a backup sheet if the extra complexity is small.
- Include a simple validation path such as checking row counts, created sheets, or exported files.
