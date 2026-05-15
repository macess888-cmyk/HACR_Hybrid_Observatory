# Reviewer Quickstart

## Purpose

This document provides a minimal path for reviewers to reproduce the repository's diagnostic surface.

The goal is not to prove governance, legitimacy, compliance, or execution authority.

The goal is to let reviewers inspect whether the same bounded diagnostic output can be reproduced from the same controlled input path.

---

## Reviewer Path

1. Use the fixed input set.
2. Run the deterministic command.
3. Inspect the generated output.
4. Compare the receipt chain.
5. Review PASS / HOLD / FAIL as diagnostic semantics only.
6. Check parser and scenario limitations.
7. Confirm explicit non-claims.
8. Attempt to break or falsify the result.

---

## Fixed Input Set

Current fixed historical cases are located in:

```text
failure_locator/cases/