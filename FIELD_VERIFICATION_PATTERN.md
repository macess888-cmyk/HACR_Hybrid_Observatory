# Field Verification Pattern

## Purpose

This note captures an observer-side verification pattern discovered during field sealing of an execution-bound artifact.

It does not make the Observatory an execution gate.
It does not authorize execution.
It does not certify correctness.
It only records reproducible verification hygiene.

## Pattern

A field-shareable artifact should be treated as untrusted unless it can be independently verified after transfer.

Minimum useful structure:

1. Sealed artifact
2. Lock manifest
3. Verifier script
4. Replayable PASS / FAIL result
5. No silent success path

## Boundary Rule

A verifier must fail closed.

If verification cannot parse the lock,
cannot find files,
cannot reproduce hashes,
or reports any missing dependency,
the result is FAIL.

A verifier must not print PASS after an internal failure.

## Replay Lesson

Visible success is not containment.

During replay, a package may appear sealed while:

- the lock file is malformed
- encoding changes break verification
- required files are missing
- self-referential hashes invalidate the manifest
- scripts print PASS despite internal failure

These are verification-surface failures, not user errors.

## Self-Reference Rule

A lock file should not hash itself.

If the manifest includes its own hash, the artifact becomes recursively unstable because the manifest changes when the manifest changes.

The stable pattern is:

- hash the protected files
- exclude the lock file from its own protected set
- verify the lock externally or as part of a sealed outer package

## Observatory Relevance

This pattern is useful to the HACR Hybrid Observatory as an observer-side reproducibility lesson.

It supports:

- deterministic replay
- artifact integrity checks
- false-PASS detection
- dependency-local verification
- non-authoritative inspection
- reproducible reviewer challengeability

It does not create execution authority.

## Non-Claims

This pattern does not claim:

- governance validity
- execution admissibility
- legal compliance
- deployment safety
- certification
- authorization
- operational correctness

It only improves the visibility of whether a shared artifact still matches what was sealed.

## Reduction

Verification systems themselves require replayable falsification pressure, or they can silently become trust surfaces.