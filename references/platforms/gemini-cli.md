# Gemini CLI

Use this reference when the repository should work well in Gemini CLI or when the user mentions Gemini CLI, `GEMINI.md`, or Google’s terminal agent workflow.

## Key Model For This Repository

Gemini CLI is built around:

- `GEMINI.md` context files
- `/memory` commands
- `settings.json`
- trusted folders
- sandboxing
- custom commands and MCP integrations

## Best Adaptation Pattern For This Repo

Gemini CLI can be aligned with this repository in two practical ways:

### Option 1. Use `GEMINI.md` and import or mirror repo guidance

Keep a project `GEMINI.md` that points at the repo’s main instructions.

### Option 2. Configure Gemini CLI to also read `AGENTS.md`

Gemini CLI supports `context.fileName` in `settings.json`, which can include multiple accepted context filenames such as:

```json
{
  "context": {
    "fileName": ["AGENTS.md", "CONTEXT.md", "GEMINI.md"]
  }
}
```

For this repository, this is the most direct bridge if you want to preserve `AGENTS.md` as the canonical source.

## What Matters Most In Gemini CLI

### Context

Gemini CLI uses hierarchical context loaded from `GEMINI.md` files and lets users inspect or refresh it with `/memory`.

Useful commands:

- `/memory show`
- `/memory list`
- `/memory refresh`

### Approval modes

Gemini CLI settings expose a default approval mode. Documented modes include:

- `default`
- `auto_edit`
- `plan`

YOLO mode exists, but the official docs note that it is enabled via the command line rather than the normal settings UI.

### Trusted folders

Gemini CLI now has a trusted-folders system. When a folder is untrusted, Gemini CLI runs in a restricted safe mode and does not load project-specific settings, commands, or MCP servers.

For this repository, that means trusted-folder guidance matters if you expect project-local settings or commands to be honored.

### Sandboxing

Gemini CLI documents sandboxing directly, including:

- command flag `-s` or `--sandbox`
- environment variable `GEMINI_SANDBOX`
- settings-based sandbox configuration
- sandbox expansion requests for extra permissions

## Practical Guidance For This Repo

- keep `AGENTS.md` as the canonical repo instruction file
- add a `GEMINI.md` wrapper if you want first-class Gemini ergonomics
- or configure `context.fileName` to include `AGENTS.md`
- prefer trusted folders when you need project-level commands or settings
- prefer sandboxed runs for unfamiliar or risky repositories
- keep local Gemini settings conservative for file writes and tool execution

## Good Gemini CLI Fit

Gemini CLI is especially useful here when you want:

- command-line automation help
- reusable project-local commands
- hierarchical project context
- sandboxing plus permission expansion
- multi-tool workflows in a terminal-first environment

## Official References

- Gemini CLI repository: https://github.com/google-gemini/gemini-cli
- GEMINI.md context files: https://geminicli.com/docs/cli/gemini-md/
- Gemini CLI commands: https://geminicli.com/docs/reference/commands/
- Gemini CLI settings: https://geminicli.com/docs/cli/settings/
- Gemini CLI trusted folders: https://geminicli.com/docs/cli/trusted-folders/
- Gemini CLI sandboxing: https://geminicli.com/docs/cli/sandbox/
