#!/bin/bash
# Install dependencies for Burnout Prediction System

set -e

echo "📦 Installing Burnout Prediction System..."
echo "========================================="

# Change to script directory
cd "$(dirname "$0")"
cd ..

# Check Python installation
echo "🐍 Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found. Please install Python 3.8+"
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "   macOS: brew install python3"
    exit 1
fi

echo "✅ Found: $($PYTHON_CMD --version)"

# Setup virtual environment
echo "� Setting up virtual environment..."
[ -d "venv" ] && rm -rf venv
$PYTHON_CMD -m venv venv
source venv/bin/activate

# Install packages
echo "📦 Installing packages..."
pip install --upgrade pip -q
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install fastapi uvicorn pandas numpy scikit-learn xgboost joblib pydantic optuna matplotlib seaborn scipy python-multipart
fi

echo "✅ Installation complete!"
echo
echo "Next steps:"
echo "  1. Activate environment: source venv/bin/activate"
echo "  2. Train model: python burnout_prediction_model.py"
echo "  3. Start system: ./unix_setup/start_full_system.sh"