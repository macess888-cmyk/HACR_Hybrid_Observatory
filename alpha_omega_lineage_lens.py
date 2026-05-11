import json
import os

INPUT_FILE = "Inputs/alpha_omega_case.json"
OUTPUT_FILE = "Outputs/alpha_omega_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

origin = data.get("origin_state", {})
terminal = data.get("terminal_state", {})

status = "PASS"
observations = []

if origin.get("authority") != terminal.get("authority"):
    status = "HOLD"
    observations.append(
        "authority lineage divergence detected"
    )

if terminal.get("effect_capable") is True and \
   origin.get("fresh_bind") is False:
    status = "SHADOW"
    observations.append(
        "effect-capable terminal state without fresh bind origin"
    )

if terminal.get("retry_path") is True:
    status = "SHADOW"
    observations.append(
        "retry-capable lineage continuity detected"
    )

report = {
    "lens": "ALPHA_OMEGA_LINEAGE",
    "status": status,
    "origin": origin,
    "terminal": terminal,
    "observations": observations,
    "observer_mode": True,
    "non_claims": [
        "Not execution governance",
        "Not lineage proof",
        "Not operational authorization",
        "Not runtime enforcement"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")