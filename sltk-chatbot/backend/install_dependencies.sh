#!/bin/bash
# SLTK Chatbot - Install Dependencies on IBM i
# Run this script to install all required Python packages

echo "=========================================="
echo "  SLTK Chatbot - Dependency Installation"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    exit 1
fi
echo ""

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip --user
echo ""

# Install packages
echo "Installing required packages..."
echo "This may take a few minutes..."
echo ""

python3 -m pip install --user \
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
    echo "Try running manually:"
    echo "  python3 -m pip install --user Flask pandas openpyxl pyodbc"
    exit 1
fi

echo ""
echo "=========================================="
echo "  Verifying Installation"
echo "=========================================="
echo ""

# Verify each package
echo "Checking Flask..."
python3 -c "import flask; print('  ✅ Flask version:', flask.__version__)"

echo "Checking pandas..."
python3 -c "import pandas; print('  ✅ Pandas version:', pandas.__version__)"

echo "Checking openpyxl..."
python3 -c "import openpyxl; print('  ✅ openpyxl version:', openpyxl.__version__)"

echo "Checking pyodbc..."
python3 -c "import pyodbc; print('  ✅ pyodbc version:', pyodbc.version)"

echo "Checking Flask-SocketIO..."
python3 -c "import flask_socketio; print('  ✅ Flask-SocketIO installed')"

echo ""
echo "=========================================="
echo "  ✅ Installation Complete!"
echo "=========================================="
echo ""
echo "You can now run the application:"
echo "  python3 app.py"
echo ""

