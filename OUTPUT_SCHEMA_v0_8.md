# HACR v0.8 Output Schema Reference

## Purpose

Defines the canonical report structure for observer outputs.

This improves:
- reviewer readability
- deterministic structure
- lineage consistency
- cross-lens interoperability
- output normalization

---

# Canonical Structure

```json
{
  "lens": "STRING",
  "status": "PASS | HOLD | SHADOW | FAIL | CRITICAL | TRACEABLE | PROJECTED | EXPORTED",
  "score": 0,
  "observer_mode": true,
  "summary": "STRING",
  "findings": [],
  "derived_from": [],
  "non_claims": []
}