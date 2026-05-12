# Diagram Evidence Binding

Purpose:
Prevent architecture and topology diagrams from becoming free-floating symbolic structures detached from executable evidence.

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
| Observable State | FAIL / SHADOW |
| Limitation | bounded observer visibility only |

---

# Descendant Effect Map

| Surface | Mapping |
|---|---|
| Input | Inputs/distributed_reconstruction_case.json |
| Execution | python run_all.py |
| Artifact | Outputs/descendant_effect_map.svg |
| Observable State | TRACEABLE |
| Limitation | partial topology visibility |

---

# Reconstruction Projection Diagram

| Surface | Mapping |
|---|---|
| Input | Inputs/reconstruction_path_case.json |
| Execution | python run_all.py |
| Artifact | Outputs/reconstruction_projection.svg |
| Observable State | PROJECTED |
| Limitation | observer-side inference only |

---

# Deterministic Export Graphs

| Surface | Mapping |
|---|---|
| Input | deterministic topology inputs |
| Execution | graph export pipeline |
| Artifact | SVG / JSON graph outputs |
| Observable State | EXPORTED |
| Limitation | inspection artifact only |

---

# Diagram Constraint

Diagrams are inspection artifacts only.

Diagrams do not represent:

- complete system topology
- operational truth
- runtime authority
- governance legitimacy
- execution control surfaces
- production completeness

All diagrams remain:

- observer-restricted
- deterministic
- bounded
- reproducible
- non-authoritative

---

# Interpretation Constraint

If a diagram requires narrative explanation exceeding executable evidence support,
the diagram should be treated as conceptual-only rather than operationally stabilized.

Executable evidence must upper-bound diagram interpretation scope.