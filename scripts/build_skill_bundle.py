"""Build a Claude Web / Claude Code Skill bundle.

Produces ``dist/ai-builder.zip`` containing only the files a Skill consumer
needs. Excludes local overlays, git metadata, CI config, and the ``dist/``
directory itself.

Usage::

    python scripts/build_skill_bundle.py

The bundle layout mirrors the repository so relative links inside ``SKILL.md``
resolve correctly once the archive is unpacked.
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "dist"
OUT_FILE = OUT_DIR / "ai-builder.zip"

INCLUDE_FILES = [
    "SKILL.md",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "ANTIGRAVITY.md",
    "README.md",
    "LICENSE",
]

INCLUDE_DIRS = [
    "references",
    "examples",
    "assets/starters",
]

EXCLUDE_SUFFIXES = (
    ".zip",
    ".DS_Store",
)

EXCLUDE_DIR_NAMES = {
    ".git",
    ".github",
    ".claude",
    ".gemini",
    ".antigravity",
    "dist",
    "__pycache__",
    "node_modules",
}


def iter_bundle_files() -> list[Path]:
    files: list[Path] = []

    for rel in INCLUDE_FILES:
        path = ROOT / rel
        if path.is_file():
            files.append(path)

    for rel in INCLUDE_DIRS:
        base = ROOT / rel
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            if any(part in EXCLUDE_DIR_NAMES for part in path.parts):
                continue
            if path.name.endswith(EXCLUDE_SUFFIXES):
                continue
            files.append(path)

    return files


def build() -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if OUT_FILE.exists():
        OUT_FILE.unlink()

    files = iter_bundle_files()
    if not files:
        raise SystemExit("[FAIL] No files matched the bundle spec.")

    with zipfile.ZipFile(OUT_FILE, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            arcname = path.relative_to(ROOT).as_posix()
            zf.write(path, arcname)

    return OUT_FILE


def main() -> None:
    out = build()
    size_kb = out.stat().st_size / 1024
    print(f"[OK] Built {out.relative_to(ROOT)} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
