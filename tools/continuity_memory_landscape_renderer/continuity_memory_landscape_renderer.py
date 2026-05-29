import json
import hashlib
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "input" / "sample_memory_landscape.json"
OUTPUT_DIR = ROOT / "output"

SVG_FILE = OUTPUT_DIR / "continuity_memory_landscape.svg"
RECEIPT_FILE = OUTPUT_DIR / "continuity_memory_landscape_receipt.json"

WIDTH = 1800
HEIGHT = 1100


NODE_POSITIONS = {
    "Documentation": (550, 380),
    "Tooling": (950, 360),
    "Governance": (1300, 560),
    "Boundary Layer": (950, 860)
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
        f'<text x="30" y="50" fill="white" font-size="34">'
        f'{title}'
        f'</text>'
    )

    svg.append(
        '<text x="30" y="90" fill="#aaaaaa" font-size="14">'
        'Observer-only continuity-memory landscape'
        '</text>'
    )

    #
    # Memory Landscape Layers
    #

    contour_levels = [
        (340, 0.020),
        (280, 0.030),
        (220, 0.040),
        (170, 0.050),
        (120, 0.070)
    ]

    landscape_center_x = 950
    landscape_center_y = 560

    for radius, opacity in contour_levels:

        svg.append(
            f'<circle '
            f'cx="{landscape_center_x}" '
            f'cy="{landscape_center_y}" '
            f'r="{radius}" '
            f'fill="#2196F3" '
            f'fill-opacity="{opacity}" '
            f'stroke="none"/>'
        )

    #
    # Shared Basin Gradients
    #

    for pair, count in pair_counts.items():

        a, b = pair

        x1, y1 = NODE_POSITIONS[a]
        x2, y2 = NODE_POSITIONS[b]

        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2

        for step in range(4):

            radius = 60 + (count * 25) + (step * 35)

            opacity = max(
                0.12 - (step * 0.025),
                0.015
            )

            svg.append(
                f'<circle '
                f'cx="{mx}" '
                f'cy="{my}" '
                f'r="{radius}" '
                f'fill="#00C853" '
                f'fill-opacity="{opacity}" '
                f'stroke="none"/>'
            )

    #
    # Convergence Plateau
    #

    svg.append(
        '<ellipse '
        'cx="950" '
        'cy="560" '
        'rx="220" '
        'ry="150" '
        'fill="#00C853" '
        'fill-opacity="0.05" '
        'stroke="#00C853" '
        'stroke-opacity="0.10" '
        'stroke-width="2"/>'
    )

    #
    # Terrain Ridges
    #

    for pair, count in pair_counts.items():

        a, b = pair

        x1, y1 = NODE_POSITIONS[a]
        x2, y2 = NODE_POSITIONS[b]

        width = 1 + count * 2

        svg.append(
            f'<line '
            f'x1="{x1}" '
            f'y1="{y1}" '
            f'x2="{x2}" '
            f'y2="{y2}" '
            f'stroke="#cccccc" '
            f'stroke-width="{width}" '
            f'opacity="0.20"/>'
        )

    #
    # Nodes
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
            f'y="{y - 10}" '
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

    #
    # Landscape Labels
    #

    svg.append(
        '<text x="950" y="565" '
        'text-anchor="middle" '
        'fill="#66ff99" '
        'font-size="16">'
        'Convergence Plateau'
        '</text>'
    )

    svg.append(
        '<text x="30" y="1060" '
        'fill="#888888" '
        'font-size="12">'
        'Historical co-visibility terrain only • '
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
        "corridors": len(pair_counts),
        "observer_mode": True,
        "prediction": False,
        "causality_certification": False,
        "svg_sha256": hashlib.sha256(
            svg.encode("utf-8")
        ).hexdigest()
    }

    with open(RECEIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print("Continuity Memory Landscape Rendered")
    print(SVG_FILE)
    print(RECEIPT_FILE)


if __name__ == "__main__":
    main()