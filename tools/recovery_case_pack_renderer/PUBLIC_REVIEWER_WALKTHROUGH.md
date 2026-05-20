# Public Reviewer Walkthrough

## Purpose

This walkthrough helps reviewers reproduce the recovery case pack outputs and visuals.

## Steps

1. Open this folder.
2. Run `python batch_recovery_case_runner.py`.
3. Review generated JSON outputs in `outputs/`.
4. Run `python batch_svg_renderer.py`.
5. Review generated SVG visuals in `visuals/`.

## What To Check

- Does surface continuity remain green?
- Does recovery remain materially reachable?
- Do earlier layers survive while later layers collapse?
- Does the classification follow the timing window?
- Does the visual avoid implying authority?

## Core Reductions

- Green is not viable.
- Visible is not traversable.
- Interrupted is not recovered.
- Being seen is not being protected.
- Layer survival is not layer inheritance.
- UNKNOWN -> HOLD.

## Boundary

Observer-only.

No governance.
No certification.
No authority.