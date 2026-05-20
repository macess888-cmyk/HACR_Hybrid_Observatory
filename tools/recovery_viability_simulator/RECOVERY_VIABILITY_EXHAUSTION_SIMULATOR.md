# Recovery Viability Exhaustion Simulator

## Purpose

This simulator pressures whether recovery remains materially reachable before consequence hardens.

## Core Reduction

Recovery visibility is not recovery viability.

## Runtime Inputs

- detection delay
- explanation delay
- escalation delay
- reviewer traversal burden
- replay locality fragmentation
- synchronization pressure
- interruption execution delay
- recovery routing delay
- consequence hardening speed

## Runtime Model

effective_recovery_time =
detection
+ explanation
+ escalation
+ traversal
+ interruption
+ recovery
+ fragmentation_penalty
+ synchronization_penalty

## Runtime Evaluation

IF:

effective_recovery_time
>
consequence_hardening_window

THEN:

RECOVERY_EXHAUSTED

## Output Semantics

### RECOVERABLE

Recovery remains materially reachable.

### PARTIAL_RECOVERY

Bounded recovery survives locally.

### HOLD

Recovery viability cannot be verified.

### RECOVERY_EXHAUSTED

Consequence hardens before recovery remains materially reachable.

## Strongest Runtime Pressure

Systems may preserve recovery visibility after recovery viability collapses.

## Boundary

Observer-only and runtime-local.