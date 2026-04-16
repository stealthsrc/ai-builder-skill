# Google Apps Script Builder

Use this reference for Google Workspace automation: Sheets, Docs, Drive, Gmail, Forms, and Calendar macros.

## Use It For

- Google Sheets macros, formulas, and workbook automation
- Google Docs generation and templating
- Gmail drafting, filtering, and batch send workflows
- Drive file management and folder automation
- Time-based or trigger-based workflows in Google Workspace
- replacing VBA workflows for teams that have migrated to Google Workspace

## Default Approach

- Write Apps Script (JavaScript-based) that runs inside the Google project editor.
- Prefer `getValues()` / `setValues()` over cell-by-cell iteration — a single batch call is 100× faster for large ranges.
- Keep configurable values (sheet names, column indices, thresholds) in a visible `CONFIG` block at the top.
- Use `PropertiesService` for secrets and configuration that must not be hard-coded.
- Prefer `Logger.log()` for debugging and `SpreadsheetApp.getActiveSpreadsheet()` as the safe default entry point.

## Execution Limits

| Account type | Max run time | Daily triggers |
|---|---|---|
| Consumer (@gmail.com) | 6 min | 20 |
| Google Workspace | 30 min | unlimited |

Batch all reads and writes. Never call `getRange().getValue()` inside a loop over rows — always read the full range first, transform in memory, then write back.

## Script Editor Entry Point

- Open the script editor from **Extensions → Apps Script** (Sheets/Docs) or directly at script.google.com.
- Scripts are attached to a Spreadsheet, Document, or Standalone project.
- Tell the user which attachment type the solution uses.
- Tell the user to authorize the script on first run (OAuth consent for the required Workspace scopes).

## Safety And Practical Limits

- Do not hard-code OAuth tokens, API keys, or passwords in the script. Use `PropertiesService.getScriptProperties()`.
- GmailApp send is quota-limited — consumer accounts are capped at 100 emails/day, Workspace at 1,500.
- DriveApp and Sheets mutations are irreversible in bulk — always offer a backup tab or copy workflow first.
- Read the security baseline before any workflow that sends email, calls external URLs, or deletes files.

## What To Deliver

- State the attachment type (Spreadsheet-bound, Document-bound, or Standalone).
- Provide the full script ready to paste in the editor.
- Explain how to set up any triggers (time-based or installable) the script uses.
- Include a quick validation path and any quota caveats.

## Deep References

Load these when the task is non-trivial:

- [../patterns/google-apps-script-patterns.md](../patterns/google-apps-script-patterns.md) — skeleton with `CONFIG` block, batch read/write idioms, `PropertiesService` usage, `UrlFetchApp` with retry, `GmailApp` safe send, time-based trigger setup, quota-aware loops, anti-patterns.
- [../recipes/sheets-dedup.md](../recipes/sheets-dedup.md) — full dedup-by-key macro with backup tab and status log, Google Sheets equivalent of the VBA dedup recipe.
