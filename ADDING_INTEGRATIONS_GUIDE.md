# Complete Guide: Adding New Integrations

This guide explains how to add new integrations to the platform, including creating the backend integration module and using it in the UI.

---

## 🎯 Overview

When you create an **Integration Type** in the UI, you also need a corresponding **backend integration module** that handles the actual API calls and tasks.

### The Flow:
1. **Create Backend Integration Module** (Python) - Handles API calls
2. **Create Integration Type in UI** - Defines credentials needed
3. **Create Integration in UI** - Stores credentials
4. **Use Integration in Workflows** - Execute tasks

---

## 📁 Part 1: Creating Backend Integration Module

### Structure

Each integration is a Python module in `backend/app/integrations/<integration_name>/`

```
backend/app/integrations/
├── slack/              # New integration
│   ├── __init__.py
│   └── tasks.py        # All tasks for this integration
├── jira/               # Existing example
│   ├── __init__.py
│   └── tasks.py
└── github/             # Existing example
    ├── __init__.py
    └── tasks.py
```

---

## 📝 Example: Adding Slack Integration

### Step 1: Create the Integration Module

Create directory:
```bash
mkdir backend/app/integrations/slack
```

### Step 2: Create `tasks.py`

**File: `backend/app/integrations/slack/tasks.py`**

```python
import requests
from typing import Dict, Any

def test_connection(credentials: Dict[str, Any]) -> Dict[str, Any]:
    """
    Test Slack connection
    
    Expected credentials:
    {
        "webhook_url": "https://hooks.slack.com/services/xxx/yyy/zzz",
        "bot_token": "xoxb-xxxxx" (optional, for advanced features)
    }
    """
    try:
        webhook_url = credentials.get("webhook_url")
        
        if not webhook_url:
            return {
                "success": False,
                "message": "Missing webhook_url"
            }
        
        # Test by sending a test message
        response = requests.post(
            webhook_url,
            json={"text": "✅ Connection test successful!"},
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": "Successfully connected to Slack!",
                "data": {"status": "connected"}
            }
        else:
            return {
                "success": False,
                "message": f"Connection failed: {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

def send_message(credentials: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send a message to Slack
    
    params:
    {
        "text": "Hello from workflow!",
        "channel": "#general" (optional if using webhook)
    }
    """
    try:
        webhook_url = credentials.get("webhook_url")
        text = params.get("text")
        channel = params.get("channel")
        
        if not text:
            return {
                "success": False,
                "message": "Missing 'text' parameter"
            }
        
        payload = {"text": text}
        if channel:
            payload["channel"] = channel
        
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": "Message sent successfully!",
                "data": {"text": text, "channel": channel}
            }
        else:
            return {
                "success": False,
                "message": f"Failed to send message: {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

def send_notification(credentials: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send a notification with formatting
    
    params:
    {
        "title": "Alert!",
        "message": "Something important happened",
        "color": "danger" (good, warning, danger)
    }
    """
    try:
        webhook_url = credentials.get("webhook_url")
        title = params.get("title", "Notification")
        message = params.get("message")
        color = params.get("color", "good")
        
        if not message:
            return {
                "success": False,
                "message": "Missing 'message' parameter"
            }
        
        payload = {
            "attachments": [{
                "color": color,
                "title": title,
                "text": message,
                "footer": "Workflow Automation Platform",
                "ts": int(time.time())
            }]
        }
        
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": "Notification sent!",
                "data": {"title": title}
            }
        else:
            return {
                "success": False,
                "message": f"Failed: {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

def upload_file(credentials: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Upload a file to Slack
    
    params:
    {
        "file_path": "/path/to/file.txt",
        "channels": "#general",
        "title": "File Title"
    }
    
    Note: Requires bot_token in credentials
    """
    try:
        bot_token = credentials.get("bot_token")
        
        if not bot_token:
            return {
                "success": False,
                "message": "bot_token required for file uploads"
            }
        
        file_path = params.get("file_path")
        channels = params.get("channels")
        title = params.get("title", "Uploaded File")
        
        if not file_path:
            return {
                "success": False,
                "message": "Missing 'file_path' parameter"
            }
        
        # This is a placeholder - implement actual file upload
        return {
            "success": True,
            "message": f"Would upload file: {file_path}",
            "data": {"file": file_path, "title": title}
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }
```

### Step 3: Create `__init__.py`

**File: `backend/app/integrations/slack/__init__.py`**

```python
from .tasks import (
    test_connection,
    send_message,
    send_notification,
    upload_file
)

__all__ = [
    "test_connection",
    "send_message", 
    "send_notification",
    "upload_file"
]
```

---

## 🎨 Part 2: Creating Integration Type in UI

Now that you have the backend module, create the Integration Type in the UI.

### Step 1: Open the Application
```
http://localhost:3000
```

### Step 2: Go to "Integration Types" Tab

### Step 3: Click "Create Integration Type"

### Step 4: Fill in the Form

**Name:** (Must match the folder name in backend!)
```
slack
```

**Description:**
```
Slack messaging integration for sending notifications
```

**Parameters:**

Click "Add Parameter" for each credential needed:

**Parameter 1:**
- Name: `webhook_url`
- Type: `password`
- Required: ✓ (checked)
- Description: `Slack Webhook URL (https://hooks.slack.com/services/...)`

**Parameter 2:** (Optional)
- Name: `bot_token`
- Type: `password`
- Required: ✗ (unchecked)
- Description: `Slack Bot Token (for advanced features)`

### Step 5: Click "Create"

✅ The Integration Type is now created!

---

## 🔗 Part 3: Creating an Integration

### Step 1: Go to "Integrations" Tab

### Step 2: Click "Create Integration"

### Step 3: Fill in the Form

**Integration Name:**
```
My Slack Workspace
```

**Integration Type:**
```
Select: slack
```

**Credentials:**

The form will automatically show the parameters you defined!

- **webhook_url:** `https://hooks.slack.com/services/YOUR/WEBHOOK/URL`
- **bot_token:** (optional, leave empty if not using)

### Step 4: Click "Test Connection"

This calls the `test_connection` function in your `slack/tasks.py`

✅ Should show: "Successfully connected to Slack!"

### Step 5: Click "Create"

✅ The Integration is now saved with encrypted credentials!

---

## 🔄 Part 4: Using in Workflows

### Step 1: Go to "Workflows" Tab

### Step 2: Click "Create Workflow"

### Step 3: Add a Node

Click "Add Node"

**Integration:** Select "My Slack Workspace"

**Task Name:** Choose one of the tasks from your `tasks.py`:
- `test_connection`
- `send_message`
- `send_notification`
- `upload_file`

**Parameters:** (JSON format based on the task)

For `send_message`:
```json
{
  "text": "Hello from my workflow!",
  "channel": "#general"
}
```

For `send_notification`:
```json
{
  "title": "Workflow Alert",
  "message": "Your workflow completed successfully!",
  "color": "good"
}
```

### Step 4: Connect Nodes (if multiple)

Drag from one node to another to create connections.

### Step 5: Save the Workflow

### Step 6: Execute!

Click the "Play" button (▶️) to execute the workflow.

---

## 📚 Available Tasks Examples

### GitHub Integration (Multiple Operations)

**File: `backend/app/integrations/github/tasks.py`**

```python
# Task 1: Test connection
def test_connection(credentials, params):
    # Returns user info

# Task 2: Create repository
def create_repo(credentials, params):
    # Creates a new repo

# Task 3: Create issue
def create_issue(credentials, params):
    # Creates an issue

# Task 4: Create pull request (you can add this!)
def create_pull_request(credentials, params):
    # Creates a PR
```

In workflow, you can use:
- Task: `test_connection` with params: `{}`
- Task: `create_repo` with params: `{"repo_name": "my-repo", "private": true}`
- Task: `create_issue` with params: `{"repo": "user/repo", "title": "Bug"}`

---

## 🎯 Adding More Operations to Existing Integration

### Example: Adding "Close Issue" to GitHub

**File: `backend/app/integrations/github/tasks.py`**

Add this function:

```python
def close_issue(credentials: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Close a GitHub issue
    
    params:
    {
        "repo": "owner/repo-name",
        "issue_number": 42
    }
    """
    try:
        token = credentials.get("token")
        repo = params.get("repo")
        issue_number = params.get("issue_number")
        
        if not all([repo, issue_number]):
            return {
                "success": False,
                "message": "Missing required parameters"
            }
        
        response = requests.patch(
            f"https://api.github.com/repos/{repo}/issues/{issue_number}",
            json={"state": "closed"},
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": f"Issue #{issue_number} closed!",
                "data": response.json()
            }
        else:
            return {
                "success": False,
                "message": f"Failed: {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }
```

**Update `__init__.py`:**

```python
from .tasks import (
    test_connection,
    create_repo,
    create_issue,
    close_issue  # Add this!
)

__all__ = [
    "test_connection",
    "create_repo",
    "create_issue",
    "close_issue"  # Add this!
]
```

**Restart backend:**
```bash
docker-compose restart backend
```

**Now you can use it in workflows!**

Task: `close_issue`
Params:
```json
{
  "repo": "username/my-repo",
  "issue_number": 42
}
```

---

## 🔑 Key Points

### 1. **Naming Convention**
- Integration folder name = Integration Type name in UI
- Must be lowercase, no spaces
- Example: `slack`, `jira`, `github`

### 2. **Required Functions**
Every integration MUST have:
```python
def test_connection(credentials, params):
    # Test if credentials work
    return {"success": True/False, "message": "..."}
```

### 3. **Task Functions**
Any other function becomes a usable task:
```python
def task_name(credentials, params):
    # Do something
    return {"success": True/False, "message": "...", "data": {...}}
```

### 4. **Return Format**
Always return this structure:
```python
{
    "success": True/False,
    "message": "Human-readable message",
    "data": {}  # Optional, any additional data
}
```

### 5. **Error Handling**
Always wrap in try-except:
```python
try:
    # Your code
    return {"success": True, "message": "Success!"}
except Exception as e:
    return {"success": False, "message": f"Error: {str(e)}"}
```

---

## 📋 Complete Checklist: Adding New Integration

- [ ] Create folder: `backend/app/integrations/<name>/`
- [ ] Create `tasks.py` with functions
- [ ] Create `__init__.py` with exports
- [ ] Restart backend: `docker-compose restart backend`
- [ ] Create Integration Type in UI (name must match folder)
- [ ] Define all required credentials as parameters
- [ ] Create Integration in UI
- [ ] Test connection
- [ ] Use in workflow with any task function
- [ ] Execute and verify!

---

## 🎓 Advanced Examples

### Database Integration (PostgreSQL)

```python
import psycopg2

def test_connection(credentials, params):
    try:
        conn = psycopg2.connect(
            host=credentials.get("host"),
            user=credentials.get("username"),
            password=credentials.get("password"),
            database=credentials.get("database")
        )
        conn.close()
        return {"success": True, "message": "Connected!"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def execute_query(credentials, params):
    query = params.get("query")
    # Execute and return results
```

### Email Integration (SendGrid)

```python
def send_email(credentials, params):
    api_key = credentials.get("api_key")
    to = params.get("to")
    subject = params.get("subject")
    body = params.get("body")
    
    # Use SendGrid API
    # Return success/failure
```

### AWS S3 Integration

```python
import boto3

def upload_file(credentials, params):
    s3 = boto3.client(
        's3',
        aws_access_key_id=credentials.get("access_key"),
        aws_secret_access_key=credentials.get("secret_key")
    )
    # Upload file
```

---

## 🚀 Next Steps

1. **Create your first custom integration** (try Slack!)
2. **Add more tasks to existing integrations**
3. **Build complex workflows** combining multiple integrations
4. **Share integration templates** with your team

---

## 💡 Pro Tips

- **Test functions individually** before using in workflows
- **Use clear parameter names** and descriptions
- **Add comprehensive error messages**
- **Document expected parameters** in docstrings
- **Return useful data** in the response for debugging
- **Keep credentials secure** - they're encrypted!

---

**You now have the complete knowledge to add any integration! 🎉**
