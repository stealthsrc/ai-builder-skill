# Concrete Use Cases

This repository is most useful when a request is practical, execution-oriented, and tied to a real operating environment.

The examples below show how AI Builder should route work and what a good outcome looks like.

---

## 1. Excel Cleanup Macro

**Prompt**

```text
Clean this workbook, remove blank rows, trim invoice IDs, and highlight duplicates.
```

**Primary builder**

- `references/builders/office-script-builder.md`
- `references/builders/vba-builder.md`

**Expected result**

- a VBA macro for Excel desktop
- explicit instructions for where to paste the code
- validation steps on a copy of the workbook
- clear notes on which sheet or columns will be modified

**Why this route**

The work belongs inside Excel and should stay easy for a non-developer to run again.

---

## 2. Windows File Renaming Utility

**Prompt**

```text
Rename every PDF in this folder using the date already present in the filename.
```

**Primary builder**

- `references/builders/office-script-builder.md`
- `references/builders/powershell-builder.md`
- `references/rules/security-baseline.md`

**Expected result**

- a PowerShell script with a visible path configuration block
- dry-run or preview behavior before any rename
- path-bounded file handling
- rollback guidance if the pattern was wrong

**Why this route**

This is Windows-native filesystem work and should not require extra runtime dependencies.

---

## 3. CSV Merge And Report Export

**Prompt**

```text
Merge these monthly CSV exports and generate a simple Excel report with totals by region.
```

**Primary builder**

- `references/builders/office-script-builder.md`
- `references/builders/python-builder.md`

**Expected result**

- a Python script that reads multiple CSV files
- one clean output workbook or report file
- visible input and output paths
- a quick validation method such as row counts or grouped totals

**Why this route**

This is structured data work across multiple files, which is easier to maintain in Python than in VBA or PowerShell.

---

## 4. Lightweight Browser Dashboard

**Prompt**

```text
Build a small HTML/CSS/JavaScript dashboard to track weekly sales KPIs for an internal team.
```

**Primary builder**

- `references/builders/html-css-javascript-builder.md`

**Expected result**

- plain `index.html`, `styles.css`, and `script.js`
- a responsive layout that works on desktop and mobile
- a UI that feels intentional rather than boilerplate
- no framework unless explicitly requested

**Why this route**

The task is best delivered as a lightweight browser tool with low setup cost and easy handoff.

---

## 5. Macro Hardening Before Email Sends

**Prompt**

```text
Fix this existing VBA macro and make it safer before it sends Outlook emails.
```

**Primary builder**

- `references/builders/security-builder.md`
- `references/builders/vba-builder.md`
- `references/rules/security-baseline.md`

**Expected result**

- a safer macro flow
- clear explanation of what data is used in the email
- validation of cell values before they reach message fields
- warnings about destructive or irreversible send actions

**Why this route**

The script touches Office automation and outbound communication, which increases operational risk.

---

## 6. PowerShell Script Security Review

**Prompt**

```text
Review this PowerShell script for dangerous patterns and harden it.
```

**Primary builder**

- `references/builders/security-builder.md`
- `references/builders/powershell-builder.md`
- `references/rules/security-baseline.md`

**Expected result**

- removal of unsafe patterns like `Invoke-Expression` or string-built commands
- explicit argument passing
- better path validation
- safer handling of downloads, certificates, and secrets

**Why this route**

The request is explicitly about hardening and should be led by the security layer first.

---

## 7. Internal Admin Tool With A Browser UI

**Prompt**

```text
Create a browser-based form where staff can paste client rows and export a cleaned CSV.
```

**Primary builder**

- `references/builders/html-css-javascript-builder.md`
- `references/rules/security-baseline.md`

**Expected result**

- a local or static browser tool
- client-side validation and clear error states
- safe handling of pasted content
- no unnecessary backend if the workflow can stay local

**Why this route**

The workflow benefits from a lightweight frontend but still needs input safety and operational clarity.

---

## 8. Ambiguous Request That Needs Routing

**Prompt**

```text
Automate this weekly finance reporting task for me.
```

**Expected routing behavior**

- inspect the actual inputs and outputs first
- choose VBA if the work lives inside an existing workbook
- choose PowerShell if the task is mostly Windows file and Office automation
- choose Python if the task spans multiple exports, transformations, or report formats
- load the security baseline if the workflow touches credentials, email, or file overwrites

**Why this matters**

The core job of this skill is not just generating code. It is choosing the right implementation path before code is written.
