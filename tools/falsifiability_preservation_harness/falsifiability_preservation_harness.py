import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

UNIVERSAL_EXPLANATION_TERMS = [
    "explains all",
    "all forms",
    "everything fits",
    "universal explanation",
    "applies everywhere",
    "total explanation",
    "complete explanatory model",
]

NON_DISCONFIRMABLE_TERMS = [
    "cannot be disproven",
    "always true",
    "unfalsifiable",
    "non-disconfirmable",
    "every outcome confirms",
    "contradiction proves",
]

SELF_SEALING_TERMS = [
    "failure confirms",
    "success confirms",
    "hesitation confirms",
    "silence confirms",
    "denial confirms",
    "contradiction confirms",
    "contradiction can be interpreted as evidence",
]

EVIDENCE_FREE_CERTAINTY_TERMS = [
    "certainly",
    "undeniably",
    "proves without",
    "obvious proof",
    "self-evident",
    "no evidence needed",
]

ELASTICITY_TERMS = [
    "can be interpreted as evidence",
    "any outcome",
    "all outcomes",
    "every failure",
    "every success",
    "every hesitation",
]

def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def inspect_text(text):
    findings = []
    lowered = text.lower()

    checks = [
        ("UNIVERSAL_EXPLANATION_DRIFT", UNIVERSAL_EXPLANATION_TERMS),
        ("NON_DISCONFIRMABLE_FRAMING", NON_DISCONFIRMABLE_TERMS),
        ("SELF_SEALING_LOGIC", SELF_SEALING_TERMS),
        ("EVIDENCE_FREE_CERTAINTY", EVIDENCE_FREE_CERTAINTY_TERMS),
        ("INTERPRETIVE_ELASTICITY", ELASTICITY_TERMS),
    ]

    for label, terms in checks:
        for term in terms:
            if term.lower() in lowered:
                findings.append({"type": label, "term": term})

    word_count = len(text.split())

    if word_count > 350:
        findings.append({"type": "FALSIFIABILITY_DENSITY_LOAD", "term": f"{word_count} words"})

    stop_types = [
        "NON_DISCONFIRMABLE_FRAMING",
        "SELF_SEALING_LOGIC",
    ]

    cool_types = [
        "UNIVERSAL_EXPLANATION_DRIFT",
        "EVIDENCE_FREE_CERTAINTY",
        "INTERPRETIVE_ELASTICITY",
        "FALSIFIABILITY_DENSITY_LOAD",
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
        print("Usage: python falsifiability_preservation_harness.py <input_file>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    status, findings, word_count = inspect_text(text)

    receipt = {
        "tool": "falsifiability_preservation_harness",
        "status": status,
        "input_file": str(input_path),
        "input_sha256": sha256_text(text),
        "word_count": word_count,
        "findings": findings,
        "boundary": "claims must remain bounded, locally testable, and disconfirmable",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "closure": "UNKNOWN -> HOLD. Break survivability, not ontology."
    }

    print("=" * 60)
    print("FALSIFIABILITY PRESERVATION HARNESS")
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
        print("No major falsifiability preservation risks detected.")

    output_path = input_path.with_suffix(".falsifiability_receipt.json")
    output_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")

    print()
    print(f"Receipt written: {output_path}")
    print("UNKNOWN -> HOLD")
    print("Break survivability, not ontology.")

if __name__ == "__main__":
    main()