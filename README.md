# HACR Hybrid Observatory

Observer-restricted execution-bound continuity survivability observatory.

The repository focuses on deterministic continuity inspection at execution-boundary surfaces under controlled conditions.

The observatory is intentionally:
- observer-only
- deterministic
- reproducible
- non-authoritative
- publication-safe
- execution-bound

The observatory does not:
- govern execution
- authorize actions
- certify systems
- provide production guarantees
- replace runtime admissibility
- act as operational authority

The repository only exposes whether continuation-survivability remained observable after refusal under controlled conditions.

---

# Core Boundary

No present-state proof → no execution.  
No proof → no bind.  
No bind → no admissible effect.

Bind is the only admissible transition surface for execution-real consequence.

If inherited effect-capability remains realizable without fresh admissible bind:

→ NO_VALID_DECISION

---

# Runtime Survivability Harness

The repository includes a minimal runtime survivability harness for controlled execution-boundary pressure testing.

Purpose:
- simulate distributed refusal invalidation scenarios
- test replay/re-entry survivability
- test delayed worker execution
- test unresolved convergence behavior
- pressure-test PASS / HOLD / FAIL semantics under controlled runtime conditions

The harness does not:
- govern execution
- authorize runtime actions
- certify systems
- provide production guarantees
- enforce distributed invalidation

It only exposes whether inherited effect-capability remained realizable after refusal under controlled runtime scenarios.

Current runtime scenarios:
- delayed worker false refusal
- queue uncertainty HOLD behavior
- bind-gated retry survivability

Run locally:

```bash
python runtime/runtime_survivability_harness.py
```

---

# PASS / HOLD / FAIL

PASS:
Inherited effect-capability was invalidated before residual realizability survived elsewhere.

HOLD:
Propagation, convergence, or invalidation completeness could not be independently established.

FAIL:
Inherited effect-capability remained runtime-reachable without fresh admissible bind.

---

# Governance and Containment

- `governance/EXPANSION_BOUNDARY.md`

The repository intentionally prioritizes:
- compression over ontology expansion
- runtime falsifiability over semantic growth
- infrastructure realism over representational governance
- reviewer reproducibility over delegated trust

---

# Reviewer Reproducibility

The repository includes deterministic reviewer reproducibility paths for controlled continuity inspection and runtime survivability pressure testing.

Reviewers should independently regenerate outputs locally from the same controlled inputs.

The observatory should remain:
- inspectable
- pressure-testable
- falsifiable
- independently reproducible

rather than dependent on institutional trust or delegated authority.

---

# Publication Boundary

The repository is:
- observer-restricted
- non-consumable by execution
- non-remediating
- non-routing
- non-binding

Observer artifacts must never become:
- execution authority
- runtime admissibility
- operational dependency
- substitute bind proof

If observer output becomes operationally consumable by execution:

→ boundary failure

---

# Current Runtime Compression

Represented refusal != execution-real refusal.

Expected convergence != execution-real refusal.

Surface existence != capability survivability.

Continuation is not forbidden.  
Unbound continuation is forbidden.

A local brake is not fail-closed if inherited effect-capability remains realizable elsewhere inside the governed execution boundary.

No bind -> no effect.