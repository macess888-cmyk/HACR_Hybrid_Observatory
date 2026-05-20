import json
from pathlib import Path

INPUT_FILE = Path("sample_input.json")
OUTPUT_FILE = Path("green_surface_dead_recovery_output.svg")

def main():
    data = json.loads(INPUT_FILE.read_text(encoding="utf-8"))

    case_id = data.get("case_id", "unknown")
    surface = data.get("surface_continuity", "UNKNOWN")
    classification = data.get("classification", "HOLD")
    recovery_time = data.get("effective_recovery_time_minutes", "UNKNOWN")
    hardening_window = data.get("consequence_hardening_window_minutes", "UNKNOWN")
    reduction = data.get("reduction", "UNKNOWN -> HOLD")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="620" viewBox="0 0 1200 620">
  <rect width="1200" height="620" fill="#ffffff"/>

  <text x="40" y="45" font-family="Arial" font-size="30" font-weight="bold">
    Green Surface / Dead Recovery
  </text>

  <text x="40" y="78" font-family="Arial" font-size="15">
    Observer-only deterministic visualization. Does not govern, authorize, certify, or determine legitimacy.
  </text>

  <rect x="60" y="130" width="470" height="320" rx="18" fill="#dff5df" stroke="#2c662d" stroke-width="2"/>
  <text x="90" y="175" font-family="Arial" font-size="24" font-weight="bold">
    Surface Continuity
  </text>
  <text x="100" y="240" font-family="Arial" font-size="22">Status: {surface}</text>
  <text x="100" y="285" font-family="Arial" font-size="18">Dashboard stable</text>
  <text x="100" y="325" font-family="Arial" font-size="18">Replay available</text>
  <text x="100" y="365" font-family="Arial" font-size="18">Validator passing</text>
  <text x="100" y="405" font-family="Arial" font-size="18">Procedure coherent</text>

  <rect x="650" y="130" width="470" height="320" rx="18" fill="#f7dddd" stroke="#7a1f1f" stroke-width="2"/>
  <text x="690" y="175" font-family="Arial" font-size="24" font-weight="bold">
    Recovery Viability
  </text>
  <text x="690" y="240" font-family="Arial" font-size="22">Classification: {classification}</text>
  <text x="690" y="295" font-family="Arial" font-size="18">Effective recovery time: {recovery_time} min</text>
  <text x="690" y="340" font-family="Arial" font-size="18">Hardening window: {hardening_window} min</text>
  <text x="690" y="385" font-family="Arial" font-size="18">Recovery viability exhausted before consequence boundary.</text>

  <line x1="530" y1="290" x2="650" y2="290" stroke="#333" stroke-width="3"/>
  <polygon points="650,290 635,280 635,300" fill="#333"/>

  <text x="60" y="520" font-family="Arial" font-size="22" font-weight="bold">
    {reduction}
  </text>

  <text x="60" y="565" font-family="Arial" font-size="16">
    Case: {case_id} | Observer-only • Not authority • UNKNOWN -&gt; HOLD
  </text>
</svg>'''

    OUTPUT_FILE.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")

if __name__ == "__main__":
    main()