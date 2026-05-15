# Translation Integrity Layer (TIL)

## Purpose

The Translation Integrity Layer (TIL) inspects whether semantic translation changes operational meaning across observer-side artifacts, interfaces, or documentation layers.

The layer remains:

- observer-only
- diagnostic
- deterministic
- bounded
- non-authoritative
- non-consumable by execution

It does not:

- authorize execution
- validate correctness
- certify semantic equivalence
- resolve interpretation conflicts
- replace bind-local proof

---

## Core Question

Did translation preserve the operational boundary meaning?

---

## Boundary Principle

Translation may improve readability.

Translation may not introduce:

- authority inheritance
- execution permission
- governance implication
- operational dependency
- routing legitimacy
- admissibility inference
- propagation authorization

If translation changes operational meaning:

→ HOLD

---

## Diagnostic States

### PRESERVED

Translation preserved the declared boundary meaning.

No authority, execution, or dependency shift observed.

---

### DRIFT_DETECTED

Translation changed meaning, scope, or operational interpretation.

No execution implication may be inferred.

---

### AUTHORITY_INDUCING

Translation introduced language that may imply authority, validation, governance, certification, or execution legitimacy.

Default classification:

→ HOLD

---

### HOLD

Semantic equivalence, provenance, or operational interpretation remains unclear.

No interpretation escalation permitted.

---

## Classification Inputs

The TIL may inspect:

- source text
- translated text
- terminology substitutions
- removed qualifiers
- added authority language
- scope expansion
- dependency-language drift
- governance-language drift
- execution-language drift
- recovery-language drift

These inputs remain diagnostic only.

---

## Classification Rule

If translation preserves operational boundary meaning:

→ PRESERVED

If translation changes scope, dependency interpretation, or operational meaning:

→ DRIFT_DETECTED

If translation introduces authority, certification, governance, legitimacy, or execution permission language:

→ AUTHORITY_INDUCING

If equivalence cannot be determined:

→ HOLD

---

## Non-Claims

The TIL does not determine:

- correctness
- legitimacy
- admissibility
- compliance
- execution safety
- semantic truth

It only inspects whether translation appears to preserve observer-side boundary meaning.

---

## Observatory Constraint

Translated artifacts must remain:

- observer-restricted
- bounded
- reproducible
- non-authoritative
- non-consumable by execution

Translation must not become an authority surface.