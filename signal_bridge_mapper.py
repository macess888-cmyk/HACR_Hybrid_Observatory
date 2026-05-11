import json

INPUT_FILE = "Inputs/signal_bridge_case.json"
OUTPUT_FILE = "Outputs/signal_bridge_report.json"

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

signal = data.get("signal", "")
layer = data.get("layer", "")
drift_risk = data.get("drift_risk", "LOW")

status = "PASS"

if drift_risk == "HIGH":
    status = "HOLD"

if "authority" in signal.lower():
    status = "SHADOW"

report = {
    "signal": signal,
    "layer": layer,
    "drift_risk": drift_risk,
    "status": status,
    "observer_mode": True,
    "non_claims": [
        "Not authority",
        "Not certification",
        "Not governance enforcement",
        "Not operational authorization"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")