import json
import os

INPUT_FILE = "Inputs/topology_case.json"
OUTPUT_FILE = "Outputs/topology_graph.dot"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

nodes = data.get("nodes", [])
edges = data.get("edges", [])

dot = []
dot.append("digraph HACRTopology {")
dot.append('    rankdir=LR;')

for node in nodes:
    dot.append(f'    "{node}";')

for edge in edges:
    src = edge.get("from")
    dst = edge.get("to")
    hidden = edge.get("hidden", False)
    effect = edge.get("effect_capable", False)

    style = "solid"
    color = "black"

    if hidden:
        style = "dashed"
        color = "red"

    if effect:
        color = "blue"

    dot.append(
        f'    "{src}" -> "{dst}" [color={color}, style={style}];'
    )

dot.append("}")

with open(OUTPUT_FILE, "w") as f:
    f.write("\n".join(dot))

print(f"{INPUT_FILE} -> TOPOLOGY_GRAPH_GENERATED")