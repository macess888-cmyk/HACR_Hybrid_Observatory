# OUTPUT SEMANTICS

HACR Hybrid Observatory outputs are diagnostic classifications only.

They are not execution permissions, governance rulings, safety guarantees, certification results, or admissibility proofs.

## Core States

| State | Meaning |
|---|---|
| PASS | A bounded observable condition was detected without the tested failure condition. |
| HOLD | Insufficient present-state evidence exists to classify the condition safely. |
| FAIL | A tested failure condition was observed. |
| SHADOW | A hidden, deferred, latent, reconstructible, or survivability-bearing surface was observed. |
| UNSTABLE | Cross-lens pressure, drift, or topology instability was observed. |
| CRITICAL | Concentrated survivability pressure or high-severity continuity exposure was observed. |

## Supporting States

| State | Meaning |
|---|---|
| TRACEABLE | A deterministic trace or receipt chain was generated and linked. |
| PROJECTED | A rendering-ready topology projection was generated. |
| EXPORTED | A deterministic export artifact was generated. |
| SVG_GENERATED | A local SVG visualization artifact was generated. |
| LANGUAGE_SIMPLIFIED | A simplified explanation artifact was generated. |
| TOPOLOGY_GRAPH_GENERATED | A topology graph artifact was generated. |

## Boundary Rule

No state in this repository means:

- execution is authorized
- execution is safe
- execution is governed
- execution is certified
- refusal globally collapsed
- downstream consequence is impossible
- production safety is guaranteed

## Observer Rule

All states are observer-side classifications.

They may support human review.

They may not become execution authority.

They may not substitute for present-state proof at the actual execution surface.

## Safe Reading

Read outputs as:

> “This observatory detected this diagnostic condition in this deterministic test case.”

Do not read outputs as:

> “This system has approved, blocked, certified, governed, or controlled execution.”