import json

TRIGGERS = [
    "weapon", "weapons", "arsenal", "hunter", "striker",
    "active defense", "sentinel", "intercept", "disable",
    "force projection", "dominance", "deterrence",
    "sanitization", "target", "kill chain"
]

def run(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    text = json.dumps(data, ensure_ascii=False).lower()
    hits = [t for t in TRIGGERS if t in text]

    if hits:
        result = {
            "lens": "weaponization_boundary_lens",
            "status": "HOLD",
            "weaponization_risk": "HIGH",
            "trigger_surface": hits,
            "decision": "NO_PROPAGATION",
            "note": "Pattern held internally. No authority, endorsement, or integration."
        }
    else:
        result = {
            "lens": "weaponization_boundary_lens",
            "status": "PASS",
            "weaponization_risk": "LOW",
            "trigger_surface": [],
            "decision": "OBSERVE_ONLY",
            "note": "No weaponization trigger detected."
        }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    run("Inputs/weaponization_probe.json", "Outputs/weaponization_boundary_result.json")