#!/bin/bash
# SLTK Chatbot - Step-by-Step Installation for IBM i
# This script installs packages one by one to avoid build issues

echo "=========================================="
echo "  SLTK Chatbot - Step-by-Step Installation"
echo "=========================================="
echo ""

cd /home/VIJAYVERMA/SLTK

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo ""

# Install packages one by one
echo "Installing packages (this may take a while)..."
echo ""

echo "1/8 Installing Flask..."
pip install Flask==3.0.0 --no-cache-dir
echo ""

echo "2/8 Installing Flask-CORS..."
pip install Flask-CORS==4.0.0 --no-cache-dir
echo ""

echo "3/8 Installing python-socketio..."
pip install python-socketio==5.10.0 --no-cache-dir
echo ""

echo "4/8 Installing Flask-SocketIO..."
pip install Flask-SocketIO==5.3.5 --no-cache-dir
echo ""

echo "5/8 Installing openpyxl..."
pip install openpyxl==3.1.2 --no-cache-dir
echo ""

echo "6/8 Installing python-dotenv..."
pip install python-dotenv==1.0.0 --no-cache-dir
echo ""

echo "7/8 Installing pyodbc..."
pip install pyodbc==5.0.1 --no-cache-dir || echo "⚠️  pyodbc failed, trying without version..."
pip install pyodbc --no-cache-dir || echo "⚠️  pyodbc installation failed (optional)"
echo ""

echo "8/8 Installing pandas (may take a while)..."
# Try to install pandas without building from source
pip install pandas --only-binary=:all: --no-cache-dir 2>/dev/null || {
    echo "⚠️  Pre-built pandas not available, trying older version..."
    pip install pandas==1.5.3 --no-cache-dir 2>/dev/null || {
        echo "⚠️  Pandas installation failed"
        echo "    The app will work without pandas for basic features"
    }
}
echo ""

echo "=========================================="
echo "  Verifying Installation"
echo "=========================================="
echo ""

python << 'EOF'
import sys
print("Python version:", sys.version)
print("\nInstalled packages:\n")

packages = [
    ('flask', 'Flask'),
    ('flask_cors', 'Flask-CORS'),
    ('flask_socketio', 'Flask-SocketIO'),
    ('socketio', 'python-socketio'),
    ('openpyxl', 'openpyxl'),
    ('dotenv', 'python-dotenv'),
    ('pyodbc', 'pyodbc'),
    ('pandas', 'pandas')
]

installed = []
missing = []

for module, name in packages:
    try:
        mod = __import__(module)
        version = getattr(mod, '__version__', 'installed')
        print(f"  ✅ {name}: {version}")
        installed.append(name)
    except ImportError:
        print(f"  ❌ {name}: NOT INSTALLED")
        missing.append(name)

print(f"\n{len(installed)}/{len(packages)} packages installed successfully")

if 'pandas' in missing:
    print("\n⚠️  WARNING: pandas is not installed")
    print("   Excel upload will not work without pandas")
    print("   Try: yum install python313-pandas")

if 'pyodbc' in missing:
    print("\n⚠️  WARNING: pyodbc is not installed")
    print("   Database features will not work without pyodbc")
    print("   Try: yum install python313-pyodbc")
EOF

echo ""
echo "=========================================="
echo "  Installation Complete!"
echo "=========================================="
echo ""
echo "To run the application:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""

