import json
import os

INPUT_FILE = "Inputs/superposition_case.json"
OUTPUT_FILE = "Outputs/superposition_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

paths = data.get("paths", [])

reachable = []
hidden = []
status = "PASS"

for path in paths:
    if path.get("reachable"):
        reachable.append(path)

    if path.get("hidden"):
        hidden.append(path)

if reachable:
    status = "HOLD"

for path in reachable:
    if path.get("effect_capable"):
        status = "SHADOW"

report = {
    "lens": "SUPERPOSITION_REACHABILITY",
    "status": status,
    "reachable_path_count": len(reachable),
    "hidden_path_count": len(hidden),
    "paths": paths,
    "observer_mode": True,
    "non_claims": [
        "Not execution control",
        "Not orchestration authority",
        "Not runtime enforcement",
        "Not proof of isolation"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")