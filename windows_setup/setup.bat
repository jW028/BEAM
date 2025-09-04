@echo off
REM Burnout Prediction API Setup Script for Windows

echo 🚀 Starting Burnout Prediction API Setup...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python first.
    echo You can download it from https://python.org
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found
    echo Creating requirements.txt file...
    echo fastapi==0.104.1> requirements.txt
    echo uvicorn==0.24.0>> requirements.txt
    echo joblib==1.3.2>> requirements.txt
    echo pandas==2.1.3>> requirements.txt
    echo numpy==1.25.2>> requirements.txt
    echo scikit-learn==1.3.2>> requirements.txt
    echo xgboost==2.0.1>> requirements.txt
    echo pydantic==2.5.0>> requirements.txt
    echo scipy==1.11.4>> requirements.txt
    echo optuna==3.4.0>> requirements.txt
)

REM Install requirements
echo 📚 Installing requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)

REM Check if model exists
if not exist "models\burnout_prediction_model.pkl" (
    echo ❌ Model file not found at models\burnout_prediction_model.pkl
    echo Please run the training script first to generate the model:
    echo python burnout_prediction_model.py
    pause
    exit /b 1
)

echo ✅ Setup complete!
echo.
echo To start the API server, run:
echo cd api ^&^& uvicorn app:app --host 0.0.0.0 --port 8000 --reload
echo.
echo Or use the quick start command:
echo start_api.bat
echo.
pause
