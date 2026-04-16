# PowerShell Builder

Use this reference for Windows-native automation, operational scripts, and COM automation.

## Build Safely

- Default to Windows PowerShell 5.1 compatible syntax unless the user explicitly targets PowerShell 7.
- Use `Set-StrictMode -Version Latest` and `$ErrorActionPreference = 'Stop'` for non-trivial scripts.
- Prefer `Join-Path`, `Test-Path`, and `-LiteralPath` for filesystem work.
- Avoid destructive actions without an explicit preview, confirmation switch, or clearly documented behavior.
- Do not assume administrator rights.

## Structure The Script

- Use a `param()` block or a short configuration block at the top.
- Prefer advanced functions or scripts with named parameters when the script will be reused.
- Emit clear status messages for major steps.
- Use `try`/`finally` when automating COM objects so Excel, Word, or Outlook always closes cleanly.

## Tell The User How To Run It

- State the file name and extension, usually `.ps1`.
- Provide the exact command to run, including example arguments.
- Mention execution-policy friction when relevant and prefer a one-time, process-scoped bypass over permanent changes.
- State any prerequisites such as Office desktop being installed for COM automation.

## Validate And Protect Data

- Recommend testing on a sample folder or copied files first.
- If the script changes files, explain the expected before and after state.
- Prefer `-WhatIf` semantics or an explicit dry-run mode when practical.
- Call out common failure modes such as locked files, missing paths, or insufficient permissions.

## Deep References

Load these when the task is non-trivial:

- [../patterns/powershell-patterns.md](../patterns/powershell-patterns.md) — script skeleton, `SupportsShouldProcess`, parameter validation attributes, COM release, splatting, pipeline functions, logging, safe external command execution, anti-patterns.
- [../recipes/bulk-rename-safe.md](../recipes/bulk-rename-safe.md) — regex-based rename with `-WhatIf`, collision detection, and reversible map CSV.
- [../recipes/archive-by-date.md](../recipes/archive-by-date.md) — sweep files into monthly folders with audit log and rollback path.
- [../recipes/outlook-send-confirmed.md](../recipes/outlook-send-confirmed.md) — Outlook send with explicit confirmation token.
