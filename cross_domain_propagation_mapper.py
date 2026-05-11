import json
import os

INPUT_FILE = "Inputs/cross_domain_propagation_case.json"
OUTPUT_FILE = "Outputs/cross_domain_propagation_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

transitions = data.get("domain_transitions", [])

propagating = []
status = "PASS"

for transition in transitions:
    if transition.get("propagates") is True:
        propagating.append({
            "transition_id": transition.get("transition_id"),
            "from_domain": transition.get("from_domain"),
            "to_domain": transition.get("to_domain"),
            "effect_capable": transition.get("effect_capable", False),
            "reconstructible": transition.get("reconstructible", False),
            "reason": "cross-domain propagation detected"
        })

if propagating:
    status = "HOLD"

if any(p.get("reconstructible") for p in propagating):
    status = "SHADOW"

if any(p.get("effect_capable") and p.get("reconstructible") for p in propagating):
    status = "FAIL"

report = {
    "lens": "CROSS_DOMAIN_PROPAGATION",
    "status": status,
    "propagating_transition_count": len(propagating),
    "propagating_transitions": propagating,
    "observer_mode": True,
    "non_claims": [
        "Not cross-domain authority",
        "Not runtime enforcement",
        "Not certification",
        "Not operational authorization"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")