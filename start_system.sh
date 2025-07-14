#!/bin/bash

echo "🏥 Starting Healthcare Brain Tumor Detection System..."
echo "=================================================="

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "❌ MongoDB is not running!"
    echo "💡 Please start MongoDB first:"
    echo "   - macOS: brew services start mongodb/brew/mongodb-community"
    echo "   - Linux: sudo systemctl start mongod"
    echo "   - Windows: net start MongoDB"
    exit 1
fi

echo "✅ MongoDB is running"

# Function to run backend
start_backend() {
    echo "🔧 Starting Flask Backend..."
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    echo "📥 Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Start Flask server
    echo "🚀 Starting Flask server on http://localhost:5000"
    python app.py &
    BACKEND_PID=$!
    echo $BACKEND_PID > backend.pid
    cd ..
}

# Function to run frontend
start_frontend() {
    echo "⚛️  Starting React Frontend..."
    cd frontend
    
    # Install dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        echo "📥 Installing Node.js dependencies..."
        npm install
    fi
    
    # Start React server
    echo "🚀 Starting React server on http://localhost:3000"
    npm start &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > frontend.pid
    cd ..
}

# Cleanup function
cleanup() {
    echo "🛑 Stopping servers..."
    if [ -f "backend/backend.pid" ]; then
        kill $(cat backend/backend.pid) 2>/dev/null
        rm backend/backend.pid
    fi
    if [ -f "frontend/frontend.pid" ]; then
        kill $(cat frontend/frontend.pid) 2>/dev/null
        rm frontend/frontend.pid
    fi
    echo "✅ Servers stopped"
    exit 0
}

# Handle Ctrl+C
trap cleanup SIGINT

# Start services
start_backend
sleep 5  # Wait for backend to start
start_frontend

echo ""
echo "🎉 System is starting up!"
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend:  http://localhost:5000"
echo ""
echo "🔑 Login Credentials:"
echo "   Admin:   admin@healthcare.com / admin123"
echo "   Doctor:  doctor@healthcare.com / doctor123"
echo "   Patient: patient@healthcare.com / patient123"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for processes
wait