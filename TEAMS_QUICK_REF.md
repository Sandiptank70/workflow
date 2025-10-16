# Teams Integration - Quick Reference Card

## 🚀 Quick Setup

```bash
# 1. Restart backend
docker-compose restart backend

# 2. Create Integration Type in UI
Name: teams
Param: webhook_url (password, required)

# 3. Get Teams Webhook
Teams → Channel → Connectors → Incoming Webhook → Copy URL

# 4. Create Integration
Paste webhook URL → Test → Create

# 5. Use in Workflows!
```

---

## 📋 All 7 Operations

### 1️⃣ test_connection
```json
{}
```
✅ Tests webhook is working

---

### 2️⃣ send_simple_message
```json
{
  "text": "Your message here"
}
```
📝 Quick plain text message

---

### 3️⃣ send_card_message
```json
{
  "title": "Title Here",
  "text": "Message body",
  "color": "0078D4"
}
```
💳 Formatted card with color

**Colors:** Green `28A745`, Red `DC3545`, Yellow `FFC107`, Blue `0078D4`

---

### 4️⃣ send_notification
```json
{
  "title": "Notification Title",
  "message": "Your message",
  "status": "success"
}
```
🔔 Auto-colored status notification

**Status:** `success`, `warning`, `error`, `info`

---

### 5️⃣ send_rich_card
```json
{
  "title": "Card Title",
  "sections": [
    {
      "title": "Section 1",
      "facts": [
        {"name": "Field", "value": "Value"}
      ]
    }
  ]
}
```
📊 Detailed card with sections

---

### 6️⃣ send_workflow_status
```json
{
  "workflow_name": "My Workflow",
  "status": "success",
  "execution_time": "3.5s",
  "details": "Additional info"
}
```
🔄 Workflow execution updates

**Status:** `success`, `failed`, `running`, `pending`

---

### 7️⃣ send_alert
```json
{
  "title": "Alert Title",
  "message": "Alert message",
  "severity": "high",
  "source": "System Name"
}
```
🚨 Urgent alerts

**Severity:** `critical`, `high`, `medium`, `low`

---

## 🎨 Quick Colors

| Use | Color |
|-----|-------|
| ✅ Success | `28A745` |
| ❌ Error | `DC3545` |
| ⚠️ Warning | `FFC107` |
| ℹ️ Info | `0078D4` |
| 🚨 Critical | `8B0000` |

---

## 💡 Common Use Cases

```json
// Deployment notification
{
  "task": "send_notification",
  "params": {
    "title": "Deploy Complete",
    "message": "v2.0 is live!",
    "status": "success"
  }
}

// Error alert
{
  "task": "send_alert",
  "params": {
    "title": "Service Down",
    "message": "API not responding",
    "severity": "critical"
  }
}

// Daily report
{
  "task": "send_rich_card",
  "params": {
    "title": "Daily Report",
    "sections": [{
      "facts": [
        {"name": "Users", "value": "1,234"},
        {"name": "Revenue", "value": "$5,678"}
      ]
    }]
  }
}

// Workflow update
{
  "task": "send_workflow_status",
  "params": {
    "workflow_name": "Backup",
    "status": "success",
    "execution_time": "2m"
  }
}
```

---

## ✅ Testing Checklist

- [ ] Backend restarted
- [ ] Integration type `teams` created
- [ ] Webhook URL obtained from Teams
- [ ] Integration instance created
- [ ] Test connection successful ✅
- [ ] Test message sent to Teams ✅
- [ ] Message appeared in channel ✅

---

## 🐛 Quick Fixes

**No message in Teams?**
→ Check correct channel, webhook not deleted

**Invalid webhook error?**
→ Must start with `https://` and contain `office.com/webhook`

**Timeout error?**
→ Check internet connection, verify webhook URL

**Missing parameter?**
→ Check JSON format, field names (case-sensitive)

---

## 📞 Get Help

See full guide: `TEAMS_INTEGRATION_GUIDE.md`
