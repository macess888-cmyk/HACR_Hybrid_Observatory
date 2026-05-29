import json
import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).parent
REPO_ROOT = ROOT.parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.observatory_core.anchor_basin import extract_anchor_basins


INPUT_FILE = ROOT / "input" / "sample_anchor_basin.json"
OUTPUT_DIR = ROOT / "output"

SVG_FILE = OUTPUT_DIR / "anchor_basin_observatory.svg"
REPORT_FILE = OUTPUT_DIR / "anchor_basin_report.json"
RECEIPT_FILE = OUTPUT_DIR / "anchor_basin_receipt.json"

WIDTH = 1900
HEIGHT = 1200


def build_svg(title, report):

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
        'Observer-only anchor basin extraction'
        '</text>'
    )

    #
    # Basin Layers
    #

    layers = [
        (320, 0.020),
        (260, 0.030),
        (200, 0.040),
        (140, 0.050)
    ]

    for radius, opacity in layers:

        svg.append(
            f'<circle '
            f'cx="950" '
            f'cy="650" '
            f'r="{radius}" '
            f'fill="#00C853" '
            f'fill-opacity="{opacity}" '
            f'stroke="none"/>'
        )

    #
    # Anchor Basin Core
    #

    svg.append(
        '<circle '
        'cx="950" '
        'cy="650" '
        'r="110" '
        'fill="#88ffbb" '
        'fill-opacity="0.08" '
        'stroke="#88ffbb" '
        'stroke-opacity="0.40" '
        'stroke-width="3"/>'
    )

    svg.append(
        '<text x="950" y="645" '
        'text-anchor="middle" '
        'fill="#88ffbb" '
        'font-size="24">'
        'Anchor Basin Core'
        '</text>'
    )

    svg.append(
        '<text x="950" y="675" '
        'text-anchor="middle" '
        'fill="#cccccc" '
        'font-size="12">'
        'stability concentration'
        '</text>'
    )

    #
    # Anchor Cluster
    #

    positions = [
        (650, 400),
        (1250, 400),
        (950, 980)
    ]

    for idx, anchor in enumerate(report["anchors"]):

        if idx >= len(positions):
            break

        x, y = positions[idx]

        svg.append(
            f'<line '
            f'x1="{x}" '
            f'y1="{y}" '
            f'x2="950" '
            f'y2="650" '
            f'stroke="#00C853" '
            f'stroke-width="8" '
            f'stroke-opacity="0.28"/>'
        )

        svg.append(
            f'<circle '
            f'cx="{x}" '
            f'cy="{y}" '
            f'r="76" '
            f'fill="#00C853" '
            f'fill-opacity="0.18" '
            f'stroke="#00C853" '
            f'stroke-width="4"/>'
        )

        svg.append(
            f'<text '
            f'x="{x}" '
            f'y="{y - 8}" '
            f'text-anchor="middle" '
            f'fill="white" '
            f'font-size="20">'
            f'{anchor["name"]}'
            f'</text>'
        )

        svg.append(
            f'<text '
            f'x="{x}" '
            f'y="{y + 16}" '
            f'text-anchor="middle" '
            f'fill="#ffffff" '
            f'font-size="11">'
            f'ANCHOR'
            f'</text>'
        )

    svg.append(
        '<text x="30" y="1120" '
        'fill="#bbbbbb" '
        'font-size="14">'
        'Anchor Basin = concentration of reduction-stable structures'
        '</text>'
    )

    svg.append(
        '<text x="30" y="1160" '
        'fill="#888888" '
        'font-size="12">'
        'Historical anchor basins only • No prediction • '
        'No routing • No causality certification • UNKNOWN → HOLD'
        '</text>'
    )

    svg.append('</svg>')

    return "\n".join(svg)


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    report = extract_anchor_basins(data)

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    svg = build_svg(
        data.get("title", "Anchor Basin Observatory"),
        report
    )

    with open(SVG_FILE, "w", encoding="utf-8") as f:
        f.write(svg)

    receipt = {
        "title": data.get("title"),
        "anchors": len(report["anchors"]),
        "connectivity_anchors": len(
            report["connectivity_anchors"]
        ),
        "observer_mode": True,
        "prediction": False,
        "routing": False,
        "causality_certification": False,
        "svg_sha256": hashlib.sha256(
            svg.encode("utf-8")
        ).hexdigest()
    }

    with open(RECEIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print("Anchor Basin Observatory Complete")
    print(REPORT_FILE)
    print(SVG_FILE)
    print(RECEIPT_FILE)


if __name__ == "__main__":
    main()