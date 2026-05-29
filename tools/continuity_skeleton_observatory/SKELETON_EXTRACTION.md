# Skeleton Extraction

## Purpose

Extract persistent structural visibility from historical observation windows.

A skeleton is not:

- a route
- a prediction
- a recommendation
- a causality claim
- governance authority
- execution authorization

A skeleton is:

- repeated visibility
- persistent visibility
- structural visibility surviving reduction

## Extraction Flow

Epoch Visibility
→ Region Persistence
→ Connectivity Persistence
→ Structural Persistence
→ Skeleton

## Region Classification

visible_epochs / total_epochs

- >= 0.90 → PRIMARY_BACKBONE
- >= 0.60 → SECONDARY_BACKBONE
- >= 0.30 → PERSISTENCE_BRANCH
- otherwise → STRUCTURAL_REMNANT

## Corridor Classification

shared_visible_epochs / total_epochs

- >= 0.90 → PRIMARY_SPINE
- >= 0.60 → SECONDARY_SPINE
- >= 0.30 → PERSISTENCE_BRANCH
- otherwise → STRUCTURAL_REMNANT

## Visibility Invariant

A visibility invariant is visible in every observation epoch.

It may apply to:

- regions
- corridors

Visibility invariants are not proof of causality.
They only represent complete historical visibility across bounded observation windows.