# Failure Formation Locator v0.1
# Observer-only diagnostic simulator
# Purpose: locate where continuation pressure survives after validity degrades

CASES = {
    "737_max_mcas": {
        "declared_intent": "handling augmentation",
        "validity_conditions": [
            "sensor reliability",
            "pilot recoverability",
            "automation authority remains bounded",
        ],
        "drift_point": "single-sensor dependency and automation authority expansion",
        "detection_loss": "crew not reliably positioned to detect/control failure mode in time",
        "continuation_pressure": [
            "certification continuity",
            "market competition",
            "fleet commonality",
        ],
        "interruption_viability": "degraded during live execution",
        "failure_locator": [
            "Human-Control Window Collapse",
            "Runtime Authority Drift",
            "Detection Failure",
        ],
    },
    "space_shuttle": {
        "declared_intent": "low-cost reusable space transportation",
        "validity_conditions": [
            "rapid turnaround",
            "low refurbishment burden",
            "broad mission utility",
        ],
        "drift_point": "reusability remained declared while maintenance reality diverged",
        "detection_loss": "program identity preserved despite cost and turnaround mismatch",
        "continuation_pressure": [
            "institutional commitment",
            "political requirements",
            "sunk cost",
        ],
        "interruption_viability": "low once program infrastructure and mission dependency formed",
        "failure_locator": [
            "Maintenance Reality Divergence",
            "Continuation Momentum Failure",
            "Design Assumption Failure",
        ],
    },
    "vasa": {
        "declared_intent": "prestige warship with heavy firepower",
        "validity_conditions": [
            "stability margin",
            "weight distribution",
            "seaworthiness",
        ],
        "drift_point": "armament and height exceeded stability capacity",
        "detection_loss": "visible instability warnings did not stop launch",
        "continuation_pressure": [
            "royal pressure",
            "prestige",
            "schedule momentum",
        ],
        "interruption_viability": "available but politically suppressed",
        "failure_locator": [
            "Physical Constraint Violation",
            "Interruption Viability Collapse",
            "Continuation Momentum Failure",
        ],
    },
    "tacoma_narrows": {
        "declared_intent": "economical long-span suspension bridge",
        "validity_conditions": [
            "aeroelastic stability",
            "torsional rigidity",
            "wind response tolerance",
        ],
        "drift_point": "cost-driven slenderness reduced dynamic stability",
        "detection_loss": "oscillation behavior normalized before collapse",
        "continuation_pressure": [
            "cost efficiency",
            "design confidence",
            "operational use",
        ],
        "interruption_viability": "degraded once dynamic instability appeared under wind load",
        "failure_locator": [
            "Physical Constraint Violation",
            "Detection Failure",
            "Design Assumption Failure",
        ],
    },
    "ulcc": {
        "declared_intent": "maximize crude transport efficiency",
        "validity_conditions": [
            "port compatibility",
            "route compatibility",
            "market demand",
        ],
        "drift_point": "ship scale exceeded operational topology",
        "detection_loss": "local transport efficiency obscured system incompatibility",
        "continuation_pressure": [
            "cheap transport logic",
            "scale economics",
            "market expectation",
        ],
        "interruption_viability": "low after construction and fleet commitment",
        "failure_locator": [
            "Topology Incompatibility",
            "Design Assumption Failure",
            "Continuation Momentum Failure",
        ],
    },
}


def classify(case):
    unresolved = []
    fail_signals = []

    if "degraded" in case["interruption_viability"].lower():
        fail_signals.append("interruption viability degraded")

    if "low" in case["interruption_viability"].lower():
        fail_signals.append("stopping became structurally difficult")

    if case["detection_loss"]:
        fail_signals.append("detection loss or normalization present")

    if case["continuation_pressure"]:
        fail_signals.append("continuation pressure present")

    if fail_signals:
        verdict = "FAIL"
    elif unresolved:
        verdict = "HOLD"
    else:
        verdict = "PASS"

    return verdict, fail_signals


def print_case(name, case):
    verdict, signals = classify(case)

    print("=" * 72)
    print(f"CASE: {name}")
    print(f"VERDICT: {verdict}")
    print("-" * 72)
    print(f"Declared intent: {case['declared_intent']}")
    print("\nValidity conditions:")
    for item in case["validity_conditions"]:
        print(f"  - {item}")

    print(f"\nDrift point: {case['drift_point']}")
    print(f"Detection loss: {case['detection_loss']}")

    print("\nContinuation pressure:")
    for item in case["continuation_pressure"]:
        print(f"  - {item}")

    print(f"\nInterruption viability: {case['interruption_viability']}")

    print("\nFailure locator:")
    for item in case["failure_locator"]:
        print(f"  - {item}")

    print("\nDiagnostic signals:")
    for item in signals:
        print(f"  - {item}")

    print("\nCore question:")
    print("  Where did stopping stop being viable before visible failure?")
    print("=" * 72)
    print()


def main():
    print("\nFailure Formation Locator v0.1")
    print("Observer-only diagnostic simulator")
    print("No authority. No certification. No blame determination.\n")

    for name, case in CASES.items():
        print_case(name, case)


if __name__ == "__main__":
    main()