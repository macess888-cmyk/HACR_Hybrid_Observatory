import json


def evaluate_watchdog(case):
    stale_restart = case.get("stale_restart", False)
    preserved_state = case.get("preserved_state", False)
    fresh_bind_required = case.get("fresh_bind_required", True)
    recovery_path_active = case.get("recovery_path_active", False)
    hidden_continuation = case.get("hidden_continuation", False)
    effect_reachable = case.get("effect_reachable", False)

    result = {
        "watchdog_status": "PASS",
        "reason": [],
    }

    if hidden_continuation:
        result["watchdog_status"] = "SHADOW"
        result["reason"].append(
            "Hidden continuation path detected."
        )

    if stale_restart or preserved_state:
        result["watchdog_status"] = "HOLD"
        result["reason"].append(
            "Restart continuity may preserve stale execution assumptions."
        )

    if recovery_path_active and not fresh_bind_required:
        result["watchdog_status"] = "FAIL"
        result["reason"].append(
            "Recovery path active without mandatory fresh bind."
        )

    if effect_reachable:
        result["watchdog_status"] = "STOP"
        result["reason"].append(
            "Effect reachable through continuation path before fresh bind."
        )

    if not result["reason"]:
        result["reason"].append(
            "No watchdog continuity contradictions detected within tested scope."
        )

    return result


def run_watchdog(input_path, output_path):
    with open(input_path, "r") as f:
        case = json.load(f)

    result = evaluate_watchdog(case)

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    print(
        f"{input_path} -> "
        f"{result['watchdog_status']}"
    )


if __name__ == "__main__":
    run_watchdog(
        "Inputs/watchdog_continuity_case.json",
        "Outputs/watchdog_report.json"
    )