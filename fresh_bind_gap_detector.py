import json
import os

INPUT_FILE = "Inputs/fresh_bind_gap_case.json"
OUTPUT_FILE = "Outputs/fresh_bind_gap_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    case = json.load(f)

paths = case.get("continuation_paths", [])

findings = []
score = 0

for path in paths:
    name = path.get("name")
    path_type = path.get("type")
    continuation_after_refusal = path.get("continuation_after_refusal", False)
    fresh_bind_required = path.get("fresh_bind_required", False)
    fresh_bind_enforced = path.get("fresh_bind_enforced", False)
    carries_prior_authority = path.get("carries_prior_authority", False)

    if continuation_after_refusal and not fresh_bind_required:
        findings.append({
            "path": name,
            "type": path_type,
            "condition": "CONTINUATION_WITHOUT_FRESH_BIND_REQUIREMENT",
            "severity": "CRITICAL"
        })
        score += 5

    if fresh_bind_required and not fresh_bind_enforced:
        findings.append({
            "path": name,
            "type": path_type,
            "condition": "FRESH_BIND_DECLARED_BUT_NOT_ENFORCED",
            "severity": "HIGH"
        })
        score += 4

    if carries_prior_authority:
        findings.append({
            "path": name,
            "type": path_type,
            "condition": "PRIOR_AUTHORITY_CARRIED_FORWARD",
            "severity": "HIGH"
        })
        score += 4

if score >= 10:
    status = "FAIL"
elif score >= 5:
    status = "SHADOW"
elif score > 0:
    status = "HOLD"
else:
    status = "PASS"

report = {
    "lens": "FRESH_BIND_GAP_DETECTOR",
    "status": status,
    "score": score,
    "observer_mode": True,
    "summary": "Detects continuation paths that survive refusal without mandatory fresh bind revalidation.",
    "findings": findings,
    "non_claims": [
        "Not runtime enforcement",
        "Not production monitoring",
        "Not authorization",
        "Not certification",
        "Not execution control"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")