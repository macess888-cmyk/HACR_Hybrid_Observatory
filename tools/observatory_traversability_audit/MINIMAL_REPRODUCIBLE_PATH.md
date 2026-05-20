# Minimal Reproducible Path

## Goal

A reviewer should be able to:

1. run one deterministic case
2. generate one SVG
3. inspect one output
4. understand one reduction

within minutes.

## Canonical Path

python batch_recovery_case_runner.py
↓
python batch_svg_renderer.py
↓
visuals/
↓
review SVG output

## Preserve

Smallest operational traversal surface.