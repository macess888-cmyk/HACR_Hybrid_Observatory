# Interactive Replay Delta Release Checklist

## Scope

This release includes:

- interactive viewer stabilization
- multi-domain scenario topology rendering
- cyber continuity replay traversal
- frame delta overlay generation
- replay and delta receipt generation
- bounded observer-only public visibility

---

# Required Checks

## Renderer

- [ ] All scenario SVGs regenerate successfully
- [ ] All scenario receipts regenerate successfully
- [ ] No missing scenario JSON files
- [ ] Shadow dependency panels render cleanly
- [ ] Recoverability corridors render cleanly
- [ ] Metadata panels render cleanly

## Interactive Viewer

- [ ] Scenario dropdown loads all scenarios
- [ ] Open SVG works
- [ ] Download JSON works
- [ ] Download Receipt works
- [ ] Zoom controls work
- [ ] Fit view works
- [ ] Notes toggle works
- [ ] Non-claim toggle works

## Replay

- [ ] Replay frames regenerate successfully
- [ ] Replay receipt generates successfully
- [ ] Load Replay works
- [ ] First / Previous / Next / Last work
- [ ] Play / Pause work
- [ ] Replay JSON download works
- [ ] Replay receipt download works

## Delta Overlay

- [ ] Delta overlays regenerate successfully
- [ ] Delta receipt generates successfully
- [ ] Load Delta works
- [ ] First / Previous / Next / Last work
- [ ] Delta JSON download works
- [ ] Delta receipt download works

## Boundary Review

- [ ] No prediction claims
- [ ] No governance authority claims
- [ ] No certification claims
- [ ] No operational guidance claims
- [ ] No scoring claims
- [ ] No safety guarantee claims
- [ ] Observer-only framing preserved
- [ ] Deterministic artifact framing preserved

---

# Release Reduction

visible continuity != preserved recoverability

This release provides bounded continuity evolution visibility only.