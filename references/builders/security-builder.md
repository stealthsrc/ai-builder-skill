# Security Builder

Use this reference when the user asks to secure, harden, audit, review, or make safer an automation or script.

Use it also when the task touches any of these risk points:

- secrets, credentials, API keys, tokens, or signed URLs
- file deletion, overwrite, or bulk rename or move
- external downloads, web requests, or webhook handling
- command execution, shell calls, COM automation, or scheduled tasks
- email, attachments, exports, logs, or PII
- AI assistants, no-code connectors, agent permissions, or copied untrusted content

## Security Workflow

1. Identify what the automation can read, write, execute, or disclose.
2. Minimize blast radius with least privilege, dry-run behavior, bounded paths, and new output files by default.
3. Remove dangerous language-specific patterns before adding features.
4. Keep secrets out of code, prompts, examples, and Git history.
5. Explain validation, rollback, and likely failure modes clearly.

## Load The Right Companion References

- Read [../rules/security-baseline.md](../rules/security-baseline.md) for shared guardrails.
- Pair with `vba-builder.md` for Office macros.
- Pair with `powershell-builder.md` for Windows-native automation and COM.
- Pair with `python-builder.md` for scripts that process files, APIs, or structured data.

## Default Security Decisions

- Prefer a new output file over in-place edits unless the user explicitly requests otherwise.
- Prefer argumentized command calls over string-built shell commands.
- Prefer HTTPS with certificate validation intact.
- Prefer allowlists and path-bound checks when working with filenames, folders, sheet names, or user-provided values.
- Prefer environment variables, vaults, or secret stores over hardcoded credentials.
- Prefer human confirmation for high-impact actions such as delete, deploy, force-push, or broad external writes.

## What To Deliver

- Call out the main risk areas in one short block near the start.
- Build the smallest viable secure implementation, not the most elaborate one.
- Include the exact place to save the code, how to run it, and how to test it safely on non-production inputs first.
