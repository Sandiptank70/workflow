# Integration Creation Flow - Visual Guide

## 🎯 The Complete Process

```
┌─────────────────────────────────────────────────────────────┐
│  Step 1: CREATE BACKEND INTEGRATION MODULE                  │
│  (Developer writes Python code)                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
    backend/app/integrations/slack/
    ├── __init__.py
    └── tasks.py ─────────────────┐
         │                         │
         ├─ test_connection()      │  All functions become
         ├─ send_message()         │  available tasks!
         ├─ send_notification()    │
         └─ upload_file()          │
                                   │
┌──────────────────────────────────┴──────────────────────────┐
│  Step 2: CREATE INTEGRATION TYPE IN UI                      │
│  (Define what credentials are needed)                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
    UI: Integration Types → Create
    ┌─────────────────────────────────────┐
    │ Name: slack   (must match folder!)  │
    │ Description: Slack integration      │
    │ Parameters:                         │
    │   - webhook_url (password, required)│
    │   - bot_token (password, optional)  │
    └─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: CREATE INTEGRATION INSTANCE                        │
│  (Store actual credentials)                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
    UI: Integrations → Create
    ┌─────────────────────────────────────┐
    │ Name: My Slack Workspace            │
    │ Type: slack                         │
    │ Credentials:                        │
    │   webhook_url: https://hooks...     │
    │   bot_token: xoxb-...               │
    │                                     │
    │ [Test Connection] → ✅ Success!     │
    │ [Create] → Saved! (encrypted)       │
    └─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 4: USE IN WORKFLOW                                    │
│  (Build visual workflow)                                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
    UI: Workflows → Create Workflow
    
    ┌─────────────────┐
    │  Add Node 1     │
    │                 │
    │  Integration:   │
    │  My Slack       │
    │                 │
    │  Task:          │
    │  send_message   │
    │                 │
    │  Params:        │
    │  {              │
    │   "text": "Hi!" │
    │  }              │
    └────────┬────────┘
             │
             ▼ (connect)
    ┌────────┴────────┐
    │  Add Node 2     │
    │                 │
    │  Integration:   │
    │  My Slack       │
    │                 │
    │  Task:          │
    │  send_notification
    │                 │
    │  Params:        │
    │  {              │
    │   "title": "..." │
    │  }              │
    └─────────────────┘
    
    [Save Workflow]
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 5: EXECUTE WORKFLOW                                   │
│  (Run the actual tasks)                                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
    UI: Workflows → Click [▶️ Play]
    
    Backend Execution:
    1. Load workflow definition
    2. Get integration credentials (decrypt)
    3. For each node in order:
       - Import: app.integrations.slack
       - Call: send_message(credentials, params)
       - Get: {"success": True, "message": "..."}
    4. Save execution log
    5. Return result to UI
    
    ✅ Workflow Executed Successfully!
```

---

## 🔄 How Multiple Operations Work

```
Backend File: tasks.py
┌────────────────────────────────────────┐
│  def test_connection(creds, params):   │ ─┐
│      # Check if creds work             │  │
│      return {...}                      │  │
│                                        │  │
│  def operation_1(creds, params):       │  │
│      # Do something                    │  │  All these become
│      return {...}                      │  ├─ available tasks
│                                        │  │  in the UI!
│  def operation_2(creds, params):       │  │
│      # Do something else               │  │
│      return {...}                      │  │
│                                        │  │
│  def operation_3(creds, params):       │  │
│      # Yet another operation           │  │
│      return {...}                      │ ─┘
└────────────────────────────────────────┘
                │
                ▼
    In Workflow Node, you choose:
    
    Task: operation_1  ─┐
    Task: operation_2  ─┼─ Any function from tasks.py
    Task: operation_3  ─┘
    Task: test_connection
```

---

## 📦 Real Example: GitHub Integration

```
Backend Structure:
backend/app/integrations/github/
├── __init__.py
└── tasks.py
    ├── test_connection()      → Task: "test_connection"
    ├── create_repo()          → Task: "create_repo"
    ├── create_issue()         → Task: "create_issue"
    └── (add more functions)   → (more tasks)

Integration Type in UI:
┌──────────────────────────┐
│ Name: github             │
│ Parameters:              │
│   - token (password)     │
│   - username (text)      │
└──────────────────────────┘

Integration Instance:
┌──────────────────────────┐
│ Name: My GitHub          │
│ Type: github             │
│ token: ghp_xxxxx         │
│ username: myusername     │
└──────────────────────────┘

Workflow Usage:
Node 1: test_connection    → {} (no params needed)
Node 2: create_repo        → {"repo_name": "test", "private": true}
Node 3: create_issue       → {"repo": "user/test", "title": "Bug"}
```

---

## 🎨 Credentials Flow

```
UI Form                    Backend Storage         Workflow Execution
┌──────────────┐          ┌──────────────┐        ┌──────────────┐
│ webhook_url: │          │ credentials: │        │ Decrypt      │
│ https://...  │          │ ENCRYPTED!   │        │ credentials  │
│              │  Save    │ ZkFBQUFB...  │ Load   │              │
│ bot_token:   │  ────▶   │ encrypted    │ ────▶  │ Use in API   │
│ xoxb-...     │ Encrypt  │ blob         │ Decrypt│ calls        │
└──────────────┘          └──────────────┘        └──────────────┘
```

---

## 🔀 Task Parameter Examples

### Simple Task (No Parameters)
```python
def test_connection(credentials, params):
    # params = {} (empty)
    return {"success": True, "message": "Connected!"}
```

Workflow Usage:
```json
{
  "task": "test_connection",
  "params": {}
}
```

### Task with Parameters
```python
def send_message(credentials, params):
    text = params.get("text")
    channel = params.get("channel")
    # Use text and channel
    return {"success": True, "message": "Sent!"}
```

Workflow Usage:
```json
{
  "task": "send_message",
  "params": {
    "text": "Hello!",
    "channel": "#general"
  }
}
```

### Task with Complex Parameters
```python
def create_issue(credentials, params):
    repo = params.get("repo")
    title = params.get("title")
    labels = params.get("labels", [])
    assignees = params.get("assignees", [])
    # Process all params
    return {"success": True, "message": "Issue created!"}
```

Workflow Usage:
```json
{
  "task": "create_issue",
  "params": {
    "repo": "user/repo",
    "title": "Bug report",
    "labels": ["bug", "high-priority"],
    "assignees": ["developer1", "developer2"]
  }
}
```

---

## 🎯 Quick Reference

### Adding New Operation to Existing Integration

1. **Edit** `backend/app/integrations/<name>/tasks.py`
2. **Add** new function:
   ```python
   def my_new_operation(credentials, params):
       # Your code here
       return {"success": True, "message": "Done!"}
   ```
3. **Update** `__init__.py`:
   ```python
   from .tasks import my_new_operation
   __all__ = [..., "my_new_operation"]
   ```
4. **Restart** backend:
   ```bash
   docker-compose restart backend
   ```
5. **Use** in workflow:
   - Task: `my_new_operation`
   - Params: `{...}`

### Creating Completely New Integration

1. **Create** folder: `backend/app/integrations/myintegration/`
2. **Create** `tasks.py` with functions
3. **Create** `__init__.py` with exports
4. **Restart** backend
5. **Create Integration Type** in UI (name = folder name)
6. **Create Integration** instance
7. **Test** connection
8. **Use** in workflows!

---

**Everything is connected! Backend code → UI → Workflows** 🚀
