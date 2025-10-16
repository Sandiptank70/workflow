# Execution History - Quick Reference

## 🚀 Quick Access

### UI:
```
http://localhost:3000/executions
```

### API:
```bash
# All executions
curl http://localhost:8000/api/workflows/executions/all

# Specific workflow
curl http://localhost:8000/api/workflows/1/executions
```

---

## 📊 What You See

### Execution Table:
- ID | Status | Started At | Duration | Nodes | Trigger | Actions

### View Details Modal:
- Summary cards (status, duration, nodes, trigger)
- Timeline (start/end time)
- Error message (if failed)
- Node-by-node results:
  - ① Number
  - ✅/❌ Icon
  - Task name
  - ⏱️ Time
  - 💬 Message
  - 📦 **Response data** (expandable!)
  - 🕐 Timestamp

---

## 🎯 Common Tasks

### View All Executions:
1. Go to **Executions** tab
2. See history table

### View Execution Details:
1. Click **"View Details"** button
2. Explore modal

### See Response Data:
1. Open execution modal
2. Scroll to node
3. Click **"View Response Data"**
4. See full JSON

### Refresh List:
Click **"Refresh"** button

---

## 💡 Quick Tips

✅ Green badge = Success
❌ Red badge = Failed  
🔵 Blue badge = Running
⏱️ Duration shows execution time
📊 Nodes shows progress (3/3)
🔄 Trigger shows source (api, manual, etc.)

---

## 📡 API Examples

```bash
# Get all executions
curl http://localhost:8000/api/workflows/executions/all

# Filter successful (with jq)
curl http://localhost:8000/api/workflows/executions/all | \
  jq '.[] | select(.status == "success")'

# Get execution count
curl http://localhost:8000/api/workflows/executions/all | \
  jq 'length'
```

---

## 🎉 Try It

```bash
# 1. Execute workflow
curl -X POST http://localhost:8000/api/workflows/1/trigger

# 2. View history
Open http://localhost:3000/executions

# 3. Click "View Details"

# 4. Expand response data!
```

---

**See complete history with all data!** 📊✨
