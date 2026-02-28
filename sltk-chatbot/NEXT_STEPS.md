# 🚀 SLTK Chatbot - Next Steps

## ✅ **What's Done:**

1. ✅ Code pushed to GitHub: `https://github.com/Vijay-Ashley/sltk-ai-agent.git`
2. ✅ Code cloned on Windows Server: `C:\sltk-ai-agent\`
3. ✅ Frontend configured for port 8001
4. ✅ Backend ready for IBM i (port 44001)

---

## 📋 **On Windows Server (ae1dcvpap23919):**

### **Current Location:**
```
C:\sltk-ai-agent\sltk-chatbot\frontend>
```

### **Next Commands to Run:**

#### **1. Create .env file with IBM i hostname:**

```cmd
echo VITE_API_URL=http://your-ibmi-hostname:44001 > .env
```

**Replace `your-ibmi-hostname`** with your actual IBM i hostname or IP address.

**Examples:**
```cmd
REM If you know the hostname:
echo VITE_API_URL=http://ibmi-prod.ashley.com:44001 > .env

REM If you know the IP:
echo VITE_API_URL=http://192.168.1.100:44001 > .env
```

#### **2. Install dependencies:**

```cmd
npm install
```

This will take a few minutes to download all packages.

#### **3. Start the frontend server:**

```cmd
start-windows.bat
```

Or:
```cmd
npm run dev
```

#### **4. Configure firewall (PowerShell as Admin):**

```powershell
New-NetFirewallRule -DisplayName "SLTK Chatbot Frontend" `
    -Direction Inbound `
    -LocalPort 8001 `
    -Protocol TCP `
    -Action Allow
```

#### **5. Access the UI:**

**From Windows Server:**
```
http://localhost:8001
```

**From other computers:**
```
http://ae1dcvpap23919:8001
```

---

## 📋 **On IBM i:**

### **1. Clone the repository:**

```bash
cd /home/VIJAYVERMA
git clone https://github.com/Vijay-Ashley/sltk-ai-agent.git
cd sltk-ai-agent/sltk-chatbot/backend
```

### **2. Setup virtual environment:**

```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

### **3. Start the backend:**

```bash
source venv/bin/activate
python app.py
```

**Expected output:**
```
✅ POC dropbox folder verified: /HOME/VIJAYVERMA
⚠️  WARNING: pyodbc not available - database features disabled

🚀 Starting server...
 * Running on http://0.0.0.0:44001
```

---

## 🧪 **Testing:**

### **Test 1: Check IBM i Backend**

From IBM i or Windows:
```bash
curl http://ibmi-hostname:44001/
```

Should return JSON with status "running".

### **Test 2: Check Windows Frontend**

Open browser:
```
http://ae1dcvpap23919:8001
```

Should show the SLTK Upload Chatbot UI.

### **Test 3: Upload a File**

1. Open the UI
2. Click "Upload Excel File"
3. Select a test Excel file
4. Click "Upload"
5. File should be uploaded to IBM i

---

## 📁 **File Structure:**

```
Windows Server (C:\sltk-ai-agent\)
└── sltk-chatbot/
    ├── frontend/
    │   ├── .env                    ← Create this with IBM i hostname
    │   ├── start-windows.bat       ← Run this to start
    │   ├── package.json
    │   └── src/App.tsx
    │
    └── WINDOWS_SERVER_SETUP.md     ← Full setup guide

IBM i (/home/VIJAYVERMA/sltk-ai-agent/)
└── sltk-chatbot/
    ├── backend/
    │   ├── app.py                  ← Main Flask app
    │   ├── setup_venv.sh           ← Run this first
    │   ├── start.sh                ← Or use this to start
    │   └── requirements.txt
    │
    └── INSTALL_IBMI.md             ← Full setup guide
```

---

## 🎯 **Summary:**

| Task | Location | Status |
|------|----------|--------|
| Push to GitHub | ✅ Done | Complete |
| Clone on Windows | ✅ Done | Complete |
| Create .env | Windows Server | ⏳ **Next** |
| Install npm packages | Windows Server | ⏳ Pending |
| Start frontend | Windows Server | ⏳ Pending |
| Clone on IBM i | IBM i | ⏳ Pending |
| Setup venv | IBM i | ⏳ Pending |
| Start backend | IBM i | ⏳ Pending |

---

## 🆘 **Need Help?**

- **Windows Setup:** See `WINDOWS_SERVER_SETUP.md`
- **IBM i Setup:** See `backend/INSTALL_IBMI.md`
- **GitHub Deployment:** See `GITHUB_DEPLOYMENT.md`

---

## 🎊 **You're Almost There!**

**Next immediate step on Windows Server:**

```cmd
echo VITE_API_URL=http://your-ibmi-hostname:44001 > .env
npm install
start-windows.bat
```

**Then access:** `http://ae1dcvpap23919:8001` 🚀

