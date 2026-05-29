"""
HACR Hybrid Observatory — SVG Renderer v10

Temporal ecology renderer.

Invariant:
temporal ecology visibility != prediction
"""

from pathlib import Path
import json
import math
import html


BASE_DIR = Path(__file__).resolve().parent

SVG_WIDTH = 2200
SVG_HEIGHT = 1650
CENTER_X = SVG_WIDTH // 2
CENTER_Y = SVG_HEIGHT // 2

OUTER_RADIUS = 545
INNER_RADIUS = 345

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


OBSERVATION_WINDOWS = [
    ("T0", "Baseline"),
    ("T1", "Boundary Expansion"),
    ("T2", "Verification Hardening"),
    ("T3", "Semantic Topology"),
    ("T4", "Ecology Stabilization"),
]


CLIMATE_FRONTS = [
    {"label": "STABILIZATION FRONT", "color": "#38bdf8", "radius": 405, "start": 210, "end": 335, "opacity": 0.34},
    {"label": "TURBULENCE FRONT", "color": "#facc15", "radius": 565, "start": 145, "end": 245, "opacity": 0.28},
    {"label": "CONGESTION WAVE", "color": "#f97316", "radius": 615, "start": 250, "end": 355, "opacity": 0.26},
    {"label": "DIFFUSION BAND", "color": "#a78bfa", "radius": 470, "start": 25, "end": 120, "opacity": 0.24},
    {"label": "CALM BASIN", "color": "#22c55e", "radius": 360, "start": 40, "end": 115, "opacity": 0.22},
]


BRAIDED_CURRENTS = [
    {"label": "Canonical Current", "regions": ["canonical_layer", "semantic_topology_layer", "reviewer_traversability_layer", "boundary_layer"], "color": "#38bdf8"},
    {"label": "Canonical Side Braid", "regions": ["canonical_layer", "semantic_topology_layer", "boundary_layer"], "color": "#38bdf8"},
    {"label": "Containment Current", "regions": ["canonical_layer", "boundary_layer", "runtime_constraints_layer", "verification_layer"], "color": "#facc15"},
    {"label": "Containment Side Braid", "regions": ["canonical_layer", "runtime_constraints_layer", "boundary_layer"], "color": "#facc15"},
    {"label": "Engineering Current", "regions": ["runtime_reduction_layer", "runtime_constraints_layer", "verification_layer", "boundary_layer"], "color": "#22c55e"},
    {"label": "Engineering Return Braid", "regions": ["runtime_reduction_layer", "runtime_constraints_layer", "boundary_layer"], "color": "#22c55e"},
    {"label": "Semantic Current", "regions": ["semantic_topology_layer", "governance_observability_region", "documentation_region", "boundary_layer"], "color": "#a78bfa"},
    {"label": "Semantic Side Braid", "regions": ["semantic_topology_layer", "documentation_region", "boundary_layer"], "color": "#a78bfa"},
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
            seen[region] = {"id": region, "label": region.replace("_", " ").title()}
    return list(seen.values())


def density_count(density, region_id):
    return density.get(region_id, {}).get("document_count", 1)


def density_pressure(density, region_id):
    return density.get(region_id, {}).get("density_pressure", "LOW")


def climate_state(count, pressure):
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


def adaptive_offset(count, max_count, region_id):
    pressure = count / max(max_count, 1)

    if region_id in {"tooling_region", "governance_observability_region"}:
        return int(30 * pressure), int(-20 * pressure)
    if region_id in {"boundary_layer", "documentation_region"}:
        return int(-18 * pressure), int(22 * pressure)

    return int(10 * pressure), int(8 * pressure)


def circular_positions(regions, radius, offset=0, density=None, max_count=1):
    positions = {}
    count = len(regions)

    for i, region in enumerate(regions):
        angle = offset + (2 * math.pi * i) / max(count, 1)
        x = CENTER_X + int(radius * math.cos(angle))
        y = CENTER_Y + int(radius * math.sin(angle))

        if density is not None:
            doc_count = density_count(density, region["id"])
            dx, dy = adaptive_offset(doc_count, max_count, region["id"])
            x += dx
            y += dy

        positions[region["id"]] = (x, y)

    return positions


def polar_point(radius, degrees):
    angle = math.radians(degrees)
    return CENTER_X + radius * math.cos(angle), CENTER_Y + radius * math.sin(angle)


def arc_path(radius, start_deg, end_deg, deflection=0):
    start = polar_point(radius + deflection, start_deg)
    end = polar_point(radius - deflection, end_deg)
    large_arc = 1 if abs(end_deg - start_deg) > 180 else 0
    return f"M {start[0]:.2f} {start[1]:.2f} A {radius} {radius} 0 {large_arc} 1 {end[0]:.2f} {end[1]:.2f}"


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


def render_climate_front(svg, front, index):
    deflection = [8, -14, 18, -10, 6][index % 5]
    path = arc_path(front["radius"], front["start"], front["end"], deflection=deflection)

    svg.append(
        f'<path d="{path}" fill="none" stroke="{front["color"]}" '
        f'stroke-width="20" opacity="{front["opacity"]}" stroke-linecap="round" />'
    )
    svg.append(
        f'<path d="{path}" fill="none" stroke="{front["color"]}" '
        f'stroke-width="4" opacity="{min(front["opacity"] + 0.25, 0.7)}" stroke-linecap="round" />'
    )

    mid = (front["start"] + front["end"]) / 2
    lx, ly = polar_point(front["radius"] + 32, mid)

    svg.append(
        f'<text x="{lx:.2f}" y="{ly:.2f}" fill="{front["color"]}" '
        f'font-size="12" text-anchor="middle" '
        f'font-family="Arial, sans-serif">{html.escape(front["label"])}</text>'
    )


def curved_path(points, bend=0):
    if len(points) < 2:
        return ""

    d = f"M {points[0][0]} {points[0][1]}"

    for i in range(1, len(points)):
        x1, y1 = points[i - 1]
        x2, y2 = points[i]
        mx = (x1 + x2) / 2 + bend
        my = (y1 + y2) / 2 - bend
        d += f" Q {mx:.2f} {my:.2f} {x2:.2f} {y2:.2f}"

    return d


def render_current(svg, positions, current, index):
    points = [positions[r] for r in current["regions"] if r in positions]
    if len(points) < 2:
        return

    bend = ((index % 4) - 1.5) * 18
    path = curved_path(points, bend=bend)

    svg.append(
        f'<path d="{path}" fill="none" stroke="{current["color"]}" '
        f'stroke-width="20" opacity="0.08" stroke-linecap="round" stroke-linejoin="round" />'
    )
    svg.append(
        f'<path d="{path}" fill="none" stroke="{current["color"]}" '
        f'stroke-width="5" opacity="0.40" stroke-linecap="round" stroke-linejoin="round" />'
    )


def render_temporal_windows(svg):
    x = 70
    y = 145

    svg.append(
        f'<rect x="{x}" y="{y}" width="430" height="190" '
        f'fill="#020617" stroke="#334155" stroke-width="1.5" rx="14" />'
    )
    svg.append(
        f'<text x="{x + 22}" y="{y + 36}" fill="white" '
        f'font-size="18" font-family="Arial, sans-serif">Replay Observation Windows</text>'
    )

    for i, (label, text) in enumerate(OBSERVATION_WINDOWS):
        yy = y + 70 + i * 24
        svg.append(
            f'<text x="{x + 24}" y="{yy}" fill="#93c5fd" font-size="13" '
            f'font-family="Arial, sans-serif">{html.escape(label)}</text>'
        )
        svg.append(
            f'<text x="{x + 70}" y="{yy}" fill="#cbd5e1" font-size="13" '
            f'font-family="Arial, sans-serif">{html.escape(text)}</text>'
        )


def render_svg(topology):
    nodes = topology.get("nodes", [])
    corridors = topology.get("corridors", [])
    density = density_map(topology)
    regions = unique_regions(nodes)

    max_count = max((density_count(density, r["id"]) for r in regions), default=1)

    inner_regions = [r for r in regions if r["id"] in INNER_RING]
    outer_regions = [r for r in regions if r["id"] in OUTER_RING]

    positions = {}
    positions.update(circular_positions(inner_regions, INNER_RADIUS, offset=0.1, density=density, max_count=max_count))
    positions.update(circular_positions(outer_regions, OUTER_RADIUS, offset=-0.25, density=density, max_count=max_count))

    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" '
        f'viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">'
    )
    svg.append('<rect width="100%" height="100%" fill="#020617" />')

    svg.append(
        f'<text x="{CENTER_X}" y="50" fill="white" font-size="34" '
        f'text-anchor="middle" font-family="Arial, sans-serif">HACR Temporal Ecology</text>'
    )
    svg.append(
        f'<text x="{CENTER_X}" y="86" fill="#93c5fd" font-size="18" '
        f'text-anchor="middle" font-family="Arial, sans-serif">'
        f'Observer-Only • Non-Authoritative • Temporal Ecology Visibility • UNKNOWN → HOLD</text>'
    )
    svg.append(
        f'<text x="{CENTER_X}" y="112" fill="#cbd5e1" font-size="13" '
        f'text-anchor="middle" font-family="Arial, sans-serif">'
        f'Temporal ecology visibility is replay-window visibility only. It does not imply prediction, causality, governance, or operational truth.</text>'
    )

    render_temporal_windows(svg)

    render_shell(svg, INNER_RADIUS + 135, "#475569", 0.45, "Containment / Coordination Shell")
    render_shell(svg, OUTER_RADIUS + 120, "#334155", 0.35, "Peripheral Semantic Field")

    for index, front in enumerate(CLIMATE_FRONTS):
        render_climate_front(svg, front, index)

    for region in regions:
        region_id = region["id"]
        if region_id not in positions:
            continue

        x, y = positions[region_id]
        count = density_count(density, region_id)
        pressure = density_pressure(density, region_id)
        state = climate_state(count, pressure)
        radius = scale_radius(count, max_count)

        if state in {"CONGESTED", "TURBULENT"}:
            svg.append(
                f'<ellipse cx="{x}" cy="{y}" rx="{radius + 115}" ry="{radius + 58}" '
                f'fill="#fef3c7" opacity="0.055" transform="rotate(-22 {x} {y})" />'
            )

        if state == "CONGESTED":
            opacity, rx, ry, color = 0.20, radius + 78, radius + 42, "#fef3c7"
        elif state == "TURBULENT":
            opacity, rx, ry, color = 0.16, radius + 54, radius + 32, "#fde68a"
        elif state == "STABLE":
            opacity, rx, ry, color = 0.10, radius + 34, radius + 34, "#bfdbfe"
        elif state == "DIFFUSED":
            opacity, rx, ry, color = 0.08, radius + 28, radius + 20, "#93c5fd"
        else:
            opacity, rx, ry, color = 0.05, radius + 18, radius + 14, "#94a3b8"

        svg.append(
            f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" '
            f'fill="{color}" opacity="{opacity}" transform="rotate(-24 {x} {y})" />'
        )

    for corridor in corridors:
        src = corridor["source_region"]
        dst = corridor["target_region"]
        if src not in positions or dst not in positions:
            continue

        x1, y1 = positions[src]
        x2, y2 = positions[dst]

        svg.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="#475569" stroke-width="2.3" opacity="0.30" />'
        )

    for index, current in enumerate(BRAIDED_CURRENTS):
        render_current(svg, positions, current, index)

    for region in regions:
        region_id = region["id"]
        if region_id not in positions:
            continue

        x, y = positions[region_id]
        count = density_count(density, region_id)
        pressure = density_pressure(density, region_id)
        state = climate_state(count, pressure)
        radius = scale_radius(count, max_count)
        color = REGION_COLORS.get(region_id, "#64748b")

        stroke = "#e5e7eb"
        stroke_width = 2
        if pressure == "HIGH":
            stroke, stroke_width = "#fef3c7", 4
        elif pressure == "MEDIUM":
            stroke, stroke_width = "#bfdbfe", 3

        svg.append(
            f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" '
            f'stroke="{stroke}" stroke-width="{stroke_width}" opacity="0.96" />'
        )

        svg.append(text_lines(x, y - 12, multiline_label(region["label"]), size=14))

        svg.append(
            f'<text x="{x}" y="{y + radius - 30}" fill="#e2e8f0" font-size="12" '
            f'text-anchor="middle" font-family="Arial, sans-serif">{count} docs • {pressure}</text>'
        )
        svg.append(
            f'<text x="{x}" y="{y + radius - 14}" fill="#fef3c7" font-size="11" '
            f'text-anchor="middle" font-family="Arial, sans-serif">{state}</text>'
        )

    legend_x = 55
    legend_y = SVG_HEIGHT - 315
    svg.append(
        f'<rect x="{legend_x}" y="{legend_y}" width="810" height="270" '
        f'fill="#020617" stroke="#334155" stroke-width="1.5" rx="14" />'
    )
    svg.append(
        f'<text x="{legend_x + 22}" y="{legend_y + 36}" fill="white" '
        f'font-size="18" font-family="Arial, sans-serif">Temporal Ecology Legend</text>'
    )

    legend_lines = [
        "Observation windows show replayable ecology stages only",
        "Temporal visibility does not predict future repository behavior",
        "Fronts, basins, currents, and fog remain observational descriptors",
        "Ecology drift visibility does not imply causality",
        "Temporal ecology visibility != prediction",
    ]

    for i, line in enumerate(legend_lines):
        svg.append(
            f'<text x="{legend_x + 22}" y="{legend_y + 72 + i * 25}" '
            f'fill="#cbd5e1" font-size="13" font-family="Arial, sans-serif">• {html.escape(line)}</text>'
        )

    note_x = SVG_WIDTH - 865
    note_y = SVG_HEIGHT - 315
    svg.append(
        f'<rect x="{note_x}" y="{note_y}" width="810" height="270" '
        f'fill="#020617" stroke="#334155" stroke-width="1.5" rx="14" />'
    )
    svg.append(
        f'<text x="{note_x + 22}" y="{note_y + 36}" fill="white" '
        f'font-size="18" font-family="Arial, sans-serif">Containment Notes</text>'
    )

    notes = [
        "Temporal ecology is replay-window visibility only.",
        "No window predicts operational outcome.",
        "No drift certifies causality, truth, legitimacy, risk, or priority.",
        "Currents do not define governance workflow.",
        "Observer-only containment remains active.",
        "UNKNOWN → HOLD remains active.",
    ]

    for i, note in enumerate(notes):
        svg.append(
            f'<text x="{note_x + 22}" y="{note_y + 72 + i * 25}" '
            f'fill="#cbd5e1" font-size="13" font-family="Arial, sans-serif">• {html.escape(note)}</text>'
        )

    svg.append(
        f'<text x="{CENTER_X}" y="{SVG_HEIGHT - 20}" fill="#94a3b8" font-size="13" '
        f'text-anchor="middle" font-family="Arial, sans-serif">'
        f'Bounded temporal ecology visibility only. Temporal ecology visibility != prediction.</text>'
    )

    svg.append("</svg>")
    return "\n".join(svg)


def main():
    topology = load_topology()
    svg = render_svg(topology)

    output_dir = BASE_DIR / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    out_file = output_dir / "semantic_topology_v10.svg"
    out_file.write_text(svg, encoding="utf-8")

    print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()