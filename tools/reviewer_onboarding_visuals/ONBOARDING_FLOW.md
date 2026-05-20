# Reviewer Onboarding Flow

## Goal

Allow reviewers to reproduce deterministic observability outputs in under two minutes.

## Reviewer Path

1. Open:
   `tools/recovery_case_pack_renderer/`

2. Run:
   `python batch_recovery_case_runner.py`

3. Run:
   `python batch_svg_renderer.py`

4. Open:
   `visuals/`

5. Compare:
   - classifications
   - timing windows
   - layer survival states
   - reductions

6. Confirm:
   - observable ≠ inspectable
   - inspectable ≠ traversable
   - traversable ≠ interruptible
   - interruptible ≠ destabilizable
   - destabilizable ≠ recoverable

7. Preserve:
   UNKNOWN -> HOLD

## Boundary

Visual inspection is not authority.