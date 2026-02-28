#!/bin/bash
# SLTK Chatbot - Setup Virtual Environment on IBM i
# This script creates a Python virtual environment and installs all dependencies

echo "=========================================="
echo "  SLTK Chatbot - Virtual Environment Setup"
echo "=========================================="
echo ""

# Navigate to the SLTK directory
cd /home/VIJAYVERMA/SLTK

# Step 1: Create virtual environment
echo "Step 1: Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    echo "Try: yum install python313-pip"
    exit 1
fi

echo "✅ Virtual environment created: /home/VIJAYVERMA/SLTK/venv"
echo ""

# Step 2: Activate virtual environment
echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo "✅ Virtual environment activated"
echo ""

# Step 3: Upgrade pip
echo "Step 3: Upgrading pip..."
pip install --upgrade pip

echo ""

# Step 4: Install required packages
echo "Step 4: Installing required packages..."
echo "This may take a few minutes..."
echo ""

pip install \
    Flask==3.0.0 \
    Flask-CORS==4.0.0 \
    Flask-SocketIO==5.3.5 \
    python-socketio==5.10.0 \
    pandas==2.1.4 \
    openpyxl==3.1.2 \
    pyodbc==5.0.1 \
    python-dotenv==1.0.0

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Installation failed!"
    exit 1
fi

echo ""
echo "=========================================="
echo "  Verifying Installation"
echo "=========================================="
echo ""

# Verify each package
python << EOF
import sys
print("Python version:", sys.version)
print("\nInstalled packages:")

try:
    import flask
    print("  ✅ Flask:", flask.__version__)
except ImportError:
    print("  ❌ Flask: NOT INSTALLED")

try:
    import pandas
    print("  ✅ Pandas:", pandas.__version__)
except ImportError:
    print("  ❌ Pandas: NOT INSTALLED")

try:
    import openpyxl
    print("  ✅ openpyxl:", openpyxl.__version__)
except ImportError:
    print("  ❌ openpyxl: NOT INSTALLED")

try:
    import pyodbc
    print("  ✅ pyodbc:", pyodbc.version)
except ImportError:
    print("  ❌ pyodbc: NOT INSTALLED")

try:
    import flask_socketio
    print("  ✅ Flask-SocketIO: INSTALLED")
except ImportError:
    print("  ❌ Flask-SocketIO: NOT INSTALLED")
EOF

echo ""
echo "=========================================="
echo "  ✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To run the application:"
echo ""
echo "  1. Activate virtual environment:"
echo "     source /home/VIJAYVERMA/SLTK/venv/bin/activate"
echo ""
echo "  2. Run the app:"
echo "     python app.py"
echo ""
echo "  3. To deactivate virtual environment:"
echo "     deactivate"
echo ""

