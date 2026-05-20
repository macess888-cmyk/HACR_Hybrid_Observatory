import json
import hashlib
from pathlib import Path

CASE_FILE = Path("demo_case_green_surface_dead_recovery.json")
OUTPUT_FILE = Path("actual_output.json")

REQUIRED_TIMING_FIELDS = [
    "detection_delay",
    "explanation_delay",
    "escalation_delay",
    "reviewer_traversal_time",
    "interruption_execution_time",
    "recovery_routing_time",
    "fragmentation_penalty",
    "synchronization_penalty",
    "consequence_hardening_window",
]

def classify(case):
    timing = case.get("timing_minutes", {})
    missing = [field for field in REQUIRED_TIMING_FIELDS if field not in timing]

    if missing:
        return {
            "classification": "HOLD",
            "reason": "Required timing fields missing",
            "missing_fields": missing,
            "reduction": "UNKNOWN -> HOLD"
        }

    effective_recovery_time = sum(
        timing[field] for field in REQUIRED_TIMING_FIELDS
        if field != "consequence_hardening_window"
    )

    hardening_window = timing["consequence_hardening_window"]

    surface = case.get("surface_signals", {})
    surface_green = all(surface.values()) if surface else False

    if effective_recovery_time <= hardening_window:
        classification = "RECOVERABLE"
    else:
        classification = "RECOVERY_EXHAUSTED"

    result = {
        "case_id": case.get("case_id", "unknown"),
        "surface_continuity": "GREEN" if surface_green else "PARTIAL_OR_UNKNOWN",
        "effective_recovery_time_minutes": effective_recovery_time,
        "consequence_hardening_window_minutes": hardening_window,
        "classification": classification,
        "reduction": "Recovery visibility is not recovery viability"
    }

    receipt_source = json.dumps(result, sort_keys=True).encode("utf-8")
    result["sha256_receipt"] = hashlib.sha256(receipt_source).hexdigest()

    return result

def main():
    case = json.loads(CASE_FILE.read_text(encoding="utf-8"))
    result = classify(case)

    OUTPUT_FILE.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8"
    )

    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()