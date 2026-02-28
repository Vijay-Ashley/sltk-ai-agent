# 🪟 Deploy SLTK Chatbot Frontend on Windows Server

## 🎯 **Architecture Overview**

```
┌─────────────────────────────────────┐
│  Windows Server (ae1dcvpap23919)    │
│  ├── React Frontend (Port 80/3000)  │
│  │   └── Calls IBM i API via HTTP   │
│  └── IIS or Node.js Server          │
└─────────────────────────────────────┘
              ↓ HTTP
┌─────────────────────────────────────┐
│  IBM i Server                       │
│  └── Flask Backend (Port 44001)     │
│      ├── File Upload API            │
│      ├── Status Monitoring          │
│      └── WebSocket Updates          │
└─────────────────────────────────────┘
```

---

## 📋 **Prerequisites**

### On Windows Server (ae1dcvpap23919):
- ✅ Node.js 18+ installed
- ✅ IIS installed (optional, for production)
- ✅ Network access to IBM i on port 44001

### On IBM i:
- ✅ Flask backend running on port 44001
- ✅ Port 44001 accessible from Windows server

---

## 🚀 **Deployment Options**

### **Option 1: Node.js Development Server** (Quick Test)
### **Option 2: IIS Production Server** (Recommended)
### **Option 3: Node.js Production Server** (PM2)

---

## 📦 **Option 1: Node.js Development Server**

### **Step 1: Transfer Files to Windows Server**

```powershell
# On your local machine, copy the frontend folder to Windows server
# Replace with your actual IBM i hostname/IP
$ibmiHost = "your-ibmi-hostname"

# Copy via network share or use SCP
scp -r sltk-chatbot/frontend user@ae1dcvpap23919:C:\inetpub\wwwroot\sltk-chatbot
```

### **Step 2: Configure API URL**

Edit `frontend/src/App.tsx` line 6:

```typescript
// Change from:
const API_URL = 'http://localhost:44001';

// To your IBM i hostname:
const API_URL = 'http://your-ibmi-hostname:44001';
```

### **Step 3: Install Dependencies**

```powershell
# On Windows Server
cd C:\inetpub\wwwroot\sltk-chatbot\frontend
npm install
```

### **Step 4: Start Development Server**

```powershell
npm run dev
```

**Access at:** `http://ae1dcvpap23919:3000/`

---

## 🏭 **Option 2: IIS Production Server** ⭐ **Recommended**

### **Step 1: Build the React App**

```powershell
# On Windows Server
cd C:\inetpub\wwwroot\sltk-chatbot\frontend
npm run build
```

This creates a `dist` folder with static files.

### **Step 2: Configure IIS**

1. **Open IIS Manager**
2. **Create New Website:**
   - Site name: `SLTK-Chatbot`
   - Physical path: `C:\inetpub\wwwroot\sltk-chatbot\frontend\dist`
   - Binding: `http://ae1dcvpap23919:80`
3. **Add URL Rewrite Rule** (for React Router):
   - Install URL Rewrite module if not installed
   - Add `web.config` (see below)

### **Step 3: Create web.config**

Create `frontend/dist/web.config`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.webServer>
    <rewrite>
      <rules>
        <rule name="React Routes" stopProcessing="true">
          <match url=".*" />
          <conditions logicalGrouping="MatchAll">
            <add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" />
            <add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" />
          </conditions>
          <action type="Rewrite" url="/" />
        </rule>
      </rules>
    </rewrite>
  </system.webServer>
</configuration>
```

**Access at:** `http://ae1dcvpap23919/`

---

## 🔧 **Option 3: Node.js Production Server (PM2)**

### **Step 1: Install PM2**

```powershell
npm install -g pm2
```

### **Step 2: Build the App**

```powershell
cd C:\inetpub\wwwroot\sltk-chatbot\frontend
npm run build
```

### **Step 3: Serve with PM2**

```powershell
# Install serve
npm install -g serve

# Start with PM2
pm2 serve dist 80 --name sltk-chatbot --spa

# Save PM2 config
pm2 save

# Setup PM2 to start on boot
pm2 startup
```

**Access at:** `http://ae1dcvpap23919/`

---

## ⚙️ **Configuration**

### **Update API URL for Production**

**Option A: Environment Variable (Recommended)**

Create `frontend/.env.production`:

```env
VITE_API_URL=http://your-ibmi-hostname:44001
```

Update `frontend/src/App.tsx`:

```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:44001';
```

**Option B: Direct Configuration**

Edit `frontend/src/App.tsx` line 6:

```typescript
const API_URL = 'http://your-ibmi-hostname:44001';
```

---

## 🧪 **Testing**

### **Test 1: Check IBM i Backend**

```powershell
# From Windows Server
curl http://your-ibmi-hostname:44001/
```

**Expected:**
```json
{
  "status": "running",
  "message": "SLTK Monitor API is operational"
}
```

### **Test 2: Access Frontend**

Open browser: `http://ae1dcvpap23919/`

You should see the SLTK Upload Chatbot UI.

### **Test 3: Upload a File**

1. Click "Upload Excel File"
2. Select a test Excel file
3. Click "Upload"
4. Check if file appears in `/HOME/VIJAYVERMA` on IBM i

---

## 🔥 **Firewall Configuration**

### **On Windows Server:**

```powershell
# Allow inbound on port 80 (if using IIS)
New-NetFirewallRule -DisplayName "SLTK Chatbot HTTP" -Direction Inbound -LocalPort 80 -Protocol TCP -Action Allow

# Allow inbound on port 3000 (if using dev server)
New-NetFirewallRule -DisplayName "SLTK Chatbot Dev" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow
```

### **On IBM i:**

Port 44001 should already be accessible (as per your POC).

---

## 📝 **Quick Deployment Script**

Save as `deploy.ps1`:

```powershell
# SLTK Chatbot - Windows Deployment Script

$ibmiHost = "your-ibmi-hostname"  # CHANGE THIS
$deployPath = "C:\inetpub\wwwroot\sltk-chatbot"

Write-Host "🚀 Deploying SLTK Chatbot Frontend..." -ForegroundColor Green

# Step 1: Update API URL
Write-Host "📝 Updating API URL..." -ForegroundColor Yellow
$appTsx = Get-Content "$deployPath\frontend\src\App.tsx"
$appTsx = $appTsx -replace "const API_URL = 'http://localhost:44001';", "const API_URL = 'http://$ibmiHost:44001';"
$appTsx | Set-Content "$deployPath\frontend\src\App.tsx"

# Step 2: Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
cd "$deployPath\frontend"
npm install

# Step 3: Build
Write-Host "🔨 Building production bundle..." -ForegroundColor Yellow
npm run build

# Step 4: Copy to IIS
Write-Host "📂 Deploying to IIS..." -ForegroundColor Yellow
Copy-Item -Path "$deployPath\frontend\dist\*" -Destination "C:\inetpub\wwwroot\sltk" -Recurse -Force

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "🌐 Access at: http://ae1dcvpap23919/" -ForegroundColor Cyan
```

Run with:
```powershell
.\deploy.ps1
```

---

## 🆘 **Troubleshooting**

### **Issue: Can't connect to IBM i API**

**Check:**
```powershell
# Test connectivity
Test-NetConnection -ComputerName your-ibmi-hostname -Port 44001

# Test API
curl http://your-ibmi-hostname:44001/
```

**Fix:** Ensure IBM i port 44001 is open and Flask backend is running.

### **Issue: CORS errors in browser**

**Fix:** Backend already has CORS enabled:
```python
CORS(app, resources={r"/*": {"origins": "*"}})
```

### **Issue: WebSocket connection fails**

**Check:** Browser console for errors.

**Fix:** Ensure WebSocket URL matches API URL in `App.tsx`.

---

## ✅ **Summary**

| Step | Action | Status |
|------|--------|--------|
| 1 | Transfer files to Windows | ⏳ |
| 2 | Update API URL | ⏳ |
| 3 | Install dependencies | ⏳ |
| 4 | Build production bundle | ⏳ |
| 5 | Deploy to IIS/Node | ⏳ |
| 6 | Test from browser | ⏳ |

---

**Next:** Choose your deployment option and follow the steps above! 🚀

