# Storage Consistency Failure Modes
Observer-Restricted Provenance Divergence Taxonomy

## Purpose

This document catalogs bounded storage and provenance divergence patterns observed during recursive audit workflows.

The goal is not prevention authority.

The goal is reproducible observer-side visibility into survivable inconsistency mechanisms.

---

# Core Principle

A storage layer may remain operationally coherent while hidden provenance divergence survives locally.

Global consistency signals alone are insufficient.

---

# Failure Mode Categories

## 1. Duplicate Provenance Occupancy

Multiple stored entries occupy effectively identical operational corridors.

Potential causes:

- replay overlap
- insufficient deduplication radius
- normalization inconsistency
- stale replay survivability
- reconstruction drift

Symptoms:

- located state > counted state
- recursive mismatch localization
- bracket overlap anomalies

---

## 2. Boundary-Crossing Bracket Drift

Bracket generation exceeds requested audit corridor.

Example pattern:

```text
requested:
204.174 → 204.187

generated:
204.165 → 204.214