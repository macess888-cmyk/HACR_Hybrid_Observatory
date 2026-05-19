from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

KEY_TERMS = [
    "UNKNOWN -> HOLD",
    "Replay availability is not practical reconstructability",
    "Reviewer traversal is not authority",
    "Break survivability, not ontology"
]

SCAN_EXTENSIONS = [".md", ".json"]

def scan_files():
    metrics = {
        "markdown_files": 0,
        "json_files": 0,
        "term_hits": {},
        "total_lines": 0
    }

    for term in KEY_TERMS:
        metrics["term_hits"][term] = 0

    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in SCAN_EXTENSIONS:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue

        if path.suffix.lower() == ".md":
            metrics["markdown_files"] += 1

        if path.suffix.lower() == ".json":
            metrics["json_files"] += 1

        metrics["total_lines"] += len(text.splitlines())

        for term in KEY_TERMS:
            metrics["term_hits"][term] += text.count(term)

    return metrics

def main():
    metrics = scan_files()

    print("Replay Reconstructability Index")
    print("--------------------------------")
    print(json.dumps(metrics, indent=2))
    print("--------------------------------")
    print("Replay metrics are not authority.")
    print("UNKNOWN -> HOLD.")

if __name__ == "__main__":
    main()