# HACR Minimal Replay Harness

## Purpose

This harness exists to support:

- bounded replayability
- reviewer challengeability
- deterministic falsification
- false PASS detection
- topology-local inspection
- interruption realism
- HOLD preservation under uncertainty

The harness is intentionally:

- minimal
- replay-oriented
- reviewer-reachable
- deterministic
- bounded
- non-authoritative

---

# Harness States

The harness currently supports:

- PASS
- HOLD
- FAIL
- FALSE_PASS

---

# Core Principle

Replayability must remain operationally reachable.

If replay cannot independently fail:

-> replay becomes representational.

---

# Reviewer Goal

A reviewer should be able to:

- reproduce outcomes
- challenge assumptions
- trigger HOLD conditions
- detect false PASS
- inspect topology limits
- and independently reach failure states

without inheriting semantic authority.

---

# Repository Direction

The harness prioritizes:

- runtime falsification
- replay discipline
- interruption realism
- bounded inspection
- operational uncertainty visibility
- topology-aware HOLD behavior

rather than semantic expansion.