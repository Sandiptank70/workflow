# Docker Setup - WORKING COMMANDS ✅

## 🎯 The API is working but tables are empty!

You confirmed:
- ✅ Backend is running
- ✅ API responds with `[]` (empty array)
- ❌ No integration types in database

---

## 🚀 **SOLUTION - Run These Commands:**

### **Step 1: Initialize Database Tables**
```bash
docker-compose exec backend python -c "from app.database import init_db; init_db(); print('✅ Tables created!')"
```

### **Step 2: Add Sample Integration Types**
```bash
docker-compose exec backend python setup_integration_types.py
```

### **Step 3: Verify**
```bash
curl http://localhost:8000/api/integration-types
```

You should now see JSON with 4 integration types instead of `[]`

---

## 📋 **Alternative: Use the New Init Script**

I've created a simpler script that works better in Docker:

```bash
docker-compose exec backend python init_db.py
docker-compose exec backend python setup_integration_types.py
curl http://localhost:8000/api/integration-types
```

---

## 🔍 **Detailed Debugging:**

### **Check if tables exist:**
```bash
docker-compose exec db mysql -u root -psecurepassword workflow_db -e "SHOW TABLES;"
```

Expected output:
```
+-------------------------+
| Tables_in_workflow_db   |
+-------------------------+
| execution_logs          |
| integration_types       |
| integrations            |
| workflows               |
+-------------------------+
```

If you see **Empty set**, tables don't exist yet. Run Step 1 above.

---

### **Check if integration types exist:**
```bash
docker-compose exec db mysql -u root -psecurepassword workflow_db -e "SELECT id, name FROM integration_types;"
```

Expected output:
```
+----+--------+
| id | name   |
+----+--------+
|  1 | jira   |
|  2 | github |
|  3 | aws    |
|  4 | azure  |
+----+--------+
```

If you see **Empty set**, run Step 2 above.

---

## 🛠️ **Manual Database Setup (If Above Fails):**

### **Access the database container:**
```bash
docker-compose exec db mysql -u root -psecurepassword workflow_db
```

### **Create tables manually:**
```sql
CREATE TABLE IF NOT EXISTS integration_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    parameters TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS integrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    integration_type_id INT NOT NULL,
    credentials TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (integration_type_id) REFERENCES integration_types(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS workflows (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    workflow_data TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS execution_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    workflow_id INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    execution_data TEXT,
    error_message TEXT,
    FOREIGN KEY (workflow_id) REFERENCES workflows(id) ON DELETE CASCADE
);

EXIT;
```

Then run Step 2 to add integration types.

---

## 🔄 **Complete Reset (If Nothing Works):**

```bash
# 1. Stop everything
docker-compose down -v

# 2. Start fresh
docker-compose up --build -d

# 3. Wait 60 seconds
timeout /t 60

# 4. Create tables
docker-compose exec backend python -c "from app.database import init_db; init_db(); print('✅ Done!')"

# 5. Add integration types
docker-compose exec backend python setup_integration_types.py

# 6. Verify
curl http://localhost:8000/api/integration-types
```

---

## ✅ **Success Check:**

After running the commands, this should work:

```bash
curl http://localhost:8000/api/integration-types
```

**Before (Empty):**
```json
[]
```

**After (With Data):**
```json
[
  {
    "id": 1,
    "name": "jira",
    "description": "Atlassian Jira project management integration",
    "parameters": [...],
    "created_at": "2025-10-15T08:10:00"
  },
  {
    "id": 2,
    "name": "github",
    ...
  },
  ...
]
```

---

## 🌐 **Open the Application:**

Once the API returns data:

```bash
start http://localhost:3000
```

You should see 4 integration type cards on the "Integration Types" page!

---

## 🐛 **Common Issues:**

### **Issue: "Command not found" error**
**Solution:** Make sure you're in the project directory:
```bash
cd C:\Users\Sandip Tank\Downloads\files\workflow-automation-platform
```

### **Issue: Tables exist but still empty**
**Solution:** Run the setup script:
```bash
docker-compose exec backend python setup_integration_types.py
```

### **Issue: "Access denied" database error**
**Solution:** Check docker-compose.yml passwords match:
```yaml
backend:
  environment:
    - DB_PASSWORD=securepassword
db:
  environment:
    - MYSQL_ROOT_PASSWORD=securepassword
```

### **Issue: API returns 500 error**
**Solution:** Check backend logs:
```bash
docker-compose logs backend
```

---

## 📊 **Verification Commands:**

Run all these to verify everything:

```bash
# 1. Containers running?
docker-compose ps

# 2. Backend healthy?
curl http://localhost:8000/health

# 3. Tables exist?
docker-compose exec db mysql -u root -psecurepassword workflow_db -e "SHOW TABLES;"

# 4. Integration types exist?
docker-compose exec db mysql -u root -psecurepassword workflow_db -e "SELECT COUNT(*) FROM integration_types;"

# 5. API returns data?
curl http://localhost:8000/api/integration-types

# 6. Frontend loads?
curl http://localhost:3000
```

---

## 🎉 **Expected Final State:**

✅ All 4 containers running  
✅ Backend returns `{"status":"healthy"}`  
✅ Database has 4 tables  
✅ `integration_types` table has 4 rows  
✅ API returns array with 4 integration types  
✅ Frontend shows 4 cards on Integration Types page  

---

## 🎯 **ONE COMMAND TO FIX EVERYTHING:**

```powershell
docker-compose exec backend python -c "from app.database import init_db; init_db(); print('✅ Tables created!')"; `
docker-compose exec backend python setup_integration_types.py; `
curl http://localhost:8000/api/integration-types
```

---

**Try the commands above and the "Failed to load integration types" error should be gone!** 🚀
