import json
import hashlib
from pathlib import Path

CASES_DIR = Path("cases")
OUTPUTS_DIR = Path("outputs")
OUTPUTS_DIR.mkdir(exist_ok=True)

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
        result = {
            "case_id": case.get("case_id", "unknown"),
            "title": case.get("title", "Unknown Case"),
            "classification": "HOLD",
            "reason": "Required timing fields missing",
            "missing_fields": missing,
            "reduction": "UNKNOWN -> HOLD",
            "layers": case.get("layers", {})
        }
    else:
        effective_recovery_time = sum(
            timing[field] for field in REQUIRED_TIMING_FIELDS
            if field != "consequence_hardening_window"
        )

        hardening_window = timing["consequence_hardening_window"]

        surface = case.get("surface_signals", {})
        surface_green = all(surface.values()) if surface else False

        if effective_recovery_time <= hardening_window:
            classification = "RECOVERABLE"
        elif effective_recovery_time <= hardening_window * 1.25:
            classification = "PARTIAL_RECOVERY"
        else:
            classification = "RECOVERY_EXHAUSTED"

        result = {
            "case_id": case.get("case_id", "unknown"),
            "title": case.get("title", "Unknown Case"),
            "surface_continuity": "GREEN" if surface_green else "PARTIAL_OR_UNKNOWN",
            "effective_recovery_time_minutes": effective_recovery_time,
            "consequence_hardening_window_minutes": hardening_window,
            "classification": classification,
            "reduction": case.get("reduction", "Recovery visibility is not recovery viability."),
            "layers": case.get("layers", {})
        }

    receipt_source = json.dumps(result, sort_keys=True).encode("utf-8")
    result["sha256_receipt"] = hashlib.sha256(receipt_source).hexdigest()
    return result

def main():
    case_files = sorted(CASES_DIR.glob("*.json"))

    for case_file in case_files:
        case = json.loads(case_file.read_text(encoding="utf-8"))
        result = classify(case)

        output_file = OUTPUTS_DIR / f"{result['case_id']}_output.json"
        output_file.write_text(
            json.dumps(result, indent=2, sort_keys=True),
            encoding="utf-8"
        )

        print(f"Wrote {output_file}")

if __name__ == "__main__":
    main()