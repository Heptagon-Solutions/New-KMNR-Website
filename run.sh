#!/bin/bash

clear


# Function to kill processes on a specific port (silent)
kill_port() {
    local port=$1
    local pids=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pids" ]; then
        kill -9 $pids 2>/dev/null
        sleep 1
    fi
}

# Cleanup ports
echo "Cleaning ports..."
kill_port 5001
kill_port 4200

# Start Flask backend in background (suppress output)
echo "Starting Flask backend..."
cd backend
pipenv run flask run --host=0.0.0.0 --port=5001 >/dev/null 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
sleep 2

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "Failed to start backend"
    exit 1
fi

# Start Angular frontend
echo "Preparing Angular frontend..."
cd ../frontend

echo ""
echo "Services ready:"
echo "   Backend:  http://localhost:5001"
echo "   Frontend: http://localhost:4200"
echo ""
echo "Press Ctrl+C to stop all services"

# Trap Ctrl+C to clean up background processes
trap 'echo ""; echo "Stopping services..."; kill $BACKEND_PID 2>/dev/null; kill_port 5001; kill_port 4200; exit 0' INT

# Start Angular with suppressed output except for ready message
npm start 2>/dev/null | grep -E "(Local:|compiled|ERROR)" || true

# If we get here, Angular exited - clean up backend
kill $BACKEND_PID 2>/dev/null