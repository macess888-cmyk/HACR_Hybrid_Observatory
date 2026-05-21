import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

STATE_FILE = ROOT / "tools" / "runtime_state_renderer" / "SAMPLE_RUNTIME_STATE_SEQUENCE.json"
RECEIPT_FILE = ROOT / "Receipts" / "HOSTILE_RUNTIME_CASE_001_RECEIPT.json"
VERIFY_SCRIPT = ROOT / "tools" / "receipt_integrity_verifier" / "verify_receipt.py"

print("=== HOSTILE RUNTIME PIPELINE RUNNER ===")
print()

print(f"Loading runtime state sequence:")
print(f"  {STATE_FILE}")
print()

state_data = json.loads(STATE_FILE.read_text(encoding="utf-8"))

print("Runtime sequence loaded.")
print(f"Sequence ID: {state_data['runtime_sequence_id']}")
print()

print("Runtime states:")
for state in state_data["states"]:
    print(
        f"  step={state['step']} "
        f"classification={state['classification']} "
        f"continuation_hardening={state['continuation_hardening']}"
    )

print()
print("Verifying receipt...")
print()

result = subprocess.run(
    ["python", str(VERIFY_SCRIPT), str(RECEIPT_FILE)],
    capture_output=True,
    text=True
)

print(result.stdout)

if result.returncode != 0:
    print("Pipeline verification FAILED.")
    exit(1)

print("Pipeline verification PASSED.")
print()
print("Deterministic hostile-runtime replay complete.")