#!/bin/bash
# Install dependencies for Burnout Prediction System

set -e

echo "📦 Installing Burnout Prediction System..."
echo "========================================="

# Change to script directory
cd "$(dirname "$0")"
cd ..

# Check Python installation and version
echo "🐍 Checking Python..."
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
    echo "✅ Found: $(python3.12 --version)"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
    echo "✅ Found: $(python3 --version)"
    
    # Check if it's Python 3.12
    if [[ "$PYTHON_VERSION" != "3.12" ]]; then
        echo "⚠️ Warning: Python 3.12 recommended for best compatibility"
        echo "Found: Python $PYTHON_VERSION"
        echo
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Installation cancelled. Please install Python 3.12"
            exit 1
        fi
    fi
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "⚠️ Found: $(python --version)"
    echo "Warning: 'python' command found, but 'python3' preferred"
else
    echo "❌ Python not found. Please install Python 3.12"
    echo "   Ubuntu/Debian: sudo apt install python3.12 python3.12-pip python3.12-venv"
    echo "   macOS: brew install python@3.12"
    exit 1
fi

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