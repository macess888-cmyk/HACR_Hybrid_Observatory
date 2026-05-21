import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CASE_FILE = ROOT / "tools" / "interruption_traversability_mapper" / "SAMPLE_INTERRUPTION_TRAVERSABILITY_CASE.json"

case = json.loads(CASE_FILE.read_text(encoding="utf-8"))

print("=== INTERRUPTION TRAVERSABILITY MAPPER ===")
print()

for key, value in case.items():
    print(f"{key}: {value}")

print()
print("Traversability reduction:")
print(case["reduction"])
print()
print("Runtime condition:")
print("interruption remains represented while executable interruption corridors become operationally non-traversable")
print()
print("classification:", case["classification"])
print("UNKNOWN -> HOLD")
print("Break survivability, not ontology.")