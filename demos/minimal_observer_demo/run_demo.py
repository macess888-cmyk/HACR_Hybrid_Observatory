import json
import hashlib
from pathlib import Path

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("\n=== HACR MINIMAL OBSERVER DEMO ===\n")

for input_file in INPUT_DIR.glob("*.json"):

    with open(input_file, "r") as f:
        data = json.load(f)

    continuity = data.get("continuity_status")
    coupling = data.get("coupling_status")
    interruptibility = data.get("interruptibility")

    inspection_result = "PASS"

    if coupling != "stable":
        inspection_result = "HOLD"

    if interruptibility == "degraded":
        inspection_result = "HOLD"

    result = {
        "event_id": data["event_id"],
        "inspection_result": inspection_result,
        "reason": "observer-local continuity inspection",
        "continuity_status": continuity,
        "coupling_status": coupling,
        "interruptibility": interruptibility,
        "runtime_grounding": (
            "grounded"
            if inspection_result == "PASS"
            else "uncertain"
        ),
        "observer_scope": "bounded_observer_local"
    }

    serialized = json.dumps(result, sort_keys=True).encode()

    receipt = hashlib.sha256(serialized).hexdigest()

    result["receipt_sha256"] = receipt

    output_file = OUTPUT_DIR / f"{data['event_id']}_result.json"

    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))
    print("\n---\n")

print("Deterministic replay inspection complete.")