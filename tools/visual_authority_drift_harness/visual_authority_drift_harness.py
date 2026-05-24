import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

VISUAL_AUTHORITY_TERMS = [
    "complete map",
    "total view",
    "reveals",
    "hidden structure",
    "master map",
    "final diagram",
    "definitive",
    "proves",
    "truth",
]

PREDICTION_TERMS = [
    "predicts",
    "inevitable path",
    "will happen",
    "future certainty",
    "guaranteed outcome",
]

GOVERNANCE_DRIFT_TERMS = [
    "must respond",
    "should govern",
    "policy engine",
    "decision engine",
    "control interface",
    "management system",
]

SHADOW_RISK_TERMS = [
    "hidden control",
    "secret system",
    "invisible rulers",
    "shadow government",
    "hidden power",
]

CIVILIZATION_TOTALIZATION_TERMS = [
    "civilization-scale",
    "entire society",
    "all systems",
    "everything connects",
    "total system",
]

def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def inspect_text(text):
    findings = []
    lowered = text.lower()

    checks = [
        ("VISUAL_AUTHORITY_DRIFT", VISUAL_AUTHORITY_TERMS),
        ("PREDICTION_DRIFT", PREDICTION_TERMS),
        ("GOVERNANCE_DRIFT", GOVERNANCE_DRIFT_TERMS),
        ("SHADOW_MYTHOLOGY_RISK", SHADOW_RISK_TERMS),
        ("CIVILIZATION_TOTALIZATION", CIVILIZATION_TOTALIZATION_TERMS),
    ]

    for label, terms in checks:
        for term in terms:
            if term.lower() in lowered:
                findings.append({"type": label, "term": term})

    word_count = len(text.split())

    if word_count > 250:
        findings.append({"type": "VISUAL_DENSITY_LOAD", "term": f"{word_count} words"})

    if any(f["type"] in ["SHADOW_MYTHOLOGY_RISK", "PREDICTION_DRIFT"] for f in findings):
        status = "STOP"
    elif any(f["type"] in ["VISUAL_AUTHORITY_DRIFT", "GOVERNANCE_DRIFT", "CIVILIZATION_TOTALIZATION"] for f in findings):
        status = "COOL"
    elif findings:
        status = "HOLD"
    else:
        status = "PASS"

    return status, findings, word_count

def main():
    if len(sys.argv) != 2:
        print("Usage: python visual_authority_drift_harness.py <input_file>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    status, findings, word_count = inspect_text(text)

    receipt = {
        "tool": "visual_authority_drift_harness",
        "status": status,
        "input_file": str(input_path),
        "input_sha256": sha256_text(text),
        "word_count": word_count,
        "findings": findings,
        "boundary": "visual artifacts are observer-only, supplemental, non-authoritative, non-predictive",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "closure": "UNKNOWN -> HOLD. Break survivability, not ontology."
    }

    print("=" * 60)
    print("VISUAL AUTHORITY DRIFT HARNESS")
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
        print("No major visual authority drift detected.")

    output_path = input_path.with_suffix(".visual_authority_receipt.json")
    output_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")

    print()
    print(f"Receipt written: {output_path}")
    print("UNKNOWN -> HOLD")
    print("Break survivability, not ontology.")

if __name__ == "__main__":
    main()