import json
import os

INPUT_FILE = "Inputs/dynamic_drift_case.json"
OUTPUT_FILE = "Outputs/dynamic_drift_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

previous = data.get("previous_state", {})
current = data.get("current_state", {})

changes = []
status = "STABLE"

for key in sorted(set(previous.keys()) | set(current.keys())):
    old = previous.get(key)
    new = current.get(key)

    if old != new:
        changes.append({
            "field": key,
            "previous": old,
            "current": new
        })

if changes:
    status = "DRIFTING"

critical_fields = [
    "authority_source",
    "fresh_bind_required",
    "retry_enabled",
    "effect_capable_path",
    "shared_surface"
]

for change in changes:
    if change["field"] in critical_fields:
        status = "UNSTABLE"

report = {
    "lens": "DYNAMIC_DRIFT",
    "status": status,
    "change_count": len(changes),
    "changes": changes,
    "observer_mode": True,
    "non_claims": [
        "Not runtime enforcement",
        "Not execution authorization",
        "Not certification",
        "Not proof of global safety"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")