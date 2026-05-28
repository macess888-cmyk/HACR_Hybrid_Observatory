"""
HACR Hybrid Observatory — SVG Renderer v2

Density-aware bounded semantic topology renderer.

Invariant:
visual density != semantic authority
"""

from pathlib import Path
import json
import math
import html


BASE_DIR = Path(__file__).resolve().parent

SVG_WIDTH = 1800
SVG_HEIGHT = 1300
CENTER_X = SVG_WIDTH // 2
CENTER_Y = SVG_HEIGHT // 2
RADIUS = 430

MIN_NODE_RADIUS = 52
MAX_NODE_RADIUS = 105


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


def load_topology() -> dict:
    path = BASE_DIR / "output" / "traversal_topology.json"

    if not path.exists():
        raise FileNotFoundError(
            "Missing traversal topology. Run traversal_mapper.py first."
        )

    return json.loads(path.read_text(encoding="utf-8"))


def region_density(topology: dict) -> dict:
    density = {}

    for item in topology.get("density_analysis", []):
        density[item["region"]] = {
            "count": item["document_count"],
            "pressure": item["density_pressure"],
        }

    return density


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


def scale_radius(count: int, max_count: int) -> int:
    if max_count <= 0:
        return MIN_NODE_RADIUS

    normalized = count / max_count
    return int(MIN_NODE_RADIUS + (MAX_NODE_RADIUS - MIN_NODE_RADIUS) * math.sqrt(normalized))


def generate_region_positions(regions):
    positions = {}
    count = len(regions)

    for i, region in enumerate(regions):
        angle = (2 * math.pi * i) / max(count, 1)

        x = CENTER_X + int(RADIUS * math.cos(angle))
        y = CENTER_Y + int(RADIUS * math.sin(angle))

        positions[region["id"]] = (x, y)

    return positions


def wrap_label(label: str, max_len: int = 18):
    words = label.split()
    lines = []
    current = ""

    for word in words:
        if len(current + " " + word) <= max_len:
            current = (current + " " + word).strip()
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines[:3]


def svg_text_multiline(x, y, lines, size=14, fill="white"):
    out = []
    start_y = y - ((len(lines) - 1) * size * 0.6)

    for i, line in enumerate(lines):
        out.append(
            f'<text x="{x}" y="{start_y + i * (size + 4)}" '
            f'fill="{fill}" font-size="{size}" text-anchor="middle" '
            f'font-family="Arial, sans-serif">{html.escape(line)}</text>'
        )

    return "\n".join(out)


def render_svg(topology: dict) -> str:
    nodes = topology.get("nodes", [])
    corridors = topology.get("corridors", [])
    traversals = topology.get("reviewer_traversals", [])

    density = region_density(topology)
    regions = unique_regions(nodes)
    positions = generate_region_positions(regions)

    max_count = max((density.get(r["id"], {}).get("count", 1) for r in regions), default=1)

    svg = []

    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">'
    )

    svg.append('<rect width="100%" height="100%" fill="#0f172a" />')

    # Title
    svg.append(
        f'<text x="{CENTER_X}" y="55" fill="white" font-size="32" '
        f'text-anchor="middle" font-family="Arial, sans-serif">'
        f'HACR Semantic Topology — Density Aware</text>'
    )

    # Boundary reminder
    svg.append(
        f'<text x="{CENTER_X}" y="92" fill="#93c5fd" font-size="17" '
        f'text-anchor="middle" font-family="Arial, sans-serif">'
        f'Observer-Only • Non-Authoritative • Bounded Semantic Visualization • UNKNOWN → HOLD</text>'
    )

    # Containment note
    svg.append(
        f'<text x="{CENTER_X}" y="122" fill="#cbd5e1" font-size="13" '
        f'text-anchor="middle" font-family="Arial, sans-serif">'
        f'Visual density indicates document concentration only. Density != authority.</text>'
    )

    # Corridors
    for corridor in corridors:
        src = corridor["source_region"]
        dst = corridor["target_region"]

        if src not in positions or dst not in positions:
            continue

        x1, y1 = positions[src]
        x2, y2 = positions[dst]

        src_count = density.get(src, {}).get("count", 1)
        dst_count = density.get(dst, {}).get("count", 1)

        stroke_width = 2 + min(5, int((src_count + dst_count) / max(max_count, 1) * 4))

        svg.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="#64748b" stroke-width="{stroke_width}" opacity="0.65" />'
        )

    # Region nodes
    for region in regions:
        region_id = region["id"]
        x, y = positions[region_id]

        item = density.get(region_id, {"count": 1, "pressure": "LOW"})
        count = item["count"]
        pressure = item["pressure"]

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
            f'<circle cx="{x}" cy="{y}" r="{radius}" '
            f'fill="{color}" stroke="{stroke}" stroke-width="{stroke_width}" opacity="0.96" />'
        )

        label_lines = wrap_label(region["label"])
        svg.append(svg_text_multiline(x, y - 5, label_lines, size=14))

        svg.append(
            f'<text x="{x}" y="{y + radius - 18}" fill="#e2e8f0" font-size="12" '
            f'text-anchor="middle" font-family="Arial, sans-serif">'
            f'{count} docs • {pressure}</text>'
        )

    # Legend box
    legend_x = 45
    legend_y = SVG_HEIGHT - 220

    svg.append(
        f'<rect x="{legend_x}" y="{legend_y}" width="490" height="175" '
        f'fill="#020617" stroke="#334155" stroke-width="1.5" rx="14" />'
    )

    svg.append(
        f'<text x="{legend_x + 20}" y="{legend_y + 34}" fill="white" font-size="18" '
        f'font-family="Arial, sans-serif">Legend</text>'
    )

    legend_lines = [
        "Node size = document concentration",
        "Line thickness = corridor density relationship",
        "HIGH / MEDIUM / LOW = semantic density pressure",
        "Density visibility is observational only",
        "Rendering does not certify importance, truth, or authority",
    ]

    for i, line in enumerate(legend_lines):
        svg.append(
            f'<text x="{legend_x + 20}" y="{legend_y + 65 + i * 23}" '
            f'fill="#cbd5e1" font-size="13" font-family="Arial, sans-serif">'
            f'{html.escape(line)}</text>'
        )

    # Traversal summary box
    box_x = SVG_WIDTH - 545
    box_y = SVG_HEIGHT - 220

    svg.append(
        f'<rect x="{box_x}" y="{box_y}" width="500" height="175" '
        f'fill="#020617" stroke="#334155" stroke-width="1.5" rx="14" />'
    )

    svg.append(
        f'<text x="{box_x + 20}" y="{box_y + 34}" fill="white" font-size="18" '
        f'font-family="Arial, sans-serif">Reviewer Traversals</text>'
    )

    for i, traversal in enumerate(traversals[:5]):
        svg.append(
            f'<text x="{box_x + 20}" y="{box_y + 65 + i * 22}" '
            f'fill="#cbd5e1" font-size="13" font-family="Arial, sans-serif">'
            f'• {html.escape(traversal["label"])}</text>'
        )

    svg.append("</svg>")

    return "\n".join(svg)


def main() -> None:
    topology = load_topology()
    svg = render_svg(topology)

    output_dir = BASE_DIR / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    out_file = output_dir / "semantic_topology_v2.svg"
    out_file.write_text(svg, encoding="utf-8")

    print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()