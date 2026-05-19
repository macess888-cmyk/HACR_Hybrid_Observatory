import argparse
import hashlib
import json
from datetime import datetime, UTC
from pathlib import Path


PASS = "PASS"
HOLD = "HOLD"
FAIL = "FAIL"


NON_CLAIMS = [
    "does not govern",
    "does not authorize",
    "does not adjudicate",
    "does not certify",
    "does not determine legitimacy",
    "does not infer political truth",
    "does not infer hidden authority",
    "does not infer inevitability",
    "does not operationalize consequence",
    "does not replace institutional authority",
    "does not replace bind proof"
]


SEMANTIC_DRIFT_TERMS = [
    "illegitimate",
    "corrupt",
    "conspiracy",
    "hidden authority",
    "inevitable",
    "destiny",
    "institutional failure",
    "political truth",
    "proof of failure",
    "governance truth",
    "finality"
]


REQUIRED_FIELDS = [
    "governance_visibility_present",
    "oversight_channel_visible",
    "review_body_exists",
    "interruption_surface_known",
    "interruption_surface_reachable",
    "interruption_authority_executable",
    "escalation_path_connected_to_interruption",
    "time_to_consequence_hardening",
    "time_to_review_activation",
    "time_to_interruption_execution"
]


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_case(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_semantic_drift(text):
    lowered = text.lower()
    hits = []

    for term in SEMANTIC_DRIFT_TERMS:
        if term in lowered:
            hits.append(term)

    return hits


def evaluate_case(case):
    missing = [field for field in REQUIRED_FIELDS if field not in case]

    if missing:
        return HOLD, f"missing_required_fields:{','.join(missing)}"

    visible_governance = (
        case["governance_visibility_present"]
        or case["oversight_channel_visible"]
        or case["review_body_exists"]
    )

    interruption_materially_connected = (
        case["interruption_surface_known"]
        and case["interruption_surface_reachable"]
        and case["interruption_authority_executable"]
        and case["escalation_path_connected_to_interruption"]
    )

    timing_viable = (
        case["time_to_review_activation"] <= case["time_to_consequence_hardening"]
        and case["time_to_interruption_execution"] <= case["time_to_consequence_hardening"]
    )

    if not visible_governance:
        return HOLD, "governance_visibility_not_established"

    if visible_governance and not interruption_materially_connected:
        return FAIL, "visible_governance_without_material_interruption_connection"

    if interruption_materially_connected and not timing_viable:
        return FAIL, "interruption_path_exists_but_not_in_time"

    if interruption_materially_connected and timing_viable:
        return PASS, "visible_governance_connected_to_executable_interruption"

    return HOLD, "conditions_not_materially_reconstructable"


def build_receipt(case):
    semantic_hits = detect_semantic_drift(case.get("semantic_input", ""))

    if semantic_hits:
        verdict = HOLD
        reason = "semantic_drift_detected"
    else:
        verdict, reason = evaluate_case(case)

    receipt = {
        "case_id": case.get("case_id", "UNKNOWN"),
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "observer_only": True,
        "harness": "governance_theater_survivability",
        "verdict": verdict,
        "reason": reason,
        "semantic_drift_hits": semantic_hits,
        "inputs": case,
        "non_claims": NON_CLAIMS,
        "verdict_semantics": {
            "PASS": "visible governance remains materially connected to executable interruption",
            "HOLD": "conditions cannot be materially measured, reconstructed, or falsified",
            "FAIL": "governance visibility survives while executable interruption capability is absent, delayed, disconnected, or practically unreachable"
        },
        "core_locks": [
            "governance visibility is not interruption capability",
            "oversight visibility is not executable interruption",
            "persistence is not legitimacy",
            "asymmetry does not imply destiny",
            "UNKNOWN -> HOLD",
            "break survivability, not ontology"
        ]
    }

    receipt_text = json.dumps(receipt, indent=2, sort_keys=True)
    receipt["receipt_sha256"] = sha256_text(receipt_text)

    return receipt


def write_outputs(receipt, outdir):
    outdir.mkdir(parents=True, exist_ok=True)

    case_id = receipt["case_id"]
    json_path = outdir / f"{case_id}_receipt.json"
    md_path = outdir / f"{case_id}_receipt.md"

    json_text = json.dumps(receipt, indent=2, sort_keys=True)
    json_path.write_text(json_text, encoding="utf-8")

    md_lines = [
        f"# Governance Theater Survivability Receipt: {case_id}",
        "",
        f"Timestamp UTC: {receipt['timestamp_utc']}",
        "",
        f"Verdict: {receipt['verdict']}",
        "",
        f"Reason: {receipt['reason']}",
        "",
        "## Semantic Drift Hits",
        "",
        ", ".join(receipt["semantic_drift_hits"]) if receipt["semantic_drift_hits"] else "None",
        "",
        "## Non-Claims",
        ""
    ]

    for claim in NON_CLAIMS:
        md_lines.append(f"- {claim}")

    md_lines.extend([
        "",
        "## Core Locks",
        "",
        "- Governance visibility is not interruption capability.",
        "- Oversight visibility is not executable interruption.",
        "- Persistence is not legitimacy.",
        "- Asymmetry does not imply destiny.",
        "- UNKNOWN -> HOLD.",
        "- Break survivability, not ontology.",
        "",
        f"Receipt SHA256: {receipt['receipt_sha256']}",
        ""
    ])

    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    return json_path, md_path


def main():
    parser = argparse.ArgumentParser(
        description="Governance Theater Survivability Harness"
    )
    parser.add_argument("--case", required=True, help="Path to case JSON")
    parser.add_argument(
        "--outdir",
        default="harnesses/governance_theater_survivability/outputs",
        help="Output directory"
    )

    args = parser.parse_args()

    case = load_case(Path(args.case))
    receipt = build_receipt(case)

    json_path, md_path = write_outputs(receipt, Path(args.outdir))

    print("Artifacts written:")
    print(f" - {json_path}")
    print(f" - {md_path}")
    print(f"Status: {receipt['verdict']}")


if __name__ == "__main__":
    main()