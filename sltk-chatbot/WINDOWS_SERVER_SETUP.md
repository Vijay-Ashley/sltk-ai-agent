# 🪟 SLTK Chatbot - Windows Server Setup (Port 8001)

## 🎯 **Architecture**

```
Windows Server (ae1dcvpap23919)
├── React Frontend (Port 8001) - Vite Dev Server
│   └── Calls IBM i API
│
IBM i Server
└── Flask Backend (Port 44001)
```

---

## 📋 **Setup Steps**

### **Step 1: Clone Repository** ✅

```cmd
cd C:\
mkdir sltk-ai-agent
cd sltk-ai-agent
git clone https://github.com/Vijay-Ashley/sltk-ai-agent.git .
```

### **Step 2: Navigate to Frontend**

```cmd
cd sltk-chatbot\frontend
```

### **Step 3: Create .env File**

Create a file named `.env` with your IBM i hostname:

```cmd
echo VITE_API_URL=http://your-ibmi-hostname:44001 > .env
```

**Examples:**
```cmd
REM If using hostname:
echo VITE_API_URL=http://ibmi-prod.ashley.com:44001 > .env

REM If using IP address:
echo VITE_API_URL=http://192.168.1.100:44001 > .env
```

### **Step 4: Install Node.js (if not installed)**

```cmd
REM Check if Node.js is installed
node --version

REM If not installed, download from:
REM https://nodejs.org/
```

### **Step 5: Install Dependencies**

```cmd
npm install
```

This will install all required packages (React, Vite, etc.)

### **Step 6: Start the Frontend Server**

**Option A: Using the start script**
```cmd
start-windows.bat
```

**Option B: Using npm directly**
```cmd
npm run dev
```

**Expected Output:**
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:8001/
  ➜  Network: http://192.168.1.50:8001/
  ➜  press h + enter to show help
```

### **Step 7: Configure Firewall**

Open PowerShell as Administrator:

```powershell
New-NetFirewallRule -DisplayName "SLTK Chatbot Frontend" `
    -Direction Inbound `
    -LocalPort 8001 `
    -Protocol TCP `
    -Action Allow
```

### **Step 8: Access the UI**

**From Windows Server:**
```
http://localhost:8001
```

**From other computers:**
```
http://ae1dcvpap23919:8001
```

---

## 🧪 **Testing**

### **Test 1: Check Frontend**

Open browser: `http://localhost:8001`

You should see the SLTK Upload Chatbot UI.

### **Test 2: Check Backend Connection**

The UI should show:
- ✅ "Connected" status (green checkmark) if IBM i backend is running
- ❌ "Disconnected" if IBM i backend is not accessible

### **Test 3: Upload a File**

1. Click "Upload Excel File"
2. Select a test Excel file
3. Click "Upload"
4. File should be uploaded to IBM i

---

## 🔄 **Starting/Stopping the Server**

### **Start:**
```cmd
cd C:\sltk-ai-agent\sltk-chatbot\frontend
start-windows.bat
```

### **Stop:**
Press `Ctrl+C` in the terminal

---

## 🔧 **Configuration**

### **Change IBM i Hostname:**

Edit `.env` file:
```
VITE_API_URL=http://your-new-hostname:44001
```

Then restart the server.

### **Change Port:**

Edit `vite.config.ts`:
```typescript
server: {
  port: 8001,  // Change this
}
```

---

## 🆘 **Troubleshooting**

### **Issue: "npm: command not found"**

**Fix:** Install Node.js from https://nodejs.org/

### **Issue: Port 8001 already in use**

**Fix:** 
```cmd
REM Find what's using port 8001
netstat -ano | findstr :8001

REM Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### **Issue: Frontend shows "Disconnected"**

**Fix:**
1. Check if IBM i backend is running on port 44001
2. Check `.env` file has correct IBM i hostname
3. Test connectivity: `curl http://your-ibmi-hostname:44001/`

### **Issue: Can't access from other computers**

**Fix:**
1. Check firewall rule is created
2. Check Windows Server firewall settings
3. Make sure Vite is listening on `0.0.0.0` (already configured)

---

## 📝 **Summary**

| Step | Command | Status |
|------|---------|--------|
| 1. Clone repo | `git clone ...` | ✅ |
| 2. Navigate | `cd sltk-chatbot\frontend` | ✅ |
| 3. Create .env | `echo VITE_API_URL=... > .env` | ⏳ |
| 4. Install deps | `npm install` | ⏳ |
| 5. Start server | `start-windows.bat` | ⏳ |
| 6. Configure firewall | PowerShell command | ⏳ |
| 7. Access UI | `http://ae1dcvpap23919:8001` | ⏳ |

---

## 🎯 **Quick Start Commands**

```cmd
cd C:\sltk-ai-agent\sltk-chatbot\frontend
echo VITE_API_URL=http://your-ibmi-hostname:44001 > .env
npm install
start-windows.bat
```

---

**Access at:** `http://ae1dcvpap23919:8001` 🚀

