import json
import os

INPUT_FILE = "Inputs/shared_persistence_lineage_case.json"
OUTPUT_FILE = "Outputs/shared_persistence_lineage_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    case = json.load(f)

paths = case.get("paths", [])
shared_surfaces = case.get("shared_persistence_surfaces", [])

findings = []
score = 0

for path in paths:
    name = path.get("name")
    role = path.get("role")
    persistence = set(path.get("persistence", []))
    fresh_bind_required = path.get("fresh_bind_required", False)

    for other in paths:
        if other is path:
            continue

        other_name = other.get("name")
        other_role = other.get("role")
        other_persistence = set(other.get("persistence", []))

        overlap = persistence.intersection(other_persistence)

        if overlap:
            finding = {
                "path": name,
                "role": role,
                "shares_with": other_name,
                "shares_with_role": other_role,
                "shared_persistence": sorted(list(overlap)),
                "fresh_bind_required": fresh_bind_required,
                "lineage_risk": "HIGH" if not fresh_bind_required else "ELEVATED"
            }

            findings.append(finding)

            if not fresh_bind_required:
                score += 4
            else:
                score += 2

for surface in shared_surfaces:
    if surface.get("used_by_refusal_path") and surface.get("used_by_forward_path"):
        findings.append({
            "surface": surface.get("name"),
            "condition": "REFUSAL_AND_FORWARD_SHARE_PERSISTENCE",
            "lineage_risk": "CRITICAL"
        })
        score += 5

if score >= 10:
    status = "FAIL"
elif score >= 5:
    status = "SHADOW"
elif score > 0:
    status = "HOLD"
else:
    status = "PASS"

report = {
    "lens": "SHARED_PERSISTENCE_LINEAGE",
    "status": status,
    "score": score,
    "observer_mode": True,
    "summary": "Detects shared persistence lineage between refusal, retry, recovery, and forward execution paths.",
    "findings": findings,
    "non_claims": [
        "Not runtime monitoring",
        "Not queue instrumentation",
        "Not production discovery",
        "Not execution control",
        "Not certification"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")