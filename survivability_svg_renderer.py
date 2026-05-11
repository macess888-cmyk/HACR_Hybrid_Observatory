import json
from pathlib import Path

INPUT = Path("Outputs/survivability_graph_export.json")
OUTPUT = Path("Outputs/survivability_graph.svg")

STATUS_COLORS = {
    "LOW": "#8fd19e",
    "ELEVATED": "#ffd966",
    "HIGH": "#f6b26b",
    "CRITICAL": "#e06666",
    "FAIL": "#cc0000",
    "SHADOW": "#8e7cc3",
    "UNSTABLE": "#c27ba0",
    "PROJECTED": "#6fa8dc"
}

def load(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def color(status):
    return STATUS_COLORS.get(status, "#cccccc")

def main():
    graph = load(INPUT)

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    width = 1200
    height = max(600, 120 + len(nodes) * 90)

    positions = {}
    x_left = 180
    x_right = 850

    for i, node in enumerate(nodes):
        name = node.get("node", f"node_{i}")
        x = x_left if i % 2 == 0 else x_right
        y = 80 + i * 70
        positions[name] = (x, y)

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')
    svg.append('<rect width="100%" height="100%" fill="#111111"/>')
    svg.append('<text x="40" y="40" fill="white" font-size="24" font-family="Arial">HACR Survivability Graph Export</text>')
    svg.append('<text x="40" y="68" fill="#cccccc" font-size="14" font-family="Arial">Observer-restricted topology visualization. Not runtime control.</text>')

    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")
        if source not in positions or target not in positions:
            continue

        x1, y1 = positions[source]
        x2, y2 = positions[target]
        stroke = color(edge.get("status"))
        mag = edge.get("magnitude", 1)
        width_px = max(1, min(8, mag // 4))

        svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width_px}" marker-end="url(#arrow)"/>')

    svg.append("""
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto" markerUnits="strokeWidth">
    <path d="M0,0 L0,6 L6,3 z" fill="#ffffff" />
  </marker>
</defs>
""")

    for node in nodes:
        name = node.get("node")
        if not name or name not in positions:
            continue

        x, y = positions[name]
        status = node.get("status", "LOW")
        weight = node.get("weight", 0)

        svg.append(f'<circle cx="{x}" cy="{y}" r="24" fill="{color(status)}" stroke="white" stroke-width="2"/>')
        svg.append(f'<text x="{x + 34}" y="{y - 4}" fill="white" font-size="14" font-family="Arial">{name}</text>')
        svg.append(f'<text x="{x + 34}" y="{y + 14}" fill="#cccccc" font-size="12" font-family="Arial">status={status} weight={weight}</text>')

    svg.append("</svg>")

    OUTPUT.write_text("\n".join(svg), encoding="utf-8")
    print("Inputs/survivability_svg_renderer -> SVG_GENERATED")

if __name__ == "__main__":
    main()