# Invariant Extraction

## Purpose

Extract structures surviving all observation windows.

## Visibility Invariant

visible_epochs == total_epochs

Examples:

Documentation
Tooling

## Connectivity Invariant

corridor_visible_epochs == total_epochs

Examples:

Documentation ↔ Tooling

## Backbone Invariant

PRIMARY_BACKBONE
AND
visible_epochs == total_epochs

## Junction Invariant

Junction remains visible after skeleton reduction.

## Persistence Invariant

Remains visible after all reduction passes.

## Observer Boundary

Invariants are not:

- predictions
- recommendations
- routes
- authority
- governance

They are bounded historical visibility artifacts only.