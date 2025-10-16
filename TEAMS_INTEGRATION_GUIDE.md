# Microsoft Teams Integration - Complete Setup Guide

## 🎯 Overview

I've created a complete Microsoft Teams integration with **7 different operations** for sending various types of notifications to Teams channels via webhooks.

---

## 📦 What's Included

### Available Operations:

1. **test_connection** - Test webhook connectivity
2. **send_simple_message** - Send plain text messages
3. **send_card_message** - Send formatted card messages
4. **send_notification** - Send status notifications (success/warning/error/info)
5. **send_rich_card** - Send rich cards with sections and facts
6. **send_workflow_status** - Send workflow execution status updates
7. **send_alert** - Send alert/urgent notifications

---

## 🚀 Setup Instructions

### Step 1: Get Your Teams Webhook URL

1. **Open Microsoft Teams**
2. **Go to the channel** where you want to receive notifications
3. **Click the three dots (...)** next to the channel name
4. **Select "Connectors"**
5. **Find "Incoming Webhook"** and click "Configure"
6. **Give it a name** (e.g., "Workflow Notifications")
7. **Click "Create"**
8. **Copy the webhook URL** - it looks like:
   ```
   https://outlook.office.com/webhook/xxxxx@xxxxx/IncomingWebhook/xxxxx
   ```
9. **Click "Done"**

---

### Step 2: Restart Backend (to load new integration)

```bash
docker-compose restart backend
```

Or if running locally:
```bash
# Stop uvicorn (Ctrl+C)
# Then restart:
uvicorn app.main:app --reload
```

---

### Step 3: Create Integration Type in UI

1. **Open** http://localhost:3000
2. **Go to "Integration Types"** tab
3. **Click "Create Integration Type"**

**Fill in the form:**

- **Name:** `teams`
- **Description:** `Microsoft Teams webhook integration for notifications`
- **Parameters:**
  - Click "Add Parameter"
  - **Name:** `webhook_url`
  - **Type:** `password`
  - **Required:** ✓ (checked)
  - **Description:** `Teams Incoming Webhook URL`

4. **Click "Create"**

✅ Integration Type created!

---

### Step 4: Create Integration Instance

1. **Go to "Integrations"** tab
2. **Click "Create Integration"**

**Fill in the form:**

- **Name:** `My Teams Channel` (or any name you like)
- **Type:** Select `teams`
- **Credentials:**
  - **webhook_url:** Paste your Teams webhook URL

3. **Click "Test Connection"**

✅ Should show: "Successfully connected to Microsoft Teams!"

4. **Click "Create"**

✅ Integration saved!

---

## 📚 Usage Examples

### Operation 1: Send Simple Message

**Use Case:** Quick text notifications

**Task:** `send_simple_message`

**Parameters:**
```json
{
  "text": "Hello from Workflow Automation Platform! 👋"
}
```

---

### Operation 2: Send Card Message

**Use Case:** Formatted messages with title and color

**Task:** `send_card_message`

**Parameters:**
```json
{
  "title": "Deployment Complete",
  "text": "Version 2.0 has been successfully deployed to production.",
  "color": "28A745"
}
```

**Color Options:**
- `28A745` - Green (success)
- `DC3545` - Red (error)
- `FFC107` - Yellow (warning)
- `0078D4` - Blue (info)
- Any hex color code

---

### Operation 3: Send Notification (with status)

**Use Case:** Status updates with automatic color coding

**Task:** `send_notification`

**Parameters:**

**Success Example:**
```json
{
  "title": "Backup Complete",
  "message": "Database backup completed successfully",
  "status": "success",
  "subtitle": "All data has been safely backed up"
}
```

**Warning Example:**
```json
{
  "title": "Disk Space Low",
  "message": "Server disk usage is at 85%",
  "status": "warning"
}
```

**Error Example:**
```json
{
  "title": "Build Failed",
  "message": "The build process encountered errors",
  "status": "error"
}
```

**Status Options:** `success`, `warning`, `error`, `info`

---

### Operation 4: Send Rich Card

**Use Case:** Detailed information with multiple sections and fields

**Task:** `send_rich_card`

**Parameters:**
```json
{
  "title": "Server Health Report",
  "summary": "Daily server status",
  "color": "0078D4",
  "sections": [
    {
      "title": "Production Server",
      "facts": [
        {"name": "Status", "value": "Online"},
        {"name": "CPU Usage", "value": "45%"},
        {"name": "Memory", "value": "8GB / 16GB"},
        {"name": "Uptime", "value": "15 days"}
      ],
      "text": "All systems operational"
    },
    {
      "title": "Database Server",
      "facts": [
        {"name": "Status", "value": "Online"},
        {"name": "Connections", "value": "127"},
        {"name": "Response Time", "value": "12ms"}
      ]
    }
  ]
}
```

---

### Operation 5: Send Workflow Status

**Use Case:** Notify about workflow execution results

**Task:** `send_workflow_status`

**Parameters:**

**Success:**
```json
{
  "workflow_name": "Daily Data Sync",
  "status": "success",
  "execution_time": "3.5s",
  "details": "Successfully synced 1,234 records"
}
```

**Failed:**
```json
{
  "workflow_name": "Payment Processing",
  "status": "failed",
  "execution_time": "1.2s",
  "details": "Connection to payment gateway timed out"
}
```

**Running:**
```json
{
  "workflow_name": "Batch Upload",
  "status": "running",
  "details": "Processing file 3 of 10"
}
```

**Status Options:** `success`, `failed`, `running`, `pending`, `error`

---

### Operation 6: Send Alert

**Use Case:** Urgent notifications requiring attention

**Task:** `send_alert`

**Parameters:**

**Critical Alert:**
```json
{
  "title": "Service Down",
  "message": "Production API is not responding",
  "severity": "critical",
  "source": "Monitoring System"
}
```

**High Alert:**
```json
{
  "title": "High Error Rate",
  "message": "Error rate exceeded 5% threshold",
  "severity": "high",
  "source": "Application Logs"
}
```

**Medium Alert:**
```json
{
  "title": "Unusual Activity",
  "message": "Login attempts from unknown location",
  "severity": "medium",
  "source": "Security System"
}
```

**Severity Options:** `critical`, `high`, `medium`, `low`

---

## 🎯 Real-World Workflow Examples

### Example 1: Deployment Notification Workflow

**Workflow:** Build → Deploy → Notify Teams

**Nodes:**
1. **GitHub**: `create_repo` or run build
2. **Teams**: `send_notification`
   ```json
   {
     "title": "Deployment Started",
     "message": "Deploying version 2.1.0",
     "status": "info"
   }
   ```
3. **Teams**: `send_notification`
   ```json
   {
     "title": "Deployment Complete",
     "message": "Version 2.1.0 is now live!",
     "status": "success"
   }
   ```

---

### Example 2: Daily Status Report

**Workflow:** Collect data → Send rich card

**Node:**
- **Teams**: `send_rich_card`
  ```json
  {
    "title": "Daily Status Report",
    "summary": "System health check",
    "sections": [
      {
        "title": "Application Metrics",
        "facts": [
          {"name": "Active Users", "value": "1,234"},
          {"name": "API Calls", "value": "45,678"},
          {"name": "Error Rate", "value": "0.02%"}
        ]
      },
      {
        "title": "Infrastructure",
        "facts": [
          {"name": "Server Status", "value": "All Online"},
          {"name": "Database Load", "value": "Normal"},
          {"name": "Cache Hit Rate", "value": "98%"}
        ]
      }
    ]
  }
  ```

---

### Example 3: Error Monitoring

**Workflow:** Monitor → Alert on error

**Nodes:**
1. Check for errors (custom logic)
2. **Teams**: `send_alert`
   ```json
   {
     "title": "Critical Error Detected",
     "message": "Payment processing service has failed",
     "severity": "critical",
     "source": "Error Monitoring"
   }
   ```

---

### Example 4: Workflow Status Updates

**Workflow:** Long-running task with status updates

**Nodes:**
1. **Teams**: `send_workflow_status` (Start)
   ```json
   {
     "workflow_name": "Data Migration",
     "status": "running",
     "details": "Starting data migration process"
   }
   ```

2. Execute migration tasks

3. **Teams**: `send_workflow_status` (Complete)
   ```json
   {
     "workflow_name": "Data Migration",
     "status": "success",
     "execution_time": "45m 30s",
     "details": "Migrated 1,000,000 records successfully"
   }
   ```

---

## 🎨 Color Reference

Use these hex colors for visual coding:

| Color | Hex Code | Use Case |
|-------|----------|----------|
| 🟢 Green | `28A745` | Success, completed |
| 🔴 Red | `DC3545` | Error, failed |
| 🟡 Yellow | `FFC107` | Warning, caution |
| 🔵 Blue | `0078D4` | Info, default |
| 🟤 Dark Red | `8B0000` | Critical alerts |
| 🔷 Cyan | `17A2B8` | Low priority |

---

## 🔍 Testing Your Integration

### Quick Test Workflow:

1. **Create a workflow** with one node
2. **Select your Teams integration**
3. **Choose task:** `send_simple_message`
4. **Set params:**
   ```json
   {
     "text": "🎉 Testing my Teams integration!"
   }
   ```
5. **Save and Execute**

✅ Check your Teams channel for the message!

---

## 🐛 Troubleshooting

### Error: "Invalid Teams webhook URL format"
- Make sure your URL starts with `https://`
- Must contain `office.com/webhook`
- Copy the full URL from Teams connector settings

### Error: "Connection timeout"
- Check your internet connection
- Verify the webhook URL is correct
- Make sure the webhook wasn't deleted in Teams

### Message not appearing in Teams
- Check you're looking at the correct channel
- Verify the webhook is still active (not removed)
- Try the `test_connection` task first

### Error: "Missing parameter"
- Check the JSON format is correct
- Make sure required fields are included
- Verify field names match exactly (case-sensitive)

---

## 📊 All Operations Summary

| Operation | Use Case | Required Params |
|-----------|----------|----------------|
| `test_connection` | Test webhook | None |
| `send_simple_message` | Plain text | `text` |
| `send_card_message` | Formatted message | `title`, `text` |
| `send_notification` | Status update | `title`, `message`, `status` |
| `send_rich_card` | Detailed info | `title`, `sections` |
| `send_workflow_status` | Workflow update | `workflow_name`, `status` |
| `send_alert` | Urgent alert | `title`, `message`, `severity` |

---

## 🎓 Pro Tips

1. **Use color coding** to make important messages stand out
2. **Add emojis** in text for better visibility: 🚀 ✅ ⚠️ ❌
3. **Keep messages concise** - Teams cards can be scrolled but short is better
4. **Use facts** in rich cards for structured data
5. **Test with `send_simple_message`** first before complex formats
6. **Create multiple integrations** for different channels
7. **Use workflow_status** for automated status updates

---

## ✅ You're All Set!

You now have a fully functional Microsoft Teams integration with 7 different notification types!

**Next Steps:**
1. Set up your webhook in Teams
2. Create the integration type in UI
3. Create an integration instance
4. Start using it in workflows!

---

**Happy notifying!** 🎉📢
