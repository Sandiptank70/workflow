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

class IntegrationTypeCreate(BaseModel):
    name: str
    description: str = ""
    parameters: List[dict]

class IntegrationTypeResponse(BaseModel):
    id: int
    name: str
    description: str
    parameters: List[dict]
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
            description=data.description
        )
        return IntegrationTypeResponse(
            id=integration_type.id,
            name=integration_type.name,
            description=integration_type.description or "",
            parameters=json.loads(integration_type.parameters),
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
        created_at=integration_type.created_at.isoformat()
    )
