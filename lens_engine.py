def continuity_lens(state):

    drift = state.get("semantic_drift", False)
    replay = state.get("replay_detected", False)

    if drift or replay:
        return "DRIFT"

    return "STABLE"


def symmetry_lens(state):

    if state.get("hidden_privilege_path", False):
        return "ASYMMETRIC"

    return "SYMMETRIC"


def constructibility_lens(state):

    plurality = state.get("constructible_states", 0)

    if plurality <= 1:
        return "COLLAPSED"

    return "OPEN"