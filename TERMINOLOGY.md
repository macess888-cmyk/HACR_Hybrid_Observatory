# HACR Hybrid Observatory — Terminology

## Core posture

Observer-restricted means the observatory inspects, maps, classifies, and reports. It does not authorize execution, certify systems, or enforce runtime behavior.

Bounded inspection means each result applies only to the provided test input and controlled diagnostic condition.

Deterministic diagnostics means the same input should produce the same observable output.

## Output states

PASS means the tested condition appears bounded within the provided input.

HOLD means the input is insufficient, ambiguous, too broad, or not safely classifiable.

FAIL means the tested condition contradicts the expected boundary or freshness requirement.

STOP means the execution boundary appears compromised within the tested condition.

REVERSE means an admitted effect identity appears to drift or invert.

SHADOW means a hidden, deferred, shared, or concealed continuation surface appears reachable.

## Mapping terms

Topology means the graph of nodes, edges, queues, retries, workers, caches, replay surfaces, and downstream consumers.

Reachability means whether a path can still reach an effect-capable surface.

Condition trace means following a required condition across execution, retry, reversal, recovery, or downstream paths.

Bind freshness means whether the condition used at action time is present-state rather than inherited from a prior state.

## Lens terms

Symmetric means forward and reversal paths behave equivalently.

Asymmetric means execution, reversal, retry, or refusal paths behave unequally.

Dynamic means the topology, condition, or reachability state changes over time.

Alpha means the origin/input side of an execution path.

Omega means the final/effect side of an execution path.

Matrix means a node-to-node reachability map.

Super-matrix means a full topology reachability map across multiple surfaces. This is descriptive only, not authoritative.

## Public boundary

Observation is not authority.

Classification is not admissibility.

Mapping is not certification.

Diagnostics are not operational approval.

Reports do not authorize execution.