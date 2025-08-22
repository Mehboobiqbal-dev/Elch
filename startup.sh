#!/bin/bash

# Azure App Service Startup Script for Python FastAPI Application
# This script handles the initialization and startup of the Elch application

echo "Starting Elch application deployment..."

# Set environment variables for production
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONOPTIMIZE=2
export PYTHONHASHSEED=0
export ENVIRONMENT=production

# Set default port if not provided by Azure
if [ -z "$PORT" ]; then
    export PORT=8000
fi

echo "Environment: $ENVIRONMENT"
echo "Port: $PORT"
echo "Python version: $(python --version)"

# Create necessary directories
mkdir -p /home/site/wwwroot/logs
mkdir -p /home/site/wwwroot/saved_task_data
mkdir -p /home/site/wwwroot/scraped_data

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "Dependencies installed successfully"
else
    echo "Warning: requirements.txt not found"
fi

# Initialize database if init script exists
if [ -f "init_db_script.py" ]; then
    echo "Initializing database..."
    python init_db_script.py || echo "Database initialization completed with warnings"
else
    echo "No database initialization script found"
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found in the application directory"
    exit 1
fi

# Set up logging
echo "Setting up application logging..."
export PYTHONPATH="/home/site/wwwroot:$PYTHONPATH"

# Health check function
health_check() {
    local max_attempts=30
    local attempt=1
    
    echo "Performing health check..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "http://localhost:$PORT/healthz" > /dev/null 2>&1; then
            echo "Health check passed on attempt $attempt"
            return 0
        fi
        
        echo "Health check attempt $attempt failed, retrying in 2 seconds..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "Health check failed after $max_attempts attempts"
    return 1
}

# Start the application with gunicorn
echo "Starting FastAPI application with Gunicorn..."

# Use optimized gunicorn configuration for Azure App Service
exec gunicorn main:app \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output \
    --enable-stdio-inheritance