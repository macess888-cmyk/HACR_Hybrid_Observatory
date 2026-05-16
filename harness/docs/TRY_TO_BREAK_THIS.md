# HACR Minimal Replay Harness
# Try To Break This

Reviewer Challenge / False PASS Detection / Runtime Falsification

---

## Purpose

This document invites reviewers to challenge the minimal replay harness.

The harness is stronger when reviewers can attempt to break it.

---

## Core Challenge

Try to produce a false PASS.

A false PASS occurs when the harness reports PASS while unresolved continuation, topology uncertainty, hidden carriers, replay ambiguity, stale state, or operational memory still exists.

---

## Break Attempts

Reviewers should attempt to create cases where:

- topology is incomplete but PASS is returned
- hidden carriers survive but PASS is returned
- replay is ambiguous but PASS is returned
- stale state survives but PASS is returned
- operational memory survives but PASS is returned
- local interruption succeeds but aggregate continuation survives
- visible calm exists while hidden continuation remains
- continuation survives through fragmented surfaces
- uncertainty is compressed into confidence

---

## Expected Safe Behavior

If topology is incomplete:

-> HOLD

If continuation survives:

-> FAIL

If hidden carriers are unknown:

-> HOLD

If replay is ambiguous:

-> HOLD

If stale state or operational memory survives:

-> FAIL

---

## Unsafe Harness Behavior

The harness should be considered weakened if:

- PASS appears under incomplete visibility
- HOLD is suppressed by confidence
- hidden continuation is ignored
- replay ambiguity is treated as closure
- local silence is treated as aggregate containment
- semantic clarity replaces runtime falsification

---

## Final Rule

A harness that cannot independently fail becomes theater.

Replayable failure must remain reachable.