import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RECEIPT = ROOT / "Receipts" / "HOSTILE_RUNTIME_CASE_001_RECEIPT.json"
DEFAULT_OUTPUT = ROOT / "Receipts" / "HOSTILE_RUNTIME_CASE_001_RECEIPT_SHA256.json"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def sha256_file(path: Path) -> str:
    if not path.exists():
        fail(f"Receipt not found: {path}")

    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> None:
    receipt_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_RECEIPT
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUTPUT

    receipt_hash = sha256_file(receipt_path)

    output = {
        "hash_receipt_id": f"{receipt_path.stem}_SHA256",
        "source_receipt": str(receipt_path.relative_to(ROOT)),
        "sha256": receipt_hash,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "verification_scope": "deterministic hostile-runtime receipt integrity",
        "boundary": {
            "observer_only": True,
            "runtime_local": True,
            "anti_authoritative": True,
            "non_remedial": True,
            "does_not_authorize_intervention": True
        },
        "invariant": "Break survivability, not ontology.",
        "default": "UNKNOWN -> HOLD"
    }

    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print("PASS: receipt SHA256 generated")
    print(f"source: {receipt_path}")
    print(f"sha256: {receipt_hash}")
    print(f"output: {output_path}")


if __name__ == "__main__":
    main()