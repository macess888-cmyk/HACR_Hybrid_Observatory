# FIE Instrumentation Boundary

FIE is treated here as a bounded instrumentation pattern.

It is not a governance layer, orchestration system, execution authority, or proof engine.

## Allowed Role

FIE-style instrumentation may support:

- manifests
- ledgers
- gates
- verification records
- append-only registries
- typed observational claims
- bounded reproducibility checks

## Claim Tags

- FORMAL
- DERIVED
- OBSERVED
- HEURISTIC

## Verdict Tags

- PASS_OBSERVED
- INCONCLUSIVE
- FAIL_INSTRUMENT
- COUNTEREXAMPLE_FOUND

## Boundary Rule

Instrument outputs remain evidence artifacts.

Evidence artifacts do not authorize execution.

## Default

If a claim cannot be classified within declared scope:

HOLD.