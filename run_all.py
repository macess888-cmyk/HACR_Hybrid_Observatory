import subprocess

def run(script):
    print(f"\n=== Running {script} ===")
    subprocess.run(
        ["python", script],
        check=True
    )

run("hacr_core.py")
run("lens_engine.py")
run("matrix_engine.py")
run("drift_engine.py")
run("dependency_engine.py")
run("watchdog_engine.py")
run("topology_mapper.py")
run("pricing_scope_engine.py")
run("receipt_engine.py")

print("\nHACR Hybrid Observatory full run complete.")