# Pipeline Output Schema

The runtime pipeline runner may emit deterministic replay outputs containing:

- pipeline_id
- runtime_sequence_id
- receipt_id
- verification_status
- semantic_outputs_observed
- boundary_status
- invariant
- default_behavior

Pipeline outputs are observer-only replay artifacts.

They do NOT:
- authorize interruption
- certify governance
- prescribe remediation
- or create operational authority.

UNKNOWN -> HOLD.

Break survivability, not ontology.