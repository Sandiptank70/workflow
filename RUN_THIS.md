# 🎯 FINISH IN 30 SECONDS

## You're here: `/mnt/user-data/outputs/workflow-automation-platform/backend`

## Run These 3 Commands:

```bash
# 1. Add the tasks column
python3 add_column_simple.py

# 2. Go back and restart
cd ..
docker-compose restart backend

# 3. Test it (wait 10 seconds)
sleep 10
curl http://localhost:8000/api/import-export/export/all
```

## If You See JSON → ✅ SUCCESS!

---

## What You Get:

1. ✅ Export/Import entire configuration
2. ✅ Human-readable task names
3. ✅ Deploy to new environments in seconds
4. ✅ Separate export for types, integrations, workflows

---

## Quick Examples:

```bash
# Export everything
curl http://localhost:8000/api/import-export/export/all > backup.json

# Import everything
curl -X POST http://localhost:8000/api/import-export/import/all \
  -H "Content-Type: application/json" \
  -d @backup.json

# Export only workflows
curl http://localhost:8000/api/import-export/export/workflows > workflows.json

# Import only workflows
curl -X POST http://localhost:8000/api/import-export/import/workflows \
  -H "Content-Type: application/json" \
  -d @workflows.json
```

---

**Copy-paste these 3 lines:**
```bash
python3 add_column_simple.py && cd .. && docker-compose restart backend
```

**Done!** 🎉
