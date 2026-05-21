import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CASE_FILE = ROOT / "tools" / "runtime_governability_decay_index" / "SAMPLE_RUNTIME_GOVERNABILITY_DECAY_CASE.json"

case = json.loads(CASE_FILE.read_text(encoding="utf-8"))

print("=== RUNTIME GOVERNABILITY DECAY INDEX ===")
print()

for key, value in case.items():
    print(f"{key}: {value}")

print()
print("Runtime compression:")
print("governability appearance persists while executable interruption viability degrades")
print()
print("classification:", case["classification"])
print("UNKNOWN -> HOLD")
print("Break survivability, not ontology.")