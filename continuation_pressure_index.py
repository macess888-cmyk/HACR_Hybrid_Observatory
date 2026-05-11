import json
import os
from pathlib import Path

OUTPUT_DIR = Path("Outputs")
OUTPUT_FILE = OUTPUT_DIR / "continuation_pressure_report.json"

LENS_FILES = {
    "authority_surface": "authority_surface_report.json",
    "constructibility_collapse": "constructibility_collapse_report.json",
    "replay_vector": "replay_vector_report.json",
    "refusal_propagation": "refusal_propagation_report.json",
    "lineage_consumption": "lineage_consumption_report.json",
    "semantic_fragmentation": "semantic_fragmentation_report.json",
    "descendant_effect": "descendant_effect_report.json",
    "distributed_reconstruction": "distributed_reconstruction_report.json",
    "latent_path": "latent_path_report.json",
    "superposition": "superposition_report.json"
}

SCORES = {
    "PASS": 0,
    "HOLD": 1,
    "SHADOW": 2,
    "UNSTABLE": 3,
    "FAIL": 4
}

signals = []
pressure_score = 0

for lens, filename in LENS_FILES.items():
    path = OUTPUT_DIR / filename

    if path.exists():
        with open(path, "r") as f:
            data = json.load(f)

        status = data.get("status", "HOLD")
        score = SCORES.get(status, 1)

        pressure_score += score

        signals.append({
            "lens": lens,
            "status": status,
            "score": score
        })

max_score = len(signals) * 4
pressure_ratio = pressure_score / max_score if max_score else 0

if pressure_ratio == 0:
    pressure_state = "LOW"
elif pressure_ratio < 0.35:
    pressure_state = "MODERATE"
elif pressure_ratio < 0.70:
    pressure_state = "HIGH"
else:
    pressure_state = "CRITICAL"

report = {
    "index": "CONTINUATION_PRESSURE",
    "pressure_state": pressure_state,
    "pressure_score": pressure_score,
    "max_score": max_score,
    "pressure_ratio": round(pressure_ratio, 3),
    "signals": signals,
    "observer_mode": True,
    "non_claims": [
        "Not risk certification",
        "Not execution control",
        "Not operational authorization",
        "Not runtime enforcement"
    ]
}

OUTPUT_DIR.mkdir(exist_ok=True)

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print("Inputs/continuation_pressure_index ->", pressure_state)