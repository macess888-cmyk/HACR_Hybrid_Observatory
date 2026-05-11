import json
import os

INPUT_FILE = "Inputs/descendant_effect_case.json"
OUTPUT_FILE = "Outputs/descendant_effect_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

descendants = data.get("descendant_surfaces", [])

effect_survivors = []
status = "PASS"

for descendant in descendants:
    if descendant.get("can_produce_effect") is True:
        effect_survivors.append({
            "surface_id": descendant.get("surface_id"),
            "surface_type": descendant.get("surface_type"),
            "inherits_from": descendant.get("inherits_from"),
            "requires_fresh_bind": descendant.get("requires_fresh_bind", True),
            "reason": "descendant surface can still produce effect"
        })

if effect_survivors:
    status = "HOLD"

if any(d.get("requires_fresh_bind") is False for d in effect_survivors):
    status = "FAIL"

report = {
    "lens": "DESCENDANT_EFFECT",
    "status": status,
    "descendant_effect_count": len(effect_survivors),
    "descendant_effect_surfaces": effect_survivors,
    "observer_mode": True,
    "non_claims": [
        "Not downstream control",
        "Not execution authorization",
        "Not certification",
        "Not runtime enforcement"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")