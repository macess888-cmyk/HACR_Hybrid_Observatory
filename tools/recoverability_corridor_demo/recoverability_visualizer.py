import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "input" / "small_business_case.json"
OUTPUT_PATH = ROOT / "output" / "recoverability_corridor.svg"


def clamp(value, minimum=0.0, maximum=1.0):
    return max(minimum, min(maximum, float(value)))


def load_case(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_recoverability(case):
    supplier = clamp(case.get("supplier_concentration", 0.0))
    redundancy = clamp(case.get("staff_redundancy", 0.0))
    fragility = clamp(case.get("dependency_fragility", 0.0))

    pressure = (supplier + fragility + (1.0 - redundancy)) / 3.0
    recoverability = 1.0 - pressure

    return round(clamp(recoverability), 2)


def classify_recoverability(score):
    if score > 0.70:
        return "RECOVERABILITY STABLE", "#35c759"
    if score > 0.40:
        return "RECOVERABILITY NARROWING", "#ffcc00"
    return "RECOVERABILITY CRITICAL", "#ff453a"


def build_svg(case, score, status, corridor_color):
    business_name = case.get("business_name", "Unnamed Operational Case")
    supplier = case.get("supplier_concentration", "unknown")
    redundancy = case.get("staff_redundancy", "unknown")
    fragility = case.get("dependency_fragility", "unknown")
    recovery_window = case.get("interruption_recovery_window_days", "unknown")
    visible_status = case.get("visible_operational_status", "unknown")

    bar_width = int(score * 1000)

    return f'''<svg width="1200" height="700" xmlns="http://www.w3.org/2000/svg">
  <style>
    .title {{
      font: bold 30px Arial, sans-serif;
      fill: #ffffff;
    }}
    .subtitle {{
      font: 18px Arial, sans-serif;
      fill: #cfd8ff;
    }}
    .label {{
      font: 18px Arial, sans-serif;
      fill: #ffffff;
    }}
    .small {{
      font: 15px Arial, sans-serif;
      fill: #c8c8c8;
    }}
    .metric {{
      font: bold 22px Arial, sans-serif;
      fill: #ffffff;
    }}
  </style>

  <rect width="100%" height="100%" fill="#0b1020"/>

  <text x="50" y="60" class="title">Recoverability Corridor Visualization</text>
  <text x="50" y="98" class="subtitle">Observer-only operational inspection | deterministic demo output</text>

  <rect x="50" y="130" width="1100" height="90" rx="22" fill="#151d33" stroke="#2d3a5f" stroke-width="2"/>
  <text x="80" y="165" class="label">Case</text>
  <text x="80" y="198" class="metric">{business_name}</text>

  <text x="50" y="280" class="label">Recoverability Corridor</text>
  <rect x="50" y="305" width="1000" height="70" rx="18" fill="#1e2a44"/>
  <rect x="50" y="305" width="{bar_width}" height="70" rx="18" fill="{corridor_color}"/>
  <text x="1070" y="350" class="metric">{score}</text>

  <text x="50" y="425" class="metric">{status}</text>

  <rect x="50" y="465" width="330" height="105" rx="16" fill="#151d33" stroke="#2d3a5f"/>
  <text x="75" y="505" class="label">Supplier Concentration</text>
  <text x="75" y="545" class="metric">{supplier}</text>

  <rect x="435" y="465" width="330" height="105" rx="16" fill="#151d33" stroke="#2d3a5f"/>
  <text x="460" y="505" class="label">Staff Redundancy</text>
  <text x="460" y="545" class="metric">{redundancy}</text>

  <rect x="820" y="465" width="330" height="105" rx="16" fill="#151d33" stroke="#2d3a5f"/>
  <text x="845" y="505" class="label">Dependency Fragility</text>
  <text x="845" y="545" class="metric">{fragility}</text>

  <text x="50" y="620" class="small">Visible operational status: {visible_status}</text>
  <text x="50" y="645" class="small">Interruption recovery window: {recovery_window} days</text>
  <text x="50" y="670" class="small">Core reduction: visible continuity != preserved recoverability</text>
</svg>
'''


def main():
    case = load_case(INPUT_PATH)
    score = calculate_recoverability(case)
    status, color = classify_recoverability(score)
    svg = build_svg(case, score, status, color)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        file.write(svg)

    print("Recoverability corridor visualization generated.")
    print(f"Recoverability Score: {score}")
    print(f"Classification: {status}")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()