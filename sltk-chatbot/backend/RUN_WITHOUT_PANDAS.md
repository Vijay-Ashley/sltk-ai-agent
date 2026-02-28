# 🚀 Running SLTK Chatbot Without pandas/pyodbc

## ✅ **Good News!**

The app has been modified to run **without pandas and pyodbc**. It will work in limited mode with the packages you have installed.

---

## 📦 **What's Installed:**

✅ Flask  
✅ Flask-CORS  
✅ Flask-SocketIO  
✅ python-socketio  
✅ openpyxl  
✅ python-dotenv  

---

## ⚠️ **What's Missing:**

❌ pandas - Excel processing will be limited  
❌ pyodbc - Database features will be disabled  

---

## 🎯 **How to Run the App:**

```bash
cd /home/VIJAYVERMA/SLTK
source venv/bin/activate
python app.py
```

---

## 📋 **What Works:**

### ✅ **File Upload (Limited Mode)**
- Upload Excel files to IFS dropbox folder
- Files are saved as-is without pandas processing
- No timestamp column added (requires pandas)

### ✅ **Health Check**
- `GET /` - Server status check

### ❌ **Database Features (Disabled)**
- `GET /api/loads` - Requires pyodbc
- `GET /api/status/<groupId>` - Requires pyodbc
- `GET /api/errors/<groupId>` - Requires pyodbc
- `GET /api/history` - Requires pyodbc

---

## 🔧 **To Enable Full Features:**

### **Option 1: Install via YUM (if available)**
```bash
yum search python313 | grep pandas
yum search python313 | grep pyodbc

# If found:
yum install -y python313-pandas python313-pyodbc
```

### **Option 2: Install via pip (may fail on IBM i)**
```bash
source venv/bin/activate
pip install pandas pyodbc
```

### **Option 3: Use Alternative Libraries**
The app can work with just openpyxl for basic Excel operations.

---

## 🧪 **Testing the App:**

### **1. Start the Server**
```bash
cd /home/VIJAYVERMA/SLTK
source venv/bin/activate
python app.py
```

**Expected Output:**
```
⚠️  WARNING: pandas not available: No module named 'pandas'
   Excel upload feature will be limited
   To install: yum install python313-pandas
✅ Using openpyxl as fallback for Excel processing
⚠️  WARNING: pyodbc not available: No module named 'pyodbc'
   Database features will be disabled
   To install: yum install python313-pyodbc
   App will run in limited mode without database access
✅ SUCCESS: Flask imported successfully

==========================================================
  SLTK Upload Chatbot - Flask API
==========================================================
  Port: 44001
  Dropbox Root: /sltk/dropbox
  POC Folder: /HOME/VIJAYVERMA
  SLTK Library: ASHLEY
==========================================================

  Endpoints:
    Health check:  http://localhost:44001/
    Get Loads:     GET  http://localhost:44001/api/loads
    Upload:        POST http://localhost:44001/upload/excel
    Status:        GET  http://localhost:44001/api/status/<groupId>
    Errors:        GET  http://localhost:44001/api/errors/<groupId>
    History:       GET  http://localhost:44001/api/history
    WebSocket:     ws://localhost:44001/socket.io/
==========================================================

✅ POC dropbox folder verified: /HOME/VIJAYVERMA
⚠️  WARNING: pyodbc not available - database features disabled
   Install with: yum install python313-pyodbc

🚀 Starting server...

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:44001
```

### **2. Test Health Check**
```bash
curl http://localhost:44001/
```

**Expected Response:**
```json
{
  "status": "running",
  "message": "SLTK Monitor API is operational",
  "timestamp": "2024-02-28T10:30:00",
  "endpoints": [...]
}
```

### **3. Test File Upload**
```bash
curl -X POST http://localhost:44001/upload/excel \
  -F "excel_file=@test.xlsx"
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "File uploaded successfully",
  "filename": "test.xlsx",
  "path": "/HOME/VIJAYVERMA/test.xlsx"
}
```

---

## 📝 **Next Steps:**

1. ✅ **Run the app in limited mode** - Works for basic file uploads
2. ⏳ **Contact IBM i admin** - Request pandas/pyodbc installation
3. ⏳ **Test with real Excel files** - Upload to SLTK dropbox
4. ⏳ **Monitor SLTKDRP** - Verify files are processed

---

## 🆘 **Troubleshooting:**

### **Error: Address already in use**
```bash
# Change port in app.py
PORT = 44002  # Or any available port
```

### **Error: Permission denied on /HOME/VIJAYVERMA**
```bash
# Create folder manually
mkdir -p /HOME/VIJAYVERMA
chmod 755 /HOME/VIJAYVERMA
```

### **Error: Module not found**
```bash
# Make sure venv is activated
source venv/bin/activate
python app.py
```

---

## ✅ **Summary:**

- ✅ App will run without pandas/pyodbc
- ✅ File upload works (limited mode)
- ❌ Database features disabled
- ⏳ Install pandas/pyodbc later for full features

**The app is ready to run! Try it now:** 🚀

```bash
cd /home/VIJAYVERMA/SLTK
source venv/bin/activate
python app.py
```

