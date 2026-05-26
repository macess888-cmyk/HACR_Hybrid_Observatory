import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "input" / "sample_earth_case.json"
OUTPUT_PATH = ROOT / "output" / "earth_system_drift_receipt.json"


NON_CLAIMS = [
    "not environmental certification",
    "not climate-policy instruction",
    "not geological safety certification",
    "not ecological management",
    "not intervention authorization",
    "not prediction",
    "not operational command software"
]


def bounded_float(value):
    if value is None:
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    return max(0.0, min(1.0, value))


def load_case(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def hash_payload(payload):
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def classify(case):
    continuity_values = [
        bounded_float(case.get("hydrological_continuity")),
        bounded_float(case.get("atmospheric_continuity")),
        bounded_float(case.get("geological_stability_appearance"))
    ]

    regeneration_values = [
        bounded_float(case.get("soil_viability")),
        bounded_float(case.get("groundwater_recharge_viability")),
        bounded_float(case.get("biome_coupling")),
        bounded_float(case.get("regeneration_corridor_evidence"))
    ]

    stress_values = [
        bounded_float(case.get("thermal_accumulation")),
        bounded_float(case.get("chemical_accumulation")),
        bounded_float(case.get("erosion_pressure"))
    ]

    if any(v is None for v in continuity_values + regeneration_values + stress_values):
        return "HOLD", "UNKNOWN -> HOLD; insufficient bounded present-state evidence."

    continuity_score = sum(continuity_values) / len(continuity_values)
    regeneration_score = sum(regeneration_values) / len(regeneration_values)
    stress_score = sum(stress_values) / len(stress_values)
    divergence = continuity_score - regeneration_score

    if continuity_score >= 0.65 and regeneration_score < 0.45:
        return "FAIL", "Earth-system continuity persists while regeneration corridor is degraded."

    if divergence >= 0.25 and stress_score >= 0.50:
        return "SHADOW", "Hidden Earth-system drift pressure detected beneath continuity persistence."

    if continuity_score < 0.45 and regeneration_score >= 0.55:
        return "REVERSE", "Apparent discontinuity may not imply loss of regeneration viability under supplied evidence."

    if continuity_score >= 0.60 and regeneration_score >= 0.60 and stress_score < 0.50:
        return "PASS", "Earth-system continuity and regeneration viability remain coupled under supplied bounded evidence."

    return "HOLD", "UNKNOWN -> HOLD; evidence does not support a stronger observer-only classification."


def build_receipt(case):
    classification, reason = classify(case)

    receipt = {
        "tool": "earth_system_drift_observatory",
        "version": "v1.5",
        "observer_mode": "earth_system_drift_topology",
        "claim_scope": "diagnostic_only",
        "authority": "none",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "case_id": case.get("case_id"),
        "classification": classification,
        "reason": reason,
        "core_reduction": "environmental observability is not proof of regeneration viability",
        "input_snapshot": case,
        "non_claims": NON_CLAIMS
    }

    receipt["receipt_sha256"] = hash_payload(receipt)
    return receipt


def main():
    case = load_case(INPUT_PATH)
    receipt = build_receipt(case)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, sort_keys=True)

    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()