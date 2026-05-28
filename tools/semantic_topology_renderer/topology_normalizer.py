"""
HACR Hybrid Observatory — Topology Normalizer

Normalizes semantic topology into bounded deterministic structure.

Invariant:
normalization != semantic authority
"""

from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent


def load_density_topology() -> dict:
    path = BASE_DIR / "output" / "semantic_density.json"
    if not path.exists():
        raise FileNotFoundError(
            "Missing semantic density output. Run density_analyzer.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_topology(topology: dict) -> dict:
    nodes = topology.get("nodes", [])
    corridors = topology.get("corridors", [])

    normalized_nodes = sorted(nodes, key=lambda n: (n["region"], n["label"]))
    normalized_corridors = sorted(corridors, key=lambda c: c["id"])

    return {
        "schema_version": "v1.0",
        "topology_type": "bounded_semantic_observability_topology",
        "observer_posture": "observer_only",
        "authority_posture": "non_authoritative",
        "normalization_status": "deterministic",
        "node_count": len(normalized_nodes),
        "corridor_count": len(normalized_corridors),
        "nodes": normalized_nodes,
        "corridors": normalized_corridors,
        "density_analysis": topology.get("density_analysis", []),
        "normalization_invariants": [
            "NORMALIZATION != AUTHORITY",
            "ORDERING != LEGITIMACY",
            "STRUCTURE != TRUTH",
            "UNKNOWN -> HOLD",
        ],
    }


def main() -> None:
    topology = load_density_topology()
    normalized = normalize_topology(topology)

    out_file = BASE_DIR / "output" / "normalized_topology.json"
    out_file.write_text(json.dumps(normalized, indent=2), encoding="utf-8")

    print(f"Wrote {out_file}")
    print(f"Normalized Nodes: {normalized['node_count']}")
    print(f"Normalized Corridors: {normalized['corridor_count']}")


if __name__ == "__main__":
    main()