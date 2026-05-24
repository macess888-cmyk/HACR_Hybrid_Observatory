import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

AUTHORITY_TERMS = [
    "necessary", "must", "inevitable", "destiny", "required",
    "authoritative", "unavoidable", "civilization-scale governance",
]

ONTOLOGY_TERMS = [
    "universal truth", "hidden reality", "ultimate structure",
    "complete model", "totalizing",
]

SHADOW_RISK_TERMS = [
    "hidden control", "secret system", "conspiracy", "invisible rulers",
]

INEVITABILITY_TERMS = [
    "will happen", "cannot be stopped", "guaranteed", "certain outcome",
]

def inspect_text(text):
    findings = []

    checks = [
        ("AUTHORITY_DRIFT", AUTHORITY_TERMS),
        ("ONTOLOGY_DRIFT", ONTOLOGY_TERMS),
        ("SHADOW_MYTHOLOGY_RISK", SHADOW_RISK_TERMS),
        ("INEVITABILITY_RISK", INEVITABILITY_TERMS),
    ]

    lowered = text.lower()

    for label, terms in checks:
        for term in terms:
            if term.lower() in lowered:
                findings.append({"type": label, "term": term})

    word_count = len(text.split())

    if word_count > 400:
        findings.append({"type": "DENSITY_LOAD", "term": f"{word_count} words"})

    if any(f["type"] == "ONTOLOGY_DRIFT" for f in findings):
        status = "STOP"
    elif any(f["type"] in ["AUTHORITY_DRIFT", "INEVITABILITY_RISK"] for f in findings):
        status = "COOL"
    elif findings:
        status = "HOLD"
    else:
        status = "PASS"

    return status, findings, word_count

def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def main():
    if len(sys.argv) != 2:
        print("Usage: python semantic_cooling_auditor.py <input_file>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    status, findings, word_count = inspect_text(text)

    receipt = {
        "tool": "semantic_cooling_auditor",
        "status": status,
        "input_file": str(input_path),
        "input_sha256": sha256_text(text),
        "word_count": word_count,
        "findings": findings,
        "boundary": "observer-only, runtime-local, non-authoritative, non-ontological",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "closure": "UNKNOWN -> HOLD. Break survivability, not ontology."
    }

    print("=" * 60)
    print("SEMANTIC COOLING AUDITOR")
    print("=" * 60)
    print(f"STATUS: {status}")
    print(f"WORDS: {word_count}")
    print(f"SHA256: {receipt['input_sha256']}")
    print()

    if findings:
        print("FINDINGS:")
        for finding in findings:
            print(f"- {finding['type']}: {finding['term']}")
    else:
        print("No major semantic survivability risks detected.")

    output_path = input_path.with_suffix(".semantic_cooling_receipt.json")
    output_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")

    print()
    print(f"Receipt written: {output_path}")
    print("UNKNOWN -> HOLD")
    print("Break survivability, not ontology.")

if __name__ == "__main__":
    main()