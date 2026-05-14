powershell -NoProfile -Command "Set-Content -Path README.md -Encoding UTF8 -Value @'
# HACR Hybrid Observatory

Observer-Restricted Runtime Diagnostics and Topology Inspection Framework

---

## Overview

HACR Hybrid Observatory is a bounded runtime diagnostics and topology inspection framework intended for reproducibility-oriented inspection of runtime continuation visibility under declared observation conditions.

The repository focuses on inspecting whether continuation persistence, retry persistence, replay persistence, dependency visibility, downstream continuation reachability, or recovery-state persistence remain observable after interruption or invalidation under topology-scoped runtime conditions.

The observatory is intentionally:

- observer-restricted
- non-authoritative
- topology-scoped
- runtime-bounded
- reproducibility-oriented
- diagnostic-only
- operationally external

---

## Repository Boundary

The observatory does not:

- authorize execution
- govern systems
- certify safety
- enforce policy
- replace operational controls
- replace governance systems
- replace compliance processes
- provide operational guarantees
- provide compliance guarantees
- function as execution infrastructure
- function as operational authorization infrastructure
- function as execution control infrastructure
- function as autonomous safety infrastructure

All outputs remain observer-side runtime diagnostics only.

---

## Final Constraint

The repository remains:

- observer-restricted
- non-authoritative
- execution-external
- topology-scoped
- runtime-bounded
- diagnostic-only

The repository inspects runtime continuation visibility under declared observation conditions.

It does not authorize, govern, certify, enforce, or control execution.
'@"