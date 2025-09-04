# Burnout Prediction System

A complete AI-powered system for predicting employee burnout risk using machine learning, featuring a REST API and modern web interface with confidence scoring.

## 🎯 Features

- **Machine Learning Models**: XGBoost with quantile regression for 91% confidence intervals
- **REST API**: FastAPI with single/batch prediction endpoints
- **Modern Web Interface**: Responsive design with mathematical confidence tooltips
- **Cross-Platform**: Supports Windows, macOS, and Linux
- **Confidence Scoring**: Statistical uncertainty quantification

## 🚀 Quick Setup Guide

### 📋 Prerequisites

**All Systems:**
- Python 3.8+ installed
- Git (optional, for cloning)

**Windows:**
- Command Prompt or PowerShell with Administrator privileges
- Ensure Python is added to PATH during installation

**Unix/Linux/macOS:**
- Terminal access
- Basic command line familiarity

---

## 🖥️ Platform-Specific Installation

### 🪟 **Windows Setup**

#### **Option 1: Automated Setup (Recommended)**
```cmd
# Navigate to project directory
cd C:\path\to\burnout_prediction

# Run automated installer
windows_setup\install_dependencies.bat
```

#### **Option 2: Manual Setup**
```cmd
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
venv\Scripts\activate.bat

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Train the model
python burnout_prediction_model.py

# 6. Start the system
windows_setup\start_full_system.bat
```

#### **Windows Troubleshooting**

**"System cannot find the path specified":**
```cmd
# Try with py launcher
py -m venv venv

# Or use full paths
python -m venv "C:\full\path\to\your\project\venv"
```

**Python not found:**
- Reinstall Python from [python.org](https://python.org)
- ✅ Check "Add Python to PATH" during installation
- Restart Command Prompt after installation

**Permission errors:**
- Run Command Prompt as Administrator
- Or move project to `C:\burnout_prediction` (shorter path)

---

### 🐧 **Unix/Linux/macOS Setup**

#### **Option 1: Automated Setup (Recommended)**
```bash
# Navigate to project directory
cd /path/to/burnout_prediction

# Make scripts executable
chmod +x unix_setup/*.sh

# Run automated installer
./unix_setup/install_dependencies.sh
```

#### **Option 2: Manual Setup**
```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Train the model
python burnout_prediction_model.py

# 6. Start the system
./unix_setup/start_full_system.sh
```

#### **Unix Troubleshooting**

**Permission denied:**
```bash
chmod +x unix_setup/*.sh
# Or
sudo ./unix_setup/install_dependencies.sh
```

**Python3 not found:**
```bash
# Try different Python commands
python --version
python3 --version
py --version

# Install Python (Ubuntu/Debian)
sudo apt update && sudo apt install python3 python3-pip python3-venv

# Install Python (CentOS/RHEL)
sudo yum install python3 python3-pip

# Install Python (macOS with Homebrew)
brew install python3
```

---

## 🚀 Quick Start (Any Platform)

### **1. Complete System Launch**

**Windows:**
```cmd
windows_setup\start_full_system.bat
```

**Unix/Linux/macOS:**
```bash
./unix_setup/start_full_system.sh
```

This launches:
- 🔧 **API Server** on http://localhost:8000
- 🌐 **Frontend** on http://localhost:3000  
- 📚 **API Documentation** on http://localhost:8000/docs

### **2. Individual Components**

**Train Model:**
```bash
# Windows
python burnout_prediction_model.py

# Unix/Linux/macOS
python burnout_prediction_model.py
```

**Start API Only:**
```bash
# Windows
cd api && uvicorn app:app --reload

# Unix/Linux/macOS
cd api && uvicorn app:app --reload
```

**Start Frontend Only:**
```bash
# Windows
cd frontend && python server.py

# Unix/Linux/macOS  
cd frontend && python server.py
```

---

## 📁 Cross-Platform Project Structure

```
burnout_prediction/
├── 📁 api/                          # FastAPI backend
│   └── app.py                       # Main API application
├── 📁 frontend/                     # Web interface
│   ├── index.html                   # Main HTML file
│   └── server.py                    # Frontend server
├── 📁 models/                       # Trained ML models
│   ├── burnout_prediction_model.pkl # Main XGBoost model
│   ├── lower_quantile_model.pkl     # 1st percentile model
│   └── upper_quantile_model.pkl     # 99th percentile model
├── 📁 windows_setup/                # Windows-specific scripts
│   ├── install_dependencies.bat     # Dependency installer
│   ├── start_full_system.bat        # System launcher
│   └── activate_env.bat             # Environment activator
├── 📁 unix_setup/                   # Unix/Linux/macOS scripts
│   ├── install_dependencies.sh      # Dependency installer
│   ├── start_full_system.sh         # System launcher
│   └── activate_env.sh              # Environment activator
├── 📁 input/                        # Training data
│   ├── train.csv                    # Training dataset
│   └── test.csv                     # Test dataset
├── burnout_prediction_model.py      # Model training script
├── validate_confidence.py           # Confidence validation
├── requirements.txt                 # Python dependencies
└── README.md                        # This documentation
```

## 🌐 Web Interface

The frontend provides a user-friendly interface with:

### ✨ Features
- **Responsive Design**: Works on all devices (desktop, tablet, mobile)
- **Interactive Sliders**: Real-time input adjustment with visual feedback
- **Risk Visualization**: Color-coded results with confidence tooltips
- **Batch Processing**: CSV upload for multiple predictions
- **Mathematical Tooltips**: Statistical explanations of confidence scores
- **Error Handling**: Clear user feedback and input validation
- **Modern UI**: Beautiful gradients, animations, and professional styling

### 📊 Input Parameters
- **Job Designation**: Level 0-5 (Intern to Executive/Director)
- **Gender**: Male/Female selection
- **Company Type**: Product-based vs Service-based
- **Work From Home**: Available vs Not Available
- **Resource Allocation**: 0-10 scale (workload distribution)
- **Mental Fatigue**: 0-10 scale (stress/exhaustion level)

### 🎨 Risk Categories
- 🟢 **Low Risk** (≤30%): Healthy work-life balance maintained
- 🟡 **Medium Risk** (30-60%): Caution needed, monitor closely
- 🔴 **High Risk** (>60%): Immediate attention and intervention required

### � Confidence Scoring
The system provides **91% confidence intervals** using quantile regression:
- **High Confidence (85-100%)**: Very reliable prediction
- **Medium Confidence (70-84%)**: Reliable with minor uncertainty
- **Lower Confidence (<70%)**: Consider additional factors

---

## 📖 API Documentation

### 🔌 API Endpoints

**Base URL:** `http://localhost:8000`

#### Health Check
```http
GET /health
```
Returns system status and model information.

#### Single Prediction
```http
POST /predict
Content-Type: application/json

{
  "designation": 3,
  "resource_allocation": 7.5,
  "mental_fatigue": 6.2,
  "is_male": 1,
  "is_service": 0,
  "wfh_available": 1
}
```

#### Batch Prediction
```http
POST /predict/batch
Content-Type: application/json

[
  {
    "designation": 3,
    "resource_allocation": 7.5,
    "mental_fatigue": 6.2,
    "is_male": 1,
    "is_service": 0,
    "wfh_available": 1
  }
]
```

#### Model Information
```http
GET /model/info
```

### 📊 Input Parameters Reference

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `designation` | int | 0-5 | Job level: 0=Intern, 1=Junior, 2=Mid, 3=Senior, 4=Lead, 5=Director |
| `resource_allocation` | float | 0-10 | Workload distribution and resource availability |
| `mental_fatigue` | float | 0-10 | Mental exhaustion and stress level |
| `is_male` | int | 0,1 | Gender: 0=Female, 1=Male |
| `is_service` | int | 0,1 | Company type: 0=Product-based, 1=Service-based |
| `wfh_available` | int | 0,1 | Work from home option: 0=Not Available, 1=Available |

### 📈 Response Format

```json
{
  "predicted_burn_rate": 0.6234,
  "risk_category": "Medium Risk", 
  "confidence_score": 0.8456,
  "confidence_interval": {
    "lower": 0.5123,
    "upper": 0.7345
  }
}
```

---

## 🧪 Testing & Validation

### 🌐 Interactive API Documentation
Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 🧪 Testing with cURL

**Health Check:**
```bash
curl -X GET "http://localhost:8000/health"
```

**Single Prediction:**
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "designation": 3,
       "resource_allocation": 7.5,
       "mental_fatigue": 6.2,
       "is_male": 1,
       "is_service": 0,
       "wfh_available": 1
     }'
```

**Batch Prediction:**
```bash
curl -X POST "http://localhost:8000/predict/batch" \
     -H "Content-Type: application/json" \
     -d '[
       {
         "designation": 3,
         "resource_allocation": 7.5,
         "mental_fatigue": 6.2,
         "is_male": 1,
         "is_service": 0,
         "wfh_available": 1
       }
     ]'
```

### 🐍 Python Client Example

```python
import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

# Single prediction
def predict_single(data):
    response = requests.post(f"{BASE_URL}/predict", json=data)
    return response.json()

# Batch prediction
def predict_batch(data_list):
    response = requests.post(f"{BASE_URL}/predict/batch", json=data_list)
    return response.json()

# Example usage
single_data = {
    "designation": 3,
    "resource_allocation": 7.5,
    "mental_fatigue": 6.2,
    "is_male": 1,
    "is_service": 0,
    "wfh_available": 1
}

result = predict_single(single_data)
print(f"Burn Rate: {result['predicted_burn_rate']:.4f}")
print(f"Risk: {result['risk_category']}")
print(f"Confidence: {result['confidence_score']:.1%}")
```

---

## 🚦 Error Handling

The API returns appropriate HTTP status codes:
- **200**: Success
- **400**: Bad Request (invalid input)
- **422**: Validation Error (parameter out of range)
- **500**: Internal Server Error

**Error Response Format:**
```json
{
  "detail": [
    {
      "loc": ["body", "designation"],
      "msg": "ensure this value is less than or equal to 5",
      "type": "value_error.number.not_le",
      "ctx": {"limit_value": 5}
    }
  ]
}
```

---

## � Development & Deployment

### 🛠️ Development Mode
```bash
# Windows
cd api && python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Unix/Linux/macOS
cd api && uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 🚀 Production Deployment
```bash
# With multiple workers
uvicorn api.app:app --host 0.0.0.0 --port 8000 --workers 4

# With Gunicorn (Unix/Linux only)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.app:app --bind 0.0.0.0:8000
```

### 🐳 Docker Deployment (Optional)

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build and run:**
```bash
docker build -t burnout-prediction .
docker run -p 8000:8000 burnout-prediction
```

---

## 🧠 Model Details

### 🤖 Machine Learning Architecture
- **Primary Model**: XGBoost Regressor with quantile regression
- **Confidence Intervals**: 91% coverage using 1st-99th percentile quantiles
- **Backup Models**: Random Forest, Decision Tree (for comparison)
- **Hyperparameter Optimization**: Optuna with 100 trials
- **Validation**: Statistical coverage testing (91.12% achieved)

### 📊 Model Performance
- **R² Score**: ~90% (XGBoost)
- **Confidence Range**: 60-90% (practical range)
- **Coverage**: 91.12% (validated on test set)
- **Training Features**: 6 engineered features from original dataset

### 🎯 Feature Engineering
Original dataset transformed into:
- `designation`: Job level (0-5)
- `resource_allocation`: Workload score (0-10)
- `mental_fatigue`: Stress level (0-10)
- `is_male`: Gender encoding (0/1)
- `is_service`: Company type (0/1)
- `wfh_available`: Remote work option (0/1)

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### 🛠️ Development Setup
1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/burnout_prediction.git
   ```
3. **Set up development environment:**
   ```bash
   # Windows
   windows_setup\install_dependencies.bat
   
   # Unix/Linux/macOS
   ./unix_setup/install_dependencies.sh
   ```
4. **Create a feature branch:**
   ```bash
   git checkout -b feature/amazing-feature
   ```

### 🧪 Testing Guidelines
- Add tests for new features
- Ensure all existing tests pass
- Test both API and frontend components
- Validate cross-platform compatibility

### 📝 Code Standards
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings for functions
- Comment complex logic
- Maintain backward compatibility

### 🚀 Submission Process
1. **Commit your changes:**
   ```bash
   git commit -m "Add amazing feature"
   ```
2. **Push to your branch:**
   ```bash
   git push origin feature/amazing-feature
   ```
3. **Open a Pull Request**
4. **Describe your changes** clearly
5. **Wait for review** and address feedback

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### 📋 License Summary
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ Liability
- ❌ Warranty

---

## 🎉 Acknowledgments

- **XGBoost Team**: For the excellent gradient boosting framework
- **FastAPI Team**: For the modern, fast web framework
- **Optuna Team**: For hyperparameter optimization tools
- **Open Source Community**: For the amazing ecosystem of tools

---

## 📞 Support

Having issues? Here's how to get help:

### 🐛 Bug Reports
- Check [existing issues](https://github.com/yourusername/burnout_prediction/issues)
- Create a new issue with detailed reproduction steps
- Include system information and error messages

### 💬 Questions & Discussions  
- Start a [discussion](https://github.com/yourusername/burnout_prediction/discussions)
- Tag with appropriate labels
- Be specific about your use case

### � Contact
- **Email**: your.email@example.com
- **GitHub**: @yourusername

---

**🎯 Ready to predict burnout risk with confidence!** 🚀
