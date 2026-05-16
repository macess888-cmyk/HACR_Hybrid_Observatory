# HACR Hybrid Observatory
# Interruption Realism Checklist

Reachability / Traversability / Timing / Human Capacity

---

## Purpose

This checklist supports bounded inspection of whether interruption is realistic, reachable, and operationally meaningful.

---

## Core Principle

A theoretically available interruption path is not necessarily a realistic interruption path.

Interruption realism depends on reachability, timing, topology, and human capacity.

---

## Checklist

### 1. Reachability

- Can the interruption surface be reached?
- Can the correct actor reach it in time?
- Are required credentials available?
- Is the path accessible under degraded conditions?
- Are there hidden dependencies?

If unclear:

-> HOLD

---

### 2. Timing

- Can interruption occur before consequence persists?
- Can it occur before retry/replay activates?
- Can it occur before downstream propagation?
- Can it occur before residue becomes re-entrant?

If unclear:

-> HOLD

---

### 3. Traversability

- Can a human realistically find the path?
- Can they understand the path?
- Can they use the path under pressure?
- Does traversal require unrealistic expertise?
- Does administrative burden exceed capacity?

If unclear:

-> HOLD

---

### 4. Topology

- Are all relevant surfaces visible?
- Are downstream systems known?
- Are hidden carriers excluded?
- Are fallback paths known?
- Are recovery paths constrained?

If unclear:

-> HOLD

---

### 5. Human Capacity

- Does the path assume infinite persistence?
- Does it require repeated escalation?
- Does it require emotional endurance?
- Does it depend on family/caregiver support?
- Does it depend on digital fluency?

If unclear:

-> HOLD

---

### 6. Operational Continuation

- Can consequence continue despite interruption?
- Can stale state preserve continuation?
- Can retry/fallback restore effect-capability?
- Can operational memory reconstruct the path?

If yes:

-> FAIL

If unclear:

-> HOLD

---

## Unsafe Assumptions

Do not assume:

- visible halt means interruption
- support exists because it is documented
- escalation exists because a policy says so
- humans can traverse all declared paths
- recovery equals legitimacy
- silence equals safety

---

## Final Constraint

A consequence is not realistically interruptible unless interruption remains reachable before consequence survivability escapes the local surface.