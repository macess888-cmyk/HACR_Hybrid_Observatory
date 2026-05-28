"""
HACR Hybrid Observatory — Corridor Builder

Builds bounded semantic corridors from parsed repository topology.

Invariant:
corridor visibility != operational workflow
"""

from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent


CANONICAL_CORRIDORS = [
    {
        "id": "observability_to_authority",
        "source_region": "semantic_topology_layer",
        "target_region": "boundary_layer",
        "label": "Observability → Authority Containment",
        "risk": "authority_inheritance",
        "invariant": "OBSERVABILITY != AUTHORITY",
    },
    {
        "id": "replay_to_legitimacy",
        "source_region": "runtime_reduction_layer",
        "target_region": "boundary_layer",
        "label": "Replay → Legitimacy Containment",
        "risk": "legitimacy_inheritance",
        "invariant": "REPLAY != REALITY",
    },
    {
        "id": "verification_to_truth",
        "source_region": "verification_layer",
        "target_region": "boundary_layer",
        "label": "Verification → Truth Containment",
        "risk": "truth_inheritance",
        "invariant": "VERIFICATION != CERTIFICATION",
    },
    {
        "id": "traversability_to_authority",
        "source_region": "reviewer_traversability_layer",
        "target_region": "boundary_layer",
        "label": "Traversal → Authority Containment",
        "risk": "reviewer_authority_drift",
        "invariant": "TRAVERSAL GUIDANCE != INTERPRETIVE AUTHORITY",
    },
    {
        "id": "canonical_to_legitimacy",
        "source_region": "canonical_layer",
        "target_region": "boundary_layer",
        "label": "Canonical → Legitimacy Containment",
        "risk": "canonical_authority_drift",
        "invariant": "CANONICAL != AUTHORITATIVE",
    },
]


def load_parsed_topology() -> dict:
    path = BASE_DIR / "output" / "parsed_semantic_topology.json"
    if not path.exists():
        raise FileNotFoundError(
            "Missing parsed topology. Run semantic_parser.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def build_corridors(topology: dict) -> dict:
    regions = sorted({node["region"] for node in topology.get("nodes", [])})

    corridors = []
    for corridor in CANONICAL_CORRIDORS:
        if (
            corridor["source_region"] in regions
            and corridor["target_region"] in regions
        ):
            corridors.append(
                {
                    **corridor,
                    "type": "semantic_corridor",
                    "observer_posture": "observer_only",
                    "authority_posture": "non_authoritative",
                }
            )

    return {
        **topology,
        "corridors": corridors,
        "corridor_invariants": [
            "CORRIDOR VISIBILITY != OPERATIONAL WORKFLOW",
            "SEMANTIC FLOW != GOVERNANCE ROUTING",
            "UNKNOWN -> HOLD",
        ],
    }


def main() -> None:
    topology = load_parsed_topology()
    corridor_topology = build_corridors(topology)

    out_file = BASE_DIR / "output" / "semantic_corridors.json"
    out_file.write_text(json.dumps(corridor_topology, indent=2), encoding="utf-8")

    print(f"Wrote {out_file}")
    print(f"Corridors: {len(corridor_topology['corridors'])}")


if __name__ == "__main__":
    main()