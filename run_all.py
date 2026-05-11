import subprocess

def run(script):
    print(f"\n=== Running {script} ===")
    subprocess.run(["python", script], check=False)

# =========================================================
# HACR Hybrid Observatory
# Observer-Restricted Continuity Survivability Observatory
# =========================================================

# ---------------------------------------------------------
# Core Engines
# ---------------------------------------------------------
run("hacr_core.py")
run("lens_engine.py")
run("matrix_engine.py")
run("drift_engine.py")
run("dependency_engine.py")
run("watchdog_engine.py")

# ---------------------------------------------------------
# Topology & Structural Mapping
# ---------------------------------------------------------
run("topology_mapper.py")
run("topology_visualizer.py")
run("topology_drift_timeline.py")
run("topology_pressure_field.py")
run("topology_stability_gradient.py")

# ---------------------------------------------------------
# Pricing / Signal / Bind Analysis
# ---------------------------------------------------------
run("pricing_scope_engine.py")
run("signal_bridge_mapper.py")
run("condition_trace_mapper.py")
run("bind_freshness_checker.py")

# ---------------------------------------------------------
# Semantic / Language / Interpretation Layers
# ---------------------------------------------------------
run("language_simplifier.py")
run("reversal_asymmetry_lens.py")
run("semantic_asymmetry_lens.py")
run("semantic_fragmentation_lens.py")
run("semantic_lineage_chain.py")

# ---------------------------------------------------------
# Receipt / Traceability
# ---------------------------------------------------------
run("receipt_integrity_chain.py")

# ---------------------------------------------------------
# Dynamic Drift / Continuity / Lineage
# ---------------------------------------------------------
run("dynamic_drift_lens.py")
run("alpha_omega_lineage_lens.py")
run("lineage_consumption_checker.py")
run("lineage_consumption_auditor.py")
run("refusal_propagation_mapper.py")

# ---------------------------------------------------------
# Reachability / Reconstruction / Propagation
# ---------------------------------------------------------
run("superposition_reachability_mapper.py")
run("latent_path_detector.py")
run("cross_domain_propagation_mapper.py")
run("descendant_effect_mapper.py")
run("distributed_reconstruction_lens.py")

# ---------------------------------------------------------
# Authority / Replay / Collapse
# ---------------------------------------------------------
run("authority_surface_mapper.py")
run("replay_vector_mapper.py")
run("constructibility_collapse_mapper.py")
run("irreversibility_surface_mapper.py")

# ---------------------------------------------------------
# Correlation / Pressure / Aggregation
# ---------------------------------------------------------
run("cross_lens_correlation_engine.py")
run("continuation_pressure_index.py")
run("continuity_collapse_index.py")

# ---------------------------------------------------------
# Observatory State & Spatial Mapping
# ---------------------------------------------------------
run("observatory_state_atlas.py")
run("survivability_corridor_mapper.py")
run("survivability_heatmap_generator.py")

# ---------------------------------------------------------
# Final Receipt Generation
# ---------------------------------------------------------
run("receipt_engine.py")

print("\nHACR Hybrid Observatory full run complete.")