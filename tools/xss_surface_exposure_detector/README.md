# XSS Surface Exposure Detector

Defensive observer-only scanner for identifying possible XSS exposure surfaces.

## Purpose

Detect code patterns that may indicate XSS risk without exploiting them.

## Detects

- unsafe innerHTML usage
- document.write usage
- inline event handlers
- unescaped template output
- unsafe URL parameter rendering
- risky script injection patterns

## Boundary

This tool does NOT:
- exploit vulnerabilities
- generate attack payloads
- bypass filters
- test live targets without authorization
- provide offensive instructions

Detect exposure only.

UNKNOWN -> HOLD.