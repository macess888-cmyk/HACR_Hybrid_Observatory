import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "input" / "sample_marine_case.json"
OUTPUT_PATH = ROOT / "output" / "marine_recoverability_receipt.json"


NON_CLAIMS = [
    "not ecological certification",
    "not conservation authority",
    "not fisheries guidance",
    "not climate-policy instruction",
    "not species-risk classification",
    "not intervention authorization",
    "not prediction",
    "not mission control"
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
        bounded_float(case.get("productivity_continuity")),
        bounded_float(case.get("species_presence"))
    ]

    recoverability_values = [
        bounded_float(case.get("recruitment_viability")),
        bounded_float(case.get("habitat_condition")),
        bounded_float(case.get("trophic_coupling")),
        bounded_float(case.get("recovery_corridor_evidence"))
    ]

    stress_values = [
        bounded_float(case.get("temperature_anomaly")) / 5.0 if case.get("temperature_anomaly") is not None else None,
        bounded_float(case.get("oxygen_stress")),
        bounded_float(case.get("acidification_stress")),
        bounded_float(case.get("stratification_stress")),
        bounded_float(case.get("migration_displacement"))
    ]

    if any(v is None for v in continuity_values + recoverability_values + stress_values):
        return "HOLD", "UNKNOWN -> HOLD; insufficient bounded present-state evidence."

    continuity_score = sum(continuity_values) / len(continuity_values)
    recoverability_score = sum(recoverability_values) / len(recoverability_values)
    stress_score = sum(stress_values) / len(stress_values)
    divergence = continuity_score - recoverability_score

    if continuity_score >= 0.65 and recoverability_score < 0.45:
        return "FAIL", "Continuity persists while biological recoverability corridor is degraded."

    if divergence >= 0.25 and stress_score >= 0.50:
        return "SHADOW", "Hidden degradation pressure detected beneath continuity persistence."

    if continuity_score < 0.45 and recoverability_score >= 0.55:
        return "REVERSE", "Apparent discontinuity may not imply loss of recoverability under supplied evidence."

    if continuity_score >= 0.60 and recoverability_score >= 0.60 and stress_score < 0.50:
        return "PASS", "Continuity and recoverability remain coupled under supplied bounded evidence."

    return "HOLD", "UNKNOWN -> HOLD; evidence does not support a stronger observer-only classification."


def build_receipt(case):
    classification, reason = classify(case)

    receipt = {
        "tool": "marine_recoverability_observatory",
        "version": "v1.4",
        "observer_mode": "marine_continuity_recoverability_topology",
        "claim_scope": "diagnostic_only",
        "authority": "none",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "case_id": case.get("case_id"),
        "classification": classification,
        "reason": reason,
        "core_reduction": "continued ocean function is not proof of preserved ecological recovery",
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