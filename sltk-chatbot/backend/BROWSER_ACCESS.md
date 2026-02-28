# 🌐 Accessing SLTK Chatbot from Browser

## ✅ **Current Status:**

- ✅ API works via `curl` on IBM i
- ❌ Browser can't access from Windows

---

## 🔧 **Solution: Changed Port to 8080**

I've changed the port from `44001` to `8080` (more likely to be open).

---

## 🚀 **Steps to Access from Browser:**

### **1. Restart the Server**

On IBM i:
```bash
# Stop current server (Ctrl+C)
cd /home/VIJAYVERMA/SLTK
source venv/bin/activate
python app.py
```

**Expected output:**
```
Port: 8080
Running on http://0.0.0.0:8080
```

### **2. Find Your IBM i Hostname**

On IBM i:
```bash
hostname
# Example output: IBMI-PROD.ashley.com
```

### **3. Access from Windows Browser**

Try these URLs:
```
http://your-ibmi-hostname:8080/
http://ibmi-ip-address:8080/
http://localhost:8080/  (if using SSH tunnel)
```

---

## 🛡️ **If Port 8080 Still Blocked:**

### **Option A: Contact IBM i Admin**

Ask them to open port 8080 (or 44001) in the firewall:
```
Firewall rule: Allow TCP port 8080 inbound
```

### **Option B: Use SSH Tunnel (Temporary)**

On Windows PowerShell:
```powershell
ssh -L 8080:localhost:8080 VIJAYVERMA@your-ibmi-hostname
```

Then access: `http://localhost:8080/`

### **Option C: Try Different Ports**

Edit `app.py` and try these ports:
```python
PORT = 8080   # HTTP alternate
PORT = 8000   # Common dev port
PORT = 5000   # Flask default
PORT = 3000   # Node.js default
PORT = 80     # Standard HTTP (requires admin)
```

---

## 🧪 **Testing:**

### **Test 1: From IBM i (should work)**
```bash
curl http://localhost:8080/
```

### **Test 2: From Windows Command Prompt**
```cmd
curl http://ibmi-hostname:8080/
```

### **Test 3: From Windows Browser**
```
http://ibmi-hostname:8080/
```

---

## 🔍 **Troubleshooting:**

### **Check if Port is Open**

On IBM i:
```bash
netstat -an | grep 8080
```

Should show:
```
tcp  0  0  0.0.0.0:8080  0.0.0.0:*  LISTEN
```

### **Check Firewall Status**

```bash
# Check if firewall is active
system "DSPSYSVAL SYSVAL(QALWOBJRST)"

# Or contact your admin
```

### **Test Network Connectivity**

On Windows:
```cmd
ping ibmi-hostname
telnet ibmi-hostname 8080
```

---

## 📋 **Common Ports and Their Status:**

| Port | Purpose | Likely Open? |
|------|---------|--------------|
| 80 | HTTP | ✅ Usually open (needs admin) |
| 443 | HTTPS | ✅ Usually open (needs admin) |
| 8080 | HTTP Alt | ⚠️ Maybe |
| 8000 | Dev | ⚠️ Maybe |
| 5000 | Flask | ⚠️ Maybe |
| 44001 | Custom | ❌ Likely blocked |

---

## ✅ **Recommended Solution:**

1. **Try port 8080 first** (already changed in app.py)
2. **If blocked, contact IBM i admin** to open the port
3. **Or use SSH tunnel** for testing

---

## 🎯 **Next Steps:**

1. Restart server with new port (8080)
2. Test from browser
3. If still blocked, contact admin or use SSH tunnel

**Restart the server now and try accessing from browser!** 🚀

