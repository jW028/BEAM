@echo off
REM Quick start script for the API on Windows

echo 🚀 Starting Burnout Prediction API...

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo 📦 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ❌ Virtual environment not found. Run setup.bat first
    pause
    exit /b 1
)

REM Check if model exists
if not exist "models\burnout_prediction_model.pkl" (
    echo ❌ Model file not found. Run python burnout_prediction_model.py first
    pause
    exit /b 1
)

REM Start the FastAPI server
echo 🔧 Starting API server on port 8000...
cd api
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
