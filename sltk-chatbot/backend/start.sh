#!/bin/bash
# SLTK Chatbot - Start Script
# This script activates the virtual environment and starts the Flask app

cd /home/VIJAYVERMA/SLTK

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run setup_venv.sh first:"
    echo "  chmod +x setup_venv.sh"
    echo "  ./setup_venv.sh"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Run the Flask app
echo "Starting SLTK Chatbot API..."
python app.py

