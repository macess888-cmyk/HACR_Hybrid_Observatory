import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CASE_FILE = ROOT / "tools" / "governability_mirage_visualizer" / "SAMPLE_GOVERNABILITY_MIRAGE_CASE.json"

case = json.loads(CASE_FILE.read_text(encoding="utf-8"))

print("=== GOVERNABILITY MIRAGE VISUALIZER ===")
print()

for key, value in case.items():
    print(f"{key}: {value}")

print()
print("Mirage condition detected:")
print("representation continuity persists while executable interruption viability degrades")
print()
print("UNKNOWN -> HOLD")
print("Break survivability, not ontology.")