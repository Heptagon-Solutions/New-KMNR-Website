#!/bin/bash

# KMNR Website Runner Script
# This script handles common port conflicts and Docker issues

echo "🎵 KMNR Website Startup Script 🎵"
echo "=================================="

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to kill processes on common ports
kill_port_processes() {
    local port=$1
    local pids=$(lsof -ti:$port 2>/dev/null)
    
    if [ ! -z "$pids" ]; then
        echo -e "${YELLOW}⚠️  Port $port is in use. Killing processes: $pids${NC}"
        for pid in $pids; do
            kill -9 $pid 2>/dev/null
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✅ Killed process $pid on port $port${NC}"
            fi
        done
        sleep 1
    else
        echo -e "${GREEN}✅ Port $port is available${NC}"
    fi
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}❌ Docker is not running. Please start Docker Desktop and try again.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Docker is running${NC}"
}

# Function to clean up Docker
cleanup_docker() {
    echo -e "${YELLOW}🧹 Cleaning up existing Docker containers...${NC}"
    docker compose down --remove-orphans 2>/dev/null || true
    
    # Remove any orphaned containers
    docker container prune -f > /dev/null 2>&1 || true
    
    echo -e "${GREEN}✅ Docker cleanup complete${NC}"
}

# Main execution
main() {
    echo "🔍 Checking prerequisites..."
    
    # Check if Docker is running
    check_docker
    
    # Clean up any existing Docker containers
    cleanup_docker
    
    # Check and free up common ports
    echo "🔍 Checking ports..."
    kill_port_processes 3000  # Frontend (Angular)
    kill_port_processes 5000  # Backend (Flask)
    kill_port_processes 3306  # Database (MySQL/MariaDB)
    
    # Wait a moment for ports to be fully released
    echo "⏳ Waiting for ports to be released..."
    sleep 2
    
    # Start the application
    echo -e "${GREEN}🚀 Starting KMNR Website...${NC}"
    echo "This will start:"
    echo "  - Frontend (Angular) on http://localhost:4200"
    echo "  - Backend (Flask) on http://localhost:5000" 
    echo "  - Database (MariaDB) on localhost:3306"
    echo ""
    echo "📱 Open http://localhost:4200 in your browser"
    echo "🛑 Press Ctrl+C to stop all services"
    echo ""
    
    # Start with watch mode for hot reloading
    docker compose up --watch
}

# Handle script interruption
trap 'echo -e "\n${YELLOW}🛑 Shutting down...${NC}"; docker compose down; exit 0' INT

# Run the main function
main