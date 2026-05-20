# React Error Recovery Auditor

## Purpose

This tooling converts React runtime failure signals into a bounded repair path.

Initial focus:

- React minified error #185
- maximum update depth exceeded
- render/effect/state update loops
- unstable dependency loops
- recursive state-triggered rerenders

## Core Reduction

Visual failure should become a deterministic repair path.

## Output States

- PROCEED
- HOLD
- FIX

## Boundary

Observer-only.

Not framework authority.
Not certification.
Not deployment approval.

UNKNOWN -> HOLD.