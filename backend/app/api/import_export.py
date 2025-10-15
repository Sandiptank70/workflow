from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from app.database import get_db
from app.models import IntegrationType, Integration, Workflow
import json
from datetime import datetime

router = APIRouter(prefix="/import-export", tags=["Import/Export"])

# ================== EXPORT MODELS ==================

class ExportData(BaseModel):
    """Complete export data structure"""
    version: str = "1.0"
    exported_at: str
    integration_types: List[Dict[str, Any]]
    integrations: List[Dict[str, Any]]
    workflows: List[Dict[str, Any]]

# ================== EXPORT ENDPOINTS ==================

@router.get("/export/all")
def export_all(db: Session = Depends(get_db)):
    """
    Export all configuration (Integration Types, Integrations, Workflows)
    
    Returns JSON file with all data for easy deployment to another environment
    """
    try:
        # Export Integration Types
        integration_types = db.query(IntegrationType).all()
        integration_types_data = [
            {
                "name": it.name,
                "description": it.description,
                "parameters": json.loads(it.parameters),
                "tasks": json.loads(it.tasks) if it.tasks else None
            }
            for it in integration_types
        ]
        
        # Export Integrations (without sensitive credentials)
        integrations = db.query(Integration).all()
        integrations_data = [
            {
                "name": i.name,
                "integration_type_name": i.integration_type.name,
                "is_active": i.is_active,
                # Note: Credentials are NOT exported for security
                "credentials_template": "REPLACE_WITH_YOUR_CREDENTIALS"
            }
            for i in integrations
        ]
        
        # Export Workflows
        workflows = db.query(Workflow).all()
        workflows_data = [
            {
                "name": w.name,
                "description": w.description,
                "workflow_data": json.loads(w.workflow_data),
                "is_active": w.is_active
            }
            for w in workflows
        ]
        
        export_data = {
            "version": "1.0",
            "exported_at": datetime.utcnow().isoformat(),
            "integration_types": integration_types_data,
            "integrations": integrations_data,
            "workflows": workflows_data
        }
        
        return export_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.get("/export/integration-types")
def export_integration_types(db: Session = Depends(get_db)):
    """Export only Integration Types"""
    try:
        integration_types = db.query(IntegrationType).all()
        data = [
            {
                "name": it.name,
                "description": it.description,
                "parameters": json.loads(it.parameters),
                "tasks": json.loads(it.tasks) if it.tasks else None
            }
            for it in integration_types
        ]
        
        return {
            "version": "1.0",
            "exported_at": datetime.utcnow().isoformat(),
            "integration_types": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.get("/export/integrations")
def export_integrations(db: Session = Depends(get_db)):
    """Export only Integrations (without credentials)"""
    try:
        integrations = db.query(Integration).all()
        data = [
            {
                "name": i.name,
                "integration_type_name": i.integration_type.name,
                "is_active": i.is_active,
                "credentials_template": "REPLACE_WITH_YOUR_CREDENTIALS"
            }
            for i in integrations
        ]
        
        return {
            "version": "1.0",
            "exported_at": datetime.utcnow().isoformat(),
            "integrations": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.get("/export/workflows")
def export_workflows(db: Session = Depends(get_db)):
    """Export only Workflows"""
    try:
        workflows = db.query(Workflow).all()
        data = [
            {
                "name": w.name,
                "description": w.description,
                "workflow_data": json.loads(w.workflow_data),
                "is_active": w.is_active
            }
            for w in workflows
        ]
        
        return {
            "version": "1.0",
            "exported_at": datetime.utcnow().isoformat(),
            "workflows": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


# ================== IMPORT ENDPOINTS ==================

class ImportAllRequest(BaseModel):
    """Request body for importing all data"""
    integration_types: List[Dict[str, Any]] = []
    integrations: List[Dict[str, Any]] = []
    workflows: List[Dict[str, Any]] = []
    skip_existing: bool = True  # Skip if already exists


@router.post("/import/all")
def import_all(data: ImportAllRequest, db: Session = Depends(get_db)):
    """
    Import all configuration (Integration Types, Integrations, Workflows)
    
    - skip_existing: If True, skip items that already exist
    """
    results = {
        "integration_types": {"imported": 0, "skipped": 0, "errors": []},
        "integrations": {"imported": 0, "skipped": 0, "errors": []},
        "workflows": {"imported": 0, "skipped": 0, "errors": []}
    }
    
    try:
        # Import Integration Types
        for it_data in data.integration_types:
            try:
                existing = db.query(IntegrationType).filter(
                    IntegrationType.name == it_data["name"]
                ).first()
                
                if existing and data.skip_existing:
                    results["integration_types"]["skipped"] += 1
                    continue
                
                if existing:
                    # Update existing
                    existing.description = it_data.get("description")
                    existing.parameters = json.dumps(it_data["parameters"])
                    existing.tasks = json.dumps(it_data.get("tasks")) if it_data.get("tasks") else None
                else:
                    # Create new
                    new_it = IntegrationType(
                        name=it_data["name"],
                        description=it_data.get("description"),
                        parameters=json.dumps(it_data["parameters"]),
                        tasks=json.dumps(it_data.get("tasks")) if it_data.get("tasks") else None
                    )
                    db.add(new_it)
                
                results["integration_types"]["imported"] += 1
                
            except Exception as e:
                results["integration_types"]["errors"].append(f"{it_data.get('name', 'unknown')}: {str(e)}")
        
        db.commit()
        
        # Import Integrations (requires manual credential setup)
        for i_data in data.integrations:
            try:
                # Find integration type
                it = db.query(IntegrationType).filter(
                    IntegrationType.name == i_data["integration_type_name"]
                ).first()
                
                if not it:
                    results["integrations"]["errors"].append(
                        f"{i_data['name']}: Integration type '{i_data['integration_type_name']}' not found"
                    )
                    continue
                
                existing = db.query(Integration).filter(
                    Integration.name == i_data["name"],
                    Integration.integration_type_id == it.id
                ).first()
                
                if existing and data.skip_existing:
                    results["integrations"]["skipped"] += 1
                    continue
                
                # Note: Credentials must be set manually after import
                if not existing:
                    results["integrations"]["errors"].append(
                        f"{i_data['name']}: Skipped - credentials must be configured manually"
                    )
                    results["integrations"]["skipped"] += 1
                    
            except Exception as e:
                results["integrations"]["errors"].append(f"{i_data.get('name', 'unknown')}: {str(e)}")
        
        # Import Workflows
        for w_data in data.workflows:
            try:
                existing = db.query(Workflow).filter(
                    Workflow.name == w_data["name"]
                ).first()
                
                if existing and data.skip_existing:
                    results["workflows"]["skipped"] += 1
                    continue
                
                if existing:
                    # Update existing
                    existing.description = w_data.get("description")
                    existing.workflow_data = json.dumps(w_data["workflow_data"])
                    existing.is_active = w_data.get("is_active", True)
                else:
                    # Create new
                    new_w = Workflow(
                        name=w_data["name"],
                        description=w_data.get("description"),
                        workflow_data=json.dumps(w_data["workflow_data"]),
                        is_active=w_data.get("is_active", True)
                    )
                    db.add(new_w)
                
                results["workflows"]["imported"] += 1
                
            except Exception as e:
                results["workflows"]["errors"].append(f"{w_data.get('name', 'unknown')}: {str(e)}")
        
        db.commit()
        
        return {
            "success": True,
            "message": "Import completed",
            "results": results
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


class ImportIntegrationTypesRequest(BaseModel):
    integration_types: List[Dict[str, Any]]
    skip_existing: bool = True


@router.post("/import/integration-types")
def import_integration_types(data: ImportIntegrationTypesRequest, db: Session = Depends(get_db)):
    """Import only Integration Types"""
    imported = 0
    skipped = 0
    errors = []
    
    try:
        for it_data in data.integration_types:
            try:
                existing = db.query(IntegrationType).filter(
                    IntegrationType.name == it_data["name"]
                ).first()
                
                if existing and data.skip_existing:
                    skipped += 1
                    continue
                
                if existing:
                    # Update
                    existing.description = it_data.get("description")
                    existing.parameters = json.dumps(it_data["parameters"])
                    existing.tasks = json.dumps(it_data.get("tasks")) if it_data.get("tasks") else None
                else:
                    # Create
                    new_it = IntegrationType(
                        name=it_data["name"],
                        description=it_data.get("description"),
                        parameters=json.dumps(it_data["parameters"]),
                        tasks=json.dumps(it_data.get("tasks")) if it_data.get("tasks") else None
                    )
                    db.add(new_it)
                
                imported += 1
                
            except Exception as e:
                errors.append(f"{it_data.get('name', 'unknown')}: {str(e)}")
        
        db.commit()
        
        return {
            "success": True,
            "imported": imported,
            "skipped": skipped,
            "errors": errors
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


class ImportWorkflowsRequest(BaseModel):
    workflows: List[Dict[str, Any]]
    skip_existing: bool = True


@router.post("/import/workflows")
def import_workflows(data: ImportWorkflowsRequest, db: Session = Depends(get_db)):
    """Import only Workflows"""
    imported = 0
    skipped = 0
    errors = []
    
    try:
        for w_data in data.workflows:
            try:
                existing = db.query(Workflow).filter(
                    Workflow.name == w_data["name"]
                ).first()
                
                if existing and data.skip_existing:
                    skipped += 1
                    continue
                
                if existing:
                    # Update
                    existing.description = w_data.get("description")
                    existing.workflow_data = json.dumps(w_data["workflow_data"])
                    existing.is_active = w_data.get("is_active", True)
                else:
                    # Create
                    new_w = Workflow(
                        name=w_data["name"],
                        description=w_data.get("description"),
                        workflow_data=json.dumps(w_data["workflow_data"]),
                        is_active=w_data.get("is_active", True)
                    )
                    db.add(new_w)
                
                imported += 1
                
            except Exception as e:
                errors.append(f"{w_data.get('name', 'unknown')}: {str(e)}")
        
        db.commit()
        
        return {
            "success": True,
            "imported": imported,
            "skipped": skipped,
            "errors": errors
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")