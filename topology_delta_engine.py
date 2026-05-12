import json
import os

INPUT_FILE = "Inputs/topology_delta_case.json"
OUTPUT_FILE = "Outputs/topology_delta_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    case = json.load(f)

pre = case.get("pre_refusal_topology", {})
post = case.get("post_refusal_topology", {})

pre_paths = set(pre.get("effect_capable_paths", []))
post_paths = set(post.get("effect_capable_paths", []))

collapsed_paths = sorted(list(pre_paths - post_paths))
surviving_paths = sorted(list(pre_paths.intersection(post_paths)))
new_paths = sorted(list(post_paths - pre_paths))

findings = []
score = 0

for path in surviving_paths:
    findings.append({
        "path": path,
        "condition": "EFFECT_CAPABLE_PATH_SURVIVED_REFUSAL",
        "severity": "CRITICAL"
    })
    score += 5

for path in new_paths:
    findings.append({
        "path": path,
        "condition": "NEW_EFFECT_CAPABLE_PATH_EMERGED_AFTER_REFUSAL",
        "severity": "HIGH"
    })
    score += 4

for path in collapsed_paths:
    findings.append({
        "path": path,
        "condition": "PATH_COLLAPSED_AFTER_REFUSAL",
        "severity": "INFO"
    })

if score >= 10:
    status = "FAIL"
elif score >= 5:
    status = "SHADOW"
elif score > 0:
    status = "HOLD"
else:
    status = "PASS"

report = {
    "lens": "TOPOLOGY_DELTA_ENGINE",
    "status": status,
    "score": score,
    "observer_mode": True,
    "summary": "Compares pre-refusal and post-refusal topology to detect surviving or newly emergent effect-capable paths.",
    "pre_refusal_paths": sorted(list(pre_paths)),
    "post_refusal_paths": sorted(list(post_paths)),
    "collapsed_paths": collapsed_paths,
    "surviving_paths": surviving_paths,
    "new_paths": new_paths,
    "findings": findings,
    "non_claims": [
        "Not runtime monitoring",
        "Not production discovery",
        "Not execution control",
        "Not certification",
        "Not prediction"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")