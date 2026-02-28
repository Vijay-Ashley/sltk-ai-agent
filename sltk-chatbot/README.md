# 🤖 SLTK Upload Chatbot

Complete solution for monitoring SLTK uploads on IBM i with real-time web interface.

## 📋 Overview

This application provides:
- ✅ **Web-based file upload** to IBM i IFS folder
- ✅ **Real-time monitoring** of SLTK processing via WebSocket
- ✅ **Error detection** with resolution guidance
- ✅ **Progress tracking** with live percentage updates
- ✅ **Beautiful UI** similar to your RAG chatbot

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│  React Frontend (Port 3000)                              │
│  - Upload Excel files                                    │
│  - Monitor progress in real-time                         │
│  - View errors and resolutions                           │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ HTTP + WebSocket
                 ↓
┌─────────────────────────────────────────────────────────┐
│  Flask API on IBM i (Port 44001)                        │
│  - Receive file uploads                                  │
│  - Query DB2 tables (SLTKGRP, SLTKTRN, SLTKERR)         │
│  - Push real-time updates via WebSocket                 │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ Saves to IFS + Queries DB2
                 ↓
┌─────────────────────────────────────────────────────────┐
│  IBM i System                                            │
│  - IFS Folder: /HOME/VIJAYVERMA/                        │
│  - SLTKDRP: Auto-processes files                        │
│  - DB2 Tables: SLTKGRP, SLTKTRN, SLTKERR                │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### **Deployment via GitHub** ⭐ **Recommended**

See **[GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md)** for complete step-by-step instructions.

**Quick Summary:**

1. **Clone on Windows Server:**
   ```powershell
   cd C:\inetpub\wwwroot
   git clone https://github.com/Vijay-Ashley/sltk-ai-agent.git sltk-chatbot
   cd sltk-chatbot\sltk-chatbot\frontend
   .\deploy-windows.ps1 -IBMiHostname "your-ibmi-hostname"
   ```

2. **Clone on IBM i:**
   ```bash
   cd /home/VIJAYVERMA
   git clone https://github.com/Vijay-Ashley/sltk-ai-agent.git
   cd sltk-ai-agent/sltk-chatbot/backend
   ./setup_venv.sh
   source venv/bin/activate
   python app.py
   ```

3. **Access:** `http://ae1dcvpap23919/`

---

## 📚 Documentation

- **[GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md)** - Deploy via GitHub clone (recommended)
- **[COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md)** - Complete setup guide
- **[WINDOWS_DEPLOYMENT.md](WINDOWS_DEPLOYMENT.md)** - Windows server deployment options
- **[RUN_WITHOUT_PANDAS.md](backend/RUN_WITHOUT_PANDAS.md)** - Running without pandas/pyodbc
- **[INSTALL_IBMI.md](backend/INSTALL_IBMI.md)** - IBM i installation guide

---

## 🚀 Manual Installation

### Part 1: Backend (Flask API on IBM i)

#### 1. Install Python packages on IBM i

```bash
# SSH into your IBM i system
ssh your-user@your-ibmi-ip

# Install required packages
pip install Flask Flask-CORS Flask-SocketIO pandas openpyxl pyodbc

# Or use requirements.txt
cd /path/to/sltk-chatbot/backend
pip install -r requirements.txt
```

#### 2. Configure the API

Edit `backend/app.py`:

**Line 35 - Set your IFS folder:**
```python
DROPBOX_FOLDER = '/HOME/VIJAYVERMA'  # Change to your path
```

**Lines 51-57 - Set your database connection:**
```python
connection_string = (
    "DRIVER={IBM i Access ODBC Driver};"
    "SYSTEM=localhost;"      # Your IBM i system name
    "DATABASE=ACTLIBDB;"
    "UID=your_user;"         # Your IBM i user
    "PWD=your_password;"     # Your IBM i password
)
```

#### 3. Start the Flask API

```bash
# On IBM i
cd /path/to/sltk-chatbot/backend
python app.py

# Server will start on port 44001
# You should see:
# ✅ Dropbox folder verified
# ✅ Database connection successful
# 🚀 Starting server...
```

### Part 2: Frontend (React UI on your PC)

#### 1. Install Node.js dependencies

```bash
# On your Windows PC
cd sltk-chatbot/frontend
npm install
```

#### 2. Configure API URL

Edit `frontend/src/App.tsx` line 6:

```typescript
const API_URL = 'http://your-ibmi-ip:44001';  // Change to your IBM i IP
```

#### 3. Start the development server

```bash
npm run dev

# UI will open at http://localhost:3000
```

## 📖 Usage

### 1. Upload a File

1. Open http://localhost:3000 in your browser
2. Drag & drop an Excel file or click "Browse Files"
3. Click "Upload to IBM i"
4. File is saved to IFS folder
5. SLTKDRP will automatically process it

### 2. Monitor Progress

1. After upload, you'll see "File uploaded. Enter Group ID to monitor"
2. Find the Group ID in SLTKGRP table or from SLTKDRP logs
3. The UI will automatically connect via WebSocket
4. Watch real-time progress updates:
   - Status (Preparing → Processing → Success/Error)
   - Percentage complete
   - Transaction counts

### 3. View Errors

1. If errors occur, click "View X Errors" button
2. See detailed error information:
   - Error message
   - Issue description
   - Fix suggestions
   - SQL queries to investigate

## 🔧 Troubleshooting

### Backend Issues

#### Database Connection Failed
```
ERROR: Database connection failed
```

**Fix:**
1. Verify ODBC driver is installed on IBM i
2. Check connection string credentials
3. Test with: `SELECT * FROM SLTKGRP FETCH FIRST 1 ROW ONLY`

#### Permission Denied on IFS Folder
```
ERROR: Permission denied: Cannot access /HOME/VIJAYVERMA
```

**Fix:**
```bash
# On IBM i
mkdir /HOME/VIJAYVERMA
chmod 777 /HOME/VIJAYVERMA
```

#### Port Already in Use
```
ERROR: Address already in use
```

**Fix:**
```bash
# Find process using port 44001
netstat -an | grep 44001

# Kill the process or change PORT in app.py
```

### Frontend Issues

#### Cannot Connect to API
```
WebSocket connection failed
```

**Fix:**
1. Verify Flask API is running on IBM i
2. Check firewall allows port 44001
3. Update API_URL in App.tsx with correct IBM i IP

#### CORS Errors
```
Access to fetch blocked by CORS policy
```

**Fix:** Already handled by Flask-CORS in backend

## 📊 API Endpoints

### REST API

```http
GET  /                          # Health check
POST /upload/excel              # Upload Excel file
GET  /api/status/<groupId>      # Get current status
GET  /api/errors/<groupId>      # Get errors
GET  /api/history               # Get upload history
```

### WebSocket Events

```javascript
// Client → Server
socket.emit('monitor', groupId)
socket.emit('stop-monitor', groupId)

// Server → Client
socket.on('status-update', (status) => { })
socket.on('processing-complete', (status) => { })
socket.on('error', (error) => { })
```

## 🎨 UI Features

- **Drag & Drop Upload** - Easy file selection
- **Real-Time Progress** - Live percentage updates
- **Status Indicators** - Color-coded status badges
- **Error Modal** - Detailed error information with fixes
- **Responsive Design** - Works on desktop and mobile
- **Similar to RAG Chatbot** - Familiar UI/UX

## 📁 Project Structure

```
sltk-chatbot/
├── backend/                    # Flask API (runs on IBM i)
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Backend documentation
│
├── frontend/                   # React UI (runs on your PC)
│   ├── src/
│   │   ├── App.tsx           # Main React component
│   │   ├── main.tsx          # Entry point
│   │   └── index.css         # Tailwind CSS
│   ├── package.json          # Node dependencies
│   ├── vite.config.ts        # Vite configuration
│   └── tailwind.config.js    # Tailwind configuration
│
└── README.md                   # This file
```

## 🔐 Security Notes

- Change default credentials in `app.py`
- Use HTTPS in production
- Implement authentication for production use
- Restrict CORS origins in production

## 📝 License

ISC - Ashley Furniture Industries, Inc.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Flask API logs
3. Check browser console for frontend errors
4. Contact your system administrator

---

**Happy Uploading! 🚀**

