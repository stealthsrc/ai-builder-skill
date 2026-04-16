# AI Builder

> A practical skill hub for Office automation, Windows scripting, lightweight business tooling, and security-aware workflow generation.

AI Builder helps route real-world automation requests to the right implementation path:

- `HTML/CSS/JavaScript` for lightweight browser tools and static frontends
- `VBA` for Office desktop macros and workbook logic
- `PowerShell` for Windows-native automation and COM workflows
- `Python` for data pipelines, reporting, and maintainable scripting
- `Security-first guidance` for risky or high-impact automation

It is built for people who live close to Excel, folders, reports, admin workflows, and internal business operations, not just full-time software engineers.

---

## Why This Exists

Most automation requests are not framework problems. They are practical work problems:

- clean and reformat a workbook
- rename or move batches of files
- merge CSV exports into a report
- automate an Office task without overengineering it
- harden a script before it touches files, secrets, or production data

This skill exists to make those requests routable, consistent, and safe.

Instead of treating every task like a generic coding problem, AI Builder chooses the smallest viable implementation for the user's environment and technical level.

---

## What The Skill Does

AI Builder acts as a hub-and-references skill:

| Area | What it helps with |
|---|---|
| Lightweight frontend build | HTML, CSS, JavaScript dashboards, forms, calculators, static internal tools |
| Office automation | Excel, Word, Outlook macros, worksheet logic, workbook events, buttons, forms |
| Windows operations | File and folder automation, COM scripting, scheduled tasks, admin-heavy workflows |
| Data processing | CSV merges, Excel reporting, ETL-style scripts, structured transformations |
| Safer automation | Secret handling, destructive action awareness, bounded paths, safer command execution |
| Audience adaptation | Copy-paste-ready guidance for non-developers, concise structure for technical users |

---

## Routing Model

The skill uses a simple routing model:

| Request type | Default route |
|---|---|
| Lightweight browser tool, static dashboard, or no-framework frontend | `references/builders/html-css-javascript-builder.md` |
| Office desktop macro or existing macro maintenance | `references/builders/vba-builder.md` |
| Windows-native automation or operational scripting | `references/builders/powershell-builder.md` |
| Cross-file data processing or maintainable automation | `references/builders/python-builder.md` |
| Hardening, audit, risky automation, secrets, or high-impact operations | `references/builders/security-builder.md` |
| No-code / admin / office-heavy request with no explicit language | `references/builders/office-script-builder.md` first |

If the user does not specify a language, AI Builder chooses the safest practical option with the lowest setup burden.

---

## Security Is Built In

This is not just a code-routing skill.

AI Builder includes a shared security baseline for tasks that involve:

- credentials, API keys, tokens, or signed URLs
- file overwrite, deletion, rename, or move operations
- command execution and external process launching
- downloads, web requests, webhooks, and external content
- Office COM automation, email, exports, or PII-bearing workflows
- AI-assisted or agent-driven automation that could act on untrusted input

The security layer is intentionally pragmatic:

- prefer new output files over silent in-place changes
- avoid hardcoded secrets
- bound paths before touching the filesystem
- avoid unsafe language-specific patterns
- explain validation, rollback, and blast radius clearly

The current security guidance was shaped with help from the excellent `StealthyLabsHQ/security-hardening` corpus and adapted to this repository's narrower business-automation scope.

---

## Repository Layout

```text
.
|-- SKILL.md
|-- AGENTS.md
|-- LICENSE
|-- README.md
`-- references/
    |-- builders/
    |   |-- html-css-javascript-builder.md
    |   |-- office-script-builder.md
    |   |-- security-builder.md
    |   |-- powershell-builder.md
    |   |-- python-builder.md
    |   `-- vba-builder.md
    |-- rules/
    |   |-- output-and-safety.md
    |   `-- security-baseline.md
    `-- templates/
        `-- builder-template.md
```

### Design Philosophy

- Keep the root `SKILL.md` as the orchestration hub
- Load only the references that materially help with the current task
- Prefer executable, maintainable solutions over abstract guidance
- Preserve clarity for non-technical users
- Default to the smallest viable implementation

---

## Typical Prompts

Examples of requests this skill is designed to handle well:

```text
Clean this Excel workbook and highlight duplicate invoice IDs.
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

---

## Who It Is For

AI Builder is especially useful for:

- operations and back-office teams
- analysts working with Excel and CSV exports
- admins and power users on Windows
- founders and small teams automating internal workflows
- AI users who need practical scripts, not app architecture

It assumes many users are not full-time developers and optimizes for:

- fewer setup steps
- direct copy-paste execution
- clear run instructions
- visible configuration
- operational safety

---

## How To Use It

This repository is structured as a skill source.

The canonical behavior lives in [SKILL.md](SKILL.md), while implementation-specific and safety-specific behavior lives under [`references/`](references).

If you are using a skill-aware coding assistant, point it at this repository or copy the skill files into your local skill system. If you are using the repository manually, start with:

1. `SKILL.md`
2. `references/builders/office-script-builder.md`
3. the matching language builder
4. `references/rules/security-baseline.md` when the task is risky

---

## Current Focus

The repository is intentionally narrow.

It is optimized for:

- lightweight frontend tools
- Office automation
- Windows scripting
- business data workflows
- secure-by-default scripting guidance

It is not trying to be a general software engineering framework or a giant generic prompt library.

---

## Roadmap Direction

Likely next extensions:

- richer Office-specific security references
- reusable static frontend patterns and examples
- reusable examples for common VBA, PowerShell, and Python workflows
- public installation notes for multiple AI tooling environments
- audit-oriented references for internal automation and no-code connectors

---

## License

This repository currently uses the [MIT License](LICENSE).
