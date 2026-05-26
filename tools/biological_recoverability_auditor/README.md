# Biological Recoverability Auditor

Observer-only diagnostic tool for inspecting divergence between biological continuity and regeneration viability.

## Purpose

The tool inspects whether organisms, populations, or biological systems can remain visibly persistent while reproductive, habitat, trophic, or regeneration corridors degrade underneath that persistence.

## Core Reduction

Life persistence is not proof of preserved biological recoverability.

## Inputs

The tool accepts a bounded JSON case containing observer-local indicators such as:

- population continuity
- reproductive viability
- habitat viability
- resource continuity
- trophic dependency
- mutation pressure
- temperature stress
- oxygen stress
- regeneration corridor evidence

## Outputs

Possible classifications:

- PASS: continuity and recoverability remain coupled under supplied evidence
- HOLD: insufficient present-state proof
- FAIL: continuity persists while recoverability is degraded
- SHADOW: hidden degradation pressure detected beneath continuity
- REVERSE: apparent discontinuity may not imply loss of recoverability under supplied evidence

## Non-Claims

This tool is not:

- biological certification
- ecological certification
- conservation authority
- species-risk classification
- intervention authorization
- prediction
- environmental management guidance

UNKNOWN -> HOLD.