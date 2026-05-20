import json
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = [
    "README.md",
    "START_HERE.md",
    "RUN_DEMO.bat",
    "RUN_STABILIZATION_AUDIT.bat",
    "tools/recovery_case_pack_renderer/batch_recovery_case_runner.py",
    "tools/recovery_case_pack_renderer/batch_svg_renderer.py",
    "tools/stabilization_cycle_auditor/stabilization_cycle_auditor.py",
]

EXPECTED_OUTPUTS = [
    "tools/recovery_case_pack_renderer/outputs/case_001_green_surface_dead_recovery_output.json",
    "tools/recovery_case_pack_renderer/outputs/case_002_visible_not_traversable_output.json",
    "tools/recovery_case_pack_renderer/outputs/case_003_interrupted_not_recovered_output.json",
    "tools/recovery_case_pack_renderer/outputs/case_004_seen_not_protected_output.json",
]

EXPECTED_VISUALS = [
    "tools/recovery_case_pack_renderer/visuals/case_001_green_surface_dead_recovery.svg",
    "tools/recovery_case_pack_renderer/visuals/case_002_visible_not_traversable.svg",
    "tools/recovery_case_pack_renderer/visuals/case_003_interrupted_not_recovered.svg",
    "tools/recovery_case_pack_renderer/visuals/case_004_seen_not_protected.svg",
]

def run_command(command, cwd):
    result = subprocess.run(
        command,
        cwd=cwd,
        shell=True,
        text=True,
        capture_output=True
    )
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip()
    }

def exists_list(paths):
    return {
        path: (ROOT / path).exists()
        for path in paths
    }

def all_true(mapping):
    return all(mapping.values())

def main():
    recovery_dir = ROOT / "tools" / "recovery_case_pack_renderer"
    audit_dir = ROOT / "tools" / "stabilization_cycle_auditor"

    run_cases = run_command("python batch_recovery_case_runner.py", recovery_dir)
    render_svgs = run_command("python batch_svg_renderer.py", recovery_dir)
    audit = run_command("python stabilization_cycle_auditor.py", audit_dir)

    required_files = exists_list(REQUIRED_FILES)
    outputs = exists_list(EXPECTED_OUTPUTS)
    visuals = exists_list(EXPECTED_VISUALS)

    healthy = (
        run_cases["returncode"] == 0
        and render_svgs["returncode"] == 0
        and audit["returncode"] == 0
        and all_true(required_files)
        and all_true(outputs)
        and all_true(visuals)
    )

    decision = "PROCEED" if healthy else "HOLD"

    summary = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "decision": decision,
        "core_reduction": "A reviewer should not need to understand the whole repository to verify one bounded claim.",
        "runtime_boundary": "Observer-only. Not authority. UNKNOWN -> HOLD.",
        "commands": {
            "run_cases": run_cases,
            "render_svgs": render_svgs,
            "stabilization_audit": audit
        },
        "checks": {
            "required_files": required_files,
            "expected_outputs": outputs,
            "expected_visuals": visuals
        }
    }

    output_file = ROOT / "tools" / "one_click_review_pipeline" / "review_summary.json"
    output_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps({
        "decision": decision,
        "summary_file": str(output_file),
        "core_reduction": summary["core_reduction"],
        "runtime_boundary": summary["runtime_boundary"]
    }, indent=2))

if __name__ == "__main__":
    main()