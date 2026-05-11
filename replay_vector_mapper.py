import json
import os

INPUT_FILE = "Inputs/replay_vector_case.json"
OUTPUT_FILE = "Outputs/replay_vector_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

vectors = data.get("replay_vectors", [])

detected = []
status = "PASS"

for vector in vectors:
    if vector.get("replay_possible") is True:
        entry = {
            "vector_id": vector.get("vector_id"),
            "surface_type": vector.get("surface_type"),
            "effect_capable": vector.get("effect_capable", False),
            "requires_fresh_bind": vector.get("requires_fresh_bind", True),
            "reason": "replay-capable surface detected"
        }

        detected.append(entry)

if detected:
    status = "HOLD"

if any(not v.get("requires_fresh_bind", True) for v in detected):
    status = "SHADOW"

if any(v.get("effect_capable") for v in detected):
    status = "FAIL"

report = {
    "lens": "REPLAY_VECTOR_MAPPER",
    "status": status,
    "replay_vector_count": len(detected),
    "replay_vectors": detected,
    "observer_mode": True,
    "non_claims": [
        "Not runtime protection",
        "Not replay prevention",
        "Not authorization enforcement",
        "Not certification"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")