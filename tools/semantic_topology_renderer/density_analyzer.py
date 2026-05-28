"""
HACR Hybrid Observatory — Density Analyzer

Calculates bounded semantic density visibility.

Invariant:
density visibility != semantic completeness
"""

from pathlib import Path
import json
from collections import Counter


BASE_DIR = Path(__file__).resolve().parent


def load_corridor_topology() -> dict:
    path = BASE_DIR / "output" / "semantic_corridors.json"
    if not path.exists():
        raise FileNotFoundError(
            "Missing semantic corridors. Run corridor_builder.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def analyze_density(topology: dict) -> dict:
    nodes = topology.get("nodes", [])
    region_counts = Counter(node["region"] for node in nodes)

    density = []
    for region, count in sorted(region_counts.items()):
        if count >= 25:
            pressure = "HIGH"
        elif count >= 10:
            pressure = "MEDIUM"
        else:
            pressure = "LOW"

        density.append(
            {
                "region": region,
                "document_count": count,
                "density_pressure": pressure,
                "interpretation": "bounded_visibility_only",
                "invariant": "DENSITY != AUTHORITY",
            }
        )

    return {
        **topology,
        "density_analysis": density,
        "density_invariants": [
            "DENSITY VISIBILITY != SEMANTIC COMPLETENESS",
            "DOCUMENT COUNT != IMPORTANCE",
            "HIGH DENSITY != AUTHORITY",
            "UNKNOWN -> HOLD",
        ],
    }


def main() -> None:
    topology = load_corridor_topology()
    density_topology = analyze_density(topology)

    out_file = BASE_DIR / "output" / "semantic_density.json"
    out_file.write_text(json.dumps(density_topology, indent=2), encoding="utf-8")

    print(f"Wrote {out_file}")
    for item in density_topology["density_analysis"]:
        print(
            f"{item['region']}: {item['document_count']} "
            f"({item['density_pressure']})"
        )


if __name__ == "__main__":
    main()