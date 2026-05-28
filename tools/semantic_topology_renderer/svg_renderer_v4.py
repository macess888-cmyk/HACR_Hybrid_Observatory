"""
HACR Hybrid Observatory — SVG Renderer v4

Traversal-flow semantic field renderer.

Invariant:
traversal visualization != interpretive authority
"""

from pathlib import Path
import json
import math
import html


BASE_DIR = Path(__file__).resolve().parent

SVG_WIDTH = 2000
SVG_HEIGHT = 1450
CENTER_X = SVG_WIDTH // 2
CENTER_Y = SVG_HEIGHT // 2

OUTER_RADIUS = 500
INNER_RADIUS = 320

MIN_NODE_RADIUS = 48
MAX_NODE_RADIUS = 110


REGION_COLORS = {
    "boundary_layer": "#4b5563",
    "runtime_reduction_layer": "#2563eb",
    "reviewer_traversability_layer": "#059669",
    "semantic_topology_layer": "#7c3aed",
    "verification_layer": "#dc2626",
    "canonical_layer": "#ea580c",
    "runtime_constraints_layer": "#0891b2",
    "governance_observability_region": "#64748b",
    "documentation_region": "#64748b",
    "tooling_region": "#64748b",
    "unclassified_observability_region": "#64748b",
}


INNER_RING = {
    "boundary_layer",
    "semantic_topology_layer",
    "runtime_reduction_layer",
    "reviewer_traversability_layer",
}

OUTER_RING = {
    "verification_layer",
    "canonical_layer",
    "runtime_constraints_layer",
    "governance_observability_region",
    "documentation_region",
    "tooling_region",
    "unclassified_observability_region",
}


TRAVERSAL_FLOWS = [
    {
        "id": "canonical_entry_flow",
        "label": "Canonical Entry Flow",
        "regions": [
            "canonical_layer",
            "semantic_topology_layer",
            "reviewer_traversability_layer",
            "boundary_layer",
        ],
        "color": "#38bdf8",
    },
    {
        "id": "boundary_flow",
        "label": "Boundary Flow",
        "regions": [
            "canonical_layer",
            "boundary_layer",
            "runtime_constraints_layer",
            "verification_layer",
        ],
        "color": "#facc15",
    },
    {
        "id": "engineering_flow",
        "label": "Engineering Flow",
        "regions": [
            "runtime_reduction_layer",
            "runtime_constraints_layer",
            "verification_layer",
            "boundary_layer",
        ],
        "color": "#22c55e",
    },
    {
        "id": "semantic_topology_flow",
        "label": "Semantic Topology Flow",
        "regions": [
            "semantic_topology_layer",
            "governance_observability_region",
            "documentation_region",
            "boundary_layer",
        ],
        "color": "#a78bfa",
    },
]


def load_topology() -> dict:
    path = BASE_DIR / "output" / "traversal_topology.json"

    if not path.exists():
        raise FileNotFoundError(
            "Missing traversal topology. Run traversal_mapper.py first."
        )

    return json.loads(path.read_text(encoding="utf-8"))


def density_map(topology):
    return {
        item["region"]: item
        for item in topology.get("density_analysis", [])
    }


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


def scale_radius(count, max_count):
    normalized = count / max(max_count, 1)

    return int(
        MIN_NODE_RADIUS +
        (MAX_NODE_RADIUS - MIN_NODE_RADIUS) *
        math.sqrt(normalized)
    )


def circular_positions(regions, radius, offset=0):
    positions = {}

    count = len(regions)

    for i, region in enumerate(regions):
        angle = offset + (2 * math.pi * i) / max(count, 1)

        x = CENTER_X + int(radius * math.cos(angle))
        y = CENTER_Y + int(radius * math.sin(angle))

        positions[region["id"]] = (x, y)

    return positions


def multiline_label(label, max_len=18):
    words = label.split()

    lines = []
    current = ""

    for word in words:
        candidate = (current + " " + word).strip()

        if len(candidate) <= max_len:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines[:3]


def render_multiline_text(x, y, lines, size=14):
    out = []

    start_y = y - ((len(lines) - 1) * size * 0.55)

    for i, line in enumerate(lines):
        out.append(
            f'<text x="{x}" y="{start_y + i * (size + 4)}" '
            f'fill="white" font-size="{size}" '
            f'text-anchor="middle" '
            f'font-family="Arial, sans-serif">'
            f'{html.escape(line)}</text>'
        )

    return "\n".join(out)


def render_shell(svg, radius, color, opacity, label):
    svg.append(
        f'<circle cx="{CENTER_X}" cy="{CENTER_Y}" '
        f'r="{radius}" fill="none" '
        f'stroke="{color}" stroke-width="3" '
        f'opacity="{opacity}" />'
    )

    svg.append(
        f'<text x="{CENTER_X}" y="{CENTER_Y - radius - 14}" '
        f'fill="{color}" font-size="15" '
        f'text-anchor="middle" '
        f'font-family="Arial, sans-serif">'
        f'{html.escape(label)}</text>'
    )


def render_flow_path(svg, positions, flow):
    points = []

    for region in flow["regions"]:
        if region in positions:
            points.append(positions[region])

    if len(points) < 2:
        return

    point_string = " ".join(f"{x},{y}" for x, y in points)

    svg.append(
        f'<polyline points="{point_string}" fill="none" '
        f'stroke="{flow["color"]}" stroke-width="5" '
        f'opacity="0.42" stroke-linecap="round" '
        f'stroke-linejoin="round" />'
    )

    svg.append(
        f'<polyline points="{point_string}" fill="none" '
        f'stroke="{flow["color"]}" stroke-width="13" '
        f'opacity="0.10" stroke-linecap="round" '
        f'stroke-linejoin="round" />'
    )


def render_svg(topology):
    nodes = topology.get("nodes", [])
    corridors = topology.get("corridors", [])

    density = density_map(topology)

    regions = unique_regions(nodes)

    inner_regions = [
        r for r in regions
        if r["id"] in INNER_RING
    ]

    outer_regions = [
        r for r in regions
        if r["id"] in OUTER_RING
    ]

    positions = {}

    positions.update(
        circular_positions(
            inner_regions,
            INNER_RADIUS,
            offset=0.1
        )
    )

    positions.update(
        circular_positions(
            outer_regions,
            OUTER_RADIUS,
            offset=-0.25
        )
    )

    max_count = max(
        (
            density.get(r["id"], {}).get("document_count", 1)
            for r in regions
        ),
        default=1
    )

    svg = []

    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{SVG_WIDTH}" height="{SVG_HEIGHT}" '
        f'viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">'
    )

    svg.append(
        '<rect width="100%" height="100%" fill="#020617" />'
    )

    svg.append(
        f'<text x="{CENTER_X}" y="50" fill="white" '
        f'font-size="34" text-anchor="middle" '
        f'font-family="Arial, sans-serif">'
        f'HACR Semantic Traversal Field</text>'
    )

    svg.append(
        f'<text x="{CENTER_X}" y="86" fill="#93c5fd" '
        f'font-size="18" text-anchor="middle" '
        f'font-family="Arial, sans-serif">'
        f'Observer-Only • Non-Authoritative • Traversal Flow Visualization • UNKNOWN → HOLD</text>'
    )

    render_shell(
        svg,
        INNER_RADIUS + 135,
        "#475569",
        0.45,
        "Containment / Coordination Shell"
    )

    render_shell(
        svg,
        OUTER_RADIUS + 120,
        "#334155",
        0.35,
        "Peripheral Semantic Field"
    )

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
            f'stroke="#475569" stroke-width="2.5" '
            f'opacity="0.45" />'
        )

    for flow in TRAVERSAL_FLOWS:
        render_flow_path(svg, positions, flow)

    for region in regions:
        region_id = region["id"]

        if region_id not in positions:
            continue

        x, y = positions[region_id]

        item = density.get(
            region_id,
            {
                "document_count": 1,
                "density_pressure": "LOW",
            }
        )

        count = item["document_count"]
        pressure = item["density_pressure"]

        radius = scale_radius(count, max_count)

        color = REGION_COLORS.get(region_id, "#64748b")

        if pressure == "HIGH":
            stroke = "#fef3c7"
            stroke_width = 4
        elif pressure == "MEDIUM":
            stroke = "#bfdbfe"
            stroke_width = 3
        else:
            stroke = "#e5e7eb"
            stroke_width = 2

        svg.append(
            f'<circle cx="{x}" cy="{y}" '
            f'r="{radius}" fill="{color}" '
            f'stroke="{stroke}" '
            f'stroke-width="{stroke_width}" '
            f'opacity="0.96" />'
        )

        svg.append(
            render_multiline_text(
                x,
                y - 6,
                multiline_label(region["label"]),
                size=14
            )
        )

        svg.append(
            f'<text x="{x}" y="{y + radius - 18}" '
            f'fill="#e2e8f0" font-size="12" '
            f'text-anchor="middle" '
            f'font-family="Arial, sans-serif">'
            f'{count} docs • {pressure}</text>'
        )

    svg.append("</svg>")

    return "\n".join(svg)


def main():
    topology = load_topology()

    svg = render_svg(topology)

    output_dir = BASE_DIR / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    out_file = output_dir / "semantic_topology_v4.svg"

    out_file.write_text(svg, encoding="utf-8")

    print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()