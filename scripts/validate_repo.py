from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    ROOT / ".claude" / "settings.example.json",
    ROOT / ".gemini" / "settings.example.json",
    ROOT / "AGENTS.md",
    ROOT / "CHANGELOG.md",
    ROOT / "CLAUDE.md",
    ROOT / "CLAUDE.local.example.md",
    ROOT / "GEMINI.md",
    ROOT / "GEMINI.local.example.md",
    ROOT / "SKILL.md",
    ROOT / "README.md",
    ROOT / "release-notes" / "v0.1.0.md",
    ROOT / "release-notes" / "v0.2.0.md",
    ROOT / "LICENSE",
    ROOT / ".github" / "workflows" / "ci.yml",
    ROOT / "scripts" / "validate_repo.py",
    ROOT / "scripts" / "check_eval_cases.py",
    ROOT / "references" / "builders" / "html-css-javascript-builder.md",
    ROOT / "references" / "builders" / "office-script-builder.md",
    ROOT / "references" / "builders" / "powershell-builder.md",
    ROOT / "references" / "builders" / "python-builder.md",
    ROOT / "references" / "builders" / "security-builder.md",
    ROOT / "references" / "builders" / "vba-builder.md",
    ROOT / "references" / "platforms" / "claude-code-hooks.md",
    ROOT / "references" / "platforms" / "claude-code.md",
    ROOT / "references" / "platforms" / "codex-claude-gemini-crosswalk.md",
    ROOT / "references" / "platforms" / "codex-task-shaping.md",
    ROOT / "references" / "platforms" / "codex.md",
    ROOT / "references" / "platforms" / "gemini-cli.md",
    ROOT / "references" / "rules" / "output-and-safety.md",
    ROOT / "references" / "rules" / "security-baseline.md",
    ROOT / "references" / "rules" / "risk-trigger-matrix.md",
    ROOT / "examples" / "prompt-cookbook.md",
    ROOT / "examples" / "concrete-use-cases.md",
    ROOT / "examples" / "browser-kpi-tool" / "index.html",
    ROOT / "examples" / "powershell" / "rename-pdfs-by-date.ps1",
    ROOT / "examples" / "python" / "merge-csv-report.py",
    ROOT / "examples" / "security" / "unsafe-to-safe.md",
    ROOT / "examples" / "vba" / "clean-invoices.bas",
    ROOT / "eval" / "routing-cases.json",
]
MARKDOWN_FILES = [
    ROOT / "README.md",
    ROOT / "CHANGELOG.md",
    ROOT / "SKILL.md",
    ROOT / "AGENTS.md",
    ROOT / "CLAUDE.md",
    ROOT / "CLAUDE.local.example.md",
    ROOT / "GEMINI.md",
    ROOT / "GEMINI.local.example.md",
    *ROOT.glob("references/**/*.md"),
    *ROOT.glob("examples/**/*.md"),
]

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HTML_SRC_RE = re.compile(r"""<(?:img|source)[^>]+(?:src|srcset)=["']([^"']+)["']""")
AT_INCLUDE_RE = re.compile(r"(?m)^@([^\s]+)")


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def check_required_files() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        fail(f"Missing required files: {', '.join(missing)}")


def check_skill_frontmatter() -> None:
    content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter.")
    if "\nname:" not in content or "\ndescription:" not in content:
        fail("SKILL.md frontmatter must include name and description.")


def check_openai_yaml() -> None:
    openai_yaml = ROOT / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        fail("agents/openai.yaml is missing.")
    content = openai_yaml.read_text(encoding="utf-8")
    if 'display_name:' not in content or 'default_prompt:' not in content:
        fail("agents/openai.yaml must include display_name and default_prompt.")
    if "$ai-builder" not in content:
        fail("agents/openai.yaml default_prompt must mention $ai-builder.")


def normalize_target(source: Path, target: str) -> Path | None:
    target = target.strip()
    if not target or target.startswith("http://") or target.startswith("https://"):
        return None
    if target.startswith("#"):
        return None
    target = target.split()[0]
    return (source.parent / target).resolve()


def check_links() -> None:
    for markdown_file in MARKDOWN_FILES:
        content = markdown_file.read_text(encoding="utf-8")
        for pattern in (MARKDOWN_LINK_RE, HTML_SRC_RE):
            for match in pattern.findall(content):
                candidate = normalize_target(markdown_file, match)
                if candidate is None:
                    continue
                if not candidate.exists():
                    fail(
                        f"Broken local reference in {markdown_file.relative_to(ROOT)}: {match}"
                    )


def check_context_imports() -> None:
    for context_file in (ROOT / "CLAUDE.md", ROOT / "GEMINI.md"):
        content = context_file.read_text(encoding="utf-8")
        for match in AT_INCLUDE_RE.findall(content):
            candidate = normalize_target(context_file, match)
            if candidate is None:
                continue
            if not candidate.exists():
                fail(
                    f"Broken context import in {context_file.relative_to(ROOT)}: {match}"
                )


def main() -> None:
    check_required_files()
    check_skill_frontmatter()
    check_openai_yaml()
    check_links()
    check_context_imports()
    print("[OK] Repository structure and local links are valid.")


if __name__ == "__main__":
    main()
