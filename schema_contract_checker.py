import json
import os

SCHEMA_FILE = "canonical_output_schema.json"
OUTPUT_DIR = "Outputs"

with open(SCHEMA_FILE, "r") as f:
    schema = json.load(f)

required_fields = schema["required_fields"]
valid_status = schema["status_values"]

results = []

for file in os.listdir(OUTPUT_DIR):
    if not file.endswith(".json"):
        continue

    path = os.path.join(OUTPUT_DIR, file)

    try:
        with open(path, "r") as f:
            data = json.load(f)

        missing = [
            field for field in required_fields
            if field not in data
        ]

        invalid_status = (
            "status" in data
            and data["status"] not in valid_status
        )

        results.append({
            "file": file,
            "missing_fields": missing,
            "invalid_status": invalid_status,
            "valid": len(missing) == 0 and not invalid_status
        })

    except Exception as e:
        results.append({
            "file": file,
            "error": str(e),
            "valid": False
        })

report = {
    "lens": "SCHEMA_CONTRACT_CHECKER",
    "status": "TRACEABLE",
    "observer_mode": True,
    "summary": "Checks repository outputs against canonical schema contract.",
    "findings": results,
    "non_claims": [
        "Not runtime enforcement",
        "Not certification",
        "Not execution control"
    ]
}

with open("schema_contract_report.json", "w") as f:
    json.dump(report, f, indent=2)

print("schema_contract_report.json -> TRACEABLE")