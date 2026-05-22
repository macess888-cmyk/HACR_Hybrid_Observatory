@echo off
echo Running HACR Minimal Runtime Suite
echo.

echo [1/5] Continuation Hardening Renderer
python ..\..\tools\continuation_hardening_renderer\continuation_hardening_renderer.py

echo.
echo [2/5] Synchronization Pressure Mapper
python ..\..\tools\synchronization_pressure_mapper\synchronization_pressure_mapper.py

echo.
echo [3/5] Interruption Window Decay Mapper
python ..\..\tools\interruption_window_decay_mapper\interruption_window_decay_mapper.py

echo.
echo [4/5] Escalation Traversal Renderer
python ..\..\tools\escalation_traversal_renderer\escalation_traversal_renderer.py

echo.
echo [5/5] Dependency Gravity Renderer
python ..\..\tools\dependency_gravity_renderer\dependency_gravity_renderer.py

echo.
echo Minimal runtime suite complete.
echo Outputs are bounded observability artifacts only.
echo UNKNOWN -^> HOLD.