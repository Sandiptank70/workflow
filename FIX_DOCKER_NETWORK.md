# Docker Network Fix - Frontend Can't Connect to Backend

## 🔍 Problem

Frontend shows error:
```
Error: connect ECONNREFUSED ::1:8000
```

This means the frontend container is trying to connect to `localhost:8000`, but in Docker, containers have separate network spaces. The frontend needs to use the backend's **service name** (`backend`) instead of `localhost`.

---

## ✅ **SOLUTION - Fixed Files**

I've updated two files to fix this:

### 1. **frontend/vite.config.ts**
Changed from:
```typescript
target: 'http://localhost:8000'
```

To:
```typescript
target: process.env.VITE_API_URL || 'http://backend:8000'
```

### 2. **docker-compose.yml**
Changed from:
```yaml
environment:
  - VITE_API_URL=http://localhost:8000
```

To:
```yaml
environment:
  - VITE_API_URL=http://backend:8000
```

---

## 🚀 **Apply the Fix:**

### **Step 1: Restart the containers with new configuration**

```powershell
# Stop containers
docker-compose down

# Rebuild and start (to pick up new config)
docker-compose up --build -d
```

### **Step 2: Wait for services to start**
```powershell
# Wait 30 seconds
Start-Sleep -Seconds 30
```

### **Step 3: Verify backend is accessible**
```powershell
# Test from host machine
curl http://localhost:8000/health

# Test from frontend container to backend container
docker-compose exec frontend curl http://backend:8000/health
```

Both should return: `{"status":"healthy"}`

### **Step 4: Check frontend logs**
```powershell
docker-compose logs frontend
```

You should NO LONGER see `ECONNREFUSED` errors!

### **Step 5: Open browser**
```powershell
start http://localhost:3000
```

The Integration Types page should now load correctly! ✨

---

## 🔍 **Verify the Fix:**

### Test 1: Backend accessible from frontend container
```powershell
docker-compose exec frontend curl http://backend:8000/health
```
✅ Should return: `{"status":"healthy"}`

### Test 2: API proxy working
```powershell
docker-compose exec frontend curl http://localhost:3000/api/integration-types
```
✅ Should return: JSON array with integration types

### Test 3: Browser console (F12)
```
Open: http://localhost:3000
Press F12 → Console tab
```
✅ Should NOT see any CORS or network errors

---

## 🐛 **If Still Not Working:**

### Check 1: Containers are on the same network
```powershell
docker network inspect workflow-automation-platform_default
```

Should show both `frontend` and `backend` containers.

### Check 2: Backend is actually running
```powershell
docker-compose ps
```

All should show "Up" status.

### Check 3: Environment variable is set correctly
```powershell
docker-compose exec frontend printenv | findstr VITE_API_URL
```

Should show: `VITE_API_URL=http://backend:8000`

### Check 4: Vite picked up the new config
```powershell
# Check if Vite is using the correct proxy target
docker-compose logs frontend | findstr "proxy"
```

---

## 🔄 **Complete Fresh Restart:**

If issues persist, do a complete rebuild:

```powershell
# 1. Stop and remove everything
docker-compose down -v

# 2. Remove old images
docker-compose rm -f

# 3. Rebuild from scratch
docker-compose build --no-cache

# 4. Start services
docker-compose up -d

# 5. Wait for everything to start
Start-Sleep -Seconds 60

# 6. Initialize database (if needed)
docker-compose exec backend python -c "from app.database import init_db; init_db()"
docker-compose exec backend python setup_integration_types.py

# 7. Test
curl http://localhost:8000/api/integration-types
start http://localhost:3000
```

---

## 📊 **Understanding Docker Networking:**

In Docker Compose:

### ❌ **WRONG** (doesn't work in Docker):
```
Frontend Container → localhost:8000 → ❌ Nothing there!
```

### ✅ **CORRECT** (works in Docker):
```
Frontend Container → backend:8000 → ✅ Backend Container!
```

Docker Compose creates a network where containers can reach each other using their **service names** as hostnames.

---

## 🎯 **Key Changes Made:**

1. **vite.config.ts**: Use `backend:8000` instead of `localhost:8000`
2. **docker-compose.yml**: Set `VITE_API_URL=http://backend:8000`
3. **vite.config.ts**: Added `host: true` for Docker compatibility
4. **docker-compose.yml**: Removed obsolete `version` field

---

## ✅ **Success Indicators:**

After the fix:

✅ No `ECONNREFUSED` errors in logs  
✅ `curl http://localhost:8000/health` returns healthy  
✅ `docker-compose exec frontend curl http://backend:8000/health` works  
✅ Browser shows Integration Types page with 4 cards  
✅ No errors in browser console (F12)  

---

## 🎉 **Quick Fix Command:**

```powershell
docker-compose down; `
docker-compose up --build -d; `
Start-Sleep -Seconds 30; `
start http://localhost:3000
```

---

**The fix is already applied to your files! Just restart the containers and it should work!** 🚀
