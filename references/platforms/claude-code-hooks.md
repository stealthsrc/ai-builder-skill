# Claude Code Hooks

Use this reference when you want deterministic enforcement in Claude Code rather than relying on prompt adherence alone.

## When To Use Hooks

Use hooks when a step must always happen:

- format files after edits
- block writes to protected files
- force review on risky commands
- notify the user when Claude needs attention
- audit configuration or permission changes

Use skills when you want reusable workflows.
Use hooks when you want deterministic control.

## Hook Events Worth Caring About

The most useful events for this repository are:

- `PreToolUse`
- `PostToolUse`
- `PermissionRequest`
- `SessionStart`
- `Notification`

## Recommended Patterns For This Repo

### 1. Force review on destructive shell commands

Use a `PreToolUse` hook to force an approval step or add context before:

- `rm`
- deploy commands
- force pushes
- bulk rename scripts

### 2. Auto-format browser example files

Use a `PostToolUse` hook after `Edit|Write` to run formatting on:

- `*.html`
- `*.css`
- `*.js`

### 3. Protect secret-bearing files

Use a `PreToolUse` hook or deny rules to guard:

- `.env`
- `secrets/**`
- credential files

## Example Shared Project Hook

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "echo '{\"decision\":\"ask\",\"reason\":\"Destructive command requires explicit confirmation.\"}'"
          }
        ]
      }
    ]
  }
}
```

## Example Format Hook

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs -I {} sh -c 'case \"$1\" in *.html|*.css|*.js) echo formatted \"$1\" ;; esac' -- {}"
          }
        ]
      }
    ]
  }
}
```

## Important Design Rule

Do not push business logic into hooks.

Hooks should enforce policy, validation, or automation boundaries. The skill itself should still own routing and implementation guidance.

## Official References

- Claude Code hooks guide: https://code.claude.com/docs/en/hooks-guide
- Claude Code hooks reference: https://code.claude.com/docs/en/hooks
- Claude Code settings: https://code.claude.com/docs/en/settings
