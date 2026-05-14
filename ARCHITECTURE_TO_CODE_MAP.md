# Architecture to Code Map

This document maps observatory architecture concepts to implementation artifacts.

The map is diagnostic-only.

It does not imply runtime orchestration, execution permission, operational authorization, certification, governance, or execution control.

---

## Mapping Table

| Diagnostic Area | Implementation Artifact | Output Artifact |
|---|---|---|
| Runtime State Semantics | hacr_core.py | core diagnostic output |
| Lens Execution | lens_engine.py | lens diagnostic output |
| Matrix Reachability | matrix_engine.py | matrix report |
| Drift Trajectory | drift_engine.py | drift report |
| Dependency Observability | dependency_engine.py | dependency report |
| Watchdog Continuity | watchdog_engine.py | watchdog report |
| Receipt Integrity | receipt_engine.py | receipt report |
| Runtime Dependency Persistence | runtime_dependency_mapper.py | runtime_dependency_report.json |

---

## Boundary

The architecture supports bounded diagnostic inspection only.

It does not:

- authorize execution
- govern systems
- certify safety
- enforce policy
- control orchestration
- replace operational controls
- provide compliance guarantees

---

## Final Constraint

The repository inspects runtime continuation visibility and dependency visibility.

It does not inherit execution authority.