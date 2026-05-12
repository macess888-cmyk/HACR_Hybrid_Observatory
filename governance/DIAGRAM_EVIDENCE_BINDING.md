# Diagram Evidence Binding

Purpose:
Prevent architecture diagrams from becoming free-floating symbolic structures detached from executable evidence.

Core rule:

Every diagram must map directly to:

- executable source
- deterministic run path
- observable artifact
- bounded interpretation scope

No diagram may imply:

- orchestration authority
- runtime control
- governance enforcement
- universal topology visibility
- operational completeness

---

# Replay Vector Diagram

| Surface | Mapping |
|---|---|
| Input | Inputs/watchdog_continuity_case.json |
| Execution | python run_all.py |
| Artifact | Outputs/replay_vector_graph.svg |
| Limitation | bounded observer visibility only |

---

# Descendant Effect Map

| Surface | Mapping |
|---|---|
| Input | Inputs/distributed_reconstruction_case.json |
| Execution | python run_all.py |
| Artifact | Outputs/descendant_effect_map.svg |
| Limitation | partial topology visibility |

---

# Reconstruction Projection Diagram

| Surface | Mapping |
|---|---|
| Input | Inputs/reconstruction_path_case.json |
| Execution | python run_all.py |
| Artifact | Outputs/reconstruction_projection.svg |
| Limitation | observer-side inference only |

---

# Diagram Constraint

Diagrams are inspection artifacts only.

Diagrams do not represent:

- complete system topology
- operational truth
- runtime state authority
- governance legitimacy
- execution control surfaces

All diagrams remain:

- observer-restricted
- deterministic
- bounded
- reproducible
- non-authoritative