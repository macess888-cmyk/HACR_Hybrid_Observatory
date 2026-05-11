import json
import os

INPUT_FILE = "Inputs/authority_surface_case.json"
OUTPUT_FILE = "Outputs/authority_surface_report.json"

os.makedirs("Outputs", exist_ok=True)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

surfaces = data.get("authority_surfaces", [])

surviving = []
status = "PASS"

for surface in surfaces:
    if surface.get("survives_refusal") is True:
        surviving.append({
            "surface_id": surface.get("surface_id"),
            "surface_type": surface.get("surface_type"),
            "authority_source": surface.get("authority_source"),
            "risk": "authority surface survives refusal"
        })

if surviving:
    status = "SHADOW"

if any(s.get("authority_source") == "prior_state" for s in surviving):
    status = "FAIL"

report = {
    "lens": "AUTHORITY_SURFACE_MAPPER",
    "status": status,
    "surviving_authority_surface_count": len(surviving),
    "surviving_authority_surfaces": surviving,
    "observer_mode": True,
    "non_claims": [
        "Not authority validation",
        "Not execution authorization",
        "Not runtime enforcement",
        "Not certification"
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"{INPUT_FILE} -> {status}")