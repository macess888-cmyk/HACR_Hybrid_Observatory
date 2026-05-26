import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "input" / "sample_bridge_case.json"
OUTPUT_PATH = ROOT / "output" / "hybrid_bridge_receipt.json"


NON_CLAIMS = [
    "not expansion authority",
    "not governance authority",
    "not domain certification",
    "not operational command",
    "not intervention authorization",
    "not prediction",
    "not truth determination",
    "not human behavior inspection authority"
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
    need_values = [
        bounded_float(case.get("topology_gap_severity")),
        bounded_float(case.get("reproducibility_benefit")),
        bounded_float(case.get("ambiguity_reduction"))
    ]

    containment_values = [
        bounded_float(case.get("observer_only_fit"))
    ]

    risk_values = [
        bounded_float(case.get("authority_drift_risk")),
        bounded_float(case.get("human_behavior_risk")),
        bounded_float(case.get("certification_risk")),
        bounded_float(case.get("prediction_risk")),
        bounded_float(case.get("governance_risk"))
    ]

    coverage_value = bounded_float(case.get("existing_layer_coverage"))

    all_values = need_values + containment_values + risk_values + [coverage_value]

    if any(v is None for v in all_values):
        return "HOLD", "UNKNOWN -> HOLD; insufficient bounded bridge evidence."

    need_score = sum(need_values) / len(need_values)
    containment_score = sum(containment_values) / len(containment_values)
    risk_score = sum(risk_values) / len(risk_values)

    if max(risk_values) >= 0.75:
        return "STOP", "Proposed bridge crosses prohibited or high-risk authority boundary."

    if risk_score >= 0.50:
        return "FAIL", "Proposed bridge introduces authority drift or containment risk."

    if coverage_value >= 0.70 and need_score < 0.65:
        return "REVERSE", "Proposed bridge may be unnecessary; existing layers appear to cover the topology."

    if need_score >= 0.65 and containment_score >= 0.75 and risk_score < 0.35:
        return "PASS", "Bridge appears bounded, useful, observer-only, and containment-preserving under supplied evidence."

    if need_score >= 0.65 and risk_score < 0.50:
        return "SHADOW", "Bridge need detected, but hidden dependency or containment uncertainty remains."

    return "HOLD", "UNKNOWN -> HOLD; evidence does not support a stronger bridge classification."


def build_receipt(case):
    classification, reason = classify(case)

    receipt = {
        "tool": "hybrid_bridge_finder",
        "version": "v1.8",
        "observer_mode": "hybrid_bridge_finding_topology",
        "claim_scope": "diagnostic_only",
        "authority": "none",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "case_id": case.get("case_id"),
        "source_layer": case.get("source_layer"),
        "target_layer": case.get("target_layer"),
        "proposed_bridge": case.get("proposed_bridge"),
        "classification": classification,
        "reason": reason,
        "core_reduction": "bridge discovery is diagnostic, not expansion authority",
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