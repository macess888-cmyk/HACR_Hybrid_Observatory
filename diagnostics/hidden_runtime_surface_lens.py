import json
from pathlib import Path

CASE_DIR = Path("diagnostics/cases")


def classify_surface(surface):
    declared = surface.get("declared")
    reachable = surface.get("runtime_reachable")
    effect_capability = surface.get("effect_capability")
    invalidation_status = surface.get("invalidation_status")

    if declared is False and reachable is True and effect_capability is True:
        return "SHADOW_SURFACE"

    if reachable == "unknown" or effect_capability == "unknown" or invalidation_status == "unknown":
        return "UNVERIFIED_SURFACE"

    if declared is True and reachable is True and effect_capability is False:
        return "KNOWN_SURFACE"

    if declared is True and reachable is True and effect_capability is True and invalidation_status != "invalidated":
        return "HOLD_REQUIRED"

    return "UNVERIFIED_SURFACE"


def run_case(path):
    data = json.loads(path.read_text(encoding="utf-8"))

    classifications = []

    for surface in data.get("runtime_surfaces", []):
        classifications.append({
            "surface": surface.get("surface"),
            "classification": classify_surface(surface)
        })

    if any(c["classification"] == "SHADOW_SURFACE" for c in classifications):
        final = "FAIL"
    elif any(c["classification"] in ["UNVERIFIED_SURFACE", "HOLD_REQUIRED"] for c in classifications):
        final = "HOLD"
    else:
        final = "PASS"

    return {
        "case": data.get("name"),
        "question": data.get("question"),
        "verdict": final,
        "classifications": classifications
    }


def main():
    results = []

    for path in sorted(CASE_DIR.glob("hidden_surface_*.json")):
        results.append(run_case(path))

    for result in results:
        print(f"{result['case']} -> {result['verdict']}")
        for item in result["classifications"]:
            print(f"  - {item['surface']}: {item['classification']}")

    pass_count = sum(1 for r in results if r["verdict"] == "PASS")
    hold_count = sum(1 for r in results if r["verdict"] == "HOLD")
    fail_count = sum(1 for r in results if r["verdict"] == "FAIL")

    print()
    print("Hidden runtime surface diagnostic lens complete.")
    print(f"PASS: {pass_count}")
    print(f"HOLD: {hold_count}")
    print(f"FAIL: {fail_count}")


if __name__ == "__main__":
    main()