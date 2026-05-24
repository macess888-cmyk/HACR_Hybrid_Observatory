import sys
from pathlib import Path

AUTHORITY_TERMS = [
    "necessary",
    "must",
    "inevitable",
    "destiny",
    "required",
    "authoritative",
    "unavoidable",
    "civilization-scale governance",
]

ONTOLOGY_TERMS = [
    "universal truth",
    "hidden reality",
    "ultimate structure",
    "complete model",
    "totalizing",
]

SHADOW_RISK_TERMS = [
    "hidden control",
    "secret system",
    "conspiracy",
    "invisible rulers",
]

def inspect_text(text):
    findings = []

    for term in AUTHORITY_TERMS:
        if term.lower() in text.lower():
            findings.append(("AUTHORITY_DRIFT", term))

    for term in ONTOLOGY_TERMS:
        if term.lower() in text.lower():
            findings.append(("ONTOLOGY_DRIFT", term))

    for term in SHADOW_RISK_TERMS:
        if term.lower() in text.lower():
            findings.append(("SHADOW_MYTHOLOGY_RISK", term))

    density_score = len(text.split())

    if density_score > 400:
        findings.append(("DENSITY_LOAD", f"{density_score} words"))

    if findings:
        if any(f[0] == "ONTOLOGY_DRIFT" for f in findings):
            status = "STOP"
        elif any(f[0] == "AUTHORITY_DRIFT" for f in findings):
            status = "COOL"
        else:
            status = "HOLD"
    else:
        status = "PASS"

    return status, findings

def main():
    if len(sys.argv) != 2:
        print("Usage: python semantic_cooling_auditor.py <input_file>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")

    status, findings = inspect_text(text)

    print("=" * 60)
    print("SEMANTIC COOLING AUDITOR")
    print("=" * 60)
    print(f"STATUS: {status}")
    print()

    if findings:
        print("FINDINGS:")
        for finding_type, detail in findings:
            print(f"- {finding_type}: {detail}")
    else:
        print("No major semantic survivability risks detected.")

    print()
    print("UNKNOWN -> HOLD")
    print("Break survivability, not ontology.")

if __name__ == "__main__":
    main()