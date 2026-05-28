"""
HACR Hybrid Observatory — Traversal Mapper

Builds bounded reviewer traversal visibility.

Invariant:
traversal mapping != interpretive authority
"""

from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent


CANONICAL_TRAVERSALS = [
    {
        "id": "canonical_entry_path",
        "label": "Canonical Entry Path",
        "paths": [
            "docs/canonical/START_HERE_CANONICAL.md",
            "governance/SEMANTIC_COMPRESSION.md",
            "governance/REPOSITORY_COHERENCE_MODEL.md",
            "governance/boundaries/README.md",
        ],
    },
    {
        "id": "boundary_path",
        "label": "Boundary Traversal Path",
        "paths": [
            "governance/boundaries/REALITY_BOUNDARY.md",
            "governance/boundaries/ONTOLOGY_BOUNDARY.md",
            "governance/boundaries/NON_CLOSURE_BOUNDARY.md",
            "governance/boundaries/BOUNDARY_HUMILITY.md",
        ],
    },
    {
        "id": "semantic_topology_path",
        "label": "Semantic Topology Path",
        "paths": [
            "governance/semantic_topology/SEMANTIC_TOPOLOGY_MODEL.md",
            "governance/semantic_topology/SEMANTIC_CORRIDORS.md",
            "governance/semantic_topology/TOPOLOGY_RENDER_TARGETS.md",
        ],
    },
    {
        "id": "verification_path",
        "label": "Verification Path",
        "paths": [
            "governance/verification/VERIFICATION_LIMITATIONS.md",
            "governance/verification/QA_BOUNDARY_MODEL.md",
        ],
    },
]


def load_normalized_topology() -> dict:
    path = BASE_DIR / "output" / "normalized_topology.json"
    if not path.exists():
        raise FileNotFoundError(
            "Missing normalized topology. Run topology_normalizer.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def map_traversals(topology: dict) -> dict:
    traversals = []

    for traversal in CANONICAL_TRAVERSALS:
        traversals.append(
            {
                **traversal,
                "type": "reviewer_traversal",
                "observer_posture": "observer_only",
                "authority_posture": "non_authoritative",
                "invariant": "TRAVERSAL != AUTHORITY",
            }
        )

    return {
        **topology,
        "reviewer_traversals": traversals,
        "traversal_invariants": [
            "TRAVERSAL MAPPING != INTERPRETIVE AUTHORITY",
            "ROUTING != GOVERNANCE",
            "VISIBILITY != CONTROL",
            "UNKNOWN -> HOLD",
        ],
    }


def main() -> None:
    topology = load_normalized_topology()
    traversal_topology = map_traversals(topology)

    out_file = BASE_DIR / "output" / "traversal_topology.json"
    out_file.write_text(json.dumps(traversal_topology, indent=2), encoding="utf-8")

    print(f"Wrote {out_file}")
    print(f"Traversals: {len(traversal_topology['reviewer_traversals'])}")


if __name__ == "__main__":
    main()