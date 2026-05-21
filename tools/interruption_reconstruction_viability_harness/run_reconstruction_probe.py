import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASE_FILE = ROOT / "tools" / "interruption_reconstruction_viability_harness" / "SAMPLE_INTERRUPTION_RECONSTRUCTION_CASE.json"

case = json.loads(CASE_FILE.read_text(encoding="utf-8"))

print("=== INTERRUPTION RECONSTRUCTION VIABILITY HARNESS ===")
print()
print(f"case_id: {case['case_id']}")
print(f"representation_status: {case['representation_status']}")
print(f"interruption_representation: {case['interruption_representation']}")
print(f"reconstruction_latency: {case['reconstruction_latency']}")
print(f"synchronization_feasibility: {case['synchronization_feasibility']}")
print(f"locality_fragmentation: {case['locality_fragmentation']}")
print(f"continuation_hardening: {case['continuation_hardening']}")
print(f"executable_effect_window: {case['executable_effect_window']}")
print()
print(f"classification: {case['classification']}")
print(f"reduction: {case['reduction']}")
print()
print("UNKNOWN -> HOLD")
print("Break survivability, not ontology.")