import json
import hashlib
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "input" / "sample_terrain_flow_network.json"
OUTPUT_DIR = ROOT / "output"

SVG_FILE = OUTPUT_DIR / "terrain_flow_network.svg"
RECEIPT_FILE = OUTPUT_DIR / "terrain_flow_network_receipt.json"

WIDTH = 1900
HEIGHT = 1200


NODE_POSITIONS = {
    "Documentation": (550, 400),
    "Tooling": (950, 380),
    "Governance": (1350, 620),
    "Boundary Layer": (950, 930)
}


def build_metrics(data):

    node_counts = {}
    pair_counts = {}

    for epoch in data["epochs"]:

        regions = epoch["regions"]

        for region in regions:
            node_counts[region] = node_counts.get(region, 0) + 1

        for a, b in combinations(sorted(regions), 2):

            key = (a, b)
            pair_counts[key] = pair_counts.get(key, 0) + 1

    return node_counts, pair_counts


def build_svg(title, node_counts, pair_counts):

    svg = []

    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">'
    )

    svg.append(
        '<rect width="100%" height="100%" fill="#0d1117"/>'
    )

    svg.append(
        f'<text x="30" y="50" fill="white" font-size="34">{title}</text>'
    )

    svg.append(
        '<text x="30" y="90" fill="#aaaaaa" font-size="14">'
        'Observer-only terrain connectivity visibility'
        '</text>'
    )

    #
    # TERRAIN BACKDROP
    #

    terrain_layers = [
        (540, "#082040", 0.020),
        (460, "#0d3560", 0.025),
        (380, "#124b80", 0.030),
        (300, "#17689a", 0.035),
        (220, "#15886d", 0.040),
        (150, "#19b15f", 0.050)
    ]

    cx = 950
    cy = 620

    for radius, color, opacity in terrain_layers:

        svg.append(
            f'<ellipse '
            f'cx="{cx}" '
            f'cy="{cy}" '
            f'rx="{radius}" '
            f'ry="{radius * 0.72}" '
            f'fill="{color}" '
            f'fill-opacity="{opacity}" '
            f'stroke="none"/>'
        )

    #
    # FLOW CORRIDORS
    #

    for pair, count in pair_counts.items():

        a, b = pair

        x1, y1 = NODE_POSITIONS[a]
        x2, y2 = NODE_POSITIONS[b]

        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2

        #
        # corridor glow
        #

        svg.append(
            f'<ellipse '
            f'cx="{mx}" '
            f'cy="{my}" '
            f'rx="{80 + count * 40}" '
            f'ry="{40 + count * 18}" '
            f'fill="#00C853" '
            f'fill-opacity="0.05" '
            f'stroke="none"/>'
        )

        #
        # connector
        #

        width = 2 + count

        svg.append(
            f'<line '
            f'x1="{x1}" '
            f'y1="{y1}" '
            f'x2="{x2}" '
            f'y2="{y2}" '
            f'stroke="#ffffff" '
            f'stroke-opacity="0.18" '
            f'stroke-width="{width}"/>'
        )

    #
    # SADDLE REGION
    #

    svg.append(
        '<ellipse '
        'cx="950" '
        'cy="620" '
        'rx="180" '
        'ry="90" '
        'fill="#88ffbb" '
        'fill-opacity="0.03" '
        'stroke="#88ffbb" '
        'stroke-opacity="0.10" '
        'stroke-width="2"/>'
    )

    #
    # FLOW LABELS
    #

    svg.append(
        '<text x="950" y="620" '
        'text-anchor="middle" '
        'fill="#88ffbb" '
        'font-size="18">'
        'Terrain Saddle'
        '</text>'
    )

    svg.append(
        '<text x="760" y="520" '
        'fill="#99ccff" '
        'font-size="14">'
        'Flow Corridor'
        '</text>'
    )

    svg.append(
        '<text x="1120" y="730" '
        'fill="#99ccff" '
        'font-size="14">'
        'Gradient Transition Zone'
        '</text>'
    )

    #
    # NODES
    #

    for node, count in node_counts.items():

        x, y = NODE_POSITIONS[node]

        radius = 40 + (count * 10)

        if count >= 3:
            color = "#00C853"
        elif count >= 2:
            color = "#2196F3"
        else:
            color = "#FF9800"

        svg.append(
            f'<circle '
            f'cx="{x}" '
            f'cy="{y}" '
            f'r="{radius}" '
            f'fill="{color}" '
            f'fill-opacity="0.18" '
            f'stroke="{color}" '
            f'stroke-width="3"/>'
        )

        svg.append(
            f'<text '
            f'x="{x}" '
            f'y="{y - 12}" '
            f'text-anchor="middle" '
            f'fill="white" '
            f'font-size="20">'
            f'{node}'
            f'</text>'
        )

        svg.append(
            f'<text '
            f'x="{x}" '
            f'y="{y + 18}" '
            f'text-anchor="middle" '
            f'fill="#cccccc" '
            f'font-size="12">'
            f'{count} epochs'
            f'</text>'
        )

    svg.append(
        '<text x="30" y="1160" '
        'fill="#888888" '
        'font-size="12">'
        'Historical terrain connectivity only • '
        'No prediction • '
        'No causality certification • '
        'UNKNOWN → HOLD'
        '</text>'
    )

    svg.append("</svg>")

    return "\n".join(svg)


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    node_counts, pair_counts = build_metrics(data)

    svg = build_svg(
        data["title"],
        node_counts,
        pair_counts
    )

    with open(SVG_FILE, "w", encoding="utf-8") as f:
        f.write(svg)

    receipt = {
        "title": data["title"],
        "regions": len(node_counts),
        "flow_corridors": len(pair_counts),
        "observer_mode": True,
        "prediction": False,
        "causality_certification": False,
        "svg_sha256": hashlib.sha256(
            svg.encode("utf-8")
        ).hexdigest()
    }

    with open(RECEIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print("Terrain Flow Network Rendered")
    print(SVG_FILE)
    print(RECEIPT_FILE)


if __name__ == "__main__":
    main()