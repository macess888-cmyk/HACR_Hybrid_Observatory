import json
from pathlib import Path

SCENARIO_DIR = Path("runtime/scenarios")


def classify_surface(surface):
    delay = surface.get("invalidation_delay_ms")
    exposure = surface.get("capability_exposure_ms")
    capability = surface.get("capability_realizable")
    fresh_bind = surface.get("fresh_bind_required")

    if fresh_bind is True:
        return "PASS"

    if capability is True:
        return "FAIL"

    if capability == "unknown":
        return "HOLD"

    if delay is None or exposure is None:
        return "HOLD"

    if exposure > delay:
        return "FAIL"

    return "PASS"


def run_scenario(path):
    data = json.loads(path.read_text(encoding="utf-8"))

    verdicts = []
    surfaces = []

    for surface in data.get("runtime_surfaces", []):
        verdict = classify_surface(surface)
        verdicts.append(verdict)

        surfaces.append({
            "surface": surface.get("surface"),
            "verdict": verdict,
            "invalidation_delay_ms": surface.get("invalidation_delay_ms"),
            "capability_exposure_ms": surface.get("capability_exposure_ms"),
        })

    if "FAIL" in verdicts:
        final = "FAIL"
    elif "HOLD" in verdicts:
        final = "HOLD"
    else:
        final = "PASS"

    return {
        "scenario": data.get("name"),
        "question": data.get("question"),
        "verdict": final,
        "surfaces": surfaces,
    }


def main():
    results = []

    for path in sorted(SCENARIO_DIR.glob("*.json")):
        results.append(run_scenario(path))

    for result in results:
        print(f"{result['scenario']} -> {result['verdict']}")
        for surface in result["surfaces"]:
            print(
                f"  - {surface['surface']}: {surface['verdict']} "
                f"(delay={surface['invalidation_delay_ms']}ms, "
                f"exposure={surface['capability_exposure_ms']}ms)"
            )

    pass_count = sum(1 for r in results if r["verdict"] == "PASS")
    hold_count = sum(1 for r in results if r["verdict"] == "HOLD")
    fail_count = sum(1 for r in results if r["verdict"] == "FAIL")

    print()
    print("Distributed invalidation propagation simulation complete.")
    print(f"PASS: {pass_count}")
    print(f"HOLD: {hold_count}")
    print(f"FAIL: {fail_count}")


if __name__ == "__main__":
    main()