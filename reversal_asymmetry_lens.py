import json
import os

INPUT_FILE = "Inputs/reversal_asymmetry_case.json"
OUTPUT_FILE = "Outputs/reversal_asymmetry_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

forward_path = data.get("forward_path", {})
reversal_path = data.get("reversal_path", {})

shared_queue = data.get("shared_queue", False)
shared_cache = data.get("shared_cache", False)
shared_retry_surface = data.get("shared_retry_surface", False)
reversal_requires_fresh_bind = data.get("reversal_requires_fresh_bind", True)

status = "PASS"
reasons = []

if shared_queue:
    status = "SHADOW"
    reasons.append("Forward and reversal paths share a queue.")

if shared_cache:
    status = "SHADOW"
    reasons.append("Forward and reversal paths share cached state.")

if shared_retry_surface:
    status = "SHADOW"
    reasons.append("Forward and reversal paths share a retry surface.")

if not reversal_requires_fresh_bind:
    status = "FAIL"
    reasons.append("Reversal path does not require fresh bind.")

report = {
    "lens": "REVERSAL_ASYMMETRY",
    "status": status,
    "forward_path": forward_path,
    "reversal_path": reversal_path,
    "shared_queue": shared_queue,
    "shared_cache": shared_cache,
    "shared_retry_surface": shared_retry_surface,
    "reversal_requires_fresh_bind": reversal_requires_fresh_bind,
    "reasons": reasons,
    "observer_mode": True,
    "non_claims": [
        "Not payment authorization",
        "Not execution control",
        "Not certification",
        "Not runtime enforcement"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")