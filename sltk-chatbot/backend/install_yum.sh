#!/bin/bash
# SLTK Chatbot - Install using YUM (IBM i Package Manager)
# This is the EASIEST method for IBM i

echo "=========================================="
echo "  SLTK Chatbot - YUM Installation"
echo "=========================================="
echo ""
echo "This script will install Python packages using IBM i's package manager (yum)"
echo "This is the recommended method for IBM i systems"
echo ""

# Install system packages using yum
echo "Installing Python packages via yum..."
echo ""

echo "Installing Flask..."
yum install -y python313-flask

echo "Installing pandas..."
yum install -y python313-pandas

echo "Installing openpyxl..."
yum install -y python313-openpyxl || echo "⚠️  openpyxl not available via yum"

echo "Installing pyodbc..."
yum install -y python313-pyodbc || echo "⚠️  pyodbc not available via yum"

echo ""
echo "Installing additional packages via pip (in venv)..."
echo ""

cd /home/VIJAYVERMA/SLTK

# Create venv for packages not available via yum
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Install remaining packages
pip install --no-cache-dir Flask-CORS Flask-SocketIO python-socketio python-dotenv

# If openpyxl wasn't installed via yum, install via pip
python -c "import openpyxl" 2>/dev/null || pip install --no-cache-dir openpyxl

echo ""
echo "=========================================="
echo "  Verifying Installation"
echo "=========================================="
echo ""

python << 'EOF'
packages = [
    ('flask', 'Flask'),
    ('pandas', 'pandas'),
    ('openpyxl', 'openpyxl'),
    ('pyodbc', 'pyodbc'),
    ('flask_cors', 'Flask-CORS'),
    ('flask_socketio', 'Flask-SocketIO'),
]

for module, name in packages:
    try:
        mod = __import__(module)
        version = getattr(mod, '__version__', 'installed')
        print(f"  ✅ {name}: {version}")
    except ImportError:
        print(f"  ❌ {name}: NOT INSTALLED")
EOF

echo ""
echo "=========================================="
echo "  Installation Complete!"
echo "=========================================="
echo ""
echo "To run the application:"
echo "  cd /home/VIJAYVERMA/SLTK"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""

