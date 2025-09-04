@echo off
REM Check system setup for Burnout Prediction System on Windows

echo 🔍 Checking Burnout Prediction System Setup...
echo ==============================================

REM Check Python installation
echo 1. Checking Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    python --version
    echo ✅ Python is installed
) else (
    echo ❌ Python is not installed
)

REM Check virtual environment
echo.
echo 2. Checking virtual environment...
if exist "venv\Scripts\activate.bat" (
    echo ✅ Virtual environment found
) else (
    echo ❌ Virtual environment missing - run: install_dependencies.bat
)

REM Check model file
echo.
echo 3. Checking model file...
if exist "models\burnout_prediction_model.pkl" (
    echo ✅ Model file found
) else (
    echo ❌ Model file missing - run: python burnout_prediction_model.py
)

REM Check API directory
echo.
echo 4. Checking API components...
if exist "api" (
    echo ✅ API directory found
    if exist "api\app.py" (
        echo ✅ API application found
    ) else (
        echo ❌ API application missing
    )
) else (
    echo ❌ API directory missing
)

REM Check frontend directory
echo.
echo 5. Checking frontend components...
if exist "frontend" (
    echo ✅ Frontend directory found
    if exist "frontend\index.html" (
        echo ✅ Frontend HTML found
    ) else (
        echo ❌ Frontend HTML missing
    )
    if exist "frontend\server.py" (
        echo ✅ Frontend server found
    ) else (
        echo ❌ Frontend server missing
    )
) else (
    echo ❌ Frontend directory missing
)

REM Check Python dependencies (if venv exists)
echo.
echo 6. Checking Python dependencies...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    python -c "import fastapi, uvicorn, pandas, numpy, xgboost, sklearn, joblib; print('✅ All required packages installed')" 2>nul
    if %errorlevel% neq 0 (
        echo ❌ Missing packages - run: install_dependencies.bat
    )
) else (
    echo ⚠️ Cannot check dependencies - virtual environment missing
)

echo.
echo 📋 Quick Start Commands:
echo ========================
echo 1. Install dependencies: install_dependencies.bat
echo 2. Train model:         python burnout_prediction_model.py
echo 3. Start full system:   start_full_system.bat
echo 4. API only:            start_api.bat
echo 5. Frontend only:       start_frontend.bat
echo.
pause
