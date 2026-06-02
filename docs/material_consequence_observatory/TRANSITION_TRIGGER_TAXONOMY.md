# Material Consequence Observatory — Transition Trigger Taxonomy

Status: Experimental v0.5 Candidate

Mode: Observer-only inspection

Control posture:

UNKNOWN → HOLD

---

# Purpose

This document attempts to identify, classify, reduce, and pressure-test transition triggers.

Current observatory architecture can identify:

* primitives
* primitive degradation
* latent persistence
* consequence

The largest remaining uncertainty is:

```text
What activates transition?
```

---

# Transition Logic Under Test

Current model:

```text
Primitive Degradation
↓
Latent Persistence
↓
Transition Trigger
↓
Compound Failure
↓
Consequence
```

Question:

```text
What is a transition trigger?
```

---

# Current Candidate Trigger Families

Observed during validation receipts:

```text
Load Exposure

Time Compression

Novelty Exposure

Contradiction Exposure

Resource Exhaustion

Dependency Activation

Environmental Change

Authority Compression

Coordination Saturation
```

Current task:

Determine whether these are:

```text
Independent trigger families
```

or

```text
Variants of a deeper trigger.
```

---

# Trigger Family 1

Load Exposure

Definition:

```text
Required capacity exceeds available capacity.
```

Examples:

* power grid overload
* hospital demand surge
* infrastructure stress
* liquidity pressure

Assessment:

Strong candidate.

---

# Trigger Family 2

Time Compression

Definition:

```text
Required response speed exceeds available decision capacity.
```

Examples:

* military identification
* emergency medicine
* cyber incident response

Observation:

May be load exposure expressed through time.

Candidate reduction:

```text
Time Compression
=
Capacity Mismatch
```

Assessment:

Possibly derived.

---

# Trigger Family 3

Novelty Exposure

Definition:

```text
Reality presents conditions outside learned, expected,
or modeled conditions.
```

Examples:

* novel disease
* novel attack
* novel market event
* novel model input

Observation:

May expose hidden primitive degradation.

Assessment:

Candidate trigger.

---

# Trigger Family 4

Contradiction Exposure

Definition:

```text
Reality presents evidence inconsistent with existing representation.
```

Examples:

* scientific contradiction
* governance audit
* model evaluation failure

Observation:

May activate coupling stress.

Assessment:

Strong candidate.

---

# Trigger Family 5

Resource Exhaustion

Definition:

```text
Required resources exceed available resources.
```

Examples:

* staffing depletion
* energy depletion
* liquidity depletion
* compute exhaustion

Observation:

Potential special case of load exposure.

Assessment:

Likely derived.

---

# Trigger Family 6

Dependency Activation

Definition:

```text
Previously hidden dependency becomes operationally relevant.
```

Examples:

* supply chain failure
* infrastructure dependency exposure
* software dependency activation

Observation:

Creates visibility pressure.

Assessment:

Candidate trigger.

---

# Trigger Family 7

Environmental Change

Definition:

```text
External conditions change sufficiently
to invalidate assumptions.
```

Examples:

* climate event
* regulatory shift
* market regime change
* geopolitical change

Observation:

May create novelty exposure.

Assessment:

Possibly derived.

---

# Trigger Family 8

Authority Compression

Definition:

```text
Decision demand exceeds available review capacity.
```

Examples:

* military escalation
* executive crisis response
* emergency governance

Observation:

Appears related to time compression.

Assessment:

Possibly derived.

---

# Trigger Family 9

Coordination Saturation

Definition:

```text
Required coordination exceeds available coherence.
```

Examples:

* organizational collapse
* hospital overload
* large-system failure

Observation:

Appears related to capacity mismatch.

Assessment:

Possibly derived.

---

# First Reduction Attempt

Current reduction:

```text
Load Exposure

Time Compression

Resource Exhaustion

Authority Compression

Coordination Saturation
```

all appear reducible to:

```text
Required Capacity
>
Available Capacity
```

Candidate super-family:

```text
Capacity Mismatch
```

---

# Second Reduction Attempt

Current reduction:

```text
Novelty Exposure

Environmental Change

Dependency Activation

Contradiction Exposure
```

appear related to:

```text
Reality reveals assumption failure.
```

Candidate super-family:

```text
Assumption Exposure
```

---

# Emerging Trigger Hierarchy

## Tier 1 Candidate Families

```text
Capacity Mismatch

Assumption Exposure
```

---

## Tier 2 Candidate Families

```text
Load Exposure

Time Compression

Novelty Exposure

Contradiction Exposure

Dependency Activation

Environmental Change

Authority Compression

Coordination Saturation

Resource Exhaustion
```

---

# Capacity Mismatch

Candidate definition:

```text
The system is required to provide
more capability than currently exists.
```

Examples:

* hospital overload
* power grid overload
* decision overload
* coordination overload

Assessment:

Strong candidate root trigger.

---

# Assumption Exposure

Candidate definition:

```text
Reality reveals assumptions
that can no longer be maintained.
```

Examples:

* scientific contradiction
* model failure
* governance audit
* novel event

Assessment:

Strong candidate root trigger.

---

# Reduction Question

Can all trigger families collapse into:

```text
Capacity Mismatch

and

Assumption Exposure
```

Current evidence:

Possibly.

Further pressure required.

---

# Cross-Domain Validation

Infrastructure:

```text
Capacity Mismatch
```

Healthcare:

```text
Capacity Mismatch
```

Finance:

```text
Assumption Exposure
+
Capacity Mismatch
```

Military:

```text
Time Compression
→ Capacity Mismatch
```

Governance:

```text
Authority Compression
→ Capacity Mismatch
```

Models:

```text
Novelty Exposure
→ Assumption Exposure
```

Scientific Consensus:

```text
Contradiction Exposure
→ Assumption Exposure
```

Current pressure:

Supports reduction.

---

# Strongest Trigger Candidate

Current strongest candidate:

```text
Capacity Mismatch
```

because it appears repeatedly across domains.

---

# Most Interesting Open Question

Can:

```text
Assumption Exposure
```

be reduced further into:

```text
Capacity Mismatch
```

or are they fundamentally distinct?

Current evidence:

Insufficient.

---

# Current Assessment

```text
Architecture = STABLE

Primitive Registry = UNDER REDUCTION

Transition Logic = UNDER REDUCTION

Strongest Trigger Candidate = Capacity Mismatch

Second Trigger Candidate = Assumption Exposure

Research Complete = NO

UNKNOWN → HOLD
```

---

# Next Required Artifact

```text
FAILURE_COMPOUND_REGISTRY.md
```

Purpose:

Determine whether primitive combinations form stable compound families analogous to:

```text
chemistry
```

rather than isolated failures.

UNKNOWN → HOLD
