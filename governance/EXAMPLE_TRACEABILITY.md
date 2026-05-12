# Example Traceability

Purpose:
Anchor key observatory examples from input to output so reviewers can inspect deterministic evidence paths without relying on symbolic interpretation.

Core rule:

Each example must show:

input → execution → output → observable state → limitation

---

# Example 1: Watchdog Continuity Case

| Stage | Evidence |
|---|---|
| Input | Inputs/watchdog_continuity_case.json |
| Execution | python run_all.py |
| Expected State | FAIL / SHADOW |
| Artifact Type | deterministic output / graph artifact |
| Inspection Question | Can consequence survivability remain reachable after refusal through replay, retry, or watchdog continuation? |
| Limitation | Bounded to modeled topology and available observer visibility |

Interpretation:

This example does not prove global consequence extinction.

It only exposes whether continuation survivability remains observable within the inspected evidence surface.

---

# Example 2: Distributed Reconstruction Case

| Stage | Evidence |
|---|---|
| Input | Inputs/distributed_reconstruction_case.json |
| Execution | python run_all.py |
| Expected State | TRACEABLE / PROJECTED |
| Artifact Type | reconstruction or descendant-effect artifact |
| Inspection Question | Can consequence become reconstructible through distributed continuation paths after local refusal? |
| Limitation | Partial topology visibility only |

Interpretation:

This example does not assert complete system topology.

It maps bounded reconstructibility pressure visible to the observer layer.

---

# Example Constraint

Examples are inspection traces only.

They do not:

- authorize execution
- enforce refusal
- certify safety
- prove completeness
- replace runtime admissibility checks
- mediate operational decisions

Each example remains:

- deterministic
- reproducible
- bounded
- observer-restricted
- non-authoritative