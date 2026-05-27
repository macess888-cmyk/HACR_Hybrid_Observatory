import json
import math
import hashlib
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "input" / "regional_supply_chain_case.json"
OUTPUT_PATH = ROOT / "output" / "regional_supply_chain_topology.svg"
RECEIPT_PATH = ROOT / "output" / "regional_supply_chain_topology_receipt.json"


def clamp(value, minimum=0.0, maximum=1.0):
    return max(minimum, min(maximum, float(value)))


def load_case(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def node_color(recoverability, dependency_exposure):
    recoverability = clamp(recoverability)
    dependency_exposure = clamp(dependency_exposure)

    if recoverability < 0.35 or dependency_exposure > 0.80:
        return "#ff453a"
    if recoverability < 0.55 or dependency_exposure > 0.65:
        return "#ff9f0a"
    return "#35c759"


def edge_color(fragility):
    fragility = clamp(fragility)

    if fragility > 0.75:
        return "#ff453a"
    if fragility > 0.50:
        return "#ff9f0a"
    return "#35c759"


def build_layout(nodes, width=1400, height=1040):
    center_x = width / 2
    center_y = height / 2 - 60
    radius = 285
    positions = {}

    for index, node in enumerate(nodes):
        angle = (2 * math.pi * index / len(nodes)) - math.pi / 2
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        positions[node["id"]] = (x, y)

    return positions


def build_drift_panel(time_steps):
    if not time_steps:
        return ""

    x = 40
    y = 780

    parts = [
        f'<rect x="{x}" y="{y}" width="420" height="155" rx="16" fill="#151d33" stroke="#2d3a5f"/>',
        f'<text x="{x + 25}" y="{y + 35}" class="label">Drift Progression</text>'
    ]

    row_y = y + 65
    for step in time_steps:
        label = step.get("label", f"Step {step.get('step', '?')}")
        avg = (
            clamp(step.get("primary_supplier_recoverability", 0))
            + clamp(step.get("delivery_route_recoverability", 0))
            + clamp(step.get("manual_coordination_recoverability", 0))
        ) / 3

        color = node_color(avg, 1 - avg)
        bar_width = int(avg * 220)

        parts.append(f'<text x="{x + 25}" y="{row_y}" class="small">{label}</text>')
        parts.append(f'<rect x="{x + 170}" y="{row_y - 12}" width="220" height="14" rx="7" fill="#25314f"/>')
        parts.append(f'<rect x="{x + 170}" y="{row_y - 12}" width="{bar_width}" height="14" rx="7" fill="{color}"/>')
        row_y += 32

    return "\n".join(parts)


def build_human_oversight_panel(oversight):
    if not oversight:
        return ""

    x = 500
    y = 780

    interruption = clamp(oversight.get("interruption_authority", 0))
    visibility = clamp(oversight.get("decision_visibility", 0))
    recovery = clamp(oversight.get("manual_recovery_capacity", 0))

    avg = round((interruption + visibility + recovery) / 3, 2)
    color = node_color(avg, 1 - avg)

    return f'''
  <rect x="{x}" y="{y}" width="390" height="155" rx="16" fill="#151d33" stroke="#2d3a5f"/>
  <text x="{x + 25}" y="{y + 35}" class="label">Human Oversight Boundary</text>
  <text x="{x + 25}" y="{y + 70}" class="small">Interruption authority: {interruption}</text>
  <text x="{x + 25}" y="{y + 95}" class="small">Decision visibility: {visibility}</text>
  <text x="{x + 25}" y="{y + 120}" class="small">Manual recovery capacity: {recovery}</text>
  <text x="{x + 250}" y="{y + 105}" class="metric" fill="{color}">Score {avg}</text>
'''


def build_svg(case):
    width = 1400
    height = 1040

    nodes = case.get("nodes", [])
    edges = case.get("edges", [])
    shadow_edges = case.get("shadow_dependencies", [])
    reductions = case.get("core_reductions", [])
    positions = build_layout(nodes, width, height)

    svg_parts = []

    svg_parts.append(f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .title {{ font: bold 32px Arial, sans-serif; fill: #ffffff; }}
    .subtitle {{ font: 17px Arial, sans-serif; fill: #cfd8ff; }}
    .label {{ font: bold 15px Arial, sans-serif; fill: #ffffff; }}
    .small {{ font: 12px Arial, sans-serif; fill: #d0d0d0; }}
    .metric {{ font: bold 13px Arial, sans-serif; fill: #ffffff; }}
  </style>

  <rect width="100%" height="100%" fill="#0b1020"/>

  <text x="50" y="55" class="title">Continuity Drift Topology Renderer</text>
  <text x="50" y="88" class="subtitle">Observer-only dependency and recoverability visualization | deterministic demo output</text>
  <text x="50" y="125" class="small">Case: {case.get("case_name", "Unnamed Case")}</text>
  <text x="50" y="148" class="small">Visible operational status: {case.get("visible_operational_status", "unknown")}</text>
''')

    center_x = width / 2
    center_y = height / 2 - 60

    for r, opacity in [(330, 0.08), (250, 0.10), (170, 0.12)]:
        svg_parts.append(
            f'<circle cx="{center_x}" cy="{center_y}" r="{r}" fill="none" stroke="#7aa2ff" stroke-width="1" opacity="{opacity}"/>\n'
        )

    for edge in edges:
        source = edge.get("from")
        target = edge.get("to")
        if source not in positions or target not in positions:
            continue

        x1, y1 = positions[source]
        x2, y2 = positions[target]
        fragility = clamp(edge.get("interruption_fragility", 0.0))
        strength = clamp(edge.get("strength", 0.0))
        color = edge_color(fragility)
        stroke_width = 2 + (strength * 5)

        svg_parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{stroke_width}" opacity="0.65"/>\n'
        )

    for edge in shadow_edges:
        source = edge.get("from")
        target = edge.get("to")
        if source not in positions or target not in positions:
            continue

        x1, y1 = positions[source]
        x2, y2 = positions[target]
        risk = clamp(edge.get("risk", 0.0))
        visibility = clamp(edge.get("visibility", 0.0))
        opacity = 0.25 + risk * 0.5

        svg_parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="#bf5cff" stroke-width="{2 + risk * 5}" '
            f'opacity="{opacity}" stroke-dasharray="9 7"/>\n'
        )

        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2

        svg_parts.append(
            f'<text x="{mid_x}" y="{mid_y}" class="small" text-anchor="middle" fill="#d8b4ff">'
            f'shadow:{edge.get("relationship", "hidden_dependency")} V:{visibility}</text>\n'
        )

    for node in nodes:
        node_id = node.get("id")
        x, y = positions[node_id]

        recoverability = clamp(node.get("recoverability", 0.0))
        dependency = clamp(node.get("dependency_exposure", 0.0))
        continuity_pressure = clamp(node.get("continuity_pressure", 0.0))

        color = node_color(recoverability, dependency)
        radius = 45 + (continuity_pressure * 20)

        svg_parts.append(
            f'<circle cx="{x}" cy="{y}" r="{radius}" fill="#151d33" stroke="{color}" stroke-width="4"/>\n'
        )

        svg_parts.append(
            f'<text x="{x}" y="{y - 8}" class="label" text-anchor="middle">{node.get("label", node_id)}</text>\n'
        )

        svg_parts.append(
            f'<text x="{x}" y="{y + 15}" class="metric" text-anchor="middle">R:{recoverability} D:{dependency}</text>\n'
        )

    svg_parts.append(f'''
  <circle cx="{center_x}" cy="{center_y}" r="86" fill="#111827" stroke="#7aa2ff" stroke-width="3"/>
  <text x="{center_x}" y="{center_y - 12}" class="label" text-anchor="middle">VISIBLE</text>
  <text x="{center_x}" y="{center_y + 12}" class="label" text-anchor="middle">CONTINUITY</text>
  <text x="{center_x}" y="{center_y + 36}" class="small" text-anchor="middle">may mask pressure</text>
''')

    svg_parts.append(build_drift_panel(case.get("time_steps", [])))
    svg_parts.append(build_human_oversight_panel(case.get("human_oversight", {})))

    svg_parts.append('''
  <rect x="930" y="780" width="420" height="155" rx="16" fill="#151d33" stroke="#2d3a5f"/>
  <text x="955" y="815" class="label">Core Reductions</text>
''')

    y = 845
    for reduction in reductions[:4]:
        svg_parts.append(f'<text x="955" y="{y}" class="small">- {reduction}</text>\n')
        y += 24

    svg_parts.append('''
  <text x="50" y="1015" class="small">Purple dashed edges = shadow dependencies / low-visibility hidden coupling</text>
''')

    svg_parts.append("</svg>")
    return "".join(svg_parts)


def write_receipt(case, svg_text):
    digest = hashlib.sha256(svg_text.encode("utf-8")).hexdigest()

    receipt = {
        "case_id": case.get("case_id"),
        "case_name": case.get("case_name"),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "output_file": str(OUTPUT_PATH),
        "sha256": digest,
        "claim_scope": "diagnostic_only",
        "authority": "observer_only",
        "non_claims": case.get("non_claims", [])
    }

    with open(RECEIPT_PATH, "w", encoding="utf-8") as file:
        json.dump(receipt, file, indent=2)


def main():
    case = load_case(INPUT_PATH)
    svg = build_svg(case)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        file.write(svg)

    write_receipt(case, svg)

    print("Continuity topology visualization generated.")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Receipt: {RECEIPT_PATH}")


if __name__ == "__main__":
    main()