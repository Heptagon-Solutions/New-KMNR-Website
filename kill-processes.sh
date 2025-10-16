#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    source .env
else
    echo "Error: .env file not found. Please create one based on .env.example"
    exit 1
fi

# Kill processes on backend and frontend ports
echo ">>> Killing processes on backend port ${BACKEND_PORT}..."
pkill -f ":${BACKEND_PORT}"

echo ">>> Killing processes on frontend port ${FRONTEND_PORT}..."
pkill -f ":${FRONTEND_PORT}"

echo ">>> Process termination complete."