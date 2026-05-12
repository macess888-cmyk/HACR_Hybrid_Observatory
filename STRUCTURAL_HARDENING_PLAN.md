# HACR Structural Hardening Plan

## Purpose

This plan translates external structural pressure-testing into bounded repository hardening.

The goal is not to turn HACR into a production orchestration system.

The goal is to improve:

- repository coherence
- interface clarity
- architecture-to-code traceability
- reviewer reproducibility
- deterministic inspection discipline

while preserving the observer-restricted boundary.

---

# Adopted Hardening Principles

## 1. Narrative must not exceed structure

Architecture claims should map to visible repository artifacts.

If a concept is documented, it should be traceable to:

- input case
- module
- output report
- schema field
- test or reproducibility artifact

---

## 2. Architecture-to-code mapping

Create a mapping between:

- architectural concept
- concrete file
- generated output
- review artifact

This prevents symbolic architecture from floating beyond implementation.

---

## 3. Dependency graph visibility

Generate a source dependency graph and compare it with the claimed architecture map.

Purpose:

- reveal coupling
- expose structural debt
- detect interface drift
- support reviewer inspection

---

## 4. Interface discipline

Move toward clearer input/output contracts.

Near-term target:

- every lens consumes declared input
- every lens produces canonical output
- every report follows v0.8 schema
- every output declares `derived_from`

---

## 5. Validation and reproducibility

Continue strengthening:

- schema validation
- normalization
- reproducibility hashes
- deterministic demo runs
- canonical minimal cases

---

# Deferred / Not Adopted

The following are not adopted as current HACR scope:

- production orchestration core
- runtime monitoring dashboards
- execution routing
- governance authority layer
- operational control system
- certification framework

These would change the category of the repository.

---

# Current Boundary

HACR remains:

- observer-restricted
- deterministic
- reproducible
- non-authoritative
- non-consumable by execution

---

# Near-Term Execution Order

1. Create architecture-to-code mapping.
2. Generate dependency graph.
3. Add dependency/cycle visibility.
4. Add `derived_from` normalization.
5. Improve interface documentation.
6. Add minimal tests for core lenses.
7. Improve reviewer reproducibility flow.

---

# Core Stabilization Rule

Constraints > narrative  
Reproducibility > assertion  
Traceability > symbolism  
Observer boundary > architecture expansion