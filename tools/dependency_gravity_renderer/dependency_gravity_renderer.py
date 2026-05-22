import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "examples"
RECEIPTS = ROOT / "receipts"


def classify_node(node):
    dependency_count = float(node.get("dependency_count", 0))
    dependency_weight = float(node.get("dependency_weight", 0))
    sync_density = float(node.get("sync_density", 0))
    traversal_drag = float(node.get("traversal_drag", 0))
    interruption_locality = float(node.get("interruption_locality", 0))

    gravity_score = (
        dependency_count
        + dependency_weight
        + sync_density
        + traversal_drag
        - interruption_locality
    )

    if gravity_score >= 28:
        classification = "DEPENDENCY_GRAVITY_CONCENTRATION_ZONE"
    elif gravity_score >= 18:
        classification = "HIGH_DEPENDENCY_TRAVERSAL_PRESSURE_ZONE"
    elif gravity_score >= 9:
        classification = "DEPENDENCY_COMPRESSION_PRESSURE_ZONE"
    else:
        classification = "LOCAL_DEPENDENCY_PRESSURE_STILL_TRAVERSABLE"

    return {
        "id": node.get("id", "UNKNOWN_NODE"),
        "dependency_count": dependency_count,
        "dependency_weight": dependency_weight,
        "sync_density": sync_density,
        "traversal_drag": traversal_drag,
        "interruption_locality": interruption_locality,
        "gravity_score": gravity_score,
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
        "tool": "dependency_gravity_renderer",
        "observer_only": True,
        "non_authoritative": True,
        "non_predictive": True,
        "non_remediative": True,
        "case_id": case.get("case_id", "UNKNOWN_CASE"),
        "description": case.get("description", ""),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "outputs_do_not_imply": [
            "dependency optimization",
            "intervention recommendation",
            "escalation authorization",
            "governance validity",
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
    sample = EXAMPLES / "sample_dependency_gravity_input.json"
    render_case(sample)