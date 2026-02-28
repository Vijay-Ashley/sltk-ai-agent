# 🚀 SLTK Chatbot - Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Setup Backend on IBM i (2 minutes)

```bash
# 1. SSH into IBM i
ssh your-user@your-ibmi-ip

# 2. Install Python packages
pip install Flask Flask-CORS Flask-SocketIO pandas openpyxl pyodbc

# 3. Edit app.py configuration
# - Line 35: Set DROPBOX_FOLDER = '/HOME/VIJAYVERMA'
# - Lines 51-57: Set database connection string

# 4. Start the server
cd /path/to/sltk-chatbot/backend
python app.py

# ✅ You should see:
# ✅ Dropbox folder verified
# ✅ Database connection successful
# 🚀 Starting server...
```

### Step 2: Setup Frontend on Your PC (3 minutes)

```bash
# 1. Install dependencies
cd sltk-chatbot/frontend
npm install

# 2. Edit API URL in src/App.tsx line 6
# Change: const API_URL = 'http://your-ibmi-ip:44001';

# 3. Start the dev server
npm run dev

# ✅ UI opens at http://localhost:3000
```

### Step 3: Test It! (1 minute)

1. Open http://localhost:3000
2. Drag & drop an Excel file
3. Click "Upload to IBM i"
4. Watch real-time progress! 🎉

---

## 🎯 What You Get

✅ **Web-based upload** - No more manual FTP  
✅ **Real-time monitoring** - See progress live  
✅ **Error guidance** - Know exactly what to fix  
✅ **Beautiful UI** - Similar to your RAG chatbot  

---

## 🔧 Configuration Checklist

### Backend (app.py)

- [ ] Line 35: `DROPBOX_FOLDER` set to your IFS path
- [ ] Line 36: `SLTK_LIBRARY` set to 'ACTLIBDB' (or your library)
- [ ] Line 53: `SYSTEM` set to your IBM i hostname
- [ ] Line 55: `UID` set to your IBM i username
- [ ] Line 56: `PWD` set to your IBM i password

### Frontend (src/App.tsx)

- [ ] Line 6: `API_URL` set to `http://your-ibmi-ip:44001`

---

## 📊 How It Works

```
1. User uploads Excel file via web UI
   ↓
2. Flask API saves to IFS folder
   ↓
3. SLTKDRP auto-detects and processes file
   ↓
4. Flask API polls SLTKGRP table every 2 seconds
   ↓
5. WebSocket pushes updates to UI in real-time
   ↓
6. User sees live progress and errors
```

---

## 🆘 Common Issues

### "Database connection failed"
**Fix:** Update connection string in `app.py` lines 51-57

### "Cannot access IFS folder"
**Fix:** Run on IBM i:
```bash
mkdir /HOME/VIJAYVERMA
chmod 777 /HOME/VIJAYVERMA
```

### "WebSocket connection failed"
**Fix:** 
1. Verify Flask API is running
2. Check firewall allows port 44001
3. Update API_URL in App.tsx

---

## 📝 Next Steps

1. ✅ Test with a sample Excel file
2. ✅ Monitor a real SLTK upload
3. ✅ View error details and resolutions
4. ✅ Check upload history
5. 🚀 Deploy to production!

---

**Need Help?** Check the full README.md for detailed documentation.

**Happy Uploading! 🎉**

