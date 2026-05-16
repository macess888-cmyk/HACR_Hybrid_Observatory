import json
from pathlib import Path
from datetime import datetime, timezone
import hashlib

ROOT = Path(__file__).resolve().parents[2]
CASES_DIR = ROOT / "harness" / "cases"
OUTPUTS_DIR = ROOT / "harness" / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def classify(case):
    topology = case.get("topology_visibility")
    hidden = case.get("hidden_carriers")
    survivability = case.get("continuation_survivability")
    interruption = case.get("interruption_locality")
    incorrect = case.get("incorrect_assertion")
    replayability = case.get("replayability")
    operational_memory = case.get("operational_memory")
    stale_state = case.get("stale_state")
    observable_calm = case.get("observable_calm")
    fragmented = case.get("fragmented_continuation")

    if incorrect == "PASS" and topology == "incomplete":
        return "HOLD"

    if hidden is True or survivability is True:
        return "FAIL"

    if fragmented is True:
        return "FAIL"

    if observable_calm is True and hidden is True:
        return "FAIL"

    if operational_memory == "survives" or stale_state is True:
        return "FAIL"

    if topology == "incomplete":
        return "HOLD"

    if hidden == "unknown" or survivability == "unknown" or interruption == "uncertain":
        return "HOLD"

    if replayability in ("partial", "ambiguous", "unknown"):
        return "HOLD"

    if topology == "partial" and hidden == "unknown":
        return "HOLD"

    if topology == "sufficient" and hidden is False and survivability is False and interruption == "reachable":
        return "PASS"

    return "HOLD"


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    results = []

    for path in sorted(CASES_DIR.glob("*.json")):
        raw = path.read_text(encoding="utf-8")
        case = json.loads(raw)

        observed = classify(case)
        expected = case.get("expected_state")
        matched = observed == expected

        result = {
            "case_file": path.name,
            "case": case.get("case"),
            "expected_state": expected,
            "observed_state": observed,
            "matched_expected": matched,
            "case_sha256": sha256_text(raw),
        }
        results.append(result)

    receipt = {
        "harness": "HACR Minimal Replay Harness",
        "mode": "observer_side_diagnostic",
        "authority": "non_authoritative",
        "execution_consumable": False,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "case_count": len(results),
        "results": results,
    }

    receipt_body = json.dumps(receipt, indent=2, sort_keys=True)
    receipt["receipt_sha256"] = sha256_text(receipt_body)

    output = OUTPUTS_DIR / "latest_harness_receipt.json"
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True), encoding="utf-8")

    print("HACR Minimal Replay Harness")
    print("--------------------------------")
    for item in results:
        status = "OK" if item["matched_expected"] else "MISMATCH"
        print(
            f'{item["case"]}: expected={item["expected_state"]} '
            f'observed={item["observed_state"]} [{status}]'
        )

    print("--------------------------------")
    print(f"Receipt written: {output}")
    print(f'Receipt SHA256: {receipt["receipt_sha256"]}')


if __name__ == "__main__":
    main()