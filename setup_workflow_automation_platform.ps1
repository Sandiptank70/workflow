# File: setup_workflow_automation_platform.ps1
# Description: Creates directory and file structure for the workflow-automation-platform project

$root = "workflow-automation-platform"
New-Item -Path $root -ItemType Directory -Force | Out-Null

# --- FRONTEND ---
$frontend = "$root/frontend"
New-Item -Path $frontend -ItemType Directory -Force | Out-Null

$frontendSrc = "$frontend/src"
New-Item -Path $frontendSrc -ItemType Directory -Force | Out-Null

$frontendDirs = @("components", "pages", "services", "types", "utils")
foreach ($dir in $frontendDirs) {
    New-Item -Path "$frontendSrc/$dir" -ItemType Directory -Force | Out-Null
}

New-Item -Path "$frontend/Dockerfile" -ItemType File -Force | Out-Null
New-Item -Path "$frontend/package.json" -ItemType File -Force | Out-Null

# --- BACKEND ---
$backend = "$root/backend"
New-Item -Path $backend -ItemType Directory -Force | Out-Null

$app = "$backend/app"
New-Item -Path $app -ItemType Directory -Force | Out-Null

$appDirs = @("api", "models", "services", "utils")
foreach ($dir in $appDirs) {
    New-Item -Path "$app/$dir" -ItemType Directory -Force | Out-Null
}

# Integrations inside backend
$integrations = "$app/integrations"
New-Item -Path $integrations -ItemType Directory -Force | Out-Null

$integrationNames = @("jira", "github", "aws", "azure")
foreach ($name in $integrationNames) {
    New-Item -Path "$integrations/$name" -ItemType Directory -Force | Out-Null
}

# Backend root files
New-Item -Path "$app/database.py" -ItemType File -Force | Out-Null
New-Item -Path "$app/main.py" -ItemType File -Force | Out-Null
New-Item -Path "$backend/Dockerfile" -ItemType File -Force | Out-Null
New-Item -Path "$backend/requirements.txt" -ItemType File -Force | Out-Null
New-Item -Path "$backend/.env" -ItemType File -Force | Out-Null
New-Item -Path "$backend/setup_integration_types.py" -ItemType File -Force | Out-Null

# --- ROOT LEVEL FILES ---
New-Item -Path "$root/docker-compose.yml" -ItemType File -Force | Out-Null
New-Item -Path "$root/README.md" -ItemType File -Force | Out-Null
New-Item -Path "$root/QUICKSTART.md" -ItemType File -Force | Out-Null

Write-Host "Workflow Automation Platform structure created successfully at: $(Resolve-Path $root)"
