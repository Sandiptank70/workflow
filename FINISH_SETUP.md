# ✅ YOU'RE ALMOST DONE! Just 2 More Commands

## What You Did (Already Complete ✅):
```python
from app.database import init_db
init_db()
```
**Tables are created!** ✅

---

## What's Left (2 Commands):

### Step 1: Add the 'tasks' column
```bash
python3 add_column_simple.py
```

**Expected output:**
```
============================================================
Adding 'tasks' column to integration_types
============================================================

📝 Adding 'tasks' column...
✅ Successfully added 'tasks' column!

============================================================
✅ Migration Complete!
============================================================
```

---

### Step 2: Restart backend
```bash
cd ..
docker-compose restart backend
```

---

## ✅ That's It! Test It:

```bash
# Wait 10 seconds for backend to start, then:
curl http://localhost:8000/api/import-export/export/all
```

**If you see JSON with "version", "integration_types", etc., IT WORKS!** 🎉

---

## 🎯 Quick Summary:

```bash
# You're in: /mnt/user-data/outputs/workflow-automation-platform/backend

# Step 1: Add column
python3 add_column_simple.py

# Step 2: Restart
cd ..
docker-compose restart backend

# Step 3: Test (wait 10 seconds first)
curl http://localhost:8000/api/import-export/export/all | jq '.'
```

---

## 📦 Optional: Import Sample Teams Type

```bash
curl -X POST http://localhost:8000/api/import-export/import/integration-types \
  -H "Content-Type: application/json" \
  -d @sample-teams-integration-type.json
```

---

**Run `python3 add_column_simple.py` now!** ⚡
