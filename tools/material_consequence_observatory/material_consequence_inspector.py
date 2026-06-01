"""
Material Consequence Observatory

Version: 0.2

Observer-only consequence inspection.

This tool does not:
- synthesize
- optimize
- deploy
- weaponize
- enhance

It generates consequence receipts only.

UNKNOWN → HOLD
"""

import json
from datetime import datetime, timezone


BOUNDARY_NOTE = (
    "This receipt is observational only. "
    "It does not provide synthesis, optimization, "
    "deployment, or capability-generation guidance."
)


def create_receipt(
    material_or_class: str,
    use_context: str = "general",
    inspection_scope: str = "consequence visibility"
):
    """
    Create a Material Consequence Receipt.

    Observer-only.
    No capability generation.
    """

    return {
        "receipt_type": "material_consequence_receipt",
        "version": "0.2",
        "created_utc": datetime.now(timezone.utc).isoformat(),

        "material_or_class": material_or_class,
        "use_context": use_context,
        "inspection_scope": inspection_scope,

        "known_properties": [],
        "interaction_surfaces": [],
        "degradation_or_decay_pathways": [],
        "exposure_pathways": [],
        "environmental_persistence": [],

        "human_concerns": [],
        "ecological_concerns": [],
        "dependency_effects": [],

        "recoverability_notes": [],
        "misuse_or_dual_use_flags": [],
        "known_unknowns": [],

        "status": "GREEN",

        "boundary_note": BOUNDARY_NOTE
    }


def print_receipt(receipt: dict):
    """
    Pretty-print receipt.
    """
    print(json.dumps(receipt, indent=2))


def main():
    """
    Safe example inspection.
    """

    receipt = create_receipt(
        material_or_class="iron",
        use_context="common material",
        inspection_scope="corrosion consequence visibility"
    )

    print_receipt(receipt)


if __name__ == "__main__":
    main()