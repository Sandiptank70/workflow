# Workflow API Trigger - Complete Guide

## 🎯 Overview

Your workflows can now be triggered via API! This allows external systems, webhooks, scheduled jobs, or any HTTP client to execute workflows programmatically.

---

## 📡 API Endpoints

### 1. Execute Workflow (Manual/UI)
```
POST /api/workflows/{workflow_id}/execute
```

### 2. Trigger Workflow (API/External)
```
POST /api/workflows/{workflow_id}/trigger
```

**Note:** Both endpoints work the same way, but `/trigger` is specifically designed for external API calls.

---

## 🚀 Basic Usage

### Simple Trigger (No Parameters)

```bash
curl -X POST http://localhost:8000/api/workflows/1/trigger \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "execution_id": 1,
  "workflow_id": 1,
  "workflow_name": "My Workflow",
  "status": "success",
  "started_at": "2025-10-15T10:30:00",
  "completed_at": "2025-10-15T10:30:03",
  "execution_time_seconds": 3.245,
  "nodes_executed": 3,
  "nodes_total": 3,
  "node_results": [
    {
      "node_id": "node-1",
      "task": "test_connection",
      "integration_id": 1,
      "success": true,
      "message": "Successfully connected to Teams!",
      "data": {...},
      "execution_time_seconds": 0.523,
      "timestamp": "2025-10-15T10:30:00"
    },
    {
      "node_id": "node-2",
      "task": "send_notification",
      "integration_id": 1,
      "success": true,
      "message": "Notification sent successfully!",
      "data": {...},
      "execution_time_seconds": 1.234,
      "timestamp": "2025-10-15T10:30:01"
    },
    {
      "node_id": "node-3",
      "task": "send_simple_message",
      "integration_id": 1,
      "success": true,
      "message": "Message sent!",
      "data": {...},
      "execution_time_seconds": 1.488,
      "timestamp": "2025-10-15T10:30:02"
    }
  ],
  "error_message": null,
  "trigger_source": "api"
}
```

---

## 🎨 Advanced Usage

### Trigger with Runtime Parameters

You can pass parameters that will be merged with or override node parameters:

```bash
curl -X POST http://localhost:8000/api/workflows/1/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "runtime_params": {
      "text": "Deployment completed!",
      "status": "success",
      "user": "john@example.com"
    },
    "trigger_source": "github_webhook",
    "trigger_metadata": {
      "commit": "abc123def",
      "branch": "main",
      "author": "johndoe"
    }
  }'
```

**Request Body Schema:**
```json
{
  "runtime_params": {
    // Optional: Parameters to pass to ALL nodes
    // These will be merged with node-specific parameters
    "key1": "value1",
    "key2": "value2"
  },
  "trigger_source": "api",  // Optional: Source identifier
  "trigger_metadata": {
    // Optional: Additional metadata about the trigger
    "any_key": "any_value"
  }
}
```

---

## 📊 Response Structure

### Successful Execution

```json
{
  "execution_id": 1,                    // Unique execution ID
  "workflow_id": 1,                     // Workflow that was executed
  "workflow_name": "My Workflow",       // Name of the workflow
  "status": "success",                  // success | failed | running
  "started_at": "2025-10-15T10:30:00", // ISO timestamp
  "completed_at": "2025-10-15T10:30:03", // ISO timestamp
  "execution_time_seconds": 3.245,     // Total execution time
  "nodes_executed": 3,                 // Number of nodes executed
  "nodes_total": 3,                    // Total nodes in workflow
  "node_results": [                    // Detailed results for each node
    {
      "node_id": "node-1",
      "task": "send_notification",
      "integration_id": 1,
      "success": true,
      "message": "Notification sent!",
      "data": {                        // Task-specific response data
        "title": "Deployment",
        "status": "success"
      },
      "execution_time_seconds": 1.234,
      "timestamp": "2025-10-15T10:30:00"
    }
  ],
  "error_message": null,
  "trigger_source": "api"
}
```

### Failed Execution

```json
{
  "execution_id": 2,
  "workflow_id": 1,
  "workflow_name": "My Workflow",
  "status": "failed",
  "started_at": "2025-10-15T10:31:00",
  "completed_at": "2025-10-15T10:31:01",
  "execution_time_seconds": 1.123,
  "nodes_executed": 1,
  "nodes_total": 3,
  "node_results": [
    {
      "node_id": "node-1",
      "task": "send_notification",
      "integration_id": 1,
      "success": false,
      "message": "Connection timeout",
      "data": {},
      "execution_time_seconds": 1.123,
      "timestamp": "2025-10-15T10:31:00"
    }
  ],
  "error_message": "Node node-1 (send_notification) failed: Connection timeout",
  "trigger_source": "api"
}
```

---

## 💡 Use Cases

### 1. GitHub Webhook Integration

Trigger workflow when code is pushed:

```bash
# GitHub Webhook payload
curl -X POST http://your-server.com/api/workflows/1/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "runtime_params": {
      "text": "New commit pushed to main",
      "commit_message": "'"$COMMIT_MESSAGE"'"
    },
    "trigger_source": "github_webhook",
    "trigger_metadata": {
      "event": "push",
      "repository": "myapp",
      "branch": "main",
      "commit_sha": "'"$COMMIT_SHA"'"
    }
  }'
```

---

### 2. CI/CD Pipeline

Notify Teams after deployment:

```bash
# In your CI/CD script
WORKFLOW_RESULT=$(curl -X POST http://localhost:8000/api/workflows/1/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "runtime_params": {
      "title": "Deployment Complete",
      "message": "Version 2.0 deployed to production",
      "status": "success"
    },
    "trigger_source": "ci_cd_pipeline",
    "trigger_metadata": {
      "pipeline": "deploy-prod",
      "version": "2.0.0",
      "environment": "production"
    }
  }')

echo "Workflow executed: $WORKFLOW_RESULT"
```

---

### 3. Scheduled Cron Job

Daily status report:

```bash
#!/bin/bash
# In crontab: 0 9 * * * /path/to/daily-report.sh

curl -X POST http://localhost:8000/api/workflows/2/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "runtime_params": {
      "title": "Daily Status Report",
      "message": "System health check completed"
    },
    "trigger_source": "cron_job",
    "trigger_metadata": {
      "schedule": "daily_9am",
      "date": "'"$(date +%Y-%m-%d)"'"
    }
  }'
```

---

### 4. Monitoring Alert

Trigger on system alert:

```bash
# When CPU > 80%
curl -X POST http://localhost:8000/api/workflows/3/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "runtime_params": {
      "title": "High CPU Usage",
      "message": "CPU usage is at 85%",
      "severity": "high"
    },
    "trigger_source": "monitoring_system",
    "trigger_metadata": {
      "server": "prod-web-01",
      "metric": "cpu_usage",
      "value": "85%",
      "threshold": "80%"
    }
  }'
```

---

### 5. API Gateway / Microservice

From your application:

```python
import requests

def trigger_notification_workflow(user_action):
    response = requests.post(
        "http://localhost:8000/api/workflows/1/trigger",
        json={
            "runtime_params": {
                "text": f"User {user_action['user']} performed {user_action['action']}",
                "status": "info"
            },
            "trigger_source": "api_gateway",
            "trigger_metadata": {
                "user_id": user_action['user_id'],
                "action": user_action['action'],
                "timestamp": user_action['timestamp']
            }
        }
    )
    return response.json()
```

```javascript
// JavaScript/Node.js
async function triggerWorkflow(workflowId, data) {
  const response = await fetch(`http://localhost:8000/api/workflows/${workflowId}/trigger`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      runtime_params: data,
      trigger_source: 'nodejs_app',
      trigger_metadata: {
        app: 'my-app',
        version: '1.0.0'
      }
    })
  });
  
  return await response.json();
}

// Usage
const result = await triggerWorkflow(1, {
  text: 'Order #12345 completed',
  status: 'success'
});

console.log('Execution ID:', result.execution_id);
```

---

## 🔐 Security Considerations

### Add Authentication (Recommended)

Currently, the API is open. For production, add authentication:

```python
# backend/app/api/workflows.py
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "your-secret-api-key":
        raise HTTPException(status_code=401, detail="Invalid API key")

@router.post("/{workflow_id}/trigger")
def trigger_workflow_via_api(
    workflow_id: int,
    request: Optional[WorkflowExecuteRequest] = None,
    api_key: str = Depends(verify_api_key),  # Add this
    db: Session = Depends(get_db)
):
    # ... rest of code
```

Then use it:
```bash
curl -X POST http://localhost:8000/api/workflows/1/trigger \
  -H "X-API-Key: your-secret-api-key" \
  -H "Content-Type: application/json"
```

---

## 📈 Monitoring Executions

### Get Execution History

```bash
# Get all executions for a workflow
curl http://localhost:8000/api/workflows/1/executions
```

**Response:**
```json
[
  {
    "id": 3,
    "workflow_id": 1,
    "status": "success",
    "started_at": "2025-10-15T10:35:00",
    "completed_at": "2025-10-15T10:35:02",
    "execution_data": {...},
    "error_message": null
  },
  {
    "id": 2,
    "workflow_id": 1,
    "status": "failed",
    "started_at": "2025-10-15T10:31:00",
    "completed_at": "2025-10-15T10:31:01",
    "execution_data": {...},
    "error_message": "Connection timeout"
  }
]
```

---

## 🎯 Best Practices

### 1. Always Check Response Status
```bash
RESPONSE=$(curl -s -X POST http://localhost:8000/api/workflows/1/trigger \
  -H "Content-Type: application/json")

STATUS=$(echo $RESPONSE | jq -r '.status')

if [ "$STATUS" == "success" ]; then
  echo "Workflow executed successfully!"
else
  ERROR=$(echo $RESPONSE | jq -r '.error_message')
  echo "Workflow failed: $ERROR"
  exit 1
fi
```

### 2. Use Meaningful Trigger Sources
```json
{
  "trigger_source": "github_webhook",  // ✅ Good
  "trigger_source": "webhook"          // ❌ Too vague
}
```

### 3. Include Useful Metadata
```json
{
  "trigger_metadata": {
    "source_system": "monitoring",
    "alert_id": "12345",
    "severity": "high",
    "server": "prod-web-01"
  }
}
```

### 4. Handle Errors Gracefully
```python
try:
    response = requests.post(url, json=data, timeout=30)
    response.raise_for_status()
    result = response.json()
    
    if result['status'] == 'failed':
        logger.error(f"Workflow failed: {result['error_message']}")
except requests.exceptions.RequestException as e:
    logger.error(f"API request failed: {e}")
```

---

## 🧪 Testing

### Test with curl
```bash
# Test basic trigger
curl -X POST http://localhost:8000/api/workflows/1/trigger

# Test with parameters
curl -X POST http://localhost:8000/api/workflows/1/trigger \
  -H "Content-Type: application/json" \
  -d '{"runtime_params": {"text": "Test message"}}'

# Test error handling (invalid workflow ID)
curl -X POST http://localhost:8000/api/workflows/999/trigger
```

### Test with Postman
1. Create new POST request
2. URL: `http://localhost:8000/api/workflows/1/trigger`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
   ```json
   {
     "runtime_params": {
       "text": "Test from Postman"
     }
   }
   ```
5. Send

---

## 📚 Examples by Language

### Python
```python
import requests

def trigger_workflow(workflow_id, params=None):
    url = f"http://localhost:8000/api/workflows/{workflow_id}/trigger"
    payload = {
        "runtime_params": params or {},
        "trigger_source": "python_script"
    }
    response = requests.post(url, json=payload)
    return response.json()

# Usage
result = trigger_workflow(1, {"text": "Hello from Python!"})
print(f"Status: {result['status']}")
```

### JavaScript
```javascript
async function triggerWorkflow(workflowId, params = {}) {
  const response = await fetch(`http://localhost:8000/api/workflows/${workflowId}/trigger`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      runtime_params: params,
      trigger_source: 'javascript'
    })
  });
  return await response.json();
}

// Usage
const result = await triggerWorkflow(1, {text: 'Hello from JS!'});
console.log(`Status: ${result.status}`);
```

### PHP
```php
<?php
function triggerWorkflow($workflowId, $params = []) {
    $url = "http://localhost:8000/api/workflows/$workflowId/trigger";
    $data = [
        'runtime_params' => $params,
        'trigger_source' => 'php_script'
    ];
    
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    
    $response = curl_exec($ch);
    curl_close($ch);
    
    return json_decode($response, true);
}

// Usage
$result = triggerWorkflow(1, ['text' => 'Hello from PHP!']);
echo "Status: " . $result['status'];
?>
```

---

## ✅ Quick Reference

| Feature | Endpoint |
|---------|----------|
| Execute workflow | `POST /api/workflows/{id}/execute` |
| Trigger via API | `POST /api/workflows/{id}/trigger` |
| View executions | `GET /api/workflows/{id}/executions` |
| Get workflow | `GET /api/workflows/{id}` |

**Key Parameters:**
- `runtime_params` - Override/merge with node parameters
- `trigger_source` - Identify the trigger source
- `trigger_metadata` - Additional context

**Response Fields:**
- `status` - success | failed | running
- `node_results` - Detailed results for each node
- `execution_time_seconds` - Total execution time
- `error_message` - Error details if failed

---

**You can now trigger workflows from anywhere!** 🚀🎉
