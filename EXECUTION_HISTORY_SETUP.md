# 🔧 Execution History - Setup & Test Guide

## 🚀 Quick Setup

### Step 1: Restart Backend
```bash
cd /mnt/user-data/outputs/workflow-automation-platform
docker-compose restart backend
```

**Wait for:** "Application startup complete"

---

### Step 2: Restart Frontend
```bash
docker-compose restart frontend
```

**Wait for:** Frontend to rebuild (about 30 seconds)

---

### Step 3: Clear Browser Cache
1. Open http://localhost:3000
2. Press `Ctrl+Shift+R` (or `Cmd+Shift+R` on Mac)
3. This hard refreshes the page

---

## 🧪 Test Execution History

### Test 1: Execute a Workflow First

You need some executions to see history!

**Via UI:**
1. Go to http://localhost:3000/workflows
2. Click ▶️ Play button on any workflow
3. Wait for execution to complete
4. Modal should show

**Via API:**
```bash
curl -X POST http://localhost:8000/api/workflows/1/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "runtime_params": {"text": "Test execution"},
    "trigger_source": "test"
  }'
```

---

### Test 2: View Execution History

**Via UI:**
1. Go to http://localhost:3000
2. Click **"Executions"** tab in navigation
3. You should see your execution(s) in the table

**Via API:**
```bash
# Get all executions
curl http://localhost:8000/api/workflows/executions/all

# Pretty print
curl http://localhost:8000/api/workflows/executions/all | jq '.'
```

---

### Test 3: View Execution Details

1. In the Executions page
2. Click **"View Details"** button on any execution
3. Modal should open with:
   - Summary cards at top
   - Node-by-node results
   - Expandable response data

---

## 🔍 Troubleshooting

### Problem: "Executions" tab not showing

**Solution:**
```bash
# Check if frontend is running
docker-compose ps frontend

# Restart frontend
docker-compose restart frontend

# Check logs
docker-compose logs -f frontend
```

---

### Problem: Executions page is empty

**Possible causes:**

#### Cause 1: No executions yet
**Solution:** Execute a workflow first!
```bash
curl -X POST http://localhost:8000/api/workflows/1/trigger
```

#### Cause 2: API endpoint issue
**Check:**
```bash
curl http://localhost:8000/api/workflows/executions/all
```

**Should return:** JSON array (even if empty: `[]`)

**If error:** Restart backend
```bash
docker-compose restart backend
```

---

### Problem: Modal not opening

**Solution:**
1. Check browser console (F12)
2. Look for errors
3. Try hard refresh: `Ctrl+Shift+R`

---

### Problem: API returns 404

**Solution:**
```bash
# Restart backend
docker-compose restart backend

# Wait 10 seconds, then test
curl http://localhost:8000/api/workflows/executions/all
```

---

## ✅ Verification Checklist

Run through this checklist:

- [ ] Backend is running: `docker-compose ps backend`
- [ ] Frontend is running: `docker-compose ps frontend`
- [ ] Can access UI: http://localhost:3000
- [ ] "Executions" tab visible in navigation
- [ ] At least one workflow exists
- [ ] Execute a workflow (via UI or API)
- [ ] Go to Executions page: http://localhost:3000/executions
- [ ] See execution in table
- [ ] Click "View Details"
- [ ] Modal opens with data
- [ ] Can expand "View Response Data"

---

## 📊 Expected Behavior

### When You Open http://localhost:3000/executions

**If NO executions yet:**
```
┌────────────────────────────────────┐
│  Execution History                 │
│  View all workflow executions...   │
├────────────────────────────────────┤
│                                    │
│         🕐 No execution history    │
│                                    │
│  No execution history yet          │
│  Execute a workflow to see...      │
│                                    │
└────────────────────────────────────┘
```

**If executions exist:**
```
┌────────────────────────────────────────────────────────┐
│  Execution History                    [Refresh]        │
├────────────────────────────────────────────────────────┤
│ ID | Status  | Started At | Duration | Nodes | Trigger │
├────────────────────────────────────────────────────────┤
│ #1 | Success | Oct 15...  | 3.24s    | 3/3   | api    │
│ #2 | Failed  | Oct 15...  | 1.12s    | 1/3   | manual │
└────────────────────────────────────────────────────────┘
```

---

## 🎯 Complete Test Script

Run this complete test:

```bash
#!/bin/bash

echo "🧪 Testing Execution History Feature"
echo ""

echo "1️⃣ Checking backend..."
curl -s http://localhost:8000/api/workflows/executions/all > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backend API working"
else
    echo "❌ Backend API not responding"
    exit 1
fi

echo ""
echo "2️⃣ Checking if workflows exist..."
WORKFLOWS=$(curl -s http://localhost:8000/api/workflows)
WORKFLOW_COUNT=$(echo $WORKFLOWS | jq 'length')
echo "Found $WORKFLOW_COUNT workflows"

if [ $WORKFLOW_COUNT -eq 0 ]; then
    echo "⚠️  No workflows found. Create one first!"
    exit 1
fi

echo ""
echo "3️⃣ Executing test workflow..."
RESULT=$(curl -s -X POST http://localhost:8000/api/workflows/1/trigger \
  -H "Content-Type: application/json" \
  -d '{"runtime_params": {"text": "Test"}, "trigger_source": "test_script"}')

EXEC_ID=$(echo $RESULT | jq -r '.execution_id')
STATUS=$(echo $RESULT | jq -r '.status')

echo "Execution ID: $EXEC_ID"
echo "Status: $STATUS"

echo ""
echo "4️⃣ Checking execution history..."
sleep 1
EXECUTIONS=$(curl -s http://localhost:8000/api/workflows/executions/all)
EXEC_COUNT=$(echo $EXECUTIONS | jq 'length')
echo "Found $EXEC_COUNT executions"

if [ $EXEC_COUNT -gt 0 ]; then
    echo "✅ Execution history working!"
    echo ""
    echo "Latest execution:"
    echo $EXECUTIONS | jq '.[0] | {id, status, workflow_id}'
else
    echo "❌ No executions found"
    exit 1
fi

echo ""
echo "✅ ALL TESTS PASSED!"
echo ""
echo "🎉 Now open: http://localhost:3000/executions"
```

Save as `test_execution_history.sh` and run:
```bash
chmod +x test_execution_history.sh
./test_execution_history.sh
```

---

## 🔄 Full Reset (If Needed)

If nothing works, do a full reset:

```bash
# Stop everything
docker-compose down

# Remove volumes (this deletes the database!)
docker-compose down -v

# Rebuild
docker-compose build

# Start fresh
docker-compose up -d

# Wait 30 seconds
sleep 30

# Check status
docker-compose ps

# All should be "Up"
```

Then:
1. Create integration types
2. Create integrations
3. Create workflows
4. Execute workflows
5. View execution history!

---

## 📞 Quick Commands

```bash
# Restart both
docker-compose restart

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Test API
curl http://localhost:8000/api/workflows/executions/all | jq '.'

# Execute workflow
curl -X POST http://localhost:8000/api/workflows/1/trigger

# Open UI
xdg-open http://localhost:3000/executions  # Linux
open http://localhost:3000/executions      # Mac
```

---

## ✅ Success Criteria

You'll know it's working when:

1. ✅ http://localhost:3000 shows 4 tabs (including "Executions")
2. ✅ Clicking "Executions" shows the execution history page
3. ✅ After executing a workflow, it appears in the table
4. ✅ Clicking "View Details" opens a modal with full data
5. ✅ Can expand "View Response Data" for each node
6. ✅ API returns data: `curl http://localhost:8000/api/workflows/executions/all`

---

**Follow this guide and execution history will work perfectly!** 🎉
