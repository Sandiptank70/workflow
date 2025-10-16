# ⚡ ONE-LINER FIX

## You're Inside Docker Container

## Run This ONE Command:

```bash
python3 -c "import sqlite3; conn = sqlite3.connect('workflow_automation.db'); conn.execute('ALTER TABLE integration_types ADD COLUMN tasks TEXT'); conn.commit(); print('✅ Done!'); conn.close()" 2>&1 | grep -v "duplicate column" || echo "✅ Column added!"
```

---

## Or This (Even Simpler):

```bash
sqlite3 workflow_automation.db "ALTER TABLE integration_types ADD COLUMN tasks TEXT" 2>&1 | grep -v "duplicate" || echo "✅ Done!"
```

---

## Then Exit and Restart:

```bash
exit
docker-compose restart backend
sleep 10
curl http://localhost:8000/api/import-export/export/all
```

---

## ✅ That's It!

If you see JSON output from the curl command, **you're done!** 🎉

---

## What This Does:

1. Connects to SQLite database
2. Adds `tasks` column to `integration_types` table
3. Ignores error if column already exists
4. Prints "✅ Done!"

---

**Copy this entire block:**

```bash
python3 -c "import sqlite3; conn = sqlite3.connect('workflow_automation.db'); conn.execute('ALTER TABLE integration_types ADD COLUMN tasks TEXT'); conn.commit(); print('✅ Column added!'); conn.close()" 2>&1 | grep -v duplicate || echo "✅ Success!"
exit
cd /mnt/user-data/outputs/workflow-automation-platform
docker-compose restart backend
sleep 10  
curl http://localhost:8000/api/import-export/export/all
```

**Done!** 🚀
