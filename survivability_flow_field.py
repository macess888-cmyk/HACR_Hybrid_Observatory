import json
from pathlib import Path

CORRIDORS = Path("Outputs/survivability_corridor_report.json")
HEATMAP = Path("Outputs/survivability_heatmap_report.json")
OUTPUT = Path("Outputs/survivability_flow_field_report.json")

def load(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def classify(score):
    if score >= 20:
        return "CRITICAL"
    if score >= 12:
        return "HIGH"
    if score >= 6:
        return "ELEVATED"
    return "LOW"

def main():
    corridors = load(CORRIDORS)
    heatmap = load(HEATMAP)

    node_scores = {
        h["node"]: h["survivability_score"]
        for h in heatmap.get("heatmap", [])
    }

    flows = []

    for corridor in corridors.get("corridors", []):
        surfaces = corridor.get("surfaces", [])

        for i in range(len(surfaces) - 1):
            source = surfaces[i]
            target = surfaces[i + 1]

            source_score = node_scores.get(source, 1)
            target_score = node_scores.get(target, 1)

            flow_strength = source_score + target_score

            flows.append({
                "source": source,
                "target": target,
                "flow_strength": flow_strength,
                "status": classify(flow_strength)
            })

    strongest = max([f["flow_strength"] for f in flows], default=0)

    report = {
        "lens": "SURVIVABILITY_FLOW_FIELD",
        "status": classify(strongest),
        "flow_count": len(flows),
        "strongest_flow": strongest,
        "flows": flows,
        "observer_mode": True,
        "interpretation": "Maps directional survivability pressure movement across connected topology surfaces.",
        "non_claims": [
            "Not runtime orchestration",
            "Not execution control",
            "Not prediction",
            "Not production monitoring",
            "Not certification"
        ]
    }

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2))
    print(f"Inputs/survivability_flow_field -> {report['status']}")

if __name__ == "__main__":
    main()