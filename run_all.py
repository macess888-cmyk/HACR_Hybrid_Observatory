import os

scripts = [
    "hacr_core.py",
    "lens_engine.py",
    "matrix_engine.py",
    "drift_engine.py",
    "dependency_engine.py",
    "watchdog_engine.py",
    "topology_mapper.py",
    "pricing_scope_engine.py",
    "signal_bridge_mapper.py",
    "condition_trace_mapper.py",
    "bind_freshness_checker.py",
    "language_simplifier.py",
    "reversal_asymmetry_lens.py",
    "receipt_engine.py"
]

for script in scripts:
    print(f"\n=== Running {script} ===")
    os.system(f"python {script}")

print("\nHACR Hybrid Observatory full run complete.")