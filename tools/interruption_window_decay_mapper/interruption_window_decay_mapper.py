import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "examples"
RECEIPTS = ROOT / "receipts"


def classify_node(node):
    available_window = float(node.get("available_window", 0))
    traversal_delay = float(node.get("traversal_delay", 0))
    sync_exhaustion = float(node.get("sync_exhaustion", 0))
    dependency_compression = float(node.get("dependency_compression", 0))
    escalation_arrival_delay = float(node.get("escalation_arrival_delay", 0))

    decay_score = (
        traversal_delay
        + sync_exhaustion
        + dependency_compression
        + escalation_arrival_delay
        - available_window
    )

    if decay_score >= 20:
        classification = "INTERRUPTION_WINDOW_COLLAPSE_ZONE"
    elif decay_score >= 12:
        classification = "HIGH_WINDOW_DECAY_ZONE"
    elif decay_score >= 6:
        classification = "INTERRUPTION_WINDOW_PRESSURE_ZONE"
    else:
        classification = "LOCAL_INTERRUPTION_WINDOW_STILL_OBSERVABLE"

    return {
        "id": node.get("id", "UNKNOWN_NODE"),
        "available_window": available_window,
        "traversal_delay": traversal_delay,
        "sync_exhaustion": sync_exhaustion,
        "dependency_compression": dependency_compression,
        "escalation_arrival_delay": escalation_arrival_delay,
        "decay_score": decay_score,
        "classification": classification
    }


def stable_hash(payload):
    encoded = json.dumps(payload, sort_keys=True, indent=2).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def render_case(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        case = json.load(f)

    rendered_nodes = [classify_node(node) for node in case.get("nodes", [])]

    receipt = {
        "tool": "interruption_window_decay_mapper",
        "observer_only": True,
        "non_authoritative": True,
        "non_predictive": True,
        "non_remediative": True,
        "case_id": case.get("case_id", "UNKNOWN_CASE"),
        "description": case.get("description", ""),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "outputs_do_not_imply": [
            "interruption infeasibility",
            "intervention necessity",
            "escalation authorization",
            "governance invalidity",
            "remediation instruction",
            "predictive certainty"
        ],
        "nodes": rendered_nodes,
        "final_boundary": "UNKNOWN -> HOLD"
    }

    receipt["sha256"] = stable_hash(receipt)

    RECEIPTS.mkdir(exist_ok=True)
    output_path = RECEIPTS / f"{receipt['case_id']}_receipt.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print(f"Wrote receipt: {output_path}")
    print(f"SHA256: {receipt['sha256']}")


if __name__ == "__main__":
    sample = EXAMPLES / "sample_interruption_window_input.json"
    render_case(sample)