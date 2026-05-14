# Failure Formation Locator v0.17
# Observer-only diagnostic simulator
# Purpose: load case files, export deterministic receipts, and attach receipt SHA256 integrity hashes

import hashlib
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
CASES_DIR = BASE_DIR / "cases"
RECEIPTS_DIR = BASE_DIR / "receipts"

REQUIRED_FIELDS = [
    "name",
    "declared_intent",
    "validity_conditions",
    "drift_point",
    "detection_loss",
    "continuation_pressure",
    "interruption_viability",
    "failure_locator",
]


def validate_case(case):
    missing = [field for field in REQUIRED_FIELDS if field not in case]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"

    for field in ["validity_conditions", "continuation_pressure", "failure_locator"]:
        if not isinstance(case[field], list):
            return False, f"Field must be a list: {field}"

    return True, "valid"


def load_cases():
    cases = []

    if not CASES_DIR.exists():
        print(f"HOLD: cases directory not found: {CASES_DIR}")
        return cases

    for path in sorted(CASES_DIR.glob("*.json")):
        try:
            with open(path, "r", encoding="utf-8") as file:
                case = json.load(file)

            valid, message = validate_case(case)
            if not valid:
                print(f"HOLD: {path.name} invalid — {message}")
                continue

            cases.append(case)

        except json.JSONDecodeError as error:
            print(f"HOLD: {path.name} invalid JSON — {error}")
        except OSError as error:
            print(f"HOLD: could not read {path.name} — {error}")

    return cases


def classify(case):
    unresolved = []
    fail_signals = []

    interruption = case["interruption_viability"].lower().strip()

    degraded_terms = [
        "degraded",
        "collapsed",
        "impaired",
        "reduced",
        "weakened",
    ]

    low_viability_terms = [
        "low",
        "structurally difficult",
        "not viable",
        "non-viable",
    ]

    unresolved_interruption_states = {
        "unknown",
        "unresolved",
        "unclear",
        "not established",
        "cannot be established",
    }

    if any(term in interruption for term in degraded_terms):
        fail_signals.append("interruption viability degraded")

    if any(term in interruption for term in low_viability_terms):
        fail_signals.append("stopping became structurally difficult")

    if interruption in unresolved_interruption_states:
        unresolved.append("interruption viability unresolved")

    if case["detection_loss"]:
        fail_signals.append("detection loss or normalization present")
    else:
        unresolved.append("detection status unresolved")

    if case["continuation_pressure"]:
        fail_signals.append("continuation pressure present")
    else:
        unresolved.append("continuation pressure unresolved")

    if fail_signals:
        verdict = "FAIL"
    elif unresolved:
        verdict = "HOLD"
    else:
        verdict = "PASS"

    return verdict, fail_signals, unresolved


def build_receipt(case, verdict, signals, unresolved):
    return {
        "tool": "Failure Formation Locator",
        "version": "v0.17",
        "observer_only": True,
        "authority_claim": False,
        "certification_claim": False,
        "blame_determination": False,
        "case": case["name"],
        "verdict": verdict,
        "declared_intent": case["declared_intent"],
        "drift_point": case["drift_point"],
        "interruption_viability": case["interruption_viability"],
        "diagnostic_signals": signals,
        "unresolved_signals": unresolved,
        "failure_locator": case["failure_locator"],
        "core_question": "Where did stopping stop being viable before visible failure?",
    }


def canonical_json(data):
    return json.dumps(data, indent=2, sort_keys=True)


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_receipt(receipt):
    RECEIPTS_DIR.mkdir(exist_ok=True)

    receipt_without_hash = dict(receipt)
    canonical_without_hash = canonical_json(receipt_without_hash)
    receipt_hash = sha256_text(canonical_without_hash)

    receipt_with_hash = dict(receipt_without_hash)
    receipt_with_hash["receipt_sha256"] = receipt_hash

    path = RECEIPTS_DIR / f"{receipt['case']}_receipt.json"

    with open(path, "w", encoding="utf-8") as file:
        file.write(canonical_json(receipt_with_hash))
        file.write("\n")

    return path, receipt_hash


def print_case(case):
    verdict, signals, unresolved = classify(case)
    receipt = build_receipt(case, verdict, signals, unresolved)
    receipt_path, receipt_hash = write_receipt(receipt)

    print("=" * 72)
    print(f"CASE: {case['name']}")
    print(f"VERDICT: {verdict}")
    print("-" * 72)
    print(f"Declared intent: {case['declared_intent']}")

    print("\nValidity conditions:")
    for item in case["validity_conditions"]:
        print(f"  - {item}")

    print(f"\nDrift point: {case['drift_point']}")
    print(f"Detection loss: {case['detection_loss']}")

    print("\nContinuation pressure:")
    for item in case["continuation_pressure"]:
        print(f"  - {item}")

    print(f"\nInterruption viability: {case['interruption_viability']}")

    print("\nFailure locator:")
    for item in case["failure_locator"]:
        print(f"  - {item}")

    print("\nDiagnostic signals:")
    if signals:
        for item in signals:
            print(f"  - {item}")
    else:
        print("  - none")

    if unresolved:
        print("\nUnresolved signals:")
        for item in unresolved:
            print(f"  - {item}")

    print(f"\nReceipt written: {receipt_path}")
    print(f"Receipt SHA256: {receipt_hash}")
    print("\nCore question:")
    print("  Where did stopping stop being viable before visible failure?")
    print("=" * 72)
    print()


def main():
    print("\nFailure Formation Locator v0.17")
    print("Observer-only diagnostic simulator")
    print("No authority. No certification. No blame determination.")
    print("External JSON case loader enabled.")
    print("Deterministic receipt export enabled.")
    print("Receipt SHA256 integrity enabled.")
    print("Interruption viability parser tightened.\n")

    cases = load_cases()

    if not cases:
        print("HOLD: no valid case files loaded.")
        return

    for case in cases:
        print_case(case)

    print(f"Run complete: {len(cases)} case(s) loaded.")


if __name__ == "__main__":
    main()