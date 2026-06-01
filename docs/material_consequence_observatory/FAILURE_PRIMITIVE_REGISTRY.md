# Material Consequence Observatory — Failure Primitive Registry

Status: Experimental v0.4 Candidate

Mode: Observer-only inspection

Control Posture:

UNKNOWN → HOLD

---

# Purpose

The Failure Primitive Registry records recurring failure classes that appear across domains.

The registry does not classify systems.

The registry classifies recurring failure mechanisms.

A primitive failure is a failure pattern that appears capable of combining with other failure patterns to produce larger consequence structures.

The goal is not prediction.

The goal is localization.

---

# Primitive Families

Current candidate families:

FP-C
Coupling Failures

FP-A
Authority Failures

FP-B
Boundary Failures

FP-R
Review Failures

FP-M
Memory Failures

FP-V
Visibility Failures

FP-T
Transfer Failures

FP-L
Localization Failures

FP-D
Drift Failures

FP-P
Preservation Failures

Status:

UNDER ACTIVE REVIEW

---

# FP-C — Coupling Failures

Definition:

Representation loses reliable correspondence with the underlying reality condition.

Examples:

Signal ≠ Reality

Confidence ≠ Verification

Consensus ≠ Coherence

Indicators:

* stale measurements
* recursive reinforcement
* hidden divergence
* degraded contradiction pathways

Potential Transitions:

FP-C → FP-D

FP-C → FP-V

FP-C → FP-A

---

# FP-A — Authority Failures

Definition:

Authority becomes detached from legitimacy, accountability, or admissibility.

Examples:

Authorization ≠ Governance

Observation → Authority

Prediction → Authority

Indicators:

* authority drift
* accountability loss
* governance fragmentation

Potential Transitions:

FP-A → FP-B

FP-A → FP-C

FP-A → FP-P

---

# FP-B — Boundary Failures

Definition:

Distinct operational layers collapse into one another.

Examples:

Observation = Execution

Interpretation = Authority

Governance = Action

Indicators:

* collapsed review surfaces
* missing separation
* implicit authority migration

Potential Transitions:

FP-B → FP-A

FP-B → FP-C

---

# FP-R — Review Failures

Definition:

Review processes become self-reinforcing rather than corrective.

Examples:

Review
↓
Confidence
↓
Suppression

Indicators:

* contradiction reduction
* alternative elimination
* recursive agreement

Potential Transitions:

FP-R → FP-M

FP-R → FP-C

---

# FP-M — Memory Failures

Definition:

Stored history begins degrading future determination quality.

Examples:

Poisoned memory

Recursive reinforcement

Consolidated error

Indicators:

* repeated historical reuse
* correction failure
* path dependency

Potential Transitions:

FP-M → FP-R

FP-M → FP-C

---

# FP-V — Visibility Failures

Definition:

Relevant conditions become hidden while remaining active.

Examples:

Latent drift

Invisible degradation

Silent dependency collapse

Indicators:

* delayed detection
* hidden transitions
* missing observability

Potential Transitions:

FP-V → FP-D

FP-V → FP-C

---

# FP-T — Transfer Failures

Definition:

A property is assumed transferable without validating admissibility.

Examples:

Similarity → Permission

Model A → Model B

Domain A → Domain B

Indicators:

* analogical transfer
* unsupported equivalence
* domain collapse

Potential Transitions:

FP-T → FP-C

FP-T → FP-A

---

# FP-L — Localization Failures

Definition:

The system cannot reliably determine where responsibility, causation, or condition resides.

Examples:

Responsibility fragmentation

Attribution collapse

Causation ambiguity

Indicators:

* diffuse ownership
* unclear source conditions
* attribution uncertainty

Potential Transitions:

FP-L → FP-A

FP-L → FP-V

---

# FP-D — Drift Failures

Definition:

The system changes while appearing stable.

Examples:

Capability remains

Coherence degrades

Certificate remains

Trust degrades

Indicators:

* divergence accumulation
* baseline shift
* hidden transition

Potential Transitions:

FP-D → FP-C

FP-D → FP-V

FP-D → FP-P

---

# FP-P — Preservation Failures

Definition:

The structures required to maintain a condition degrade.

Examples:

Condition ≠ Formation Preconditions

Presence ≠ Integrity

Persistence ≠ Function

Indicators:

* maintenance erosion
* formation degradation
* recoverability collapse

Potential Transitions:

FP-P → FP-D

FP-P → FP-C

---

# Compound Failure Candidates

CF-001

Consensus Drift

FP-R + FP-M + FP-C

---

CF-002

Authority Mislocalization

FP-A + FP-L + FP-C

---

CF-003

Governance Collapse

FP-A + FP-B + FP-V

---

CF-004

Trust Degradation

FP-P + FP-D + FP-C

---

CF-005

Review-Lock Formation

FP-R + FP-M + FP-V

---

# Open Questions

Are these primitive?

Are additional families required?

Can primitives combine recursively?

Can primitive transitions be mapped?

Can primitive compounds predict consequence surfaces?

Status:

ACTIVE RESEARCH

---

Repository Status

Invariant Registry
✓

Formation Preconditions
✓

Geometry Collapse Atlas
✓

Transition Logic Queue
✓

Failure Primitive Registry
✓ Candidate

UNKNOWN → HOLD
