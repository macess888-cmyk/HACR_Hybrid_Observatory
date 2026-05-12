import json
import os

OUTPUT_DIR = "Outputs"
REPORT_FILE = "Outputs/output_schema_validation_report.json"

REQUIRED_FIELDS = [
    "lens",
    "status",
    "observer_mode",
    "summary",
    "non_claims"
]

results = []
failures = 0

for filename in os.listdir(OUTPUT_DIR):
    if not filename.endswith(".json"):
        continue

    path = os.path.join(OUTPUT_DIR, filename)

    try:
        with open(path, "r") as f:
            data = json.load(f)

        missing = [field for field in REQUIRED_FIELDS if field not in data]

        if missing:
            failures += 1
            status = "SCHEMA_GAP"
        else:
            status = "SCHEMA_OK"

        results.append({
            "file": filename,
            "status": status,
            "missing_fields": missing
        })

    except Exception as e:
        failures += 1
        results.append({
            "file": filename,
            "status": "READ_ERROR",
            "error": str(e)
        })

overall_status = "PASS" if failures == 0 else "HOLD"

report = {
    "lens": "OUTPUT_SCHEMA_VALIDATOR",
    "status": overall_status,
    "score": failures,
    "observer_mode": True,
    "summary": "Validates generated JSON reports against the canonical v0.8 observer output schema.",
    "findings": results,
    "derived_from": [
        "OUTPUT_SCHEMA_v0_8.md",
        "Outputs/*.json"
    ],
    "non_claims": [
        "Not runtime enforcement",
        "Not certification",
        "Not production monitoring",
        "Not execution control"
    ]
}

with open(REPORT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{REPORT_FILE} -> {overall_status}")