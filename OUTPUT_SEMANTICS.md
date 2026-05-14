# Output Semantics

PASS / HOLD / FAIL are observer-side runtime diagnostic observations.

They are not execution permissions, governance rulings, safety guarantees, certification results, compliance determinations, or runtime execution prerequisite verification.

---

## PASS

No continuation persistence observed within declared runtime and topology scope.

PASS does not mean:

- safe
- certified
- approved
- compliant
- execution-authorized
- globally complete

---

## HOLD

Insufficient visibility for reliable diagnostic observation.

HOLD may indicate:

- incomplete topology visibility
- incomplete runtime visibility
- incomplete dependency visibility
- incomplete replay visibility
- incomplete recovery visibility
- unresolved downstream continuation visibility

---

## FAIL

Continuation persistence remained observable after interruption or invalidation.

FAIL may indicate:

- retry persistence
- replay persistence
- cached execution continuity
- downstream continuation reachability
- recovery-state persistence
- continuation path visibility

---

## Boundary

Outputs may inform human review.

Outputs may not become:

- execution permission
- operational authorization
- runtime dependency
- orchestration input
- certification artifact
- compliance determination

---

## Final Constraint

Diagnostic observations remain bounded to declared topology scope, runtime conditions, and observability limits.