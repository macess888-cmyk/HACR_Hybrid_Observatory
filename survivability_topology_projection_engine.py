import json
from pathlib import Path

HEATMAP = Path("Outputs/survivability_heatmap_report.json")
VECTOR = Path("Outputs/survivability_vector_field_report.json")
TENSOR = Path("Outputs/survivability_tensor_report.json")
BASIN = Path("Outputs/survivability_basin_report.json")
OUTPUT = Path("Outputs/survivability_topology_projection_report.json")

def load(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def main():
    heatmap = load(HEATMAP)
    vector = load(VECTOR)
    tensor = load(TENSOR)
    basin = load(BASIN)

    nodes = []
    edges = []
    overlays = []

    for item in heatmap.get("heatmap", []):
        nodes.append({
            "node": item.get("node"),
            "weight": item.get("survivability_score", 0),
            "status": item.get("status"),
            "projection_type": "NODE_WEIGHT"
        })

    for item in vector.get("vectors", []):
        edges.append({
            "source": item.get("source"),
            "target": item.get("target"),
            "magnitude": item.get("magnitude", 0),
            "status": item.get("status"),
            "projection_type": "DIRECTIONAL_EDGE"
        })

    for item in tensor.get("tensors", []):
        overlays.append({
            "node": item.get("node"),
            "tensor_score": item.get("tensor_score", 0),
            "directional_coupling": item.get("directional_coupling", 0),
            "status": item.get("status"),
            "projection_type": "TENSOR_OVERLAY"
        })

    for item in basin.get("basins", []):
        overlays.append({
            "node": item.get("basin_node"),
            "basin_score": item.get("accumulated_score", 0),
            "convergence_depth": item.get("convergence_depth", 0),
            "status": item.get("status"),
            "projection_type": "BASIN_OVERLAY"
        })

    report = {
        "engine": "SURVIVABILITY_TOPOLOGY_PROJECTION",
        "status": "PROJECTED",
        "node_projection_count": len(nodes),
        "edge_projection_count": len(edges),
        "overlay_projection_count": len(overlays),
        "nodes": nodes,
        "edges": edges,
        "overlays": overlays,
        "observer_mode": True,
        "interpretation": "Projects survivability heatmap, vector, tensor, and basin outputs into a rendering-ready topology representation.",
        "non_claims": [
            "Not runtime visualization",
            "Not execution control",
            "Not prediction",
            "Not production monitoring",
            "Not certification"
        ]
    }

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2))
    print("Inputs/survivability_topology_projection -> PROJECTED")

if __name__ == "__main__":
    main()