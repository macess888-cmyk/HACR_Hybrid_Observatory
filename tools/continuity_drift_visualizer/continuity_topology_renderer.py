from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

SCENARIOS = {
    "regional_supply_chain": {
        "input": ROOT / "tools" / "continuity_drift_visualizer" / "input" / "regional_supply_chain_case.json",
        "output": ROOT / "assets" / "demo_maps" / "regional_supply_chain_topology.svg",
        "receipt": ROOT / "tools" / "continuity_drift_visualizer" / "output" / "regional_supply_chain_topology_receipt.json",
        "title": "Regional Supply Chain Continuity Topology",
    },
    "hospital_continuity": {
        "input": ROOT / "scenarios" / "hospital_continuity" / "json" / "hospital_continuity_case_v1.json",
        "output": ROOT / "scenarios" / "hospital_continuity" / "svg" / "hospital_continuity_topology.svg",
        "receipt": ROOT / "scenarios" / "hospital_continuity" / "receipts" / "hospital_continuity_topology_receipt.json",
        "title": "Hospital Continuity Observability Topology",
    },
    "distributed_hospital_continuity": {
        "input": ROOT / "scenarios" / "distributed_hospital_continuity" / "json" / "distributed_hospital_continuity_case_v1.json",
        "output": ROOT / "scenarios" / "distributed_hospital_continuity" / "svg" / "distributed_hospital_continuity_topology.svg",
        "receipt": ROOT / "scenarios" / "distributed_hospital_continuity" / "receipts" / "distributed_hospital_continuity_topology_receipt.json",
        "title": "Distributed Hospital Continuity Topology",
    },
    "cyber_recoverability": {
        "input": ROOT / "scenarios" / "cyber_recoverability" / "json" / "cyber_recoverability_case_v1.json",
        "output": ROOT / "scenarios" / "cyber_recoverability" / "svg" / "cyber_recoverability_topology.svg",
        "receipt": ROOT / "scenarios" / "cyber_recoverability" / "receipts" / "cyber_recoverability_topology_receipt.json",
        "title": "Cyber Recoverability Continuity Topology",
    },
    "ai_oversight_continuity": {
        "input": ROOT / "scenarios" / "ai_oversight_continuity" / "json" / "ai_oversight_continuity_case_v1.json",
        "output": ROOT / "scenarios" / "ai_oversight_continuity" / "svg" / "ai_oversight_continuity_topology.svg",
        "receipt": ROOT / "scenarios" / "ai_oversight_continuity" / "receipts" / "ai_oversight_continuity_topology_receipt.json",
        "title": "AI Oversight Continuity Topology",
    },
    "energy_grid_recoverability": {
        "input": ROOT / "scenarios" / "energy_grid_recoverability" / "json" / "energy_grid_recoverability_case_v1.json",
        "output": ROOT / "scenarios" / "energy_grid_recoverability" / "svg" / "energy_grid_recoverability_topology.svg",
        "receipt": ROOT / "scenarios" / "energy_grid_recoverability" / "receipts" / "energy_grid_recoverability_topology_receipt.json",
        "title": "Energy Grid Recoverability Topology",
    },
    "emergency_response_continuity": {
        "input": ROOT / "scenarios" / "emergency_response_continuity" / "json" / "emergency_response_continuity_case_v1.json",
        "output": ROOT / "scenarios" / "emergency_response_continuity" / "svg" / "emergency_response_continuity_topology.svg",
        "receipt": ROOT / "scenarios" / "emergency_response_continuity" / "receipts" / "emergency_response_continuity_topology_receipt.json",
        "title": "Emergency Response Continuity Topology",
    },
}

WIDTH = 1200
HEIGHT = 820
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2 + 20
RADIUS = 260
TOPOLOGY_VERTICAL_SHIFT = -35

COLORS = {
    "background": "#f8fafc",
    "grid": "#64748b",
    "panel": "#ffffff",
    "text": "#0f172a",
    "muted": "#475569",
    "edge": "#64748b",
    "critical": "#ef4444",
    "high": "#f97316",
    "medium": "#eab308",
    "shadow": "#8b5cf6",
    "corridor": "#22c55e",
    "degraded": "#ef4444",
    "strained": "#f97316",
    "operational": "#22c55e",
    "partial": "#eab308",
    "unknown": "#94a3b8",
}


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing scenario input: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def group(name: str, content: list[str] | str) -> str:
    body = "\n".join(content) if isinstance(content, list) else content
    return f'<g class="{name}">\n{body}\n</g>'


def state_color(state: str) -> str:
    state = str(state).lower()

    if "degraded" in state or "degrading" in state:
        return COLORS["degraded"]
    if "strained" in state or "constrained" in state or "narrowing" in state:
        return COLORS["strained"]
    if "partial" in state:
        return COLORS["partial"]
    if "operational" in state:
        return COLORS["operational"]

    return COLORS["unknown"]


def node_radius(state: str) -> int:
    state = str(state).lower()

    if "degraded" in state or "degrading" in state:
        return 62
    if "strained" in state or "constrained" in state:
        return 56
    if "partial" in state:
        return 52

    return 46


def dependency_width(level: str) -> int:
    level = str(level).lower()

    if level == "critical":
        return 5
    if level == "high":
        return 4
    if level == "medium":
        return 3

    return 2


def dependency_color(level: str) -> str:
    level = str(level).lower()

    if level == "critical":
        return COLORS["critical"]
    if level == "high":
        return COLORS["high"]
    if level == "medium":
        return COLORS["medium"]

    return COLORS["edge"]


def normalize_shadow_dependency(item) -> str:
    if isinstance(item, str):
        return item.replace("_", " ")

    if isinstance(item, dict):
        source = item.get("source") or item.get("from") or item.get("origin")
        target = item.get("target") or item.get("to") or item.get("destination")
        relation = item.get("relationship_type") or item.get("relationship") or item.get("dependency") or item.get("type")
        criticality = item.get("criticality") or item.get("severity") or item.get("level")

        parts = []

        if source and target:
            parts.append(f"{source} → {target}")
        elif target:
            parts.append(str(target))
        elif source:
            parts.append(str(source))
        else:
            values = [
                str(value).replace("_", " ")
                for value in item.values()
                if isinstance(value, (str, int, float))
            ]
            parts.append(" / ".join(values[:3]) if values else "declared dependency")

        if relation:
            parts.append(str(relation).replace("_", " "))

        if criticality:
            parts.append(f"criticality: {str(criticality).replace('_', ' ')}")

        return " — ".join(parts)

    return str(item).replace("_", " ")


def polar_layout(nodes: list[dict]) -> dict[str, tuple[float, float]]:
    positions = {}
    total = max(len(nodes), 1)

    for index, node in enumerate(nodes):
        angle = -math.pi / 2 + (2 * math.pi * index / total)
        x = CENTER_X + RADIUS * math.cos(angle)
        y = CENTER_Y + TOPOLOGY_VERTICAL_SHIFT + RADIUS * math.sin(angle)
        positions[node["id"]] = (x, y)

    return positions


def shorten_line(x1, y1, x2, y2, source_radius, target_radius):
    dx = x2 - x1
    dy = y2 - y1
    distance = math.hypot(dx, dy)

    if distance == 0:
        return x1, y1, x2, y2

    ux = dx / distance
    uy = dy / distance

    return (
        x1 + ux * source_radius,
        y1 + uy * source_radius,
        x2 - ux * target_radius,
        y2 - uy * target_radius,
    )


def svg_text(x, y, text, size=14, weight="400", anchor="middle", color=None):
    color = color or COLORS["text"]

    return (
        f'<text x="{x:.1f}" y="{y:.1f}" '
        f'font-family="Inter, Arial, sans-serif" '
        f'font-size="{size}" '
        f'font-weight="{weight}" '
        f'text-anchor="{anchor}" '
        f'fill="{color}">{escape(str(text))}</text>'
    )


def svg_line(
    x1,
    y1,
    x2,
    y2,
    color,
    width=2,
    dashed=False,
    opacity=0.9,
    arrow=False,
    tooltip=""
):
    dash = ' stroke-dasharray="7,5"' if dashed else ""
    marker = ' marker-end="url(#arrowhead)"' if arrow else ""
    title = f"<title>{escape(tooltip)}</title>" if tooltip else ""

    return (
        f'<line '
        f'x1="{x1:.1f}" y1="{y1:.1f}" '
        f'x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" '
        f'stroke-width="{width}" '
        f'opacity="{opacity}"'
        f'{dash}{marker}>'
        f'{title}</line>'
    )


def svg_node(x, y, node):
    node_id = node.get("id", "unknown")
    node_type = node.get("type", "node")
    state = node.get("state", "unknown")

    fill = state_color(state)
    radius = node_radius(state)

    tooltip = (
        f"Node: {node_id}\n"
        f"Type: {node_type}\n"
        f"State: {state}\n"
        f"Observer-only continuity visibility"
    )

    return "\n".join([
        f'<g class="node-inspection">',
        f'<title>{escape(tooltip)}</title>',
        f'<circle '
        f'cx="{x:.1f}" '
        f'cy="{y:.1f}" '
        f'r="{radius}" '
        f'fill="{fill}" '
        f'opacity="0.18" '
        f'stroke="{fill}" '
        f'stroke-width="3" />',
        svg_text(x, y - 6, node_id, size=15, weight="700"),
        svg_text(x, y + 14, node_type.replace("_", " "), size=11, color=COLORS["muted"]),
        svg_text(x, y + 30, state, size=11, color=COLORS["muted"]),
        "</g>"
    ])


def render_defs():
    return """
<defs>
  <style>
    .node-inspection:hover circle {
      stroke-width: 5;
      opacity: 0.28;
    }
  </style>

  <marker id="arrowhead"
          markerWidth="10"
          markerHeight="10"
          refX="8"
          refY="3"
          orient="auto"
          markerUnits="strokeWidth">
    <path d="M0,0 L0,6 L9,3 z"
          fill="#64748b"
          opacity="0.65" />
  </marker>
</defs>
""".strip()


def render_background_grid():
    lines = []
    spacing = 80

    for x in range(0, WIDTH + spacing, spacing):
        lines.append(
            f'<line x1="{x}" y1="0" x2="{x}" y2="{HEIGHT}" '
            f'stroke="{COLORS["grid"]}" '
            f'stroke-width="1" opacity="0.02" />'
        )

    for y in range(0, HEIGHT + spacing, spacing):
        lines.append(
            f'<line x1="0" y1="{y}" x2="{WIDTH}" y2="{y}" '
            f'stroke="{COLORS["grid"]}" '
            f'stroke-width="1" opacity="0.02" />'
        )

    return group("layer-grid", lines)


def render_pressure_panel(data: dict) -> str:
    pressure = data.get("continuity_pressure", {})
    recoverability = data.get("recoverability_state", {})

    lines = [
        '<rect x="40" y="100" width="310" height="250" rx="18" fill="#ffffff" stroke="#cbd5e1" />',
        svg_text(195, 132, "Continuity Pressure", size=17, weight="700"),
    ]

    y = 168

    for key, value in pressure.items():
        label = key.replace("_", " ")

        if isinstance(value, (int, float)):
            bar_width = max(0, min(1, float(value))) * 125
            lines.append(svg_text(65, y, label, size=11, anchor="start", color=COLORS["muted"]))
            lines.append(f'<rect x="210" y="{y - 10}" width="125" height="10" rx="5" fill="#e2e8f0" />')
            lines.append(f'<rect x="210" y="{y - 10}" width="{bar_width:.1f}" height="10" rx="5" fill="#64748b" />')
        else:
            lines.append(svg_text(65, y, f"{label}: {value}", size=12, anchor="start", color=COLORS["muted"]))

        y += 30

    y += 12
    lines.append(svg_text(195, y, "Recoverability State", size=15, weight="700"))
    y += 28

    for key, value in recoverability.items():
        lines.append(svg_text(65, y, f"{key.replace('_', ' ')}: {value}", size=12, anchor="start", color=COLORS["muted"]))
        y += 24

    return group("layer-panels layer-text", lines)


def render_shadow_panel(data: dict) -> str:
    shadows = data.get("shadow_dependencies", [])

    lines = [
        '<rect x="850" y="100" width="310" height="250" rx="18" fill="#ffffff" stroke="#cbd5e1" />',
        svg_text(1005, 132, "Shadow Dependencies", size=17, weight="700"),
    ]

    y = 170

    if not shadows:
        lines.append(svg_text(1005, y, "None declared", size=13, color=COLORS["muted"]))
    else:
        for item in shadows[:6]:
            label = normalize_shadow_dependency(item)
            if len(label) > 42:
                label = label[:39] + "..."
            lines.append(svg_text(880, y, f"• {label}", size=12, anchor="start", color=COLORS["muted"]))
            y += 28

    return group("layer-panels layer-shadow layer-text", lines)


def render_legend_panel() -> str:
    x = 40
    y = HEIGHT - 295

    lines = [
        f'<rect x="{x}" y="{y}" width="310" height="210" rx="18" fill="#ffffff" stroke="#cbd5e1" />',
        svg_text(x + 155, y + 30, "Topology Legend", size=16, weight="700"),
    ]

    legend_items = [
        ("Operational", COLORS["operational"]),
        ("Strained", COLORS["strained"]),
        ("Degrading", COLORS["degraded"]),
    ]

    current_y = y + 62

    for label, color in legend_items:
        lines.append(
            f'<circle cx="{x + 28}" cy="{current_y}" r="10" fill="{color}" opacity="0.35" stroke="{color}" stroke-width="2" />'
        )
        lines.append(svg_text(x + 50, current_y + 5, label, size=12, anchor="start", color=COLORS["muted"]))
        current_y += 28

    lines.append(svg_line(x + 18, current_y + 8, x + 52, current_y + 8, COLORS["corridor"], width=4, dashed=True, opacity=0.35))
    lines.append(svg_text(x + 65, current_y + 13, "Recoverability Corridor", size=12, anchor="start", color=COLORS["muted"]))

    current_y += 28

    lines.append(svg_line(x + 18, current_y + 8, x + 52, current_y + 8, COLORS["shadow"], width=3, dashed=True, opacity=0.35))
    lines.append(svg_text(x + 65, current_y + 13, "Shadow Dependency Visibility", size=12, anchor="start", color=COLORS["muted"]))

    return group("layer-panels layer-text", lines)


def render_metadata_panel(data: dict) -> str:
    x = WIDTH - 350
    y = HEIGHT - 295

    lines = [
        f'<rect x="{x}" y="{y}" width="310" height="210" rx="18" fill="#ffffff" stroke="#cbd5e1" />',
        svg_text(x + 155, y + 30, "Scenario Metadata", size=16, weight="700"),
    ]

    metadata = [
        f"scenario id: {data.get('scenario_id', 'unknown')}",
        f"scenario domain: {data.get('scenario_type', 'continuity observability')}",
        "render mode: deterministic",
        "observer-only: true",
        "receipt generation: enabled",
        "topology type: continuity observability",
    ]

    current_y = y + 62

    for item in metadata:
        if len(item) > 43:
            item = item[:40] + "..."
        lines.append(svg_text(x + 20, current_y, item, size=12, anchor="start", color=COLORS["muted"]))
        current_y += 22

    return group("layer-panels layer-text", lines)


def render_recovery_corridor(positions: dict[str, tuple[float, float]]) -> str:
    if len(positions) < 2:
        return ""

    points = " ".join(f"{x:.1f},{y:.1f}" for x, y in positions.values())

    lines = [
        (
            f'<polygon points="{points}" fill="{COLORS["corridor"]}" fill-opacity="0.05" '
            f'stroke="{COLORS["corridor"]}" stroke-width="5" '
            f'stroke-dasharray="10,7" opacity="0.18">'
            f"<title>Recoverability corridor: bounded visibility field only. Not a prediction or guarantee.</title></polygon>"
        ),
        svg_text(WIDTH / 2, CENTER_Y + 185, "Recoverability Corridor", size=13, color=COLORS["corridor"]),
    ]

    return group("layer-corridor layer-text", lines)


def render_edges(edges, positions, node_by_id):
    lines = []

    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")
        level = edge.get("dependency", "medium")

        if source in positions and target in positions:
            x1, y1 = positions[source]
            x2, y2 = positions[target]

            source_radius = node_radius(node_by_id[source].get("state", "unknown"))
            target_radius = node_radius(node_by_id[target].get("state", "unknown"))

            sx1, sy1, sx2, sy2 = shorten_line(
                x1,
                y1,
                x2,
                y2,
                source_radius,
                target_radius + 6
            )

            tooltip = (
                f"Dependency: {source} → {target}\n"
                f"Dependency level: {level}\n"
                f"Observer-only dependency visibility"
            )

            lines.append(
                svg_line(
                    sx1,
                    sy1,
                    sx2,
                    sy2,
                    dependency_color(level),
                    dependency_width(level),
                    opacity=0.55,
                    arrow=True,
                    tooltip=tooltip,
                )
            )

    return group("layer-edges", lines)


def render_nodes(nodes, positions):
    rendered = []

    for node in nodes:
        node_id = node.get("id")

        if node_id in positions:
            x, y = positions[node_id]
            rendered.append(svg_node(x, y, node))

    return group("layer-nodes layer-text", rendered)


def render_shadow_footer() -> str:
    shadow_y = HEIGHT - 58

    lines = [
        svg_text(
            WIDTH / 2,
            shadow_y,
            "Dashed boundary: shadow dependencies are visible but non-authoritative",
            size=13,
            color=COLORS["muted"]
        ),
        svg_line(
            WIDTH / 2 - 210,
            shadow_y + 22,
            WIDTH / 2 + 210,
            shadow_y + 22,
            COLORS["shadow"],
            width=3,
            dashed=True,
            opacity=0.35
        ),
    ]

    return group("layer-shadow layer-text", lines)


def render_footer_text() -> str:
    return group(
        "layer-footer layer-text",
        [
            svg_text(
                WIDTH / 2,
                HEIGHT - 32,
                "NON-CLAIM: This does not predict, govern, authorize, certify, or replace operators.",
                size=13,
                weight="700",
                color=COLORS["muted"]
            ),
            svg_text(
                WIDTH / 2,
                HEIGHT - 12,
                "Visible continuity does not prove preserved recoverability.",
                size=13,
                color=COLORS["muted"]
            ),
        ],
    )


def render_svg(data: dict, title: str):
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    positions = polar_layout(nodes)
    node_by_id = {node.get("id"): node for node in nodes}

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        render_defs(),
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{COLORS["background"]}" />',
        render_background_grid(),
        group(
            "layer-title layer-text",
            [
                svg_text(WIDTH / 2, 48, title, size=26, weight="800"),
                svg_text(
                    WIDTH / 2,
                    78,
                    "Observer-only bounded deterministic operational continuity inspection",
                    size=14,
                    color=COLORS["muted"]
                ),
            ],
        ),
        render_pressure_panel(data),
        render_shadow_panel(data),
        render_legend_panel(),
        render_metadata_panel(data),
        render_recovery_corridor(positions),
        render_edges(edges, positions, node_by_id),
        render_shadow_footer(),
        render_nodes(nodes, positions),
        render_footer_text(),
        "</svg>",
    ]

    return "\n".join(part for part in parts if part)


def write_receipt(data, svg, scenario_key, paths):
    receipt = {
        "scenario_key": scenario_key,
        "scenario_id": data.get("scenario_id", scenario_key),
        "scenario_type": data.get("scenario_type", "continuity_observability"),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "observer_only": True,
        "non_authoritative": True,
        "input_path": str(paths["input"].relative_to(ROOT)),
        "output_path": str(paths["output"].relative_to(ROOT)),
        "svg_sha256": sha256_text(svg),
        "node_count": len(data.get("nodes", [])),
        "edge_count": len(data.get("edges", [])),
        "svg_features": {
            "native_node_tooltips": True,
            "native_edge_tooltips": True,
            "hover_node_emphasis": True,
            "deterministic_svg_output": True,
        },
        "non_claims": {
            "not_predictive": True,
            "not_governance": True,
            "not_authorization": True,
            "not_certification": True,
            "not_operator_replacement": True,
        },
    }

    paths["receipt"].parent.mkdir(parents=True, exist_ok=True)

    paths["receipt"].write_text(
        json.dumps(receipt, indent=2),
        encoding="utf-8"
    )


def render_scenario(scenario_key):
    paths = SCENARIOS[scenario_key]
    data = load_json(paths["input"])
    svg = render_svg(data, paths["title"])

    paths["output"].parent.mkdir(parents=True, exist_ok=True)
    paths["output"].write_text(svg, encoding="utf-8")

    write_receipt(data, svg, scenario_key, paths)

    print(f"Rendered: {paths['output']}")
    print(f"Receipt:  {paths['receipt']}")


def main():
    for scenario_key, paths in SCENARIOS.items():
        if paths["input"].exists():
            render_scenario(scenario_key)
        else:
            print(f"Skipped missing scenario input: {paths['input']}")


if __name__ == "__main__":
    main()