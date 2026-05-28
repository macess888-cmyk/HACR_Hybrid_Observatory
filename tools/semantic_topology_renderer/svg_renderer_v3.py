"""
HACR Hybrid Observatory — SVG Renderer v3

Boundary-shell semantic field renderer.

Invariant:
field rendering != governance authority
"""

from pathlib import Path
import json
import math
import html


BASE_DIR = Path(__file__).resolve().parent

SVG_WIDTH = 1900
SVG_HEIGHT = 1400

CENTER_X = SVG_WIDTH // 2
CENTER_Y = SVG_HEIGHT // 2

OUTER_RADIUS = 470
INNER_RADIUS = 300

MIN_NODE_RADIUS = 50
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


def load_topology() -> dict:
    path = BASE_DIR / "output" / "traversal_topology.json"

    if not path.exists():
        raise FileNotFoundError(
            "Missing traversal topology."
        )

    return json.loads(path.read_text(encoding="utf-8"))


def density_map(topology):
    out = {}

    for item in topology.get("density_analysis", []):
        out[item["region"]] = item

    return out


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


def circular_positions(regions, radius):
    positions = {}

    count = len(regions)

    for i, region in enumerate(regions):
        angle = (2 * math.pi * i) / max(count, 1)

        x = CENTER_X + int(radius * math.cos(angle))
        y = CENTER_Y + int(radius * math.sin(angle))

        positions[region["id"]] = (x, y)

    return positions


def multiline_label(label, max_len=18):
    words = label.split()

    lines = []
    current = ""

    for word in words:
        if len(current + " " + word) <= max_len:
            current = (current + " " + word).strip()
        else:
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
        f'{label}</text>'
    )


def render_svg(topology):
    nodes = topology.get("nodes", [])
    corridors = topology.get("corridors", [])

    density = density_map(topology)

    regions = unique_regions(nodes)

    inner_regions = [r for r in regions if r["id"] in INNER_RING]
    outer_regions = [r for r in regions if r["id"] in OUTER_RING]

    positions = {}

    positions.update(circular_positions(inner_regions, INNER_RADIUS))
    positions.update(circular_positions(outer_regions, OUTER_RADIUS))

    max_count = max(
        density.get(r["id"], {}).get("document_count", 1)
        for r in regions
    )

    svg = []

    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{SVG_WIDTH}" height="{SVG_HEIGHT}" '
        f'viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">'
    )

    svg.append('<rect width="100%" height="100%" fill="#020617" />')

    # Title
    svg.append(
        f'<text x="{CENTER_X}" y="50" fill="white" '
        f'font-size="34" text-anchor="middle" '
        f'font-family="Arial, sans-serif">'
        f'HACR Semantic Field Topology</text>'
    )

    svg.append(
        f'<text x="{CENTER_X}" y="85" fill="#93c5fd" '
        f'font-size="18" text-anchor="middle" '
        f'font-family="Arial, sans-serif">'
        f'Observer-Only • Non-Authoritative • Boundary-Shell Visualization • UNKNOWN → HOLD</text>'
    )

    # Shells
    render_shell(
        svg,
        INNER_RADIUS + 130,
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

    # Corridors
    for corridor in corridors:
        src = corridor["source_region"]
        dst = corridor["target_region"]

        if src not in positions or dst not in positions:
            continue

        x1, y1 = positions[src]
        x2, y2 = positions[dst]

        src_count = density.get(src, {}).get("document_count", 1)
        dst_count = density.get(dst, {}).get("document_count", 1)

        pressure = src_count + dst_count

        width = 2 + min(7, pressure / max(max_count, 1))

        svg.append(
            f'<line x1="{x1}" y1="{y1}" '
            f'x2="{x2}" y2="{y2}" '
            f'stroke="#64748b" '
            f'stroke-width="{width}" '
            f'opacity="0.55" />'
        )

    # Nodes
    for region in regions:
        region_id = region["id"]

        x, y = positions[region_id]

        item = density.get(
            region_id,
            {"document_count": 1, "density_pressure": "LOW"}
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
            f'opacity="0.95" />'
        )

        lines = multiline_label(region["label"])

        svg.append(
            render_multiline_text(
                x,
                y - 6,
                lines,
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

    # Boundary center emphasis
    if "boundary_layer" in positions:
        x, y = positions["boundary_layer"]

        svg.append(
            f'<circle cx="{x}" cy="{y}" '
            f'r="145" fill="none" '
            f'stroke="#f8fafc" stroke-width="2" '
            f'opacity="0.18" />'
        )

    # Footer
    svg.append(
        f'<text x="{CENTER_X}" y="{SVG_HEIGHT - 35}" '
        f'fill="#94a3b8" font-size="13" '
        f'text-anchor="middle" '
        f'font-family="Arial, sans-serif">'
        f'Visual density indicates semantic concentration only. '
        f'Field rendering does not imply authority, governance, or operational legitimacy.'
        f'</text>'
    )

    svg.append("</svg>")

    return "\n".join(svg)


def main():
    topology = load_topology()

    svg = render_svg(topology)

    output_dir = BASE_DIR / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    out_file = output_dir / "semantic_topology_v3.svg"

    out_file.write_text(svg, encoding="utf-8")

    print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()