#!/bin/bash

# Quick start script for the API

echo "🚀 Starting Burnout Prediction API..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the FastAPI server
cd ../api && uvicorn app:app --host 0.0.0.0 --port 8000 --reload
