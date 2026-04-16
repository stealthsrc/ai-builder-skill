# Antigravity

Use this reference when the repository should work well inside Google Antigravity, Google's agentic IDE, or when the user explicitly mentions Antigravity, `.antigravity/`, or Google's agent-manager workflow.

## Positioning

Antigravity reads `AGENTS.md` natively and supports an `.antigravity/` directory for project-scoped rules, commands, and settings. It also integrates with MCP and has a manager-agent model where one orchestrator can spawn worker agents.

For this repository, the cleanest pattern is:

1. keep `AGENTS.md` as the canonical source
2. add a minimal `ANTIGRAVITY.md` root adapter that imports `AGENTS.md`
3. mirror the routing hub into `.antigravity/rules/ai-builder.md`
4. expose a slash command through `.antigravity/commands/ai-builder.md`
5. ship a conservative workspace baseline in `.antigravity/settings.example.json`

## Recommended Repository Pattern

Use this layout so Antigravity picks up the skill without extra configuration:

```text
ANTIGRAVITY.md                       # thin adapter, imports AGENTS.md
.antigravity/
  rules/
    ai-builder.md                    # points to SKILL.md for routing
  commands/
    ai-builder.md                    # slash command /ai-builder
  settings.example.json              # conservative defaults
```

This mirrors the same pattern used for Claude Code (`.claude/`) and Gemini CLI (`.gemini/`).

## Where Antigravity Is Strong

- manager-agent orchestration with subagents
- first-class MCP integration
- project-scoped rules and commands
- trusted-workspace approval flow
- Chrome and terminal automation surfaces

## Practical Guidance For This Repo

- keep rules files thin and route through `SKILL.md` instead of duplicating logic
- keep slash commands declarative; put the actual procedure in `SKILL.md` and `references/builders/`
- keep `settings.example.json` conservative: require approval for destructive shell commands, network calls, and file writes outside the workspace
- do not rely on auto-approved tool calls for anything that touches secrets, credentials, external downloads, or bulk file changes
- use MCP only for resources the user has explicitly trusted

## Safety Posture

Antigravity runs agents with real computer-use surfaces. For this skill that means:

- recommend dry-run or preview for every destructive action
- surface risk flags from `references/rules/risk-trigger-matrix.md` before acting
- require explicit approval for `rm`, bulk renames, `Invoke-Expression`, outbound network calls, email sends, and COM automation
- prefer writing to new files over in-place edits

## Official References

- Antigravity product page: https://antigravity.google
- AGENTS.md open format (adopted by Antigravity): https://github.com/openai/agents.md
- MCP specification: https://modelcontextprotocol.io
