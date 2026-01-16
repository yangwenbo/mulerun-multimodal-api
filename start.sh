#!/bin/bash
# Video Generation Client Startup Script

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Checking dependencies..."
if [ -f "pyproject.toml" ]; then
    pip install -q -e .
else
    pip install -q -r requirements.txt
fi

# Run the application
echo "Starting Video Generation Client..."
python main.py
