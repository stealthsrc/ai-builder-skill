# ai-builder-skill

<p align="center">
  <a href="https://github.com/StealthyLabsHQ/ai-builder-skill/blob/main/LICENSE"><img src="https://img.shields.io/github/license/StealthyLabsHQ/ai-builder-skill?style=flat-square" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/runtimes-Codex%20%7C%20Claude%20Code%20%7C%20Claude%20Web%20%7C%20ChatGPT%20%7C%20Gemini%20CLI%20%7C%20Antigravity-16333B?style=flat-square" alt="Runtimes badge">
  <img src="https://img.shields.io/badge/routing-VBA%20%7C%20PowerShell%20%7C%20Python%20%7C%20HTML%2FCSS%2FJS-1F766C?style=flat-square" alt="Routing badge">
  <img src="https://img.shields.io/badge/focus-business%20automation%20%2B%20security-5B2A86?style=flat-square" alt="Focus badge">
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
|-- .github/workflows/ci.yml
|-- .antigravity/
|   |-- commands/ai-builder.md
|   |-- rules/ai-builder.md
|   `-- settings.example.json
|-- .claude/
|   |-- commands/ai-builder.md
|   |-- skills/ai-builder/SKILL.md
|   `-- settings.example.json
|-- .gemini/settings.example.json
|-- AGENTS.md
|-- ANTIGRAVITY.md
|-- CHANGELOG.md
|-- CLAUDE.md
|-- CLAUDE.local.example.md
|-- GEMINI.md
|-- GEMINI.local.example.md
|-- LICENSE
|-- README.md
|-- SKILL.md
|-- agents/openai.yaml
|-- assets/starters/
|   |-- html-tool/
|   |-- powershell-script/
|   |-- python-cli/
|   `-- vba-module/
|-- dist/
|   `-- chatgpt-custom-gpt.md
|-- eval/routing-cases.json
|-- examples/
|   |-- browser-kpi-tool/
|   |-- concrete-use-cases.md
|   |-- prompt-cookbook.md
|   |-- powershell/
|   |-- python/
|   |-- security/
|   `-- vba/
|-- references/
|   |-- builders/
|   |   |-- html-css-javascript-builder.md
|   |   |-- office-script-builder.md
|   |   |-- powershell-builder.md
|   |   |-- python-builder.md
|   |   |-- security-builder.md
|   |   `-- vba-builder.md
|   |-- patterns/
|   |   |-- html-js-patterns.md
|   |   |-- powershell-patterns.md
|   |   |-- python-patterns.md
|   |   `-- vba-patterns.md
|   |-- recipes/
|   |   |-- archive-by-date.md
|   |   |-- bulk-rename-safe.md
|   |   |-- csv-merge-excel-ready.md
|   |   |-- dedup-workbook.md
|   |   |-- kpi-dashboard.md
|   |   `-- outlook-send-confirmed.md
|   |-- platforms/
|   |   |-- antigravity.md
|   |   |-- chatgpt.md
|   |   |-- claude-code-hooks.md
|   |   |-- claude-code.md
|   |   |-- claude-web.md
|   |   |-- codex-claude-gemini-crosswalk.md
|   |   |-- codex-task-shaping.md
|   |   |-- codex.md
|   |   `-- gemini-cli.md
|   |-- rules/
|   |   |-- output-and-safety.md
|   |   |-- risk-trigger-matrix.md
|   |   `-- security-baseline.md
|   `-- templates/builder-template.md
|-- release-notes/
`-- scripts/
    |-- build_skill_bundle.py
    |-- check_eval_cases.py
    `-- validate_repo.py
```

## Patterns And Recipes

The builders are routers. The depth for code generation lives in two layers loaded on demand:

- **Patterns** — one file per language with skeletons, idioms, and anti-patterns:
  - [references/patterns/vba-patterns.md](references/patterns/vba-patterns.md)
  - [references/patterns/powershell-patterns.md](references/patterns/powershell-patterns.md)
  - [references/patterns/python-patterns.md](references/patterns/python-patterns.md)
  - [references/patterns/html-js-patterns.md](references/patterns/html-js-patterns.md)

- **Recipes** — end-to-end solutions with code, run steps, validation, and rollback:
  - [references/recipes/dedup-workbook.md](references/recipes/dedup-workbook.md) (VBA)
  - [references/recipes/bulk-rename-safe.md](references/recipes/bulk-rename-safe.md) (PowerShell)
  - [references/recipes/csv-merge-excel-ready.md](references/recipes/csv-merge-excel-ready.md) (Python)
  - [references/recipes/outlook-send-confirmed.md](references/recipes/outlook-send-confirmed.md) (VBA + PowerShell)
  - [references/recipes/kpi-dashboard.md](references/recipes/kpi-dashboard.md) (HTML/CSS/JS)
  - [references/recipes/archive-by-date.md](references/recipes/archive-by-date.md) (PowerShell)

Each builder links to its matching pattern and recipes under a **Deep References** section so progressive-disclosure runtimes (Claude Skills, ChatGPT knowledge files) load only what the task needs.

## Multi-Runtime Support

This repository is designed to run cleanly across six AI runtimes behind one routing hub:

| Runtime | Entry point | Adapter |
|---|---|---|
| Codex CLI | `AGENTS.md` | native |
| Claude Code | `CLAUDE.md` imports `@AGENTS.md` | `.claude/skills/ai-builder/`, `.claude/commands/ai-builder.md` |
| Claude Web Skills | `SKILL.md` bundle | `scripts/build_skill_bundle.py` → `dist/ai-builder.zip` |
| ChatGPT | `agents/openai.yaml` + `dist/chatgpt-custom-gpt.md` | paste-ready Custom GPT system prompt |
| Gemini CLI | `GEMINI.md` or `context.fileName` | `.gemini/settings.example.json` |
| Antigravity (Google) | `AGENTS.md` + `ANTIGRAVITY.md` | `.antigravity/rules/`, `.antigravity/commands/` |

See [references/platforms/codex-claude-gemini-crosswalk.md](references/platforms/codex-claude-gemini-crosswalk.md) for the full mapping.

## Start Here

If you are using this repository as a skill source:

1. Read [SKILL.md](SKILL.md) for the orchestration logic.
2. Read [references/builders/office-script-builder.md](references/builders/office-script-builder.md) for office-heavy and admin-heavy routing.
3. Load the matching builder for the request.
4. Load the matching file under [references/patterns/](references/patterns) when the task is non-trivial.
5. Load the matching recipe under [references/recipes/](references/recipes) when the task matches one of the end-to-end templates.
6. Load [references/rules/security-baseline.md](references/rules/security-baseline.md) when the task touches risky operations.
7. Load [references/rules/risk-trigger-matrix.md](references/rules/risk-trigger-matrix.md) if the risk is implicit or mixed.

## Install

Use the repository in the simplest way your AI tool supports:

### Codex-style project instructions

- keep the repository as-is in your working context, or
- reuse [AGENTS.md](AGENTS.md) and [SKILL.md](SKILL.md) in the project where you want the routing behavior

### Claude-style local skills

- point Claude at the repository root as a local skill source
- use [CLAUDE.md](CLAUDE.md) as the thin Claude adapter
- copy [.claude/settings.example.json](.claude/settings.example.json) to `.claude/settings.json` if you want a shared project baseline
- copy [CLAUDE.local.example.md](CLAUDE.local.example.md) to `CLAUDE.local.md` for personal local-only overrides
- load `SKILL.md` as the primary instruction file
- keep the `references/` directory available alongside it

### Gemini CLI

- use [GEMINI.md](GEMINI.md) as the thin Gemini adapter, or
- configure Gemini CLI `context.fileName` to include `AGENTS.md`
- copy [.gemini/settings.example.json](.gemini/settings.example.json) to `.gemini/settings.json` for a conservative workspace baseline
- use [GEMINI.local.example.md](GEMINI.local.example.md) as a personal overlay to import from your global or project `GEMINI.md`
- keep `references/` available so Gemini can load only the relevant builder, rule, or platform reference

### Antigravity (Google)

- use [ANTIGRAVITY.md](ANTIGRAVITY.md) as the thin Antigravity adapter (imports `AGENTS.md`)
- keep [.antigravity/rules/ai-builder.md](.antigravity/rules/ai-builder.md) as the scoped rule that points agents at `SKILL.md`
- expose [.antigravity/commands/ai-builder.md](.antigravity/commands/ai-builder.md) as the `/ai-builder` slash command
- copy [.antigravity/settings.example.json](.antigravity/settings.example.json) to `.antigravity/settings.json` for a conservative approval baseline

### ChatGPT (Custom GPT, Projects, Apps SDK)

- paste [dist/chatgpt-custom-gpt.md](dist/chatgpt-custom-gpt.md) into a Custom GPT's Instructions field or a ChatGPT Project system prompt
- attach the knowledge files listed at the top of that file
- use [agents/openai.yaml](agents/openai.yaml) as the distribution manifest when targeting the OpenAI Apps SDK or Agents SDK
- see [references/platforms/chatgpt.md](references/platforms/chatgpt.md) for the full deployment guide

### Claude Web Skills (claude.ai)

- run `python scripts/build_skill_bundle.py` to produce `dist/ai-builder.zip`
- upload that zip to `claude.ai` → Skills
- see [references/platforms/claude-web.md](references/platforms/claude-web.md) for packaging, limits, and safety notes

### Cursor or editor-agent workflows

- use the repository as project context or copy the relevant files into your workspace rules setup
- keep `references/builders/` and `references/rules/` intact so routing and safety remain discoverable

### Generic AI setup

- start with [SKILL.md](SKILL.md)
- add [AGENTS.md](AGENTS.md) when the tool supports persistent repo instructions
- keep [references/](references) available so the assistant can load only what it needs

## Distribution Metadata

This repository now ships UI-facing metadata for skill-aware platforms in [agents/openai.yaml](agents/openai.yaml).

That file is intended for harnesses and skill lists, while [SKILL.md](SKILL.md) remains the canonical behavior layer.

Versioned release notes live in [CHANGELOG.md](CHANGELOG.md).
Draft GitHub release bodies live in [release-notes/](release-notes).

## Platform References

The repository now includes agent-specific adaptation references:

- [references/platforms/codex.md](references/platforms/codex.md)
- [references/platforms/codex-task-shaping.md](references/platforms/codex-task-shaping.md)
- [references/platforms/claude-code.md](references/platforms/claude-code.md)
- [references/platforms/claude-code-hooks.md](references/platforms/claude-code-hooks.md)
- [references/platforms/claude-web.md](references/platforms/claude-web.md)
- [references/platforms/chatgpt.md](references/platforms/chatgpt.md)
- [references/platforms/gemini-cli.md](references/platforms/gemini-cli.md)
- [references/platforms/antigravity.md](references/platforms/antigravity.md)
- [references/platforms/codex-claude-gemini-crosswalk.md](references/platforms/codex-claude-gemini-crosswalk.md)

Use them when the target runtime matters as much as the programming language.

The repository also ships ready-to-use root adapters:

- [CLAUDE.md](CLAUDE.md)
- [GEMINI.md](GEMINI.md)
- [ANTIGRAVITY.md](ANTIGRAVITY.md)
- [CLAUDE.local.example.md](CLAUDE.local.example.md)
- [GEMINI.local.example.md](GEMINI.local.example.md)
- [.claude/settings.example.json](.claude/settings.example.json)
- [.claude/skills/ai-builder/SKILL.md](.claude/skills/ai-builder/SKILL.md)
- [.claude/commands/ai-builder.md](.claude/commands/ai-builder.md)
- [.gemini/settings.example.json](.gemini/settings.example.json)
- [.antigravity/settings.example.json](.antigravity/settings.example.json)
- [.antigravity/rules/ai-builder.md](.antigravity/rules/ai-builder.md)
- [.antigravity/commands/ai-builder.md](.antigravity/commands/ai-builder.md)
- [agents/openai.yaml](agents/openai.yaml)
- [dist/chatgpt-custom-gpt.md](dist/chatgpt-custom-gpt.md)
- [scripts/build_skill_bundle.py](scripts/build_skill_bundle.py)

## Examples And Starters

### Executable examples

- [examples/vba/clean-invoices.bas](examples/vba/clean-invoices.bas)
- [examples/powershell/rename-pdfs-by-date.ps1](examples/powershell/rename-pdfs-by-date.ps1)
- [examples/python/merge-csv-report.py](examples/python/merge-csv-report.py)
- [examples/browser-kpi-tool/](examples/browser-kpi-tool)
- [examples/security/unsafe-to-safe.md](examples/security/unsafe-to-safe.md)

### Prompt guidance

- [examples/prompt-cookbook.md](examples/prompt-cookbook.md)
- [examples/concrete-use-cases.md](examples/concrete-use-cases.md)

### Starter kits

- [assets/starters/html-tool/](assets/starters/html-tool)
- [assets/starters/python-cli/](assets/starters/python-cli)
- [assets/starters/powershell-script/](assets/starters/powershell-script)
- [assets/starters/vba-module/](assets/starters/vba-module)

## Evaluation And CI

The repository now includes:

- routing fixtures in [eval/routing-cases.json](eval/routing-cases.json)
- repository validation in [scripts/validate_repo.py](scripts/validate_repo.py)
- evaluation fixture validation in [scripts/check_eval_cases.py](scripts/check_eval_cases.py)
- GitHub Actions CI in [.github/workflows/ci.yml](.github/workflows/ci.yml)

The goal is simple: make the skill testable as a routing system, not just readable as documentation.

## Who This Is For

AI Builder is especially useful for:

- operations and back-office teams
- analysts working with Excel and CSV exports
- Windows admins and power users
- founders automating internal workflows
- AI users who want practical scripts instead of generic prompt bundles

## Roadmap Direction

Likely next extensions:

- richer Office-specific security guidance
- reusable static frontend patterns and examples
- more concrete VBA, PowerShell, Python, and browser-tool workflows
- stronger install adapters for multiple AI tooling environments
- audit-oriented references for no-code and connector-heavy operations

## License

This repository uses the [MIT License](LICENSE).
