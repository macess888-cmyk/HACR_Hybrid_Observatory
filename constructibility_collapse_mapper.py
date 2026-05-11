import json
import os

INPUT_FILE = "Inputs/constructibility_collapse_case.json"
OUTPUT_FILE = "Outputs/constructibility_collapse_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

surfaces = data.get("surfaces_after_refusal", [])

surviving = []
status = "PASS"

for surface in surfaces:
    if surface.get("survives_refusal") is True:
        surviving.append({
            "surface_id": surface.get("surface_id"),
            "surface_type": surface.get("surface_type"),
            "effect_capable": surface.get("effect_capable", False),
            "reconstructible": surface.get("reconstructible", False),
            "reason": "surface survives refusal"
        })

if surviving:
    status = "HOLD"

if any(s.get("reconstructible") for s in surviving):
    status = "SHADOW"

if any(s.get("effect_capable") for s in surviving):
    status = "FAIL"

report = {
    "lens": "CONSTRUCTIBILITY_COLLAPSE",
    "status": status,
    "surviving_surface_count": len(surviving),
    "surviving_surfaces": surviving,
    "collapse_result": "COLLAPSED" if status == "PASS" else "NOT_COLLAPSED",
    "observer_mode": True,
    "non_claims": [
        "Not execution control",
        "Not proof of safety",
        "Not certification",
        "Not operational authorization"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")