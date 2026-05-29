import json
import hashlib
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "input" / "sample_shared_basin_field.json"
OUTPUT_DIR = ROOT / "output"

SVG_FILE = OUTPUT_DIR / "shared_basin_field.svg"
RECEIPT_FILE = OUTPUT_DIR / "shared_basin_field_receipt.json"

WIDTH = 1600
HEIGHT = 1000


NODE_POSITIONS = {
    "Documentation": (500, 350),
    "Tooling": (850, 330),
    "Governance": (1150, 500),
    "Boundary Layer": (850, 760)
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


def basin_strength(node, node_counts, pair_counts):

    strength = node_counts[node]

    for pair, count in pair_counts.items():

        if node in pair:
            strength += count

    return strength


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
        f'<text x="30" y="50" fill="white" font-size="32">'
        f'{title}'
        f'</text>'
    )

    svg.append(
        '<text x="30" y="85" fill="#aaaaaa" font-size="14">'
        'Observer-only shared continuity-memory field'
        '</text>'
    )

    #
    # Shared Basin Fields
    #

    for pair, count in pair_counts.items():

        a, b = pair

        x1, y1 = NODE_POSITIONS[a]
        x2, y2 = NODE_POSITIONS[b]

        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2

        radius = 90 + (count * 40)

        opacity = min(
            0.05 + (count * 0.03),
            0.18
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
    # Convergence Field
    #

    svg.append(
        '<circle '
        'cx="820" '
        'cy="470" '
        'r="260" '
        'fill="#2196F3" '
        'fill-opacity="0.04" '
        'stroke="none"/>'
    )

    #
    # Corridors
    #

    for pair, count in pair_counts.items():

        a, b = pair

        x1, y1 = NODE_POSITIONS[a]
        x2, y2 = NODE_POSITIONS[b]

        width = 1 + count * 2

        svg.append(
            f'<line '
            f'x1="{x1}" y1="{y1}" '
            f'x2="{x2}" y2="{y2}" '
            f'stroke="#bbbbbb" '
            f'stroke-width="{width}" '
            f'opacity="0.30"/>'
        )

    #
    # Nodes
    #

    scores = {
        node: basin_strength(
            node,
            node_counts,
            pair_counts
        )
        for node in node_counts
    }

    max_score = max(scores.values())

    for node, count in node_counts.items():

        x, y = NODE_POSITIONS[node]

        score = scores[node]

        ratio = score / max_score

        radius = 45 + (count * 10)

        if ratio >= 0.75:
            color = "#00C853"
            zone = "CORE"

        elif ratio >= 0.45:
            color = "#2196F3"
            zone = "EDGE"

        else:
            color = "#FF9800"
            zone = "FRINGE"

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
            f'{zone} | {score}'
            f'</text>'
        )

    svg.append(
        '<text x="30" y="960" '
        'fill="#888888" '
        'font-size="12">'
        'Shared co-visibility field only • '
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
        "shared_fields": len(pair_counts),
        "observer_mode": True,
        "prediction": False,
        "causality_certification": False,
        "svg_sha256": hashlib.sha256(
            svg.encode("utf-8")
        ).hexdigest()
    }

    with open(RECEIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print("Shared Basin Field Rendered")
    print(SVG_FILE)
    print(RECEIPT_FILE)


if __name__ == "__main__":
    main()