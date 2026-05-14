import json
import hashlib
from pathlib import Path

CASE_DIR = Path("failure_locator/cases")
RECEIPT_DIR = Path("failure_locator/receipts")

PASS = "PASS"
HOLD = "HOLD"
FAIL = "FAIL"


def ensure_receipt_dir():
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)


def load_case(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def classify_case(case):
    interruption_viability = str(
        case.get("interruption_viability", "")
    ).lower()

    continuation_pressure = case.get(
        "continuation_pressure",
        []
    )

    downstream_reachability = case.get(
        "downstream_continuation_reachability",
        False
    )

    dependency_visibility = case.get(
        "dependency_visibility",
        "unknown"
    ).lower()

    if dependency_visibility == "unknown":
        return HOLD

    if (
        interruption_viability == "degraded"
        and (
            continuation_pressure
            or downstream_reachability
        )
    ):
        return FAIL

    return PASS


def build_receipt(case, verdict):
    return {
        "case": case.get("name"),
        "verdict": verdict,
        "runtime_scope": "bounded",
        "observer_mode": "observer-only",
        "diagnostic_boundary": (
            "observer-side runtime diagnostics only"
        ),
        "non_claims": [
            "not governance",
            "not certification",
            "not operational authorization",
            "not execution control",
            "not runtime enforcement"
        ]
    }


def compute_sha256(data):
    serialized = json.dumps(
        data,
        sort_keys=True
    ).encode("utf-8")

    return hashlib.sha256(serialized).hexdigest()


def write_receipt(case_name, receipt):
    ensure_receipt_dir()

    receipt_hash = compute_sha256(receipt)

    receipt["receipt_sha256"] = receipt_hash

    output_path = (
        RECEIPT_DIR /
        f"{case_name}_receipt.json"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            receipt,
            f,
            indent=2
        )

    return receipt_hash


def run_case(path):
    case = load_case(path)

    verdict = classify_case(case)

    receipt = build_receipt(
        case,
        verdict
    )

    receipt_hash = write_receipt(
        case.get("name"),
        receipt
    )

    print(
        f"{case.get('name')} -> "
        f"{verdict} / "
        f"{receipt_hash[:12]}"
    )


def main():
    print(
        "\nFailure Formation Locator v0.23\n"
    )

    print(
        "Observer-restricted runtime diagnostics\n"
    )

    print(
        "Core inspection question:\n"
    )

    print(
        "Where did interruption viability "
        "begin degrading before visible "
        "operational failure?\n"
    )

    case_files = sorted(
        CASE_DIR.glob("*.json")
    )

    if not case_files:
        print(
            "No historical cases found."
        )
        return

    for case_path in case_files:
        run_case(case_path)

    print(
        "\nRun complete.\n"
    )

    print(
        "Outputs remain observer-side "
        "runtime diagnostics only.\n"
    )

    print(
        "The simulator does not authorize, "
        "govern, certify, enforce, or "
        "control execution.\n"
    )

    print(
        "Automation dependency scope "
        "remains bounded.\n"
    )


if __name__ == "__main__":
    main()