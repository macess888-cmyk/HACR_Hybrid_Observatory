@echo off

echo ======================================
echo React Error Recovery Auditor
echo ======================================

cd tools\react_error_recovery_auditor

python react_error_auditor.py

echo.
echo Output:
echo tools\react_error_recovery_auditor\sample_react_error_output.json

pause