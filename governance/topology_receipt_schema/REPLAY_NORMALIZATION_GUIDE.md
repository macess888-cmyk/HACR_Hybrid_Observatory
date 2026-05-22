# REPLAY NORMALIZATION GUIDE

## Purpose

This guide defines replay normalization expectations for topology-local HACR Hybrid Observatory tools.

It supports:

- deterministic replay
- reviewer reproducibility
- receipt comparison
- topology-local inspection consistency

It does not support:

- intervention routing
- governance automation
- escalation optimization
- remediation instruction

## Replay Expectations

A replay-safe topology tool SHOULD:

- consume bounded JSON input
- produce deterministic JSON receipt output
- include explicit non-claims
- include observer-only flags
- include UNKNOWN -> HOLD
- include a SHA256 receipt hash
- avoid network dependency
- avoid external state dependency
- avoid nondeterministic classification logic

## Timestamp Boundary

Receipts may include `generated_at_utc`.

Because timestamps change between runs, reviewers should compare:

- classification structure
- node-level scores
- case_id
- tool name
- explicit non-claims
- boundary flags

not timestamp equality alone.

## Hash Boundary

If `generated_at_utc` is included in the hash payload, the SHA256 value may change across runs.

This is acceptable if:

- node classifications remain deterministic
- scoring logic remains stable
- bounded input remains unchanged
- output structure remains comparable

Future tools MAY separate:

- content_hash
- receipt_instance_hash

to distinguish deterministic content from generated receipt instance identity.

## Normalized Comparison

Reviewer comparison SHOULD inspect:

- same input case
- same tool version or commit
- same node classification outputs
- same score calculations
- same non-claim boundaries
- same final boundary

## Non-Claims

Replay consistency does NOT imply:

- operational truth
- escalation feasibility
- interruption success
- governance validity
- remediation need
- predictive certainty

## Stabilization Principle

Replay normalization supports reviewer trust without converting observability into authority.

Break survivability, not ontology.

UNKNOWN -> HOLD.