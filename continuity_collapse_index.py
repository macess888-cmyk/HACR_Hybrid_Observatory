import json
from pathlib import Path

OUTPUT = Path("Outputs/continuity_collapse_index_report.json")

INPUTS = {
    "latent_path": Path("Outputs/latent_path_report.json"),
    "authority_surface": Path("Outputs/authority_surface_report.json"),
    "constructibility_collapse": Path("Outputs/constructibility_collapse_report.json"),
    "replay_vector": Path("Outputs/replay_vector_report.json"),
    "distributed_reconstruction": Path("Outputs/distributed_reconstruction_report.json"),
    "descendant_effect": Path("Outputs/descendant_effect_report.json"),
    "continuation_pressure": Path("Outputs/continuation_pressure_report.json"),
    "irreversibility_surface": Path("Outputs/irreversibility_surface_report.json")
}

WEIGHTS = {
    "PASS": 0,
    "TRACEABLE": 0,
    "LANGUAGE_SIMPLIFIED": 0,
    "TOPOLOGY_GRAPH_GENERATED": 0,
    "HOLD": 1,
    "SHADOW": 2,
    "UNSTABLE": 3,
    "FAIL": 4,
    "CRITICAL": 5
}

def load_status(path):
    if not path.exists():
        return {
            "available": False,
            "status": "MISSING",
            "weight": 1
        }

    data = json.loads(path.read_text())
    status = data.get("status") or data.get("overall_status") or data.get("chain_status") or "UNKNOWN"

    return {
        "available": True,
        "status": status,
        "weight": WEIGHTS.get(status, 1)
    }

def classify(score):
    if score >= 24:
        return "CRITICAL"
    if score >= 16:
        return "HIGH"
    if score >= 8:
        return "ELEVATED"
    return "LOW"

def main():
    signals = {}
    total = 0

    for name, path in INPUTS.items():
        result = load_status(path)
        signals[name] = result
        total += result["weight"]

    index = classify(total)

    report = {
        "engine": "CONTINUITY_COLLAPSE_INDEX",
        "status": index,
        "continuity_survivability_score": total,
        "signals": signals,
        "observer_mode": True,
        "interpretation": "Higher score indicates greater observed continuity survivability after refusal.",
        "non_claims": [
            "Not risk certification",
            "Not proof of global collapse",
            "Not runtime enforcement",
            "Not execution authorization",
            "Not production safety guarantee"
        ]
    }

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2))
    print(f"Inputs/continuity_collapse_index -> {index}")

if __name__ == "__main__":
    main()