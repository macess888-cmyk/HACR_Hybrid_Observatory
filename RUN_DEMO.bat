@echo off

echo ======================================
echo HACR Hybrid Observatory Demo Runner
echo ======================================

cd tools\recovery_case_pack_renderer

echo.
echo Running deterministic recovery cases...
python batch_recovery_case_runner.py

echo.
echo Rendering SVG outputs...
python batch_svg_renderer.py

echo.
echo Outputs available in:
echo tools\recovery_case_pack_renderer\visuals

pause