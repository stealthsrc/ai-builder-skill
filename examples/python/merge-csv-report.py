from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


INPUT_DIR = Path("input-csv")
OUTPUT_FILE = Path("regional_summary.csv")


def parse_amount(raw_value: str) -> float:
    cleaned = raw_value.replace(",", "").strip()
    return float(cleaned or 0)


def collect_totals(input_dir: Path) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)

    for csv_path in sorted(input_dir.glob("*.csv")):
        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)

            for row in reader:
                region = row.get("region", "").strip() or "Unknown"
                amount = parse_amount(row.get("amount", "0"))
                totals[region] += amount

    return dict(sorted(totals.items()))


def write_summary(output_file: Path, totals: dict[str, float]) -> None:
    with output_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["region", "total_amount"])

        for region, total in totals.items():
            writer.writerow([region, f"{total:.2f}"])


def main() -> None:
    if not INPUT_DIR.exists():
        raise SystemExit(f"Input directory not found: {INPUT_DIR}")

    totals = collect_totals(INPUT_DIR)
    write_summary(OUTPUT_FILE, totals)
    print(f"Wrote {OUTPUT_FILE} with {len(totals)} regions.")


if __name__ == "__main__":
    main()
