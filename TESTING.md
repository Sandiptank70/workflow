# Testing & Verification Guide

This guide will help you verify that all components of the Workflow Automation Platform are working correctly.

## Pre-Testing Setup

### 1. Ensure Services are Running

**Local:**
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Initialize data
cd backend
python setup_integration_types.py
```

**Docker:**
```bash
docker-compose up
docker-compose exec backend python setup_integration_types.py
```

### 2. Access Points
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Test Suite

### Test 1: Backend Health Check

```bash
# Test backend is running
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy"}
```

✅ **Pass Criteria**: Returns 200 with `{"status":"healthy"}`

### Test 2: Database Connection

```bash
# Check database tables were created
mysql -u root -p workflow_db -e "SHOW TABLES;"

# Expected tables:
# - integration_types
# - integrations
# - workflows
# - execution_logs
```

✅ **Pass Criteria**: All 4 tables exist

### Test 3: Integration Types API

```bash
# List integration types
curl http://localhost:8000/api/integration-types

# Expected: Array of integration types (jira, github, aws, azure)
```

**Via UI:**
1. Navigate to http://localhost:3000
2. Click "Integration Types" tab
3. Verify 4 cards displayed (if setup script was run)

✅ **Pass Criteria**: Can see and create integration types

### Test 4: Create Integration Type

**Via API:**
```bash
curl -X POST http://localhost:8000/api/integration-types \
  -H "Content-Type: application/json" \
  -d '{
    "name": "slack",
    "description": "Slack messaging integration",
    "parameters": [
      {
        "name": "webhook_url",
        "type": "password",
        "required": true,
        "description": "Slack Webhook URL"
      }
    ]
  }'
```

**Via UI:**
1. Click "Create Integration Type"
2. Fill in name: "slack"
3. Add parameter: webhook_url (password, required)
4. Click "Create"

✅ **Pass Criteria**: New integration type appears in list

### Test 5: Encryption Service

```bash
cd backend
python -c "
from app.utils.encryption import encryption_service
encrypted = encryption_service.encrypt('test_secret')
print(f'Encrypted: {encrypted}')
decrypted = encryption_service.decrypt(encrypted)
print(f'Decrypted: {decrypted}')
assert decrypted == 'test_secret', 'Encryption/Decryption failed!'
print('✓ Encryption working correctly')
"
```

✅ **Pass Criteria**: Successfully encrypts and decrypts

### Test 6: GitHub Integration Test

**Prerequisites:**
- GitHub Personal Access Token
- Create at: https://github.com/settings/tokens

**Via UI:**
1. Go to "Integrations" tab
2. Click "Create Integration"
3. Name: "Test GitHub"
4. Type: github
5. Token: (your GitHub PAT)
6. Click "Test Connection"

✅ **Pass Criteria**: Shows green checkmark with "Connected successfully as [username]"

### Test 7: Jira Integration Test

**Prerequisites:**
- Jira instance URL
- Jira API token
- Generate at: https://id.atlassian.com/manage-profile/security/api-tokens

**Via UI:**
1. Go to "Integrations" tab
2. Click "Create Integration"
3. Name: "Test Jira"
4. Type: jira
5. Fill credentials
6. Click "Test Connection"

✅ **Pass Criteria**: Shows green checkmark with connection success message

### Test 8: Create Integration (Full Flow)

1. Test connection (should succeed)
2. Click "Create" button
3. Should see integration in the list
4. Verify in database:
   ```bash
   mysql -u root -p workflow_db -e "SELECT id, name, is_active FROM integrations;"
   ```

✅ **Pass Criteria**: Integration saved with encrypted credentials

### Test 9: Workflow Builder UI

1. Navigate to "Workflows" tab
2. Click "Create Workflow"
3. Verify React Flow canvas appears
4. Name: "Test Workflow"
5. Click "Add Node"

✅ **Pass Criteria**: Workflow builder opens with empty canvas

### Test 10: Add Workflow Node

1. In workflow builder, click "Add Node"
2. Select an integration
3. Enter task name: "test_connection"
4. Enter params: `{}`
5. Click "Add Node"
6. Verify node appears on canvas

✅ **Pass Criteria**: Node appears with correct label

### Test 11: Connect Workflow Nodes

1. Add two nodes
2. Drag from first node's edge to second node
3. Verify connection line appears
4. Click "Save"

✅ **Pass Criteria**: Connection created and workflow saved

### Test 12: Execute Workflow

**Simple Test Workflow:**
```json
{
  "name": "GitHub Connection Test",
  "nodes": [
    {
      "id": "1",
      "integration_id": <your-github-integration-id>,
      "task": "test_connection",
      "params": {}
    }
  ],
  "connections": []
}
```

1. Create workflow with GitHub test_connection
2. Save workflow
3. Click "Play" button (▶️)
4. Check alert for execution result

**Verify in Database:**
```bash
mysql -u root -p workflow_db -e "SELECT * FROM execution_logs ORDER BY started_at DESC LIMIT 1\G"
```

✅ **Pass Criteria**: 
- Alert shows "Workflow executed successfully"
- Execution log shows status='success'

### Test 13: Failed Workflow Execution

1. Create workflow with invalid integration ID
2. Execute workflow
3. Verify error handling

✅ **Pass Criteria**: Graceful error message, execution_log shows 'failed' status

### Test 14: Complex Workflow

**Two-Step Workflow:**

1. Create workflow: "GitHub to Jira"
2. Node 1: GitHub `test_connection`
3. Node 2: Jira `test_connection`
4. Connect: Node 1 → Node 2
5. Execute workflow

✅ **Pass Criteria**: Both nodes execute in correct order

### Test 15: Workflow Update

1. Open existing workflow
2. Add new node
3. Save
4. Verify updated workflow has new node

✅ **Pass Criteria**: Workflow saves with changes

### Test 16: Delete Operations

**Delete Integration:**
1. Click trash icon on integration
2. Confirm deletion
3. Verify removed from list

**Delete Workflow:**
1. Click trash icon on workflow
2. Confirm deletion
3. Verify removed from list

✅ **Pass Criteria**: Items deleted successfully

---

## Integration-Specific Tests

### GitHub Integration Tests

```bash
# Test via API
curl -X POST http://localhost:8000/api/integrations/test \
  -H "Content-Type: application/json" \
  -d '{
    "integration_type_id": 2,
    "credentials": {
      "token": "github_pat_YOUR_TOKEN"
    }
  }'
```

**Available Tasks:**
1. `test_connection` - Should return user info
2. `create_repo` - Test with:
   ```json
   {
     "repo_name": "test-workflow-repo",
     "description": "Created by workflow automation",
     "private": true
   }
   ```
3. `create_issue` - Test with:
   ```json
   {
     "repo": "username/repo-name",
     "title": "Test Issue",
     "body": "Created via workflow"
   }
   ```

### Jira Integration Tests

**Available Tasks:**
1. `test_connection` - Should return account info
2. `create_issue` - Test with:
   ```json
   {
     "project": "TEST",
     "summary": "Workflow Test Issue",
     "description": "Created automatically",
     "issue_type": "Task"
   }
   ```

---

## Performance Tests

### Test 17: Multiple Nodes

Create workflow with 5+ nodes and verify execution time is reasonable.

✅ **Pass Criteria**: Completes within 30 seconds

### Test 18: Concurrent Executions

Execute multiple workflows simultaneously.

✅ **Pass Criteria**: All complete successfully

---

## Security Tests

### Test 19: Credential Encryption

```bash
# Check database - credentials should be encrypted
mysql -u root -p workflow_db -e "SELECT credentials FROM integrations LIMIT 1;"
```

✅ **Pass Criteria**: Credentials are base64 encoded gibberish, not readable

### Test 20: API Validation

```bash
# Try to create integration without required fields
curl -X POST http://localhost:8000/api/integrations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invalid"
  }'
```

✅ **Pass Criteria**: Returns 422 validation error

---

## Docker Tests

### Test 21: Docker Build

```bash
docker-compose build
```

✅ **Pass Criteria**: All services build without errors

### Test 22: Docker Startup

```bash
docker-compose up -d
docker-compose ps
```

✅ **Pass Criteria**: All 3 services (frontend, backend, db) running

### Test 23: Docker Health

```bash
# Wait for services to be ready
sleep 10

# Test backend
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000
```

✅ **Pass Criteria**: Both return successful responses

---

## Troubleshooting Common Test Failures

### Backend Won't Start
```bash
# Check if port is in use
lsof -i :8000

# Check database connection
mysql -u root -p -e "SELECT 1;"

# Check encryption key
grep ENCRYPTION_KEY backend/.env
```

### Frontend Won't Start
```bash
# Clear node_modules
rm -rf frontend/node_modules
npm install

# Check port
lsof -i :3000
```

### Integration Test Fails
- Verify credentials are correct
- Check API token hasn't expired
- Ensure integration module exists in backend/app/integrations/

### Workflow Execution Fails
- Check integration exists
- Verify task name is correct
- Ensure parameters match expected format
- Check execution_logs table for error details

---

## Test Checklist

- [ ] Backend health check passes
- [ ] Database tables created
- [ ] Integration types can be created
- [ ] Integrations can be created and tested
- [ ] Workflows can be built visually
- [ ] Workflows can be saved
- [ ] Workflows can be executed
- [ ] Execution logs are created
- [ ] Credentials are encrypted
- [ ] Error handling works correctly
- [ ] UI is responsive
- [ ] All API endpoints return correct status codes
- [ ] Docker builds successfully
- [ ] Docker Compose starts all services

---

## Success Criteria

✅ **All tests pass** - System is ready for use!

If any tests fail, check:
1. Service logs
2. Database state
3. Configuration files
4. API documentation at /docs

---

## Reporting Issues

If you encounter issues:

1. **Check logs:**
   ```bash
   # Local
   tail -f backend/app.log
   
   # Docker
   docker-compose logs -f backend
   ```

2. **Verify configuration:**
   - backend/.env
   - Database credentials
   - Encryption key

3. **Test individual components:**
   - API endpoints via /docs
   - Database queries
   - Integration modules

---

**Happy Testing!** 🧪
