import json

INPUT_FILE = "Outputs/survivability_graph_export.json"
OUTPUT_FILE = "Outputs/survivability_graph.svg"

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

nodes = data.get("nodes", [])
edges = data.get("edges", [])

svg_width = 1600
svg_height = 900

positions = {
    "retry_queue_handle": (220, 120),
    "downstream_callback": (220, 320),
    "schema_interpretation": (220, 520),
    "cached_approval_token": (220, 720),
    "cached_payment_state": (220, 860),

    "cached_authority_snapshot": (1150, 220),
    "semantic_fragment": (1150, 460),
    "descendant_effect_surface": (1150, 650),
    "shared_retry_queue": (1150, 860)
}

color_map = {
    "CRITICAL": "#ff6b6b",
    "HIGH": "#f7b267",
    "ELEVATED": "#f4d35e",
    "LOW": "#8fd19e"
}

svg = []

svg.append(f'''
<svg width="{svg_width}" height="{svg_height}"
xmlns="http://www.w3.org/2000/svg"
style="background:#05070d;font-family:Arial,sans-serif">
''')

# Title
svg.append('''
<text x="40" y="50"
font-size="28"
fill="white"
font-weight="bold">
HACR Survivability Graph Export
</text>
''')

# Subtitle
svg.append('''
<text x="40" y="85"
font-size="18"
fill="#cccccc">
Observer-restricted topology visualization. Not runtime control.
</text>
''')

# Demo question
svg.append('''
<text x="40" y="125"
font-size="20"
fill="#ffffff"
font-weight="bold">
Demo Question:
</text>
''')

svg.append('''
<text x="260" y="125"
font-size="20"
fill="#ffcc66">
After refusal, can consequence still become real?
</text>
''')

# Legend
legend_y = 180

legend_items = [
    ("#ff6b6b", "Critical survivability path"),
    ("#f7b267", "Elevated continuation surface"),
    ("#8fd19e", "Low observed pressure")
]

for i, (color, label) in enumerate(legend_items):
    y = legend_y + (i * 35)

    svg.append(f'''
    <circle cx="60" cy="{y}" r="10"
    fill="{color}" />
    ''')

    svg.append(f'''
    <text x="85" y="{y + 5}"
    font-size="16"
    fill="#dddddd">
    {label}
    </text>
    ''')

# Draw edges
for edge in edges:
    source = edge["source"]
    target = edge["target"]

    if source not in positions or target not in positions:
        continue

    x1, y1 = positions[source]
    x2, y2 = positions[target]

    weight = edge.get("weight", 1)

    if weight >= 15:
        stroke = "#ff6b6b"
        width = 6
    elif weight >= 8:
        stroke = "#f7b267"
        width = 4
    else:
        stroke = "#8fd19e"
        width = 2

    svg.append(f'''
    <line
    x1="{x1}"
    y1="{y1}"
    x2="{x2}"
    y2="{y2}"
    stroke="{stroke}"
    stroke-width="{width}"
    opacity="0.85"
    />
    ''')

# Draw nodes
for node in nodes:
    node_id = node["id"]

    if node_id not in positions:
        continue

    x, y = positions[node_id]

    status = node.get("status", "LOW")
    weight = node.get("weight", 1)

    color = color_map.get(status, "#cccccc")

    radius = 42 if weight >= 15 else 34 if weight >= 8 else 28

    svg.append(f'''
    <circle
    cx="{x}"
    cy="{y}"
    r="{radius}"
    fill="{color}"
    stroke="white"
    stroke-width="4"
    />
    ''')

    svg.append(f'''
    <text
    x="{x + 55}"
    y="{y - 8}"
    font-size="16"
    fill="white"
    font-weight="bold">
    {node_id}
    </text>
    ''')

    svg.append(f'''
    <text
    x="{x + 55}"
    y="{y + 18}"
    font-size="15"
    fill="#cccccc">
    status={status} weight={weight}
    </text>
    ''')

# Footer
svg.append('''
<text x="40" y="880"
font-size="15"
fill="#999999">
Deterministic observer artifact • Non-authoritative • Reproducible topology exposure
</text>
''')

svg.append('</svg>')

with open(OUTPUT_FILE, "w") as f:
    f.write("\n".join(svg))

print(f"{OUTPUT_FILE} -> SVG_GENERATED")