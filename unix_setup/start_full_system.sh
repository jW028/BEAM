#!/bin/bash
# Start the complete Burnout Prediction System on Unix/Linux/macOS

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_status "🚀 Starting Burnout Prediction System..."
echo "======================================"

# Change to script directory
cd "$(dirname "$0")"
cd ..

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found. Please run ./unix_setup/install_dependencies.sh first"
    exit 1
fi

# Activate virtual environment
print_status "� Activating virtual environment..."
source venv/bin/activate

# Check if model exists
if [ ! -f "models/burnout_prediction_model.pkl" ]; then
    print_status "🤖 Training model (first time setup)..."
    python burnout_prediction_model.py
    if [ $? -ne 0 ]; then
        print_error "Model training failed"
        exit 1
    fi
    print_success "Model trained successfully!"
fi

# Function to cleanup background processes
cleanup() {
    print_status "🛑 Shutting down services..."
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null
        print_status "API server stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        print_status "Frontend server stopped"
    fi
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM EXIT

# Start API server in background
print_status "🔧 Starting API server on http://localhost:8000..."
cd api
python -m uvicorn app:app --host 0.0.0.0 --port 8000 &
API_PID=$!
cd ..

# Wait for API to start
sleep 3

# Check if API is running
if ! kill -0 $API_PID 2>/dev/null; then
    print_error "API server failed to start"
    exit 1
fi

# Start frontend server in background
print_status "🌐 Starting frontend server on http://localhost:3000..."
cd frontend
python server.py &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 2

# Check if frontend is running
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    print_error "Frontend server failed to start"
    cleanup
    exit 1
fi

print_success "🎉 System is now running!"
echo
echo "📱 Access Points:"
echo "  🌐 Frontend:       http://localhost:3000"
echo "  🔧 API:           http://localhost:8000"
echo "  📚 API Docs:      http://localhost:8000/docs"
echo "  📖 ReDoc:         http://localhost:8000/redoc"
echo
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
wait
