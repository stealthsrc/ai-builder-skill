---
name: ai-builder
description: Route practical office, Windows automation, lightweight browser tools, business scripting, and security-hardening requests to the right implementation approach. Use when an AI agent needs to build, maintain, review, or harden Excel, Word, or Outlook macros, Windows file or system automation, HTML/CSS/JavaScript utilities, CSV or Excel report pipelines, or similar admin and no-code workflows where VBA, PowerShell, Python, or plain web stack should be chosen pragmatically and safely.
---

# AI Builder

Use this skill as a hub for business automation requests that need a practical implementation, not architecture work.

## Canonical Source

This skill exists in two equivalent entry points for different runtimes:

- `AGENTS.md` is the canonical repo-native instruction file for Codex CLI, Gemini CLI (via `context.fileName`), Antigravity, and any harness that reads `AGENTS.md`.
- `SKILL.md` (this file) is the canonical skill-format entry point for Claude Code skills, Claude Web skills, ChatGPT Apps / Custom GPT, and any harness that loads packaged skills.

Both entry points route to the same references under `references/`. Thin platform adapters (`CLAUDE.md`, `GEMINI.md`, `ANTIGRAVITY.md`) import `AGENTS.md` so the routing stays single-sourced.

## Start Here

- Read the user request and identify the actual business task before choosing a language.
- Read [references/rules/output-and-safety.md](references/rules/output-and-safety.md) for the shared response and safety baseline.
- If the request touches credentials, secrets, external downloads, command execution, file deletion, COM automation, email, or asks for an audit or hardening pass, also read [references/rules/security-baseline.md](references/rules/security-baseline.md).
- If the request includes multiple risk signals or the blast radius is unclear, also read [references/rules/risk-trigger-matrix.md](references/rules/risk-trigger-matrix.md).
- If the user explicitly mentions Codex, Claude Code, Claude, Gemini CLI, `CLAUDE.md`, or `GEMINI.md`, also read the matching file under [references/platforms/](references/platforms).
- For office-heavy, admin, or no-code requests, read [references/builders/office-script-builder.md](references/builders/office-script-builder.md) first.
- For lightweight browser-based tools, static dashboards, forms, or no-framework frontend requests, read [references/builders/html-css-javascript-builder.md](references/builders/html-css-javascript-builder.md).
- For security reviews or risky automation flows, read [references/builders/security-builder.md](references/builders/security-builder.md) before the language-specific builder.
- For explicit language requests, jump directly to the matching builder reference.
- Load only the references that materially improve the answer.

## Route The Request

- Use [references/builders/vba-builder.md](references/builders/vba-builder.md) for Office desktop macros, worksheet logic, workbook events, buttons, forms, and existing macro maintenance.
- Use [references/builders/powershell-builder.md](references/builders/powershell-builder.md) for Windows-native automation, file and folder operations, COM automation, scheduled tasks, and operational scripting.
- Use [references/builders/python-builder.md](references/builders/python-builder.md) for data processing, CSV or Excel transformations, SQL queries, PDF or API workflows, reporting, ETL, and automation that benefits from portability or maintainability.
- Use [references/builders/html-css-javascript-builder.md](references/builders/html-css-javascript-builder.md) for lightweight browser tools, static internal utilities, landing pages, forms, dashboards, and no-framework frontend work that should stay portable and easy to hand off.
- Use [references/builders/google-apps-script-builder.md](references/builders/google-apps-script-builder.md) for Google Workspace automation — Sheets macros, Docs generation, Gmail workflows, Drive management, and any task that is the Google equivalent of a VBA or Office workflow.
- Use [references/builders/typescript-node-builder.md](references/builders/typescript-node-builder.md) for CLI scripts, lightweight Node APIs, file-processing pipelines, Discord/Slack bots, and cross-platform automation that needs more than a browser but less than a full backend framework.
- Use [references/builders/bash-shell-builder.md](references/builders/bash-shell-builder.md) for Linux and macOS shell automation, CI/CD scripts, cron jobs, system administration, and pipelines that wrap other CLI tools.
- Use [references/builders/react-builder.md](references/builders/react-builder.md) for internal tools, admin panels, multi-step forms, and vibe-coded UIs that need component state — use Vite + TypeScript by default, no heavy framework.
- Use [references/builders/c-cpp-builder.md](references/builders/c-cpp-builder.md) for systems programming, embedded firmware, performance-critical tools, and C/C++ codebases.
- Use [references/builders/csharp-builder.md](references/builders/csharp-builder.md) for Windows desktop apps, .NET automation scripts, ASP.NET Core APIs, Office VSTO, and Unity game scripts.
- Use [references/builders/java-builder.md](references/builders/java-builder.md) for enterprise applications, Spring Boot microservices, Android apps, and complex JVM-based pipelines.
- Use [references/builders/php-builder.md](references/builders/php-builder.md) for web backends, Laravel or Symfony applications, WordPress customization, and server-side scripts.
- Use [references/builders/sql-builder.md](references/builders/sql-builder.md) when SQL itself is the primary deliverable — schema migrations, complex reporting queries, data cleanup, index tuning, and views.
- Use [references/builders/ruby-builder.md](references/builders/ruby-builder.md) for automation scripts, Rails or Sinatra web services, Rake tasks, Jekyll sites, and REST API clients.
- Use [references/builders/vb-net-builder.md](references/builders/vb-net-builder.md) for Windows Forms apps and existing Visual Basic .NET codebases.
- Use [references/builders/r-builder.md](references/builders/r-builder.md) for statistical analysis, data visualization, R Markdown or Quarto reports, and data science workflows.
- Use [references/builders/swift-builder.md](references/builders/swift-builder.md) for iOS and macOS apps, SwiftUI interfaces, and command-line tools on macOS.
- Use [references/builders/rust-builder.md](references/builders/rust-builder.md) for systems tools, high-performance CLI utilities, WebAssembly targets, and memory-safe alternatives to shell scripts.
- Use [references/builders/go-builder.md](references/builders/go-builder.md) for CLI tools, REST APIs, microservices, file processing, and cross-platform single-binary tools.
- Use [references/builders/kotlin-builder.md](references/builders/kotlin-builder.md) for Android apps, Ktor backend services, Gradle build scripts, and modern JVM projects.
- Use [references/builders/elixir-builder.md](references/builders/elixir-builder.md) for Phoenix web APIs, real-time features, fault-tolerant services, and functional data pipelines.
- Use [references/builders/scala-builder.md](references/builders/scala-builder.md) for Spark data pipelines, functional JVM programming, and Kafka or Akka-based systems.
- Use [references/builders/lua-builder.md](references/builders/lua-builder.md) for Roblox game scripts, Love2D or Defold games, Neovim plugin configuration, and embedded Lua scripting.
- Use [references/builders/objective-c-builder.md](references/builders/objective-c-builder.md) for maintaining legacy iOS or macOS Objective-C codebases — prefer the Swift builder for new development.
- Use [references/builders/security-builder.md](references/builders/security-builder.md) when the task is to review, harden, or make safer an automation, or when the implementation will handle secrets, external content, or high-impact actions.
- If the request is ambiguous, choose the smallest viable implementation, state the chosen language briefly, and keep assumptions explicit.

## Deepen Before You Write

When the task is non-trivial, load the matching pattern or recipe alongside the builder:

- patterns live in [references/patterns/](references/patterns) — one file per language with idioms, skeletons, and anti-patterns
- recipes live in [references/recipes/](references/recipes) — end-to-end solutions for common tasks (workbook dedup, bulk rename, CSV merge, Outlook send, KPI dashboard, monthly archive)

Each builder links to its matching pattern and recipes under a "Deep References" section.

## Build The Answer

- Prefer executable code over pseudo-code when the user asks for implementation.
- Optimize for low setup burden and direct copy-paste use when the user appears non-technical.
- Preserve original files unless the user explicitly asks for in-place edits.
- Prefer writing a new output file when the workflow modifies documents, spreadsheets, folders, or reports.
- Default to the safer implementation when two options solve the same task with similar effort.
- Keep configuration visible and minimal.
- Add short comments only where they improve readability.

## Response Contract

- Start non-trivial answers with a brief implementation plan.
- Deliver complete code when code is requested.
- Explain exactly where the code goes and how to run it.
- Include a quick validation method, likely edge cases, and rollback guidance when changes are destructive.

## Reference Notes

- Use files under `references/builders/` for language-specific implementation behavior.
- Use files under `references/rules/` for shared conventions.
- Use files under `references/platforms/` for agent-specific adaptation guidance.
- Treat `references/rules/security-baseline.md` as the shared guardrail for secrets, dangerous language patterns, network use, and file safety.
- Use `references/rules/risk-trigger-matrix.md` when the risk is implicit or spans multiple categories.
- Use files under `references/templates/` only when extending this repository with new builders or derived documentation.
