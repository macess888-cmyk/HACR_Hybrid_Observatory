import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CASE_FILE = (
    ROOT
    / "tools"
    / "compression_failure_boundary_tester"
    / "SAMPLE_COMPRESSION_BOUNDARY_CASE.json"
)

case = json.loads(CASE_FILE.read_text(encoding="utf-8"))

print("=== COMPRESSION FAILURE BOUNDARY TESTER ===")
print()
print(f"case_id: {case['case_id']}")
print(f"observation: {case['observation']}")
print(f"recurrence: {case['recurrence']}")
print()
print("Existing surfaces checked:")

for surface in case["existing_surfaces_checked"]:
    print(f"  - {surface}")

print()
print(f"compression_status: {case['compression_status']}")
print(f"expansion_pressure: {case['expansion_pressure']}")
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