import json
from pathlib import Path

INPUT_FILE = Path("sample_input.json")
OUTPUT_FILE = Path("layer_survival_heatmap_output.svg")

STATUS_FILL = {
    "survives": "#dff5df",
    "partial": "#fff1c7",
    "degraded": "#f7dddd",
    "collapsed": "#d8d8d8",
    "unknown": "#eeeeee"
}

STATUS_STROKE = {
    "survives": "#2c662d",
    "partial": "#8a6d00",
    "degraded": "#7a1f1f",
    "collapsed": "#555555",
    "unknown": "#777777"
}

def main():
    data = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    layers = data.get("layers", {})

    order = [
        "observable",
        "inspectable",
        "traversable",
        "interruptible",
        "destabilizable",
        "recoverable"
    ]

    cells = []
    x = 70
    y = 170
    width = 165
    height = 90

    for index, layer in enumerate(order):
        status = layers.get(layer, "unknown")
        fill = STATUS_FILL.get(status, STATUS_FILL["unknown"])
        stroke = STATUS_STROKE.get(status, STATUS_STROKE["unknown"])
        cell_x = x + index * 180

        cells.append(f'''
  <rect x="{cell_x}" y="{y}" width="{width}" height="{height}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>
  <text x="{cell_x + 18}" y="{y + 38}" font-family="Arial" font-size="17" font-weight="bold">{layer}</text>
  <text x="{cell_x + 18}" y="{y + 68}" font-family="Arial" font-size="16">{status}</text>
''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="460" viewBox="0 0 1200 460">
  <rect width="1200" height="460" fill="#ffffff"/>

  <text x="40" y="45" font-family="Arial" font-size="30" font-weight="bold">
    Layer Survival Heatmap
  </text>

  <text x="40" y="78" font-family="Arial" font-size="15">
    Observer-only deterministic visualization. Survival of one layer does not prove survival of the next.
  </text>

  {''.join(cells)}

  <text x="60" y="330" font-family="Arial" font-size="22" font-weight="bold">
    Layer survival is not layer inheritance.
  </text>

  <text x="60" y="375" font-family="Arial" font-size="18">
    observable ≠ inspectable ≠ traversable ≠ interruptible ≠ destabilizable ≠ recoverable
  </text>

  <text x="60" y="420" font-family="Arial" font-size="16">
    Observer-only • Not authority • UNKNOWN -&gt; HOLD
  </text>
</svg>'''

    OUTPUT_FILE.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")

if __name__ == "__main__":
    main()