# Material Consequence Receipt Schema

## Purpose

A Material Consequence Receipt is an observer-only record of consequence visibility.

It does not certify safety.

It does not authorize use.

It does not provide technical synthesis or optimization instructions.

## Receipt Fields

```json
{
  "receipt_type": "material_consequence_receipt",
  "version": "0.1",
  "material_or_class": "",
  "use_context": "",
  "inspection_scope": "",
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
  "status": "GREEN | YELLOW | HOLD",
  "boundary_note": "This receipt is observational only. It does not provide synthesis, optimization, deployment, or capability-generation guidance."
}