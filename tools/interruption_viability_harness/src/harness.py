import argparse
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASE_PATH = ROOT / "cases" / "demo_case.json"
OUTPUT_DIR = ROOT / "outputs"


def load_case(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def score_case(case: dict) -> dict:
    gv = case.get("governance_visibility", {})
    ie = case.get("interruption_executability", {})
    ch = case.get("continuation_hardening", {})

    required_fields = [
        gv.get("audit_trail_visible"),
        gv.get("review_path_visible"),
        gv.get("replay_available"),
        gv.get("escalation_path_documented"),
        ie.get("estimated_reconstruction_minutes"),
        ie.get("required_actor_count"),
        ie.get("cross_system_dependencies"),
        ie.get("human_response_window_minutes"),
        ie.get("interruption_latency_minutes"),
        ch.get("elapsed_persistence_minutes"),
        ch.get("distributed_nodes_active"),
        ch.get("rollback_complexity"),
        ch.get("ambient_dependency_density")
    ]

    if any(v is None for v in required_fields):
        return {
            "status": "HOLD",
            "reason": "Insufficient measurable runtime fields."
        }

    visible_governance = all([
        gv["audit_trail_visible"],
        gv["review_path_visible"],
        gv["replay_available"],
        gv["escalation_path_documented"]
    ])

    interruption_latency_exceeds_window = (
        ie["interruption_latency_minutes"] > ie["human_response_window_minutes"]
    )

    reconstruction_burden_high = (
        ie["estimated_reconstruction_minutes"] >= 120
        or ie["required_actor_count"] >= 6
        or ie["cross_system_dependencies"] >= 10
    )

    continuation_hardening_high = (
        ch["elapsed_persistence_minutes"] >= 180
        or ch["distributed_nodes_active"] >= 10
        or ch["rollback_complexity"] == "high"
        or ch["ambient_dependency_density"] == "high"
    )

    if (
        visible_governance
        and interruption_latency_exceeds_window
        and reconstruction_burden_high
        and continuation_hardening_high
    ):
        return {
            "status": "FAIL",
            "reason": "Visible governance persists while executable interruption capacity appears materially collapsed under measured runtime constraints."
        }

    if visible_governance and not interruption_latency_exceeds_window:
        return {
            "status": "PASS",
            "reason": "Interruption appears executable within the measured human response window."
        }

    return {
        "status": "HOLD",
        "reason": "Runtime evidence does not support PASS or FAIL."
    }


def make_receipt(case: dict, result: dict, source_case_path: Path) -> dict:
    receipt = {
        "tool": "interruption_viability_instrumentation_harness",
        "version": "0.2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_case_path": str(source_case_path),
        "case_id": case.get("case_id"),
        "result": result,
        "non_claims": [
            "Instrumentation is not authority.",
            "Measurement is not admissibility.",
            "Observability does not create interruption.",
            "Evidence does not create bind.",
            "Metrics do not create legitimacy.",
            "FAIL does not determine governance invalidity.",
            "PASS does not certify governance sufficiency.",
            "HOLD preserves unresolved runtime determination."
        ],
        "case": case
    }

    canonical = json.dumps(receipt, sort_keys=True, separators=(",", ":"))
    receipt["sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return receipt


def write_outputs(receipt: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    case_id = receipt["case_id"] or "unnamed_case"
    json_path = OUTPUT_DIR / f"{case_id}_receipt.json"
    md_path = OUTPUT_DIR / f"{case_id}_receipt.md"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Interruption Viability Harness Receipt\n\n")
        f.write(f"Case ID: `{receipt['case_id']}`\n\n")
        f.write(f"Status: **{receipt['result']['status']}**\n\n")
        f.write(f"Reason: {receipt['result']['reason']}\n\n")
        f.write(f"Source Case: `{receipt['source_case_path']}`\n\n")
        f.write(f"SHA256: `{receipt['sha256']}`\n\n")
        f.write("## Non-Claims\n\n")
        for claim in receipt["non_claims"]:
            f.write(f"- {claim}\n")

    print("Artifacts written:")
    print(f" - {json_path}")
    print(f" - {md_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Observer-only interruption viability instrumentation harness."
    )
    parser.add_argument(
        "--case",
        default=str(DEFAULT_CASE_PATH),
        help="Path to JSON case file."
    )
    return parser.parse_args()


def main():
    args = parse_args()
    case_path = Path(args.case)

    case = load_case(case_path)
    result = score_case(case)
    receipt = make_receipt(case, result, case_path)
    write_outputs(receipt)

    print(f"Status: {result['status']}")


if __name__ == "__main__":
    main()