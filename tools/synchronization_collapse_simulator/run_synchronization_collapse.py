import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASE_FILE = ROOT / "tools" / "synchronization_collapse_simulator" / "SAMPLE_SYNCHRONIZATION_COLLAPSE_CASE.json"

case = json.loads(CASE_FILE.read_text(encoding="utf-8"))

print("=== SYNCHRONIZATION COLLAPSE SIMULATOR ===")
print()

for key, value in case.items():
    print(f"{key}: {value}")

print()
print("Synchronization condition:")
print("machine-speed continuation outpaces human reconstruction and escalation timing")
print()
print("UNKNOWN -> HOLD")
print("Break survivability, not ontology.")