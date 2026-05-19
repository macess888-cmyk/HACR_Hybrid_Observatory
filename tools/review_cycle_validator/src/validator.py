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


CORE_LOCKS = [
    "reviewer traversal is not authority",
    "reproducibility is not legitimacy",
    "renderer output is not proof",
    "measurement is not admissibility",
    "UNKNOWN -> HOLD",
    "break survivability, not ontology"
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
        return FAIL, {"missing_paths": missing}

    return PASS, {"missing_paths": []}


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

    missing_terms = []

    for term in case.get("required_terms", []):
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

    hits = []

    for term in case.get("forbidden_authority_terms", []):
        if normalize_text(term) in normalized:
            hits.append(term)

    if hits:
        return FAIL, {"forbidden_hits": hits}

    if missing:
        return HOLD, {
            "forbidden_hits": [],
            "missing_paths": missing
        }

    return PASS, {"forbidden_hits": []}


def check_gitignored_outputs():
    required_ignores = {
        "tools/review_cycle_validator/.gitignore": [
            "outputs/*.json",
            "outputs/*.md"
        ],
        "harnesses/governance_theater_survivability/.gitignore": [
            "outputs/*.json",
            "outputs/*.md"
        ],
        "visualization/runtime_human_reachability/renderer/.gitignore": [
            "outputs/*.svg",
            "outputs/*.json"
        ]
    }

    missing_files = []
    missing_patterns = {}

    for path, patterns in required_ignores.items():
        p = Path(path)

        if not p.exists():
            missing_files.append(path)
            continue

        text = p.read_text(encoding="utf-8", errors="ignore")

        for pattern in patterns:
            if pattern not in text:
                missing_patterns.setdefault(path, []).append(pattern)

    if missing_files or missing_patterns:
        return HOLD, {
            "missing_gitignore_files": missing_files,
            "missing_patterns": missing_patterns
        }

    return PASS, {
        "missing_gitignore_files": [],
        "missing_patterns": {}
    }


def check_validator_self_containment(case):
    paths = [
        "tools/review_cycle_validator/README.md",
        "tools/review_cycle_validator/NON_CLAIMS.md",
        "tools/review_cycle_validator/src/validator.py"
    ]

    repo_text, missing = read_repo_text(paths)
    normalized = normalize_text(repo_text)

    required_phrases = [
        "does not govern",
        "does not authorize",
        "does not certify",
        "does not determine legitimacy",
        "UNKNOWN -> HOLD",
        "break survivability, not ontology"
    ]

    missing_phrases = []

    for phrase in required_phrases:
        if normalize_text(phrase) not in normalized:
            missing_phrases.append(phrase)

    if missing or missing_phrases:
        return HOLD, {
            "missing_paths": missing,
            "missing_phrases": missing_phrases
        }

    return PASS, {
        "missing_paths": [],
        "missing_phrases": []
    }


def check_stress_bounds(case):
    stress = case.get("stress_checks", {})

    max_review_paths = stress.get("max_review_path_count")
    max_replay_commands = stress.get("max_replay_command_count")

    review_paths = case.get("required_review_paths", [])
    replay_commands = case.get("replay_commands", [])

    violations = []

    if max_review_paths is not None and len(review_paths) > max_review_paths:
        violations.append(
            f"review_path_count_exceeds_bound:{len(review_paths)}>{max_review_paths}"
        )

    if max_replay_commands is not None and len(replay_commands) > max_replay_commands:
        violations.append(
            f"replay_command_count_exceeds_bound:{len(replay_commands)}>{max_replay_commands}"
        )

    if violations:
        return HOLD, {"bound_violations": violations}

    return PASS, {"bound_violations": []}


def check_receipt_generation(receipt_preview):
    required_keys = [
        "case_id",
        "timestamp_utc",
        "observer_only",
        "tool",
        "verdict",
        "reason",
        "checks",
        "non_claims",
        "core_locks"
    ]

    missing = [key for key in required_keys if key not in receipt_preview]

    if missing:
        return HOLD, {"missing_receipt_keys": missing}

    return PASS, {"missing_receipt_keys": []}


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

    if case.get("stress_checks"):
        gitignore_status, gitignore_details = check_gitignored_outputs()
        checks["gitignored_output_containment"] = {
            "status": gitignore_status,
            "details": gitignore_details
        }

        self_status, self_details = check_validator_self_containment(case)
        checks["validator_self_containment"] = {
            "status": self_status,
            "details": self_details
        }

        bounds_status, bounds_details = check_stress_bounds(case)
        checks["stress_bounds"] = {
            "status": bounds_status,
            "details": bounds_details
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
        "core_locks": CORE_LOCKS
    }

    receipt_status, receipt_details = check_receipt_generation(receipt)
    receipt["checks"]["receipt_generation_shape"] = {
        "status": receipt_status,
        "details": receipt_details
    }

    if receipt_status == HOLD and receipt["verdict"] == PASS:
        receipt["verdict"] = HOLD
        receipt["reason"] = "receipt_generation_shape_cannot_be_fully_reconstructed"

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
        ""
    ])

    for lock in CORE_LOCKS:
        md_lines.append(f"- {lock}.")

    md_lines.extend([
        "",
        f"Receipt SHA256: {receipt['receipt_sha256']}",
        ""
    ])

    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    return json_path, md_path


def main():
    parser = argparse.ArgumentParser(
        description="Validate review cycle traversability, reproducibility, and containment."
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