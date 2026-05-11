import json
from pathlib import Path

FLOW = Path("Outputs/survivability_flow_field_report.json")
OUTPUT = Path("Outputs/survivability_vector_field_report.json")

def load(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def classify(magnitude):
    if magnitude >= 20:
        return "CRITICAL"
    if magnitude >= 12:
        return "HIGH"
    if magnitude >= 6:
        return "ELEVATED"
    return "LOW"

def main():
    flow = load(FLOW)

    vectors = []

    for item in flow.get("flows", []):
        source = item.get("source")
        target = item.get("target")
        magnitude = item.get("flow_strength", 0)

        vectors.append({
            "vector": f"{source} -> {target}",
            "source": source,
            "target": target,
            "magnitude": magnitude,
            "orientation": "FORWARD_CONTINUITY_PRESSURE",
            "status": classify(magnitude)
        })

    strongest = max([v["magnitude"] for v in vectors], default=0)

    report = {
        "renderer": "SURVIVABILITY_VECTOR_FIELD",
        "status": classify(strongest),
        "vector_count": len(vectors),
        "strongest_vector_magnitude": strongest,
        "vectors": vectors,
        "observer_mode": True,
        "interpretation": "Renders directional survivability pressure as observer-side topology vectors.",
        "non_claims": [
            "Not runtime routing",
            "Not execution control",
            "Not prediction",
            "Not production monitoring",
            "Not certification"
        ]
    }

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2))
    print(f"Inputs/survivability_vector_field -> {report['status']}")

if __name__ == "__main__":
    main()