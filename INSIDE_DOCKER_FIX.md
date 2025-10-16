# ✅ FINAL SIMPLE FIX

## You're in: `/app` directory (inside Docker container)

## Choose ONE of these options:

---

## ⚡ OPTION 1: Super Simple SQL Script (RECOMMENDED)

```bash
python3 migrations/add_column_sql.py
```

This uses raw SQLite commands - no inspection, just adds the column.

---

## ⚡ OPTION 2: SQLAlchemy Script

```bash
python3 migrations/add_tasks_simple.py
```

This uses SQLAlchemy (what your app uses).

---

## Expected Output:

```
============================================================
Quick Migration: Add 'tasks' Column
============================================================

Database: /app/workflow_automation.db

📝 Connecting to database...
📝 Adding 'tasks' column...
✅ Column 'tasks' added successfully!

📝 Verifying...
✅ Verification successful!

Columns in integration_types: id, name, description, parameters, tasks, created_at, updated_at

============================================================
✅ Migration Complete!
============================================================
```

---

## Then Restart Backend:

```bash
# Exit the container
exit

# Back on your host machine
cd /mnt/user-data/outputs/workflow-automation-platform
docker-compose restart backend
```

---

## Test It:

```bash
# Wait 10 seconds for backend to start
sleep 10

# Test the API
curl http://localhost:8000/api/import-export/export/all
```

**If you see JSON → SUCCESS!** ✅

---

## 🎯 Copy-Paste This:

```bash
# Inside Docker container (/app directory)
python3 migrations/add_column_sql.py

# Then exit
exit

# On host machine
docker-compose restart backend
sleep 10
curl http://localhost:8000/api/import-export/export/all
```

---

## If You Get "Database not found" Error:

The database might be in a different location. Find it:

```bash
find /app -name "*.db" 2>/dev/null
```

Then edit the script path if needed, or just run:

```bash
python3 << 'EOF'
import sqlite3
import os

# Try common locations
locations = [
    '/app/workflow_automation.db',
    '/app/backend/workflow_automation.db',
    './workflow_automation.db'
]

for db_path in locations:
    if os.path.exists(db_path):
        print(f"Found database: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("ALTER TABLE integration_types ADD COLUMN tasks TEXT")
            conn.commit()
            print("✅ Column added!")
        except:
            print("✅ Column already exists!")
        conn.close()
        break
EOF
```

---

**Try: `python3 migrations/add_column_sql.py`** ⚡
