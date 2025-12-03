#!/bin/bash

# KMNR Website Stop Script
echo "🛑 Stopping KMNR Website..."

# Stop Docker containers
docker compose down --remove-orphans

# Kill any lingering processes on our ports
echo "🧹 Cleaning up any remaining processes..."

# Function to kill processes on a port
kill_port() {
    local port=$1
    local pids=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pids" ]; then
        echo "Killing processes on port $port: $pids"
        kill -9 $pids 2>/dev/null
    fi
}

kill_port 3000
kill_port 5000
kill_port 3306

echo "✅ All services stopped"