# Hybrid Bridge Finder

Observer-only diagnostic tool for identifying missing or useful bridge layers between existing observatory families.

## Purpose

The Hybrid Bridge Finder inspects whether a proposed bridge layer is necessary, bounded, observer-only, and containment-preserving.

It does not authorize expansion.

## Core Reduction

Bridge discovery is diagnostic, not expansion authority.

## Inputs

The tool accepts bounded JSON indicators such as:

- source layer
- target layer
- proposed bridge
- topology gap severity
- reproducibility benefit
- ambiguity reduction
- observer-only fit
- authority drift risk
- human behavior risk
- certification risk
- prediction risk
- governance risk

## Outputs

Possible classifications:

- PASS: bridge appears bounded and useful under supplied evidence
- HOLD: insufficient present-state proof
- FAIL: bridge introduces authority drift or containment risk
- SHADOW: hidden dependency gap detected
- REVERSE: proposed bridge may be unnecessary; existing layer may already cover it
- STOP: bridge crosses prohibited boundary

## Non-Claims

This tool is not:

- expansion authority
- governance authority
- domain certification
- operational command
- intervention authorization
- prediction
- truth determination
- human behavior inspection authority

UNKNOWN -> HOLD.