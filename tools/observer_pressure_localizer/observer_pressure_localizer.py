import json
import hashlib
from pathlib import Path

INPUT_FILE = Path("examples/sample_observer_pressure_input.json")
OUTPUT_FILE = Path("receipts/sample_observer_pressure_receipt.json")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

pressure = data["distinction_pressure"]
familiarity = data["observer_familiarity_density"]
new_evidence = data["new_operational_evidence_detected"]

classification = "EXPOSURE_STABLE"

if pressure > 0.75 and familiarity > 0.75:
    classification = "DISTINCTION_PRESSURE_RISING"

if classification == "DISTINCTION_PRESSURE_RISING" and not new_evidence:
    classification = "SEMANTIC_AUTHORIZATION_RISK"

receipt = {
    "classification": classification,
    "compression_integrity": data["compression_integrity"],
    "localization_integrity": data["localization_integrity"],
    "constraint_integrity": data["constraint_integrity"],
    "core_reduction": "persistent exposure != justified differentiation",
    "ontology_authorization": False,
    "recommended_state": "HOLD"
}

serialized = json.dumps(receipt, indent=2)
sha = hashlib.sha256(serialized.encode()).hexdigest()

receipt["sha256"] = sha

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(receipt, f, indent=2)

print("Wrote receipt:", OUTPUT_FILE)
print("SHA256:", sha)