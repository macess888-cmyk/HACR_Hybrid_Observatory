import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "input" / "sample_reproducibility_case.json"
OUTPUT_PATH = ROOT / "output" / "reproducibility_corridor_receipt.json"


NON_CLAIMS = [
    "not truth determination",
    "not scientific certification",
    "not technical certification",
    "not research ranking",
    "not policy instruction",
    "not expert legitimacy assignment",
    "not prediction",
    "not governance authority"
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
        bounded_float(case.get("publication_continuity")),
        bounded_float(case.get("citation_continuity")),
        bounded_float(case.get("technical_adoption"))
    ]

    recoverability_values = [
        bounded_float(case.get("source_availability")),
        bounded_float(case.get("dataset_availability")),
        bounded_float(case.get("method_specificity")),
        bounded_float(case.get("environment_reproducibility")),
        bounded_float(case.get("toolchain_recoverability")),
        bounded_float(case.get("independent_replication")),
        bounded_float(case.get("reproducibility_corridor_evidence"))
    ]

    pressure_values = [
        bounded_float(case.get("version_drift"))
    ]

    if any(v is None for v in continuity_values + recoverability_values + pressure_values):
        return "HOLD", "UNKNOWN -> HOLD; insufficient bounded present-state evidence."

    continuity_score = sum(continuity_values) / len(continuity_values)
    recoverability_score = sum(recoverability_values) / len(recoverability_values)
    pressure_score = sum(pressure_values) / len(pressure_values)
    divergence = continuity_score - recoverability_score

    if continuity_score >= 0.65 and recoverability_score < 0.45:
        return "FAIL", "Technical continuity persists while reproducibility recoverability corridor is degraded."

    if divergence >= 0.25 and pressure_score >= 0.50:
        return "SHADOW", "Hidden reproducibility pressure detected beneath technical continuity."

    if continuity_score < 0.45 and recoverability_score >= 0.55:
        return "REVERSE", "Apparent technical discontinuity may not imply loss of reproducibility under supplied evidence."

    if continuity_score >= 0.60 and recoverability_score >= 0.60 and pressure_score < 0.50:
        return "PASS", "Technical continuity and reproducibility recoverability remain coupled under supplied bounded evidence."

    return "HOLD", "UNKNOWN -> HOLD; evidence does not support a stronger observer-only classification."


def build_receipt(case):
    classification, reason = classify(case)

    receipt = {
        "tool": "reproducibility_corridor_auditor",
        "version": "v1.7",
        "observer_mode": "reproducibility_corridor_topology",
        "claim_scope": "diagnostic_only",
        "authority": "none",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "case_id": case.get("case_id"),
        "classification": classification,
        "reason": reason,
        "core_reduction": "technical continuity is not proof of epistemic recoverability",
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