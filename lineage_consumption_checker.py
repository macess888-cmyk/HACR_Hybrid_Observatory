import json
import os

INPUT_FILE = "Inputs/lineage_consumption_case.json"
OUTPUT_FILE = "Outputs/lineage_consumption_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

lineages = data.get("lineages", [])

unconsumed = []
status = "PASS"

for lineage in lineages:
    if lineage.get("consumed_at_bind") is False:
        unconsumed.append({
            "lineage_id": lineage.get("lineage_id"),
            "surface_type": lineage.get("surface_type"),
            "descendant_effect_capable": lineage.get("descendant_effect_capable", False),
            "replay_possible": lineage.get("replay_possible", False),
            "reason": "lineage not consumed at bind"
        })

if unconsumed:
    status = "HOLD"

if any(l.get("replay_possible") for l in unconsumed):
    status = "SHADOW"

if any(l.get("descendant_effect_capable") for l in unconsumed):
    status = "FAIL"

report = {
    "lens": "LINEAGE_CONSUMPTION",
    "status": status,
    "unconsumed_lineage_count": len(unconsumed),
    "unconsumed_lineages": unconsumed,
    "observer_mode": True,
    "non_claims": [
        "Not lineage authority",
        "Not execution control",
        "Not certification",
        "Not operational authorization"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")