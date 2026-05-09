def drift_trajectory(state):

    drift_flags = {
        "authority_drift": state.get("authority_drift", False),
        "semantic_drift": state.get("semantic_drift", False),
        "configuration_drift": state.get("configuration_drift", False),
        "dependency_drift": state.get("dependency_drift", False),
        "effect_identity_drift": state.get("effect_identity_drift", False)
    }

    drift_count = sum(1 for value in drift_flags.values() if value)

    if state.get("effect_identity_drift", False):
        status = "IRREVERSIBLE_DRIFT"
    elif drift_count >= 3:
        status = "UNSTABLE"
    elif drift_count >= 1:
        status = "DRIFTING"
    else:
        status = "STABLE"

    return {
        "status": status,
        "flags": drift_flags,
        "drift_count": drift_count
    }