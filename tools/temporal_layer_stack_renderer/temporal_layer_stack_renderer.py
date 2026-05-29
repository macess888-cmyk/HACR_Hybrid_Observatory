import json
import hashlib
from pathlib import Path


ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "input" / "sample_temporal_stack.json"
OUTPUT_DIR = ROOT / "output"

SVG_FILE = OUTPUT_DIR / "temporal_layer_stack.svg"
RECEIPT_FILE = OUTPUT_DIR / "temporal_layer_stack_receipt.json"


WIDTH = 1200
HEIGHT = 800


STATUS_COLORS = {
    "VISIBLE": "#4CAF50",
    "PERSISTENT": "#2196F3",
    "SHIFTED": "#FF9800",
    "FADED": "#9E9E9E",
    "DISCONTINUOUS": "#F44336"
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def epoch_opacity(index, total):
    if total <= 1:
        return 1.0

    return round(0.25 + ((index + 1) / total) * 0.75, 2)


def build_svg(data):

    svg = []

    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">'
    )

    svg.append(
        '<rect x="0" y="0" width="100%" height="100%" fill="#0d1117"/>'
    )

    svg.append(
        f'<text x="30" y="40" fill="white" '
        f'font-size="28" font-family="Arial">'
        f'{data.get("title","Temporal Layer Stack")}'
        f'</text>'
    )

    epochs = data.get("epochs", [])

    region_history = {}

    for epoch_index, epoch in enumerate(epochs):

        opacity = epoch_opacity(epoch_index, len(epochs))

        svg.append(
            f'<g opacity="{opacity}">'
        )

        svg.append(
            f'<text x="25" y="{90 + epoch_index * 24}" '
            f'fill="#bbbbbb" '
            f'font-size="14">'
            f'{epoch["id"]}: {epoch["label"]}'
            f'</text>'
        )

        for region in epoch.get("regions", []):

            color = STATUS_COLORS.get(
                region.get("status"),
                "#FFFFFF"
            )

            x = region["x"]
            y = region["y"]
            r = region["radius"]

            svg.append(
                f'<circle '
                f'cx="{x}" '
                f'cy="{y}" '
                f'r="{r}" '
                f'fill="{color}" '
                f'fill-opacity="0.15" '
                f'stroke="{color}" '
                f'stroke-width="2"/>'
            )

            svg.append(
                f'<text '
                f'x="{x}" '
                f'y="{y}" '
                f'text-anchor="middle" '
                f'fill="white" '
                f'font-size="12">'
                f'{region["name"]}'
                f'</text>'
            )

            region_history.setdefault(
                region["name"],
                []
            ).append((x, y))

        svg.append("</g>")

    svg.append('<g opacity="0.6">')

    for region_name, points in region_history.items():

        if len(points) < 2:
            continue

        for i in range(len(points) - 1):

            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            svg.append(
                f'<line '
                f'x1="{x1}" '
                f'y1="{y1}" '
                f'x2="{x2}" '
                f'y2="{y2}" '
                f'stroke="#ffffff" '
                f'stroke-dasharray="6,4" '
                f'stroke-width="1.5"/>'
            )

    svg.append("</g>")

    svg.append(
        '<text x="30" y="760" '
        'fill="#888888" '
        'font-size="12">'
        'Observer-only temporal visibility • '
        'No prediction • No causality certification • '
        'UNKNOWN → HOLD'
        '</text>'
    )

    svg.append("</svg>")

    return "\n".join(svg)


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    svg = build_svg(data)

    with open(SVG_FILE, "w", encoding="utf-8") as f:
        f.write(svg)

    receipt = {
        "title": data.get("title"),
        "epochs": len(data.get("epochs", [])),
        "replay_trajectories": len(
            data.get("replay_trajectories", [])
        ),
        "observer_mode": True,
        "prediction": False,
        "causality_certification": False,
        "status": "VISIBLE",
        "svg_sha256": None
    }

    receipt["svg_sha256"] = hashlib.sha256(
        svg.encode("utf-8")
    ).hexdigest()

    with open(RECEIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print("Temporal Layer Stack Rendered")
    print(SVG_FILE)
    print(RECEIPT_FILE)


if __name__ == "__main__":
    main()