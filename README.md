<p align="center">
  <img src="assets/ai-builder-banner.svg" alt="AI Builder banner" width="100%">
</p>

<p align="center">
  <a href="https://github.com/StealthyLabsHQ/ai-builder-skill/blob/main/LICENSE"><img src="https://img.shields.io/github/license/StealthyLabsHQ/ai-builder-skill?style=flat-square" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/routing-VBA%20%7C%20PowerShell%20%7C%20Python%20%7C%20HTML%2FCSS%2FJS-16333B?style=flat-square" alt="Routing badge">
  <img src="https://img.shields.io/badge/focus-business%20automation%20%2B%20security-1F766C?style=flat-square" alt="Focus badge">
</p>

<p align="center">
  A practical skill hub for Office automation, Windows scripting, lightweight browser tools, data workflows, and security-aware code generation.
</p>

## What AI Builder Is

AI Builder is a routing-first skill repository for practical automation work.

It helps an AI assistant choose the right implementation path before code is written:

- `HTML/CSS/JavaScript` for lightweight browser tools and static frontends
- `VBA` for Office desktop macros and workbook logic
- `PowerShell` for Windows-native automation and COM workflows
- `Python` for data pipelines, reporting, and maintainable scripting
- `Security-first guidance` for risky or high-impact automation

This repository is optimized for real operating work:

- Excel cleanup and workbook automation
- Windows file and folder tasks
- internal dashboards and browser tools
- report generation from CSV or export data
- safer handling of secrets, paths, commands, and destructive actions

## Why It Exists

Most internal automation requests do not need an app framework.

They need the smallest viable implementation that fits the user's actual environment, setup burden, and skill level. AI Builder exists to make those requests routable, consistent, and safer by default.

It is especially useful when the person asking for help is close to spreadsheets, reports, folders, exports, and internal business processes rather than full-time software engineering.

## Routing Model

| Request type | Default route |
|---|---|
| Lightweight browser tool, static dashboard, or no-framework frontend | `references/builders/html-css-javascript-builder.md` |
| Office desktop macro or existing macro maintenance | `references/builders/vba-builder.md` |
| Windows-native automation or operational scripting | `references/builders/powershell-builder.md` |
| Cross-file data processing or maintainable automation | `references/builders/python-builder.md` |
| Hardening, audit, risky automation, secrets, or high-impact operations | `references/builders/security-builder.md` |
| No-code, admin, or office-heavy request with no explicit language | `references/builders/office-script-builder.md` first |

If the request is ambiguous, the skill should choose the safest practical option with the lowest setup burden.

## What Makes It Different

### 1. Routing before coding

The main job is not to generate code blindly. The main job is to pick the right execution path first.

### 2. Built for practical users

The output model is designed for people who need copy-paste-ready automation with clear run instructions, not architecture lectures.

### 3. Security is part of the workflow

The repository includes a shared security baseline for tasks involving:

- secrets, credentials, tokens, or signed URLs
- downloads, web requests, and external content
- command execution and external processes
- file overwrite, deletion, move, or rename operations
- Office automation, email, exports, and PII-bearing flows
- AI-assisted or agent-driven automation with untrusted input

The security guidance is intentionally pragmatic and adapted from the excellent `StealthyLabsHQ/security-hardening` corpus to fit this narrower business-automation scope.

## Example Requests

```text
Clean this workbook, remove blank rows, and highlight duplicate invoice IDs.
```

```text
Build a small HTML/CSS/JavaScript dashboard to track weekly sales KPIs.
```

```text
Rename all PDF files in this Windows folder using the date in the filename.
```

```text
Merge these CSV exports and generate a simple Excel report in Python.
```

```text
Fix this existing VBA macro and make it safer before it sends Outlook emails.
```

```text
Review this PowerShell script for dangerous patterns and harden it.
```

For more concrete routing examples, see [examples/concrete-use-cases.md](examples/concrete-use-cases.md).

## Repository Layout

```text
.
|-- AGENTS.md
|-- LICENSE
|-- README.md
|-- SKILL.md
|-- assets/
|   |-- ai-builder-banner.svg
|   `-- ai-builder-social-preview.svg
|-- examples/
|   `-- concrete-use-cases.md
`-- references/
    |-- builders/
    |   |-- html-css-javascript-builder.md
    |   |-- office-script-builder.md
    |   |-- powershell-builder.md
    |   |-- python-builder.md
    |   |-- security-builder.md
    |   `-- vba-builder.md
    |-- rules/
    |   |-- output-and-safety.md
    |   `-- security-baseline.md
    `-- templates/
        `-- builder-template.md
```

## Start Here

If you are using this repository as a skill source:

1. Read [SKILL.md](SKILL.md) for the orchestration logic.
2. Read [references/builders/office-script-builder.md](references/builders/office-script-builder.md) for office-heavy and admin-heavy routing.
3. Load the matching builder for the request.
4. Load [references/rules/security-baseline.md](references/rules/security-baseline.md) when the task touches risky operations.

## Who This Is For

AI Builder is especially useful for:

- operations and back-office teams
- analysts working with Excel and CSV exports
- Windows admins and power users
- founders automating internal workflows
- AI users who want practical scripts instead of generic prompt bundles

## Visual Assets

The repository includes:

- [assets/ai-builder-banner.svg](assets/ai-builder-banner.svg) for the README hero
- [assets/ai-builder-social-preview.svg](assets/ai-builder-social-preview.svg) as a ready-made social preview asset for GitHub repo settings

## Roadmap Direction

Likely next extensions:

- richer Office-specific security guidance
- reusable static frontend patterns and examples
- more concrete VBA, PowerShell, Python, and browser-tool workflows
- installation notes for multiple AI tooling environments
- audit-oriented references for no-code and connector-heavy operations

## License

This repository uses the [MIT License](LICENSE).
