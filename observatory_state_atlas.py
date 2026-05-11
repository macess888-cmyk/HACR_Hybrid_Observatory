import json
from pathlib import Path

OUTPUT = Path("Outputs/observatory_state_atlas_report.json")

SOURCES = {
    "continuity_collapse": Path("Outputs/continuity_collapse_index_report.json"),
    "topology_pressure": Path("Outputs/topology_pressure_report.json"),
    "topology_stability": Path("Outputs/topology_stability_gradient_report.json"),
    "latent_path": Path("Outputs/latent_path_report.json"),
    "replay_vector": Path("Outputs/replay_vector_report.json"),
    "descendant_effect": Path("Outputs/descendant_effect_report.json"),
    "distributed_reconstruction": Path("Outputs/distributed_reconstruction_report.json"),
    "semantic_lineage": Path("Outputs/semantic_lineage_report.json"),
    "cross_domain_propagation": Path("Outputs/cross_domain_propagation_report.json")
}

def load(path):
    if not path.exists():
        return {"available": False, "status": "MISSING"}
    data = json.loads(path.read_text())
    return {
        "available": True,
        "status": data.get("status") or data.get("overall_status") or data.get("chain_status") or "UNKNOWN"
    }

def zone_for(name, status):
    if status in ["FAIL", "CRITICAL"]:
        return "HIGH_SURVIVABILITY_PRESSURE"
    if status == "UNSTABLE":
        return "UNSTABLE_REGION"
    if status == "SHADOW":
        return "LATENT_RECONSTRUCTION_REGION"
    if status == "HOLD":
        return "INSUFFICIENT_PROOF_REGION"
    if status in ["PASS", "TRACEABLE"]:
        return "STABLE_OBSERVED_REGION"
    return "UNKNOWN_REGION"

def main():
    zones = []
    counts = {}

    for name, path in SOURCES.items():
        result = load(path)
        zone = zone_for(name, result["status"])
        counts[zone] = counts.get(zone, 0) + 1

        zones.append({
            "source": name,
            "status": result["status"],
            "zone": zone,
            "available": result["available"]
        })

    dominant_zone = max(counts, key=counts.get) if counts else "UNKNOWN_REGION"

    report = {
        "atlas": "OBSERVATORY_STATE_ATLAS",
        "status": dominant_zone,
        "zone_counts": counts,
        "zones": zones,
        "observer_mode": True,
        "interpretation": "Maps observed continuity survivability concentration across existing diagnostic reports.",
        "non_claims": [
            "Not runtime topology control",
            "Not production monitoring",
            "Not proof of global safety",
            "Not execution authorization",
            "Not governance authority"
        ]
    }

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2))
    print(f"Inputs/observatory_state_atlas -> {dominant_zone}")

if __name__ == "__main__":
    main()