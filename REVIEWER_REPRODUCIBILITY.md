# Reviewer Reproducibility Guide

Purpose:
Provide a minimal deterministic path for reviewers to regenerate inspection artifacts without relying on symbolic interpretation.

---

# Boundary

This repository produces bounded observer-side inspection artifacts only.

It does not:

- authorize execution
- enforce refusal
- govern runtime behavior
- certify systems
- prove global consequence extinction

---

# Minimal Reproduction Path

From repository root:

```bash
python run_all.py