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
echo [11] XSS surface exposure detector
python tools\xss_surface_exposure_detector\xss_surface_detector.py

echo.
echo [12] Interruption arrival realism engine
python tools\interruption_arrival_realism_engine\run_arrival_realism.py

echo.
echo [13] Governability camouflage detector
python tools\governability_camouflage_detector\run_camouflage_detector.py

echo.
echo [14] Synchronization collapse simulator
python tools\synchronization_collapse_simulator\run_synchronization_collapse.py

echo.
echo ============================================
echo FULL OBSERVATORY PIPELINE COMPLETE
echo ============================================

echo.
echo Current hostile-runtime compression:
echo Governability collapses where executable interruption corridors become non-traversable under continuation pressure.
echo.

pause