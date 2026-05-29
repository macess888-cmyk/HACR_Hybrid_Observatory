import json
import hashlib
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "input" / "sample_continuity_skeleton.json"
OUTPUT_DIR = ROOT / "output"

SVG_FILE = OUTPUT_DIR / "continuity_skeleton_observatory.svg"
RECEIPT_FILE = OUTPUT_DIR / "continuity_skeleton_observatory_receipt.json"
REPORT_FILE = OUTPUT_DIR / "continuity_skeleton_report.json"

WIDTH = 1900
HEIGHT = 1200


NODE_POSITIONS = {
    "Documentation": (550, 400),
    "Tooling": (950, 380),
    "Governance": (1350, 620),
    "Boundary Layer": (950, 930)
}


def classify_region(score):
    if score >= 0.90:
        return "PRIMARY_BACKBONE"
    if score >= 0.60:
        return "SECONDARY_BACKBONE"
    if score >= 0.30:
        return "PERSISTENCE_BRANCH"
    return "STRUCTURAL_REMNANT"


def classify_corridor(score):
    if score >= 0.90:
        return "PRIMARY_SPINE"
    if score >= 0.60:
        return "SECONDARY_SPINE"
    if score >= 0.30:
        return "PERSISTENCE_BRANCH"
    return "STRUCTURAL_REMNANT"


def color_for_class(class_name):
    colors = {
        "PRIMARY_BACKBONE": "#00C853",
        "SECONDARY_BACKBONE": "#2196F3",
        "PERSISTENCE_BRANCH": "#FF9800",
        "STRUCTURAL_REMNANT": "#9E9E9E",
        "PRIMARY_SPINE": "#88ffbb",
        "SECONDARY_SPINE": "#99ccff",
        "VISIBILITY_INVARIANT": "#ffffff"
    }
    return colors.get(class_name, "#ffffff")


def extract_skeleton(data):
    epochs = data.get("epochs", [])
    total_epochs = len(epochs)

    if total_epochs == 0:
        return {
            "total_epochs": 0,
            "regions": [],
            "corridors": [],
            "visibility_invariants": [],
            "observer_mode": True,
            "status": "UNKNOWN_HOLD"
        }

    region_counts = {}
    corridor_counts = {}

    for epoch in epochs:
        regions = sorted(epoch.get("regions", []))

        for region in regions:
            region_counts[region] = region_counts.get(region, 0) + 1

        for a, b in combinations(regions, 2):
            key = f"{a} ↔ {b}"
            corridor_counts[key] = corridor_counts.get(key, 0) + 1

    regions_out = []
    corridors_out = []
    invariants = []

    for region, count in sorted(region_counts.items()):
        score = count / total_epochs
        classification = classify_region(score)

        item = {
            "name": region,
            "visible_epochs": count,
            "total_epochs": total_epochs,
            "skeleton_strength": round(score, 4),
            "classification": classification,
            "visibility_invariant": count == total_epochs
        }

        regions_out.append(item)

        if count == total_epochs:
            invariants.append({
                "type": "region",
                "name": region
            })

    for corridor, count in sorted(corridor_counts.items()):
        score = count / total_epochs
        classification = classify_corridor(score)

        item = {
            "name": corridor,
            "visible_epochs": count,
            "total_epochs": total_epochs,
            "spine_strength": round(score, 4),
            "classification": classification,
            "visibility_invariant": count == total_epochs
        }

        corridors_out.append(item)

        if count == total_epochs:
            invariants.append({
                "type": "corridor",
                "name": corridor
            })

    return {
        "total_epochs": total_epochs,
        "regions": regions_out,
        "corridors": corridors_out,
        "visibility_invariants": invariants,
        "observer_mode": True,
        "prediction": False,
        "causality_certification": False,
        "routing": False,
        "governance_authority": False,
        "status": "EXTRACTED"
    }


def parse_corridor_name(name):
    left, right = name.split(" ↔ ")
    return left, right


def build_svg(title, skeleton):
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
        'Observer-only structural persistence extraction'
        '</text>'
    )

    # Faded terrain context
    svg.append(
        '<ellipse cx="950" cy="620" rx="560" ry="400" '
        'fill="#124b80" fill-opacity="0.025" stroke="none"/>'
    )

    svg.append(
        '<ellipse cx="950" cy="620" rx="380" ry="260" '
        'fill="#15886d" fill-opacity="0.035" stroke="none"/>'
    )

    svg.append(
        '<ellipse cx="950" cy="620" rx="210" ry="140" '
        'fill="#19b15f" fill-opacity="0.045" stroke="none"/>'
    )

    # Skeleton corridors
    for corridor in skeleton["corridors"]:
        a, b = parse_corridor_name(corridor["name"])

        if a not in NODE_POSITIONS or b not in NODE_POSITIONS:
            continue

        x1, y1 = NODE_POSITIONS[a]
        x2, y2 = NODE_POSITIONS[b]

        classification = corridor["classification"]
        color = color_for_class(classification)
        width = 2 + corridor["spine_strength"] * 8

        opacity = 0.42 if corridor["visibility_invariant"] else 0.22

        svg.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{width}" '
            f'stroke-opacity="{opacity}"/>'
        )

    # Skeleton junction
    svg.append(
        '<circle cx="950" cy="620" r="82" '
        'fill="#88ffbb" fill-opacity="0.045" '
        'stroke="#88ffbb" stroke-opacity="0.22" stroke-width="2"/>'
    )

    svg.append(
        '<text x="950" y="625" text-anchor="middle" '
        'fill="#88ffbb" font-size="18">'
        'Skeleton Junction'
        '</text>'
    )

    # Nodes
    for region in skeleton["regions"]:
        node = region["name"]

        if node not in NODE_POSITIONS:
            continue

        x, y = NODE_POSITIONS[node]
        classification = region["classification"]
        color = color_for_class(classification)

        radius = 42 + region["skeleton_strength"] * 28
        stroke_width = 5 if region["visibility_invariant"] else 3

        svg.append(
            f'<circle cx="{x}" cy="{y}" r="{radius}" '
            f'fill="{color}" fill-opacity="0.16" '
            f'stroke="{color}" stroke-width="{stroke_width}"/>'
        )

        svg.append(
            f'<text x="{x}" y="{y - 14}" text-anchor="middle" '
            f'fill="white" font-size="20">{node}</text>'
        )

        svg.append(
            f'<text x="{x}" y="{y + 16}" text-anchor="middle" '
            f'fill="#cccccc" font-size="12">'
            f'{classification} | {region["skeleton_strength"]}'
            f'</text>'
        )

        if region["visibility_invariant"]:
            svg.append(
                f'<text x="{x}" y="{y + 36}" text-anchor="middle" '
                f'fill="#ffffff" font-size="11">'
                f'VISIBILITY_INVARIANT'
                f'</text>'
            )

    svg.append(
        '<text x="30" y="1120" fill="#bbbbbb" font-size="14">'
        'Skeleton = structure surviving historical visibility reduction'
        '</text>'
    )

    svg.append(
        '<text x="30" y="1160" fill="#888888" font-size="12">'
        'No prediction • No routing • No causality certification • UNKNOWN → HOLD'
        '</text>'
    )

    svg.append("</svg>")

    return "\n".join(svg)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    skeleton = extract_skeleton(data)

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(skeleton, f, indent=2)

    svg = build_svg(data.get("title", "Continuity Skeleton Observatory"), skeleton)

    with open(SVG_FILE, "w", encoding="utf-8") as f:
        f.write(svg)

    receipt = {
        "title": data.get("title"),
        "total_epochs": skeleton["total_epochs"],
        "regions": len(skeleton["regions"]),
        "corridors": len(skeleton["corridors"]),
        "visibility_invariants": len(skeleton["visibility_invariants"]),
        "observer_mode": True,
        "prediction": False,
        "causality_certification": False,
        "routing": False,
        "governance_authority": False,
        "report_sha256": hashlib.sha256(
            json.dumps(skeleton, sort_keys=True).encode("utf-8")
        ).hexdigest(),
        "svg_sha256": hashlib.sha256(
            svg.encode("utf-8")
        ).hexdigest()
    }

    with open(RECEIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print("Continuity Skeleton Observatory Extracted")
    print(REPORT_FILE)
    print(SVG_FILE)
    print(RECEIPT_FILE)


if __name__ == "__main__":
    main()