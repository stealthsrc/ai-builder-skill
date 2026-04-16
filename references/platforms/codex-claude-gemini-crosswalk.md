# Multi-Runtime Crosswalk

Use this reference when you want one repository to stay portable across Codex CLI, Claude Code, Claude Web Skills, ChatGPT, Gemini CLI, and Antigravity.

## Core Mapping

| Concern | Codex CLI | Claude Code | Claude Web Skills | ChatGPT | Gemini CLI | Antigravity |
|---|---|---|---|---|---|---|
| Canonical repo instructions | `AGENTS.md` | `CLAUDE.md` imports `AGENTS.md` | `SKILL.md` bundle | `dist/chatgpt-custom-gpt.md` + `agents/openai.yaml` | `GEMINI.md` or `context.fileName` including `AGENTS.md` | `AGENTS.md` + `ANTIGRAVITY.md` |
| Persistent project context | repo files | `CLAUDE.md` + auto memory | uploaded knowledge files | attached knowledge or project files | `GEMINI.md` + `/memory` | `AGENTS.md` + `.antigravity/rules/` |
| Scoped instructions | references + routing | `.claude/rules/` | `SKILL.md` progressive disclosure | system prompt sections | hierarchical context | `.antigravity/rules/*.md` |
| Reusable workflows | repo docs, scripts, examples | skills + `.claude/commands/` | linked files under `references/` | starter prompts + knowledge | custom commands + context | `.antigravity/commands/*.md` |
| Deterministic enforcement | repo process + CI | hooks + settings | none (read-only surface) | none (read-only surface) | trusted folders + sandbox | `.antigravity/settings` approvals |
| Safety posture | task scoping + validation | permissions + hooks | instructions only | instructions only | approval modes + sandbox | approval modes + workspace trust |
| Execution surface | full shell | full shell + tools | none | tools when present | full shell + tools | full shell + MCP tools |

## Recommended Strategy For This Repository

### Source of truth

Keep `AGENTS.md` and `SKILL.md` as the primary source of truth. `AGENTS.md` is canonical for repo-native runtimes. `SKILL.md` is canonical for skill-format runtimes.

### Adapters

- Claude Code: `CLAUDE.md` imports `@AGENTS.md`. `.claude/skills/ai-builder/SKILL.md` mirrors the hub. `.claude/commands/ai-builder.md` exposes `/ai-builder`.
- Claude Web Skills: `scripts/build_skill_bundle.py` produces `dist/ai-builder.zip` for upload to `claude.ai`.
- ChatGPT: `dist/chatgpt-custom-gpt.md` is a paste-ready system prompt. `agents/openai.yaml` is the distribution manifest.
- Gemini CLI: `GEMINI.md` imports `@./AGENTS.md`. `.gemini/settings.example.json` sets a conservative baseline.
- Antigravity: `ANTIGRAVITY.md` imports `@AGENTS.md`. `.antigravity/rules/ai-builder.md` and `.antigravity/commands/ai-builder.md` expose the skill. `.antigravity/settings.example.json` enforces approvals.
- Codex CLI: native, no adapter.

## Practical Portability Rule

Do not duplicate the whole routing system across runtimes.

Instead:

1. keep the main routing logic in `AGENTS.md` and `SKILL.md`
2. add thin platform adapters that import or mirror the canonical files
3. keep platform-specific mechanics in `references/platforms/`

## What Each Runtime Is Best At Here

### Codex CLI

- repository-driven task routing
- validation-oriented coding workflows
- decomposable coding tasks

### Claude Code

- rich skill frontmatter with progressive disclosure
- path-scoped rules under `.claude/rules/`
- hooks for deterministic automation
- slash commands for reusable entry points

### Claude Web Skills

- zero-setup user experience on `claude.ai`
- progressive disclosure through linked files
- good fit when the user cannot run a CLI

### ChatGPT

- widest distribution surface (Custom GPTs, Projects, Apps SDK)
- no filesystem access: skill must be bundled into instructions plus knowledge
- starter prompts shape first-turn behavior

### Gemini CLI

- hierarchical context via `GEMINI.md`
- trusted-folder safety model
- explicit sandboxing and expansion flow

### Antigravity

- manager-agent orchestration with subagents
- first-class MCP integration
- workspace-trust approval flow
- Chrome and terminal automation surfaces

## Suggested Repo Convention

If you want one repo to work cleanly everywhere:

- `AGENTS.md` stays canonical
- `SKILL.md` is the skill-format twin for skill-aware surfaces
- `CLAUDE.md`, `GEMINI.md`, and `ANTIGRAVITY.md` are thin adapters that import `AGENTS.md`
- `agents/openai.yaml` plus `dist/chatgpt-custom-gpt.md` cover ChatGPT
- builder and risk references stay in `references/`
- platform-specific mechanics stay in `references/platforms/`

## Official References

- AGENTS.md standard: https://github.com/openai/agents.md
- Claude Code memory: https://code.claude.com/docs/en/memory
- Claude Code skills: https://code.claude.com/docs/en/skills
- Claude Skills (claude.ai): https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- Gemini CLI context files: https://geminicli.com/docs/cli/gemini-md/
- Gemini CLI trusted folders: https://geminicli.com/docs/cli/trusted-folders/
- OpenAI Apps SDK: https://platform.openai.com/docs/apps-sdk
- Antigravity: https://antigravity.google
