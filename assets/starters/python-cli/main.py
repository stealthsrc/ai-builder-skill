from __future__ import annotations

from pathlib import Path


INPUT_FILE = Path("input.txt")
OUTPUT_FILE = Path("output.txt")


def transform(text: str) -> str:
    return text.strip().upper()


def main() -> None:
    source = INPUT_FILE.read_text(encoding="utf-8")
    result = transform(source)
    OUTPUT_FILE.write_text(result + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
