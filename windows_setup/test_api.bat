@echo off
REM Test the Burnout Prediction API on Windows

echo 🧪 Testing Burnout Prediction API...
echo ===================================

REM Check if curl is available (Windows 10+ has curl built-in)
curl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ curl is not available. Please install curl or use PowerShell Invoke-RestMethod
    echo Alternatively, test the API at: http://localhost:8000/docs
    pause
    exit /b 1
)

echo 1. Testing health endpoint...
curl -s http://localhost:8000/health
if %errorlevel% equ 0 (
    echo ✅ Health check successful
) else (
    echo ❌ Health check failed - make sure API is running
    echo Run: start_api.bat
    pause
    exit /b 1
)

echo.
echo 2. Testing single prediction...
curl -s -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d "{\"designation\": 3, \"resource_allocation\": 7.5, \"mental_fatigue\": 6.2, \"is_male\": 1, \"is_service\": 0, \"wfh_available\": 1}"
echo.

echo.
echo 3. Testing high risk employee...
curl -s -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d "{\"designation\": 5, \"resource_allocation\": 10.0, \"mental_fatigue\": 9.5, \"is_male\": 0, \"is_service\": 1, \"wfh_available\": 0}"
echo.

echo.
echo 4. Testing model info...
curl -s http://localhost:8000/model/info
echo.

echo.
echo ✅ API testing complete!
echo.
echo You can also test interactively at: http://localhost:8000/docs
pause
