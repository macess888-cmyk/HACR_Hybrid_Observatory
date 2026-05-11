import json
from pathlib import Path

INPUT = Path("Inputs/lineage_consumption_case.json")
OUTPUT = Path("Outputs/lineage_consumption_report.json")

def main():
    data = json.loads(INPUT.read_text())

    surfaces = data.get("lineage_surfaces", [])
    failures = []

    for s in surfaces:
        if s.get("survives_refusal") and not s.get("consumed"):
            failures.append({
                "surface_id": s.get("surface_id"),
                "surface_type": s.get("surface_type"),
                "risk": "lineage survives refusal without consumption"
            })

    status = "FAIL" if failures else "PASS"

    report = {
        "lens": "LINEAGE_CONSUMPTION_AUDITOR",
        "status": status,
        "unconsumed_lineage_count": len(failures),
        "unconsumed_lineage": failures,
        "observer_mode": True,
        "non_claims": [
            "Not execution control",
            "Not proof of global collapse",
            "Not runtime enforcement",
            "Not certification"
        ]
    }

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2))
    print(f"{INPUT} -> {status}")

if __name__ == "__main__":
    main()