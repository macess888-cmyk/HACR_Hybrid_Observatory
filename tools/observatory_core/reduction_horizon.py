from tools.observatory_core.anchor_attractor import (
    extract_anchor_attractor
)


def extract_reduction_horizon(data):

    attractor_report = extract_anchor_attractor(data)

    attractor = attractor_report["anchor_attractor"]

    remaining_structure = (
        attractor["source_anchor_count"]
        + attractor["source_connectivity_count"]
    )

    survivability_distance = round(
        remaining_structure / 10.0,
        4
    )

    horizon = {
        "name": "REDUCTION_HORIZON",
        "classification": "REDUCTION_HORIZON",
        "remaining_structure": remaining_structure,
        "survivability_distance": survivability_distance,
        "visibility_remainder": round(
            survivability_distance,
            4
        )
    }

    exhaustion_boundary = {
        "name": "EXHAUSTION_BOUNDARY",
        "classification": "VISIBILITY_EXHAUSTION_BOUNDARY",
        "remaining_structure": remaining_structure
    }

    return {
        "status":
            "REDUCTION_HORIZON_EXTRACTION_COMPLETE",

        "reduction_horizon":
            horizon,

        "exhaustion_boundary":
            exhaustion_boundary,

        "anchor_attractor":
            attractor,

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