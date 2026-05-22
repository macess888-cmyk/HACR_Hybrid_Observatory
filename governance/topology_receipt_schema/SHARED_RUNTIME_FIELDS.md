
---

## 4. `governance\topology_receipt_schema\SHARED_RUNTIME_FIELDS.md`

```md
# SHARED RUNTIME FIELDS

## Purpose

This document defines common runtime-local fields used across deterministic topology observability tools.

The fields exist for consistency only.

They do not imply operational authority, intervention capability, or governance validity.

## Shared Receipt Fields

| Field | Meaning |
|---|---|
| tool | Name of the deterministic observability tool |
| case_id | Local input case identifier |
| description | Bounded case description |
| generated_at_utc | Receipt generation timestamp |
| observer_only | Confirms non-executive inspection posture |
| non_authoritative | Confirms no authority inheritance |
| non_predictive | Confirms no prediction claim |
| non_remediative | Confirms no remediation instruction |
| outputs_do_not_imply | Explicit non-claims |
| nodes | Local inspected topology objects |
| final_boundary | Default unresolved boundary |
| sha256 | Deterministic receipt integrity hash |

## Shared Node Fields

Topology tools MAY use local scoring fields such as:

- classification
- score
- pressure_score
- hardening_score
- decay_score
- traversal_pressure_score
- gravity_score

Scores are local to the tool and supplied input assumptions.

Scores do NOT generalize beyond the bounded case.

## Shared Classification Semantics

Classifications are descriptive labels only.

They do not imply:

- escalation requirement
- intervention necessity
- interruption impossibility
- governance invalidity
- operational certainty

## Field Containment

Runtime fields must remain:

- local
- bounded
- deterministic
- observer-only
- non-authoritative
- non-remediative

UNKNOWN -> HOLD.