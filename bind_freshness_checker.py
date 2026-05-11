import json
import os

INPUT_FILE = "Inputs/bind_freshness_case.json"
OUTPUT_FILE = "Outputs/bind_freshness_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

condition_age_ms = data.get("condition_age_ms", 0)
freshness_limit_ms = data.get("freshness_limit_ms", 1000)
reused_prior_authority = data.get("reused_prior_authority", False)
retry_context = data.get("retry_context", False)

status = "FRESH"

if condition_age_ms > freshness_limit_ms:
    status = "STALE"

if reused_prior_authority:
    status = "REPLAY_RISK"

if retry_context and reused_prior_authority:
    status = "FAIL"

report = {
    "checker": "BIND_FRESHNESS",
    "status": status,
    "condition_age_ms": condition_age_ms,
    "freshness_limit_ms": freshness_limit_ms,
    "reused_prior_authority": reused_prior_authority,
    "retry_context": retry_context,
    "observer_mode": True,
    "non_claims": [
        "Not execution authorization",
        "Not proof of admissibility",
        "Not runtime enforcement"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")