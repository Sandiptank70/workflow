# Workflow Parameters - Updated Guide

## ✅ What's Fixed

The Parameters (JSON) field in the workflow builder now works better:

1. **Optional Field** - You can leave it as `{}` if no parameters needed
2. **Better Validation** - Won't break if you type invalid JSON
3. **Clearer Instructions** - Shows helpful tips
4. **Graceful Handling** - Uses `{}` if JSON is invalid

---

## 🎯 How to Use Parameters

### Option 1: No Parameters Needed

**When:** Tasks like `test_connection` that don't need any input

**What to do:** Just leave it as `{}`

```json
{}
```

**Example Tasks:**
- `test_connection` (any integration)
- `list_s3_buckets` (AWS)

---

### Option 2: Simple Parameters

**When:** Tasks need basic input values

**What to do:** Add key-value pairs

```json
{
  "text": "Hello Teams!"
}
```

**Example Tasks:**
- `send_simple_message` (Teams)
  ```json
  {
    "text": "Your message here"
  }
  ```

- `create_repo` (GitHub)
  ```json
  {
    "repo_name": "my-new-repo",
    "private": true
  }
  ```

---

### Option 3: Complex Parameters

**When:** Tasks need multiple fields or nested data

**What to do:** Format JSON with proper structure

```json
{
  "title": "Deployment Complete",
  "message": "Version 2.0 is live!",
  "status": "success"
}
```

**Example Tasks:**
- `send_notification` (Teams)
  ```json
  {
    "title": "Build Status",
    "message": "Build completed successfully",
    "status": "success"
  }
  ```

- `send_rich_card` (Teams)
  ```json
  {
    "title": "Server Report",
    "sections": [
      {
        "title": "Status",
        "facts": [
          {"name": "CPU", "value": "45%"},
          {"name": "Memory", "value": "8GB"}
        ]
      }
    ]
  }
  ```

- `create_issue` (Jira)
  ```json
  {
    "project": "BUG",
    "summary": "Bug found in login",
    "description": "Users cannot log in",
    "issue_type": "Bug"
  }
  ```

---

## 📋 Parameter Templates

### Teams Integration

**send_simple_message:**
```json
{
  "text": "Message here"
}
```

**send_notification:**
```json
{
  "title": "Title",
  "message": "Message",
  "status": "success"
}
```
*Status options: success, warning, error, info*

**send_alert:**
```json
{
  "title": "Alert Title",
  "message": "Alert message",
  "severity": "high"
}
```
*Severity options: critical, high, medium, low*

**send_workflow_status:**
```json
{
  "workflow_name": "My Workflow",
  "status": "success",
  "execution_time": "3.5s"
}
```

---

### GitHub Integration

**test_connection:**
```json
{}
```

**create_repo:**
```json
{
  "repo_name": "repository-name",
  "description": "Description here",
  "private": false
}
```

**create_issue:**
```json
{
  "repo": "username/repository",
  "title": "Issue title",
  "body": "Issue description"
}
```

---

### Jira Integration

**test_connection:**
```json
{}
```

**create_issue:**
```json
{
  "project": "PROJECT_KEY",
  "summary": "Issue summary",
  "description": "Detailed description",
  "issue_type": "Bug"
}
```
*Issue types: Bug, Task, Story, Epic*

---

## 💡 Tips

### Tip 1: Leave Empty for Test
When testing connection, just use:
```json
{}
```

### Tip 2: Copy from Documentation
Each integration has example parameters in:
- `TEAMS_INTEGRATION_GUIDE.md` (for Teams)
- `ADDING_INTEGRATIONS_GUIDE.md` (for others)

### Tip 3: Check Task Function
Look at the task function's docstring in `backend/app/integrations/<name>/tasks.py` to see what parameters it expects.

Example from `teams/tasks.py`:
```python
def send_notification(credentials, params):
    """
    params:
    {
        "title": "Notification Title",
        "message": "Notification message",
        "status": "success" | "warning" | "error" | "info"
    }
    """
```

### Tip 4: Use JSON Validator
If unsure if your JSON is valid, paste it into: https://jsonlint.com

### Tip 5: Common Mistakes
❌ **Wrong:**
```json
{
  title: "No quotes on key"
}
```

❌ **Wrong:**
```json
{
  "title": 'Single quotes not allowed'
}
```

❌ **Wrong:**
```json
{
  "title": "Missing comma"
  "message": "here"
}
```

✅ **Correct:**
```json
{
  "title": "Proper quotes",
  "message": "With comma"
}
```

---

## 🔧 What Happens If JSON Is Invalid?

**Old behavior:** Node wouldn't be added, no error message

**New behavior:** 
1. Shows alert: "Invalid JSON format in parameters. Using empty object instead."
2. Node is still added with `{}` as parameters
3. You can edit the node later to fix parameters

---

## 🎯 Quick Reference

| Task Type | Parameters Needed? | Example |
|-----------|-------------------|---------|
| test_connection | ❌ No | `{}` |
| send_simple_message | ✅ Yes | `{"text": "..."}` |
| send_notification | ✅ Yes | `{"title": "...", "message": "...", "status": "..."}` |
| create_repo | ✅ Yes | `{"repo_name": "...", "private": true}` |
| create_issue | ✅ Yes | `{"repo": "...", "title": "...", "body": "..."}` |

---

## 🚀 Testing Your Parameters

### Step 1: Add a Test Node
1. Create workflow
2. Add node with your parameters
3. Save workflow

### Step 2: Execute
Click the Play button (▶️)

### Step 3: Check Results
- ✅ Success: Parameters were correct!
- ❌ Error: Check the error message, adjust parameters

### Step 4: Iterate
Edit workflow → Update parameters → Execute again

---

## 📞 Need Help?

**For Teams integration parameters:**
→ See `TEAMS_INTEGRATION_GUIDE.md`

**For adding your own integrations:**
→ See `ADDING_INTEGRATIONS_GUIDE.md`

**For JSON help:**
→ Use https://jsonlint.com to validate

---

**Remember: When in doubt, start with `{}` and add parameters gradually!** ✨
