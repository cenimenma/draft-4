@echo off
echo ========================================
echo Argus Auto Review - Local Test
echo ========================================
echo.
echo This simulates the GitHub Actions workflow locally
echo.

REM Check if API is running
echo Checking API status...
curl -s http://localhost:8000/health > nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: API server is not running at http://localhost:8000
    echo Please start the API server first:
    echo   cd ..\draft_3
    echo   python backend\main.py
    echo.
    echo Continuing with mock mode...
    echo.
)

REM Run auto review script
echo Running auto review...
python auto_review.py

echo.
echo ========================================
echo Test completed!
echo ========================================
pause
