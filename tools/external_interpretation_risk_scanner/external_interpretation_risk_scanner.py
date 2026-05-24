import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

CONSPIRACY_RISK_TERMS = [
    "hidden system",
    "hidden control",
    "secret network",
    "shadow government",
    "invisible rulers",
    "they control",
    "behind everything",
]

PREDICTION_ENGINE_TERMS = [
    "predicts the future",
    "inevitable future",
    "future path",
    "will happen",
    "guaranteed outcome",
    "destined",
]

GOVERNANCE_AUTHORITY_TERMS = [
    "society must follow",
    "must govern",
    "governance authority",
    "policy engine",
    "decision authority",
    "control layer",
    "intervention logic",
]

IDEOLOGY_DOCTRINE_TERMS = [
    "doctrine",
    "movement",
    "belief system",
    "truth system",
    "worldview",
    "the only way",
]

TOTALIZATION_TERMS = [
    "civilization-scale governance",
    "all systems",
    "everything connects",
    "total view",
    "universal explanation",
    "complete explanation",
]

SURVIVAL_PRESSURE_TERMS = [
    "to survive",
    "save civilization",
    "humanity depends",
    "civilization depends",
    "species survival",
]

def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def inspect_text(text):
    findings = []
    lowered = text.lower()

    checks = [
        ("CONSPIRACY_MISREAD_RISK", CONSPIRACY_RISK_TERMS),
        ("PREDICTION_ENGINE_MISREAD_RISK", PREDICTION_ENGINE_TERMS),
        ("GOVERNANCE_AUTHORITY_MISREAD_RISK", GOVERNANCE_AUTHORITY_TERMS),
        ("IDEOLOGY_DOCTRINE_MISREAD_RISK", IDEOLOGY_DOCTRINE_TERMS),
        ("TOTALIZATION_MISREAD_RISK", TOTALIZATION_TERMS),
        ("SURVIVAL_PRESSURE_MISREAD_RISK", SURVIVAL_PRESSURE_TERMS),
    ]

    for label, terms in checks:
        for term in terms:
            if term.lower() in lowered:
                findings.append({"type": label, "term": term})

    word_count = len(text.split())

    if word_count > 300:
        findings.append({"type": "PUBLIC_DENSITY_LOAD", "term": f"{word_count} words"})

    stop_types = [
        "CONSPIRACY_MISREAD_RISK",
        "PREDICTION_ENGINE_MISREAD_RISK",
        "GOVERNANCE_AUTHORITY_MISREAD_RISK",
    ]

    cool_types = [
        "IDEOLOGY_DOCTRINE_MISREAD_RISK",
        "TOTALIZATION_MISREAD_RISK",
        "SURVIVAL_PRESSURE_MISREAD_RISK",
        "PUBLIC_DENSITY_LOAD",
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
        print("Usage: python external_interpretation_risk_scanner.py <input_file>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    status, findings, word_count = inspect_text(text)

    receipt = {
        "tool": "external_interpretation_risk_scanner",
        "status": status,
        "input_file": str(input_path),
        "input_sha256": sha256_text(text),
        "word_count": word_count,
        "findings": findings,
        "boundary": "public interpretation risk is diagnostic only and does not determine intent or truth",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "closure": "UNKNOWN -> HOLD. Break survivability, not ontology."
    }

    print("=" * 60)
    print("EXTERNAL INTERPRETATION RISK SCANNER")
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
        print("No major external interpretation risks detected.")

    output_path = input_path.with_suffix(".external_interpretation_receipt.json")
    output_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")

    print()
    print(f"Receipt written: {output_path}")
    print("UNKNOWN -> HOLD")
    print("Break survivability, not ontology.")

if __name__ == "__main__":
    main()