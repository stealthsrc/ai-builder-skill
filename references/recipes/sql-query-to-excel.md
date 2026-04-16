# Recipe: SQL Query to Formatted Excel Report

Complete Python script that connects to a SQLite database (or CSV files treated as tables via DuckDB), runs a SQL query, and exports the result as a formatted `.xlsx` with frozen header, bold column names, and auto-width columns.

Pair with [../builders/python-builder.md](../builders/python-builder.md) and [../patterns/python-patterns.md](../patterns/python-patterns.md).

---

## What It Does

1. Accepts a SQL query from a `.sql` file or the command line.
2. Connects to a SQLite file or treats a folder of CSV files as tables (via DuckDB).
3. Executes the query and streams results into a pandas DataFrame.
4. Writes the result to a new `.xlsx` file with:
   - Frozen first row (header)
   - Bold, filled header cells
   - Auto-width columns
   - A summary print of row count and output path.

---

## Dependencies

```bash
pip install pandas openpyxl duckdb
```

| Package | Purpose |
|---|---|
| `pandas` | Result DataFrame and Excel bridge |
| `openpyxl` | Excel formatting (freeze, bold, fill, auto-width) |
| `duckdb` | Query CSV files with SQL without a database server |

---

## Full Script — sql_to_excel.py

```python
"""Run a SQL query and export results to a formatted Excel report."""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

import duckdb
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


# ---- Configuration ----
HEADER_FILL_COLOR = "2563EB"   # blue header
HEADER_FONT_COLOR = "FFFFFF"   # white text
MIN_COL_WIDTH     = 10
MAX_COL_WIDTH     = 50


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--db",   type=Path, help="SQLite database file (.db / .sqlite)")
    g.add_argument("--csv-dir", type=Path, help="Folder of CSV files (queried via DuckDB)")
    p.add_argument("--query",  type=str,  help="SQL query string (use quotes)")
    p.add_argument("--sql",    type=Path, help="Path to a .sql file")
    p.add_argument("--output", type=Path, default=Path("report.xlsx"), help="Output .xlsx path")
    return p.parse_args()


def load_query(args: argparse.Namespace) -> str:
    if args.sql:
        return args.sql.read_text(encoding="utf-8").strip()
    if args.query:
        return args.query.strip()
    raise ValueError("Provide --query or --sql.")


def run_sqlite(db: Path, sql: str) -> pd.DataFrame:
    with sqlite3.connect(db) as conn:
        return pd.read_sql_query(sql, conn)


def run_duckdb_csv(csv_dir: Path, sql: str) -> pd.DataFrame:
    con = duckdb.connect()
    # Register every CSV in the folder as a table named by stem
    for csv_file in sorted(csv_dir.glob("*.csv")):
        con.execute(
            f"CREATE VIEW {csv_file.stem} AS SELECT * FROM read_csv_auto('{csv_file}')"
        )
    return con.execute(sql).df()


def write_excel(df: pd.DataFrame, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_suffix(".tmp.xlsx")

    with pd.ExcelWriter(tmp, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Report")
        ws = writer.sheets["Report"]

        # Freeze header row
        ws.freeze_panes = "A2"

        # Style header row
        header_font  = Font(bold=True, color=HEADER_FONT_COLOR)
        header_fill  = PatternFill("solid", fgColor=HEADER_FILL_COLOR)
        header_align = Alignment(horizontal="center", vertical="center")

        for cell in ws[1]:
            cell.font      = header_font
            cell.fill      = header_fill
            cell.alignment = header_align

        # Auto-width columns
        for col_idx, column_cells in enumerate(ws.columns, start=1):
            max_len = max(
                (len(str(c.value)) if c.value is not None else 0) for c in column_cells
            )
            col_letter = get_column_letter(col_idx)
            ws.column_dimensions[col_letter].width = max(
                MIN_COL_WIDTH, min(max_len + 2, MAX_COL_WIDTH)
            )

    tmp.replace(output)   # atomic rename


def main() -> int:
    args  = parse_args()
    sql   = load_query(args)
    print(f"Running query...")

    if args.db:
        if not args.db.exists():
            print(f"[ERROR] Database not found: {args.db}", file=sys.stderr)
            return 2
        df = run_sqlite(args.db, sql)
    else:
        if not args.csv_dir.is_dir():
            print(f"[ERROR] CSV directory not found: {args.csv_dir}", file=sys.stderr)
            return 2
        df = run_duckdb_csv(args.csv_dir, sql)

    print(f"Rows returned: {len(df)}")
    write_excel(df, args.output)
    print(f"Report written: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

## Run

```bash
# Install
pip install pandas openpyxl duckdb

# Query a SQLite database
python sql_to_excel.py --db sales.db --query "SELECT region, SUM(amount) AS total FROM orders GROUP BY region ORDER BY total DESC" --output reports/sales-by-region.xlsx

# Query CSV files as SQL tables
python sql_to_excel.py --csv-dir exports/ --sql queries/monthly.sql --output reports/monthly.xlsx
```

---

## SQL File Example — queries/monthly.sql

```sql
SELECT
    strftime('%Y-%m', order_date) AS month,
    COUNT(*)                      AS order_count,
    ROUND(SUM(amount), 2)         AS revenue
FROM orders
WHERE order_date >= date('now', '-12 months')
GROUP BY month
ORDER BY month
```

---

## Validation

- Open the output `.xlsx` in Excel — confirm the header row is blue and bold.
- Scroll to the bottom — row count should match the printed "Rows returned" count.
- Resize a column manually — auto-width may truncate very long values (capped at 50 chars).

---

## Edge Cases

| Case | Behavior |
|---|---|
| Query returns 0 rows | Writes an Excel file with only the header row |
| Column value is None/NULL | Width calculation treats it as 0 length |
| CSV filename contains spaces | DuckDB view name will fail — rename files to snake_case |
| SQLite file is locked | `sqlite3.OperationalError` — close any open Excel/DB connection first |
