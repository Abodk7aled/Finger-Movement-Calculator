#!/bin/bash

# Finger Movement Calculator - Startup Script
# This script sets up and launches the Finger Movement Calculator application

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================="
echo "  Finger Movement Calculator"
echo "========================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed.${NC}"
    echo "Please install Python 3.7 or higher and try again."
    exit 1
fi

# Display Python version
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓${NC} Found $PYTHON_VERSION"

# Check if virtual environment exists, if not offer to create one
if [ ! -d "venv" ]; then
    echo ""
    echo -e "${YELLOW}No virtual environment found.${NC}"
    read -p "Would you like to create one? (recommended) [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓${NC} Virtual environment created successfully"
        else
            echo -e "${RED}Error: Failed to create virtual environment${NC}"
            exit 1
        fi
    fi
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo -e "${GREEN}✓${NC} Virtual environment activated"
fi

# Check if requirements are installed
echo ""
echo "Checking dependencies..."
if [ -f "requirements.txt" ]; then
    pip3 install -q -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} All dependencies are installed"
    else
        echo -e "${RED}Error: Failed to install dependencies${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}Warning: requirements.txt not found${NC}"
fi

# Check if webcam is accessible (Linux-specific)
if [ -e /dev/video0 ]; then
    echo -e "${GREEN}✓${NC} Webcam detected"
else
    echo -e "${YELLOW}Warning: No webcam detected at /dev/video0${NC}"
    echo "The application may not work properly without a webcam."
fi

# Launch the application
echo ""
echo "========================================="
echo "  Starting Finger Movement Calculator..."
echo "========================================="
echo ""
echo "Instructions:"
echo "  - Use pinch gesture (index + middle finger) to click"
echo "  - Press ESC to exit"
echo ""

# Add src directory to Python path and run the application
export PYTHONPATH="${SCRIPT_DIR}/src:${PYTHONPATH}"
cd src
python3 main.py

# Capture exit code
EXIT_CODE=$?

# Deactivate virtual environment if it was activated
if [ -d "../venv" ]; then
    deactivate 2>/dev/null
fi

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}Application closed successfully${NC}"
else
    echo -e "${RED}Application exited with error code: $EXIT_CODE${NC}"
fi

exit $EXIT_CODE
