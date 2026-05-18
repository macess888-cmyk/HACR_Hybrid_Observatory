# Failure Formation Locator (FFL)

Observer-only diagnostic simulator for locating where continuation pressure survives after structural validity degrades.

---

# Core Question

> Where did stopping stop being viable before visible failure?

The simulator does not determine blame, predict catastrophe, certify safety, or govern execution.

Its purpose is to provide deterministic, reproducible diagnostic observations around historical failure formation conditions.

---

# Scope

The Failure Formation Locator examines:

- continuation pressure
- interruption viability
- detection degradation
- topology incompatibility
- maintenance reality divergence
- operational momentum
- operational-control drift
- hidden survivability conditions

The focus is where interruption viability begins degrading before visible collapse.

---

# Layer Separation

Diagnostic visibility is not:

- governance permission
- runtime admissibility
- execution authorization
- physical possibility determination
- operational control

Continuation observability does not determine:

- consequence legitimacy
- governance validity
- execution permissibility
- legal responsibility
- operational safety

The simulator observes diagnostic morphology only.

---

# Semantic Compression Risk

Complex operational categories can become compressed during discussion, including:

- admissibility
- governance
- permission
- synchronization
- coherence
- execution viability
- physical possibility
- runtime survivability

The simulator does not assume these categories are interchangeable.

The simulator does not use one category as a substitute for another.

---

# Observer Restriction

The simulator is strictly:

- observer-only
- deterministic
- reproducible
- non-authoritative
- execution-external

The simulator does not:

- authorize execution
- certify systems
- determine legal liability
- replace engineering review
- replace safety analysis
- predict future failure
- govern operational systems
- determine admissibility
- control runtime environments

Diagnostic outputs remain observational artifacts only.

---

# PASS / HOLD / FAIL Semantics

PASS:
- no unresolved survivability pressure detected within observed scope

HOLD:
- insufficient information
- unresolved topology visibility
- unresolved interruption viability
- unresolved continuation pressure

FAIL:
- continuation pressure survives after structural validity degradation
- interruption viability degraded
- stopping became structurally difficult
- operational continuation remained favored despite degraded validity

FAIL is not:

- a legal conclusion
- a certification result
- a governance verdict
- proof of future catastrophe

FAIL is a bounded diagnostic observation only.

---

# Current Architecture

```text
external case
->
deterministic loader
->
classification
->
portable receipt
->
canonical serialization
->
SHA256 integrity surface
```

---

# Repository Structure

```text
failure_locator/
|-- cases/
|-- receipts/
|-- failure_locator.py
`-- README.md
```

---

# Current Historical Cases

Current cases include:

- Boeing 737 MAX MCAS
- Silicon Valley Bank (2023)
- Challenger (1986)
- Deepwater Horizon (2010)

These are used as historically inspectable operational cases only.

The simulator does not perform:

- live institutional scoring
- predictive risk analysis
- regulatory assessment
- operational certification

---

# Historical Case Selection Boundary

Historical cases are selected for:

- operational inspectability
- publicly documented morphology
- continuation/interruption analysis utility

Case inclusion does not imply:

- completeness
- representational universality
- comparative severity ranking
- legal or regulatory conclusion

---

# Case File Structure

Example:

```json
{
  "name": "737_max_mcas",
  "declared_intent": "handling augmentation",
  "validity_conditions": [
    "sensor reliability"
  ],
  "drift_point": "single-sensor dependency",
  "detection_loss": "crew visibility degraded",
  "continuation_pressure": [
    "certification continuity"
  ],
  "interruption_viability": "degraded during live execution",
  "failure_locator": [
    "Human-Control Window Collapse"
  ]
}
```

---

# Receipt Structure

Example:

```json
{
  "case": "737_max_mcas",
  "diagnostic_verdict": "FAIL",
  "receipt_sha256": "..."
}
```

Receipts are:

- deterministic
- machine-readable
- reproducible
- integrity-checkable

Receipt hashes verify artifact consistency only.

Receipt hashes do not imply operational legitimacy or governance authority.

---

# Reproducibility

Run:

```bash
python failure_locator/failure_locator.py
```

The simulator:

1. Loads JSON cases
2. Validates schema structure
3. Produces deterministic classifications
4. Exports deterministic receipts
5. Generates SHA256 integrity hashes

---

# Deterministic Replay Expectation

Repeated execution against unchanged case files should produce:

- identical diagnostic outputs
- identical receipts
- identical SHA256 hashes

Any divergence indicates:

- code modification
- input modification
- environment drift
- serialization inconsistency

---

# Current Parser Limitations

Current classification logic is intentionally bounded and simplified.

The simulator currently does not:

- perform probabilistic analysis
- infer causality
- reconstruct hidden state
- perform semantic reasoning
- validate historical completeness
- model dynamic runtime evolution
- determine legal or regulatory fault
- establish predictive risk likelihood

Classification currently depends on:

- explicitly declared case structure
- bounded keyword/state interpretation
- deterministic rule evaluation

The simulator intentionally prioritizes:

- inspectability
- reproducibility
- bounded falsifiability

over semantic sophistication.

---

# Environment Validation

Validated under:

- Windows 10/11
- Python 3.x
- local filesystem execution

---

# Design Constraint

The simulator intentionally remains small enough to:

- inspect directly
- falsify directly
- reproduce independently
- pressure-test operationally

Runtime falsification overrides semantic confidence.

---

# Development Direction

Current priorities:

- reproducibility
- bounded semantics
- deterministic outputs
- reviewer falsifiability
- operational clarity
- topology-bounded diagnostics
- parser tightening
- receipt integrity
- layer separation

Avoided directions:

- ontology inflation
- generalized governance claims
- predictive authority
- universal systems theory
- operational dependency formation
- category collapse

---

# Current Stabilization Posture

Current development prioritizes:

- refinement
- parser integrity
- reproducibility
- reviewer inspectability
- bounded historical cases
- explicit limitations

The project is intentionally avoiding:

- generalized governance expansion
- predictive operationalization
- runtime integration
- execution authority
- autonomous decision systems

---

# Release Lineage

- v0.10 - initial failure formation locator
- v0.11 - external JSON case loading
- v0.12 - deterministic receipt export
- v0.13 - receipt SHA256 integrity
- v0.14 - hardened README and explicit non-claims
- v0.15 - Silicon Valley Bank historical case
- v0.16 - Challenger and Deepwater Horizon cross-domain historical cases
- v0.17 - tightened interruption viability parsing
- v0.18 - release lineage refresh
- v0.19 - README encoding artifact fix
- v0.20 - README ASCII-safe formatting
- v0.21 - simulator/runtime lineage separation
- v0.22 - reviewer hardening and stabilization notes
- v0.23 - layer separation and semantic compression limits

---

# Current Posture

The repository remains:

- observer-only
- deterministic
- historically grounded
- reproducible
- execution-external
- independently reviewable

The system is intended for:

- inspection
- falsification
- adversarial review
- historical morphology observation

It is not intended to function as:

- operational governance infrastructure
- execution authority
- regulatory enforcement
- institutional risk scoring
- predictive catastrophe modeling