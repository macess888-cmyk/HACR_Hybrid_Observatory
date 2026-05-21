import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

STATE_FILE = ROOT / "tools" / "runtime_state_renderer" / "SAMPLE_RUNTIME_STATE_SEQUENCE.json"
RECEIPT_FILE = ROOT / "Receipts" / "HOSTILE_RUNTIME_CASE_001_RECEIPT.json"
VERIFY_SCRIPT = ROOT / "tools" / "receipt_integrity_verifier" / "verify_receipt.py"
PIPELINE_OUTPUT_FILE = ROOT / "Receipts" / "PIPELINE_RUN_001_OUTPUT.json"

PIPELINE_ID = "HOSTILE_RUNTIME_PIPELINE_001"


def load_json(path: Path) -> dict:
    if not path.exists():
        print(f"FAIL: missing file: {path}")
        sys.exit(1)

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"FAIL: invalid JSON in {path}: {exc}")
        sys.exit(1)


def main() -> None:
    print("=== HOSTILE RUNTIME PIPELINE RUNNER ===")
    print()

    print("Loading runtime state sequence:")
    print(f"  {STATE_FILE}")
    print()

    state_data = load_json(STATE_FILE)

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
        [sys.executable, str(VERIFY_SCRIPT), str(RECEIPT_FILE)],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        print("Pipeline verification FAILED.")
        sys.exit(1)

    receipt_data = load_json(RECEIPT_FILE)

    semantic_outputs = [
        state["classification"] for state in state_data["states"]
    ]

    output = {
        "pipeline_id": PIPELINE_ID,
        "runtime_sequence_id": state_data["runtime_sequence_id"],
        "receipt_id": receipt_data["receipt_id"],
        "verification_status": "PASS",
        "semantic_outputs_observed": semantic_outputs,
        "final_runtime_classification": semantic_outputs[-1],
        "verified_receipt_semantic_output": receipt_data["semantic_output"],
        "boundary_status": {
            "observer_only": True,
            "runtime_local": True,
            "anti_authoritative": True,
            "non_remedial": True,
            "does_not_authorize_intervention": True
        },
        "invariant": "Break survivability, not ontology.",
        "default": "UNKNOWN -> HOLD"
    }

    PIPELINE_OUTPUT_FILE.write_text(
        json.dumps(output, indent=2),
        encoding="utf-8"
    )

    print("Pipeline verification PASSED.")
    print()
    print("Pipeline output written:")
    print(f"  {PIPELINE_OUTPUT_FILE}")
    print()
    print("Deterministic hostile-runtime replay complete.")


if __name__ == "__main__":
    main()