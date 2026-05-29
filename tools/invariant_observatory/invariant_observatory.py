import json
import hashlib
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "input" / "sample_invariant_observatory.json"
OUTPUT_DIR = ROOT / "output"

SVG_FILE = OUTPUT_DIR / "invariant_observatory.svg"
REPORT_FILE = OUTPUT_DIR / "invariant_report.json"
RECEIPT_FILE = OUTPUT_DIR / "invariant_receipt.json"

WIDTH = 1900
HEIGHT = 1200


NODE_POSITIONS = {
    "Documentation": (700, 450),
    "Tooling": (1200, 450),
    "Invariant Core": (950, 700)
}


def extract_invariants(data):

    epochs = data.get("epochs", [])
    total_epochs = len(epochs)

    region_counts = {}
    corridor_counts = {}

    for epoch in epochs:

        regions = sorted(epoch.get("regions", []))

        for region in regions:
            region_counts[region] = region_counts.get(region, 0) + 1

        for a, b in combinations(regions, 2):
            key = f"{a} ↔ {b}"
            corridor_counts[key] = corridor_counts.get(key, 0) + 1

    visibility_invariants = []
    connectivity_invariants = []
    backbone_invariants = []

    for region, count in sorted(region_counts.items()):

        if count == total_epochs:

            visibility_invariants.append(region)

            backbone_invariants.append({
                "name": region,
                "classification": "BACKBONE_INVARIANT"
            })

    for corridor, count in sorted(corridor_counts.items()):

        if count == total_epochs:

            connectivity_invariants.append(corridor)

    report = {
        "total_epochs": total_epochs,
        "visibility_invariants": visibility_invariants,
        "connectivity_invariants": connectivity_invariants,
        "backbone_invariants": backbone_invariants,
        "observer_mode": True,
        "prediction": False,
        "routing": False,
        "causality_certification": False,
        "governance_authority": False,
        "status": "INVARIANT_EXTRACTION_COMPLETE"
    }

    return report


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
        'Observer-only invariant extraction'
        '</text>'
    )

    #
    # Invariant Core
    #

    svg.append(
        '<circle cx="950" cy="700" r="120" '
        'fill="#88ffbb" fill-opacity="0.05" '
        'stroke="#88ffbb" stroke-opacity="0.30" '
        'stroke-width="3"/>'
    )

    svg.append(
        '<text x="950" y="700" '
        'text-anchor="middle" '
        'fill="#88ffbb" '
        'font-size="24">'
        'Invariant Core'
        '</text>'
    )

    #
    # Backbone Invariants
    #

    invariant_regions = report["visibility_invariants"]

    positions = [
        (700, 450),
        (1200, 450),
        (550, 650),
        (1350, 650)
    ]

    for idx, region in enumerate(invariant_regions):

        if idx >= len(positions):
            break

        x, y = positions[idx]

        svg.append(
            f'<line '
            f'x1="{x}" '
            f'y1="{y}" '
            f'x2="950" '
            f'y2="700" '
            f'stroke="#00C853" '
            f'stroke-width="6" '
            f'stroke-opacity="0.35"/>'
        )

        svg.append(
            f'<circle '
            f'cx="{x}" '
            f'cy="{y}" '
            f'r="72" '
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
            f'font-size="22">'
            f'{region}'
            f'</text>'
        )

        svg.append(
            f'<text '
            f'x="{x}" '
            f'y="{y + 20}" '
            f'text-anchor="middle" '
            f'fill="#ffffff" '
            f'font-size="11">'
            f'BACKBONE_INVARIANT'
            f'</text>'
        )

    #
    # Connectivity Invariants
    #

    y = 980

    svg.append(
        '<text x="30" y="980" fill="#88ffbb" font-size="16">'
        'Connectivity Invariants'
        '</text>'
    )

    for corridor in report["connectivity_invariants"]:

        svg.append(
            f'<text '
            f'x="50" '
            f'y="{y + 30}" '
            f'fill="#cccccc" '
            f'font-size="13">'
            f'{corridor}'
            f'</text>'
        )

        y += 24

    svg.append(
        '<text x="30" y="1160" '
        'fill="#888888" '
        'font-size="12">'
        'Historical invariants only • No prediction • '
        'No causality certification • UNKNOWN → HOLD'
        '</text>'
    )

    svg.append("</svg>")

    return "\n".join(svg)


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    report = extract_invariants(data)

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    svg = build_svg(
        data.get("title", "Invariant Observatory"),
        report
    )

    with open(SVG_FILE, "w", encoding="utf-8") as f:
        f.write(svg)

    receipt = {
        "title": data.get("title"),
        "visibility_invariants":
            len(report["visibility_invariants"]),
        "connectivity_invariants":
            len(report["connectivity_invariants"]),
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

    print("Invariant Observatory Complete")
    print(REPORT_FILE)
    print(SVG_FILE)
    print(RECEIPT_FILE)


if __name__ == "__main__":
    main()