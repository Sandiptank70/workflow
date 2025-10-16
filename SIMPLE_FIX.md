# 🎯 SIMPLE FIX - Step by Step

## Your Error:
```
⚠️  no such table: integration_types
```

---

## Fix in 3 Steps:

### Step 1️⃣: Run Quick Fix
```bash
cd /mnt/user-data/outputs/workflow-automation-platform
python3 quick-fix.py
```

**What you'll see:**
```
============================================================
Quick Fix: Creating Tables + Running Migration
============================================================

1️⃣ Creating database tables...
✅ Tables created successfully!

2️⃣ Running migration to add 'tasks' column...
✅ Column 'tasks' added successfully!

============================================================
✅ Quick Fix Complete!
============================================================
```

---

### Step 2️⃣: Restart Backend
```bash
docker-compose restart backend
```

**Wait 10 seconds...**

---

### Step 3️⃣: Test It
```bash
curl http://localhost:8000/api/import-export/export/all
```

**If you see JSON, it works!** ✅

---

## That's It! 🎉

Now you can:
- Export configurations
- Import configurations
- Use dynamic task names
- Deploy to new environments

---

## Try This:

```bash
# Export everything to a file
curl http://localhost:8000/api/import-export/export/all > my-config.json

# View the file
cat my-config.json | jq '.'
```

---

## Next Steps:

See **ALL_IN_ONE_GUIDE.md** for complete usage instructions.

---

**Just run these 3 commands and you're done!** ⚡

```bash
cd /mnt/user-data/outputs/workflow-automation-platform
python3 quick-fix.py
docker-compose restart backend
```
