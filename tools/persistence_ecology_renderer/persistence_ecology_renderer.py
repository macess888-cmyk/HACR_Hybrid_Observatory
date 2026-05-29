import json
import hashlib
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "input" / "sample_persistence_ecology.json"
OUTPUT_DIR = ROOT / "output"

SVG_FILE = OUTPUT_DIR / "persistence_ecology.svg"
RECEIPT_FILE = OUTPUT_DIR / "persistence_ecology_receipt.json"

WIDTH = 1400
HEIGHT = 900


NODE_POSITIONS = {
    "Documentation": (350, 250),
    "Tooling": (700, 250),
    "Governance": (1050, 350),
    "Boundary Layer": (700, 650)
}


def build_covisibility(data):

    pair_counts = {}
    node_counts = {}

    for epoch in data["epochs"]:

        regions = epoch["regions"]

        for region in regions:
            node_counts[region] = node_counts.get(region, 0) + 1

        for a, b in combinations(sorted(regions), 2):

            key = (a, b)

            pair_counts[key] = pair_counts.get(key, 0) + 1

    return node_counts, pair_counts


def corridor_strength(count, max_count):

    if count >= max_count:
        return "STRONG_COVISIBILITY"

    if count >= max_count * 0.5:
        return "MEDIUM_COVISIBILITY"

    return "WEAK_COVISIBILITY"


def corridor_color(level):

    colors = {
        "STRONG_COVISIBILITY": "#00C853",
        "MEDIUM_COVISIBILITY": "#2196F3",
        "WEAK_COVISIBILITY": "#FF9800"
    }

    return colors[level]


def node_color(count, max_count):

    ratio = count / max_count

    if ratio >= 0.75:
        return "#00C853"

    if ratio >= 0.40:
        return "#2196F3"

    return "#FF9800"


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
        f'<text x="30" y="45" fill="white" font-size="30">'
        f'{title}'
        f'</text>'
    )

    svg.append(
        '<text x="30" y="80" fill="#aaaaaa" font-size="14">'
        'Observer-only historical co-visibility'
        '</text>'
    )

    max_pair = max(pair_counts.values()) if pair_counts else 1
    max_node = max(node_counts.values()) if node_counts else 1

    for pair, count in pair_counts.items():

        a, b = pair

        x1, y1 = NODE_POSITIONS[a]
        x2, y2 = NODE_POSITIONS[b]

        strength = corridor_strength(count, max_pair)
        color = corridor_color(strength)

        width = 2 + count * 2

        svg.append(
            f'<line '
            f'x1="{x1}" y1="{y1}" '
            f'x2="{x2}" y2="{y2}" '
            f'stroke="{color}" '
            f'stroke-width="{width}" '
            f'opacity="0.7"/>'
        )

        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2

        svg.append(
            f'<text '
            f'x="{mx}" '
            f'y="{my}" '
            f'fill="white" '
            f'font-size="12">'
            f'{count}'
            f'</text>'
        )

    for region, count in node_counts.items():

        x, y = NODE_POSITIONS[region]

        color = node_color(count, max_node)

        radius = 40 + (count * 15)

        svg.append(
            f'<circle '
            f'cx="{x}" '
            f'cy="{y}" '
            f'r="{radius}" '
            f'fill="{color}" '
            f'fill-opacity="0.15" '
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
            f'y="{y + 15}" '
            f'text-anchor="middle" '
            f'fill="#cccccc" '
            f'font-size="12">'
            f'{count} epochs'
            f'</text>'
        )

    svg.append(
        '<text x="30" y="860" '
        'fill="#888888" '
        'font-size="12">'
        'Historical co-visibility only • No prediction • '
        'No causality certification • UNKNOWN → HOLD'
        '</text>'
    )

    svg.append("</svg>")

    return "\n".join(svg)


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    node_counts, pair_counts = build_covisibility(data)

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

    print("Persistence Ecology Rendered")
    print(SVG_FILE)
    print(RECEIPT_FILE)


if __name__ == "__main__":
    main()