# Claude Web Skills (claude.ai)

Use this reference when the skill is uploaded to claude.ai as a Skill bundle rather than used inside Claude Code (terminal) or via the API.

## What Claude Web Skills Expect

A Skill is a folder bundled as a `.zip` archive containing:

- `SKILL.md` at the root with YAML frontmatter that includes `name` and `description`
- any supporting files referenced from `SKILL.md` (references, scripts, examples)

Progressive disclosure model:

- Claude first reads only `SKILL.md` frontmatter and body
- it opens additional files on demand when the body links to them
- keep `SKILL.md` short so the first read stays useful
- keep support files specific and linked from `SKILL.md`

## Frontmatter Limits To Respect

- `name` must be short and must match `^[a-z0-9-]+$`
- `description` should be kept under about 1024 characters so it fits claude.ai's metadata pipeline
- the whole `SKILL.md` should stay small, ideally under a few KB, to leave room in context for support files

The repository's `scripts/validate_repo.py` now enforces the name and description sanity checks.

## How To Build The Bundle

This repository ships a bundler. From the repo root:

```bash
python scripts/build_skill_bundle.py
```

This produces `dist/ai-builder.zip` containing:

- `SKILL.md`
- `AGENTS.md`
- `references/` (builders, rules, platforms, templates)
- `examples/` (curated runnable examples)
- `assets/starters/` (starter kits)

The bundler excludes local overlays, git metadata, `dist/`, and CI files so the archive stays focused.

## How To Upload

1. Open `claude.ai` → Skills.
2. Create a new skill and upload `dist/ai-builder.zip`.
3. Enable the skill on conversations where business automation routing is useful.

## What Does Not Work On Claude Web

Claude Web skills do not have:

- filesystem write access
- shell execution
- background hooks

That means any guidance in this repository that assumes Claude Code hooks, CLI execution, or on-disk state does not apply on the web. Treat Claude Web as a routing and code-generation surface, not an execution surface.

When a workflow truly needs execution, suggest that the user switch to Claude Code, Gemini CLI, Codex CLI, or Antigravity for the same skill.

## Safety Posture

- never claim a command was executed; Claude Web cannot execute
- always mark destructive instructions as "run this locally" with explicit backup guidance
- keep the first turn's output copy-paste-ready so the user can run it themselves

## Official References

- Claude Skills documentation: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- Claude Skills authoring guide: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/getting-started
