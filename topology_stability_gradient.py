import json
import os

INPUT_FILE = "Inputs/topology_stability_gradient_case.json"
OUTPUT_FILE = "Outputs/topology_stability_gradient_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

segments = data.get("segments", [])

gradient_points = []
max_gradient = 0
status = "STABLE"

for segment in segments:
    start_pressure = segment.get("start_pressure", 0)
    end_pressure = segment.get("end_pressure", 0)
    gradient = end_pressure - start_pressure

    point = {
        "segment_id": segment.get("segment_id"),
        "from": segment.get("from"),
        "to": segment.get("to"),
        "start_pressure": start_pressure,
        "end_pressure": end_pressure,
        "gradient": gradient,
        "effect_capable": segment.get("effect_capable", False)
    }

    gradient_points.append(point)

    if gradient > max_gradient:
        max_gradient = gradient

if max_gradient >= 3:
    status = "DRIFTING"

if max_gradient >= 5:
    status = "UNSTABLE"

if any(
    p.get("gradient", 0) >= 5 and p.get("effect_capable")
    for p in gradient_points
):
    status = "SHADOW"

report = {
    "lens": "TOPOLOGY_STABILITY_GRADIENT",
    "status": status,
    "max_gradient": max_gradient,
    "gradient_points": gradient_points,
    "observer_mode": True,
    "non_claims": [
        "Not stability certification",
        "Not execution control",
        "Not runtime enforcement",
        "Not operational authorization"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")