
import json
import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).parent
REPO_ROOT = ROOT.parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.observatory_core.anchor_attractor import (
    extract_anchor_attractor
)


INPUT_FILE = ROOT / "input" / "sample_anchor_attractor.json"
OUTPUT_DIR = ROOT / "output"

SVG_FILE = OUTPUT_DIR / "anchor_attractor_observatory.svg"
REPORT_FILE = OUTPUT_DIR / "anchor_attractor_report.json"
RECEIPT_FILE = OUTPUT_DIR / "anchor_attractor_receipt.json"

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
        'Observer-only anchor attractor extraction'
        '</text>'
    )

    #
    # Attractor Field
    #

    field_layers = [
        (260, 0.020),
        (200, 0.030),
        (150, 0.040)
    ]

    for radius, opacity in field_layers:

        svg.append(
            f'<circle '
            f'cx="950" '
            f'cy="650" '
            f'r="{radius}" '
            f'fill="#88ffbb" '
            f'fill-opacity="{opacity}" '
            f'stroke="none"/>'
        )

    #
    # Attractor Core
    #

    svg.append(
        '<circle '
        'cx="950" '
        'cy="650" '
        'r="100" '
        'fill="#88ffbb" '
        'fill-opacity="0.10" '
        'stroke="#88ffbb" '
        'stroke-opacity="0.45" '
        'stroke-width="4"/>'
    )

    svg.append(
        '<text '
        'x="950" '
        'y="645" '
        'text-anchor="middle" '
        'fill="#88ffbb" '
        'font-size="24">'
        'Anchor Attractor'
        '</text>'
    )

    svg.append(
        '<text '
        'x="950" '
        'y="675" '
        'text-anchor="middle" '
        'fill="#cccccc" '
        'font-size="12">'
        'reduction-stable residue'
        '</text>'
    )

    attractor = report["anchor_attractor"]

    svg.append(
        '<text '
        'x="950" '
        'y="740" '
        'text-anchor="middle" '
        'fill="#ffffff" '
        'font-size="13">'
        f'anchors={attractor["source_anchor_count"]}'
        '</text>'
    )

    svg.append(
        '<text '
        'x="950" '
        'y="765" '
        'text-anchor="middle" '
        'fill="#ffffff" '
        'font-size="13">'
        f'connectivity={attractor["source_connectivity_count"]}'
        '</text>'
    )

    svg.append(
        '<text '
        'x="30" '
        'y="1120" '
        'fill="#bbbbbb" '
        'font-size="14">'
        'Anchor Attractor = structure surviving anchor-basin reduction'
        '</text>'
    )

    svg.append(
        '<text '
        'x="30" '
        'y="1160" '
        'fill="#888888" '
        'font-size="12">'
        'Historical attractors only • No prediction • '
        'No routing • No causality certification • UNKNOWN → HOLD'
        '</text>'
    )

    svg.append('</svg>')

    return "\n".join(svg)


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    report = extract_anchor_attractor(data)

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    svg = build_svg(
        data.get("title", "Anchor Attractor Observatory"),
        report
    )

    with open(SVG_FILE, "w", encoding="utf-8") as f:
        f.write(svg)

    receipt = {
        "title": data.get("title"),
        "classification": "ANCHOR_ATTRACTOR",
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

    print("Anchor Attractor Observatory Complete")
    print(REPORT_FILE)
    print(SVG_FILE)
    print(RECEIPT_FILE)


if __name__ == "__main__":
    main()