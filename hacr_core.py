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

    if not state.get("present_state_proof", False):
        failures.append("NO_PRESENT_STATE_PROOF")

    if not state.get("independent_proof", False):
        failures.append("NON_INDEPENDENT_PROOF")

    if not state.get("refusal_available", False):
        failures.append("REFUSAL_UNAVAILABLE")

    if state.get("effect_reachable_pre_bind", False):
        failures.append("PRE_BIND_EFFECT_REACHABLE")

    if failures:
        return {
            "status": "FAIL",
            "failures": failures
        }

    return {
        "status": "PASS",
        "failures": []
    }