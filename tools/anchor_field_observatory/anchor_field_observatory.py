import json
import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).parent
REPO_ROOT = ROOT.parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.observatory_core.anchor import extract_anchors


INPUT_FILE = ROOT / "input" / "sample_anchor_field.json"
OUTPUT_DIR = ROOT / "output"

SVG_FILE = OUTPUT_DIR / "anchor_field_observatory.svg"
REPORT_FILE = OUTPUT_DIR / "anchor_field_report.json"
RECEIPT_FILE = OUTPUT_DIR / "anchor_field_receipt.json"

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
        'Observer-only anchor extraction'
        '</text>'
    )

    #
    # Anchor Field
    #

    field_layers = [
        (340, 0.020),
        (280, 0.030),
        (220, 0.040),
        (160, 0.050)
    ]

    for radius, opacity in field_layers:

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
    # Anchor Core
    #

    svg.append(
        '<circle '
        'cx="950" '
        'cy="650" '
        'r="120" '
        'fill="#88ffbb" '
        'fill-opacity="0.06" '
        'stroke="#88ffbb" '
        'stroke-opacity="0.35" '
        'stroke-width="3"/>'
    )

    svg.append(
        '<text '
        'x="950" '
        'y="645" '
        'text-anchor="middle" '
        'fill="#88ffbb" '
        'font-size="24">'
        'Anchor Core'
        '</text>'
    )

    svg.append(
        '<text '
        'x="950" '
        'y="675" '
        'text-anchor="middle" '
        'fill="#cccccc" '
        'font-size="12">'
        'stability after survival'
        '</text>'
    )

    #
    # Anchors
    #

    positions = [
        (650, 380),
        (1250, 380),
        (650, 900),
        (1250, 900)
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
            f'stroke-opacity="0.30"/>'
        )

        svg.append(
            f'<circle '
            f'cx="{x}" '
            f'cy="{y}" '
            f'r="82" '
            f'fill="#00C853" '
            f'fill-opacity="0.18" '
            f'stroke="#00C853" '
            f'stroke-width="4"/>'
        )

        svg.append(
            f'<text '
            f'x="{x}" '
            f'y="{y - 10}" '
            f'text-anchor="middle" '
            f'fill="white" '
            f'font-size="22">'
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

    #
    # Connectivity Anchors
    #

    svg.append(
        '<text '
        'x="30" '
        'y="980" '
        'fill="#88ffbb" '
        'font-size="16">'
        'Connectivity Anchors'
        '</text>'
    )

    y = 1010

    for item in report["connectivity_anchors"]:

        svg.append(
            f'<text '
            f'x="50" '
            f'y="{y}" '
            f'fill="#cccccc" '
            f'font-size="13">'
            f'{item["name"]}'
            f'</text>'
        )

        y += 26

    svg.append(
        '<text '
        'x="30" '
        'y="1120" '
        'fill="#bbbbbb" '
        'font-size="14">'
        'Anchor = stability surviving fixed-point extraction'
        '</text>'
    )

    svg.append(
        '<text '
        'x="30" '
        'y="1160" '
        'fill="#888888" '
        'font-size="12">'
        'Historical anchors only • No prediction • '
        'No routing • No causality certification • UNKNOWN → HOLD'
        '</text>'
    )

    svg.append('</svg>')

    return "\n".join(svg)


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    report = extract_anchors(data)

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    svg = build_svg(
        data.get("title", "Anchor Field Observatory"),
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

    print("Anchor Field Observatory Complete")
    print(REPORT_FILE)
    print(SVG_FILE)
    print(RECEIPT_FILE)


if __name__ == "__main__":
    main()