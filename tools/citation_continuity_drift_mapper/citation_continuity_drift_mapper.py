import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "input" / "sample_citation_case.json"
OUTPUT_PATH = ROOT / "output" / "citation_continuity_drift_receipt.json"


NON_CLAIMS = [
    "not truth determination",
    "not expert legitimacy assignment",
    "not research ranking",
    "not institutional authority",
    "not scientific certification",
    "not technical certification",
    "not policy instruction",
    "not prediction"
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
        bounded_float(case.get("citation_density")),
        bounded_float(case.get("publication_velocity")),
        bounded_float(case.get("field_adoption"))
    ]

    recoverability_values = [
        bounded_float(case.get("evidence_grounding")),
        bounded_float(case.get("source_recoverability")),
        bounded_float(case.get("dataset_lineage_clarity")),
        bounded_float(case.get("replication_locality")),
        bounded_float(case.get("correction_corridor_evidence"))
    ]

    pressure_values = [
        bounded_float(case.get("benchmark_inheritance_pressure")),
        bounded_float(case.get("normalization_pressure"))
    ]

    if any(v is None for v in continuity_values + recoverability_values + pressure_values):
        return "HOLD", "UNKNOWN -> HOLD; insufficient bounded present-state evidence."

    continuity_score = sum(continuity_values) / len(continuity_values)
    recoverability_score = sum(recoverability_values) / len(recoverability_values)
    pressure_score = sum(pressure_values) / len(pressure_values)
    divergence = continuity_score - recoverability_score

    if continuity_score >= 0.65 and recoverability_score < 0.45:
        return "FAIL", "Citation continuity persists while evidence recoverability corridor is degraded."

    if divergence >= 0.25 and pressure_score >= 0.50:
        return "SHADOW", "Hidden citation or benchmark inheritance pressure detected beneath field continuity."

    if continuity_score < 0.45 and recoverability_score >= 0.55:
        return "REVERSE", "Apparent citation discontinuity may not imply loss of evidence recoverability under supplied evidence."

    if continuity_score >= 0.60 and recoverability_score >= 0.60 and pressure_score < 0.50:
        return "PASS", "Citation continuity and evidence recoverability remain coupled under supplied bounded evidence."

    return "HOLD", "UNKNOWN -> HOLD; evidence does not support a stronger observer-only classification."


def build_receipt(case):
    classification, reason = classify(case)

    receipt = {
        "tool": "citation_continuity_drift_mapper",
        "version": "v1.7",
        "observer_mode": "citation_continuity_drift_topology",
        "claim_scope": "diagnostic_only",
        "authority": "none",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "case_id": case.get("case_id"),
        "classification": classification,
        "reason": reason,
        "core_reduction": "citation continuity is not proof of evidence continuity",
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