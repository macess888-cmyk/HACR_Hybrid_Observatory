from tools.observatory_core.reduction_horizon import (
    extract_reduction_horizon
)


def extract_visibility_extinction_boundary(data):

    horizon_report = extract_reduction_horizon(data)

    horizon = horizon_report["reduction_horizon"]

    remainder = horizon["visibility_remainder"]

    extinction_boundary = {
        "name": "VISIBILITY_EXTINCTION_BOUNDARY",
        "classification":
            "VISIBILITY_EXTINCTION_BOUNDARY",

        "remaining_structure":
            horizon["remaining_structure"],

        "visibility_remainder":
            remainder,

        "distance_to_extinction":
            round(
                max(0.0, 1.0 - remainder),
                4
            )
    }

    extinction_front = {
        "name": "EXTINCTION_FRONT",
        "classification": "EXTINCTION_FRONT",
        "strength": round(
            max(0.0, 1.0 - remainder),
            4
        )
    }

    extinction_core = {
        "name": "EXTINCTION_CORE",
        "classification": "EXTINCTION_CORE",
        "stability": remainder
    }

    return {
        "status":
            "VISIBILITY_EXTINCTION_BOUNDARY_COMPLETE",

        "visibility_extinction_boundary":
            extinction_boundary,

        "extinction_front":
            extinction_front,

        "extinction_core":
            extinction_core,

        "reduction_horizon":
            horizon,

        "observer_mode":
            True,

        "prediction":
            False,

        "routing":
            False,

        "causality_certification":
            False,

        "governance_authority":
            False
    }