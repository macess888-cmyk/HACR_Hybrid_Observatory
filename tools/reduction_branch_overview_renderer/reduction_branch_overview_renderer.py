from pathlib import Path
import hashlib
import json


ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "output"

SVG_FILE = OUTPUT_DIR / "reduction_branch_overview.svg"
RECEIPT_FILE = OUTPUT_DIR / "reduction_branch_overview_receipt.json"

WIDTH = 1700
HEIGHT = 1450


LAYERS = [
    ("Skeleton", "Structural persistence"),
    ("Invariant", "Cross-epoch persistence"),
    ("Fixed Point", "Reduction-stable visibility"),
    ("Anchor", "Stability anchor"),
    ("Anchor Basin", "Anchor concentration"),
    ("Anchor Attractor", "Basin residue"),
    ("Reduction Horizon", "Remaining visibility"),
    ("Visibility Extinction Boundary", "Exhaustion boundary"),
    ("Reduction Residue", "Irreducible remainder")
]


def build_svg():
    svg = []

    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">'
    )

    svg.append('<rect width="100%" height="100%" fill="#0d1117"/>')

    svg.append(
        '<text x="50" y="60" fill="white" font-size="36">'
        'Reduction Branch Architecture'
        '</text>'
    )

    svg.append(
        '<text x="50" y="100" fill="#aaaaaa" font-size="15">'
        'Observer-only reduction lineage'
        '</text>'
    )

    start_y = 190
    spacing = 125
    center_x = 720
    desc_x = 960

    for idx, (name, desc) in enumerate(LAYERS):
        y = start_y + idx * spacing

        svg.append(
            f'<circle cx="{center_x}" cy="{y}" r="48" '
            f'fill="#88ffbb" fill-opacity="0.08" '
            f'stroke="#88ffbb" stroke-opacity="0.45" '
            f'stroke-width="3"/>'
        )

        svg.append(
            f'<text x="{center_x}" y="{y + 6}" '
            f'text-anchor="middle" fill="white" font-size="17">'
            f'{name}'
            f'</text>'
        )

        svg.append(
            f'<text x="{desc_x}" y="{y + 6}" '
            f'fill="#cccccc" font-size="17">'
            f'{desc}'
            f'</text>'
        )

        if idx < len(LAYERS) - 1:
            y2 = start_y + (idx + 1) * spacing

            svg.append(
                f'<line x1="{center_x}" y1="{y + 52}" '
                f'x2="{center_x}" y2="{y2 - 52}" '
                f'stroke="#88ffbb" stroke-opacity="0.28" '
                f'stroke-width="4"/>'
            )

            svg.append(
                f'<text x="{center_x}" y="{y + 88}" '
                f'text-anchor="middle" fill="#88ffbb" '
                f'font-size="20">↓</text>'
            )

    svg.append(
        '<text x="50" y="1340" fill="#bbbbbb" font-size="15">'
        'Observer-Only Reduction Lineage • No prediction • No routing • '
        'No causality certification • No governance authority'
        '</text>'
    )

    svg.append(
        '<text x="50" y="1375" fill="#888888" font-size="14">'
        'UNKNOWN → HOLD'
        '</text>'
    )

    svg.append('</svg>')

    return "\n".join(svg)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    svg = build_svg()

    with open(SVG_FILE, "w", encoding="utf-8") as f:
        f.write(svg)

    receipt = {
        "title": "Reduction Branch Overview",
        "layers": len(LAYERS),
        "observer_mode": True,
        "prediction": False,
        "routing": False,
        "causality_certification": False,
        "governance_authority": False,
        "svg_sha256": hashlib.sha256(
            svg.encode("utf-8")
        ).hexdigest()
    }

    with open(RECEIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print("Reduction Branch Overview Rendered")
    print(SVG_FILE)
    print(RECEIPT_FILE)


if __name__ == "__main__":
    main()