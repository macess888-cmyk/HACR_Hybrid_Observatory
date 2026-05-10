import json
import os

INPUT_FILE = "Inputs/topology_case.json"
OUTPUT_FILE = "Outputs/topology_map.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

nodes = data.get("nodes", [])
edges = data.get("edges", [])

effect_paths = []
shadow_paths = []

for edge in edges:
    if edge.get("effect_capable") is True:
        effect_paths.append(edge)

    if edge.get("hidden") is True:
        shadow_paths.append(edge)

result = {
    "topology_status": "SHADOW" if shadow_paths else "PASS",
    "node_count": len(nodes),
    "edge_count": len(edges),
    "effect_capable_paths": effect_paths,
    "shadow_paths": shadow_paths
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(result, f, indent=2)

print(f"{INPUT_FILE} -> {result['topology_status']}")