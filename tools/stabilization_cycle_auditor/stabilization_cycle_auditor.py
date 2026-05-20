import json

with open("sample_audit_input.json", "r") as f:
    data = json.load(f)

traversal = data["traversal_cost"]
falsifiability = data["falsifiability_gain"]
reassurance = data["reassurance_risk"]

decision = "HOLD"

if traversal == "LOW" and falsifiability == "HIGH" and reassurance == "LOW":
    decision = "PROCEED"

elif traversal == "HIGH" and falsifiability == "LOW":
    decision = "REVERSE"

elif reassurance == "HIGH":
    decision = "HOLD"

else:
    decision = "SIMPLIFY"

output = {
    "decision": decision,
    "runtime_reduction":
        "Healthy stabilization reduces traversal cost while increasing falsifiability and reducing reassurance inheritance risk."
}

print(json.dumps(output, indent=2))