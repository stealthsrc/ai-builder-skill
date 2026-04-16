# Office Script Builder

Use this reference first for office-heavy, no-code, and administrative workflows.

## Choose The Implementation

- Choose VBA when the automation belongs inside Excel, Word, or Outlook desktop and needs macros, worksheet events, buttons, forms, or maintenance of an existing macro-enabled file.
- Choose PowerShell when the workflow is Windows-native, operational, or file-system heavy, or when Office should be automated from outside the document through COM.
- Choose Python when the workflow spans multiple files, needs structured data transformations, or will be easier to maintain as a reusable script.

## Default Priorities

- Prefer the smallest viable solution.
- Minimize setup steps and third-party dependencies.
- Keep instructions explicit enough for a non-developer to follow.
- Preserve source files by default and write outputs to a new file or folder when practical.
- Make overwrite behavior obvious.

## Response Expectations

- State the chosen language briefly when it was not explicitly requested.
- Explain why the selected option fits the task better than the nearby alternatives.
- Tell the user exactly where to paste or save the code.
- Tell the user exactly how to run it and how to confirm it worked.

## Quick Routing Hints

- Excel cleanup, workbook buttons, worksheet formulas, or event handlers usually map to VBA.
- Bulk renaming, folder moves, scheduled jobs, Windows administration, or COM automation usually map to PowerShell.
- CSV merges, Excel reporting, PDF extraction, API pulls, or repeatable data pipelines usually map to Python.
