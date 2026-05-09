import hashlib
from pathlib import Path


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_receipt(output_text, receipt_name):
    Path("Receipts").mkdir(exist_ok=True)

    receipt_path = Path("Receipts") / receipt_name
    receipt_path.write_text(
        sha256_text(output_text),
        encoding="utf-8"
    )

    return str(receipt_path)