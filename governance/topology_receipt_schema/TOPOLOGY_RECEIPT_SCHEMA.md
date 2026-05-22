# TOPOLOGY RECEIPT SCHEMA

## Purpose

This schema defines shared receipt expectations for deterministic topology-local observability tools in the HACR Hybrid Observatory.

It exists to support:

- replay consistency
- renderer interoperability
- bounded runtime localization
- reviewer reproducibility
- deterministic receipt comparison

It does not create authority, remediation capability, escalation validity, or governance legitimacy.

## Required Receipt Fields

Each topology receipt SHOULD include:

- tool
- case_id
- description
- generated_at_utc
- observer_only
- non_authoritative
- non_predictive
- non_remediative
- nodes
- outputs_do_not_imply
- final_boundary
- sha256

## Required Boundary Flags

Receipts SHOULD explicitly preserve:

```json
{
  "observer_only": true,
  "non_authoritative": true,
  "non_predictive": true,
  "non_remediative": true
}