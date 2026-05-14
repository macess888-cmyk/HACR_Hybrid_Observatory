import json

INPUT_FILE = "Inputs/authority_surface_case.json"
OUTPUT_FILE = "Outputs/authority_surface_report.json"


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    surfaces = data.get("authority_surfaces", [])

    surviving = [
        s for s in surfaces
        if s.get("reachable_after_interruption", False)
    ]

    report = {
        "lens": "RUNTIME_DEPENDENCY_SURFACE_MAPPER",
        "surviving_runtime_dependency_surface_count": len(surviving),
        "surviving_runtime_dependency_surfaces": surviving,
        "diagnostic_boundary": (
            "observer-side runtime diagnostics only"
        ),
        "non_claims": [
            "not governance",
            "not operational authorization",
            "not runtime enforcement",
            "not certification"
        ]
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(
        "Runtime dependency surface "
        "inspection complete."
    )


if __name__ == "__main__":
    main()