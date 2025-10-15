# Workflow Automation Platform

A modular workflow automation platform that allows users to create integration types, add integrations, build workflows visually using React Flow, and execute workflows step-by-step.

## Features

- **Integration Types Management**: Define templates for Jira, GitHub, AWS, Azure, and more
- **Integrations**: Create integrations with encrypted credential storage
- **Visual Workflow Builder**: Drag-and-drop workflow creation using React Flow
- **Workflow Execution**: Execute workflows step-by-step with detailed logging
- **Secure**: All credentials are encrypted using Fernet encryption

## Tech Stack

### Frontend
- React 18 with TypeScript
- React Flow for visual workflow builder
- TailwindCSS for styling
- Axios for API calls
- React Router for navigation

### Backend
- FastAPI (Python)
- SQLAlchemy with MariaDB
- Cryptography (Fernet) for encryption
- Integration scripts for Jira, GitHub, AWS, Azure

### Database
- MariaDB

### Deployment
- Docker & Docker Compose

## Project Structure

```
workflow-automation-platform/
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Main application pages
│   │   ├── services/        # API service layer
│   │   ├── types/           # TypeScript type definitions
│   │   ├── utils/           # Utility functions
│   │   ├── App.tsx          # Main app component
│   │   └── main.tsx         # Entry point
│   ├── package.json
│   ├── Dockerfile
│   └── vite.config.ts
├── backend/
│   ├── app/
│   │   ├── api/             # API routes
│   │   ├── models/          # Database models
│   │   ├── services/        # Business logic
│   │   ├── integrations/    # Integration scripts
│   │   │   ├── jira/
│   │   │   ├── github/
│   │   │   ├── aws/
│   │   │   └── azure/
│   │   ├── utils/           # Utilities (encryption, etc.)
│   │   ├── database.py      # Database configuration
│   │   └── main.py          # FastAPI application
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
└── docker-compose.yml
```

## Getting Started

### Prerequisites

#### For Local Development:
- Python 3.11+
- Node.js 18+
- MariaDB 10.6+

#### For Docker:
- Docker
- Docker Compose

---

## Phase 1: Local Setup

### 1. Database Setup

Install and start MariaDB:

```bash
# On Ubuntu/Debian
sudo apt-get install mariadb-server
sudo systemctl start mariadb

# On macOS
brew install mariadb
brew services start mariadb

# Create database
mysql -u root -p
CREATE DATABASE workflow_db;
EXIT;
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Edit .env file and update database credentials if needed

# Generate encryption key (optional - already provided)
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Run the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 4. Testing the Application

1. **Create Integration Types**:
   - Navigate to "Integration Types"
   - Click "Create Integration Type"
   - Example for Jira:
     - Name: `jira`
     - Description: Atlassian Jira integration
     - Parameters:
       ```json
       [
         {"name": "url", "type": "string", "required": true, "description": "Jira URL"},
         {"name": "email", "type": "string", "required": true, "description": "Email"},
         {"name": "api_token", "type": "password", "required": true, "description": "API Token"}
       ]
       ```

2. **Create Integrations**:
   - Navigate to "Integrations"
   - Click "Create Integration"
   - Select integration type
   - Fill in credentials
   - Test connection before creating

3. **Build Workflows**:
   - Navigate to "Workflows"
   - Click "Create Workflow"
   - Add nodes using the "Add Node" button
   - Connect nodes by dragging from one to another
   - Configure each node with integration and task
   - Save the workflow

4. **Execute Workflows**:
   - Click the Play button on any workflow card
   - View execution logs in the database

---

## Phase 2: Docker Deployment

### 1. Build and Start All Services

```bash
# From the project root directory
docker-compose up --build
```

This will start:
- Frontend on `http://localhost:3000`
- Backend on `http://localhost:8000`
- MariaDB on `localhost:3306`

### 2. Stop Services

```bash
docker-compose down
```

### 3. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

---

## API Endpoints

### Integration Types
- `POST /api/integration-types` - Create integration type
- `GET /api/integration-types` - List all integration types
- `GET /api/integration-types/{id}` - Get specific integration type

### Integrations
- `POST /api/integrations/test` - Test integration connection
- `POST /api/integrations` - Create integration
- `GET /api/integrations` - List all integrations
- `GET /api/integrations/{id}` - Get specific integration
- `DELETE /api/integrations/{id}` - Delete integration

### Workflows
- `POST /api/workflows` - Create workflow
- `GET /api/workflows` - List all workflows
- `GET /api/workflows/{id}` - Get specific workflow
- `PUT /api/workflows/{id}` - Update workflow
- `DELETE /api/workflows/{id}` - Delete workflow
- `POST /api/workflows/{id}/execute` - Execute workflow
- `GET /api/workflows/{id}/executions` - Get execution logs

---

## Integration Examples

### Jira Integration Type

```json
{
  "name": "jira",
  "description": "Atlassian Jira integration",
  "parameters": [
    {"name": "url", "type": "string", "required": true, "description": "Jira instance URL"},
    {"name": "email", "type": "string", "required": true, "description": "User email"},
    {"name": "api_token", "type": "password", "required": true, "description": "API token"}
  ]
}
```

**Available Tasks:**
- `test_connection` - Test Jira connection
- `create_issue` - Create a new issue
  - Parameters: `{"project": "KEY", "summary": "Issue title", "description": "Details", "issue_type": "Task"}`

### GitHub Integration Type

```json
{
  "name": "github",
  "description": "GitHub integration",
  "parameters": [
    {"name": "token", "type": "password", "required": true, "description": "GitHub Personal Access Token"},
    {"name": "username", "type": "string", "required": false, "description": "GitHub username"}
  ]
}
```

**Available Tasks:**
- `test_connection` - Test GitHub connection
- `create_repo` - Create a new repository
  - Parameters: `{"repo_name": "my-repo", "description": "Repo description", "private": false}`
- `create_issue` - Create an issue
  - Parameters: `{"repo": "owner/repo-name", "title": "Issue title", "body": "Issue body"}`

---

## Sample Workflow

```json
{
  "name": "Bug Report Workflow",
  "description": "Create Jira issue and GitHub repo for new bugs",
  "nodes": [
    {
      "id": "1",
      "type": "integration",
      "integration_id": 1,
      "task": "create_issue",
      "params": {
        "project": "BUG",
        "summary": "New bug found in production",
        "description": "Critical bug that needs immediate attention",
        "issue_type": "Bug"
      }
    },
    {
      "id": "2",
      "type": "integration",
      "integration_id": 2,
      "task": "create_repo",
      "params": {
        "repo_name": "bug-fix-repo",
        "description": "Repository for bug fixes",
        "private": true
      }
    }
  ],
  "connections": [
    {"from": "1", "to": "2"}
  ]
}
```

---

## Security Notes

- All credentials are encrypted using Fernet encryption before storage
- The encryption key should be kept secure and rotated periodically
- Use environment variables for sensitive configuration
- In production, use HTTPS and proper authentication/authorization

---

## Troubleshooting

### Backend won't start
- Check if MariaDB is running: `systemctl status mariadb`
- Verify database credentials in `.env`
- Check if port 8000 is available: `lsof -i :8000`

### Frontend won't start
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check if port 3000 is available: `lsof -i :3000`

### Database connection errors
- Verify MariaDB is accessible: `mysql -u root -p -h localhost`
- Check database exists: `SHOW DATABASES;`
- Verify user permissions

### Docker issues
- Clean up: `docker-compose down -v`
- Rebuild: `docker-compose build --no-cache`
- Check logs: `docker-compose logs`

---

## Future Enhancements

- [ ] Add user authentication and authorization
- [ ] Implement Celery for async workflow execution
- [ ] Add more integration types (Slack, AWS Lambda, etc.)
- [ ] Workflow scheduling and triggers
- [ ] Real-time execution monitoring
- [ ] Workflow versioning
- [ ] Export/Import workflows
- [ ] Workflow templates marketplace

---

## License

MIT License

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
