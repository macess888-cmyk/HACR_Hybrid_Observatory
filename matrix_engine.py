def reachability_matrix(state):

    matrix = {
        "authority_path": False,
        "retry_path": False,
        "watchdog_path": False,
        "dependency_path": False,
        "downstream_effect_path": False
    }

    if state.get("authority_active", False):
        matrix["authority_path"] = True

    if state.get("retry_surface_present", False):
        matrix["retry_path"] = True

    if state.get("watchdog_recovery_enabled", False):
        matrix["watchdog_path"] = True

    if state.get("dependency_chain_present", False):
        matrix["dependency_path"] = True

    if state.get("effect_reachable_pre_bind", False):
        matrix["downstream_effect_path"] = True

    return matrix


def matrix_risk_score(matrix):

    score = 0

    for _, value in matrix.items():

        if value:
            score += 1

    if score == 0:
        return "MINIMAL"

    if score <= 2:
        return "MODERATE"

    if score <= 4:
        return "HIGH"

    return "CRITICAL"