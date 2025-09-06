@echo off
REM Install dependencies for Burnout Prediction System on Windows

echo 📦 Installing Burnout Prediction System...
echo =========================================

REM Change to script directory and go up one level
cd /d "%~dp0"
cd ..

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Found: Python %PYTHON_VERSION%

REM Setup virtual environment
echo 🐍 Setting up virtual environment...
if exist "venv" rmdir /s /q "venv" 2>nul
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    echo Trying with py launcher...
    py -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Virtual environment creation failed
        pause
        exit /b 1
    )
)

call venv\Scripts\activate.bat

REM Install packages
echo 📦 Installing packages...
python -m pip install --upgrade pip -q
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    pip install fastapi uvicorn pandas numpy scikit-learn xgboost joblib pydantic optuna matplotlib seaborn scipy python-multipart
)

if %errorlevel% neq 0 (
    echo ❌ Failed to install packages
    pause
    exit /b 1
)

echo ✅ Installation complete!
echo.
echo Next steps:
echo   1. Activate environment: venv\Scripts\activate.bat
echo   2. Train model: python train_pipeline.py
echo   3. Start system: windows_setup\start_full_system.bat
pause