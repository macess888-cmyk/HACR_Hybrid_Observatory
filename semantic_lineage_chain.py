import json
import os

INPUT_FILE = "Inputs/semantic_lineage_case.json"
OUTPUT_FILE = "Outputs/semantic_lineage_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

chains = data.get("semantic_lineages", [])

surviving = []
status = "PASS"

for chain in chains:
    if chain.get("survives_refusal") is True:
        surviving.append({
            "lineage_id": chain.get("lineage_id"),
            "origin": chain.get("origin"),
            "descendant": chain.get("descendant"),
            "semantic_payload": chain.get("semantic_payload"),
            "reconstructible": chain.get("reconstructible", False),
            "cross_topology": chain.get("cross_topology", False),
            "reason": "semantic lineage survives refusal"
        })

if surviving:
    status = "HOLD"

if any(s.get("reconstructible") for s in surviving):
    status = "SHADOW"

if any(
    s.get("reconstructible") and s.get("cross_topology")
    for s in surviving
):
    status = "FAIL"

report = {
    "lens": "SEMANTIC_LINEAGE_CHAIN",
    "status": status,
    "surviving_semantic_lineages": len(surviving),
    "semantic_lineages": surviving,
    "observer_mode": True,
    "non_claims": [
        "Not semantic authority",
        "Not execution control",
        "Not certification",
        "Not runtime governance"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")