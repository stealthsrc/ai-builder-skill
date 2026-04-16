---
name: ai-builder
description: Route practical office, Windows automation, lightweight browser tools, business scripting, and security-hardening requests to the right implementation approach (VBA, PowerShell, Python, or plain HTML/CSS/JavaScript). Use when an AI agent needs to build, maintain, review, or harden Excel, Word, or Outlook macros, Windows file or system automation, HTML/CSS/JavaScript utilities, CSV or Excel report pipelines, or similar admin and no-code workflows where the implementation language should be chosen pragmatically and safely.
---

# AI Builder (Claude Code Skill)

This is the Claude Code native skill wrapper for the `ai-builder-skill` repository. It delegates to the canonical routing hub at the repository root.

## How To Use This Skill

When invoked:

1. Open `../../../SKILL.md` at the repository root for the full routing contract.
2. Open `../../../AGENTS.md` when precedence or multi-runtime context matters.
3. Load the matching builder from `../../../references/builders/`.
4. Load `../../../references/rules/security-baseline.md` when the task touches secrets, destructive file actions, email flows, external downloads, COM automation, or command execution.
5. Load `../../../references/rules/risk-trigger-matrix.md` when the risk signals are mixed or implicit.

Respond using the contract in `../../../references/rules/output-and-safety.md`.

## When Claude Should Invoke This Skill

- the user asks for Office automation, Windows scripting, a lightweight browser tool, a CSV or Excel pipeline, or a security-hardening pass
- the user mentions VBA, PowerShell, Python, or plain HTML/CSS/JavaScript for a business task
- the user asks for a "small script", a "little tool", a "quick automation", or a "one-off utility" in an office or Windows context

## When Claude Should Skip This Skill

- the user is building a full application with a framework (React, Django, Next, etc.)
- the user is doing infrastructure or devops work
- the task is purely conversational and does not produce code
