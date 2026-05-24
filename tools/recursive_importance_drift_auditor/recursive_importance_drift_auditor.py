import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

INDISPENSABILITY_TERMS = [
    "indispensable",
    "necessary for society",
    "required for civilization",
    "cannot function without",
    "no other system",
    "must use",
]

CIVILIZATION_IMPORTANCE_TERMS = [
    "civilization-scale survival",
    "save civilization",
    "future of humanity",
    "humanity depends",
    "civilization-critical",
    "species-level",
]

UNIQUENESS_TERMS = [
    "unique truth",
    "only framework",
    "only system",
    "complete explanation",
    "final model",
    "ultimate framework",
]

SELF_AUTHORIZATION_TERMS = [
    "proves itself",
    "self-validating",
    "self-authorizing",
    "confirms its own necessity",
    "validates itself",
]

HISTORICAL_NECESSITY_TERMS = [
    "historically necessary",
    "inevitable emergence",
    "destined",
    "turning point for humanity",
    "epochal",
]

def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def inspect_text(text):
    findings = []
    lowered = text.lower()

    checks = [
        ("INDISPENSABILITY_DRIFT", INDISPENSABILITY_TERMS),
        ("CIVILIZATION_IMPORTANCE_DRIFT", CIVILIZATION_IMPORTANCE_TERMS),
        ("UNIQUENESS_ESCALATION", UNIQUENESS_TERMS),
        ("SELF_AUTHORIZATION_RISK", SELF_AUTHORIZATION_TERMS),
        ("HISTORICAL_NECESSITY_DRIFT", HISTORICAL_NECESSITY_TERMS),
    ]

    for label, terms in checks:
        for term in terms:
            if term.lower() in lowered:
                findings.append({"type": label, "term": term})

    word_count = len(text.split())

    if word_count > 350:
        findings.append({"type": "RECURSIVE_DENSITY_LOAD", "term": f"{word_count} words"})

    stop_types = [
        "SELF_AUTHORIZATION_RISK",
        "CIVILIZATION_IMPORTANCE_DRIFT",
        "HISTORICAL_NECESSITY_DRIFT",
    ]

    cool_types = [
        "INDISPENSABILITY_DRIFT",
        "UNIQUENESS_ESCALATION",
        "RECURSIVE_DENSITY_LOAD",
    ]

    if any(f["type"] in stop_types for f in findings):
        status = "STOP"
    elif any(f["type"] in cool_types for f in findings):
        status = "COOL"
    elif findings:
        status = "HOLD"
    else:
        status = "PASS"

    return status, findings, word_count

def main():
    if len(sys.argv) != 2:
        print("Usage: python recursive_importance_drift_auditor.py <input_file>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    status, findings, word_count = inspect_text(text)

    receipt = {
        "tool": "recursive_importance_drift_auditor",
        "status": status,
        "input_file": str(input_path),
        "input_sha256": sha256_text(text),
        "word_count": word_count,
        "findings": findings,
        "boundary": "observability utility does not create historical necessity",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "closure": "UNKNOWN -> HOLD. Break survivability, not ontology."
    }

    print("=" * 60)
    print("RECURSIVE IMPORTANCE DRIFT AUDITOR")
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
        print("No major recursive importance drift detected.")

    output_path = input_path.with_suffix(".recursive_importance_receipt.json")
    output_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")

    print()
    print(f"Receipt written: {output_path}")
    print("UNKNOWN -> HOLD")
    print("Break survivability, not ontology.")

if __name__ == "__main__":
    main()