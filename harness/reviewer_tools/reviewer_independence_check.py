import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASES_DIR = ROOT / "harness" / "cases"

VALID_STATES = {"PASS", "HOLD", "FAIL"}


def minimal_view(case):
    hidden_keys = {
        "case",
        "description",
        "expected_state",
        "incorrect_assertion"
    }

    return {
        key: value
        for key, value in case.items()
        if key not in hidden_keys
    }


def load_cases():
    cases = []
    for path in sorted(CASES_DIR.glob("*.json")):
        raw = path.read_text(encoding="utf-8")
        case = json.loads(raw)
        cases.append((path.name, case))
    return cases


def main():
    cases = load_cases()

    if not cases:
        print("No cases found.")
        return

    random.shuffle(cases)

    print("HACR Reviewer Independence Check")
    print("--------------------------------")
    print("Purpose:")
    print("Classify cases using only minimal runtime facts.")
    print("Do not rely on case names, descriptions, or semantic history.")
    print("")
    print("Allowed classifications: PASS, HOLD, FAIL")
    print("--------------------------------")

    results = []

    for index, (filename, case) in enumerate(cases, start=1):
        view = minimal_view(case)

        print("")
        print(f"Case {index} of {len(cases)}")
        print(json.dumps(view, indent=2, sort_keys=True))

        answer = input("Your classification (PASS/HOLD/FAIL): ").strip().upper()

        while answer not in VALID_STATES:
            answer = input("Please enter PASS, HOLD, or FAIL: ").strip().upper()

        expected = case.get("expected_state")
        matched = answer == expected

        results.append({
            "case_file": filename,
            "expected_state": expected,
            "reviewer_state": answer,
            "matched_expected": matched,
        })

        print("Result:", "MATCH" if matched else "MISMATCH")
        print(f"Expected diagnostic state: {expected}")

    print("")
    print("--------------------------------")
    print("Reviewer Independence Summary")
    print("--------------------------------")

    matches = sum(1 for r in results if r["matched_expected"])
    total = len(results)

    print(f"Matched expected: {matches}/{total}")

    false_pass = [
        r for r in results
        if r["reviewer_state"] == "PASS" and r["expected_state"] != "PASS"
    ]

    if false_pass:
        print("")
        print("False PASS risk detected:")
        for item in false_pass:
            print(f'- {item["case_file"]}: expected={item["expected_state"]}, reviewer=PASS')
    else:
        print("")
        print("No false PASS detected.")

    print("")
    print("Interpretation:")
    print("If reviewers need descriptions, insider terminology, or architecture history to classify cases, route to HOLD.")
    print("If PASS appears under uncertainty, hidden continuation, replay ambiguity, or degraded present-state attachment, treat as false PASS risk.")


if __name__ == "__main__":
    main()