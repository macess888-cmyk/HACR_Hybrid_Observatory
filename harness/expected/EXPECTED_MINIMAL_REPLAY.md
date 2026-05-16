# HACR Minimal Replay Harness
# Expected Replay Outcomes

---

## Purpose

This file defines the expected outcomes for the minimal replay harness.

The purpose is reviewer reproducibility and falsification support.

---

## Expected Case Outcomes

| Case | Expected State | Purpose |
|---|---|---|
| PASS_MINIMAL | PASS | Continuation collapses under sufficient visibility |
| HOLD_TOPOLOGY_UNKNOWN | HOLD | Incomplete topology preserves uncertainty |
| FAIL_CONTINUATION_SURVIVES | FAIL | Continuation survives interruption |
| FALSE_PASS_INCOMPLETE_TOPOLOGY | HOLD | Prevents false PASS under incomplete visibility |

---

## Expected Rule

Incomplete topology must not produce PASS.

Unknown continuation must preserve HOLD.

Observed survivability must produce FAIL.

Sufficient collapse under visible constraints may produce PASS.

---

## Non-Authority Boundary

Expected replay outcomes are diagnostic only.

They are not:

- certification
- execution permission
- admissibility proof
- governance authority
- operational clearance