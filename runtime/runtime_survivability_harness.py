import json
from pathlib import Path

SCENARIO_DIR = Path("runtime/scenarios")

def classify(surface):
    if surface.get("fresh_bind_required") is True:
        return "PASS"

    if surface.get("capability_realizable") is True:
        return "FAIL"

    if surface.get("capability_realizable") == "unknown":
        return "HOLD"

    if surface.get("invalidation_proven") is True:
        return "PASS"

    return "HOLD"


def run_scenario(path):
    data = json.loads(path.read_text(encoding="utf-8"))

    verdicts = []
    for surface in data.get("runtime_surfaces", []):
        verdicts.append(classify(surface))

    if "FAIL" in verdicts:
        final = "FAIL"
    elif "HOLD" in verdicts:
        final = "HOLD"
    else:
        final = "PASS"

    return {
        "scenario": data["name"],
        "question": data["question"],
        "verdict": final,
        "surface_verdicts": verdicts,
    }


def main():
    results = []

    for path in sorted(SCENARIO_DIR.glob("*.json")):
        results.append(run_scenario(path))

    for result in results:
        print(f"{result['scenario']} -> {result['verdict']}")

    pass_count = sum(1 for r in results if r["verdict"] == "PASS")
    hold_count = sum(1 for r in results if r["verdict"] == "HOLD")
    fail_count = sum(1 for r in results if r["verdict"] == "FAIL")

    print()
    print("Runtime survivability harness complete.")
    print(f"PASS: {pass_count}")
    print(f"HOLD: {hold_count}")
    print(f"FAIL: {fail_count}")


if __name__ == "__main__":
    main()