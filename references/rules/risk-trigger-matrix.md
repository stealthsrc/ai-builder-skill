# Risk Trigger Matrix

Use this matrix when a request looks operationally simple but still carries hidden risk.

| Trigger in the request | Extra reference to load | Main concern |
|---|---|---|
| API key, token, credential, secret, signed URL | `references/rules/security-baseline.md` | secret exposure, unsafe storage, prompt leakage |
| Delete, overwrite, rename, move, bulk update | `references/rules/security-baseline.md` | destructive file operations, rollback, preview mode |
| Download, fetch, webhook, external URL | `references/rules/security-baseline.md` | untrusted input, TLS, integrity, SSRF-style mistakes |
| Shell command, process launch, COM automation | `references/builders/security-builder.md` | injection, unsafe execution, over-privileged actions |
| Outlook email, attachment, export, report delivery | `references/builders/security-builder.md` | sensitive content, irreversible send actions, data leakage |
| Browser tool with user-entered content | `references/builders/html-css-javascript-builder.md` and `references/rules/security-baseline.md` | input validation, unsafe DOM updates, accidental secret exposure |
| Existing VBA macro that already uses `Shell`, `XMLHTTP`, `ADODB.Stream`, or Outlook | `references/builders/vba-builder.md` and `references/builders/security-builder.md` | endpoint and macro abuse patterns |
| PowerShell script with `Invoke-Expression`, `cmd /c`, or download-and-run flow | `references/builders/powershell-builder.md` and `references/builders/security-builder.md` | code execution, certificate bypass, unsafe downloads |
| Python script with `shell=True`, `eval`, `exec`, `pickle`, or broad path writes | `references/builders/python-builder.md` and `references/builders/security-builder.md` | injection, deserialization, path traversal |
| Ambiguous automation touching production-like data | `references/builders/security-builder.md` | blast radius, safer defaults, explicit validation |

## Default Rule

If the cost of loading the security baseline is low and the downside of skipping it is high, load it.
