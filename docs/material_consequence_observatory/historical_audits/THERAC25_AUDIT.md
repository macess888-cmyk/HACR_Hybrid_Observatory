# Historical Audit — Therac-25 (1985–1987)

Status: Historical Audit v0.1

Mode: Observer-only inspection

Control posture:

UNKNOWN → HOLD

---

# Purpose

This audit evaluates whether the Material Consequence Observatory can localize the Therac-25 consequence path without requiring architectural modification.

The objective is not software fault analysis.

The objective is observatory pressure.

Question:

Can the observatory localize the consequence path?

---

# Known Consequence

Period:

```text
1985–1987
```

Outcome:

```text
Multiple patients received massive radiation overdoses.

Severe injury occurred.

Multiple deaths were attributed to overdoses.
```

Consequence:

```text
Catastrophic medical treatment failure.
```

---

# Formation Preconditions

Observed formation conditions:

```text
Computer-controlled radiation therapy system

Clinical deployment

Operational treatment workflow

Trained operators

Software-mediated control

Regulatory approval
```

Assessment:

```text
Formation Preconditions = PRESENT
```

---

# Condition Before Consequence

Operational appearance:

```text
Machine functional

Clinical workflow functional

Operators trained

System considered safe

Treatments routinely delivered
```

Visible operation persisted.

Assessment:

```text
Condition = APPARENTLY STABLE
```

---

# Primitive Analysis

## FP-C Coupling Failure

Question:

Did representation diverge from reality condition?

Observed:

```text
Displayed machine state appeared valid.

Actual treatment state could differ from operator understanding.

Machine behavior did not always correspond to visible representation.
```

Assessment:

```text
FP-C PRESENT

VERY STRONG MATCH
```

---

## FP-V Visibility Failure

Question:

Were relevant conditions fully visible?

Observed:

```text
Internal execution state was not directly observable.

Operators relied on displayed information.

Failure pathways were difficult to observe.
```

Assessment:

```text
FP-V PRESENT

VERY STRONG MATCH
```

---

## FP-B Boundary Failure

Question:

Did separation between representation, execution, and consequence weaken?

Observed:

```text
Software state

↓

Machine execution

↓

Physical radiation delivery

↓

Patient consequence
```

Boundary stress appears significant.

Assessment:

```text
FP-B PRESENT

STRONG MATCH
```

---

## FP-P Preservation Failure

Question:

Did support structures degrade before consequence?

Observed:

```text
Less obvious.

Operational continuity remained visible.

Preservation degradation is not clearly primary.
```

Assessment:

```text
FP-P POSSIBLE

WEAK MATCH
```

---

# Compound Analysis

## FC-01 Hidden Divergence

Candidate composition:

```text
FP-C
+
FP-V
```

Observed pattern:

```text
Reality diverges.

Visibility weakens.

System appears operational.

Consequence emerges later.
```

Assessment:

```text
VERY STRONG MATCH
```

---

## FC-02 Authority Drift

Candidate composition:

```text
FP-B
+
FP-C
```

Observed pattern:

```text
Execution authority remains active.

Reality condition diverges.

Physical action proceeds.
```

Assessment:

```text
POSSIBLE MATCH
```

---

# Trigger Analysis

## Capacity Mismatch

Evidence:

```text
Weak
```

No significant overload condition appears central.

Assessment:

```text
NOT PRIMARY
```

---

## Assumption Exposure

Evidence:

```text
Strong
```

Observed:

```text
Assumptions regarding software correctness
became invalid under operational conditions.
```

Assessment:

```text
PRIMARY TRIGGER CANDIDATE
```

---

# Candidate Transition Path

Current localization:

```text
Formation Preconditions
↓
Condition
↓
FP-C
+
FP-V
+
FP-B
↓
FC-01 Hidden Divergence
↓
Assumption Exposure
↓
Consequence
```

---

# Strongest Survivor

Most consistent pattern:

```text
Representation appeared valid.

Reality diverged.

Visibility remained limited.

Execution continued.

Consequence emerged physically.
```

This aligns closely with current observatory architecture.

---

# What The Observatory Explains

The observatory appears capable of localizing:

```text
Representation drift

Visibility limitations

Execution under degraded coupling

Software-mediated consequence

Assumption exposure

Delayed recognition of divergence
```

---

# What The Observatory Does Not Explain

The observatory does not currently explain:

```text
Specific software defects

Race conditions

Implementation-level code behavior

Engineering root-cause reconstruction

Predictive prevention
```

These remain outside repository scope.

---

# Pressure Assessment

Question:

Can the consequence path be localized through:

```text
Primitive
↓
Compound
↓
Trigger
↓
Consequence
```

Assessment:

```text
YES
```

No architectural redesign required.

---

# Primitive Pressure Result

Therac-25 provides significant pressure against:

```text
FP-C Coupling Failure
```

Observed pattern:

```text
Representation
≠
Reality Condition
```

appears central to the consequence path.

Assessment:

```text
FP-C survives additional pressure.
```

---

# Audit Result

```text
Architecture Pressure = PASS

Primitive Registry = PASS

Compound Registry = PASS

Trigger Taxonomy = PASS

Cross-Domain Validation = PASS
```

---

# Repository Impact

Result:

```text
No architectural modification required.
```

The audit strengthens confidence in:

```text
Coupling degradation

Visibility degradation

Hidden divergence compounds

Assumption exposure triggers
```

---

# Current Status

```text
Historical Audit = COMPLETE

Architecture = STABLE

Observatory Localization = SUCCESSFUL

UNKNOWN → HOLD
```
