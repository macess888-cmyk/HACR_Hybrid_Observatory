# Start Here

HACR Hybrid Observatory is a bounded runtime diagnostics and topology inspection framework.

The repository inspects whether runtime continuation reachability remains observable after interruption or invalidation under controlled diagnostic conditions.

It is observer-restricted, non-authoritative, and reproducibility-oriented.

---

## What This Repository Does

It inspects:

- runtime continuation visibility
- retry persistence
- replay reachability
- dependency visibility
- downstream continuation reachability
- recovery-state persistence
- topology-scoped diagnostic behavior

---

## What This Repository Does Not Do

It does not:

- authorize execution
- govern systems
- certify safety
- enforce policy
- control execution
- replace operational controls
- provide compliance guarantees

---

## Diagnostic Outputs

PASS / HOLD / FAIL are diagnostic observations only.

They are not execution permissions, certification results, governance decisions, compliance findings, or operational authorization.

---

## Recommended Review Path

1. Read `README.md`
2. Read `NON_CLAIMS.md`
3. Read `ENGINEERING_LIMITATIONS.md`
4. Read `REPRODUCIBILITY.md`
5. Run the deterministic examples
6. Compare generated outputs against expected diagnostic behavior

---

## Final Constraint

The observatory inspects runtime continuation visibility.

It does not inherit execution authority.