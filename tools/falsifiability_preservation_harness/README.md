# Falsifiability Preservation Harness

## Purpose

The Falsifiability Preservation Harness inspects whether observability artifacts remain locally testable, bounded, disconfirmable, and independently compressible.

It localizes when a claim becomes too broad, elastic, universal, or self-sealing to remain useful as an observer-local artifact.

## What It Checks

- universal explanation language
- non-disconfirmable framing
- self-sealing logic
- evidence-free certainty
- excessive interpretive elasticity
- claim expansion beyond local test conditions
- compression loss

## Output Semantics

PASS
- bounded and locally testable

COOL
- falsifiability pressure detected

HOLD
- unresolved testability risk

STOP
- strong non-disconfirmable or self-sealing drift detected

REWRITE
- bounded reformulation required

## Example Usage

```bash
python falsifiability_preservation_harness.py sample_input.txt