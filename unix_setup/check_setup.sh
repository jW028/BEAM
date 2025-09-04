#!/bin/bash

echo "🔍 Checking Burnout Prediction System Setup..."
echo "================================================="

# Check if model exists
if [ -f "models/burnout_prediction_model.pkl" ]; then
    echo "✅ Model file found"
else
    echo "❌ Model file missing - run: python burnout_prediction_model.py"
fi

# Check if API directory exists
if [ -d "api" ]; then
    echo "✅ API directory found"
    if [ -f "api/app.py" ]; then
        echo "✅ API app found"
    else
        echo "❌ API app missing"
    fi
else
    echo "❌ API directory missing"
fi

# Check if frontend directory exists
if [ -d "frontend" ]; then
    echo "✅ Frontend directory found"
    if [ -f "frontend/index.html" ]; then
        echo "✅ Frontend HTML found"
    else
        echo "❌ Frontend HTML missing"
    fi
    if [ -f "frontend/server.py" ]; then
        echo "✅ Frontend server found"
    else
        echo "❌ Frontend server missing"
    fi
else
    echo "❌ Frontend directory missing"
fi

# Check Python dependencies
echo ""
echo "🐍 Checking Python dependencies..."
python3 -c "
try:
    import fastapi, uvicorn, pandas, numpy, xgboost, sklearn, joblib
    print('✅ All required packages installed')
except ImportError as e:
    print(f'❌ Missing package: {e}')
    print('Run: pip install -r requirements.txt')
"

echo ""
echo "📋 Quick Start Commands:"
echo "========================"
echo "1. Train model:      python burnout_prediction_model.py"
echo "2. Start full system: ./start_full_system.sh"
echo "3. API only:         ./start_api.sh"
echo "4. Test API:         python test_api.py"