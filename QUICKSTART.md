# Quick Start Guide

## Local Development (Fastest Way to Get Started)

### Step 1: Start MariaDB

```bash
# Install MariaDB if not already installed
# Ubuntu/Debian:
sudo apt-get install mariadb-server
sudo systemctl start mariadb

# macOS:
brew install mariadb
brew services start mariadb

# Create the database
mysql -u root -p
CREATE DATABASE workflow_db;
EXIT;
```

### Step 2: Start Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend
uvicorn app.main:app --reload
```

Backend will run at: http://localhost:8000
API Docs: http://localhost:8000/docs

### Step 3: Initialize Sample Integration Types

Open a new terminal:

```bash
cd backend
source venv/bin/activate  # If not already activated
python setup_integration_types.py
```

### Step 4: Start Frontend

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

Frontend will run at: http://localhost:3000

---

## Docker Development (All-in-One)

```bash
# Start everything
docker-compose up --build

# Wait for all services to start...
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

Initialize integration types:

```bash
# In a new terminal
docker-compose exec backend python setup_integration_types.py
```

---

## Your First Workflow

### 1. Create Jira Integration Type (if not using setup script)

Navigate to **Integration Types** → **Create Integration Type**

- **Name**: `jira`
- **Description**: Atlassian Jira integration
- **Parameters**:
  ```
  Name: url | Type: string | Required: ✓ | Description: Jira URL
  Name: email | Type: string | Required: ✓ | Description: Email
  Name: api_token | Type: password | Required: ✓ | Description: API Token
  ```

### 2. Create a Jira Integration

Navigate to **Integrations** → **Create Integration**

- **Name**: My Jira
- **Type**: jira
- **Credentials**:
  - url: `https://your-domain.atlassian.net`
  - email: `your-email@example.com`
  - api_token: `your-api-token`
- Click **Test Connection**
- If successful, click **Create**

### 3. Create GitHub Integration Type

Navigate to **Integration Types** → **Create Integration Type**

- **Name**: `github`
- **Description**: GitHub integration
- **Parameters**:
  ```
  Name: token | Type: password | Required: ✓ | Description: GitHub PAT
  Name: username | Type: string | Required: ✗ | Description: Username
  ```

### 4. Create a GitHub Integration

Navigate to **Integrations** → **Create Integration**

- **Name**: My GitHub
- **Type**: github
- **Credentials**:
  - token: `github_pat_xxxxx`
- Click **Test Connection**
- If successful, click **Create**

### 5. Build Your First Workflow

Navigate to **Workflows** → **Create Workflow**

1. Enter workflow name: "Bug Report Automation"
2. Click **Add Node**:
   - Integration: My Jira (jira)
   - Task: `create_issue`
   - Parameters:
     ```json
     {
       "project": "TEST",
       "summary": "Automated bug report",
       "description": "Created via workflow",
       "issue_type": "Bug"
     }
     ```
   - Click **Add Node**

3. Click **Add Node** again:
   - Integration: My GitHub (github)
   - Task: `create_issue`
   - Parameters:
     ```json
     {
       "repo": "username/repo-name",
       "title": "Bug found",
       "body": "Automated issue creation"
     }
     ```
   - Click **Add Node**

4. Connect the nodes: Drag from the first node to the second
5. Click **Save**

### 6. Execute the Workflow

- Go back to **Workflows** page
- Find your workflow
- Click the **Play** button (▶️)
- Check the execution result!

---

## Available Integration Tasks

### Jira
- `test_connection` - Test connection
- `create_issue` - Create an issue
  - Params: `{"project": "KEY", "summary": "Title", "description": "Details", "issue_type": "Bug"}`

### GitHub
- `test_connection` - Test connection
- `create_repo` - Create repository
  - Params: `{"repo_name": "name", "description": "desc", "private": false}`
- `create_issue` - Create issue
  - Params: `{"repo": "owner/repo", "title": "Title", "body": "Body"}`

### AWS
- `test_connection` - Validate credentials
- `list_s3_buckets` - List buckets (placeholder)

### Azure
- `test_connection` - Validate credentials
- `list_resource_groups` - List resource groups (placeholder)

---

## Troubleshooting

### Backend Error: "ENCRYPTION_KEY environment variable not set"
- The `.env` file should already have a key
- If missing, generate one:
  ```bash
  python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
  ```

### Frontend can't connect to Backend
- Make sure backend is running on port 8000
- Check vite.config.ts proxy settings
- Try accessing http://localhost:8000/docs directly

### Database Connection Failed
- Verify MariaDB is running: `systemctl status mariadb`
- Check credentials in backend/.env
- Try connecting manually: `mysql -u root -p -h localhost workflow_db`

### Docker: Port Already in Use
```bash
# Stop services using the ports
# For port 8000:
lsof -ti:8000 | xargs kill -9

# Or use different ports in docker-compose.yml
```

---

## Next Steps

- Add more integration types
- Create complex workflows with branching
- View execution logs in the database
- Export/Import workflows (coming soon)
- Set up workflow scheduling (future feature)

Happy automating! 🚀
