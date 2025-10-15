from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database import get_db
from app.services import IntegrationService
import json

router = APIRouter(prefix="/integration-types", tags=["Integration Types"])

class ParameterSchema(BaseModel):
    name: str
    type: str
    required: bool = True
    description: str = ""

class TaskSchema(BaseModel):
    """Schema for task definition"""
    name: str  # Function name (e.g., "test_connection")
    display_name: str  # Human-readable name (e.g., "Test Connection")
    description: str  # What the task does
    parameters: List[dict] = []  # Task-specific parameters

class IntegrationTypeCreate(BaseModel):
    name: str
    description: str = ""
    parameters: List[dict]
    tasks: List[dict] = []  # List of available tasks

class IntegrationTypeResponse(BaseModel):
    id: int
    name: str
    description: str
    parameters: List[dict]
    tasks: List[dict] = []
    created_at: str
    
    class Config:
        from_attributes = True

@router.post("", response_model=IntegrationTypeResponse)
def create_integration_type(
    data: IntegrationTypeCreate,
    db: Session = Depends(get_db)
):
    """Create a new integration type"""
    try:
        integration_type = IntegrationService.create_integration_type(
            db=db,
            name=data.name,
            parameters=data.parameters,
            description=data.description,
            tasks=data.tasks
        )
        return IntegrationTypeResponse(
            id=integration_type.id,
            name=integration_type.name,
            description=integration_type.description or "",
            parameters=json.loads(integration_type.parameters),
            tasks=json.loads(integration_type.tasks) if integration_type.tasks else [],
            created_at=integration_type.created_at.isoformat()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating integration type: {str(e)}")

@router.get("", response_model=List[IntegrationTypeResponse])
def get_integration_types(db: Session = Depends(get_db)):
    """Get all integration types"""
    try:
        integration_types = IntegrationService.get_integration_types(db)
        return [
            IntegrationTypeResponse(
                id=it.id,
                name=it.name,
                description=it.description or "",
                parameters=json.loads(it.parameters),
                tasks=json.loads(it.tasks) if it.tasks else [],
                created_at=it.created_at.isoformat()
            )
            for it in integration_types
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching integration types: {str(e)}")

@router.get("/{type_id}", response_model=IntegrationTypeResponse)
def get_integration_type(type_id: int, db: Session = Depends(get_db)):
    """Get a specific integration type"""
    integration_type = IntegrationService.get_integration_type(db, type_id)
    if not integration_type:
        raise HTTPException(status_code=404, detail="Integration type not found")
    
    return IntegrationTypeResponse(
        id=integration_type.id,
        name=integration_type.name,
        description=integration_type.description or "",
        parameters=json.loads(integration_type.parameters),
        tasks=json.loads(integration_type.tasks) if integration_type.tasks else [],
        created_at=integration_type.created_at.isoformat()
    )

@router.put("/{type_id}", response_model=IntegrationTypeResponse)
def update_integration_type(
    type_id: int,
    data: IntegrationTypeCreate,
    db: Session = Depends(get_db)
):
    """Update an existing integration type"""
    try:
        integration_type = IntegrationService.get_integration_type(db, type_id)
        if not integration_type:
            raise HTTPException(status_code=404, detail="Integration type not found")
        
        # Update fields
        integration_type.name = data.name
        integration_type.description = data.description
        integration_type.parameters = json.dumps(data.parameters)
        integration_type.tasks = json.dumps(data.tasks)
        
        db.commit()
        db.refresh(integration_type)
        
        return IntegrationTypeResponse(
            id=integration_type.id,
            name=integration_type.name,
            description=integration_type.description or "",
            parameters=json.loads(integration_type.parameters),
            tasks=json.loads(integration_type.tasks) if integration_type.tasks else [],
            created_at=integration_type.created_at.isoformat()
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating integration type: {str(e)}")

@router.delete("/{type_id}")
def delete_integration_type(type_id: int, db: Session = Depends(get_db)):
    """Delete an integration type"""
    try:
        integration_type = IntegrationService.get_integration_type(db, type_id)
        if not integration_type:
            raise HTTPException(status_code=404, detail="Integration type not found")
        
        # Check if any integrations are using this type
        from app.models import Integration
        integrations_count = db.query(Integration).filter(
            Integration.integration_type_id == type_id
        ).count()
        
        if integrations_count > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot delete integration type. {integrations_count} integration(s) are using it."
            )
        
        db.delete(integration_type)
        db.commit()
        
        return {"message": "Integration type deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting integration type: {str(e)}")