# 🔧 Manual Setup Guide (Without Docker)

## Problem You Encountered

```
⚠️  Migration may have already run or error occurred: 
(sqlite3.OperationalError) no such table: integration_types
```

**This means:** The database tables don't exist yet!

---

## ✅ Solution: Complete Manual Setup

### Step 1: Create Database Tables First

```bash
cd /mnt/user-data/outputs/workflow-automation-platform/backend

# Start Python
python3

# In Python console:
>>> from app.database import init_db
>>> init_db()
>>> exit()
```

**Expected output:**
```
Database tables created successfully!
```

---

### Step 2: Now Run Migration

```bash
# Still in backend directory
python migrations/add_tasks_column.py
```

**Expected output:**
```
============================================================
Running Database Migration
============================================================

Creating tables if they don't exist...
✅ Tables created/verified!
✅ Successfully added 'tasks' column to integration_types table
============================================================
✅ Migration Complete!
```

---

### Step 3: Restart Backend

If running with Docker:
```bash
cd ..
docker-compose restart backend
```

If running locally:
```bash
# Stop backend (Ctrl+C)
# Start again:
uvicorn app.main:app --reload
```

---

### Step 4: Verify It Works

```bash
# Test the API
curl http://localhost:8000/api/import-export/export/all | jq '.'
```

**Expected:**
```json
{
  "version": "1.0",
  "exported_at": "2025-10-15T...",
  "integration_types": [],
  "integrations": [],
  "workflows": []
}
```

If you see this JSON, **it's working!** ✅

---

### Step 5: Import Sample Teams Type (Optional)

```bash
cd /mnt/user-data/outputs/workflow-automation-platform

curl -X POST http://localhost:8000/api/import-export/import/integration-types \
  -H "Content-Type: application/json" \
  -d @sample-teams-integration-type.json
```

**Expected:**
```json
{
  "success": true,
  "imported": 1,
  "skipped": 0,
  "errors": []
}
```

---

### Step 6: Verify Tasks Are There

```bash
curl http://localhost:8000/api/integration-types | jq '.[0].tasks'
```

**Expected:**
```json
[
  {
    "name": "test_connection",
    "display_name": "Test Connection",
    "description": "Test the Teams webhook connection",
    "parameters": []
  },
  {
    "name": "send_notification",
    "display_name": "Send Notification",
    "description": "Send a rich notification card",
    "parameters": [...]
  }
]
```

---

## 🎯 Alternative: Use the Python Setup Script

```bash
cd /mnt/user-data/outputs/workflow-automation-platform

python3 setup-complete.py
```

This script does everything automatically!

---

## ⚡ Quick Commands Summary

```bash
# 1. Create tables
cd backend
python3 -c "from app.database import init_db; init_db()"

# 2. Run migration
python migrations/add_tasks_column.py

# 3. Restart backend
cd ..
docker-compose restart backend
# OR if local: restart uvicorn

# 4. Test
curl http://localhost:8000/api/import-export/export/all | jq '.'

# 5. Import sample
curl -X POST http://localhost:8000/api/import-export/import/integration-types \
  -H "Content-Type: application/json" \
  -d @sample-teams-integration-type.json

# 6. Verify
curl http://localhost:8000/api/integration-types | jq '.[0].tasks'
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'app'"

**Solution:**
```bash
# Make sure you're in the backend directory
cd /mnt/user-data/outputs/workflow-automation-platform/backend

# And Python path is set
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Then run commands
```

---

### Error: "Connection refused" when testing API

**Cause:** Backend not running

**Solution:**
```bash
# Start backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### Error: "Column 'tasks' already exists"

**This is fine!** It means migration already ran successfully.

---

### Error: Cannot import sample file

**Solution:**
```bash
# Check file exists
ls -la sample-teams-integration-type.json

# If not found, make sure you're in the right directory
cd /mnt/user-data/outputs/workflow-automation-platform
```

---

## ✅ Success Checklist

- [ ] Tables created (`init_db()` ran)
- [ ] Migration completed (tasks column added)
- [ ] Backend restarted
- [ ] API responds: `/api/import-export/export/all`
- [ ] Sample imported (optional)
- [ ] Tasks visible in API response

---

## 🎉 Once Complete

You can now:
- ✅ Export/import configurations
- ✅ See human-readable task names
- ✅ Deploy to new environments quickly
- ✅ Share workflows with team
- ✅ Version control your configs

---

**Next:** See **ALL_IN_ONE_GUIDE.md** for full usage instructions!
