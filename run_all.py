import json
from pathlib import Path
from datetime import datetime, UTC

from hacr_core import hacr_validate

from lens_engine import (
    continuity_lens,
    symmetry_lens,
    constructibility_lens
)

from matrix_engine import (
    reachability_matrix,
    matrix_risk_score
)

from drift_engine import (
    drift_trajectory
)

from dependency_engine import (
    dependency_observer
)

from receipt_engine import write_receipt

INPUT_DIR = Path("Inputs")
OUTPUT_DIR = Path("Outputs")


def run_case(path):

    with open(path, "r") as f:
        state = json.load(f)

    matrix = reachability_matrix(state)

    result = {
        "timestamp": datetime.now(UTC).isoformat(),

        "case": path.name,

        "hacr": hacr_validate(state),

        "lenses": {
            "continuity": continuity_lens(state),
            "symmetry": symmetry_lens(state),
            "constructibility": constructibility_lens(state)
        },

        "matrix": {
            "paths": matrix,
            "risk": matrix_risk_score(matrix)
        },

        "drift": drift_trajectory(state),

        "dependencies": dependency_observer(state)
    }

    return result


OUTPUT_DIR.mkdir(exist_ok=True)

all_results = []

for file in sorted(INPUT_DIR.glob("*.json")):

    print(f"\nRunning: {file.name}")

    result = run_case(file)

    all_results.append(result)

    print("\n=== HACR RESULT ===")
    print(result["hacr"])

    print("\n=== LENS RESULTS ===")
    print("continuity:", result["lenses"]["continuity"])
    print("symmetry:", result["lenses"]["symmetry"])
    print("constructibility:", result["lenses"]["constructibility"])

    print("\n=== MATRIX RESULTS ===")
    print(result["matrix"])

    print("\n=== DRIFT RESULTS ===")
    print(result["drift"])

    print("\n=== DEPENDENCY RESULTS ===")
    print(result["dependencies"])


output_text = json.dumps(all_results, indent=2)

report_path = OUTPUT_DIR / "hacr_hybrid_observatory_report.json"

report_path.write_text(
    output_text,
    encoding="utf-8"
)

receipt_path = write_receipt(
    output_text,
    "hacr_hybrid_observatory_report.sha256.txt"
)

print("\nReport written:")
print(report_path)

print("\nReceipt written:")
print(receipt_path)