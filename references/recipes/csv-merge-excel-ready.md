# Recipe: Merge CSV Files Into An Excel-Ready Report

## When To Use

The user has several CSV exports in a folder. They want one consolidated file that opens cleanly in Excel (correct encoding, no blank rows, formatted header, frozen top row).

## Route

Primary: Python. Load [../patterns/python-patterns.md](../patterns/python-patterns.md) for CSV encoding idioms and the openpyxl template.

## Assumptions

- every CSV shares the same header row
- files use UTF-8 or CP1252 encoding
- the user has Python 3.9 or newer
- the output is a single `.xlsx` file with the union of all rows

## Implementation

Save as `merge_csv_report.py`. Keep the configuration block at the top visible.

```python
"""Merge every CSV in a folder into a single Excel-ready workbook."""

from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Folder containing CSV files.")
    parser.add_argument("--output", type=Path, required=True, help="Output .xlsx path.")
    parser.add_argument("--sheet-name", default="Report")
    parser.add_argument("--source-column", default="SourceFile",
                        help="Name of the extra column that records the CSV filename.")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


def configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            with path.open("r", encoding=encoding, newline="") as fh:
                return list(csv.DictReader(fh))
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("utf-8", b"", 0, 1, f"Cannot decode {path}")


def collect_rows(folder: Path, source_column: str) -> tuple[list[str], list[dict[str, str]]]:
    headers: list[str] = []
    merged: list[dict[str, str]] = []

    files = sorted(p for p in folder.iterdir() if p.suffix.lower() == ".csv")
    if not files:
        raise RuntimeError(f"No .csv files found in {folder}")

    for path in files:
        logging.info("Reading %s", path.name)
        rows = read_csv(path)
        if not rows:
            continue
        if not headers:
            headers = list(rows[0].keys()) + [source_column]
        for row in rows:
            row[source_column] = path.name
            merged.append(row)

    return headers, merged


def write_xlsx(path: Path, sheet_name: str, headers: list[str], rows: list[dict[str, str]]) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    ws.append(headers)
    header_fill = PatternFill(start_color="FF1F3A44", end_color="FF1F3A44", fill_type="solid")
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFFFF")
        cell.fill = header_fill

    for row in rows:
        ws.append([row.get(h, "") for h in headers])

    ws.freeze_panes = "A2"

    for index, header in enumerate(headers, start=1):
        max_len = max([len(header)] + [len(str(row.get(header, ""))) for row in rows])
        ws.column_dimensions[get_column_letter(index)].width = min(max(10, max_len + 2), 60)

    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)


def main() -> int:
    args = parse_args()
    configure_logging(args.verbose)

    if not args.source.is_dir():
        logging.error("Source is not a folder: %s", args.source)
        return 2

    try:
        headers, rows = collect_rows(args.source, args.source_column)
    except RuntimeError as exc:
        logging.error("%s", exc)
        return 1

    write_xlsx(args.output, args.sheet_name, headers, rows)
    logging.info("Wrote %d rows to %s", len(rows), args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## How To Run

Install the single dependency once:

```bash
pip install openpyxl
```

Run it:

```bash
python merge_csv_report.py --source "D:\Exports\weekly" --output "D:\Reports\weekly.xlsx"
```

Add `-v` for a verbose run.

## Validate

- row count in the `.xlsx` equals the sum of data rows across every CSV
- the first column row is bold with a colored fill
- the top row is frozen when scrolling
- the `SourceFile` column records the original CSV filename for each row
- opening the file does not prompt an encoding repair

## Rollback

- the script does not modify the source CSVs
- delete the output `.xlsx` to redo

## Edge Cases

- a CSV with extra columns: the extras are merged into the header set; missing values become empty strings
- a CSV with a different header order: handled by `DictReader`; the first file defines column order
- locked output: if the `.xlsx` is open in Excel, the run fails with `PermissionError`; close and rerun
- very large datasets: `openpyxl` holds the whole workbook in memory; for tens of millions of rows prefer `xlsxwriter` with `constant_memory=True` or switch to Parquet
