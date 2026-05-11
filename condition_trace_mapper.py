import json

INPUT_FILE = "Inputs/condition_trace_case.json"
OUTPUT_FILE = "Outputs/condition_trace_report.json"

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

retry_enabled = data.get("retry_enabled", False)
shared_surface = data.get("shared_surface", False)
fresh_bind = data.get("fresh_bind_required", True)

status = "PASS"

if retry_enabled and shared_surface:
    status = "SHADOW"

if not fresh_bind:
    status = "FAIL"

report = {
    "condition_id": data.get("condition_id"),
    "status": status,
    "retry_enabled": retry_enabled,
    "shared_surface": shared_surface,
    "fresh_bind_required": fresh_bind,
    "observer_mode": True,
    "non_claims": [
        "Not execution control",
        "Not payment authorization",
        "Not runtime enforcement"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")