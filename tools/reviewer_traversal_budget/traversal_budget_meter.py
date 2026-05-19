from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

SEARCH_TERMS = [
    "validator",
    "renderer",
    "replay",
    "reviewer traversal",
    "UNKNOWN -> HOLD"
]

SCAN_EXTENSIONS = [".md", ".json"]

def build_metrics():
    metrics = {
        "review_surfaces": 0,
        "term_density": {},
        "total_files": 0
    }

    for term in SEARCH_TERMS:
        metrics["term_density"][term] = 0

    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in SCAN_EXTENSIONS:
            continue

        try:
            text = path.read_text(encoding="utf-8").lower()
        except Exception:
            continue

        metrics["total_files"] += 1

        for term in SEARCH_TERMS:
            metrics["term_density"][term] += text.count(term.lower())

        if "review" in text or "replay" in text:
            metrics["review_surfaces"] += 1

    return metrics

def main():
    metrics = build_metrics()

    print("Reviewer Traversal Budget Meter")
    print("--------------------------------")
    print(json.dumps(metrics, indent=2))
    print("--------------------------------")
    print("Traversal metrics are not authority.")
    print("UNKNOWN -> HOLD.")

if __name__ == "__main__":
    main()