# Burnout Prediction System - Windows Setup Guide

This guide provides Windows-specific setup instructions for the Burnout Prediction System.

## 🖥️ Windows Setup Files

The following `.bat` files are provided for Windows users:

### Core Setup Files
- **`install_dependencies.bat`** - Install all required Python packages
- **`setup.bat`** - Complete system setup and validation
- **`check_setup.bat`** - Verify system configuration

### Launch Scripts
- **`start_full_system.bat`** - Start both API and frontend servers
- **`start_api.bat`** - Start only the API server
- **`start_frontend.bat`** - Start only the frontend server

### Testing Scripts
- **`test_api.bat`** - Test API functionality with sample requests

## 🚀 Quick Start for Windows

### 1. **Complete Setup (Recommended)**
```batch
REM Run these commands in Command Prompt or PowerShell
install_dependencies.bat
python burnout_prediction_model.py
start_full_system.bat
```

### 2. **Step-by-Step Setup**
```batch
REM 1. Install dependencies
install_dependencies.bat

REM 2. Check setup
check_setup.bat

REM 3. Train the model
python burnout_prediction_model.py

REM 4. Start the system
start_full_system.bat
```

## 📋 System Requirements

- **Windows 10 or later** (for built-in curl support)
- **Python 3.8+** installed and in PATH
- **8GB RAM minimum** (for XGBoost training)
- **1GB free disk space**

## 🛠️ Manual Setup (Alternative)

If the batch files don't work, you can set up manually:

```batch
REM Create virtual environment
python -m venv venv

REM Activate virtual environment
venv\Scripts\activate.bat

REM Install packages
pip install fastapi uvicorn joblib pandas numpy scikit-learn xgboost pydantic scipy optuna

REM Train model
python burnout_prediction_model.py

REM Start API (in one terminal)
cd api
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

REM Start frontend (in another terminal)
cd frontend
python server.py
```

## 🌐 Access Points

Once running, access the system at:

- **🖥️ Web Interface**: http://localhost:3000
- **🔧 API Endpoint**: http://localhost:8000
- **📚 API Documentation**: http://localhost:8000/docs
- **🔍 Health Check**: http://localhost:8000/health

## 🐛 Troubleshooting

### Common Issues

**1. Python not found**
```
❌ Python is not installed
```
**Solution**: Install Python from https://python.org and ensure it's in PATH

**2. Virtual environment activation fails**
```
❌ venv\Scripts\activate.bat is not recognized
```
**Solution**: Run `python -m venv venv` to recreate the environment

**3. Port already in use**
```
❌ Address already in use
```
**Solution**: Kill the process or use different ports:
```batch
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**4. Model file not found**
```
❌ Model file not found
```
**Solution**: Train the model first:
```batch
python burnout_prediction_model.py
```

**5. CORS errors in browser**
```
❌ CORS policy error
```
**Solution**: Ensure both servers are running and API has CORS enabled

### Alternative Testing

If curl is not available, use PowerShell:

```powershell
# Test health endpoint
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get

# Test prediction
$body = @{
    designation = 3
    resource_allocation = 7.5
    mental_fatigue = 6.2
    is_male = 1
    is_service = 0
    wfh_available = 1
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body $body -ContentType "application/json"
```

## 📞 Support

If you encounter issues:

1. Run `check_setup.bat` to diagnose problems
2. Check the error messages in the terminal windows
3. Ensure all dependencies are installed correctly
4. Verify Python and pip are working: `python --version` and `pip --version`

## 🔄 Cross-Platform Note

For users who prefer Unix-style scripts on Windows:
- Install **Git Bash** or **WSL** (Windows Subsystem for Linux)
- Use the original `.sh` files instead of `.bat` files
