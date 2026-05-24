import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TOOLS = [
    ROOT / "tools" / "semantic_cooling_auditor" / "semantic_cooling_auditor.py",
    ROOT / "tools" / "visual_authority_drift_harness" / "visual_authority_drift_harness.py",
    ROOT / "tools" / "recursive_importance_drift_auditor" / "recursive_importance_drift_auditor.py",
    ROOT / "tools" / "falsifiability_preservation_harness" / "falsifiability_preservation_harness.py",
    ROOT / "tools" / "external_interpretation_risk_scanner" / "external_interpretation_risk_scanner.py",
]

TARGETS_FILE = Path(__file__).with_name("targets.txt")

def main():
    if not TARGETS_FILE.exists():
        print(f"Missing targets file: {TARGETS_FILE}")
        sys.exit(1)

    targets = [
        ROOT / line.strip()
        for line in TARGETS_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    print("=" * 60)
    print("COOLING STACK RUNNER")
    print("=" * 60)

    for target in targets:
        if not target.exists():
            print(f"\nSKIP missing target: {target}")
            continue

        print(f"\nTARGET: {target.relative_to(ROOT)}")

        for tool in TOOLS:
            if not tool.exists():
                print(f"  SKIP missing tool: {tool.relative_to(ROOT)}")
                continue

            print(f"\n--- {tool.parent.name} ---")
            subprocess.run([sys.executable, str(tool), str(target)], cwd=ROOT)

    print("\nUNKNOWN -> HOLD")
    print("Break survivability, not ontology.")

if __name__ == "__main__":
    main()