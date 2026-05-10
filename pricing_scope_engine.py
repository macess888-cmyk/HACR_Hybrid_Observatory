import json
import os

INPUT_FILE = "Inputs/pricing_scope_case.json"
OUTPUT_FILE = "Outputs/pricing_scope_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

surfaces = data.get("surfaces", 0)
continuation = data.get("continuation_risk", False)
topology = data.get("topology_complexity", "LOW")
replay = data.get("replay_surfaces", False)

score = surfaces

if continuation:
    score += 2

if replay:
    score += 2

if topology == "MEDIUM":
    score += 2

if topology == "HIGH":
    score += 4

if score <= 3:
    tier = "TIER_1_BOUNDARY_REVIEW"
    price = "$250-$500"

elif score <= 6:
    tier = "TIER_2_CONTINUITY_DIAGNOSTIC"
    price = "$750-$1500"

elif score <= 10:
    tier = "TIER_3_OBSERVATORY_REPORT"
    price = "$2500-$5000"

else:
    tier = "CUSTOM_RESEARCH_SCOPE"
    price = "$5000+"

result = {
    "classification": "OBSERVER_RESTRICTED_SCOPE",
    "risk_score": score,
    "suggested_tier": tier,
    "estimated_range": price,
    "non_claims": [
        "Not governance authority",
        "Not certification",
        "Not legal approval",
        "Not operational authorization"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(result, f, indent=2)

print(f"{INPUT_FILE} -> {tier}")