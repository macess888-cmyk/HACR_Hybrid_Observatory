# HACR Interface Coherence — v0.8

## Current stabilization target

Reduce symbolic surplus and tighten executable coherence.

## Core review concern

The observatory should make its operative chain easier to inspect:

Input
→ lens outputs
→ pressure signals
→ graph export
→ SVG visualization

## Canonical demo chain

Controlled input:
`Inputs/watchdog_continuity_case.json`

Primary outputs:

- `Outputs/watchdog_report.json`
- `Outputs/replay_vector_report.json`
- `Outputs/refusal_propagation_report.json`
- `Outputs/authority_surface_report.json`
- `Outputs/continuation_pressure_report.json`
- `Outputs/survivability_graph_export.json`
- `Outputs/survivability_graph.svg`

## Intended interpretation

The demo does not prove governance.

It shows whether continuity survivability remains observable after refusal under controlled deterministic conditions.

## Boundary

The observatory is:

- observer-restricted
- deterministic
- reproducible
- non-authoritative
- not runtime control
- not certification
- not production monitoring

## Next hardening target

Add consistent report fields:

- status
- observer_mode
- derived_from
- non_claims