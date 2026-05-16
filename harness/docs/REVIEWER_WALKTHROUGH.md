# Reviewer Walkthrough

## Objective

The reviewer should independently inspect whether:

- interruption collapses continuation
- topology visibility is sufficient
- replayability remains independently reachable
- hidden continuation survives
- false PASS conditions exist

without requiring semantic inheritance.

---

# Inspection Flow

1. Load case.
2. Inspect topology visibility.
3. Inspect replayability.
4. Inspect continuation survivability.
5. Evaluate interruption locality.
6. Compare expected state.
7. Attempt falsification.

---

# Reviewer Warning

A clean PASS under incomplete topology visibility should be treated as suspect.

Unknown continuation surfaces preserve HOLD.