import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CASE_FILE = ROOT / "tools" / "runtime_reconstruction_timeline_engine" / "SAMPLE_TIMELINE_CASE.json"

case = json.loads(CASE_FILE.read_text(encoding="utf-8"))

print("=== RUNTIME RECONSTRUCTION TIMELINE ENGINE ===")
print()

for item in case["timeline"]:
    print(
        f"step={item['step']} | "
        f"representation_continuity={item['representation_continuity']} | "
        f"interruptibility={item['interruptibility']}"
    )

print()
print("Timeline reduction:")
print(case["reduction"])
print()
print("classification:", case["classification"])
print("UNKNOWN -> HOLD")
print("Break survivability, not ontology.")