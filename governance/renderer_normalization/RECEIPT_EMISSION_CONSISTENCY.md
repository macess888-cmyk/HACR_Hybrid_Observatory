# RECEIPT EMISSION CONSISTENCY

## Purpose

This document defines consistency expectations for topology-local receipt emission across HACR Hybrid Observatory tools.

It supports:

- renderer interoperability
- reviewer reproducibility
- deterministic comparison
- replay normalization
- topology convergence

It does not support:

- governance automation
- escalation optimization
- remediation instruction
- operational routing

## Recommended Receipt Order

Receipts SHOULD preserve a stable high-level order:

1. tool
2. observer_only
3. non_authoritative
4. non_predictive
5. non_remediative
6. case_id
7. description
8. generated_at_utc
9. outputs_do_not_imply
10. nodes
11. final_boundary
12. sha256

## Required Non-Claims

Receipts SHOULD include explicit `outputs_do_not_imply` values such as:

- intervention recommendation
- governance validity
- escalation authority
- remediation instruction
- predictive certainty
- operational control

Tool-specific non-claims MAY be added.

## Hash Boundary

Receipt hashes may include generated timestamps unless future tools separate:

- content_hash
- receipt_instance_hash

If timestamps are included, hashes may change between runs.

Replay comparison should prioritize:

- input case
- scoring logic
- classification outputs
- node structure
- boundary flags
- explicit non-claims

## Emission Boundary

Receipt emission means:

- a deterministic tool produced a bounded observability artifact

Receipt emission does NOT mean:

- the condition is operationally true
- intervention is required
- escalation is valid
- governance is invalid
- remediation should occur

## Stabilization Principle

Receipt consistency supports reproducible review without creating authority.

Break survivability, not ontology.

UNKNOWN -> HOLD.