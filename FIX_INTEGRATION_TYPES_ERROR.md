# Fix: "Failed to load integration types" Error

## 🔍 Problem

The frontend shows "Failed to load integration types" error. This usually means:
1. Database tables don't exist
2. Backend cannot connect to database
3. CORS issue between frontend and backend
4. Backend is not running

---

## ✅ Solution - Step by Step

### Step 1: Check if Backend is Running

```bash
# Check if backend is responding
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy"}
```

If this fails, the backend is not running. Start it:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0
```

---

### Step 2: Run Database Diagnostic Script

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python diagnose_db.py
```

This will:
- ✅ Check database connection
- ✅ Create missing tables
- ✅ Verify encryption
- ✅ Test API endpoints

---

### Step 3: Verify Database & Tables Exist

#### Option A: Using the diagnostic script (recommended)
```bash
cd backend
python diagnose_db.py
```

#### Option B: Manual verification
```bash
# Check if database exists
mysql -u root -p -e "SHOW DATABASES;"

# If 'workflow_db' is not in the list, create it:
mysql -u root -p -e "CREATE DATABASE workflow_db;"

# Check if tables exist
mysql -u root -p workflow_db -e "SHOW TABLES;"

# Expected tables:
# - integration_types
# - integrations
# - workflows
# - execution_logs
```

---

### Step 4: Initialize Database Tables

If tables don't exist, they will be auto-created when you start the backend:

```bash
cd backend
source venv/bin/activate
python -c "from app.database import init_db; init_db(); print('✅ Tables created!')"
```

Or simply start the backend (it auto-creates tables on startup):
```bash
uvicorn app.main:app --reload
```

---

### Step 5: Check API Directly

Test if the backend API is working:

```bash
# Test integration types endpoint
curl http://localhost:8000/api/integration-types

# Expected response (might be empty array):
# []

# Or if you have data:
# [{"id":1,"name":"jira","description":"...","parameters":[...],"created_at":"..."}]
```

If you get an error or no response, check backend logs.

---

### Step 6: Initialize Sample Integration Types

```bash
cd backend
source venv/bin/activate
python setup_integration_types.py
```

This creates sample integration types for Jira, GitHub, AWS, and Azure.

---

### Step 7: Check Frontend Console

Open browser DevTools (F12) and check Console tab for errors:

```javascript
// Common errors:

// ❌ CORS error
// Fix: Make sure backend is running on port 8000

// ❌ Network error
// Fix: Backend might not be running

// ❌ 500 Internal Server Error
// Fix: Check backend logs for database errors
```

---

## 🐛 Common Issues & Fixes

### Issue 1: "Access denied for user 'root'"

**Problem**: Wrong database password

**Fix**:
```bash
# Update backend/.env with correct password
DB_PASSWORD=your_actual_password

# Or reset MariaDB root password:
sudo mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'securepassword';
FLUSH PRIVILEGES;
EXIT;
```

---

### Issue 2: "Can't connect to MySQL server"

**Problem**: MariaDB is not running

**Fix**:
```bash
# Start MariaDB
sudo systemctl start mariadb

# Enable on boot
sudo systemctl enable mariadb

# Check status
sudo systemctl status mariadb
```

---

### Issue 3: Tables don't exist

**Problem**: Database not initialized

**Fix**:
```bash
cd backend
python diagnose_db.py
```

Or manually:
```bash
cd backend
python -c "from app.database import init_db; init_db()"
```

---

### Issue 4: Backend running but frontend still shows error

**Problem**: CORS or proxy issue

**Fix 1** - Check Vite proxy (frontend/vite.config.ts):
```typescript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

**Fix 2** - Restart frontend:
```bash
cd frontend
npm run dev
```

**Fix 3** - Check if backend allows CORS:
```bash
# Backend should have CORS middleware (already configured)
# Check app/main.py has:
# allow_origins=["*"]
```

---

### Issue 5: "ENCRYPTION_KEY" error

**Problem**: Invalid encryption key

**Fix**: We already fixed this, but if it persists:
```bash
cd backend
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Copy the output to .env:
# ENCRYPTION_KEY=<your-new-key>
```

---

## 🔄 Complete Reset (Nuclear Option)

If nothing works, do a complete reset:

```bash
# 1. Stop everything
pkill -f uvicorn
pkill -f npm

# 2. Drop and recreate database
mysql -u root -p -e "DROP DATABASE IF EXISTS workflow_db;"
mysql -u root -p -e "CREATE DATABASE workflow_db;"

# 3. Restart backend (will create tables)
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# 4. Wait for "Database initialized successfully" message

# 5. Initialize data (new terminal)
cd backend
source venv/bin/activate
python setup_integration_types.py

# 6. Restart frontend
cd frontend
npm run dev

# 7. Open browser: http://localhost:3000
```

---

## 📋 Checklist

Use this checklist to debug:

- [ ] MariaDB is running: `systemctl status mariadb`
- [ ] Database exists: `mysql -u root -p -e "SHOW DATABASES;" | grep workflow_db`
- [ ] Backend can connect: `curl http://localhost:8000/health`
- [ ] Backend is running on port 8000: `lsof -i :8000`
- [ ] Tables exist: Run `diagnose_db.py`
- [ ] API returns data: `curl http://localhost:8000/api/integration-types`
- [ ] Frontend is running on port 3000: `lsof -i :3000`
- [ ] Browser console shows no errors (F12 → Console)
- [ ] No CORS errors in browser console

---

## 🎯 Quick Fix Command

Run this one command to fix most issues:

```bash
cd backend && \
source venv/bin/activate && \
python diagnose_db.py && \
python setup_integration_types.py && \
echo "✅ Done! Now start backend: uvicorn app.main:app --reload"
```

---

## 📞 Still Not Working?

1. **Check backend logs** - Look at terminal where backend is running
2. **Check browser console** - Press F12 and look for errors
3. **Check database logs**: `sudo journalctl -u mariadb -f`
4. **Verify ports**: Make sure 3000 and 8000 are not used by other apps

---

## ✨ Expected Result

After fixing, you should see:
- ✅ Backend health check: `{"status":"healthy"}`
- ✅ API returns data: `[{integration type objects}]`
- ✅ Frontend loads without errors
- ✅ Integration Types page shows 4 cards (Jira, GitHub, AWS, Azure)

---

**Most Common Fix**: Run `python diagnose_db.py` - it fixes 90% of issues! 🎉
