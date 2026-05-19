# React Update Loop Detector

## Purpose

Static scanner for identifying React patterns that may trigger repeated render/update loops such as React error #185.

The tool is observer-restricted.

It does not fix code automatically.

---

# Checks

The detector looks for:

- state updates inside component bodies
- useEffect blocks that update state while depending on the same state
- useLayoutEffect blocks that may update repeatedly
- unguarded update patterns
- recursive setter patterns

---

# Boundary

This tool does not:

- prove root cause
- certify correctness
- modify source code
- replace developer review

Findings are diagnostic only.

UNKNOWN -> HOLD.