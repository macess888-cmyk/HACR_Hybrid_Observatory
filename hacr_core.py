HACR_CORE = {
    "core_invariants": [
        "no_present_state_proof_no_execution",
        "no_proof_no_bind_no_side_effect",
        "bind_is_sole_origin_of_admissible_effect",
        "refusal_must_remain_independently_available",
        "proof_must_be_present_state",
        "proof_must_be_independent",
        "proof_must_be_non_replayable",
        "proof_must_be_non_transferable"
    ]
}


def hacr_validate(state):

    failures = []
    holds = []
    stops = []
    reverses = []

    if not state.get("present_state_proof", False):
        failures.append("NO_PRESENT_STATE_PROOF")

    if not state.get("independent_proof", False):
        failures.append("NON_INDEPENDENT_PROOF")

    if not state.get("refusal_available", False):
        failures.append("REFUSAL_UNAVAILABLE")

    if state.get("effect_reachable_pre_bind", False):
        failures.append("PRE_BIND_EFFECT_REACHABLE")

    if state.get("uncertain_state", False):
        holds.append("UNCERTAIN_STATE")

    if state.get("execution_boundary_compromised", False):
        stops.append("EXECUTION_BOUNDARY_COMPROMISED")

    if state.get("effect_identity_drift", False):
        reverses.append("EFFECT_IDENTITY_DRIFT")

    if stops:
        return {
            "status": "STOP",
            "failures": failures,
            "holds": holds,
            "stops": stops,
            "reverses": reverses
        }

    if reverses:
        return {
            "status": "REVERSE",
            "failures": failures,
            "holds": holds,
            "stops": stops,
            "reverses": reverses
        }

    if failures:
        return {
            "status": "FAIL",
            "failures": failures,
            "holds": holds,
            "stops": stops,
            "reverses": reverses
        }

    if holds:
        return {
            "status": "HOLD",
            "failures": failures,
            "holds": holds,
            "stops": stops,
            "reverses": reverses
        }

    return {
        "status": "PASS",
        "failures": [],
        "holds": [],
        "stops": [],
        "reverses": []
    }