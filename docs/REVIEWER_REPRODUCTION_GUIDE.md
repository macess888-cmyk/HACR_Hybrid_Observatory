# HACR Hybrid Observatory
# Reviewer Reproduction Guide

Bounded Inspection / Deterministic Review / Falsification-Oriented

---

## Purpose

This guide provides a simple reviewer-facing path for reproducing observatory outputs.

The goal is reproducible inspection, not delegated trust.

---

## Reviewer Principle

The observatory should not ask reviewers to trust a conclusion.

It should allow reviewers to:

- rerun
- inspect
- compare
- challenge
- falsify
- document limitations

---

## Minimal Reviewer Path

1. Identify the controlled input
2. Run the deterministic inspection path
3. Generate diagnostic output
4. Compare receipt artifacts
5. Review PASS / HOLD / FAIL classification
6. Inspect limitations and non-claims
7. Attempt to break or falsify the result

---

## Expected Reviewer Questions

A reviewer should be able to ask:

- What input was used?
- What run path was followed?
- What diagnostic output was generated?
- What receipt chain was produced?
- What does PASS / HOLD / FAIL mean?
- What does the observatory not claim?
- What topology was not inspected?
- What would falsify the result?

---

## PASS / HOLD / FAIL Review

### PASS

The tested survivability condition was not reproduced under the controlled path.

PASS remains bounded.

PASS is not certification.

---

### HOLD

The observation is incomplete, ambiguous, unresolved, or insufficient for closure.

HOLD preserves fail-closed diagnostic behavior.

---

### FAIL

Continuation, survivability, persistence, or effect-capable residue remained observable under inspected conditions.

FAIL is diagnostic only.

---

## Falsification Path

Reviewers are encouraged to attempt:

- hidden carrier introduction
- replay path reconstruction
- retry survival
- residue reactivation
- downstream continuation
- local silence / aggregate survival mismatch
- false PASS creation
- observer dependency exposure
- semantic compression ambiguity

If a reviewer can produce effect-capable continuation after claimed collapse:

-> FAIL

If uncertainty remains:

-> HOLD

---

## Non-Authority Boundary

Reviewer reproduction does not create authority.

A reproduced diagnostic output is not:

- certification
- admissibility
- governance validity
- execution permission
- legal judgment
- moral judgment

---

## Final Reviewer Frame

Not:

“Trust this observatory.”

But:

“Inspect this path, reproduce this output, challenge this boundary, and document where it fails.”