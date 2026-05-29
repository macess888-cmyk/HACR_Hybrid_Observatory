import json
import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).parent
REPO_ROOT = ROOT.parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.observatory_core.fixed_point import extract_fixed_points


INPUT_FILE = ROOT / "input" / "sample_fixed_point_observatory.json"
OUTPUT_DIR = ROOT / "output"

SVG_FILE = OUTPUT_DIR / "fixed_point_observatory.svg"
REPORT_FILE = OUTPUT_DIR / "fixed_point_report.json"
RECEIPT_FILE = OUTPUT_DIR / "fixed_point_receipt.json"

WIDTH = 1900
HEIGHT = 1200


POSITIONS = {
    "Documentation": (700, 430),
    "Tooling": (1200, 430),
    "Fixed Point Core": (950, 700)
}


def build_svg(title, report):
    svg = []

    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">'
    )

    svg.append('<rect width="100%" height="100%" fill="#0d1117"/>')

    svg.append(
        f'<text x="30" y="50" fill="white" font-size="34">{title}</text>'
    )

    svg.append(
        '<text x="30" y="90" fill="#aaaaaa" font-size="14">'
        'Observer-only fixed-point extraction'
        '</text>'
    )

    # Fixed point core
    svg.append(
        '<circle cx="950" cy="700" r="130" '
        'fill="#88ffbb" fill-opacity="0.045" '
        'stroke="#88ffbb" stroke-opacity="0.35" '
        'stroke-width="3"/>'
    )

    svg.append(
        '<text x="950" y="695" text-anchor="middle" '
        'fill="#88ffbb" font-size="24">'
        'Fixed Point Core'
        '</text>'
    )

    svg.append(
        '<text x="950" y="725" text-anchor="middle" '
        'fill="#cccccc" font-size="12">'
        'reduction-stable visibility'
        '</text>'
    )

    fixed_points = report.get("fixed_points", [])

    for idx, item in enumerate(fixed_points):
        name = item["name"]

        x, y = POSITIONS.get(
            name,
            (700 + idx * 250, 430)
        )

        svg.append(
            f'<line x1="{x}" y1="{y}" x2="950" y2="700" '
            f'stroke="#00C853" stroke-width="7" '
            f'stroke-opacity="0.32"/>'
        )

        svg.append(
            f'<circle cx="{x}" cy="{y}" r="78" '
            f'fill="#00C853" fill-opacity="0.18" '
            f'stroke="#00C853" stroke-width="4"/>'
        )

        svg.append(
            f'<text x="{x}" y="{y - 12}" text-anchor="middle" '
            f'fill="white" font-size="22">{name}</text>'
        )

        svg.append(
            f'<text x="{x}" y="{y + 16}" text-anchor="middle" '
            f'fill="#ffffff" font-size="11">'
            f'{item["classification"]}'
            f'</text>'
        )

        svg.append(
            f'<text x="{x}" y="{y + 34}" text-anchor="middle" '
            f'fill="#cccccc" font-size="11">'
            f'stability={item["stability"]}'
            f'</text>'
        )

    # Fixed connectivity list
    svg.append(
        '<text x="30" y="980" fill="#88ffbb" font-size="16">'
        'Fixed Connectivity'
        '</text>'
    )

    y = 1012

    for item in report.get("fixed_connectivity", []):
        svg.append(
            f'<text x="50" y="{y}" fill="#cccccc" font-size="13">'
            f'{item["name"]} | {item["classification"]}'
            f'</text>'
        )
        y += 26

    svg.append(
        '<text x="30" y="1120" fill="#bbbbbb" font-size="14">'
        'Fixed point = invariant visibility surviving reduction'
        '</text>'
    )

    svg.append(
        '<text x="30" y="1160" fill="#888888" font-size="12">'
        'Historical fixed points only • No prediction • '
        'No routing • No causality certification • UNKNOWN → HOLD'
        '</text>'
    )

    svg.append("</svg>")

    return "\n".join(svg)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    report = extract_fixed_points(data)

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    svg = build_svg(
        data.get("title", "Fixed Point Observatory"),
        report
    )

    with open(SVG_FILE, "w", encoding="utf-8") as f:
        f.write(svg)

    receipt = {
        "title": data.get("title"),
        "total_epochs": report.get("total_epochs"),
        "fixed_points": len(report.get("fixed_points", [])),
        "fixed_connectivity": len(report.get("fixed_connectivity", [])),
        "observer_mode": True,
        "prediction": False,
        "routing": False,
        "causality_certification": False,
        "report_sha256": hashlib.sha256(
            json.dumps(report, sort_keys=True).encode("utf-8")
        ).hexdigest(),
        "svg_sha256": hashlib.sha256(
            svg.encode("utf-8")
        ).hexdigest()
    }

    with open(RECEIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print("Fixed Point Observatory Complete")
    print(REPORT_FILE)
    print(SVG_FILE)
    print(RECEIPT_FILE)


if __name__ == "__main__":
    main()