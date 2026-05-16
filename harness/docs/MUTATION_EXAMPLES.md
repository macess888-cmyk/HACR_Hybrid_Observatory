# HACR Minimal Replay Harness
# Mutation Examples

Reviewer Mutation / False PASS Detection / HOLD Preservation

---

## Purpose

This document gives reviewers simple mutation ideas for testing whether the harness incorrectly produces PASS under unresolved runtime conditions.

---

## Mutation Principle

A mutation is useful if it pressures whether the harness preserves:

- HOLD under uncertainty
- FAIL under survivable continuation
- non-authority boundaries
- replayable failure reachability

---

## Mutation 1: Incomplete Topology

Change:

```json
"topology_visibility": "sufficient"