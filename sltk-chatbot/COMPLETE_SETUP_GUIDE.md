# 🚀 SLTK Chatbot - Complete Setup Guide

## 📋 **Overview**

This guide will help you deploy the complete SLTK Upload Chatbot system:
- **Backend:** Flask API on IBM i (Port 44001)
- **Frontend:** React UI on Windows Server (http://ae1dcvpap23919/)

---

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────┐
│  User's Browser                                     │
│  └── http://ae1dcvpap23919/                         │
└─────────────────────────────────────────────────────┘
                    ↓ HTTP/WebSocket
┌─────────────────────────────────────────────────────┐
│  Windows Server (ae1dcvpap23919)                    │
│  ├── React Frontend (IIS/Node.js)                   │
│  │   ├── File upload UI                             │
│  │   ├── Real-time status monitoring                │
│  │   └── Error display                              │
│  └── Calls IBM i API                                │
└─────────────────────────────────────────────────────┘
                    ↓ HTTP (Port 44001)
┌─────────────────────────────────────────────────────┐
│  IBM i Server                                       │
│  ├── Flask Backend (Port 44001)                     │
│  │   ├── /upload/excel - File upload endpoint       │
│  │   ├── /api/status - Status monitoring            │
│  │   ├── /api/errors - Error retrieval              │
│  │   └── WebSocket - Real-time updates              │
│  ├── IFS Dropbox Folders                            │
│  │   ├── /sltk/dropbox/MODATA/                      │
│  │   ├── /sltk/dropbox/DEMOITM/                     │
│  │   └── /HOME/VIJAYVERMA/ (POC)                    │
│  └── SLTK Tables (ASHLEY library)                   │
│      ├── SLTKLOD - Load definitions                 │
│      ├── SLTKGRP - Group status                     │
│      └── SLTKERR - Error messages                   │
└─────────────────────────────────────────────────────┘
```

---

## 📦 **Part 1: IBM i Backend Setup**

### **Step 1: Verify Backend is Running**

On IBM i:
```bash
cd /home/VIJAYVERMA/SLTK
source venv/bin/activate
python app.py
```

**Expected Output:**
```
⚠️  WARNING: pandas not available
✅ Using openpyxl as fallback
⚠️  WARNING: pyodbc not available - database features disabled

============================================================
  SLTK Upload Chatbot - Flask API
============================================================
  Port: 44001
  Dropbox Root: /sltk/dropbox
  POC Folder: /HOME/VIJAYVERMA
  SLTK Library: ASHLEY
============================================================

✅ POC dropbox folder verified: /HOME/VIJAYVERMA
⚠️  WARNING: pyodbc not available - database features disabled

🚀 Starting server...
 * Running on http://0.0.0.0:44001
```

### **Step 2: Test Backend from IBM i**

```bash
# In another terminal
curl http://localhost:44001/
```

**Expected Response:**
```json
{
  "status": "running",
  "message": "SLTK Monitor API is operational",
  "endpoints": [...]
}
```

### **Step 3: Find IBM i Hostname**

```bash
hostname
# Example: ibmi-prod.ashley.com
```

**Save this hostname - you'll need it for the frontend!**

---

## 🪟 **Part 2: Windows Server Frontend Setup**

### **Step 1: Transfer Files to Windows Server**

Copy the `sltk-chatbot/frontend` folder to your Windows server:

```powershell
# Option A: Via network share
Copy-Item -Path "\\your-pc\share\sltk-chatbot\frontend" -Destination "C:\inetpub\wwwroot\sltk-chatbot" -Recurse

# Option B: Via Git (if you have a repo)
cd C:\inetpub\wwwroot
git clone <your-repo-url> sltk-chatbot
```

### **Step 2: Run Deployment Script**

```powershell
# Navigate to frontend folder
cd C:\inetpub\wwwroot\sltk-chatbot\frontend

# Run deployment script (replace with your IBM i hostname)
.\deploy-windows.ps1 -IBMiHostname "your-ibmi-hostname"

# Example:
.\deploy-windows.ps1 -IBMiHostname "ibmi-prod.ashley.com"
```

This script will:
- ✅ Check Node.js installation
- ✅ Create `.env.production` with your IBM i hostname
- ✅ Install dependencies
- ✅ Build production bundle
- ✅ Create IIS configuration

### **Step 3: Deploy to IIS**

1. **Open IIS Manager** (Start → IIS Manager)

2. **Create New Website:**
   - Right-click "Sites" → "Add Website"
   - **Site name:** `SLTK-Chatbot`
   - **Physical path:** `C:\inetpub\wwwroot\sltk-chatbot\frontend\dist`
   - **Binding:**
     - Type: `http`
     - IP: `All Unassigned`
     - Port: `80`
     - Host name: `ae1dcvpap23919` (or leave blank)

3. **Click OK**

4. **Start the website** (if not already started)

### **Step 4: Configure Firewall**

```powershell
# Allow HTTP traffic on port 80
New-NetFirewallRule -DisplayName "SLTK Chatbot HTTP" -Direction Inbound -LocalPort 80 -Protocol TCP -Action Allow
```

---

## 🧪 **Part 3: Testing**

### **Test 1: Backend Connectivity from Windows**

```powershell
# Test from Windows Server
curl http://your-ibmi-hostname:44001/
```

**Expected:** JSON response with `"status": "running"`

### **Test 2: Access Frontend**

Open browser: `http://ae1dcvpap23919/`

You should see:
- ✅ SLTK Upload Chatbot header
- ✅ "Connected" status (green checkmark)
- ✅ Upload button

### **Test 3: Upload a File**

1. Create a test Excel file (e.g., `test.xlsx`)
2. Click "Upload Excel File"
3. Select the file
4. Click "Upload"
5. Check IBM i: `ls -la /HOME/VIJAYVERMA/`

**Expected:** File should appear in the IFS folder

---

## 🔧 **Troubleshooting**

### **Issue: Frontend shows "Disconnected"**

**Cause:** Can't reach IBM i backend

**Fix:**
```powershell
# Test connectivity
Test-NetConnection -ComputerName your-ibmi-hostname -Port 44001

# If fails, check:
# 1. IBM i backend is running
# 2. Port 44001 is open on IBM i
# 3. Network connectivity between Windows and IBM i
```

### **Issue: CORS errors in browser console**

**Cause:** Cross-origin request blocked

**Fix:** Backend already has CORS enabled. Check browser console for actual error.

### **Issue: File upload fails**

**Check:**
1. IBM i backend logs
2. IFS folder permissions: `chmod 755 /HOME/VIJAYVERMA`
3. Browser network tab for error details

---

## 📝 **Summary Checklist**

### IBM i Backend:
- [ ] Flask backend running on port 44001
- [ ] Can access `http://localhost:44001/` from IBM i
- [ ] IFS folder `/HOME/VIJAYVERMA` exists and is writable

### Windows Server Frontend:
- [ ] Files copied to `C:\inetpub\wwwroot\sltk-chatbot\frontend`
- [ ] Deployment script executed successfully
- [ ] IIS website created and running
- [ ] Can access `http://ae1dcvpap23919/` from browser

### Connectivity:
- [ ] Windows can reach IBM i on port 44001
- [ ] Frontend shows "Connected" status
- [ ] File upload works

---

## 🎯 **Next Steps**

1. ✅ **Test with real SLTK files** - Upload actual Excel files
2. ✅ **Install pandas/pyodbc** - Enable full features (database monitoring)
3. ✅ **Configure SSL** - Add HTTPS for production
4. ✅ **Setup auto-start** - Configure backend to start on IBM i boot

---

## 📞 **Support**

If you encounter issues:
1. Check IBM i backend logs
2. Check Windows IIS logs: `C:\inetpub\logs\LogFiles`
3. Check browser console (F12)

---

**You're all set! 🎉**

Access your SLTK Chatbot at: `http://ae1dcvpap23919/`

