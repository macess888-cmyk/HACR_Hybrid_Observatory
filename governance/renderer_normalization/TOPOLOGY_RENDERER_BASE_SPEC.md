# TOPOLOGY RENDERER BASE SPEC

## Purpose

This specification defines a shared lifecycle for deterministic topology-local renderers in the HACR Hybrid Observatory.

It exists to reduce renderer drift and improve reviewer reproducibility.

It does not create:

- governance authority
- remediation capability
- escalation validity
- operational control
- predictive certainty

## Renderer Lifecycle

A topology renderer SHOULD follow this lifecycle:

1. Load bounded JSON input.
2. Parse local runtime fields.
3. Compute local deterministic score.
4. Classify local topology node.
5. Emit bounded receipt.
6. Include explicit non-claims.
7. Include observer-only boundary flags.
8. Include UNKNOWN -> HOLD.
9. Include SHA256 receipt hash.

## Required Renderer Properties

A topology renderer SHOULD remain:

- deterministic
- observer-only
- runtime-local
- replay-safe
- non-authoritative
- non-predictive
- non-remediative

## Required Receipt Boundary Flags

Receipts SHOULD include:

```json
{
  "observer_only": true,
  "non_authoritative": true,
  "non_predictive": true,
  "non_remediative": true
}