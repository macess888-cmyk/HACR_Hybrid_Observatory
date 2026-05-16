# HACR Minimal Replay Harness
# Case Index

---

## PASS Cases

- PASS_MINIMAL.json  
  Continuation collapses under sufficient visibility.

---

## HOLD Cases

- HOLD_TOPOLOGY_UNKNOWN.json  
  Incomplete topology preserves uncertainty.

- HOLD_REPLAY_AMBIGUITY.json  
  Replay ambiguity preserves HOLD.

- FALSE_PASS_INCOMPLETE_TOPOLOGY.json  
  Prevents false PASS under incomplete topology visibility.

---

## FAIL Cases

- FAIL_CONTINUATION_SURVIVES.json  
  Continuation survives interruption.

- FAIL_HIDDEN_CONTINUATION.json  
  Hidden continuation remains effect-capable.

- FAIL_OPERATIONAL_MEMORY_SURVIVES.json  
  Stale operational memory preserves continuation.

- FAIL_OBSERVABLE_CALM_HIDDEN_CONTINUATION.json  
  Visible calm hides survivable continuation.

- FAIL_FRAGMENTED_INTERRUPTION.json  
  Local interruption misses aggregate continuation.

---

## Harness Boundary

These cases are diagnostic only.

They do not authorize execution.

They do not certify safety.

They do not prove admissibility.

They support replayable inspection and reviewer challenge.