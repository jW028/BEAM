@echo off
REM Frontend server start script for Windows

echo 🌐 Starting Frontend Server...

REM Check if frontend directory exists
if not exist "frontend" (
    echo ❌ Frontend directory not found
    pause
    exit /b 1
)

REM Check if frontend server exists
if not exist "frontend\server.py" (
    echo ❌ Frontend server file not found
    pause
    exit /b 1
)

echo 🔧 Starting frontend server on port 3000...
cd frontend
python server.py
