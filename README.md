# Burnout Early Alert Monitor (BEAM)

AI-powered employee burnout risk prediction with 91% confidence intervals.

## 🚀 Quick Start

### Prerequisites
- Python 3.12 recommended
- Git (optional)

### Setup & Run

**Windows:**
```cmd
windows_setup\install_dependencies.bat
windows_setup\start_full_system.bat
```

**Unix/Linux/macOS:**
```bash
chmod +x unix_setup/*.sh
./unix_setup/install_dependencies.sh
./unix_setup/start_full_system.sh
```

### Access the System
- 🌐 **Web Interface**: http://localhost:3000
- 🔧 **API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs

## ✨ What You Get

- **Web Interface**: Upload CSV or use sliders for single predictions
- **REST API**: Integrate with your existing systems
- **Confidence Scores**: Know how reliable each prediction is
- **Batch Processing**: Analyze multiple employees at once

## � How It Works

Input 6 simple parameters:
- Job level (0-5)
- Resource allocation (0-10)
- Mental fatigue (0-10)  
- Gender (Male/Female)
- Company type (Product/Service)
- Work from home (Yes/No)

Get back:
- **Burnout risk** (0-100%)
- **Risk category** (Low/Medium/High)
- **Confidence score** (how certain the AI is)

## 🛠️ Manual Setup (If Automated Scripts Fail)

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python burnout_prediction_model.py
```

**Unix/Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python burnout_prediction_model.py
```

Then start the system:
- **Windows**: `windows_setup\start_full_system.bat`
- **Unix/Linux/macOS**: `./unix_setup/start_full_system.sh`

## 🔌 API Usage

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

**Response:**
```json
{
  "predicted_burn_rate": 0.6234,
  "risk_category": "Medium Risk",
  "confidence_score": 0.8456
}
```

## 🎯 Parameters

| Parameter | Range | Description |
|-----------|-------|-------------|
| `designation` | 0-5 | Job level (0=Intern, 5=Director) |
| `resource_allocation` | 0-10 | Workload score |
| `mental_fatigue` | 0-10 | Stress level |
| `is_male` | 0,1 | Gender (0=Female, 1=Male) |
| `is_service` | 0,1 | Company type (0=Product, 1=Service) |
| `wfh_available` | 0,1 | Remote work (0=No, 1=Yes) |

## ⚠️ Troubleshooting

**Python not found:**
- Windows: Install from [python.org](https://python.org), check "Add to PATH"
- macOS: `brew install python3`
- Ubuntu: `sudo apt install python3 python3-pip python3-venv`

**Permission errors:**
- Windows: Run Command Prompt as Administrator
- Unix: `chmod +x unix_setup/*.sh`

**Port already in use:**
- Change ports in startup scripts or kill existing processes

### 🐍 **Python Version Issues (Recommended: Python 3.12)**

If you're using Python 3.13+ and encountering compatibility issues, downgrade to Python 3.12:

**Windows:**
```cmd
# 1. Download Python 3.12 from python.org
# 2. Install Python 3.12 (check "Add to PATH")
# 3. Recreate virtual environment
rmdir /s /q venv
py -3.12 -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

**macOS (with Homebrew):**
```bash
# Install Python 3.12
brew install python@3.12

# Recreate virtual environment
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Ubuntu/Debian:**
```bash
# Install Python 3.12
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-pip

# Recreate virtual environment
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Check your Python version:**
```bash
python --version  # Should show Python 3.12.x
```

## 📄 License

MIT License - Use freely for commercial and personal projects.

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
