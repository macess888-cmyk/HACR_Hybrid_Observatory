# Material Consequence Observatory — Audit Survivor Analysis

Status: Evidence Review v0.1

Mode: Observer-only inspection

Control posture:

UNKNOWN → HOLD

---

# Purpose

This document aggregates results from completed historical audits.

The objective is to identify:

* recurring primitives
* recurring compounds
* recurring triggers
* recurring transition structures

that survive cross-domain pressure.

This is not a theory document.

This is an evidence document.

---

# Completed Audit Set

```text
Challenger

Therac-25

Boeing 737 MAX

Chernobyl

2008 Financial Crisis

Deepwater Horizon
```

Domains represented:

```text
Aerospace

Medical Systems

Commercial Aviation

Nuclear Infrastructure

Global Finance

Industrial Infrastructure
```

---

# Primitive Survivor Analysis

## FP-C Coupling Failure

Observed:

```text
Challenger
✓

Therac-25
✓

737 MAX
✓

Chernobyl
✓

2008 Financial Crisis
✓

Deepwater Horizon
✓
```

Score:

```text
6 / 6
```

Common Pattern:

```text
Representation
≠
Reality Condition
```

Assessment:

```text
STRONGEST SURVIVING PRIMITIVE
```

---

## FP-V Visibility Failure

Observed:

```text
Challenger
✓

Therac-25
✓

737 MAX
✓

Chernobyl
✓

2008 Financial Crisis
✓

Deepwater Horizon
✓
```

Score:

```text
6 / 6
```

Assessment:

```text
VERY STRONG SURVIVOR
```

---

## FP-B Boundary Failure

Observed:

```text
Challenger
✓

Therac-25
✓

737 MAX
✓

Chernobyl
✓

2008 Financial Crisis
✓

Deepwater Horizon
✓
```

Score:

```text
6 / 6
```

Assessment:

```text
VERY STRONG SURVIVOR
```

---

## FP-P Preservation Failure

Observed:

```text
Challenger
✓

Therac-25
?

737 MAX
?

Chernobyl
✓

2008 Financial Crisis
✓

Deepwater Horizon
✓
```

Score:

```text
4 / 6
```

Assessment:

```text
STRONG SURVIVOR
```

---

# Trigger Survivor Analysis

## Assumption Exposure

Observed:

```text
Challenger
✓

Therac-25
✓

737 MAX
✓

Chernobyl
✓

2008 Financial Crisis
✓

Deepwater Horizon
✓
```

Score:

```text
6 / 6
```

Assessment:

```text
STRONGEST SURVIVING TRIGGER
```

---

## Capacity Mismatch

Observed:

```text
Challenger
?

Therac-25
?

737 MAX
?

Chernobyl
?

2008 Financial Crisis
Partial

Deepwater Horizon
Partial
```

Score:

```text
Weak
```

Assessment:

```text
NOT CURRENTLY PRIMARY
```

---

# Compound Survivor Analysis

## FC-01 Hidden Divergence

Observed:

```text
Therac-25
✓

737 MAX
✓

2008 Financial Crisis
✓
```

Score:

```text
3 / 6
```

Assessment:

```text
MODERATE SURVIVOR
```

---

## FC-02 Authority Drift

Observed:

```text
737 MAX
✓

Chernobyl
✓

Deepwater Horizon
✓
```

Score:

```text
3 / 6
```

Assessment:

```text
MODERATE SURVIVOR
```

---

## FC-03 Latent Infrastructure Failure

Observed:

```text
Challenger
✓

Chernobyl
✓

2008 Financial Crisis
✓

Deepwater Horizon
✓
```

Score:

```text
4 / 6
```

Assessment:

```text
STRONGEST COMPOUND SURVIVOR
```

---

# Compound Interaction Analysis

Observed:

```text
Chernobyl
FC-03 + FC-02

Deepwater Horizon
FC-03 + FC-02
```

Assessment:

```text
COMPOUND INTERACTION
OBSERVED
```

Evidence remains limited.

Further pressure required.

---

# Strongest Cross-Domain Pattern

Observed repeatedly:

```text
Support degrades.

Function persists.

Representation remains stable.

Reality coupling weakens.

Assumptions persist.

Stress accumulates.

Assumptions are exposed.

Consequence appears late.
```

Assessment:

```text
STRONGEST SURVIVING TRANSITION STRUCTURE
```

---

# Most Important Open Question

Current highest-value falsification target:

```text
Can consequence emerge
without FP-C Coupling Failure?
```

Current evidence:

```text
Not yet observed.
```

---

# Current Survivor Ranking

```text
FP-C Coupling Failure        6/6

FP-V Visibility Failure      6/6

FP-B Boundary Failure        6/6

Assumption Exposure          6/6

FP-P Preservation Failure    4/6

FC-03 Latent Infrastructure  4/6

FC-01 Hidden Divergence      3/6

FC-02 Authority Drift        3/6

Capacity Mismatch            Weak
```

---

# Repository Impact

Current evidence suggests:

```text
The strongest surviving reduction is:

Representation
≠
Reality Condition
```

This appears across every completed audit.

No completed audit has yet localized a major consequence path without some form of coupling degradation.

---

# Current Status

```text
Architecture                 STABLE

Historical Audits            6 COMPLETE

Strongest Primitive          FP-C

Strongest Trigger            Assumption Exposure

Strongest Compound           FC-03

Most Important Open Question:

Can consequence occur
without coupling failure?

UNKNOWN → HOLD
```
