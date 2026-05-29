from tools.observatory_core.visibility_extinction_boundary import (
    extract_visibility_extinction_boundary
)


def extract_reduction_residue(data):

    extinction_report = (
        extract_visibility_extinction_boundary(data)
    )

    boundary = extinction_report[
        "visibility_extinction_boundary"
    ]

    residue = {
        "name": "REDUCTION_RESIDUE",
        "classification": "REDUCTION_RESIDUE",
        "irreducible_structure":
            boundary["remaining_structure"],
        "residue_strength":
            boundary["visibility_remainder"],
        "reduction_depth":
            boundary["distance_to_extinction"]
    }

    residue_core = {
        "name": "RESIDUE_CORE",
        "classification": "RESIDUE_CORE",
        "stability":
            boundary["visibility_remainder"]
    }

    return {
        "status":
            "REDUCTION_RESIDUE_COMPLETE",

        "reduction_residue":
            residue,

        "residue_core":
            residue_core,

        "visibility_extinction_boundary":
            boundary,

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