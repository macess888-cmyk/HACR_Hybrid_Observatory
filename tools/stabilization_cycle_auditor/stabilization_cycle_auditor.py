import json

with open("sample_audit_input.json", "r") as f:
    data = json.load(f)

scores = {
    "LOW": 1,
    "MEDIUM": 5,
    "HIGH": 10
}

traversal_cost = scores[data["traversal_cost"]]
falsifiability_gain = scores[data["falsifiability_gain"]]
reassurance_risk = scores[data["reassurance_risk"]]

health_score = (
    falsifiability_gain
    - traversal_cost
    - reassurance_risk
)

decision = "HOLD"

if health_score >= 4:
    decision = "PROCEED"

elif health_score >= 0:
    decision = "SIMPLIFY"

elif health_score <= -5:
    decision = "REVERSE"

output = {
    "stabilization_health_score": health_score,
    "decision": decision,
    "runtime_reduction":
        "Healthy maturity reduces traversal cost while increasing falsifiability and reducing reassurance inheritance risk."
}

print(json.dumps(output, indent=2))