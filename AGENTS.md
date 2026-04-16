# AGENTS.md

This repository uses a **root skill orchestration model**.

The canonical entry point for task specialization is the root `SKILL.md` file.
Supporting instructions, builders, routing notes, templates, and specialized references live under `references/`.

This file defines how Codex should interpret that structure and apply it consistently.

---

## 1. Repository model

The repository is organized around a central skill document.

Expected structure:

- `SKILL.md` -> main skill hub and canonical high-level instruction source
- `references/builders/` -> specialized builder references such as `html-css-javascript-builder.md`, `vba-builder.md`, `powershell-builder.md`, `python-builder.md`
- `references/rules/` -> routing rules, output rules, and shared conventions
- `references/rules/` may also include risk classification aids such as trigger matrices
- `references/templates/` -> reusable templates for future builders or derived skills

Codex should treat this repository as a **hub-and-references architecture**, not as a multi-folder native skill library.

---

## 2. Canonical source priority

When working in this repository, follow this order of precedence:

1. The user's explicit request
2. The root `SKILL.md`
3. The most relevant file under `references/builders/`
4. The most relevant file under `references/rules/`
5. General repository conventions
6. Default model behavior

If there is any conflict, prefer the most specific instruction that still fits the user's request safely and clearly.

---

## 3. Default operating procedure

Before generating code, plans, implementation steps, or refactors:

1. Read the user's request and identify the main goal.
2. Use the root `SKILL.md` as the primary routing and behavior guide.
3. Determine whether a specialized reference under `references/builders/` should be applied.
4. Apply any shared constraints from `references/rules/` when relevant.
5. Produce the smallest viable solution that is executable, maintainable, and adapted to the user's technical level.

Do not assume that every reference file is equally important.
Use only the references that materially improve the result.

---

## 4. Routing policy

### 4.1 Root routing behavior

The root `SKILL.md` is the primary hub.
Codex should use it to understand:

- the overall purpose of the repository
- how builder references are organized
- when to select a specialized builder
- what response structure is expected

If `SKILL.md` indicates that a request should map to a builder reference, apply that reference as the specialized instruction layer.

### 4.2 Builder reference selection

Look under `references/builders/` for the best match.

Common examples:

- `references/builders/office-script-builder.md`
- `references/builders/html-css-javascript-builder.md`
- `references/builders/vba-builder.md`
- `references/builders/powershell-builder.md`
- `references/builders/python-builder.md`

Use the most relevant builder based on the request context.

### 4.3 Office and no-code requests

For users who mainly work in no-code, office, or administrative workflows:

1. Consult the root `SKILL.md` first.
2. Prefer `references/builders/office-script-builder.md` as the first specialized reference.
3. Then select the most suitable implementation reference:
   - `html-css-javascript-builder.md`
   - `vba-builder.md`
   - `powershell-builder.md`
   - `python-builder.md`

Use:

- **HTML/CSS/JavaScript** for lightweight browser-based tools, static internal dashboards, forms, calculators, microsites, and no-framework frontends that should stay easy to run and hand off
- **VBA** for Office desktop macros, workbook logic, worksheet events, buttons, forms, and existing macro maintenance
- **PowerShell** for Windows-native automation, file and folder operations, COM automation, system scripting, and admin-heavy workflows
- **Python** for data processing, CSV/Excel/PDF/API workflows, reporting, ETL, and broader automation that benefits from portability or maintainability

### 4.4 Explicit language requests

If the user explicitly names a language or tool, prefer the matching builder reference.

Examples:

- "build this in HTML/CSS/JavaScript" -> `references/builders/html-css-javascript-builder.md`
- "write this in VBA" -> `references/builders/vba-builder.md`
- "use PowerShell" -> `references/builders/powershell-builder.md`
- "build this in Python" -> `references/builders/python-builder.md`

### 4.5 Ambiguous requests

If the user does not specify a language:

- infer the best implementation from the environment, setup burden, maintainability, and user skill level
- state the chosen language briefly
- keep assumptions minimal and explicit

Prefer:

- HTML/CSS/JavaScript when the workflow is best delivered as a lightweight browser-based tool without backend complexity
- VBA when the workflow belongs inside Office desktop
- PowerShell when the workflow is Windows-native and operational
- Python when the workflow spans multiple file types, data transformations, or maintainability needs

---

## 5. Audience adaptation

Assume many users are not full-time developers.
Generated outputs must be practical for people who mainly operate through office tools, scripting, or light automation.

When the user appears non-technical:

- minimize setup complexity
- avoid unnecessary dependencies
- prefer direct and copy-paste-ready solutions
- explain exactly where the code goes
- explain exactly how to run it
- explain how to validate the result
- explain rollback or backup precautions when relevant

When the user appears more technical:

- keep explanations concise but complete
- preserve clarity, safety, and maintainability

---

## 6. Required response structure

For any non-trivial request, use this structure unless the root `SKILL.md` or a more specific builder reference overrides it.

### 6.1 Brief implementation plan

Start with a short plan that states:

- selected implementation approach
- chosen builder reference or language
- expected inputs and outputs
- major steps
- key assumptions or risks

### 6.2 Deliver the implementation

Then provide:

- complete executable code when code was requested
- comments where useful
- minimal configuration points
- sane defaults

### 6.3 Explain execution

Always explain:

- where to save or paste the code
- how to run it
- prerequisites and versions if relevant
- dependency installation if relevant
- what output to expect

### 6.4 Validation and safety

Always include:

- a quick validation method
- likely edge cases or failure modes
- backup or rollback guidance when the script changes files, documents, folders, or settings

---

## 7. Output quality baseline

Unless a more specific reference says otherwise, outputs should be:

- readable
- minimal
- executable
- well-structured
- adapted to the target environment
- safe for the expected usage
- explicit about assumptions

Prefer:

- clear names
- short procedures or functions
- visible configuration blocks
- simple status messages or logging
- checks before destructive actions

Avoid:

- unnecessary complexity
- hidden side effects
- over-engineering
- pseudo-code when real code is expected
- placeholders unless clearly marked

---

## 8. Safety rules

Before generating code that may modify files, systems, documents, spreadsheets, email data, or settings:

- identify what will change
- warn about destructive behavior
- recommend testing on copies first
- prefer preview or dry-run behavior when practical
- make overwrite behavior explicit

For office and business workflows:

- preserve original files unless in-place changes are explicitly requested
- prefer writing to a new file when feasible
- make risk points operationally obvious

For scripts that may require elevated privileges:

- state that permissions may be required
- do not assume admin access

---

## 9. Reference usage rules

Files under `references/` are supporting instruction modules.
Use them intentionally.

### 9.1 `references/builders/`

Use these for language or implementation-specific behavior.
They should influence:

- code style choices
- environment assumptions
- safety checks
- validation guidance
- language-specific execution steps

### 9.2 `references/rules/`

Use these for shared conventions such as:

- routing behavior
- output format
- naming conventions
- project-wide quality rules

### 9.3 `references/templates/`

Use these only when creating new builders, new references, or new derived documentation.
Do not treat templates as the primary instruction source for an end-user request.

---

## 10. Preferred philosophy

Default to the **smallest viable implementation** that:

- solves the actual request
- is realistic for the user to run
- is easy to explain
- is easy to maintain
- does not introduce unnecessary dependencies or architecture

For no-code or office-heavy users, optimize for:

- fewer steps
- lower setup burden
- lower operational risk
- easier handoff
- easier debugging

---

## 11. Practical routing examples

- User wants an Excel macro for cleaning rows and formatting sheets -> use root `SKILL.md`, then likely `references/builders/office-script-builder.md` and `references/builders/vba-builder.md`
- User wants to rename many files on Windows -> use root `SKILL.md`, then likely `references/builders/office-script-builder.md` and `references/builders/powershell-builder.md`
- User wants to merge CSV files and export an Excel report -> use root `SKILL.md`, then likely `references/builders/office-script-builder.md` and `references/builders/python-builder.md`
- User wants a lightweight internal dashboard or browser tool without a framework -> use root `SKILL.md`, then likely `references/builders/html-css-javascript-builder.md`
- User explicitly asks for Python even for an Office workflow -> prefer `references/builders/python-builder.md`
- User explicitly asks to fix an existing Excel macro -> prefer `references/builders/vba-builder.md`

---

## 12. What this file should not do

This file should not duplicate the full content of the root `SKILL.md` or all builder references.
Its role is to define:

- how Codex should interpret the repository structure
- how to route through the root `SKILL.md`
- how to select supporting references
- what response quality and safety baseline to maintain

Detailed builder behavior belongs in the relevant files under `references/`.

---

## 13. Initial reference priority

Until the reference library expands, prioritize these files when present:

1. `SKILL.md`
2. `references/builders/office-script-builder.md`
3. `references/builders/html-css-javascript-builder.md`
4. `references/builders/vba-builder.md`
5. `references/builders/powershell-builder.md`
6. `references/builders/python-builder.md`

Then use any other relevant reference under `references/` that better matches the task.
