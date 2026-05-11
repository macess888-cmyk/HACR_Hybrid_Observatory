import json
from pathlib import Path

VECTOR = Path("Outputs/survivability_vector_field_report.json")
OUTPUT = Path("Outputs/survivability_tensor_report.json")

def load(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def classify(score):
    if score >= 40:
        return "CRITICAL"
    if score >= 25:
        return "HIGH"
    if score >= 12:
        return "ELEVATED"
    return "LOW"

def main():
    data = load(VECTOR)
    vectors = data.get("vectors", [])

    interactions = {}

    for v in vectors:
        source = v.get("source")
        target = v.get("target")
        magnitude = v.get("magnitude", 0)

        for node in [source, target]:
            if not node:
                continue

            bucket = interactions.setdefault(node, {
                "node": node,
                "incoming": 0,
                "outgoing": 0,
                "interaction_magnitude": 0,
                "connected_vectors": []
            })

            bucket["interaction_magnitude"] += magnitude
            bucket["connected_vectors"].append(v.get("vector"))

            if node == source:
                bucket["outgoing"] += 1
            if node == target:
                bucket["incoming"] += 1

    tensors = []

    for node, info in interactions.items():
        coupling = info["incoming"] + info["outgoing"]
        score = info["interaction_magnitude"] + coupling

        tensors.append({
            "node": node,
            "incoming_vectors": info["incoming"],
            "outgoing_vectors": info["outgoing"],
            "directional_coupling": coupling,
            "interaction_magnitude": info["interaction_magnitude"],
            "tensor_score": score,
            "status": classify(score),
            "connected_vectors": info["connected_vectors"]
        })

    tensors.sort(key=lambda x: x["tensor_score"], reverse=True)

    strongest = tensors[0]["tensor_score"] if tensors else 0

    report = {
        "lens": "SURVIVABILITY_TENSOR_MAPPER",
        "status": classify(strongest),
        "tensor_count": len(tensors),
        "strongest_tensor_score": strongest,
        "tensors": tensors,
        "observer_mode": True,
        "interpretation": "Maps multi-directional survivability interactions across topology nodes.",
        "non_claims": [
            "Not runtime control",
            "Not prediction",
            "Not execution authorization",
            "Not production monitoring",
            "Not certification"
        ]
    }

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2))
    print(f"Inputs/survivability_tensor -> {report['status']}")

if __name__ == "__main__":
    main()