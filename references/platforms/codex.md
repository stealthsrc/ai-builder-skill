# Codex

Use this reference when the user is working in a Codex-style environment or wants the skill to behave well with a terminal-first coding agent that reads repository instructions.

## Positioning

For this repository, treat `AGENTS.md` as the canonical Codex-facing instruction layer.

This fits both the open `AGENTS.md` convention and the current Codex-style workflow used in this repository:

- keep one repo-level instruction file
- route from that file into `SKILL.md`
- then load only the builder and rule references that matter for the current task

## What Works Well In Codex

- concise repo instructions with clear precedence
- explicit task scoping
- visible validation steps
- reusable examples and starter assets
- deterministic scripts the agent can run instead of re-deriving everything from prose

Codex-oriented workflows tend to benefit from:

- tasks with a concrete output shape
- tasks that name constraints early
- requests that include a verification target
- supporting files that keep the root instruction file small

## Recommended Repository Pattern

For this repo, the strongest Codex pattern is:

1. keep `AGENTS.md` as the repo entrypoint
2. route through `SKILL.md`
3. load the builder reference that matches the execution environment
4. load the security baseline when the workflow has risk signals
5. validate with scripts, fixtures, or examples when possible

## How To Shape Work For Codex

When a request is ambiguous, push it toward:

- a clear goal
- explicit inputs
- explicit outputs
- a named runtime or host environment when known
- a validation method

Good examples:

```text
Use $ai-builder to choose the smallest viable implementation for this request. Inputs are CSV exports and the output should open cleanly in Excel.
```

```text
Use $ai-builder to harden this PowerShell script before it renames production files.
```

## Advice For This Repository

- prefer `AGENTS.md` over duplicating Codex-specific behavior across many files
- keep platform-specific notes in `references/platforms/`
- keep examples runnable
- use eval fixtures to verify routing decisions, not just code syntax
- do not bury critical safety rules only in long prose sections

## What To Emphasize In Future Codex Additions

- more eval cases for ambiguous routing
- more starter templates that Codex can copy and adapt
- more concrete examples where the same business request maps to different builders

## Official References

- AGENTS.md open format: https://github.com/openai/agents.md
- OpenAI Codex repository: https://github.com/openai/codex
- OpenAI Codex use cases: https://developers.openai.com/codex/explore/
- OpenAI Codex models: https://developers.openai.com/api/docs/models/gpt-5.3-codex
