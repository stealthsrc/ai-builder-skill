# Python Patterns

Load this reference when the task requires more than a trivial script. It provides reusable idioms and anti-patterns for maintainable data, file, and API workflows.

Pair with [../builders/python-builder.md](../builders/python-builder.md) for routing context and with [../rules/security-baseline.md](../rules/security-baseline.md) when the script handles secrets, external input, or destructive actions.

---

## 1. Script Skeleton

Use `argparse`, `logging`, `pathlib`, and an explicit `main()` guarded by `if __name__ == "__main__":`.

```python
"""Clean exported invoices and write a normalized CSV."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Input folder.")
    parser.add_argument("--output", type=Path, required=True, help="Output CSV path.")
    parser.add_argument("--dry-run", action="store_true", help="Preview only.")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


def configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def main() -> int:
    args = parse_args()
    configure_logging(args.verbose)

    if not args.source.is_dir():
        logging.error("Source folder does not exist: %s", args.source)
        return 2

    # ... work ...

    logging.info("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Return integer exit codes. Reserve `1` for "something went wrong", `2` for "bad input".

---

## 2. CSV That Opens Cleanly In Excel

Excel expects a UTF-8 BOM to display accented characters correctly when the user double-clicks a `.csv` file. Use `utf-8-sig` on write. Always pass `newline=""` to avoid blank rows on Windows.

```python
import csv
from pathlib import Path

def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
```

For reading, prefer `utf-8` first and fall back to `cp1252` when the file comes from a Windows export.

```python
def read_csv(path: Path) -> list[dict[str, str]]:
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            with path.open("r", encoding=encoding, newline="") as fh:
                return list(csv.DictReader(fh))
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("utf-8", b"", 0, 1, f"Could not decode {path}")
```

---

## 3. openpyxl vs pandas Trade-Off

- Use `openpyxl` when the workbook is small, when you need to preserve formatting, or when the user does not already have pandas installed.
- Use `pandas` when the work is mostly tabular transformation, joins, group-by, or pivoting.

Minimal `openpyxl` write pattern:

```python
from openpyxl import Workbook
from openpyxl.styles import Font

def write_report(path: Path, rows: list[dict[str, object]]) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Report"

    headers = list(rows[0].keys())
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for row in rows:
        ws.append([row.get(h) for h in headers])

    ws.freeze_panes = "A2"
    wb.save(path)
```

Minimal `pandas` read/write for CSV-to-Excel:

```python
import pandas as pd

def csv_to_excel(csv_path: Path, xlsx_path: Path) -> None:
    df = pd.read_csv(csv_path, dtype=str).fillna("")
    df.to_excel(xlsx_path, index=False, engine="openpyxl")
```

---

## 4. Atomic File Writes

For outputs that the user opens while the script runs, write to a temp file in the same folder and rename on success. That guarantees either the old or the new file exists, never a truncated one.

```python
from pathlib import Path
import os
import tempfile

def write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)
```

---

## 5. Safe Subprocess

Never use `shell=True` with any string that contains user data. Pass an argument list.

```python
import subprocess

def git_log_since(repo: Path, since: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "log", "--since", since, "--pretty=format:%h %s"],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout
```

`check=True` raises `CalledProcessError` on non-zero exit. `timeout=30` prevents infinite hangs.

---

## 6. HTTP With Retries

Use `urllib3.util.Retry` through a `requests.Session` for automatic, bounded retries on transient errors.

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def make_session() -> requests.Session:
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET", "POST"}),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def fetch_json(url: str, token: str) -> dict:
    session = make_session()
    response = session.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=(5, 30),
    )
    response.raise_for_status()
    return response.json()
```

Always set both a connect and a read timeout.

---

## 7. Input Validation Without A Heavy Dep

For simple scripts, validate via `argparse` types and explicit checks. Pull in `pydantic` only when schema validation is non-trivial.

```python
def positive_int(value: str) -> int:
    n = int(value)
    if n <= 0:
        raise argparse.ArgumentTypeError(f"must be positive: {value}")
    return n

parser.add_argument("--limit", type=positive_int, default=100)
```

For tabular data, assert expected columns immediately after reading:

```python
required = {"invoice_id", "amount", "currency"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Input is missing columns: {sorted(missing)}")
```

---

## 8. Secrets From Environment, Not Code

```python
import os

def load_token(var_name: str = "API_TOKEN") -> str:
    token = os.environ.get(var_name)
    if not token:
        raise RuntimeError(
            f"Missing required environment variable: {var_name}. "
            "Do not hardcode secrets in the script."
        )
    return token
```

For user-local storage, prefer `keyring` over `.env` in the repo. Never commit `.env` files.

---

## 9. Excel Files Locked By The User

When a workbook is open in Excel, `openpyxl` cannot overwrite it on Windows. Detect and surface a friendly error.

```python
from openpyxl import load_workbook

try:
    wb = load_workbook(path)
except PermissionError:
    raise RuntimeError(
        f"'{path.name}' is open in Excel. Close it and rerun."
    )
```

---

## 10. Anti-Patterns With Fixes

| Anti-pattern | Why it hurts | Fix |
|---|---|---|
| `os.system(cmd)` | shell injection, loses exit code | `subprocess.run([...], check=True)` |
| `subprocess.run(..., shell=True)` with user input | shell injection | pass an argument list, never a single string |
| `eval(user_input)` | arbitrary code execution | parse explicitly; `ast.literal_eval` for literals only |
| Mutable default args `def f(x=[])` | shared state between calls | use `None` then assign `[]` inside |
| Bare `except:` | swallows `KeyboardInterrupt` | catch specific exception types |
| `print()` for logs | no levels, cannot redirect | use `logging` |
| Hardcoded paths `C:\Users\...` | breaks on other machines | `pathlib.Path(__file__).parent`, `argparse` params, env vars |
| Concatenating SQL | SQL injection | parameterized queries |
| Missing `newline=""` on CSV open | blank rows on Windows | always `newline=""` |
| UTF-8 without BOM for Excel | accents broken on double-click | write with `encoding="utf-8-sig"` |
| `requests.get(url)` without timeout | can hang forever | always pass `timeout=(5, 30)` |
| Hardcoded credentials | secret leak | `os.environ`, `keyring`, secret manager |

---

## 11. SQL Patterns

For SQLite and DuckDB (CSV-as-tables), always use parameterized queries. Never build SQL strings with f-strings or `%` formatting.

```python
import sqlite3
from pathlib import Path

def query_sqlite(db: Path, sql: str, params: tuple = ()) -> list[dict]:
    """Run a parameterized query and return rows as dicts."""
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]

# ✓ Safe: parameterized
rows = query_sqlite(
    Path("sales.db"),
    "SELECT * FROM orders WHERE region = ? AND amount > ?",
    ("West", 1000),
)

# ✗ Unsafe: string interpolation → SQL injection
# rows = query_sqlite(db, f"SELECT * FROM orders WHERE region = '{user_input}'")
```

For CSV-as-tables with DuckDB:

```python
import duckdb
from pathlib import Path

def query_csvs(csv_dir: Path, sql: str) -> list[dict]:
    con = duckdb.connect()
    for csv_file in sorted(csv_dir.glob("*.csv")):
        # Table name = file stem — must be a safe identifier
        if not csv_file.stem.replace("_", "").isalnum():
            raise ValueError(f"Unsafe filename for SQL table: {csv_file.stem}")
        con.execute(f"CREATE VIEW {csv_file.stem} AS SELECT * FROM read_csv_auto(?)", [str(csv_file)])
    return con.execute(sql).fetchdf().to_dict("records")
```

Use `pandas.read_sql_query` when integrating with openpyxl or Excel output:

```python
import pandas as pd
import sqlite3

with sqlite3.connect("sales.db") as conn:
    df = pd.read_sql_query(
        "SELECT region, SUM(amount) AS total FROM orders GROUP BY region",
        conn,
    )
```

---

## Related

- Recipe: [../recipes/csv-merge-excel-ready.md](../recipes/csv-merge-excel-ready.md)
- Recipe: [../recipes/sql-query-to-excel.md](../recipes/sql-query-to-excel.md)
- Safety: [../rules/security-baseline.md](../rules/security-baseline.md)
