# Expansion Decision Rule

## Purpose

This rule controls whether a proposed observatory layer may proceed, remain held, or stop.

Expansion is not automatic.

## Core Rule

A new layer may proceed only if it improves observer-local recoverability inspection without introducing authority, prediction, certification, intervention, human-control, or operational-command semantics.

## Classifications

### PROCEED

Use PROCEED only when the proposed layer:

- improves observer-local inspection
- reduces ambiguity
- strengthens reproducibility
- preserves deterministic receipts
- remains non-authoritative
- avoids prediction/control/certification semantics
- preserves UNKNOWN -> HOLD

### HOLD

Use HOLD when the proposed layer is potentially useful but carries unclear authority gravity.

Examples:

- human behavior observability
- medical or health-system consequence surfaces
- policy-adjacent interpretation surfaces
- intervention-adjacent tooling

### STOP

Use STOP when the proposed layer would introduce:

- control authority
- intervention authority
- prediction authority
- certification authority
- human behavior scoring
- persuasion optimization
- clinical decision authority
- operational command
- governance execution
- consequence legitimacy

## Bridge Rule

A bridge may clarify topology, but it does not authorize expansion.

## Operating Rule

UNKNOWN -> HOLD.

Break survivability, not ontology.