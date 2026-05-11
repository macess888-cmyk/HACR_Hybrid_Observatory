import json
import hashlib
import os
from datetime import datetime, UTC

INPUT_FILE = "Inputs/receipt_chain_case.json"
OUTPUT_FILE = "Outputs/receipt_chain_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

receipts = data.get("receipts", [])

chain = []
previous_hash = "GENESIS"

for receipt in receipts:
    payload = json.dumps(receipt, sort_keys=True)
    combined = previous_hash + payload

    current_hash = hashlib.sha256(
        combined.encode()
    ).hexdigest()

    chain.append({
        "receipt_id": receipt.get("receipt_id"),
        "previous_hash": previous_hash,
        "current_hash": current_hash
    })

    previous_hash = current_hash

report = {
    "chain_status": "TRACEABLE",
    "receipt_count": len(receipts),
    "observer_mode": True,
    "generated_at": datetime.now(UTC).isoformat(),
    "chain": chain,
    "non_claims": [
        "Not blockchain",
        "Not legal evidence",
        "Not execution authorization",
        "Not governance authority"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> TRACEABLE")