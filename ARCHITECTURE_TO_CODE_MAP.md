# HACR Architecture-to-Code Map

## Purpose

Maps architectural concepts to concrete repository artifacts.

This document exists to reduce symbolic architecture drift and improve reviewer traceability.

The repository remains:

- observer-only
- deterministic
- reproducible
- non-authoritative

This map does not imply runtime orchestration or execution authority.

---

# Core Execution Boundary Concepts

| Concept | Concrete File | Output Artifact |
|---|---|---|
| Replay Vector Inspection | replay_vector_mapper.py | replay_vector_report.json |
| Refusal Propagation | refusal_propagation_mapper.py | refusal_propagation_report.json |
| Authority Survivability | authority_surface_mapper.py | authority_surface_report.json |
| Constructibility Collapse | constructibility_collapse_mapper.py | constructibility_collapse_report.json |
| Descendant Effect Mapping | descendant_effect_mapper.py | descendant_effect_report.json |
| Distributed Reconstruction | distributed_reconstruction_lens.py | distributed_reconstruction_report.json |
| Shared Persistence Lineage | shared_persistence_lineage_detector.py | shared_persistence_lineage_report.json |
| Fresh Bind Gap Detection | fresh_bind_gap_detector.py | fresh_bind_gap_report.json |
| Topology Delta Inspection | topology_delta_engine.py | topology_delta_report.json |
| Continuation Pressure Aggregation | continuation_pressure_index.py | continuation_pressure_report.json |

---

# Survivability Topology Layers

| Concept | Concrete File | Output Artifact |
|---|---|---|
| Survivability Basin Mapping | survivability_basin_mapper.py | survivability_basin_report.json |
| Survivability Corridor Mapping | survivability_corridor_mapper.py | survivability_corridor_report.json |
| Survivability Flow Field | survivability_flow_field.py | survivability_flow_field_report.json |
| Survivability Vector Field | survivability_vector_field_renderer.py | survivability_vector_field_report.json |
| Survivability Tensor Mapping | survivability_tensor_mapper.py | survivability_tensor_report.json |
| Survivability Heatmap | survivability_heatmap_generator.py | survivability_heatmap_report.json |
| Topology Projection | survivability_topology_projection_engine.py | survivability_topology_projection_report.json |
| Graph Export | survivability_graph_export_engine.py | survivability_graph_export.json |
| SVG Visualization | survivability_svg_renderer.py | survivability_graph.svg |

---

# Structural Stabilization Layers

| Concept | Concrete File | Output Artifact |
|---|---|---|
| Schema Validation | output_schema_validator.py | output_schema_validation_report.json |
| Schema Normalization | schema_normalizer.py | Outputs_Normalized/ |
| Reproducibility Verification | reproducibility_check.py | reproducibility_check_report.json |
| Dependency Graph Inspection | dependency_graph_generator.py | dependency_graph_report.json |
| Observatory Atlas | observatory_state_atlas.py | observatory_state_atlas_report.json |

---

# Execution Runners

| Concept | Concrete File | Purpose |
|---|---|---|
| Canonical Demo Runner | run_demo_v0_8.py | Deterministic survivability inspection sequence |
| Full Repository Runner | run_all.py | Executes repository-wide inspection lenses |

---

# Repository Boundary

HACR does not:

- authorize execution
- govern runtime systems
- enforce policy
- certify safety
- replace bind proof
- perform orchestration control

HACR inspects whether continuity survivability remains observable after refusal under controlled conditions.

---

# Stabilization Rule

Narrative architecture must not exceed enforceable repository structure.

All future conceptual additions should map to:

- executable file
- deterministic output
- reproducible artifact
- reviewable boundary