---
name: ai-builder
description: Route practical office, Windows automation, lightweight browser tools, business scripting, and security-hardening requests to the right implementation approach. Use when Codex needs to build, maintain, review, or harden Excel, Word, or Outlook macros, Windows file or system automation, HTML/CSS/JavaScript utilities, CSV or Excel report pipelines, or similar admin and no-code workflows where VBA, PowerShell, Python, or plain web stack should be chosen pragmatically and safely.
---

# AI Builder

Use this skill as a hub for business automation requests that need a practical implementation, not architecture work.

## Start Here

- Read the user request and identify the actual business task before choosing a language.
- Read [references/rules/output-and-safety.md](references/rules/output-and-safety.md) for the shared response and safety baseline.
- If the request touches credentials, secrets, external downloads, command execution, file deletion, COM automation, email, or asks for an audit or hardening pass, also read [references/rules/security-baseline.md](references/rules/security-baseline.md).
- If the request includes multiple risk signals or the blast radius is unclear, also read [references/rules/risk-trigger-matrix.md](references/rules/risk-trigger-matrix.md).
- For office-heavy, admin, or no-code requests, read [references/builders/office-script-builder.md](references/builders/office-script-builder.md) first.
- For lightweight browser-based tools, static dashboards, forms, or no-framework frontend requests, read [references/builders/html-css-javascript-builder.md](references/builders/html-css-javascript-builder.md).
- For security reviews or risky automation flows, read [references/builders/security-builder.md](references/builders/security-builder.md) before the language-specific builder.
- For explicit language requests, jump directly to the matching builder reference.
- Load only the references that materially improve the answer.

## Route The Request

- Use [references/builders/vba-builder.md](references/builders/vba-builder.md) for Office desktop macros, worksheet logic, workbook events, buttons, forms, and existing macro maintenance.
- Use [references/builders/powershell-builder.md](references/builders/powershell-builder.md) for Windows-native automation, file and folder operations, COM automation, scheduled tasks, and operational scripting.
- Use [references/builders/python-builder.md](references/builders/python-builder.md) for data processing, CSV or Excel transformations, PDF or API workflows, reporting, ETL, and automation that benefits from portability or maintainability.
- Use [references/builders/html-css-javascript-builder.md](references/builders/html-css-javascript-builder.md) for lightweight browser tools, static internal utilities, landing pages, forms, dashboards, and no-framework frontend work that should stay portable and easy to hand off.
- Use [references/builders/security-builder.md](references/builders/security-builder.md) when the task is to review, harden, or make safer an automation, or when the implementation will handle secrets, external content, or high-impact actions.
- If the request is ambiguous, choose the smallest viable implementation, state the chosen language briefly, and keep assumptions explicit.

## Build The Answer

- Prefer executable code over pseudo-code when the user asks for implementation.
- Optimize for low setup burden and direct copy-paste use when the user appears non-technical.
- Preserve original files unless the user explicitly asks for in-place edits.
- Prefer writing a new output file when the workflow modifies documents, spreadsheets, folders, or reports.
- Default to the safer implementation when two options solve the same task with similar effort.
- Keep configuration visible and minimal.
- Add short comments only where they improve readability.

## Response Contract

- Start non-trivial answers with a brief implementation plan.
- Deliver complete code when code is requested.
- Explain exactly where the code goes and how to run it.
- Include a quick validation method, likely edge cases, and rollback guidance when changes are destructive.

## Reference Notes

- Use files under `references/builders/` for language-specific implementation behavior.
- Use files under `references/rules/` for shared conventions.
- Treat `references/rules/security-baseline.md` as the shared guardrail for secrets, dangerous language patterns, network use, and file safety.
- Use `references/rules/risk-trigger-matrix.md` when the risk is implicit or spans multiple categories.
- Use files under `references/templates/` only when extending this repository with new builders or derived documentation.
