# Engineering Limitations

HACR Hybrid Observatory is a bounded runtime diagnostics and topology inspection framework.

## Known Limitations

Known limitations include:

- incomplete topology visibility
- incomplete runtime visibility
- distributed system blind spots
- orchestration opacity
- recovery-state ambiguity
- replay-path uncertainty
- dependency visibility limitations
- environmental variability
- incomplete downstream observability
- incomplete external-system visibility

## Non-Guarantees

The observatory does not guarantee:

- prevention of execution
- prevention of retries
- prevention of replay
- complete runtime visibility
- complete downstream visibility
- complete dependency visibility
- safety certification
- compliance certification
- operational correctness
- policy enforcement

## Diagnostic Boundary

Outputs remain observer-side runtime diagnostics only.

PASS, HOLD, and FAIL are diagnostic observations.

They are not:

- authorization decisions
- governance decisions
- execution permissions
- compliance determinations
- certification claims
- safety guarantees

## Review Boundary

Engineering and audit review should evaluate:

- declared topology scope
- declared runtime assumptions
- declared dependency assumptions
- declared replay assumptions
- declared recovery assumptions
- declared observability limits
- reproducibility of diagnostic results

## Final Constraint

Runtime falsification overrides representational assumptions.

Representational coherence alone does not establish continuation invalidation.