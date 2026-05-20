@echo off

echo ======================================
echo HACR Hybrid Observatory Full Review
echo ======================================

python tools\one_click_review_pipeline\one_click_review_pipeline.py

echo.
echo Review summary:
echo tools\one_click_review_pipeline\review_summary.json

pause