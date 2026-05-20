import json
from pathlib import Path

OUTPUTS_DIR = Path("outputs")
VISUALS_DIR = Path("visuals")
VISUALS_DIR.mkdir(exist_ok=True)

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

LAYER_ORDER = [
    "observable",
    "inspectable",
    "traversable",
    "interruptible",
    "destabilizable",
    "recoverable"
]

def render_svg(result):
    cells = []
    x = 60
    y = 210
    width = 165
    height = 90

    layers = result.get("layers", {})

    for index, layer in enumerate(LAYER_ORDER):
        status = layers.get(layer, "unknown")
        fill = STATUS_FILL.get(status, STATUS_FILL["unknown"])
        stroke = STATUS_STROKE.get(status, STATUS_STROKE["unknown"])
        cell_x = x + index * 185

        cells.append(f'''
  <rect x="{cell_x}" y="{y}" width="{width}" height="{height}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>
  <text x="{cell_x + 16}" y="{y + 36}" font-family="Arial" font-size="16" font-weight="bold">{layer}</text>
  <text x="{cell_x + 16}" y="{y + 66}" font-family="Arial" font-size="15">{status}</text>
''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1220" height="620" viewBox="0 0 1220 620">
  <rect width="1220" height="620" fill="#ffffff"/>

  <text x="40" y="45" font-family="Arial" font-size="28" font-weight="bold">
    {result.get("title", "Recovery Case")}
  </text>

  <text x="40" y="78" font-family="Arial" font-size="15">
    Observer-only deterministic visualization. Not authority. UNKNOWN -&gt; HOLD.
  </text>

  <text x="40" y="125" font-family="Arial" font-size="20">
    Classification: {result.get("classification", "HOLD")}
  </text>

  <text x="40" y="160" font-family="Arial" font-size="17">
    Effective recovery time: {result.get("effective_recovery_time_minutes", "UNKNOWN")} min | Hardening window: {result.get("consequence_hardening_window_minutes", "UNKNOWN")} min
  </text>

  {''.join(cells)}

  <text x="60" y="390" font-family="Arial" font-size="22" font-weight="bold">
    {result.get("reduction", "UNKNOWN -> HOLD")}
  </text>

  <text x="60" y="440" font-family="Arial" font-size="18">
    observable ≠ inspectable ≠ traversable ≠ interruptible ≠ destabilizable ≠ recoverable
  </text>

  <text x="60" y="490" font-family="Arial" font-size="15">
    Case: {result.get("case_id", "unknown")}
  </text>

  <text x="60" y="525" font-family="Arial" font-size="13">
    SHA256 receipt: {result.get("sha256_receipt", "missing")}
  </text>
</svg>'''

def main():
    output_files = sorted(OUTPUTS_DIR.glob("*_output.json"))

    for output_file in output_files:
        result = json.loads(output_file.read_text(encoding="utf-8"))
        svg = render_svg(result)

        visual_file = VISUALS_DIR / f"{result['case_id']}.svg"
        visual_file.write_text(svg, encoding="utf-8")

        print(f"Wrote {visual_file}")

if __name__ == "__main__":
    main()