import requests
from typing import Dict, Any

def test_connection(credentials: Dict[str, Any]) -> Dict[str, Any]:
    """
    Test Jira connection with provided credentials
    
    Expected credentials:
    {
        "url": "https://your-domain.atlassian.net",
        "email": "user@example.com",
        "api_token": "your-api-token"
    }
    """
    try:
        url = credentials.get("url", "").rstrip("/")
        email = credentials.get("email")
        api_token = credentials.get("api_token")
        
        if not all([url, email, api_token]):
            return {
                "success": False,
                "message": "Missing required credentials: url, email, or api_token"
            }
        
        # Test connection by fetching user info
        response = requests.get(
            f"{url}/rest/api/3/myself",
            auth=(email, api_token),
            headers={"Accept": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            return {
                "success": True,
                "message": f"Connected successfully as {user_data.get('displayName', 'Unknown')}",
                "data": {
                    "account_id": user_data.get("accountId"),
                    "display_name": user_data.get("displayName")
                }
            }
        else:
            return {
                "success": False,
                "message": f"Connection failed with status {response.status_code}: {response.text}"
            }
            
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": "Connection timeout - please check the URL"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Connection error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Unexpected error: {str(e)}"
        }

def create_issue(credentials: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a Jira issue
    
    params:
    {
        "project": "PROJECT_KEY",
        "summary": "Issue summary",
        "description": "Issue description",
        "issue_type": "Bug" (optional, defaults to "Task")
    }
    """
    try:
        url = credentials.get("url", "").rstrip("/")
        email = credentials.get("email")
        api_token = credentials.get("api_token")
        
        project = params.get("project")
        summary = params.get("summary")
        description = params.get("description", "")
        issue_type = params.get("issue_type", "Task")
        
        if not all([project, summary]):
            return {
                "success": False,
                "message": "Missing required parameters: project or summary"
            }
        
        payload = {
            "fields": {
                "project": {"key": project},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {"name": issue_type}
            }
        }
        
        response = requests.post(
            f"{url}/rest/api/3/issue",
            json=payload,
            auth=(email, api_token),
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 201:
            issue_data = response.json()
            return {
                "success": True,
                "message": f"Issue created successfully: {issue_data.get('key')}",
                "data": {
                    "key": issue_data.get("key"),
                    "id": issue_data.get("id"),
                    "self": issue_data.get("self")
                }
            }
        else:
            return {
                "success": False,
                "message": f"Failed to create issue: {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error creating issue: {str(e)}"
        }
