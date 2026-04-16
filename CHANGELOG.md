# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by Keep a Changelog and the version labels in this file are intended to support future Git tags and GitHub releases.

## [Unreleased]

- No unreleased changes yet.

## [0.5.0] - 2026-04-16

### Added

- Four new language builders: `references/builders/google-apps-script-builder.md`, `references/builders/typescript-node-builder.md`, `references/builders/bash-shell-builder.md`, `references/builders/react-builder.md`
- Four new pattern libraries: `references/patterns/google-apps-script-patterns.md`, `references/patterns/typescript-node-patterns.md`, `references/patterns/bash-shell-patterns.md`, `references/patterns/react-patterns.md`
- Five new recipes: `references/recipes/sheets-dedup.md` (GAS), `references/recipes/node-api-csv.md` (Node.js), `references/recipes/sql-query-to-excel.md` (Python+DuckDB), `references/recipes/bash-bulk-archive.md` (Bash), `references/recipes/react-kpi-dashboard.md` (Vite React)
- SQL patterns section in `references/patterns/python-patterns.md` (parameterized SQLite + DuckDB + pandas integration)
- Claude Artifacts section in `references/patterns/html-js-patterns.md` (single-file constraints, safe DOM, inline styles)
- SQL recipe reference in `references/builders/python-builder.md` Deep References

### Changed

- `SKILL.md` routing table expanded to cover all eight builders
- `scripts/validate_repo.py` REQUIRED_FILES extended with all new builders, patterns, and recipes
- `eval/routing-cases.json` expanded from 19 to 24 cases with new builder-specific routing fixtures

## [0.3.0] - 2026-04-16

### Added

- Antigravity adapter: `ANTIGRAVITY.md` root file, `.antigravity/rules/ai-builder.md`, `.antigravity/commands/ai-builder.md`, `.antigravity/settings.example.json`
- ChatGPT adapter: `references/platforms/chatgpt.md`, `dist/chatgpt-custom-gpt.md` paste-ready system prompt, enriched `agents/openai.yaml` (instructions, starter prompts, capabilities, safety posture)
- Claude Web Skills adapter: `references/platforms/claude-web.md`, `scripts/build_skill_bundle.py` producing `dist/ai-builder.zip`
- Claude Code native skill under `.claude/skills/ai-builder/SKILL.md` and slash command `.claude/commands/ai-builder.md`
- Multi-runtime crosswalk rewritten to cover Codex CLI, Claude Code, Claude Web, ChatGPT, Gemini CLI, and Antigravity
- Platform-aware routing evaluation cases in `eval/routing-cases.json`
- Frontmatter limit checks in `scripts/validate_repo.py` (name length, description length for claude.ai Skills)

### Changed

- `SKILL.md` description broadened from Codex-specific to agent-generic
- `SKILL.md` now explicitly names `AGENTS.md` and `SKILL.md` as paired canonical sources for repo-native and skill-format runtimes
- `AGENTS.md` gained a multi-runtime portability table
- `scripts/check_eval_cases.py` now requires a `platform` field and validates it against an allowlist

## [0.2.0] - 2026-04-16

### Added

- Platform-specific references for Codex, Claude Code, and Gemini CLI under `references/platforms/`
- Cross-runtime guidance for keeping one routing repository portable across Codex-style environments, Claude Code, and Gemini CLI
- Root adapter files `CLAUDE.md` and `GEMINI.md`
- Safe baseline settings templates in `.claude/settings.example.json` and `.gemini/settings.example.json`
- Local-only overlay examples in `CLAUDE.local.example.md` and `GEMINI.local.example.md`

### Changed

- Extended `SKILL.md` and `AGENTS.md` to route agent-specific requests through `references/platforms/`
- Expanded `README.md` with multi-agent installation guidance and adapter documentation
- Strengthened repository validation to check platform files, root adapters, and context imports

## [0.1.0] - 2026-04-16

### Added

- Initial public release of the AI Builder skill repository
- Root orchestration model with `SKILL.md` and `AGENTS.md`
- Builder references for Office automation, HTML/CSS/JavaScript, VBA, PowerShell, Python, and security hardening
- Shared safety and risk references for output structure, security baselines, and trigger matrices
- Public-facing `README.md`, MIT license, banner assets, and repository social preview asset
- Executable examples for VBA, PowerShell, Python, browser tools, and security hardening
- Starter assets for browser tools, Python CLI scripts, PowerShell scripts, and VBA modules
- Routing evaluation fixtures, repository validation scripts, and GitHub Actions CI
- OpenAI-facing metadata in `agents/openai.yaml`

[Unreleased]: https://github.com/StealthyLabsHQ/ai-builder-skill/compare/v0.3.0...main
[0.3.0]: https://github.com/StealthyLabsHQ/ai-builder-skill/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/StealthyLabsHQ/ai-builder-skill/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/StealthyLabsHQ/ai-builder-skill/releases/tag/v0.1.0
