#!/usr/bin/env python3
"""
Script to initialize sample integration types
Run this after starting the backend for the first time
"""

import requests
import sys

API_BASE_URL = "http://localhost:8000/api"

SAMPLE_INTEGRATION_TYPES = [
    {
        "name": "jira",
        "description": "Atlassian Jira project management integration",
        "parameters": [
            {
                "name": "url",
                "type": "string",
                "required": True,
                "description": "Jira instance URL (e.g., https://your-domain.atlassian.net)"
            },
            {
                "name": "email",
                "type": "string",
                "required": True,
                "description": "Your Jira email address"
            },
            {
                "name": "api_token",
                "type": "password",
                "required": True,
                "description": "Jira API token (generate from account settings)"
            }
        ]
    },
    {
        "name": "github",
        "description": "GitHub code repository integration",
        "parameters": [
            {
                "name": "token",
                "type": "password",
                "required": True,
                "description": "GitHub Personal Access Token"
            },
            {
                "name": "username",
                "type": "string",
                "required": False,
                "description": "GitHub username (optional)"
            }
        ]
    },
    {
        "name": "aws",
        "description": "Amazon Web Services integration",
        "parameters": [
            {
                "name": "access_key_id",
                "type": "string",
                "required": True,
                "description": "AWS Access Key ID"
            },
            {
                "name": "secret_access_key",
                "type": "password",
                "required": True,
                "description": "AWS Secret Access Key"
            },
            {
                "name": "region",
                "type": "string",
                "required": True,
                "description": "AWS Region (e.g., us-east-1)"
            }
        ]
    },
    {
        "name": "azure",
        "description": "Microsoft Azure cloud integration",
        "parameters": [
            {
                "name": "tenant_id",
                "type": "string",
                "required": True,
                "description": "Azure Tenant ID"
            },
            {
                "name": "client_id",
                "type": "string",
                "required": True,
                "description": "Azure Client ID"
            },
            {
                "name": "client_secret",
                "type": "password",
                "required": True,
                "description": "Azure Client Secret"
            }
        ]
    }
]

def create_integration_types():
    """Create sample integration types"""
    print("Creating sample integration types...")
    
    for integration_type in SAMPLE_INTEGRATION_TYPES:
        try:
            response = requests.post(
                f"{API_BASE_URL}/integration-types",
                json=integration_type
            )
            
            if response.status_code == 200:
                print(f"✓ Created integration type: {integration_type['name']}")
            elif response.status_code == 400 and "already exists" in response.text:
                print(f"- Integration type already exists: {integration_type['name']}")
            else:
                print(f"✗ Failed to create {integration_type['name']}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"✗ Error: Cannot connect to API at {API_BASE_URL}")
            print("  Make sure the backend is running (uvicorn app.main:app)")
            sys.exit(1)
        except Exception as e:
            print(f"✗ Error creating {integration_type['name']}: {str(e)}")

def main():
    print("=" * 60)
    print("Workflow Automation Platform - Setup Script")
    print("=" * 60)
    print()
    
    create_integration_types()
    
    print()
    print("=" * 60)
    print("Setup complete!")
    print()
    print("Next steps:")
    print("1. Navigate to http://localhost:3000")
    print("2. Go to 'Integrations' tab")
    print("3. Create your first integration")
    print("4. Build and execute workflows!")
    print("=" * 60)

if __name__ == "__main__":
    main()
