import requests
from typing import Dict, Any

def test_connection(credentials: Dict[str, Any]) -> Dict[str, Any]:
    """
    Test GitHub connection with provided credentials
    
    Expected credentials:
    {
        "token": "github_pat_xxxx",
        "username": "github-username" (optional)
    }
    """
    try:
        token = credentials.get("token")
        
        if not token:
            return {
                "success": False,
                "message": "Missing required credential: token"
            }
        
        # Test connection by fetching authenticated user info
        response = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            return {
                "success": True,
                "message": f"Connected successfully as {user_data.get('login', 'Unknown')}",
                "data": {
                    "username": user_data.get("login"),
                    "name": user_data.get("name"),
                    "email": user_data.get("email")
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
            "message": "Connection timeout"
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

def create_repo(credentials: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a GitHub repository
    
    params:
    {
        "repo_name": "repository-name",
        "description": "Repository description" (optional),
        "private": false (optional)
    }
    """
    try:
        token = credentials.get("token")
        repo_name = params.get("repo_name")
        description = params.get("description", "")
        is_private = params.get("private", False)
        
        if not repo_name:
            return {
                "success": False,
                "message": "Missing required parameter: repo_name"
            }
        
        payload = {
            "name": repo_name,
            "description": description,
            "private": is_private,
            "auto_init": True
        }
        
        response = requests.post(
            "https://api.github.com/user/repos",
            json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json"
            },
            timeout=10
        )
        
        if response.status_code == 201:
            repo_data = response.json()
            return {
                "success": True,
                "message": f"Repository created successfully: {repo_data.get('full_name')}",
                "data": {
                    "name": repo_data.get("name"),
                    "full_name": repo_data.get("full_name"),
                    "url": repo_data.get("html_url"),
                    "clone_url": repo_data.get("clone_url")
                }
            }
        else:
            return {
                "success": False,
                "message": f"Failed to create repository: {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error creating repository: {str(e)}"
        }

def create_issue(credentials: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a GitHub issue
    
    params:
    {
        "repo": "owner/repo-name",
        "title": "Issue title",
        "body": "Issue body" (optional)
    }
    """
    try:
        token = credentials.get("token")
        repo = params.get("repo")
        title = params.get("title")
        body = params.get("body", "")
        
        if not all([repo, title]):
            return {
                "success": False,
                "message": "Missing required parameters: repo or title"
            }
        
        payload = {
            "title": title,
            "body": body
        }
        
        response = requests.post(
            f"https://api.github.com/repos/{repo}/issues",
            json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json"
            },
            timeout=10
        )
        
        if response.status_code == 201:
            issue_data = response.json()
            return {
                "success": True,
                "message": f"Issue created successfully: #{issue_data.get('number')}",
                "data": {
                    "number": issue_data.get("number"),
                    "url": issue_data.get("html_url"),
                    "state": issue_data.get("state")
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
