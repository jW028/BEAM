@echo off
REM Launch script for the complete burnout prediction system on Windows

echo 🚀 Starting Burnout Prediction System...
echo =======================================

REM Check if model exists
if not exist "models\burnout_prediction_model.pkl" (
    echo ❌ Model file not found!
    echo Please train the model first:
    echo python burnout_prediction_model.py
    pause
    exit /b 1
)

REM Function to start API server
echo 🔧 Starting API server on port 8000...
cd api
start "Burnout API Server" cmd /k "call ..\venv\Scripts\activate.bat && uvicorn app:app --host 0.0.0.0 --port 8000 --reload"
cd ..

REM Wait for API to start
echo ⏳ Waiting for API to initialize...
timeout /t 5 /nobreak > nul

REM Test if API is running
echo 🧪 Testing API connection...
curl -s http://localhost:8000/health > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ API server started successfully!
) else (
    echo ⚠️ API may still be starting up...
)

REM Start frontend server
echo 🌐 Starting frontend server on port 3000...
cd frontend
start "Burnout Frontend Server" cmd /k "python server.py"
cd ..

REM Wait for frontend to start
echo ⏳ Waiting for frontend to initialize...
timeout /t 3 /nobreak > nul

REM Test if frontend is running
curl -s http://localhost:3000 > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Frontend server started successfully!
) else (
    echo ⚠️ Frontend may still be starting up...
)

echo.
echo 🎉 System is ready!
echo 📱 Frontend: http://localhost:3000
echo 🔧 API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🔍 Health Check: http://localhost:8000/health
echo.
echo Both servers are running in separate windows.
echo Close the server windows to stop the services.
echo.

REM Open browser automatically if available
echo 🌐 Opening browser...
start http://localhost:3000

echo Press any key to exit this setup window...
pause > nul
