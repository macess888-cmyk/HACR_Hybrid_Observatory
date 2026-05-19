import json
import subprocess
from datetime import datetime, UTC
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "tools" / "observability_survivability_workbench" / "cases_index.json"
OUTDIR = ROOT / "tools" / "observability_survivability_workbench" / "outputs"


def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        cwd=ROOT,
        capture_output=True,
        text=True
    )
    combined = (result.stdout or "") + "\n" + (result.stderr or "")
    return result.returncode, combined


def extract_status(output):
    for line in output.splitlines():
        if line.startswith("Status:"):
            return line.replace("Status:", "").strip()
    return "HOLD"


def main():
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    results = []

    for case_path in index["validator_cases"]:
        command = f"python tools/review_cycle_validator/src/validator.py --case {case_path}"
        returncode, output = run_command(command)
        status = extract_status(output)

        results.append({
            "type": "validator_case",
            "path": case_path,
            "returncode": returncode,
            "status": status
        })

    for meter in index["meters"]:
        returncode, output = run_command(meter["command"])
        expected = meter["expected_output_contains"]
        status = "PASS" if returncode == 0 and expected in output else "HOLD"

        results.append({
            "type": "meter",
            "name": meter["name"],
            "returncode": returncode,
            "status": status
        })

    statuses = [item["status"] for item in results]

    if "FAIL" in statuses:
        verdict = "FAIL"
    elif "HOLD" in statuses:
        verdict = "HOLD"
    else:
        verdict = "PASS"

    receipt = {
        "workbench_id": index["workbench_id"],
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "observer_only": True,
        "verdict": verdict,
        "results": results,
        "non_claims": index["non_claims"]
    }

    OUTDIR.mkdir(parents=True, exist_ok=True)

    out = OUTDIR / "observability_survivability_workbench_receipt.json"
    out.write_text(json.dumps(receipt, indent=2), encoding="utf-8")

    print("Observability Survivability Workbench")
    print("------------------------------------")
    print(f"Verdict: {verdict}")
    print(f"Receipt: {out}")
    print("------------------------------------")
    print("Workbench output is not authority.")
    print("UNKNOWN -> HOLD.")


if __name__ == "__main__":
    main()