import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CASE_FILE = (
    ROOT
    / "tools"
    / "judgement_formation_localizer"
    / "SAMPLE_JUDGEMENT_FORMATION_CASE.json"
)

case = json.loads(CASE_FILE.read_text(encoding="utf-8"))

print("=== JUDGEMENT FORMATION LOCALIZER ===")
print()

print(f"case_id: {case['case_id']}")
print(f"scenario: {case['scenario']}")
print()

print("Runtime conditions:")
for key, value in case["runtime_conditions"].items():
    print(f"  {key}: {value}")

print()

print("Observed surfaces:")
for surface in case["observed_surfaces"]:
    print(f"  - {surface}")

print()

print(f"formation_status: {case['formation_status']}")
print(f"classification: {case['classification']}")

print()
print("Reduction:")
print(case["reduction"])

print()
print("Boundary:")
for key, value in case["boundary"].items():
    print(f"  {key}: {value}")

print()
print("UNKNOWN -> HOLD")
print("Break survivability, not ontology.")