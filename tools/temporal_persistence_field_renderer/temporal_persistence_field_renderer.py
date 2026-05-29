import json
import hashlib
from pathlib import Path


ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "input" / "sample_persistence_field.json"
OUTPUT_DIR = ROOT / "output"

SVG_FILE = OUTPUT_DIR / "temporal_persistence_field.svg"
RECEIPT_FILE = OUTPUT_DIR / "temporal_persistence_field_receipt.json"

WIDTH = 1200
HEIGHT = 800


def persistence_level(count, max_count):

    if max_count <= 0:
        return "UNKNOWN"

    ratio = count / max_count

    if ratio >= 0.75:
        return "HIGH_PERSISTENCE"

    if ratio >= 0.40:
        return "MEDIUM_PERSISTENCE"

    return "LOW_PERSISTENCE"


def persistence_color(level):

    colors = {
        "HIGH_PERSISTENCE": "#00C853",
        "MEDIUM_PERSISTENCE": "#2196F3",
        "LOW_PERSISTENCE": "#FF9800",
        "UNKNOWN": "#9E9E9E"
    }

    return colors.get(level, "#FFFFFF")


def calculate_persistence(data):

    counts = {}

    for epoch in data["epochs"]:

        for region in epoch["regions"]:

            counts[region] = counts.get(region, 0) + 1

    max_count = max(counts.values())

    result = []

    for region, count in counts.items():

        result.append({
            "name": region,
            "count": count,
            "level": persistence_level(count, max_count)
        })

    result.sort(
        key=lambda x: x["count"],
        reverse=True
    )

    return result


def build_svg(title, persistence_data):

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
        f'<text x="30" y="40" '
        f'fill="white" '
        f'font-size="30">'
        f'{title}'
        f'</text>'
    )

    svg.append(
        '<text x="30" y="80" '
        'fill="#aaaaaa" '
        'font-size="14">'
        'Observer-only historical persistence visibility'
        '</text>'
    )

    start_y = 180
    spacing = 130

    for idx, region in enumerate(persistence_data):

        y = start_y + (idx * spacing)

        color = persistence_color(region["level"])

        radius = 30 + (region["count"] * 20)

        svg.append(
            f'<circle '
            f'cx="250" '
            f'cy="{y}" '
            f'r="{radius}" '
            f'fill="{color}" '
            f'fill-opacity="0.15" '
            f'stroke="{color}" '
            f'stroke-width="3"/>'
        )

        svg.append(
            f'<text '
            f'x="450" '
            f'y="{y - 10}" '
            f'fill="white" '
            f'font-size="20">'
            f'{region["name"]}'
            f'</text>'
        )

        svg.append(
            f'<text '
            f'x="450" '
            f'y="{y + 20}" '
            f'fill="#bbbbbb" '
            f'font-size="14">'
            f'Visible Epochs: {region["count"]} '
            f'| {region["level"]}'
            f'</text>'
        )

    svg.append(
        '<text x="30" y="760" '
        'fill="#888888" '
        'font-size="12">'
        'Historical visibility only • No prediction • '
        'No causality certification • UNKNOWN → HOLD'
        '</text>'
    )

    svg.append("</svg>")

    return "\n".join(svg)


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    persistence_data = calculate_persistence(data)

    svg = build_svg(
        data["title"],
        persistence_data
    )

    with open(SVG_FILE, "w", encoding="utf-8") as f:
        f.write(svg)

    receipt = {
        "title": data["title"],
        "regions": len(persistence_data),
        "observer_mode": True,
        "prediction": False,
        "causality_certification": False,
        "svg_sha256": hashlib.sha256(
            svg.encode("utf-8")
        ).hexdigest()
    }

    with open(RECEIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print("Temporal Persistence Field Rendered")
    print(SVG_FILE)
    print(RECEIPT_FILE)


if __name__ == "__main__":
    main()