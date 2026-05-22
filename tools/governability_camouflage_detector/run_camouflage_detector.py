import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASE_FILE = ROOT / "tools" / "governability_camouflage_detector" / "SAMPLE_CAMOUFLAGE_CASE.json"

case = json.loads(CASE_FILE.read_text(encoding="utf-8"))

print("=== GOVERNABILITY CAMOUFLAGE DETECTOR ===")
print()

for key, value in case.items():
    print(f"{key}: {value}")

print()
print("Camouflage condition:")
print("preserved visibility masks degraded executable interruption realism")
print()
print("UNKNOWN -> HOLD")
print("Break survivability, not ontology.")