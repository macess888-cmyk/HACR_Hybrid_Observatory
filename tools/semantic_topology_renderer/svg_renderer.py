"""
HACR Hybrid Observatory — SVG Renderer

Renders bounded semantic topology visibility.

Invariant:
visualization != authority
"""

from pathlib import Path
import json
import math


BASE_DIR = Path(__file__).resolve().parent


SVG_WIDTH = 1600
SVG_HEIGHT = 1200
CENTER_X = SVG_WIDTH // 2
CENTER_Y = SVG_HEIGHT // 2
RADIUS = 350


REGION_COLORS = {
    "boundary_layer": "#4b5563",
    "runtime_reduction_layer": "#2563eb",
    "reviewer_traversability_layer": "#059669",
    "semantic_topology_layer": "#7c3aed",
    "verification_layer": "#dc2626",
    "canonical_layer": "#ea580c",
    "runtime_constraints_layer": "#0891b2",
}


def load_traversal_topology() -> dict:
    path = BASE_DIR / "output" / "traversal_topology.json"

    if not path.exists():
        raise FileNotFoundError(
            "Missing traversal topology. Run traversal_mapper.py first."
        )

    return json.loads(path.read_text(encoding="utf-8"))


def unique_regions(nodes):
    seen = {}

    for node in nodes:
        region = node["region"]

        if region not in seen:
            seen[region] = {
                "id": region,
                "label": region.replace("_", " ").title(),
            }

    return list(seen.values())


def generate_region_positions(regions):
    positions = {}

    count = len(regions)

    for i, region in enumerate(regions):
        angle = (2 * math.pi * i) / max(count, 1)

        x = CENTER_X + int(RADIUS * math.cos(angle))
        y = CENTER_Y + int(RADIUS * math.sin(angle))

        positions[region["id"]] = (x, y)

    return positions


def render_svg(topology: dict) -> str:
    nodes = topology.get("nodes", [])
    corridors = topology.get("corridors", [])

    regions = unique_regions(nodes)
    positions = generate_region_positions(regions)

    svg = []

    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{SVG_WIDTH}" height="{SVG_HEIGHT}">'
    )

    svg.append(
        '<rect width="100%" height="100%" fill="#0f172a" />'
    )

    # Title
    svg.append(
        f'<text x="{CENTER_X}" y="60" '
        f'fill="white" font-size="28" text-anchor="middle">'
        f'HACR Semantic Topology'
        f'</text>'
    )

    # Observer-only label
    svg.append(
        f'<text x="{CENTER_X}" y="100" '
        f'fill="#94a3b8" font-size="16" text-anchor="middle">'
        f'Observer-Only • Non-Authoritative • UNKNOWN → HOLD'
        f'</text>'
    )

    # Corridors
    for corridor in corridors:
        src = corridor["source_region"]
        dst = corridor["target_region"]

        if src not in positions or dst not in positions:
            continue

        x1, y1 = positions[src]
        x2, y2 = positions[dst]

        svg.append(
            f'<line x1="{x1}" y1="{y1}" '
            f'x2="{x2}" y2="{y2}" '
            f'stroke="#475569" stroke-width="2" />'
        )

    # Regions
    for region in regions:
        region_id = region["id"]
        x, y = positions[region_id]

        color = REGION_COLORS.get(region_id, "#64748b")

        svg.append(
            f'<circle cx="{x}" cy="{y}" r="70" '
            f'fill="{color}" stroke="white" stroke-width="2" />'
        )

        svg.append(
            f'<text x="{x}" y="{y}" '
            f'fill="white" font-size="14" '
            f'text-anchor="middle">'
            f'{region["label"]}'
            f'</text>'
        )

    svg.append("</svg>")

    return "\n".join(svg)


def main() -> None:
    topology = load_traversal_topology()

    svg = render_svg(topology)

    output_dir = BASE_DIR / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    out_file = output_dir / "semantic_topology.svg"

    out_file.write_text(svg, encoding="utf-8")

    print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()