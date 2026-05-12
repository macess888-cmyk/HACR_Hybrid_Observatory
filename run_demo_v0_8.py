import subprocess

print("\n=== HACR v0.8 Survivability Demo ===\n")

engines = [
    "watchdog_engine.py",
    "replay_vector_mapper.py",
    "refusal_propagation_mapper.py",
    "authority_surface_mapper.py",
    "shared_persistence_lineage_detector.py",
    "continuation_pressure_index.py",
    "survivability_topology_projection_engine.py",
    "survivability_graph_export_engine.py",
    "derived_lineage_mapper.py",
    "survivability_svg_renderer.py"
]

for engine in engines:
    print(f"\n=== Running {engine} ===")
    subprocess.run(["python", engine])

print("\n=== HACR v0.8 Demo Complete ===")