import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASE_FILE = ROOT / "tools" / "care_asro_seam_integrity_tester" / "SAMPLE_SEAM_CASE.json"

case = json.loads(CASE_FILE.read_text(encoding="utf-8"))

print("=== CARE / ASRO SEAM INTEGRITY TESTER ===")
print()

for key, value in case.items():
    print(f"{key}: {value}")

print()
print("Seam condition:")
print("evidence continuity preserved without inheriting executable interruption legitimacy")
print()
print("classification:", case["classification"])
print("UNKNOWN -> HOLD")
print("Break survivability, not ontology.")