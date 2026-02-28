# 📤 Push SLTK Chatbot to GitHub

## 🎯 **Goal**

Push the SLTK Chatbot code to: `https://github.com/Vijay-Ashley/sltk-ai-agent.git`

---

## 📋 **Step-by-Step Instructions**

### **Step 1: Open Terminal/PowerShell**

```powershell
# On your local Windows machine
# Open PowerShell or Git Bash

# Navigate to the project folder
cd "C:\Users\VVerma\OneDrive - Ashley Furniture Industries, Inc\Documents\IBMI"
```

### **Step 2: Check Git Status**

```bash
# Check if git is already initialized
git status
```

**If you see:** `fatal: not a git repository`
- Continue to Step 3

**If you see:** `On branch main` or similar
- Skip to Step 4

### **Step 3: Initialize Git (if needed)**

```bash
# Initialize git repository
git init

# Add remote repository
git remote add origin https://github.com/Vijay-Ashley/sltk-ai-agent.git

# Check remote
git remote -v
```

**Expected output:**
```
origin  https://github.com/Vijay-Ashley/sltk-ai-agent.git (fetch)
origin  https://github.com/Vijay-Ashley/sltk-ai-agent.git (push)
```

### **Step 4: Add Files**

```bash
# Add all files
git add .

# Check what will be committed
git status
```

**You should see:**
```
Changes to be committed:
  new file:   sltk-chatbot/backend/app.py
  new file:   sltk-chatbot/frontend/src/App.tsx
  new file:   sltk-chatbot/GITHUB_DEPLOYMENT.md
  ... (many more files)
```

### **Step 5: Commit Changes**

```bash
# Commit with a message
git commit -m "Add SLTK Chatbot - Backend (IBM i) and Frontend (Windows)"
```

### **Step 6: Push to GitHub**

```bash
# Push to GitHub
git push -u origin main
```

**If you get an error about branch name:**
```bash
# Try with 'master' instead
git push -u origin master

# Or rename branch to main
git branch -M main
git push -u origin main
```

**If prompted for credentials:**
- Enter your GitHub username
- Enter your GitHub Personal Access Token (not password)

---

## 🔑 **GitHub Authentication**

### **Option 1: Personal Access Token (Recommended)**

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (all)
4. Click "Generate token"
5. Copy the token (you won't see it again!)
6. Use this token as your password when pushing

### **Option 2: GitHub CLI**

```bash
# Install GitHub CLI
winget install GitHub.cli

# Authenticate
gh auth login

# Follow the prompts
```

---

## ✅ **Verify Upload**

1. Go to: https://github.com/Vijay-Ashley/sltk-ai-agent
2. You should see:
   - `sltk-chatbot/` folder
   - `README.md`
   - `GITHUB_DEPLOYMENT.md`
   - All other files

---

## 🔄 **Update Code Later**

When you make changes:

```bash
# Add changes
git add .

# Commit
git commit -m "Update: description of changes"

# Push
git push origin main
```

---

## 🆘 **Troubleshooting**

### **Issue: "fatal: remote origin already exists"**

```bash
# Remove existing remote
git remote remove origin

# Add it again
git remote add origin https://github.com/Vijay-Ashley/sltk-ai-agent.git
```

### **Issue: "failed to push some refs"**

```bash
# Pull first (if repo has existing content)
git pull origin main --allow-unrelated-histories

# Then push
git push origin main
```

### **Issue: "Authentication failed"**

- Make sure you're using a Personal Access Token, not your password
- Generate a new token at: https://github.com/settings/tokens

---

## 📝 **Summary**

```bash
# Quick commands (if git is already set up)
cd "C:\Users\VVerma\OneDrive - Ashley Furniture Industries, Inc\Documents\IBMI"
git add .
git commit -m "Add SLTK Chatbot"
git push origin main
```

---

## 🎯 **Next Steps After Pushing**

1. ✅ Verify code is on GitHub
2. ✅ Clone on Windows Server (see GITHUB_DEPLOYMENT.md)
3. ✅ Clone on IBM i (see GITHUB_DEPLOYMENT.md)
4. ✅ Deploy and test!

---

**Ready to push? Run the commands above!** 🚀

