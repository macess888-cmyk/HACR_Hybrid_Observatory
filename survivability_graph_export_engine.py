import json
from pathlib import Path

PROJECTION = Path("Outputs/survivability_topology_projection_report.json")
OUTPUT = Path("Outputs/survivability_graph_export.json")

def load(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def main():
    projection = load(PROJECTION)

    graph = {
        "graph": "SURVIVABILITY_GRAPH_EXPORT",
        "version": "v4.8",
        "observer_mode": True,
        "nodes": projection.get("nodes", []),
        "edges": projection.get("edges", []),
        "overlays": projection.get("overlays", []),
        "metadata": {
            "source": "survivability_topology_projection_report.json",
            "format": "deterministic_observer_graph",
            "non_claims": [
                "Not runtime graph control",
                "Not execution routing",
                "Not prediction",
                "Not production monitoring",
                "Not certification"
            ]
        }
    }

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(graph, indent=2))
    print("Inputs/survivability_graph_export -> EXPORTED")

if __name__ == "__main__":
    main()