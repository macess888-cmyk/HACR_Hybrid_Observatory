import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "examples"
RECEIPTS = ROOT / "receipts"


def classify_node(node):
    sync_load = float(node.get("sync_load", 0))
    coordination_density = float(node.get("coordination_density", 0))
    dependency_weight = float(node.get("dependency_weight", 0))
    interruption_window = float(node.get("interruption_window", 0))

    pressure_score = sync_load + coordination_density + dependency_weight - interruption_window

    if pressure_score >= 20:
        classification = "SYNCHRONIZATION_EXHAUSTION_ZONE"
    elif pressure_score >= 14:
        classification = "HIGH_COORDINATION_PRESSURE_ZONE"
    elif pressure_score >= 8:
        classification = "INTERRUPTION_WINDOW_DECAY_ZONE"
    else:
        classification = "LOCAL_SYNCHRONIZATION_STILL_TRAVERSABLE"

    return {
        "id": node.get("id", "UNKNOWN_NODE"),
        "sync_load": sync_load,
        "coordination_density": coordination_density,
        "dependency_weight": dependency_weight,
        "interruption_window": interruption_window,
        "pressure_score": pressure_score,
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
        "tool": "synchronization_pressure_mapper",
        "observer_only": True,
        "non_authoritative": True,
        "non_predictive": True,
        "non_remediative": True,
        "case_id": case.get("case_id", "UNKNOWN_CASE"),
        "description": case.get("description", ""),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "outputs_do_not_imply": [
            "interruption feasibility",
            "governance validity",
            "escalation effectiveness",
            "remediation instruction",
            "operational authority",
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
    sample = EXAMPLES / "sample_sync_pressure_input.json"
    render_case(sample)