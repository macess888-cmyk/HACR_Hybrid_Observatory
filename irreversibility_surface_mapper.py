import json
import os

INPUT_FILE = "Inputs/irreversibility_surface_case.json"
OUTPUT_FILE = "Outputs/irreversibility_surface_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

surfaces = data.get("surfaces", [])

irreversible = []
status = "PASS"

for surface in surfaces:
    if surface.get("irreversible") is True:
        irreversible.append({
            "surface_id": surface.get("surface_id"),
            "surface_type": surface.get("surface_type"),
            "effect_propagated": surface.get("effect_propagated", False),
            "reversal_available": surface.get("reversal_available", False),
            "reason": "irreversible surface detected"
        })

if irreversible:
    status = "HOLD"

if any(s.get("effect_propagated") for s in irreversible):
    status = "SHADOW"

if any(
    s.get("effect_propagated") and not s.get("reversal_available")
    for s in irreversible
):
    status = "FAIL"

report = {
    "lens": "IRREVERSIBILITY_SURFACE",
    "status": status,
    "irreversible_surface_count": len(irreversible),
    "irreversible_surfaces": irreversible,
    "observer_mode": True,
    "non_claims": [
        "Not rollback control",
        "Not execution authorization",
        "Not certification",
        "Not runtime enforcement"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")