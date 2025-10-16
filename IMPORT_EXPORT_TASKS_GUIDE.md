# 📦 Import/Export & Task Management - Complete Guide

## 🎯 Two Major Features Added

### 1. **Dynamic Task Selection** ✅
- Integration types now define available tasks with human-readable names
- Clients see "Test Connection" instead of "test_connection"
- Task metadata includes descriptions and parameters
- Easy to update tasks in integration types

### 2. **Import/Export Functionality** ✅
- Export entire configuration to JSON
- Import configuration in new environments
- Separate export/import for:
  - Integration Types
  - Integrations
  - Workflows
- Or export/import everything at once

---

## 🎨 Feature 1: Dynamic Task Selection

### What Changed?

**Before:**
- Tasks were hardcoded function names
- User had to know: `test_connection`, `send_notification`, etc.
- No descriptions or help text

**After:**
- Integration types define available tasks
- Each task has:
  - `name`: Function name (e.g., "test_connection")
  - `display_name`: Human name (e.g., "Test Connection")
  - `description`: What it does
  - `parameters`: Task-specific params

### Example Task Definition:

```json
{
  "name": "test_connection",
  "display_name": "Test Connection",
  "description": "Test the Teams webhook connection",
  "parameters": []
},
{
  "name": "send_notification",
  "display_name": "Send Notification",
  "description": "Send a rich notification card to Teams channel",
  "parameters": [
    {
      "name": "title",
      "type": "string",
      "required": true,
      "description": "Notification title"
    },
    {
      "name": "message",
      "type": "string",
      "required": true,
      "description": "Notification message"
    },
    {
      "name": "color",
      "type": "string",
      "required": false,
      "description": "Card color (hex code)"
    }
  ]
}
```

### How to Update Integration Type with Tasks:

**Method 1: Via API**
```bash
curl -X POST http://localhost:8000/api/integration-types \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Teams",
    "description": "Microsoft Teams integration",
    "parameters": [
      {
        "name": "webhook_url",
        "type": "string",
        "required": true,
        "description": "Teams webhook URL"
      }
    ],
    "tasks": [
      {
        "name": "test_connection",
        "display_name": "Test Connection",
        "description": "Test webhook connection",
        "parameters": []
      },
      {
        "name": "send_notification",
        "display_name": "Send Notification",
        "description": "Send rich notification card",
        "parameters": [
          {"name": "title", "type": "string", "required": true},
          {"name": "message", "type": "string", "required": true}
        ]
      }
    ]
  }'
```

**Method 2: Via Import** (see below)

---

## 📦 Feature 2: Import/Export

### Available Endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/import-export/export/all` | GET | Export everything |
| `/api/import-export/export/integration-types` | GET | Export only types |
| `/api/import-export/export/integrations` | GET | Export only integrations |
| `/api/import-export/export/workflows` | GET | Export only workflows |
| `/api/import-export/import/all` | POST | Import everything |
| `/api/import-export/import/integration-types` | POST | Import only types |
| `/api/import-export/import/workflows` | POST | Import only workflows |

---

## 🚀 How to Use Import/Export

### Scenario 1: Moving to New Environment

#### Step 1: Export from OLD environment
```bash
# Export everything
curl http://old-server:8000/api/import-export/export/all > export.json

# Or export separately
curl http://old-server:8000/api/import-export/export/integration-types > types.json
curl http://old-server:8000/api/import-export/export/workflows > workflows.json
```

#### Step 2: Import to NEW environment
```bash
# Import everything
curl -X POST http://new-server:8000/api/import-export/import/all \
  -H "Content-Type: application/json" \
  -d @export.json

# Or import separately
curl -X POST http://new-server:8000/api/import-export/import/integration-types \
  -H "Content-Type: application/json" \
  -d @types.json

curl -X POST http://new-server:8000/api/import-export/import/workflows \
  -H "Content-Type: application/json" \
  -d @workflows.json
```

#### Step 3: Configure Integrations
**Important:** Credentials are NOT exported for security!

After import, manually configure integrations:
```bash
# Create integration with YOUR credentials
curl -X POST http://new-server:8000/api/integrations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Teams",
    "integration_type_id": 1,
    "credentials": {
      "webhook_url": "https://your-webhook-url"
    }
  }'
```

---

### Scenario 2: Backup Configuration

```bash
# Create backup
curl http://localhost:8000/api/import-export/export/all > backup-$(date +%Y%m%d).json

# Restore from backup
curl -X POST http://localhost:8000/api/import-export/import/all \
  -H "Content-Type: application/json" \
  -d @backup-20251015.json
```

---

### Scenario 3: Share Workflows

```bash
# Export only workflows (share with team)
curl http://localhost:8000/api/import-export/export/workflows > my-workflows.json

# Team member imports
curl -X POST http://localhost:8000/api/import-export/import/workflows \
  -H "Content-Type: application/json" \
  -d @my-workflows.json
```

---

## 📄 Export File Structure

### Complete Export (`export/all`):

```json
{
  "version": "1.0",
  "exported_at": "2025-10-15T10:30:00",
  "integration_types": [
    {
      "name": "Teams",
      "description": "Microsoft Teams",
      "parameters": [
        {
          "name": "webhook_url",
          "type": "string",
          "required": true,
          "description": "Webhook URL"
        }
      ],
      "tasks": [
        {
          "name": "test_connection",
          "display_name": "Test Connection",
          "description": "Test webhook",
          "parameters": []
        },
        {
          "name": "send_notification",
          "display_name": "Send Notification",
          "description": "Send notification card",
          "parameters": [
            {"name": "title", "type": "string", "required": true},
            {"name": "message", "type": "string", "required": true}
          ]
        }
      ]
    }
  ],
  "integrations": [
    {
      "name": "My Teams Channel",
      "integration_type_name": "Teams",
      "is_active": true,
      "credentials_template": "REPLACE_WITH_YOUR_CREDENTIALS"
    }
  ],
  "workflows": [
    {
      "name": "Daily Notification",
      "description": "Send daily status",
      "is_active": true,
      "workflow_data": {
        "nodes": [...],
        "connections": [...]
      }
    }
  ]
}
```

---

## 🔒 Security Notes

### Credentials Are NOT Exported!

For security, credentials are never included in exports.

**Export shows:**
```json
{
  "credentials_template": "REPLACE_WITH_YOUR_CREDENTIALS"
}
```

**You must manually configure:**
1. Import integration types
2. Create integrations with YOUR credentials
3. Import workflows

---

## 💡 Best Practices

### 1. Version Control Your Exports
```bash
# Create git repo for configs
mkdir workflow-configs
cd workflow-configs
git init

# Export configs
curl http://localhost:8000/api/import-export/export/all > config.json

# Commit
git add config.json
git commit -m "Updated workflow configuration"
git push
```

### 2. Separate Environments
```bash
# Development
curl http://dev-server:8000/api/import-export/export/all > dev-config.json

# Staging
curl -X POST http://staging-server:8000/api/import-export/import/all \
  -d @dev-config.json

# Production (manual review first!)
# Review staging, then:
curl -X POST http://prod-server:8000/api/import-export/import/all \
  -d @staging-config.json
```

### 3. Regular Backups
```bash
# Cron job for daily backup
0 0 * * * curl http://localhost:8000/api/import-export/export/all > /backups/workflow-$(date +\%Y\%m\%d).json
```

---

## 🎯 Import Options

### Skip Existing Items
```json
{
  "integration_types": [...],
  "skip_existing": true  // Skip if already exists
}
```

### Overwrite Existing
```json
{
  "skip_existing": false  // Update existing items
}
```

---

## 📊 Import Response

```json
{
  "success": true,
  "message": "Import completed",
  "results": {
    "integration_types": {
      "imported": 5,
      "skipped": 2,
      "errors": []
    },
    "integrations": {
      "imported": 0,
      "skipped": 3,
      "errors": ["My Teams: Skipped - credentials required"]
    },
    "workflows": {
      "imported": 10,
      "skipped": 0,
      "errors": []
    }
  }
}
```

---

## 🧪 Testing

### Test Export
```bash
# Export
curl http://localhost:8000/api/import-export/export/all | jq '.'

# Should see:
# - version: "1.0"
# - exported_at: timestamp
# - integration_types: array
# - integrations: array
# - workflows: array
```

### Test Import
```bash
# Create test export
echo '{
  "integration_types": [
    {
      "name": "TestType",
      "description": "Test",
      "parameters": [],
      "tasks": []
    }
  ],
  "integrations": [],
  "workflows": [],
  "skip_existing": true
}' > test-import.json

# Import
curl -X POST http://localhost:8000/api/import-export/import/all \
  -H "Content-Type: application/json" \
  -d @test-import.json

# Check
curl http://localhost:8000/api/integration-types | jq '.[] | select(.name=="TestType")'
```

---

## 🔧 Troubleshooting

### Problem: Import fails
**Solution:** Check JSON format
```bash
# Validate JSON
cat export.json | jq '.'
```

### Problem: Integrations not working after import
**Cause:** Credentials not included  
**Solution:** Manually configure integrations

### Problem: "Already exists" error
**Solution:** Use `skip_existing: true`

---

## 📚 Quick Reference

```bash
# Export everything
curl http://localhost:8000/api/import-export/export/all > backup.json

# Import everything  
curl -X POST http://localhost:8000/api/import-export/import/all \
  -H "Content-Type: application/json" \
  -d @backup.json

# Export types only
curl http://localhost:8000/api/import-export/export/integration-types > types.json

# Import types only
curl -X POST http://localhost:8000/api/import-export/import/integration-types \
  -H "Content-Type: application/json" \
  -d @types.json

# Export workflows only
curl http://localhost:8000/api/import-export/export/workflows > workflows.json

# Import workflows only
curl -X POST http://localhost:8000/api/import-export/import/workflows \
  -H "Content-Type: application/json" \
  -d @workflows.json
```

---

## ✅ Summary

### Dynamic Tasks Feature:
- ✅ Tasks defined in integration types
- ✅ Human-readable display names
- ✅ Task descriptions
- ✅ Parameter specifications
- ✅ Easy to update

### Import/Export Feature:
- ✅ Export all or separately
- ✅ Import all or separately
- ✅ JSON format
- ✅ Version control friendly
- ✅ Secure (no credentials exported)
- ✅ Skip/overwrite options
- ✅ Detailed import results

---

**Both features are production-ready and fully functional!** 🎉
