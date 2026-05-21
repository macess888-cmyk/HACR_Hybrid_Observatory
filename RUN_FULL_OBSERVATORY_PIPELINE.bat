@echo off

echo ============================================
echo HACR FULL HOSTILE-RUNTIME OBSERVATORY PIPELINE
echo ============================================
echo.

echo [1] Runtime replay pipeline
python tools\runtime_pipeline_runner\run_pipeline.py

echo.
echo [2] Interruption reconstruction viability
python tools\interruption_reconstruction_viability_harness\run_reconstruction_probe.py

echo.
echo [3] Governability mirage visualizer
python tools\governability_mirage_visualizer\render_mirage_probe.py

echo.
echo [4] CARE / ASRO seam integrity
python tools\care_asro_seam_integrity_tester\run_seam_test.py

echo.
echo [5] Runtime governability decay index
python tools\runtime_governability_decay_index\run_decay_index.py

echo.
echo [6] Continuation hardening topology renderer
python tools\continuation_hardening_topology_renderer\render_topology.py

echo.
echo [7] Runtime reconstruction timeline engine
python tools\runtime_reconstruction_timeline_engine\run_timeline_engine.py

echo.
echo [8] Interruption traversability mapper
python tools\interruption_traversability_mapper\run_traversability_mapper.py

echo.
echo [9] Compression failure boundary tester
python tools\compression_failure_boundary_tester\run_compression_boundary_test.py

echo.
echo [10] Judgement formation localizer
python tools\judgement_formation_localizer\run_judgement_localizer.py

echo.
echo ============================================
echo FULL OBSERVATORY PIPELINE COMPLETE
echo ============================================

pause