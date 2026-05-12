import json
import os

OUTPUT_DIR = "Outputs"
NORMALIZED_DIR = "Outputs_Normalized"

os.makedirs(NORMALIZED_DIR, exist_ok=True)

DEFAULT_NON_CLAIMS = [
    "Not runtime enforcement",
    "Not certification",
    "Not production monitoring",
    "Not execution control",
    "Not operational authorization"
]

def infer_lens_name(filename):
    return filename.replace(".json", "").upper()

def infer_status(data):
    if isinstance(data, dict):
        for key in ["status", "pressure_state", "watchdog_status", "state", "result"]:
            if key in data:
                return data[key]
    return "NORMALIZED"

def infer_summary(filename):
    base = filename.replace("_", " ").replace(".json", "")
    return f"Normalized observer report for {base}."

normalized_count = 0
wrapped_count = 0

for filename in os.listdir(OUTPUT_DIR):
    if not filename.endswith(".json"):
        continue

    source_path = os.path.join(OUTPUT_DIR, filename)
    target_path = os.path.join(NORMALIZED_DIR, filename)

    try:
        with open(source_path, "r") as f:
            data = json.load(f)

        if isinstance(data, dict):
            normalized = dict(data)
        else:
            normalized = {
                "original_payload": data
            }
            wrapped_count += 1

        if "lens" not in normalized:
            normalized["lens"] = infer_lens_name(filename)

        if "status" not in normalized:
            normalized["status"] = infer_status(data)

        if "score" not in normalized:
            if isinstance(data, dict):
                normalized["score"] = data.get("pressure_score", 0)
            else:
                normalized["score"] = 0

        if "observer_mode" not in normalized:
            normalized["observer_mode"] = True

        if "summary" not in normalized:
            normalized["summary"] = infer_summary(filename)

        if "findings" not in normalized:
            normalized["findings"] = []

        if "derived_from" not in normalized:
            normalized["derived_from"] = [filename]

        if "non_claims" not in normalized:
            normalized["non_claims"] = DEFAULT_NON_CLAIMS

        with open(target_path, "w") as f:
            json.dump(normalized, f, indent=2)

        normalized_count += 1

    except Exception as e:
        error_report = {
            "lens": infer_lens_name(filename),
            "status": "NORMALIZATION_ERROR",
            "score": 1,
            "observer_mode": True,
            "summary": f"Normalization failed for {filename}.",
            "findings": [
                {
                    "file": filename,
                    "error": str(e)
                }
            ],
            "derived_from": [filename],
            "non_claims": DEFAULT_NON_CLAIMS
        }

        with open(target_path, "w") as f:
            json.dump(error_report, f, indent=2)

        normalized_count += 1

print(f"Outputs_Normalized -> {normalized_count} reports normalized")
print(f"Wrapped non-object payloads -> {wrapped_count}")