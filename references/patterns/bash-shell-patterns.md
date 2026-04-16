# Bash Shell Patterns

Load this reference when the task requires more than a trivial shell one-liner. It provides reusable idioms and anti-patterns for safe, portable, and maintainable Bash scripts.

Pair with [../builders/bash-shell-builder.md](../builders/bash-shell-builder.md) for routing context and with [../rules/security-baseline.md](../rules/security-baseline.md) when the script touches production files, remote systems, or external credentials.

---

## 1. Script Skeleton

Every non-trivial Bash script starts with a shebang, strict mode, a configuration block, and logging helpers.

```bash
#!/usr/bin/env bash
set -euo pipefail

# ---- Configuration ----
INPUT_DIR="${INPUT_DIR:-/tmp/input}"
OUTPUT_DIR="${OUTPUT_DIR:-/tmp/output}"
DRY_RUN="${DRY_RUN:-false}"
LOG_FILE="${LOG_FILE:-/tmp/$(basename "$0" .sh)-$(date +%Y%m%d).log}"

# ---- Logging ----
log()  { echo "[$(date +%H:%M:%S)] INFO  $*" | tee -a "$LOG_FILE"; }
warn() { echo "[$(date +%H:%M:%S)] WARN  $*" | tee -a "$LOG_FILE" >&2; }
die()  { echo "[$(date +%H:%M:%S)] ERROR $*" | tee -a "$LOG_FILE" >&2; exit 1; }

# ---- Guards ----
[[ -d "$INPUT_DIR" ]] || die "Input directory does not exist: $INPUT_DIR"
mkdir -p "$OUTPUT_DIR"
```

---

## 2. Argument Parsing with getopts

Use `getopts` for short flags. For long flags, use a manual `case` over `$@`.

```bash
usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS] <source_dir>

Options:
  -o DIR   Output directory (default: ./output)
  -n       Dry run — print actions without executing
  -v       Verbose output
  -h       Show this help
EOF
  exit 0
}

OUTPUT_DIR="./output"
DRY_RUN=false
VERBOSE=false

while getopts ":o:nvh" opt; do
  case "$opt" in
    o) OUTPUT_DIR="$OPTARG" ;;
    n) DRY_RUN=true ;;
    v) VERBOSE=true ;;
    h) usage ;;
    :) die "Option -$OPTARG requires an argument." ;;
    \?) die "Unknown option: -$OPTARG" ;;
  esac
done
shift $((OPTIND - 1))

SOURCE_DIR="${1:?Usage: $(basename "$0") <source_dir>}"
```

---

## 3. Dry-Run Flag

Always support a dry-run mode for scripts that move, copy, rename, or delete files.

```bash
run() {
  if [[ "$DRY_RUN" == true ]]; then
    echo "[DRY-RUN] $*"
  else
    "$@"
  fi
}

# Usage: prefix any destructive command with run
run mv "$src_file" "$dest_file"
run rm "$old_file"
run rsync -av "$SOURCE_DIR/" "$OUTPUT_DIR/"
```

---

## 4. Temporary Files and Cleanup with trap

Use `trap` to clean up temp files on exit — including on error and Ctrl+C.

```bash
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

# Temp files are safe to use inside TMP_DIR
TMP_LIST="$TMP_DIR/file-list.txt"
find "$INPUT_DIR" -name "*.pdf" | sort > "$TMP_LIST"
```

---

## 5. Safe File Operations

Always check before touching files. Never `rm` without a guard.

```bash
# Check file exists before operating
[[ -f "$file" ]] || { warn "File not found, skipping: $file"; continue; }

# Backup before overwrite
backup() {
  local src="$1"
  local dest="${src}.bak.$(date +%Y%m%d%H%M%S)"
  cp "$src" "$dest"
  log "Backup: $dest"
}

# Never delete without a guard on the variable being non-empty
[[ -n "$TARGET_FILE" ]] || die "TARGET_FILE is empty — refusing to delete."
run rm "$TARGET_FILE"
```

---

## 6. Loops Over Files

Use `find` + `while read` for robust file iteration — handles filenames with spaces.

```bash
# ✓ Safe: handles spaces in filenames
while IFS= read -r -d '' file; do
  log "Processing: $file"
  run cp "$file" "$OUTPUT_DIR/$(basename "$file")"
done < <(find "$INPUT_DIR" -name "*.pdf" -print0)

# ✓ Also safe for simple cases with no spaces
for file in "$INPUT_DIR"/*.pdf; do
  [[ -f "$file" ]] || continue  # skip glob when no match
  run cp "$file" "$OUTPUT_DIR/"
done

# ✗ Unsafe: breaks on spaces
# for file in $(ls "$INPUT_DIR"); do ...
```

---

## 7. Color Output

Add color to distinguish info, warnings, and errors without requiring external tools.

```bash
if [[ -t 1 ]]; then  # only colorize if stdout is a terminal
  RED='\033[0;31m'; YELLOW='\033[0;33m'; GREEN='\033[0;32m'; NC='\033[0m'
else
  RED=''; YELLOW=''; GREEN=''; NC=''
fi

log()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC}  $*" >&2; }
die()  { echo -e "${RED}[ERROR]${NC} $*" >&2; exit 1; }
```

---

## 8. Here-Doc Templates

Use here-docs for multi-line strings and template generation.

```bash
generate_report() {
  local date="$1"
  local count="$2"
  cat <<EOF
=== Daily Archive Report ===
Date  : $date
Files : $count
Output: $OUTPUT_DIR
EOF
}

generate_report "$(date +%Y-%m-%d)" "$FILE_COUNT" | tee -a "$LOG_FILE"
```

---

## 9. Locking to Prevent Concurrent Runs

For cron jobs, use a lock file to prevent overlapping executions.

```bash
LOCK_FILE="/tmp/$(basename "$0" .sh).lock"

exec 200>"$LOCK_FILE"
flock -n 200 || die "Another instance is already running (lock: $LOCK_FILE)."
trap 'rm -f "$LOCK_FILE"' EXIT
```

---

## 10. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| Missing `set -euo pipefail` | Script continues after errors | Add to every script header |
| `for f in $(ls dir/)` | Breaks on filenames with spaces | `while IFS= read -r -d '' f; done < <(find ... -print0)` |
| Unquoted `$VAR` in commands | Word splitting and glob expansion | Always `"$VAR"` |
| `rm -rf $DIR` with no guard | Deletes `/` if `DIR` is empty | `[[ -n "$DIR" ]] || die` before rm |
| `cat file | grep pattern` | Useless use of cat | `grep pattern file` |
| Inline secrets in scripts | Credentials in version history | Load from env vars or a secrets file not in the repo |
| No `trap` for cleanup | Temp files left on disk after errors | `trap 'rm -rf "$TMP_DIR"' EXIT` |
