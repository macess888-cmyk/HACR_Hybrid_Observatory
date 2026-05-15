# Reproducibility

## Purpose

This repository prioritizes reproducible observer-side inspection.

Reproducibility means that declared inputs, configurations, artifacts, and outputs can be independently reviewed, regenerated where applicable, and checked against declared integrity surfaces.

## Scope

Reproducibility applies to:

- deterministic receipts
- manifests
- ledgers
- topology maps
- provenance records
- inspection outputs
- verification gates

## Non-Scope

Reproducibility does not imply:

- correctness
- certification
- authority
- execution permission
- governance validity
- downstream admissibility

## Expected Review Path

1. Inspect declared input artifacts.
2. Confirm schema and version consistency.
3. Recompute available hashes.
4. Compare generated outputs against stored receipts.
5. Review HOLD / FAIL / PASS classifications within declared caps.
6. Treat unresolved provenance, authority, recovery, or containment as HOLD.

## Failure Semantics

- Missing artifact: HOLD
- Schema mismatch: FAIL
- Hash mismatch: FAIL
- Unclear provenance: HOLD
- Unclear authority: HOLD
- Unclear containment: HOLD
- Unclear recovery path: HOLD

## Default

No reproducible artifact may be interpreted as operational authority.

Observation remains observation.