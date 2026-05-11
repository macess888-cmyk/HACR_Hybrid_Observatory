import json
from pathlib import Path

OUTPUT = Path("Outputs/survivability_heatmap_report.json")

SOURCES = [
    Path("Outputs/survivability_corridor_report.json"),
    Path("Outputs/topology_pressure_report.json"),
    Path("Outputs/latent_path_report.json"),
    Path("Outputs/replay_vector_report.json"),
    Path("Outputs/authority_surface_report.json"),
    Path("Outputs/descendant_effect_report.json"),
    Path("Outputs/distributed_reconstruction_report.json")
]

WEIGHTS = {
    "LOW": 1,
    "ELEVATED": 3,
    "SHADOW": 4,
    "UNSTABLE": 5,
    "HIGH": 7,
    "FAIL": 8,
    "CRITICAL": 10
}

def add_score(scores, node, amount):
    if not node:
        return
    scores[node] = scores.get(node, 0) + amount

def classify(score):
    if score >= 15:
        return "CRITICAL"
    if score >= 10:
        return "HIGH"
    if score >= 5:
        return "ELEVATED"
    return "LOW"

def load_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def main():
    scores = {}

    for path in SOURCES:
        data = load_json(path)

        status = data.get("status") or data.get("overall_status") or "LOW"
        base_weight = WEIGHTS.get(status, 1)

        for corridor in data.get("corridors", []):
            corridor_weight = corridor.get("corridor_strength_score", base_weight)
            for surface in corridor.get("surfaces", []):
                add_score(scores, surface, corridor_weight)

        for item_key in [
            "latent_paths",
            "replay_vectors",
            "surviving_authority_surfaces",
            "descendant_effects",
            "reconstruction_surfaces",
            "pressure_nodes",
            "hotspots"
        ]:
            for item in data.get(item_key, []):
                node = (
                    item.get("surface_id")
                    or item.get("node")
                    or item.get("target")
                    or item.get("path")
                    or item.get("effect_id")
                )
                add_score(scores, node, base_weight)

    heatmap = []

    for node, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        heatmap.append({
            "node": node,
            "survivability_score": score,
            "status": classify(score)
        })

    overall_score = heatmap[0]["survivability_score"] if heatmap else 0
    overall_status = classify(overall_score)

    report = {
        "generator": "SURVIVABILITY_HEATMAP",
        "status": overall_status,
        "node_count": len(heatmap),
        "highest_node_score": overall_score,
        "heatmap": heatmap,
        "observer_mode": True,
        "interpretation": "Maps observed survivability concentration across topology nodes and surfaces.",
        "non_claims": [
            "Not runtime monitoring",
            "Not execution control",
            "Not proof of hidden execution",
            "Not production safety guarantee",
            "Not certification"
        ]
    }

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2))
    print(f"Inputs/survivability_heatmap -> {overall_status}")

if __name__ == "__main__":
    main()