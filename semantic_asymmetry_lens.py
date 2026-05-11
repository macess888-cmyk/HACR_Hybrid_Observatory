import json
import os

INPUT_FILE = "Inputs/semantic_asymmetry_case.json"
OUTPUT_FILE = "Outputs/semantic_asymmetry_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

baseline = data.get("baseline_terms", {})
current = data.get("current_terms", {})

drift = []
status = "PASS"

for key in baseline:
    old = baseline.get(key)
    new = current.get(key)

    if old != new:
        drift.append({
            "term": key,
            "baseline": old,
            "current": new
        })

if drift:
    status = "HOLD"

critical_terms = [
    "authority",
    "bind",
    "admissibility",
    "execution",
    "proof"
]

for item in drift:
    if item["term"] in critical_terms:
        status = "SHADOW"

report = {
    "lens": "SEMANTIC_ASYMMETRY",
    "status": status,
    "semantic_drift_count": len(drift),
    "drift": drift,
    "observer_mode": True,
    "non_claims": [
        "Not semantic truth",
        "Not legal interpretation",
        "Not runtime governance",
        "Not proof of meaning"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")