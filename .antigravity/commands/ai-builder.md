---
name: ai-builder
description: Route a business automation request to the right implementation (VBA, PowerShell, Python, or HTML/CSS/JS) using the ai-builder skill hub.
---

# /ai-builder

Invoke this command when the user has a practical automation request and you want the agent to route through `SKILL.md` before writing any code.

## Procedure

1. Read `SKILL.md` at the repository root.
2. Apply the routing logic to select the correct builder reference.
3. Load the matching file under `references/builders/`.
4. If the task has any risk signal (secrets, destructive file ops, email sends, external downloads, command execution, COM automation, untrusted input), also load `references/rules/security-baseline.md` and `references/builders/security-builder.md`.
5. Produce the response using the contract in `references/rules/output-and-safety.md`.

## Response Shape

- brief implementation plan
- complete executable code
- explicit run instructions
- quick validation method
- rollback guidance when destructive
