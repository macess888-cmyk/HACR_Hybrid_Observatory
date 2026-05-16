# HACR Hybrid Observatory
# Aggregate Containment Failures

Local Silence / Fragmented Continuation / Topology-Wide Closure

---

## Purpose

This document identifies failures where local interruption, local silence, or visible calm is incorrectly treated as aggregate containment.

---

## Core Principle

Local silence is not aggregate containment.

A consequence may disappear locally while surviving elsewhere in the topology.

---

## Aggregate Failure Pattern

A system may appear contained when:

- the local process stops
- logs show refusal
- dashboards quiet down
- recovery appears complete
- one node reports closure
- one operator confirms halt

while continuation survives through:

- retries
- queues
- replay
- downstream consumers
- cached state
- stale authority
- operational memory
- hidden carriers
- fragmented workflows

---

## Fragmented Continuation

Fragmented continuation remains continuation.

A consequence may survive in pieces through:

- partial lineage
- distributed memory
- reassembled workflow
- downstream residue
- human reconstruction
- event replay
- fallback process
- manual continuation

If fragments can reconstruct effect-capable continuation:

-> FAIL

If unclear:

-> HOLD

---

## False Closure Signals

Unsafe closure may be inferred from:

- local halt
- visual calm
- successful retry cancellation at one surface
- partial downstream notification
- incomplete queue inspection
- silence from one service
- report completion
- dashboard green state

These are not aggregate closure.

---

## Aggregate Closure Requirements

Aggregate closure requires sufficient visibility into:

- local process state
- downstream reachability
- queued work
- replay eligibility
- retry policy
- cached authority
- stale state
- residue inertness
- human continuation paths
- recovery path constraints
- distributed topology

---

## HOLD Conditions

Route to HOLD if:

- topology coverage is incomplete
- downstream consumers are unknown
- replay state is unresolved
- residue inertness is unproven
- hidden carriers may exist
- fragmented continuation may reconstruct effect
- interruption only occurred locally

---

## Diagnostic Boundary

The observatory may expose aggregate containment concerns.

It may not certify aggregate closure.

---

## Final Constraint

Visible interruption is not operational interruption.

Fragmented interruption cannot guarantee aggregate containment.

Unknown consequence carriers are operationally equivalent to survivable consequence.