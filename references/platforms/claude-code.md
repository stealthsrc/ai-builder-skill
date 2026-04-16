# Claude Code

Use this reference when the repository should work well in Claude Code or when the user explicitly mentions Claude, Claude Code, or `CLAUDE.md`.

## Most Important Difference From Codex

Claude Code reads `CLAUDE.md`, not `AGENTS.md`.

The official Claude Code guidance explicitly recommends creating a `CLAUDE.md` that imports `AGENTS.md` when a repository already uses `AGENTS.md` for other coding agents.

## Recommended Pattern For This Repository

For Claude Code, the cleanest adaptation is:

1. create a project `CLAUDE.md`
2. import `@AGENTS.md`
3. add Claude-specific notes only when needed
4. keep route logic in `SKILL.md`
5. keep scoped instructions in separate rule or skill files

Example:

```md
@AGENTS.md

## Claude Code

Prefer the builder references in references/builders/ and load the security baseline when risky automation is involved.
```

## Where Claude Code Is Strong

- project memory through `CLAUDE.md`
- path-scoped rules in `.claude/rules/`
- skills with frontmatter and supporting files
- hooks for deterministic automation and policy checks
- local and shared settings layers

## Practical Guidance

- keep `CLAUDE.md` concise and specific
- move larger procedures into skills or rules
- use rules when guidance should only apply to certain files or directories
- use skills when the behavior is an actual reusable workflow
- use hooks when something must happen deterministically, not optionally

## Memory Model To Keep In Mind

Claude Code distinguishes between:

- `CLAUDE.md` files written by the user or team
- auto memory written by Claude itself

For this repo:

- put stable routing rules in `AGENTS.md` and imported `CLAUDE.md`
- do not rely on auto memory for repository-critical behavior

## How To Package This Repo For Claude Code

- a top-level `CLAUDE.md` that imports `AGENTS.md`
- a project `.claude/settings.json` copied from `.claude/settings.example.json` when you want a safe shared baseline
- a personal `CLAUDE.local.md` copied from `CLAUDE.local.example.md` when you want local-only overrides
- optional `.claude/rules/` files for path-specific behavior
- optional `.claude/skills/` wrappers if you want Claude-native slash-invocable workflows

## Official References

- Claude Code memory and `CLAUDE.md`: https://code.claude.com/docs/en/memory
- Claude Code skills: https://code.claude.com/docs/en/skills
- Claude Code settings: https://code.claude.com/docs/en/settings
- Claude Code commands: https://code.claude.com/docs/en/commands
