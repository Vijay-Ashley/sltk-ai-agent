# 🚀 Installing SLTK Chatbot on IBM i (Python 3.13)

## ⚠️ Important: Python 3.13 Uses Virtual Environments

IBM i with Python 3.13 requires using **virtual environments** (PEP 668). You cannot install packages system-wide with pip.

---

## Quick Start

### **Option 1: Automated Setup** ⭐ **RECOMMENDED**

```bash
# 1. Navigate to backend folder
cd /home/VIJAYVERMA/SLTK

# 2. Make setup script executable
chmod +x setup_venv.sh

# 3. Run setup script (creates venv and installs packages)
./setup_venv.sh

# 4. Run the application
./start.sh
```

**That's it!** The setup script will:
- ✅ Create virtual environment
- ✅ Install all required packages
- ✅ Verify installation
- ✅ Show you how to run the app

---

### **Option 2: Manual Setup**

```bash
# 1. Navigate to backend folder
cd /home/VIJAYVERMA/SLTK

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Upgrade pip
pip install --upgrade pip

# 5. Install packages
pip install Flask Flask-CORS Flask-SocketIO python-socketio pandas openpyxl pyodbc python-dotenv

# 6. Verify installation
python -c "import flask; print('Flask OK')"
python -c "import pandas; print('Pandas OK')"

# 7. Run the application
python app.py

# 8. To stop: Press Ctrl+C
# 9. To deactivate venv: deactivate
```

---

## 🎯 Daily Usage

Once setup is complete, use these commands:

### **Start the Application**
```bash
cd /home/VIJAYVERMA/SLTK
./start.sh
```

**OR manually:**
```bash
cd /home/VIJAYVERMA/SLTK
source venv/bin/activate
python app.py
```

### **Stop the Application**
```bash
# Press Ctrl+C in the terminal
```

### **Deactivate Virtual Environment**
```bash
deactivate
```

---

## 📋 Prerequisites

### **1. Python 3.6+**
```bash
python3 --version
# Should show: Python 3.6.x or higher
```

If Python is not installed:
```bash
# Contact your IBM i administrator to install Python
# Or install via ACS (Access Client Solutions)
```

### **2. IBM i Access ODBC Driver**
```bash
# Check if ODBC driver is installed
ls /QIBM/ProdData/Access/ACS/Base/
```

If not installed, download from:
- IBM i Access Client Solutions (ACS)
- https://www.ibm.com/support/pages/ibm-i-access-client-solutions

---

## 🔧 Troubleshooting

### **Error: ModuleNotFoundError: No module named 'flask'**

**Solution:**
```bash
python3 -m pip install --user Flask
```

### **Error: Permission denied**

**Solution:** Use `--user` flag:
```bash
python3 -m pip install --user Flask pandas openpyxl pyodbc
```

### **Error: pip not found**

**Solution:** Install pip:
```bash
python3 -m ensurepip --upgrade
```

### **Error: SSL Certificate verification failed**

**Solution:** Use trusted host:
```bash
python3 -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org Flask pandas
```

### **Error: pyodbc installation fails**

**Solution 1:** Check if ODBC driver is installed:
```bash
ls /QIBM/ProdData/Access/ACS/Base/
```

**Solution 2:** Install from IBM i repos:
```bash
yum install python3-pyodbc
```

**Solution 3:** Skip pyodbc for now (database features won't work):
```bash
python3 -m pip install --user Flask Flask-CORS pandas openpyxl
```

### **Error: Port 44001 already in use**

**Solution:** Change port in `app.py`:
```python
PORT = 44002  # Or any available port
```

---

## ✅ Verify Installation

Run this command to check all packages:

```bash
python3 << EOF
import sys
print("Python version:", sys.version)
print("\nChecking packages...")

try:
    import flask
    print("✅ Flask:", flask.__version__)
except ImportError:
    print("❌ Flask: NOT INSTALLED")

try:
    import pandas
    print("✅ Pandas:", pandas.__version__)
except ImportError:
    print("❌ Pandas: NOT INSTALLED")

try:
    import openpyxl
    print("✅ openpyxl:", openpyxl.__version__)
except ImportError:
    print("❌ openpyxl: NOT INSTALLED")

try:
    import pyodbc
    print("✅ pyodbc:", pyodbc.version)
except ImportError:
    print("❌ pyodbc: NOT INSTALLED")

try:
    import flask_socketio
    print("✅ Flask-SocketIO: INSTALLED")
except ImportError:
    print("❌ Flask-SocketIO: NOT INSTALLED")
EOF
```

---

## 🎯 Next Steps

Once all packages are installed:

1. **Update Configuration** (in `app.py`):
   ```python
   SLTK_LIBRARY = 'ASHLEY'  # Your SLTK library
   UID = 'VIJAYVERMA'       # Your IBM i user
   PWD = 'COSTARIC1'        # Your password
   ```

2. **Run the Application**:
   ```bash
   python3 app.py
   ```

3. **Test the API**:
   ```bash
   curl http://localhost:44001/
   ```

4. **Access from Browser**:
   - Open: `http://your-ibmi-hostname:44001/`

---

## 📞 Need Help?

If you encounter issues:

1. Check Python version: `python3 --version`
2. Check pip version: `python3 -m pip --version`
3. Check installed packages: `python3 -m pip list`
4. Check error logs in the terminal

**Common Commands:**
```bash
# List installed packages
python3 -m pip list

# Uninstall a package
python3 -m pip uninstall Flask

# Reinstall a package
python3 -m pip install --force-reinstall Flask
```

