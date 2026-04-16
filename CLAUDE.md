@AGENTS.md

## Claude Code

Use `SKILL.md` as the canonical routing hub for this repository.

- Load only the references needed for the current task.
- Prefer files under `references/builders/` for implementation guidance.
- Load `references/rules/security-baseline.md` for risky automation, secrets, destructive file actions, email flows, or external content.
- Load `references/platforms/claude-code.md` when Claude-specific behavior, memory, rules, skills, or settings matter.
- Keep Claude-specific instructions thin here and keep shared routing logic in `AGENTS.md` and `SKILL.md`.

## Working Style

- Prefer the smallest viable implementation that fits the user's environment.
- Explain where code goes, how to run it, and how to validate it.
- Recommend testing on copies first when files, spreadsheets, or system settings may change.
