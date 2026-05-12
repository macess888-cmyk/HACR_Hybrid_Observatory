"""
HACR Hybrid Observatory
Reviewer Minimal Demo Entrypoint

Purpose:
Run the minimal bounded observer-side inspection path.

This script does not:
- authorize execution
- enforce governance
- coordinate runtime behavior
- certify systems
- prove global consequence extinction

It only provides a simple reviewer entrypoint for deterministic inspection.
"""

import subprocess
import sys
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    run_all = root / "run_all.py"

    print("HACR Hybrid Observatory — Reviewer Minimal Demo")
    print("Boundary: observer-only / deterministic / non-authoritative")
    print("Running: python run_all.py")
    print("-" * 60)

    if not run_all.exists():
        print("ERROR: run_all.py not found.")
        return 1

    result = subprocess.run(
        [sys.executable, str(run_all)],
        cwd=root,
        text=True
    )

    print("-" * 60)
    print("Reviewer note:")
    print("Outputs are bounded inspection artifacts only.")
    print("Do not interpret results as enforcement, certification, or runtime authority.")

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())