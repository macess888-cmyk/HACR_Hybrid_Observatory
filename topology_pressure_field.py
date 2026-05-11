import json
import os

INPUT_FILE = "Inputs/topology_pressure_case.json"
OUTPUT_FILE = "Outputs/topology_pressure_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

surfaces = data.get("surfaces", [])

pressure_points = []
total_pressure = 0
status = "LOW"

for surface in surfaces:
    score = 0

    if surface.get("effect_capable"):
        score += 3

    if surface.get("replay_capable"):
        score += 2

    if surface.get("semantic_reconstructible"):
        score += 2

    if surface.get("survives_refusal"):
        score += 2

    if surface.get("irreversible"):
        score += 3

    if score > 0:
        pressure_points.append({
            "surface_id": surface.get("surface_id"),
            "surface_type": surface.get("surface_type"),
            "pressure_score": score
        })

    total_pressure += score

if total_pressure >= 5:
    status = "MODERATE"

if total_pressure >= 10:
    status = "HIGH"

if total_pressure >= 15:
    status = "CRITICAL"

report = {
    "lens": "TOPOLOGY_PRESSURE_FIELD",
    "status": status,
    "total_pressure": total_pressure,
    "pressure_point_count": len(pressure_points),
    "pressure_points": pressure_points,
    "observer_mode": True,
    "non_claims": [
        "Not risk certification",
        "Not execution control",
        "Not runtime enforcement",
        "Not operational authorization"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")