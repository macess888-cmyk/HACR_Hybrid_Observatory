import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"


RISK_TERMS = {
    "inevitable": "inevitability semantics",
    "guarantees": "closure semantics",
    "proves legitimacy": "legitimacy inheritance",
    "authority": "authority inheritance",
    "destiny": "destiny semantics",
    "autonomous": "agency implication",
    "self-preserving": "hidden agency",
    "control": "governance implication"
}


CONTAINMENT_TERMS = [
    "does not independently prove",
    "measurable",
    "unknown -> hold",
    "observer-restricted",
    "runtime conditions",
    "falsifiable"
]


def load_case(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def inspect_text(lines):
    joined = " ".join(lines).lower()

    risks = []
    containment_hits = []

    for term, reason in RISK_TERMS.items():
        if term in joined:
            risks.append({
                "term": term,
                "reason": reason
            })

    for term in CONTAINMENT_TERMS:
        if term in joined:
            containment_hits.append(term)

    if risks and not containment_hits:
        return {
            "status": "FAIL",
            "reason": "Language appears to inherit inevitability, legitimacy, authority, or closure semantics.",
            "risks": risks
        }

    if risks and containment_hits:
        return {
            "status": "HOLD",
            "reason": "Potential semantic drift detected but containment language remains present.",
            "risks": risks,
            "containment_terms": containment_hits
        }

    return {
        "status": "PASS",
        "reason": "Language remains semantically bounded to runtime-local measurement conditions.",
        "containment_terms": containment_hits
    }


def build_receipt(case, result, source_path):
    receipt = {
        "tool": "semantic_survivability_gravity_harness",
        "version": "0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_case_path": str(source_path),
        "case_id": case["case_id"],
        "result": result,
        "non_claims": [
            "Instrumentation is not authority.",
            "Semantic inspection is not legitimacy.",
            "Measurement is not governance.",
            "Persistence is not closure.",
            "Replayability is not admissibility.",
            "UNKNOWN -> HOLD remains valid under unresolved semantic conditions."
        ]
    }

    canonical = json.dumps(receipt, sort_keys=True).encode("utf-8")
    receipt["sha256"] = hashlib.sha256(canonical).hexdigest()

    return receipt


def write_outputs(receipt):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    case_id = receipt["case_id"]

    json_path = OUTPUT_DIR / f"{case_id}_receipt.json"
    md_path = OUTPUT_DIR / f"{case_id}_receipt.md"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Semantic Survivability Gravity Receipt\n\n")
        f.write(f"Case ID: `{case_id}`\n\n")
        f.write(f"Status: **{receipt['result']['status']}**\n\n")
        f.write(f"Reason: {receipt['result']['reason']}\n\n")
        f.write(f"SHA256: `{receipt['sha256']}`\n")

    print("Artifacts written:")
    print(f" - {json_path}")
    print(f" - {md_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True)

    args = parser.parse_args()

    case_path = Path(args.case)

    case = load_case(case_path)

    result = inspect_text(case["text"])

    receipt = build_receipt(case, result, case_path)

    write_outputs(receipt)

    print(f"Status: {result['status']}")


if __name__ == "__main__":
    main()