import json
from datetime import datetime, timezone


BOUNDARY_NOTE = (
    "This receipt is observational only. It does not provide synthesis, "
    "optimization, deployment, or capability-generation guidance."
)


def create_receipt(material_or_class: str, use_context: str = "general", inspection_scope: str = "consequence visibility"):
    return {
        "receipt_type": "material_consequence_receipt",
        "version": "0.1",
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
        "boundary_note": BOUNDARY_NOTE,
    }


if __name__ == "__main__":
    receipt = create_receipt("iron", "common material", "corrosion consequence visibility")
    print(json.dumps(receipt, indent=2))