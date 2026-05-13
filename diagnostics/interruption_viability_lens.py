import json
from pathlib import Path

CASE_DIR = Path("diagnostics/cases")


def classify(case):
    interruption_available = case.get("interruption_available")
    reconstruction_required = case.get("reconstruction_required")
    dependency_pressure = case.get("continuation_dependency_pressure")
    independent_refusal_path = case.get("independent_refusal_path")

    if reconstruction_required is True:
        return "FAIL"

    if interruption_available == "unknown":
        return "HOLD"

    if dependency_pressure == "unknown":
        return "HOLD"

    if independent_refusal_path == "unknown":
        return "HOLD"

    if interruption_available is True and independent_refusal_path is True and dependency_pressure in ["low", "bounded"]:
        return "PASS"

    if dependency_pressure in ["high", "accumulating"]:
        return "HOLD"

    return "HOLD"


def run_case(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    verdict = classify(data)

    return {
        "case": data.get("name"),
        "question": data.get("question"),
        "verdict": verdict,
        "notes": data.get("notes", "")
    }


def main():
    results = []

    for path in sorted(CASE_DIR.glob("*.json")):
        results.append(run_case(path))

    for result in results:
        print(f"{result['case']} -> {result['verdict']}")
        if result["notes"]:
            print(f"  {result['notes']}")

    pass_count = sum(1 for r in results if r["verdict"] == "PASS")
    hold_count = sum(1 for r in results if r["verdict"] == "HOLD")
    fail_count = sum(1 for r in results if r["verdict"] == "FAIL")

    print()
    print("Interruption viability diagnostic lens complete.")
    print(f"PASS: {pass_count}")
    print(f"HOLD: {hold_count}")
    print(f"FAIL: {fail_count}")


if __name__ == "__main__":
    main()