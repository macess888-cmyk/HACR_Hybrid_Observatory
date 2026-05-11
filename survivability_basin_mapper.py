import json
from pathlib import Path

HEATMAP = Path("Outputs/survivability_heatmap_report.json")
CORRIDORS = Path("Outputs/survivability_corridor_report.json")
OUTPUT = Path("Outputs/survivability_basin_report.json")

def load(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def classify(score):
    if score >= 25:
        return "CRITICAL"
    if score >= 15:
        return "HIGH"
    if score >= 8:
        return "ELEVATED"
    return "LOW"

def main():
    heatmap = load(HEATMAP)
    corridors = load(CORRIDORS)

    heat_nodes = {
        item.get("node"): item.get("survivability_score", 0)
        for item in heatmap.get("heatmap", [])
        if item.get("node")
    }

    basin_map = {}

    for corridor in corridors.get("corridors", []):
        surfaces = corridor.get("surfaces", [])
        corridor_score = corridor.get("corridor_strength_score", 0)

        if not surfaces:
            continue

        basin_node = surfaces[-1]

        basin = basin_map.setdefault(basin_node, {
            "basin_node": basin_node,
            "incoming_corridors": [],
            "accumulated_score": heat_nodes.get(basin_node, 0),
            "convergence_depth": 0
        })

        basin["incoming_corridors"].append(corridor.get("corridor_id"))
        basin["accumulated_score"] += corridor_score
        basin["convergence_depth"] += len(surfaces)

    basins = []

    for basin in basin_map.values():
        basin["incoming_corridor_count"] = len(basin["incoming_corridors"])
        basin["status"] = classify(basin["accumulated_score"])
        basins.append(basin)

    basins.sort(key=lambda x: x["accumulated_score"], reverse=True)

    strongest = basins[0]["accumulated_score"] if basins else 0
    overall = classify(strongest)

    report = {
        "lens": "SURVIVABILITY_BASIN_MAPPER",
        "status": overall,
        "basin_count": len(basins),
        "strongest_basin_score": strongest,
        "basins": basins,
        "observer_mode": True,
        "interpretation": "Maps convergence regions where observed survivability pressure accumulates across corridors and heatmap nodes.",
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
    print(f"Inputs/survivability_basin -> {overall}")

if __name__ == "__main__":
    main()