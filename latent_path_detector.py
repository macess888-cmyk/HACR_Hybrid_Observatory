import json
import os

INPUT_FILE = "Inputs/latent_path_case.json"
OUTPUT_FILE = "Outputs/latent_path_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

declared_paths = data.get("declared_paths", [])
shared_surfaces = data.get("shared_surfaces", [])

latent_paths = []
status = "PASS"

for surface in shared_surfaces:
    if surface.get("connects_forward") and surface.get("connects_reversal"):
        latent_paths.append({
            "surface_id": surface.get("surface_id"),
            "latent_path": "forward_to_reversal_bridge",
            "effect_capable": surface.get("effect_capable", False),
            "reason": "shared surface connects forward and reversal paths"
        })

    if surface.get("connects_retry") and surface.get("connects_cache"):
        latent_paths.append({
            "surface_id": surface.get("surface_id"),
            "latent_path": "retry_cache_reconstruction",
            "effect_capable": surface.get("effect_capable", False),
            "reason": "retry and cache surfaces may reconstruct continuation"
        })

if latent_paths:
    status = "HOLD"

if any(path.get("effect_capable") for path in latent_paths):
    status = "SHADOW"

report = {
    "lens": "LATENT_PATH_DETECTOR",
    "status": status,
    "declared_path_count": len(declared_paths),
    "latent_path_count": len(latent_paths),
    "latent_paths": latent_paths,
    "observer_mode": True,
    "non_claims": [
        "Not proof of hidden execution",
        "Not runtime enforcement",
        "Not execution authorization",
        "Not certification"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")