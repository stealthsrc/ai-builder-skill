# Codex Task Shaping

Use this reference when you want prompts and tasks to produce better outcomes in Codex-style coding agents.

## Core Rule

Do not ask for "automation" in the abstract when you already know the operating environment.

Instead, shape the task so the agent can choose the right builder quickly and verify the result.

## Preferred Task Template

Use this structure when the task matters:

```text
Goal:
Inputs:
Outputs:
Environment:
Constraints:
Validation:
Risk notes:
```

Example:

```text
Goal: Clean an Excel workbook and highlight duplicate invoice IDs.
Inputs: Existing macro-enabled workbook with an Invoices sheet.
Outputs: Working macro and clear run instructions.
Environment: Excel desktop on Windows.
Constraints: Keep setup minimal for a non-technical user.
Validation: Explain how to test on a copy first.
Risk notes: Avoid in-place destructive changes where possible.
```

## Good Prompt Patterns

### Builder-directed

```text
Use $ai-builder and prefer VBA because this must run inside Excel desktop.
```

### Route-first

```text
Use $ai-builder to choose the smallest viable implementation. The inputs are CSV exports and the output should be reusable next month.
```

### Security-first

```text
Use $ai-builder to harden this script before it touches production files or credentials.
```

## Weak Prompt Patterns

### Too vague

```text
Automate this for me.
```

Problem:

- no environment
- no execution target
- no validation criteria

### Overconstrained in the wrong way

```text
Use Python but keep it as an Excel workbook macro.
```

Problem:

- mismatched runtime assumptions
- forces the wrong tool for the host

### Missing risk context

```text
Fix this quickly.
```

Problem:

- the agent may not know it sends emails, deletes files, or handles secrets

## What To Include When Risk Exists

If the task touches sensitive or high-impact behavior, name it explicitly:

- credentials
- file deletion or rename
- external downloads
- COM automation
- Outlook sends
- browser tools with pasted user data

Example:

```text
Use $ai-builder to review this macro. It sends Outlook emails and reads cell values that may contain client data.
```

## What To Ask For At The End

High-quality Codex tasks usually ask for one of:

- a working implementation
- a safer implementation
- a routing decision with justification
- a validation path
- a summary of risks and assumptions

## Official References

- OpenAI Codex use cases: https://developers.openai.com/codex/use-cases?category=automation&category=engineering&task_type=analysis&task_type=code&team=engineering&team=operations
- OpenAI Codex models: https://developers.openai.com/api/docs/models/gpt-5.3-codex
- OpenAI Codex repository: https://github.com/openai/codex
