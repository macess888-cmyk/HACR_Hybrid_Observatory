"""
HACR Hybrid Observatory — Semantic Parser

Observer-only deterministic repository parser.

This parser extracts bounded semantic region visibility.
It does not infer authority, truth, legitimacy, or governance meaning.

Invariant:
parsing != authority
"""

from pathlib import Path
import json


REPO_ROOT = Path(__file__).resolve().parents[2]


CANONICAL_REGION_PATHS = {
    "boundary_layer": "governance/boundaries",
    "semantic_topology_layer": "governance/semantic_topology",
    "runtime_reduction_layer": "governance/runtime_reductions",
    "reviewer_traversability_layer": "governance/reviewer_traversability",
    "verification_layer": "governance/verification",
    "canonical_layer": "docs/canonical",
    "runtime_constraints_layer": "governance/runtime_constraints",
}


def classify_region(path: Path) -> str:
    rel = path.as_posix()

    for region_id, region_path in CANONICAL_REGION_PATHS.items():
        if rel.startswith(region_path):
            return region_id

    if rel.startswith("governance/"):
        return "governance_observability_region"

    if rel.startswith("tools/"):
        return "tooling_region"

    if rel.startswith("docs/"):
        return "documentation_region"

    return "unclassified_observability_region"


def parse_repository(root: Path = REPO_ROOT) -> dict:
    nodes = []

    for file_path in sorted(root.rglob("*.md")):
        rel = file_path.relative_to(root)

        # Skip git/internal noise
        if ".git" in rel.parts:
            continue

        region = classify_region(rel)

        nodes.append(
            {
                "id": rel.as_posix().replace("/", "__"),
                "label": file_path.stem,
                "path": rel.as_posix(),
                "region": region,
                "type": "semantic_document",
                "observer_posture": "observer_only",
                "authority_posture": "non_authoritative",
            }
        )

    return {
        "schema_version": "v1.0",
        "topology_type": "bounded_semantic_observability_topology",
        "invariants": [
            "PARSING != AUTHORITY",
            "OBSERVABILITY != GOVERNANCE",
            "REPOSITORY STRUCTURE != OPERATIONAL TRUTH",
            "UNKNOWN -> HOLD",
        ],
        "nodes": nodes,
    }


def main() -> None:
    topology = parse_repository()
    out_dir = Path(__file__).resolve().parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / "parsed_semantic_topology.json"
    out_file.write_text(json.dumps(topology, indent=2), encoding="utf-8")

    print(f"Wrote {out_file}")
    print(f"Nodes: {len(topology['nodes'])}")


if __name__ == "__main__":
    main()