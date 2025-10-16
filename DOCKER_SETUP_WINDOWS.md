# Docker Setup Commands - Windows

## 🐳 Complete Docker Setup for Windows

### **Step 1: Stop and Clean Everything**
```bash
docker-compose down -v
```

### **Step 2: Start Services**
```bash
docker-compose up --build -d
```

### **Step 3: Wait for Database (Important!)**
```bash
# Wait 60 seconds for MariaDB to fully initialize
timeout /t 60
```

### **Step 4: Run Diagnostic (Correct Command)**
```bash
# Note: Run from /app directory inside container
docker-compose exec backend bash -c "cd /app && python diagnose_db.py"
```

### **Step 5: Initialize Integration Types**
```bash
docker-compose exec backend bash -c "cd /app && python setup_integration_types.py"
```

### **Step 6: Verify**
```bash
curl http://localhost:8000/api/integration-types
```

---

## 🎯 **ONE COMMAND TO DO IT ALL (Windows PowerShell):**

```powershell
docker-compose down -v; `
docker-compose up --build -d; `
Start-Sleep -Seconds 60; `
docker-compose exec backend bash -c "cd /app && python diagnose_db.py"; `
docker-compose exec backend bash -c "cd /app && python setup_integration_types.py"; `
Write-Host "Done! Open http://localhost:3000"
```

---

## 🎯 **ONE COMMAND TO DO IT ALL (Windows CMD):**

```cmd
docker-compose down -v && docker-compose up --build -d && timeout /t 60 && docker-compose exec backend bash -c "cd /app && python diagnose_db.py" && docker-compose exec backend bash -c "cd /app && python setup_integration_types.py" && echo Done! Open http://localhost:3000
```

---

## 🔍 **Troubleshooting Commands (Windows):**

### Check if containers are running:
```bash
docker-compose ps
```

### View backend logs:
```bash
docker-compose logs backend
```

### View last 50 lines of logs:
```bash
docker-compose logs --tail=50 backend
```

### Check database logs:
```bash
docker-compose logs db
```

### Access backend shell:
```bash
docker-compose exec backend bash

# Once inside:
cd /app
python diagnose_db.py
exit
```

### Test database connection manually:
```bash
docker-compose exec backend bash -c "cd /app && python -c 'from app.database import engine; engine.connect(); print(\"✅ Connected!\")'"
```

### Check if database is ready:
```bash
docker-compose exec db mysql -u root -psecurepassword -e "SHOW DATABASES;"
```

### Manually create tables:
```bash
docker-compose exec backend bash -c "cd /app && python -c 'from app.database import init_db; init_db(); print(\"✅ Tables created!\")'"
```

### Check tables exist:
```bash
docker-compose exec db mysql -u root -psecurepassword workflow_db -e "SHOW TABLES;"
```

### Check integration types in database:
```bash
docker-compose exec db mysql -u root -psecurepassword workflow_db -e "SELECT id, name FROM integration_types;"
```

---

## 🔄 **If You Get "No module named 'app'" Error:**

The issue is running the script from wrong directory. Always use:

```bash
docker-compose exec backend bash -c "cd /app && python diagnose_db.py"
```

NOT:
```bash
docker-compose exec backend python app/diagnose_db.py  ❌
```

---

## 📋 **Complete Fresh Install (Windows):**

```cmd
REM 1. Clean everything
docker-compose down -v
docker system prune -f

REM 2. Build and start
docker-compose up --build -d

REM 3. Wait for database
timeout /t 60

REM 4. Check if services are up
docker-compose ps

REM 5. Initialize database
docker-compose exec backend bash -c "cd /app && python diagnose_db.py"

REM 6. Add sample data
docker-compose exec backend bash -c "cd /app && python setup_integration_types.py"

REM 7. Test API
curl http://localhost:8000/api/integration-types

REM 8. Open browser
start http://localhost:3000
```

---

## ✅ **Verification Checklist:**

Run these commands to verify everything is working:

```bash
# 1. Containers running?
docker-compose ps
# Should show: backend (Up), frontend (Up), db (Up healthy)

# 2. Backend healthy?
curl http://localhost:8000/health
# Should return: {"status":"healthy"}

# 3. Database accessible?
docker-compose exec db mysql -u root -psecurepassword -e "SELECT 1;"
# Should return: 1

# 4. Tables exist?
docker-compose exec db mysql -u root -psecurepassword workflow_db -e "SHOW TABLES;"
# Should show: integration_types, integrations, workflows, execution_logs

# 5. Integration types exist?
curl http://localhost:8000/api/integration-types
# Should return: JSON array with jira, github, aws, azure

# 6. Frontend accessible?
curl http://localhost:3000
# Should return: HTML content
```

---

## 🐛 **Common Errors & Fixes:**

### Error: "No module named 'app'"
**Fix:** Always run from /app directory:
```bash
docker-compose exec backend bash -c "cd /app && python diagnose_db.py"
```

### Error: "Can't connect to MySQL server"
**Fix:** Database not ready yet. Wait longer:
```bash
timeout /t 60
docker-compose exec backend bash -c "cd /app && python diagnose_db.py"
```

### Error: "Access denied for user 'root'"
**Fix:** Check docker-compose.yml has matching passwords:
```yaml
backend:
  environment:
    - DB_PASSWORD=securepassword
db:
  environment:
    - MYSQL_ROOT_PASSWORD=securepassword
```

### Error: Port already in use
**Fix:** Stop conflicting services:
```bash
# Kill processes on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or change ports in docker-compose.yml
```

---

## 🎉 **Success Indicators:**

You'll know it's working when:

1. ✅ `docker-compose ps` shows all containers "Up"
2. ✅ `curl http://localhost:8000/health` returns `{"status":"healthy"}`
3. ✅ `curl http://localhost:8000/api/integration-types` returns JSON array
4. ✅ Browser at `http://localhost:3000` shows the application
5. ✅ "Integration Types" page shows 4 cards (Jira, GitHub, AWS, Azure)

---

## 📞 **Still Having Issues?**

Run the diagnostic in verbose mode:

```bash
docker-compose exec backend bash -c "cd /app && python -u diagnose_db.py"
```

Or check individual components:

```bash
# Test Python can import app
docker-compose exec backend bash -c "cd /app && python -c 'import app; print(\"✅ Import OK\")'"

# Test database module
docker-compose exec backend bash -c "cd /app && python -c 'from app.database import engine; print(\"✅ Database module OK\")'"

# Test connection
docker-compose exec backend bash -c "cd /app && python -c 'from app.database import engine; engine.connect(); print(\"✅ Connection OK\")'"
```

---

**Key Point:** Always use `cd /app &&` before running Python scripts in Docker! 🐳
