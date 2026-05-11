import json
from pathlib import Path

INPUT = Path("Inputs/survivability_corridor_case.json")
OUTPUT = Path("Outputs/survivability_corridor_report.json")

def strength_for(corridor):
    score = 0

    score += len(corridor.get("surfaces", []))

    if corridor.get("effect_capable"):
        score += 3

    if corridor.get("reconstructible"):
        score += 2

    if corridor.get("cross_domain"):
        score += 2

    if corridor.get("retry_enabled"):
        score += 1

    if corridor.get("callback_enabled"):
        score += 1

    return score

def classify(score):
    if score >= 8:
        return "CRITICAL"
    if score >= 6:
        return "HIGH"
    if score >= 3:
        return "ELEVATED"
    return "LOW"

def main():
    data = json.loads(INPUT.read_text())
    corridors = data.get("corridors", [])

    mapped = []
    strongest = 0

    for c in corridors:
        score = strength_for(c)
        strongest = max(strongest, score)

        mapped.append({
            "corridor_id": c.get("corridor_id"),
            "surfaces": c.get("surfaces", []),
            "corridor_depth": len(c.get("surfaces", [])),
            "effect_capable": c.get("effect_capable", False),
            "reconstructible": c.get("reconstructible", False),
            "cross_domain": c.get("cross_domain", False),
            "corridor_strength_score": score,
            "corridor_status": classify(score)
        })

    overall = classify(strongest)

    report = {
        "lens": "SURVIVABILITY_CORRIDOR_MAPPER",
        "status": overall,
        "corridor_count": len(mapped),
        "strongest_corridor_score": strongest,
        "corridors": mapped,
        "observer_mode": True,
        "interpretation": "Maps connected survivability corridors across topology surfaces after refusal.",
        "non_claims": [
            "Not runtime enforcement",
            "Not execution authorization",
            "Not proof of hidden execution",
            "Not production monitoring",
            "Not certification"
        ]
    }

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2))
    print(f"{INPUT} -> {overall}")

if __name__ == "__main__":
    main()