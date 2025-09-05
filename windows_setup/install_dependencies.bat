@echo off
REM Install dependencies for Burnout Prediction System on Windows

echo 📦 Installing Burnout Prediction System...
echo =========================================

REM Change to script directory and go up one level
cd /d "%~dp0"
cd ..

REM Check if Python is installed and verify version
echo 🐍 Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Installing Python 3.12...
    echo.
    echo 📥 Downloading Python 3.12...
    
    REM Download Python 3.12 installer
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe' -OutFile 'python-3.12.6-installer.exe'"
    
    if exist "python-3.12.6-installer.exe" (
        echo 🔧 Installing Python 3.12...
        echo Please follow the installer prompts and make sure to:
        echo   ✅ Check "Add Python to PATH"
        echo   ✅ Check "Install for all users" (optional)
        echo.
        start /wait python-3.12.6-installer.exe /passive InstallAllUsers=1 PrependPath=1
        
        REM Clean up installer
        del python-3.12.6-installer.exe
        
        echo ✅ Python 3.12 installation completed
        echo 🔄 Please restart this script to continue
        pause
        exit /b 0
    ) else (
        echo ❌ Failed to download Python installer
        echo Please manually install Python 3.12 from https://python.org
        pause
        exit /b 1
    )
)

REM Get Python version and check if it's 3.12
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Found: Python %PYTHON_VERSION%

REM Extract major and minor version (e.g., 3.12 from 3.12.1)
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if not "%MAJOR%"=="3" (
    echo ❌ Python 3.x required. Found: %PYTHON_VERSION%
    echo Please install Python 3.12 from https://python.org
    pause
    exit /b 1
)

if not "%MINOR%"=="12" (
    echo ⚠️ Warning: Python 3.12 recommended for best compatibility
    echo Found: Python %PYTHON_VERSION%
    echo.
    echo Options:
    echo   1. Continue with current version
    echo   2. Install Python 3.12 automatically
    echo.
    set /p CHOICE=Choose option (1 or 2): 
    
    if "%CHOICE%"=="2" (
        echo 📥 Downloading Python 3.12...
        powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe' -OutFile 'python-3.12.10-installer.exe'"

        if exist "python-3.12.10-installer.exe" (
            echo 🔧 Installing Python 3.12...
            start /wait python-3.12.10-installer.exe /passive InstallAllUsers=1 PrependPath=1
            del python-3.12.10-installer.exe
            echo ✅ Python 3.12 installed. Please restart this script.
            pause
            exit /b 0
        )
    )
    
    if not "%CHOICE%"=="1" if not "%CHOICE%"=="2" (
        echo Installation cancelled.
        pause
        exit /b 1
    )
)

REM Setup virtual environment
echo � Setting up virtual environment...
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
echo   2. Train model: python burnout_prediction_model.py
echo   3. Start system: windows_setup\start_full_system.bat
pause
