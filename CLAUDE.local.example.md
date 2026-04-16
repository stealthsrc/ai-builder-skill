# Claude Local Overlay Example

Copy this file to `CLAUDE.local.md` if you want personal or machine-specific Claude Code behavior that should not be committed.

Keep shared routing rules in `AGENTS.md`, `SKILL.md`, and `references/`.
Keep only local preferences here.

## Local Preferences

- Prefer concise final summaries unless I explicitly ask for deeper explanation.
- Reuse existing scripts, templates, and starter assets before creating new files.
- Run repository validation after edits when validation scripts already exist.
- Keep approvals explicit for pushes, package installs, downloads, and destructive operations.
- Do not read `.env`, private keys, certificates, or export files unless I explicitly ask.

## Repo Reminders

- Treat `SKILL.md` as the routing hub.
- Load only the builder, rule, or platform reference needed for the current task.
- Use `references/platforms/claude-code.md` when Claude-native behavior matters.
