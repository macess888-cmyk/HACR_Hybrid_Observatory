import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "examples"
RECEIPTS = ROOT / "receipts"


def classify_node(node):
    continuation = float(node.get("continuation_pressure", 0))
    interruption = float(node.get("interruption_constructability", 0))
    sync = float(node.get("synchronization_load", 0))

    hardening_score = continuation + sync - interruption

    if hardening_score >= 12:
        classification = "HARDENED_CONTINUATION_ZONE"
    elif hardening_score >= 7:
        classification = "CONSTRUCTABILITY_DECAY_ZONE"
    elif hardening_score >= 3:
        classification = "SYNCHRONIZATION_PRESSURE_ZONE"
    else:
        classification = "LOCAL_INTERRUPTION_STILL_CONSTRUCTABLE"

    return {
        "id": node.get("id", "UNKNOWN_NODE"),
        "continuation_pressure": continuation,
        "interruption_constructability": interruption,
        "synchronization_load": sync,
        "hardening_score": hardening_score,
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
        "tool": "continuation_hardening_renderer",
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
    sample = EXAMPLES / "sample_continuation_hardening_input.json"
    render_case(sample)