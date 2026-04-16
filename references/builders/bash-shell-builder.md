# Bash Shell Builder

Use this reference for Linux and macOS shell automation, CI/CD scripts, file operations, and system administration tasks that belong in a terminal.

## Use It For

- File and folder operations on Linux or macOS
- CI/CD pipeline scripts (GitHub Actions, GitLab CI, etc.)
- Cron jobs and scheduled maintenance tasks
- System health checks and log analysis
- Dev environment setup and bootstrapping scripts
- Wrapper scripts around other CLI tools (git, ffmpeg, imagemagick, etc.)
- Cross-tool pipelines using pipes, redirects, and standard Unix utilities

## Default Approach

- Default to **Bash** unless the user specifies sh or another shell.
- Start every non-trivial script with `set -euo pipefail` — exits on errors, unset variables, and pipe failures.
- Use `shellcheck`-compatible syntax — avoid common pitfalls like unquoted variables.
- Keep configurable paths, names, and thresholds in variables at the top.
- Prefer absolute paths in scripts that run as cron jobs or in CI.

## Script Structure

```bash
#!/usr/bin/env bash
set -euo pipefail

# ---- Configuration ----
INPUT_DIR="${1:-/tmp/input}"
OUTPUT_DIR="${2:-/tmp/output}"
DRY_RUN="${DRY_RUN:-false}"
LOG_FILE="/tmp/script-$(date +%Y%m%d).log"

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG_FILE"; }
die() { log "ERROR: $*"; exit 1; }
```

## Safety And Practicality

- Always quote variables: `"$VAR"` not `$VAR` — prevents word splitting on paths with spaces.
- Check that directories and files exist before operating on them.
- Never use `rm -rf` without an explicit guard (non-empty variable check, interactive confirmation, or dry-run).
- Prefer `mv` to a dated backup location over permanent deletion.
- For scripts that modify production systems, require an explicit `--apply` flag and default to dry-run.
- Use `trap` to clean up temporary files even on error.

## Portability Notes

- `set -o pipefail` is Bash-specific — not available in POSIX sh. Mark the shebang `#!/usr/bin/env bash` when used.
- macOS ships with Bash 3.2. Avoid `declare -A` (associative arrays) if macOS compatibility is required, or tell users to install Bash 5 via Homebrew.
- For CI/CD, prefer POSIX-compatible sh unless the runner is known to have Bash.

## What To Deliver

- State the filename and extension (`.sh`).
- Include the exact command to make it executable: `chmod +x script.sh`.
- Provide the full invocation with example arguments.
- Mention any external tool dependencies (jq, curl, rsync, etc.).
- Include a dry-run mode or preview output for destructive operations.

## Deep References

Load these when the task is non-trivial:

- [../patterns/bash-shell-patterns.md](../patterns/bash-shell-patterns.md) — script skeleton with `set -euo pipefail`, argument parsing with `getopts`, color logging, dry-run flag, safety guards, loop idioms, `trap` cleanup, `here-doc` templates, anti-patterns.
- [../recipes/bash-bulk-archive.md](../recipes/bash-bulk-archive.md) — sweep files into dated folders with dry-run, color log output, and a rollback plan using a move log.
