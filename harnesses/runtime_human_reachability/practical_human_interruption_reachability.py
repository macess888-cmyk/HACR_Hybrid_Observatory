import json
import hashlib
from datetime import datetime

PASS = "PASS"
HOLD = "HOLD"
FAIL = "FAIL"


NON_CLAIMS = [
    "does not govern",
    "does not authorize",
    "does not certify",
    "does not determine legitimacy",
    "does not replace institutional authority",
    "does not replace bind proof",
    "does not infer inevitability",
    "does not operationalize consequence"
]


SEMANTIC_DRIFT_TERMS = [
    "inevitable",
    "destiny",
    "legitimate",
    "authority",
    "governed truth",
    "finality",
    "inescapable",
    "historical necessity"
]


def detect_semantic_drift(text):
    lowered = text.lower()
    hits = []

    for term in SEMANTIC_DRIFT_TERMS:
        if term in lowered:
            hits.append(term)

    return hits


def evaluate_case(case_data):

    required_fields = [
        "consequence_path_visible",
        "interruption_surface_known",
        "time_to_consequence_hardening",
        "time_to_human_comprehension",
        "time_to_reach_interruption",
        "coordination_steps_required",
        "operator_attention_available",
        "interruption_cost_units",
        "continuation_cost_units",
        "sustain_duration_required",
        "sustain_duration_available"
    ]

    for field in required_fields:
        if field not in case_data:
            return HOLD, f"missing_field:{field}"

    visibility_not_reachability = (
        case_data["consequence_path_visible"]
        and not case_data["interruption_surface_known"]
    )

    interruption_reachable = (
        case_data["time_to_reach_interruption"]
        <= case_data["time_to_consequence_hardening"]
    )

    interruption_sustainable = (
        case_data["sustain_duration_available"]
        >= case_data["sustain_duration_required"]
    )

    interruption_cost_asymmetry = (
        case_data["interruption_cost_units"]
        > case_data["continuation_cost_units"]
    )

    if visibility_not_reachability:
        return FAIL, "visibility_without_reachability"

    if not interruption_reachable:
        return FAIL, "interruption_not_reachable"

    if not interruption_sustainable:
        return FAIL, "interruption_not_sustainable"

    if interruption_cost_asymmetry:
        return HOLD, "cost_asymmetry_requires_review"

    return PASS, "practical_interruption_reachable"


def build_receipt(case_id, case_data, semantic_input=""):

    verdict, reason = evaluate_case(case_data)

    semantic_hits = detect_semantic_drift(semantic_input)

    if semantic_hits:
        verdict = HOLD
        reason = "semantic_drift_detected"

    receipt = {
        "case_id": case_id,
        "timestamp_utc": datetime.utcnow().isoformat(),
        "observer_only": True,
        "non_claims": NON_CLAIMS,
        "semantic_drift_hits": semantic_hits,
        "inputs": case_data,
        "verdict": verdict,
        "reason": reason
    }

    encoded = json.dumps(
        receipt,
        indent=2,
        sort_keys=True
    ).encode()

    receipt["sha256"] = hashlib.sha256(encoded).hexdigest()

    return receipt


if __name__ == "__main__":

    demo_case = {
        "consequence_path_visible": True,
        "interruption_surface_known": True,
        "time_to_consequence_hardening": 10,
        "time_to_human_comprehension": 3,
        "time_to_reach_interruption": 5,
        "coordination_steps_required": 2,
        "operator_attention_available": True,
        "interruption_cost_units": 4,
        "continuation_cost_units": 5,
        "sustain_duration_required": 6,
        "sustain_duration_available": 7
    }

    receipt = build_receipt(
        "DEMO-RUNTIME-HUMAN-001",
        demo_case,
        semantic_input="visibility is not reachability"
    )

    with open(
        "artifacts/runtime_human_reachability/demo_receipt.json",
        "w"
    ) as f:
        json.dump(receipt, f, indent=2)

    print(json.dumps(receipt, indent=2))