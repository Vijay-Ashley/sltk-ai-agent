# 🚀 Deploy SLTK Chatbot via GitHub

## 📋 **Overview**

This guide shows how to deploy the SLTK Chatbot by:
1. Pushing code to GitHub: `https://github.com/Vijay-Ashley/sltk-ai-agent.git`
2. Cloning on Windows Server (ae1dcvpap23919)
3. Cloning on IBM i

---

## 📦 **Part 1: Push Code to GitHub**

### **Step 1: Initialize Git (if not already done)**

```bash
# On your local machine (Windows)
cd "C:\Users\VVerma\OneDrive - Ashley Furniture Industries, Inc\Documents\IBMI"

# Check if git is initialized
git status

# If not initialized:
git init
git remote add origin https://github.com/Vijay-Ashley/sltk-ai-agent.git
```

### **Step 2: Create .gitignore**

Make sure you have a `.gitignore` file to exclude unnecessary files:

```gitignore
# See .gitignore file in the repo
```

### **Step 3: Commit and Push**

```bash
# Add all files
git add .

# Commit
git commit -m "Add SLTK Chatbot - Backend and Frontend"

# Push to GitHub
git push -u origin main
```

---

## 🪟 **Part 2: Deploy Frontend on Windows Server**

### **Step 1: Clone Repository on Windows Server**

```powershell
# On Windows Server (ae1dcvpap23919)
# Open PowerShell as Administrator

# Navigate to web root
cd C:\inetpub\wwwroot

# Clone the repository
git clone https://github.com/Vijay-Ashley/sltk-ai-agent.git sltk-chatbot

# Navigate to the cloned folder
cd sltk-chatbot
```

### **Step 2: Find Your IBM i Hostname**

You need to know your IBM i hostname/IP. On IBM i, run:
```bash
hostname
# Example output: ibmi-prod.ashley.com
```

**Save this hostname!**

### **Step 3: Deploy Frontend**

```powershell
# Navigate to frontend folder
cd C:\inetpub\wwwroot\sltk-chatbot\sltk-chatbot\frontend

# Run deployment script with your IBM i hostname
.\deploy-windows.ps1 -IBMiHostname "your-ibmi-hostname"

# Example:
.\deploy-windows.ps1 -IBMiHostname "ibmi-prod.ashley.com"
# Or if using IP:
.\deploy-windows.ps1 -IBMiHostname "192.168.1.100"
```

**The script will:**
- ✅ Check Node.js installation
- ✅ Create `.env.production` with IBM i hostname
- ✅ Install npm dependencies
- ✅ Build production bundle
- ✅ Create IIS web.config

### **Step 4: Deploy to IIS**

**Option A: Using IIS Manager (GUI)**

1. Open **IIS Manager** (Start → IIS Manager)
2. Right-click **Sites** → **Add Website**
3. Configure:
   - **Site name:** `SLTK-Chatbot`
   - **Physical path:** `C:\inetpub\wwwroot\sltk-chatbot\sltk-chatbot\frontend\dist`
   - **Binding:**
     - Type: `http`
     - Port: `80`
     - Host name: (leave blank or use `ae1dcvpap23919`)
4. Click **OK**
5. Start the website

**Option B: Using PowerShell**

```powershell
# Import IIS module
Import-Module WebAdministration

# Create new website
New-Website -Name "SLTK-Chatbot" `
    -PhysicalPath "C:\inetpub\wwwroot\sltk-chatbot\sltk-chatbot\frontend\dist" `
    -Port 80 `
    -Force

# Start the website
Start-Website -Name "SLTK-Chatbot"
```

### **Step 5: Configure Firewall**

```powershell
# Allow HTTP traffic on port 80
New-NetFirewallRule -DisplayName "SLTK Chatbot HTTP" `
    -Direction Inbound `
    -LocalPort 80 `
    -Protocol TCP `
    -Action Allow
```

### **Step 6: Test**

Open browser: `http://ae1dcvpap23919/`

You should see the SLTK Upload Chatbot UI!

---

## 🖥️ **Part 3: Deploy Backend on IBM i**

### **Step 1: Clone Repository on IBM i**

```bash
# SSH to IBM i
ssh VIJAYVERMA@your-ibmi-hostname

# Navigate to home directory
cd /home/VIJAYVERMA

# Clone the repository
git clone https://github.com/Vijay-Ashley/sltk-ai-agent.git

# Navigate to backend folder
cd sltk-ai-agent/sltk-chatbot/backend
```

### **Step 2: Setup Virtual Environment**

```bash
# Run setup script
chmod +x setup_venv.sh
./setup_venv.sh
```

**The script will:**
- ✅ Create Python virtual environment
- ✅ Install Flask, Flask-CORS, Flask-SocketIO
- ✅ Install openpyxl, python-dotenv
- ✅ Skip pandas/pyodbc (not available via pip on IBM i)

### **Step 3: Start the Backend**

```bash
# Activate virtual environment
source venv/bin/activate

# Start the Flask app
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
============================================================

✅ POC dropbox folder verified: /HOME/VIJAYVERMA
🚀 Starting server...
 * Running on http://0.0.0.0:44001
```

---

## 🧪 **Part 4: Testing**

### **Test 1: Backend from IBM i**

```bash
# On IBM i (in another terminal)
curl http://localhost:44001/
```

**Expected:**
```json
{
  "status": "running",
  "message": "SLTK Monitor API is operational"
}
```

### **Test 2: Backend from Windows Server**

```powershell
# On Windows Server
curl http://your-ibmi-hostname:44001/
```

### **Test 3: Frontend from Browser**

Open browser: `http://ae1dcvpap23919/`

You should see:
- ✅ SLTK Upload Chatbot header
- ✅ "Connected" status (green checkmark)
- ✅ Upload button

### **Test 4: File Upload**

1. Click "Upload Excel File"
2. Select a test Excel file
3. Click "Upload"
4. Check IBM i: `ls -la /HOME/VIJAYVERMA/`

---

## 🔄 **Updating the Code**

### **On Windows Server:**

```powershell
cd C:\inetpub\wwwroot\sltk-chatbot

# Pull latest changes
git pull origin main

# Rebuild frontend
cd sltk-chatbot\frontend
npm run build

# Restart IIS website
Restart-Website -Name "SLTK-Chatbot"
```

### **On IBM i:**

```bash
cd /home/VIJAYVERMA/sltk-ai-agent

# Pull latest changes
git pull origin main

# Restart backend (Ctrl+C to stop, then restart)
cd sltk-chatbot/backend
source venv/bin/activate
python app.py
```

---

## 📝 **Summary**

### **Repository Structure:**
```
sltk-ai-agent/
├── sltk-chatbot/
│   ├── backend/              # IBM i Flask API
│   │   ├── app.py
│   │   ├── setup_venv.sh
│   │   ├── requirements.txt
│   │   └── ...
│   ├── frontend/             # Windows React UI
│   │   ├── src/
│   │   ├── deploy-windows.ps1
│   │   ├── package.json
│   │   └── ...
│   ├── COMPLETE_SETUP_GUIDE.md
│   ├── GITHUB_DEPLOYMENT.md  # This file
│   └── ...
└── .gitignore
```

### **Deployment Steps:**
1. ✅ Push code to GitHub
2. ✅ Clone on Windows Server
3. ✅ Run `deploy-windows.ps1` script
4. ✅ Deploy to IIS
5. ✅ Clone on IBM i
6. ✅ Run `setup_venv.sh` script
7. ✅ Start Flask backend
8. ✅ Test from browser

---

## 🆘 **Troubleshooting**

### **Issue: Git not found on Windows Server**

```powershell
# Install Git for Windows
winget install Git.Git
# Or download from: https://git-scm.com/download/win
```

### **Issue: Git not found on IBM i**

```bash
# Install git via yum
yum install git
```

### **Issue: Node.js not found on Windows Server**

```powershell
# Install Node.js
winget install OpenJS.NodeJS.LTS
# Or download from: https://nodejs.org/
```

---

## ✅ **Quick Reference**

### **GitHub Repository:**
```
https://github.com/Vijay-Ashley/sltk-ai-agent.git
```

### **Windows Server Deployment:**
```powershell
cd C:\inetpub\wwwroot
git clone https://github.com/Vijay-Ashley/sltk-ai-agent.git sltk-chatbot
cd sltk-chatbot\sltk-chatbot\frontend
.\deploy-windows.ps1 -IBMiHostname "your-ibmi-hostname"
```

### **IBM i Deployment:**
```bash
cd /home/VIJAYVERMA
git clone https://github.com/Vijay-Ashley/sltk-ai-agent.git
cd sltk-ai-agent/sltk-chatbot/backend
./setup_venv.sh
source venv/bin/activate
python app.py
```

---

**You're all set! 🎉**

Push your code to GitHub, then clone on both servers!

