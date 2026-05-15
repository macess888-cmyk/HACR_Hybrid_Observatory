# CANONICAL ROUTING SPECIFICATION
Observer-Only / Boundary-First
Canonical Routing Layer v0.1

## PURPOSE

Define:
- admissible signal classes
- propagation boundaries
- hold conditions
- termination conditions

This document:
- does NOT authorize
- does NOT optimize
- does NOT route execution
- does NOT infer authority

Observer visibility only.

---

# CORE INVARIANTS

- Signals never imply commands
- Propagation is bounded
- Recovery precedes optimization
- HOLD is valid
- No centralized orchestration
- No implicit authority inheritance
- No irreversible escalation

---

# SIGNAL CLASSES

## CLASS A — OBSERVATIONAL

Examples:
- PASS
- HOLD
- FAIL
- UNSTABLE
- LOCAL_DRIFT
- RECOVERY_VISIBLE

Allowed:
- read-only propagation
- observer visibility

Forbidden:
- execution triggering
- optimization routing

---

## CLASS B — STRUCTURAL

Examples:
- geometry mismatch
- interface incompatibility
- propagation boundary breach
- load discontinuity

Allowed:
- local containment
- boundary logging

Forbidden:
- automatic correction
- autonomous adaptation

---

## CLASS C — GOVERNANCE

Examples:
- HOLD activation
- recovery state
- consent status
- escalation visibility

Allowed:
- bounded visibility
- reversible pause states

Forbidden:
- authority escalation
- enforcement logic

---

# PROPAGATION RULES

## ALLOWED

Signals may:
- inform
- expose boundaries
- expose local state
- expose recovery visibility

Signals may NOT:
- command
- rank
- optimize
- predict inevitability
- infer legitimacy

---

# HOLD CONDITIONS

Propagation enters HOLD when:
- provenance unclear
- authority inferred
- recovery absent
- escalation unresolved
- routing ambiguity detected
- boundary conflict detected

---

# TERMINATION CONDITIONS

Propagation terminates immediately when:
- signals become prescriptive
- execution authority emerges
- centralized orchestration appears
- irreversible optimization appears
- system attempts cross-boundary control

Termination is:
- local
- silent
- reversible only through explicit recovery

---

# RECOVERY CONDITIONS

Recovery allowed only if:
- scope contracts
- propagation reduces
- authority removed
- recovery visible
- boundaries restabilized

Otherwise:
- remain HOLD

---

# OUTPUT SEMANTICS

PASS:
- locally coherent
- bounded propagation

HOLD:
- unresolved
- insufficient clarity
- propagation paused

FAIL:
- boundary incompatibility detected

STOP:
- propagation terminated

---

# OBSERVER CONSTRAINT

This routing layer:
- observes only
- classifies only
- exposes only

It never:
- governs
- controls
- authorizes
- optimizes
- replaces human consent

---

# DEFAULT STATE

HOLD