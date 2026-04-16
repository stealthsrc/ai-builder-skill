# Recipe: Bash Bulk Archive by Date

Complete Bash script that sweeps files from a source directory into monthly subfolders (`YYYY/MM/`), writes a move log CSV for rollback, and supports a dry-run mode.

Pair with [../builders/bash-shell-builder.md](../builders/bash-shell-builder.md) and [../patterns/bash-shell-patterns.md](../patterns/bash-shell-patterns.md).

---

## What It Does

1. Finds all files in `SOURCE_DIR` matching an optional extension filter.
2. Reads the last-modified date of each file.
3. Moves each file into `ARCHIVE_DIR/YYYY/MM/` — creating the folder if needed.
4. Appends a move record (`source,dest,date_moved`) to a log CSV.
5. Prints a color summary and exits non-zero if any moves failed.
6. With `--dry-run`, prints planned moves without moving anything.

---

## Full Script — archive-by-date.sh

```bash
#!/usr/bin/env bash
set -euo pipefail

# ---- Configuration ----
SOURCE_DIR="${SOURCE_DIR:-./source}"
ARCHIVE_DIR="${ARCHIVE_DIR:-./archive}"
FILE_EXT="${FILE_EXT:-}"            # e.g. "pdf" — blank = all files
DRY_RUN=false
VERBOSE=false
LOG_FILE="${ARCHIVE_DIR}/move-log-$(date +%Y%m%d%H%M%S).csv"

# ---- Logging ----
if [[ -t 1 ]]; then
  GRN='\033[0;32m'; YLW='\033[0;33m'; RED='\033[0;31m'; NC='\033[0m'
else
  GRN=''; YLW=''; NC=''; RED=''
fi

log()  { echo -e "${GRN}[INFO]${NC}  $*"; }
warn() { echo -e "${YLW}[WARN]${NC}  $*" >&2; }
die()  { echo -e "${RED}[ERR]${NC}   $*" >&2; exit 1; }

# ---- Argument parsing ----
usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Move files from SOURCE_DIR into ARCHIVE_DIR/YYYY/MM/ by last-modified date.

Options:
  -s DIR   Source directory          (env: SOURCE_DIR, default: ./source)
  -a DIR   Archive root directory    (env: ARCHIVE_DIR, default: ./archive)
  -e EXT   File extension filter     (e.g. pdf — default: all files)
  -n       Dry run — print actions without moving
  -v       Verbose output
  -h       Show this help
EOF
  exit 0
}

while getopts ":s:a:e:nvh" opt; do
  case "$opt" in
    s) SOURCE_DIR="$OPTARG" ;;
    a) ARCHIVE_DIR="$OPTARG" ;;
    e) FILE_EXT="$OPTARG" ;;
    n) DRY_RUN=true ;;
    v) VERBOSE=true ;;
    h) usage ;;
    :) die "Option -$OPTARG requires an argument." ;;
    \?) die "Unknown option: -$OPTARG" ;;
  esac
done

# ---- Guards ----
[[ -d "$SOURCE_DIR" ]]  || die "Source directory not found: $SOURCE_DIR"
mkdir -p "$ARCHIVE_DIR"

if [[ "$DRY_RUN" == false ]]; then
  # Write CSV header only once
  echo "source,dest,date_moved" > "$LOG_FILE"
  log "Move log: $LOG_FILE"
fi

# ---- Build file list ----
TMP_LIST=$(mktemp)
trap 'rm -f "$TMP_LIST"' EXIT

if [[ -n "$FILE_EXT" ]]; then
  find "$SOURCE_DIR" -maxdepth 1 -type f -name "*.$FILE_EXT" -print0 > "$TMP_LIST"
else
  find "$SOURCE_DIR" -maxdepth 1 -type f -print0 > "$TMP_LIST"
fi

# ---- Move files ----
MOVED=0
FAILED=0
SKIPPED=0

while IFS= read -r -d '' src_file; do
  filename=$(basename "$src_file")

  # Get year and month from last-modified time (portable: GNU + BSD)
  if date --version &>/dev/null 2>&1; then
    # GNU date (Linux)
    year=$(date -r "$src_file" +%Y)
    month=$(date -r "$src_file" +%m)
  else
    # BSD date (macOS)
    year=$(stat -f "%Sm" -t "%Y" "$src_file")
    month=$(stat -f "%Sm" -t "%m" "$src_file")
  fi

  dest_dir="$ARCHIVE_DIR/$year/$month"
  dest_file="$dest_dir/$filename"

  # Collision guard
  if [[ -e "$dest_file" ]]; then
    warn "Destination exists, skipping: $dest_file"
    (( SKIPPED++ )) || true
    continue
  fi

  if [[ "$DRY_RUN" == true ]]; then
    echo "[DRY-RUN] mv '$src_file' → '$dest_file'"
    continue
  fi

  mkdir -p "$dest_dir"
  if mv "$src_file" "$dest_file"; then
    echo "\"$src_file\",\"$dest_file\",\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"" >> "$LOG_FILE"
    [[ "$VERBOSE" == true ]] && log "Moved: $filename → $year/$month/"
    (( MOVED++ )) || true
  else
    warn "Move failed: $src_file"
    (( FAILED++ )) || true
  fi
done < "$TMP_LIST"

# ---- Summary ----
if [[ "$DRY_RUN" == true ]]; then
  echo ""
  log "Dry-run complete — no files were moved."
else
  echo ""
  log "Archive complete — moved: $MOVED, skipped: $SKIPPED, failed: $FAILED"
  [[ "$FAILED" -gt 0 ]] && warn "Some files failed to move — check output above."
fi

[[ "$FAILED" -eq 0 ]] || exit 1
```

---

## Setup

```bash
chmod +x archive-by-date.sh
```

---

## Run

```bash
# Dry run — see what would move
./archive-by-date.sh -s /data/reports -a /data/archive -e pdf -n

# Live run — move PDFs
./archive-by-date.sh -s /data/reports -a /data/archive -e pdf

# All file types, verbose
./archive-by-date.sh -s /data/exports -a /data/archive -v

# Via environment variables (useful in CI/cron)
SOURCE_DIR=/data/reports ARCHIVE_DIR=/data/archive FILE_EXT=csv ./archive-by-date.sh
```

---

## Validation

- Dry-run first — confirm each planned destination path looks correct.
- After a live run, open `archive/move-log-YYYYMMDDHHMMSS.csv` — each row should show source, destination, and timestamp.
- Check `archive/YYYY/MM/` — confirm files are present and `source/` directory is empty or reduced.

---

## Rollback

The move log CSV records every source and destination path. To undo:

```bash
tail -n +2 archive/move-log-YYYYMMDDHHMMSS.csv | while IFS=',' read -r src dest _; do
  # Strip surrounding quotes if present
  src="${src//\"/}"
  dest="${dest//\"/}"
  [[ -f "$dest" ]] && mv "$dest" "$src" && echo "Restored: $src"
done
```

---

## Edge Cases

| Case | Behavior |
|---|---|
| Destination file already exists | Skips with a warning — never overwrites |
| Source is a symlink | `find -type f` skips symlinks by default |
| Filename with spaces | Handled via `find -print0` + `read -d ''` |
| File last-modified date unavailable | `date -r` will error — verify file permissions |
| macOS vs Linux date | Script auto-detects GNU vs BSD date syntax |
