import subprocess

SCRIPTS = [
    "hacr_core.py",
    "lens_engine.py",
    "matrix_engine.py",
    "drift_engine.py",
    "dependency_engine.py",
    "watchdog_engine.py",
    "topology_mapper.py",
    "topology_visualizer.py",
    "pricing_scope_engine.py",
    "signal_bridge_mapper.py",
    "condition_trace_mapper.py",
    "bind_freshness_checker.py",
    "language_simplifier.py",
    "reversal_asymmetry_lens.py",
    "receipt_integrity_chain.py",
    "dynamic_drift_lens.py",
    "semantic_asymmetry_lens.py",
    "alpha_omega_lineage_lens.py",
    "superposition_reachability_mapper.py",
    "cross_lens_correlation_engine.py",
    "topology_drift_timeline.py",
    "latent_path_detector.py",
    "authority_surface_mapper.py",
    "constructibility_collapse_mapper.py",
    "replay_vector_mapper.py",
    "receipt_engine.py"
]

def run_script(script):
    print(f"\n=== Running {script} ===")
    subprocess.run(["python", script])

for script in SCRIPTS:
    run_script(script)

print("\nHACR Hybrid Observatory full run complete.")