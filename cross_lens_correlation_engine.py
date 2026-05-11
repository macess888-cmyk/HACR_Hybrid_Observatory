import json
from pathlib import Path

OUTPUT_DIR = Path("Outputs")

FILES = {
    "dynamic_drift": "dynamic_drift_report.json",
    "semantic_asymmetry": "semantic_asymmetry_report.json",
    "alpha_omega": "alpha_omega_report.json",
    "superposition": "superposition_report.json",
    "condition_trace": "condition_trace_report.json"
}

signals = []

for lens, filename in FILES.items():
    path = OUTPUT_DIR / filename

    if path.exists():
        with open(path, "r") as f:
            data = json.load(f)

        signals.append({
            "lens": lens,
            "status": data.get("status", "UNKNOWN")
        })

shadow_count = sum(1 for s in signals if s["status"] == "SHADOW")
unstable_count = sum(1 for s in signals if s["status"] == "UNSTABLE")
fail_count = sum(1 for s in signals if s["status"] == "FAIL")

overall = "STABLE"

if shadow_count >= 2:
    overall = "SHADOW"

if unstable_count >= 1:
    overall = "UNSTABLE"

if fail_count >= 1:
    overall = "FAIL"

report = {
    "engine": "CROSS_LENS_CORRELATION",
    "overall_status": overall,
    "signals": signals,
    "observer_mode": True,
    "non_claims": [
        "Not orchestration authority",
        "Not runtime enforcement",
        "Not proof of safety",
        "Not operational authorization"
    ]
}

OUTPUT_DIR.mkdir(exist_ok=True)

with open(OUTPUT_DIR / "cross_lens_report.json", "w") as f:
    json.dump(report, f, indent=2)

print("Inputs/cross_lens_correlation ->", overall)