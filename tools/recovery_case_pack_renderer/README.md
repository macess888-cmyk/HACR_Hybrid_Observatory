# Recovery Case Pack Renderer

## Purpose

This tool runs tiny deterministic recovery/interruption cases and renders reviewer-readable SVG outputs.

## Core Reductions

- Green is not viable.
- Visible is not traversable.
- Interrupted is not recovered.
- Being seen is not being protected.
- UNKNOWN -> HOLD.

## Workflow

1. Run `batch_recovery_case_runner.py`.
2. Review JSON outputs in `outputs/`.
3. Run `batch_svg_renderer.py`.
4. Review SVG visuals in `visuals/`.

## Boundary

Observer-only.

Not authority.
Not certification.
Not governance.