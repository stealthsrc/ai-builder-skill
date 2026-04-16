# Codex Claude Gemini Crosswalk

Use this reference when you want one repository to stay portable across Codex-style environments, Claude Code, and Gemini CLI.

## Core Mapping

| Concern | Codex-style repo pattern | Claude Code | Gemini CLI |
|---|---|---|---|
| Canonical repo instructions | `AGENTS.md` | `CLAUDE.md` plus import of `AGENTS.md` | `GEMINI.md` or `context.fileName` including `AGENTS.md` |
| Persistent project context | repo instructions and supporting references | `CLAUDE.md` plus auto memory | `GEMINI.md` plus `/memory` |
| Scoped instructions | supporting references and explicit routing | `.claude/rules/` | hierarchical context and project settings |
| Reusable workflows | repo docs, scripts, examples, starter assets | skills and commands | custom commands plus context files |
| Deterministic enforcement | repo process, validation scripts, CI | hooks and settings | trusted folders, settings, sandboxing |
| Safety posture | explicit task scoping and validation | permission settings plus hooks | approval modes, trusted folders, sandbox |

## Recommended Strategy For This Repository

### Source of truth

Keep `AGENTS.md` and `SKILL.md` as the primary source of truth.

### Claude Code adapter

Add a minimal `CLAUDE.md` that imports `AGENTS.md`.

### Gemini CLI adapter

Either:

- add a minimal `GEMINI.md`, or
- configure Gemini CLI to read `AGENTS.md` through `context.fileName`

## Practical Portability Rule

Do not duplicate the whole routing system three times.

Instead:

1. keep the main routing logic in repo-owned files
2. add thin platform adapters
3. keep platform-specific mechanics in `references/platforms/`

## What Each Platform Is Best At Here

### Codex-style environments

- repository-driven task routing
- validation-oriented coding workflows
- decomposable coding tasks

### Claude Code

- rich skill frontmatter
- path-scoped rules
- hooks for deterministic automation

### Gemini CLI

- hierarchical context via `GEMINI.md`
- trusted-folder safety model
- explicit sandboxing and expansion flow

## Suggested Repo Convention

If you want one repo to work cleanly everywhere:

- `AGENTS.md` stays canonical
- `CLAUDE.md` imports `AGENTS.md`
- Gemini either reads `AGENTS.md` via settings or imports it from `GEMINI.md`
- builder and risk references stay in `references/`

## Official References

- AGENTS.md standard: https://github.com/openai/agents.md
- Claude Code memory: https://code.claude.com/docs/en/memory
- Claude Code skills: https://code.claude.com/docs/en/skills
- Gemini CLI context files: https://geminicli.com/docs/cli/gemini-md/
- Gemini CLI trusted folders: https://geminicli.com/docs/cli/trusted-folders/
