import argparse
import hashlib
import json
import subprocess
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
    "does not infer inevitability",
    "does not operationalize consequence",
    "does not replace institutional review",
    "does not replace bind proof"
]


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def normalize_text(text):
    return text.lower().replace("→", "->")


def read_repo_text(paths):
    chunks = []
    missing = []

    for path in paths:
        p = Path(path)
        if not p.exists():
            missing.append(path)
            continue

        try:
            chunks.append(p.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            missing.append(path)

    return "\n".join(chunks), missing


def check_review_paths(paths):
    missing = [path for path in paths if not Path(path).exists()]

    if missing:
        return FAIL, {
            "missing_paths": missing
        }

    return PASS, {
        "missing_paths": []
    }


def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    combined = (result.stdout or "") + "\n" + (result.stderr or "")

    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "combined": combined
    }


def check_replay_commands(commands):
    results = []
    hard_fail = False
    hold = False

    for item in commands:
        result = run_command(item["command"])
        expected = item.get("expected_output_contains", "")

        output_contains_expected = expected in result["combined"]

        status = PASS

        if result["returncode"] != 0:
            status = FAIL
            hard_fail = True
        elif expected and not output_contains_expected:
            status = HOLD
            hold = True

        results.append({
            "name": item.get("name", "unnamed"),
            "command": item["command"],
            "expected_output_contains": expected,
            "output_contains_expected": output_contains_expected,
            "returncode": result["returncode"],
            "status": status
        })

    if hard_fail:
        return FAIL, results

    if hold:
        return HOLD, results

    return PASS, results


def check_required_terms(case):
    paths = case.get("required_review_paths", [])
    repo_text, missing = read_repo_text(paths)
    normalized = normalize_text(repo_text)

    required_terms = case.get("required_terms", [])
    missing_terms = []

    for term in required_terms:
        if normalize_text(term) not in normalized:
            missing_terms.append(term)

    if missing:
        return HOLD, {
            "missing_paths": missing,
            "missing_terms": missing_terms
        }

    if missing_terms:
        return HOLD, {
            "missing_paths": [],
            "missing_terms": missing_terms
        }

    return PASS, {
        "missing_paths": [],
        "missing_terms": []
    }


def check_forbidden_terms(case):
    paths = case.get("required_review_paths", [])
    repo_text, missing = read_repo_text(paths)
    normalized = normalize_text(repo_text)

    forbidden_terms = case.get("forbidden_authority_terms", [])
    hits = []

    for term in forbidden_terms:
        if normalize_text(term) in normalized:
            hits.append(term)

    if hits:
        return FAIL, {
            "forbidden_hits": hits
        }

    if missing:
        return HOLD, {
            "forbidden_hits": [],
            "missing_paths": missing
        }

    return PASS, {
        "forbidden_hits": []
    }


def evaluate(case):
    checks = {}

    path_status, path_details = check_review_paths(
        case.get("required_review_paths", [])
    )
    checks["review_path_traversability"] = {
        "status": path_status,
        "details": path_details
    }

    replay_status, replay_details = check_replay_commands(
        case.get("replay_commands", [])
    )
    checks["deterministic_replay"] = {
        "status": replay_status,
        "details": replay_details
    }

    terms_status, terms_details = check_required_terms(case)
    checks["required_stabilization_terms"] = {
        "status": terms_status,
        "details": terms_details
    }

    forbidden_status, forbidden_details = check_forbidden_terms(case)
    checks["forbidden_authority_terms"] = {
        "status": forbidden_status,
        "details": forbidden_details
    }

    statuses = [item["status"] for item in checks.values()]

    if FAIL in statuses:
        verdict = FAIL
        reason = "one_or_more_validation_checks_failed"
    elif HOLD in statuses:
        verdict = HOLD
        reason = "one_or_more_validation_checks_cannot_be_fully_reconstructed"
    else:
        verdict = PASS
        reason = "review_cycle_validation_passed"

    return verdict, reason, checks


def build_receipt(case):
    verdict, reason, checks = evaluate(case)

    receipt = {
        "case_id": case.get("case_id", "UNKNOWN"),
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "observer_only": True,
        "tool": "review_cycle_validator",
        "verdict": verdict,
        "reason": reason,
        "checks": checks,
        "non_claims": NON_CLAIMS,
        "core_locks": [
            "reviewer traversal is not authority",
            "reproducibility is not legitimacy",
            "renderer output is not proof",
            "measurement is not admissibility",
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
    json_path = outdir / f"{case_id}_review_cycle_receipt.json"
    md_path = outdir / f"{case_id}_review_cycle_receipt.md"

    json_text = json.dumps(receipt, indent=2, sort_keys=True)
    json_path.write_text(json_text, encoding="utf-8")

    md_lines = [
        f"# Review Cycle Validation Receipt: {case_id}",
        "",
        f"Timestamp UTC: {receipt['timestamp_utc']}",
        "",
        f"Verdict: {receipt['verdict']}",
        "",
        f"Reason: {receipt['reason']}",
        "",
        "## Checks",
        ""
    ]

    for name, check in receipt["checks"].items():
        md_lines.append(f"- {name}: {check['status']}")

    md_lines.extend([
        "",
        "## Non-Claims",
        ""
    ])

    for claim in NON_CLAIMS:
        md_lines.append(f"- {claim}")

    md_lines.extend([
        "",
        "## Core Locks",
        "",
        "- Reviewer traversal is not authority.",
        "- Reproducibility is not legitimacy.",
        "- Renderer output is not proof.",
        "- Measurement is not admissibility.",
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
        description="Validate v1 review cycle traversability and reproducibility."
    )
    parser.add_argument("--case", required=True, help="Path to review cycle case JSON")
    parser.add_argument(
        "--outdir",
        default="tools/review_cycle_validator/outputs",
        help="Output directory"
    )

    args = parser.parse_args()

    case = load_json(args.case)
    receipt = build_receipt(case)

    json_path, md_path = write_outputs(receipt, Path(args.outdir))

    print("Artifacts written:")
    print(f" - {json_path}")
    print(f" - {md_path}")
    print(f"Status: {receipt['verdict']}")


if __name__ == "__main__":
    main()