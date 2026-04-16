# Output And Safety

Apply these shared rules unless a more specific builder reference overrides them.

## Response Shape

- Start non-trivial answers with a brief implementation plan.
- State the chosen implementation approach and the selected builder or language.
- Name the expected inputs, outputs, key steps, and assumptions.
- Deliver complete executable code when code is requested.

## Execution Guidance

- Explain exactly where the code should be saved or pasted.
- Explain exactly how to run it.
- Mention prerequisites, versions, or dependency installation only when they matter.
- Tell the user what output or visible result to expect.

## Validation And Rollback

- Include a quick validation method.
- Call out likely edge cases or failure modes.
- Recommend testing on copies first when files, documents, folders, spreadsheets, or settings may change.
- Make rollback or backup guidance explicit when the script modifies data in place.

## Safety Baseline

- Prefer preview or dry-run behavior when practical.
- Preserve originals unless the user explicitly asks for in-place modification.
- Keep destructive behavior visible and intentional.
- Avoid unnecessary dependencies and over-engineering.
