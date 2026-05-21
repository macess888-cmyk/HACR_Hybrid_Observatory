import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CASE_FILE = ROOT / "tools" / "continuation_hardening_topology_renderer" / "SAMPLE_TOPOLOGY_CASE.json"

case = json.loads(CASE_FILE.read_text(encoding="utf-8"))

print("=== CONTINUATION HARDENING TOPOLOGY RENDERER ===")
print()

for region in case["topology_regions"]:
    print(
        f"region={region['region']} | "
        f"continuation_hardening={region['continuation_hardening']} | "
        f"interruptibility={region['interruptibility']}"
    )

print()
print("Topology reduction:")
print(case["reduction"])
print()
print("classification:", case["classification"])
print("UNKNOWN -> HOLD")
print("Break survivability, not ontology.")