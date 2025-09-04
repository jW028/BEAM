#!/bin/bash

# Burnout Prediction API Startup Script

echo "🚀 Starting Burnout Prediction API Setup..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📚 Installing requirements..."
pip install -r requirements.txt

# Check if model exists
if [ ! -f "models/burnout_prediction_model.pkl" ]; then
    echo "❌ Model file not found at models/burnout_prediction_model.pkl"
    echo "Please run the training script first to generate the model:"
    echo "python burnout_prediction_model.py"
    exit 1
fi

echo "✅ Setup complete!"
echo ""
echo "To start the API server, run:"
echo "cd api && uvicorn app:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "Or use the quick start command:"
echo "./start_api.sh"
