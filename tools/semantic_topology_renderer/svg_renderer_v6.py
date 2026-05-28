"""
HACR Hybrid Observatory — SVG Renderer v6

Semantic weather overlay renderer.

Invariant:
semantic climate visibility != prediction
"""

from pathlib import Path
import json
import math
import html


BASE_DIR = Path(__file__).resolve().parent

SVG_WIDTH = 2050
SVG_HEIGHT = 1500
CENTER_X = SVG_WIDTH // 2
CENTER_Y = SVG_HEIGHT // 2

OUTER_RADIUS = 520
INNER_RADIUS = 330

MIN_NODE_RADIUS = 48
MAX_NODE_RADIUS = 112


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
        raise FileNotFoundError("Missing traversal topology. Run traversal_mapper.py first.")
    return json.loads(path.read_text(encoding="utf-8"))


def density_map(topology):
    return {item["region"]: item for item in topology.get("density_analysis", [])}


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


def density_count(density, region_id):
    return density.get(region_id, {}).get("document_count", 1)


def density_pressure(density, region_id):
    return density.get(region_id, {}).get("density_pressure", "LOW")


def weather_state(count, pressure):
    if count >= 150:
        return "CONGESTED"
    if pressure == "HIGH" and count >= 75:
        return "TURBULENT"
    if pressure == "HIGH":
        return "STABLE"
    if pressure == "MEDIUM":
        return "DIFFUSED"
    return "CALM"


def scale_radius(count, max_count):
    normalized = count / max(max_count, 1)
    return int(MIN_NODE_RADIUS + (MAX_NODE_RADIUS - MIN_NODE_RADIUS) * math.sqrt(normalized))


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


def text_lines(x, y, lines, size=14, fill="white"):
    out = []
    start_y = y - ((len(lines) - 1) * size * 0.55)

    for i, line in enumerate(lines):
        out.append(
            f'<text x="{x}" y="{start_y + i * (size + 4)}" '
            f'fill="{fill}" font-size="{size}" text-anchor="middle" '
            f'font-family="Arial, sans-serif">{html.escape(line)}</text>'
        )

    return "\n".join(out)


def render_shell(svg, radius, color, opacity, label):
    svg.append(
        f'<circle cx="{CENTER_X}" cy="{CENTER_Y}" r="{radius}" fill="none" '
        f'stroke="{color}" stroke-width="3" opacity="{opacity}" />'
    )
    svg.append(
        f'<text x="{CENTER_X}" y="{CENTER_Y - radius - 14}" '
        f'fill="{color}" font-size="15" text-anchor="middle" '
        f'font-family="Arial, sans-serif">{html.escape(label)}</text>'
    )


def render_flow(svg, positions, flow):
    points = [positions[r] for r in flow["regions"] if r in positions]
    if len(points) < 2:
        return

    point_string = " ".join(f"{x},{y}" for x, y in points)

    svg.append(
        f'<polyline points="{point_string}" fill="none" '
        f'stroke="{flow["color"]}" stroke-width="16" opacity="0.10" '
        f'stroke-linecap="round" stroke-linejoin="round" />'
    )
    svg.append(
        f'<polyline points="{point_string}" fill="none" '
        f'stroke="{flow["color"]}" stroke-width="6" opacity="0.48" '
        f'stroke-linecap="round" stroke-linejoin="round" />'
    )


def render_svg(topology):
    nodes = topology.get("nodes", [])
    corridors = topology.get("corridors", [])
    density = density_map(topology)
    regions = unique_regions(nodes)

    inner_regions = [r for r in regions if r["id"] in INNER_RING]
    outer_regions = [r for r in regions if r["id"] in OUTER_RING]

    positions = {}
    positions.update(circular_positions(inner_regions, INNER_RADIUS, offset=0.1))
    positions.update(circular_positions(outer_regions, OUTER_RADIUS, offset=-0.25))

    max_count = max((density_count(density, r["id"]) for r in regions), default=1)

    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" '
        f'viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">'
    )
    svg.append('<rect width="100%" height="100%" fill="#020617" />')

    svg.append(
        f'<text x="{CENTER_X}" y="50" fill="white" font-size="34" '
        f'text-anchor="middle" font-family="Arial, sans-serif">'
        f'HACR Semantic Weather Field</text>'
    )
    svg.append(
        f'<text x="{CENTER_X}" y="86" fill="#93c5fd" font-size="18" '
        f'text-anchor="middle" font-family="Arial, sans-serif">'
        f'Observer-Only • Non-Authoritative • Semantic Climate Visibility • UNKNOWN → HOLD</text>'
    )
    svg.append(
        f'<text x="{CENTER_X}" y="112" fill="#cbd5e1" font-size="13" '
        f'text-anchor="middle" font-family="Arial, sans-serif">'
        f'Semantic climate visibility is observational only. It is not prediction, governance, or operational truth.</text>'
    )

    render_shell(svg, INNER_RADIUS + 135, "#475569", 0.45, "Containment / Coordination Shell")
    render_shell(svg, OUTER_RADIUS + 120, "#334155", 0.35, "Peripheral Semantic Field")

    # Weather deformation halos
    for region in regions:
        region_id = region["id"]
        if region_id not in positions:
            continue

        x, y = positions[region_id]
        count = density_count(density, region_id)
        pressure = density_pressure(density, region_id)
        state = weather_state(count, pressure)
        radius = scale_radius(count, max_count)

        if state == "CONGESTED":
            opacity = 0.20
            rx = radius + 70
            ry = radius + 38
            color = "#fef3c7"
        elif state == "TURBULENT":
            opacity = 0.16
            rx = radius + 50
            ry = radius + 28
            color = "#fde68a"
        elif state == "STABLE":
            opacity = 0.10
            rx = radius + 32
            ry = radius + 32
            color = "#bfdbfe"
        elif state == "DIFFUSED":
            opacity = 0.08
            rx = radius + 26
            ry = radius + 18
            color = "#93c5fd"
        else:
            opacity = 0.05
            rx = radius + 18
            ry = radius + 14
            color = "#94a3b8"

        svg.append(
            f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" '
            f'fill="{color}" opacity="{opacity}" '
            f'transform="rotate(-18 {x} {y})" />'
        )

    # Base corridors
    for corridor in corridors:
        src = corridor["source_region"]
        dst = corridor["target_region"]
        if src not in positions or dst not in positions:
            continue

        x1, y1 = positions[src]
        x2, y2 = positions[dst]

        svg.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="#475569" stroke-width="2.5" opacity="0.38" />'
        )

    # Traversal flows
    for flow in TRAVERSAL_FLOWS:
        render_flow(svg, positions, flow)

    # Nodes
    for region in regions:
        region_id = region["id"]
        if region_id not in positions:
            continue

        x, y = positions[region_id]
        count = density_count(density, region_id)
        pressure = density_pressure(density, region_id)
        state = weather_state(count, pressure)
        radius = scale_radius(count, max_count)

        color = REGION_COLORS.get(region_id, "#64748b")

        stroke = "#e5e7eb"
        stroke_width = 2
        if pressure == "HIGH":
            stroke = "#fef3c7"
            stroke_width = 4
        elif pressure == "MEDIUM":
            stroke = "#bfdbfe"
            stroke_width = 3

        svg.append(
            f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" '
            f'stroke="{stroke}" stroke-width="{stroke_width}" opacity="0.96" />'
        )

        svg.append(text_lines(x, y - 12, multiline_label(region["label"]), size=14))

        svg.append(
            f'<text x="{x}" y="{y + radius - 30}" fill="#e2e8f0" font-size="12" '
            f'text-anchor="middle" font-family="Arial, sans-serif">'
            f'{count} docs • {pressure}</text>'
        )
        svg.append(
            f'<text x="{x}" y="{y + radius - 14}" fill="#fef3c7" font-size="11" '
            f'text-anchor="middle" font-family="Arial, sans-serif">'
            f'{state}</text>'
        )

    # Legend
    legend_x = 55
    legend_y = SVG_HEIGHT - 280
    svg.append(
        f'<rect x="{legend_x}" y="{legend_y}" width="650" height="235" '
        f'fill="#020617" stroke="#334155" stroke-width="1.5" rx="14" />'
    )
    svg.append(
        f'<text x="{legend_x + 22}" y="{legend_y + 36}" fill="white" '
        f'font-size="18" font-family="Arial, sans-serif">Semantic Weather Legend</text>'
    )

    legend_lines = [
        "CONGESTED = high semantic concentration basin",
        "TURBULENT = dense traversal-pressure zone",
        "STABLE = contained high-density region",
        "DIFFUSED = low-to-medium spread region",
        "CALM = low-density observability region",
        "Weather visibility is observational only",
        "Semantic climate visibility != prediction",
    ]

    for i, line in enumerate(legend_lines):
        svg.append(
            f'<text x="{legend_x + 22}" y="{legend_y + 70 + i * 23}" '
            f'fill="#cbd5e1" font-size="13" font-family="Arial, sans-serif">'
            f'• {html.escape(line)}</text>'
        )

    note_x = SVG_WIDTH - 725
    note_y = SVG_HEIGHT - 280
    svg.append(
        f'<rect x="{note_x}" y="{note_y}" width="670" height="235" '
        f'fill="#020617" stroke="#334155" stroke-width="1.5" rx="14" />'
    )
    svg.append(
        f'<text x="{note_x + 22}" y="{note_y + 36}" fill="white" '
        f'font-size="18" font-family="Arial, sans-serif">Containment Notes</text>'
    )

    notes = [
        "Weather labels are semantic terrain states only.",
        "No label predicts operational outcome.",
        "No basin certifies risk, truth, legitimacy, or priority.",
        "Traversal visibility does not define governance workflow.",
        "Rendering preserves observer-only containment.",
        "UNKNOWN → HOLD remains active.",
    ]

    for i, note in enumerate(notes):
        svg.append(
            f'<text x="{note_x + 22}" y="{note_y + 70 + i * 23}" '
            f'fill="#cbd5e1" font-size="13" font-family="Arial, sans-serif">'
            f'• {html.escape(note)}</text>'
        )

    svg.append(
        f'<text x="{CENTER_X}" y="{SVG_HEIGHT - 20}" fill="#94a3b8" font-size="13" '
        f'text-anchor="middle" font-family="Arial, sans-serif">'
        f'Bounded semantic climate visibility only. Semantic climate visibility != prediction.</text>'
    )

    svg.append("</svg>")
    return "\n".join(svg)


def main():
    topology = load_topology()
    svg = render_svg(topology)

    output_dir = BASE_DIR / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    out_file = output_dir / "semantic_topology_v6.svg"
    out_file.write_text(svg, encoding="utf-8")

    print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()