from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVAL_FILE = ROOT / "eval" / "routing-cases.json"
REQUIRED_FIELDS = {
    "id",
    "prompt",
    "expected_primary_builder",
    "required_references",
    "expected_risk_flags",
    "notes",
}
ALLOWED_RISK_FLAGS = {
    "bulk-file-rename",
    "destructive-file-op",
    "email-send",
    "macro-risk",
    "unsafe-command-execution",
    "untrusted-input",
}


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def main() -> None:
    data = json.loads(EVAL_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        fail("routing-cases.json must contain a non-empty list.")

    seen_ids: set[str] = set()

    for index, case in enumerate(data, start=1):
        if not isinstance(case, dict):
            fail(f"Case #{index} is not an object.")

        missing = REQUIRED_FIELDS - set(case)
        if missing:
            fail(f"Case #{index} is missing fields: {', '.join(sorted(missing))}")

        case_id = case["id"]
        if case_id in seen_ids:
            fail(f"Duplicate case id: {case_id}")
        seen_ids.add(case_id)

        builder_path = ROOT / case["expected_primary_builder"]
        if not builder_path.exists():
            fail(f"{case_id}: missing builder {case['expected_primary_builder']}")

        for reference in case["required_references"]:
            target = ROOT / reference
            if not target.exists():
                fail(f"{case_id}: missing required reference {reference}")

        for flag in case["expected_risk_flags"]:
            if flag not in ALLOWED_RISK_FLAGS:
                fail(f"{case_id}: unknown risk flag {flag}")

        if len(case["prompt"].strip()) < 10:
            fail(f"{case_id}: prompt is too short to be meaningful.")

    print(f"[OK] Validated {len(data)} routing evaluation cases.")


if __name__ == "__main__":
    main()
