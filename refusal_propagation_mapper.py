import json
import os

INPUT_FILE = "Inputs/refusal_propagation_case.json"
OUTPUT_FILE = "Outputs/refusal_propagation_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

surfaces = data.get("surfaces", [])

unpropagated = []
status = "PASS"

for surface in surfaces:
    if surface.get("refusal_received") is False:
        unpropagated.append({
            "surface_id": surface.get("surface_id"),
            "surface_type": surface.get("surface_type"),
            "effect_capable": surface.get("effect_capable", False),
            "reason": "refusal did not propagate to this surface"
        })

if unpropagated:
    status = "HOLD"

if any(s.get("effect_capable") for s in unpropagated):
    status = "FAIL"

report = {
    "lens": "REFUSAL_PROPAGATION",
    "status": status,
    "unpropagated_surface_count": len(unpropagated),
    "unpropagated_surfaces": unpropagated,
    "observer_mode": True,
    "non_claims": [
        "Not refusal enforcement",
        "Not execution control",
        "Not certification",
        "Not operational authorization"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")