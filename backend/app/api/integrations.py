from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from app.database import get_db
from app.services import IntegrationService
import json

router = APIRouter(prefix="/integrations", tags=["Integrations"])

class IntegrationTest(BaseModel):
    integration_type_id: int
    credentials: Dict[str, Any]

class IntegrationCreate(BaseModel):
    name: str
    integration_type_id: int
    credentials: Dict[str, Any]

class IntegrationResponse(BaseModel):
    id: int
    name: str
    integration_type_id: int
    integration_type_name: str
    is_active: bool
    created_at: str
    
    class Config:
        from_attributes = True

@router.post("/test")
def test_integration(
    data: IntegrationTest,
    db: Session = Depends(get_db)
):
    """Test integration connection"""
    try:
        result = IntegrationService.test_integration(
            db=db,
            integration_type_id=data.integration_type_id,
            credentials=data.credentials
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing integration: {str(e)}")

@router.post("", response_model=IntegrationResponse)
def create_integration(
    data: IntegrationCreate,
    db: Session = Depends(get_db)
):
    """Create a new integration"""
    try:
        integration = IntegrationService.create_integration(
            db=db,
            name=data.name,
            integration_type_id=data.integration_type_id,
            credentials=data.credentials
        )
        return IntegrationResponse(
            id=integration.id,
            name=integration.name,
            integration_type_id=integration.integration_type_id,
            integration_type_name=integration.integration_type.name,
            is_active=integration.is_active,
            created_at=integration.created_at.isoformat()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating integration: {str(e)}")

@router.get("", response_model=List[IntegrationResponse])
def get_integrations(db: Session = Depends(get_db)):
    """Get all integrations"""
    try:
        integrations = IntegrationService.get_integrations(db)
        return [
            IntegrationResponse(
                id=i.id,
                name=i.name,
                integration_type_id=i.integration_type_id,
                integration_type_name=i.integration_type.name,
                is_active=i.is_active,
                created_at=i.created_at.isoformat()
            )
            for i in integrations
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching integrations: {str(e)}")

@router.get("/{integration_id}", response_model=IntegrationResponse)
def get_integration(integration_id: int, db: Session = Depends(get_db)):
    """Get a specific integration"""
    integration = IntegrationService.get_integration(db, integration_id)
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    return IntegrationResponse(
        id=integration.id,
        name=integration.name,
        integration_type_id=integration.integration_type_id,
        integration_type_name=integration.integration_type.name,
        is_active=integration.is_active,
        created_at=integration.created_at.isoformat()
    )

@router.delete("/{integration_id}")
def delete_integration(integration_id: int, db: Session = Depends(get_db)):
    """Delete an integration"""
    success = IntegrationService.delete_integration(db, integration_id)
    if not success:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    return {"message": "Integration deleted successfully"}
