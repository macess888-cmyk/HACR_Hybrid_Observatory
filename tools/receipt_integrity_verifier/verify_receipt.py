import json
import sys
from pathlib import Path

REQUIRED_TOP_LEVEL = [
    "receipt_id",
    "case_id",
    "semantic_output",
    "inspection_scope",
    "observed_conditions",
    "runtime_reductions",
    "boundary",
    "result",
    "invariant",
    "default",
]

REQUIRED_BOUNDARY = [
    "observer_only",
    "runtime_local",
    "anti_authoritative",
    "non_remedial",
    "does_not_authorize_intervention",
]

VALID_OUTPUTS = {"PASS", "HOLD", "FAIL", "STOP", "REVERSE", "SHADOW"}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python verify_receipt.py <receipt.json>")

    path = Path(sys.argv[1])

    if not path.exists():
        fail(f"Receipt not found: {path}")

    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON: {exc}")

    for field in REQUIRED_TOP_LEVEL:
        if field not in receipt:
            fail(f"Missing top-level field: {field}")

    if receipt["semantic_output"] not in VALID_OUTPUTS:
        fail(f"Invalid semantic_output: {receipt['semantic_output']}")

    boundary = receipt["boundary"]

    for field in REQUIRED_BOUNDARY:
        if field not in boundary:
            fail(f"Missing boundary field: {field}")
        if boundary[field] is not True:
            fail(f"Boundary field must be true: {field}")

    if receipt["invariant"] != "Break survivability, not ontology.":
        fail("Invariant mismatch")

    if receipt["default"] != "UNKNOWN -> HOLD":
        fail("Default mismatch")

    print("PASS: receipt structure verified")
    print(f"receipt_id: {receipt['receipt_id']}")
    print(f"case_id: {receipt['case_id']}")
    print(f"semantic_output: {receipt['semantic_output']}")


if __name__ == "__main__":
    main()