import subprocess


def run(script_name):
    print(f"\n=== Running {script_name} ===")
    subprocess.run(["python", script_name], check=True)


run("hacr_core.py")
run("lens_engine.py")
run("matrix_engine.py")
run("drift_engine.py")
run("dependency_engine.py")
run("watchdog_engine.py")
run("receipt_engine.py")

print("\nHACR Hybrid Observatory full run complete.")