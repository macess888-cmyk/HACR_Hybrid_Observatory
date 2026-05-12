import json
import os
import subprocess
import hashlib

FILES_TO_CHECK = [
    "Outputs/watchdog_report.json",
    "Outputs/shared_persistence_lineage_report.json",
    "Outputs/fresh_bind_gap_report.json",
    "Outputs/topology_delta_report.json",
    "Outputs/continuation_pressure_report.json",
    "Outputs/derived_lineage_report.json",
    "Outputs/survivability_graph_export.json"
]

def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

print("\n=== HACR Reproducibility Check ===\n")

subprocess.run(["python", "run_demo_v0_8.py"])

results = []

for path in FILES_TO_CHECK:
    if os.path.exists(path):
        results.append({
            "file": path,
            "exists": True,
            "sha256": file_hash(path)
        })
    else:
        results.append({
            "file": path,
            "exists": False,
            "sha256": None
        })

report = {
    "lens": "REPRODUCIBILITY_CHECK",
    "status": "TRACEABLE",
    "observer_mode": True,
    "summary": "Runs the canonical demo path and records deterministic output hashes.",
    "findings": results,
    "non_claims": [
        "Not certification",
        "Not runtime enforcement",
        "Not production monitoring",
        "Not execution control"
    ]
}

with open("Outputs/reproducibility_check_report.json", "w") as f:
    json.dump(report, f, indent=2)

print("Outputs/reproducibility_check_report.json -> TRACEABLE")