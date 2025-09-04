@echo off
REM Install all dependencies for Burnout Prediction System on Windows

echo 📦 Installing Burnout Prediction System Dependencies...
echo ====================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python first.
    echo You can download it from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 🐍 Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install required packages
echo 📥 Installing required packages...
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install joblib==1.3.2
pip install pandas==2.1.3
pip install numpy==1.25.2
pip install scikit-learn==1.3.2
pip install xgboost==2.0.1
pip install pydantic==2.5.0
pip install scipy==1.11.4
pip install optuna==3.4.0

if %errorlevel% neq 0 (
    echo ❌ Failed to install packages
    pause
    exit /b 1
)

echo ✅ Installation complete!
echo.
echo To activate the virtual environment in the future, run:
echo venv\Scripts\activate.bat
echo.
echo Next steps:
echo 1. Train the model: python burnout_prediction_model.py
echo 2. Start the full system: start_full_system.bat
echo.
pause
