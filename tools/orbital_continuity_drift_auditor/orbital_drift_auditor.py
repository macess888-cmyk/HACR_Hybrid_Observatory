import json
import math
import hashlib
from pathlib import Path

BASE = Path(__file__).parent
INPUT = BASE / "input" / "sample_orbit_case.json"
OUTPUT = BASE / "output" / "orbital_receipt.json"

def distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def classify(case):
    drift_km = distance(
        case["expected_position_km"],
        case["observed_position_km"]
    )

    uncertainty = case["uncertainty_margin_km"]
    fuel = case["fuel_margin_percent"]
    window = case["maneuver_window_minutes"]
    perturbations = case["perturbations"]

    active_perturbations = [
        name for name, active in perturbations.items() if active
    ]

    if drift_km <= uncertainty and fuel >= 25 and window >= 60:
        result = "PASS"
        reason = "trajectory remains localized and correction appears viable"
    elif drift_km <= uncertainty * 2 and fuel >= 10 and window >= 20:
        result = "HOLD"
        reason = "orbital continuity persists but recoverability or coupling is uncertain"
    else:
        result = "FAIL"
        reason = "trajectory continuity persists while recoverability corridor appears degraded"

    if len(active_perturbations) >= 2 and result == "PASS":
        result = "HOLD"
        reason = "hidden perturbation pressure requires uncertainty preservation"

    receipt = {
        "case_id": case["case_id"],
        "inspection_result": result,
        "reason": reason,
        "drift_km": round(drift_km, 4),
        "uncertainty_margin_km": uncertainty,
        "fuel_margin_percent": fuel,
        "maneuver_window_minutes": window,
        "active_perturbations": active_perturbations,
        "observer_scope": "bounded_orbital_observer_local"
    }

    digest_source = json.dumps(receipt, sort_keys=True).encode("utf-8")
    receipt["receipt_sha256"] = hashlib.sha256(digest_source).hexdigest()

    return receipt

def main():
    case = json.loads(INPUT.read_text(encoding="utf-8"))
    receipt = classify(case)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2), encoding="utf-8")

    print("=== ORBITAL CONTINUITY DRIFT AUDITOR ===")
    print(json.dumps(receipt, indent=2))
    print("\nDeterministic orbital continuity receipt generated.")

if __name__ == "__main__":
    main()

