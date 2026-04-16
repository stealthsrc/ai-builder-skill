# Prompt Cookbook

Use these patterns when invoking the skill so routing stays predictable and the output shape stays useful.

---

## Good Prompt Patterns

### 1. Explicit language

```text
Use VBA to clean this workbook and highlight duplicate invoice IDs.
```

Why it works:

- the builder is unambiguous
- the expected runtime is obvious
- the response can jump straight to implementation

### 2. Explicit environment

```text
Use PowerShell on Windows to rename all PDFs in this folder based on the date in the filename.
```

Why it works:

- the operating environment is clear
- the script can be written with the right safety defaults

### 3. Explicit frontend scope

```text
Build a plain HTML/CSS/JavaScript internal dashboard, no framework, mobile-friendly.
```

Why it works:

- the toolchain is constrained
- the UI expectations are clear

### 4. Explicit hardening request

```text
Review this PowerShell script for dangerous patterns and harden it before it touches production files.
```

Why it works:

- the security layer should trigger immediately
- the response can prioritize risk, not just syntax

---

## When To Let Routing Decide

Use a high-level prompt when the task is clear but the best language is not:

```text
Automate this weekly finance reporting workflow. Inputs are CSV exports and the output should open cleanly in Excel.
```

This gives the skill enough signal to choose Python without forcing it.

---

## When To Force A Safer Answer

If the task touches secrets, file deletion, email sends, or external downloads, say so directly:

```text
Make this safer. It handles API keys and renames production files.
```

```text
Before writing code, identify the risk points and use the safest practical implementation.
```

---

## Weak Prompt Patterns To Avoid

### Too vague

```text
Automate this for me.
```

Problem:

- no environment
- no input/output shape
- no signal for builder selection

### Tool conflict

```text
Use Python but keep it inside Excel as a workbook macro.
```

Problem:

- runtime and host model conflict
- likely forces an unnatural solution

### Missing risk context

```text
Fix this script quickly.
```

Problem:

- if the script sends emails, deletes files, or uses secrets, the assistant may not know to load the security layer early

---

## Recommended Add-Ons

Append one of these lines when helpful:

- `Use the smallest viable implementation.`
- `Keep setup minimal for a non-technical user.`
- `Write to a new output file rather than editing in place.`
- `Assume the input may be messy or untrusted.`
- `Add a quick validation step.`

---

## Trigger Cheatsheet

| If you want... | Say... |
|---|---|
| VBA | `Use VBA` |
| PowerShell | `Use PowerShell on Windows` |
| Python | `Use Python` |
| Plain browser tool | `Use plain HTML/CSS/JavaScript, no framework` |
| Security-first output | `Harden this` or `Make this safer first` |
