# Evidence Anchor Map

Purpose:
Ensure all major observability concepts remain directly tied to executable evidence surfaces.

Core rule:

No major concept may exist without:
- executable input
- deterministic run path
- observable artifact
- bounded limitation statement

---

# Replay Vector Inspection

| Surface | Evidence |
|---|---|
| Input | Inputs/watchdog_continuity_case.json |
| Execution | python run_all.py |
| Artifact | Outputs/replay_vector_graph.svg |
| Observable State | FAIL / SHADOW |
| Limitation | bounded observer visibility only |

---

# Descendant Effect Mapping

| Surface | Evidence |
|---|---|
| Input | Inputs/distributed_reconstruction_case.json |
| Execution | python run_all.py |
| Artifact | Outputs/descendant_effect_map.svg |
| Observable State | TRACEABLE |
| Limitation | partial topology visibility |

---

# Distributed Reconstruction Visibility

| Surface | Evidence |
|---|---|
| Input | Inputs/reconstruction_path_case.json |
| Execution | python run_all.py |
| Artifact | Outputs/reconstruction_projection.svg |
| Observable State | PROJECTED |
| Limitation | observer-restricted inference only |

---

# Deterministic Graph Export

| Surface | Evidence |
|---|---|
| Input | deterministic topology input |
| Execution | graph export pipeline |
| Artifact | SVG / JSON graph outputs |
| Observable State | EXPORTED |
| Limitation | graph is inspection artifact only |

---

# Observer Boundary

All evidence surfaces remain:

- observer-only
- non-authoritative
- non-remediating
- non-execution-addressable
- non-orchestrative

No artifact may become operationally consumable by execution systems.