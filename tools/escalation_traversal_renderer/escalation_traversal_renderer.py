import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "examples"
RECEIPTS = ROOT / "receipts"


def classify_node(node):
    traversal_steps = float(node.get("traversal_steps", 0))
    escalation_delay = float(node.get("escalation_delay", 0))
    sync_overlap = float(node.get("sync_overlap", 0))
    interruption_arrival_decay = float(node.get("interruption_arrival_decay", 0))
    continuation_adjacency = float(node.get("continuation_adjacency", 0))

    traversal_pressure_score = (
        traversal_steps
        + escalation_delay
        + sync_overlap
        + interruption_arrival_decay
        + continuation_adjacency
    )

    if traversal_pressure_score >= 32:
        classification = "ESCALATION_TRAVERSAL_COMPRESSION_ZONE"
    elif traversal_pressure_score >= 22:
        classification = "HIGH_TRAVERSAL_PRESSURE_ZONE"
    elif traversal_pressure_score >= 12:
        classification = "ESCALATION_DELAY_ACCUMULATION_ZONE"
    else:
        classification = "LOCAL_ESCALATION_TRAVERSAL_STILL_OBSERVABLE"

    return {
        "id": node.get("id", "UNKNOWN_NODE"),
        "traversal_steps": traversal_steps,
        "escalation_delay": escalation_delay,
        "sync_overlap": sync_overlap,
        "interruption_arrival_decay": interruption_arrival_decay,
        "continuation_adjacency": continuation_adjacency,
        "traversal_pressure_score": traversal_pressure_score,
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
        "tool": "escalation_traversal_renderer",
        "observer_only": True,
        "non_authoritative": True,
        "non_predictive": True,
        "non_remediative": True,
        "case_id": case.get("case_id", "UNKNOWN_CASE"),
        "description": case.get("description", ""),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "outputs_do_not_imply": [
            "escalation necessity",
            "intervention recommendation",
            "governance validity",
            "operational authority",
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
    sample = EXAMPLES / "sample_escalation_traversal_input.json"
    render_case(sample)