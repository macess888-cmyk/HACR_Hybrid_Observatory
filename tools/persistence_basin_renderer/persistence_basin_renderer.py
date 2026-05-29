import json
import hashlib
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "input" / "sample_persistence_basin.json"
OUTPUT_DIR = ROOT / "output"

SVG_FILE = OUTPUT_DIR / "persistence_basin.svg"
RECEIPT_FILE = OUTPUT_DIR / "persistence_basin_receipt.json"

WIDTH = 1400
HEIGHT = 900


NODE_POSITIONS = {
    "Documentation": (450, 320),
    "Tooling": (750, 300),
    "Governance": (980, 420),
    "Boundary Layer": (760, 650)
}


def calculate_metrics(data):

    node_counts = {}
    pair_counts = {}

    for epoch in data["epochs"]:

        regions = epoch["regions"]

        for region in regions:
            node_counts[region] = node_counts.get(region, 0) + 1

        for a, b in combinations(sorted(regions), 2):
            key = (a, b)
            pair_counts[key] = pair_counts.get(key, 0) + 1

    basin_strength = {}

    for region in node_counts:

        strength = node_counts[region]

        for pair, count in pair_counts.items():

            if region in pair:
                strength += count

        basin_strength[region] = strength

    return node_counts, pair_counts, basin_strength


def basin_level(score, max_score):

    ratio = score / max_score

    if ratio >= 0.75:
        return "CORE"

    if ratio >= 0.45:
        return "EDGE"

    return "FRINGE"


def basin_color(level):

    colors = {
        "CORE": "#00C853",
        "EDGE": "#2196F3",
        "FRINGE": "#FF9800"
    }

    return colors[level]


def build_svg(title, node_counts, pair_counts, basin_strength):

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
        f'<text x="30" y="45" fill="white" font-size="30">'
        f'{title}'
        f'</text>'
    )

    svg.append(
        '<text x="30" y="80" fill="#aaaaaa" font-size="14">'
        'Observer-only historical co-visibility concentration'
        '</text>'
    )

    max_score = max(basin_strength.values())

    #
    # Basin halos first
    #

    for region, score in basin_strength.items():

        x, y = NODE_POSITIONS[region]

        level = basin_level(score, max_score)
        color = basin_color(level)

        halo_radius = 80 + (score * 8)

        svg.append(
            f'<circle '
            f'cx="{x}" '
            f'cy="{y}" '
            f'r="{halo_radius}" '
            f'fill="{color}" '
            f'fill-opacity="0.06" '
            f'stroke="none"/>'
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
            f'stroke="#cccccc" '
            f'stroke-width="{width}" '
            f'opacity="0.35"/>'
        )

    #
    # Nodes
    #

    for region, count in node_counts.items():

        x, y = NODE_POSITIONS[region]

        score = basin_strength[region]

        level = basin_level(score, max_score)
        color = basin_color(level)

        radius = 40 + count * 12

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
            f'font-size="18">'
            f'{region}'
            f'</text>'
        )

        svg.append(
            f'<text '
            f'x="{x}" '
            f'y="{y + 16}" '
            f'text-anchor="middle" '
            f'fill="#cccccc" '
            f'font-size="12">'
            f'{level} | {score}'
            f'</text>'
        )

    svg.append(
        '<text x="30" y="860" '
        'fill="#888888" '
        'font-size="12">'
        'Historical concentration only • No prediction • '
        'No causality certification • UNKNOWN → HOLD'
        '</text>'
    )

    svg.append("</svg>")

    return "\n".join(svg)


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    node_counts, pair_counts, basin_strength = calculate_metrics(data)

    svg = build_svg(
        data["title"],
        node_counts,
        pair_counts,
        basin_strength
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

    print("Persistence Basin Rendered")
    print(SVG_FILE)
    print(RECEIPT_FILE)


if __name__ == "__main__":
    main()