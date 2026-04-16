---
description: Route a business automation request through the ai-builder skill hub.
argument-hint: "<describe the automation task>"
---

# /ai-builder

Route the user's request through the ai-builder skill hub.

## Procedure

1. Read `SKILL.md` at the repository root for the full routing contract.
2. Identify the actual business task before choosing a language.
3. Select the matching builder reference under `references/builders/`:
   - VBA for Office desktop macros
   - PowerShell for Windows-native automation
   - Python for data pipelines and portable scripting
   - HTML/CSS/JavaScript for lightweight browser tools
   - security-builder for hardening, audit, or risky flows
4. Load `references/rules/security-baseline.md` if the task has any risk signal (secrets, destructive file actions, email flows, external downloads, COM automation, command execution).
5. Load `references/rules/risk-trigger-matrix.md` when the risk signals are mixed or implicit.

## Response Shape

Use the contract in `references/rules/output-and-safety.md`:

- brief implementation plan
- complete executable code
- explicit run instructions
- quick validation method
- rollback guidance for destructive changes

## Arguments

User request: $ARGUMENTS
