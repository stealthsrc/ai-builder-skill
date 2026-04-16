# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by Keep a Changelog and the version labels in this file are intended to support future Git tags and GitHub releases.

## [Unreleased]

- No unreleased changes yet.

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

[Unreleased]: https://github.com/StealthyLabsHQ/ai-builder-skill/compare/v0.2.0...main
[0.2.0]: https://github.com/StealthyLabsHQ/ai-builder-skill/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/StealthyLabsHQ/ai-builder-skill/releases/tag/v0.1.0
