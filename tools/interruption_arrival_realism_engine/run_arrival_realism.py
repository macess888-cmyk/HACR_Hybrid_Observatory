import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASE_FILE = ROOT / "tools" / "interruption_arrival_realism_engine" / "SAMPLE_ARRIVAL_REALISM_CASE.json"

case = json.loads(CASE_FILE.read_text(encoding="utf-8"))

print("=== INTERRUPTION ARRIVAL REALISM ENGINE ===")
print()

for key, value in case.items():
    print(f"{key}: {value}")

print()
print("Runtime compression:")
print(case["reduction"])
print()
print("UNKNOWN -> HOLD")
print("Break survivability, not ontology.")