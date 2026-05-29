from tools.observatory_core.reduction_residue import (
    extract_reduction_residue
)


def extract_irreducible_core(data):

    residue_report = extract_reduction_residue(data)

    residue = residue_report[
        "reduction_residue"
    ]

    irreducible_core = {
        "name": "IRREDUCIBLE_CORE",
        "classification": "IRREDUCIBLE_CORE",

        "core_structure":
            residue["irreducible_structure"],

        "core_stability":
            residue["residue_strength"],

        "reduction_limit":
            residue["reduction_depth"]
    }

    core_invariant = {
        "name": "CORE_INVARIANT",
        "classification": "CORE_INVARIANT",

        "stability":
            residue["residue_strength"]
    }

    core_residue = {
        "name": "CORE_RESIDUE",
        "classification": "CORE_RESIDUE",

        "remaining_visibility":
            residue["residue_strength"]
    }

    reduction_limit = {
        "name": "REDUCTION_LIMIT",
        "classification": "REDUCTION_LIMIT",

        "depth":
            residue["reduction_depth"]
    }

    return {
        "status":
            "IRREDUCIBLE_CORE_COMPLETE",

        "irreducible_core":
            irreducible_core,

        "core_invariant":
            core_invariant,

        "core_residue":
            core_residue,

        "reduction_limit":
            reduction_limit,

        "reduction_residue":
            residue,

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