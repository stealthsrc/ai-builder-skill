# Gemini Local Overlay Example

This file is an example personal overlay for Gemini CLI.

Gemini CLI does not automatically load a `GEMINI.local.md` file.
Use this template by either:

- copying the content into your global `~/.gemini/GEMINI.md`, or
- importing it from your global or project `GEMINI.md` with the normal `@file.md` syntax

Keep shared routing rules in `AGENTS.md`, `SKILL.md`, and `references/`.
Keep only local preferences here.

## Local Preferences

- Prefer sandboxed runs for unfamiliar or risky repositories.
- Keep the default approval mode conservative unless I explicitly relax it.
- Prefer trusted folders only after I review the repository.
- Reuse existing scripts, templates, and starter assets before creating new files.
- Do not read `.env`, private keys, certificates, or export files unless I explicitly ask.

## Repo Reminders

- Treat `SKILL.md` as the routing hub.
- Load only the builder, rule, or platform reference needed for the current task.
- Use `references/platforms/gemini-cli.md` when Gemini-specific settings, trust, or sandbox behavior matters.
