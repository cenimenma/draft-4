@echo off
echo ========================================
echo 🤖 Argus Auto Review - Quick Demo
echo ========================================
echo.
echo This will demonstrate the complete workflow:
echo   GitHub Actions → Argus API → AI Review → PR Comment
echo.

REM Check if API is running
echo Checking API status...
curl -s http://localhost:8000/health > nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  WARNING: API server is not running at http://localhost:8000
    echo.
    echo The demo will use mock data to show the workflow.
    echo.
    echo To use real AI review, start the API first:
    echo   cd ..\draft_3
    echo   python backend\main.py
    echo.
    pause
) else (
    echo ✅ API server is running!
    echo.
)

echo Starting demo...
echo.

REM Run the demo script
python demo_simple.py

echo.
echo ========================================
echo Demo completed!
echo ========================================
echo.
echo Next steps:
echo   1. Push this code to GitHub
echo   2. Configure GitHub Secrets (ARGUS_API_URL)
echo   3. Create a PR to see auto-review in action!
echo.
pause
