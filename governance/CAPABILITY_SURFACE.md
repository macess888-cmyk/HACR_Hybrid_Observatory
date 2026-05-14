# Capability Surface

## Supported Capability Scope

| Capability Area | Status | Notes |
|---|---|---|
| Runtime Diagnostics | SUPPORTED | observer-side diagnostics |
| Continuation Visibility Inspection | SUPPORTED | topology-scoped |
| Replay/Retry Visibility Analysis | SUPPORTED | runtime-bounded |
| Dependency Visibility Inspection | SUPPORTED | reproducibility-oriented |
| Deterministic Diagnostic Runs | SUPPORTED | bounded inspection |
| Runtime Topology Inspection | SUPPORTED | observer-restricted |

---

## Explicitly Unsupported

| Capability Area | Status | Notes |
|---|---|---|
| Execution Authorization | NOT SUPPORTED | explicitly excluded |
| Governance Infrastructure | NOT SUPPORTED | explicitly excluded |
| Runtime Enforcement | NOT SUPPORTED | observer-only boundary |
| Compliance Determination | NOT SUPPORTED | diagnostic-only outputs |
| Certification Authority | NOT SUPPORTED | no certification claims |
| Operational Control | NOT SUPPORTED | execution-external |
| Autonomous Safety Infrastructure | NOT SUPPORTED | excluded positioning |

---

## Final Constraint

The repository remains a bounded runtime diagnostics and topology inspection framework.

It does not inherit execution authority.