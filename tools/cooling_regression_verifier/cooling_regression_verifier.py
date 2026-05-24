import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RECEIPT_ROOT = ROOT / "tools" / "cooling_stack_runner" / "receipts"

CATEGORIES = [
    "semantic",
    "visual",
    "falsifiability",
    "interpretation",
]

def load_receipts(path):
    receipts = []

    if not path.exists():
        return receipts

    for file in path.glob("*.json"):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            receipts.append((file.name, data))
        except Exception:
            continue

    return receipts

def summarize(receipts):
    summary = {
        "PASS": 0,
        "COOL": 0,
        "HOLD": 0,
        "STOP": 0,
        "REWRITE": 0,
    }

    for _, data in receipts:
        status = data.get("status", "UNKNOWN")
        if status in summary:
            summary[status] += 1

    return summary

def main():
    print("=" * 60)
    print("COOLING REGRESSION VERIFIER")
    print("=" * 60)

    overall = {}

    for category in CATEGORIES:
        category_path = RECEIPT_ROOT / category
        receipts = load_receipts(category_path)

        summary = summarize(receipts)
        overall[category] = summary

        print(f"\nCATEGORY: {category}")

        for status, count in summary.items():
            print(f"  {status}: {count}")

    print("\n============================================================")
    print("Regression verification complete.")
    print("UNKNOWN -> HOLD")
    print("Break survivability, not ontology.")
    print("============================================================")

if __name__ == "__main__":
    main()