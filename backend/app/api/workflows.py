from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.database import get_db
from app.services import WorkflowService
import json

router = APIRouter(prefix="/workflows", tags=["Workflows"])

class WorkflowCreate(BaseModel):
    name: str
    description: str = ""
    workflow_data: Dict[str, Any]

class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    workflow_data: Optional[Dict[str, Any]] = None

class WorkflowResponse(BaseModel):
    id: int
    name: str
    description: str
    workflow_data: Dict[str, Any]
    is_active: bool
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

class ExecutionLogResponse(BaseModel):
    id: int
    workflow_id: int
    status: str
    started_at: str
    completed_at: Optional[str]
    execution_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    
    class Config:
        from_attributes = True

@router.post("", response_model=WorkflowResponse)
def create_workflow(
    data: WorkflowCreate,
    db: Session = Depends(get_db)
):
    """Create a new workflow"""
    try:
        workflow = WorkflowService.create_workflow(
            db=db,
            name=data.name,
            workflow_data=data.workflow_data,
            description=data.description
        )
        return WorkflowResponse(
            id=workflow.id,
            name=workflow.name,
            description=workflow.description or "",
            workflow_data=json.loads(workflow.workflow_data),
            is_active=workflow.is_active,
            created_at=workflow.created_at.isoformat(),
            updated_at=workflow.updated_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating workflow: {str(e)}")

@router.get("", response_model=List[WorkflowResponse])
def get_workflows(db: Session = Depends(get_db)):
    """Get all workflows"""
    try:
        workflows = WorkflowService.get_workflows(db)
        return [
            WorkflowResponse(
                id=w.id,
                name=w.name,
                description=w.description or "",
                workflow_data=json.loads(w.workflow_data),
                is_active=w.is_active,
                created_at=w.created_at.isoformat(),
                updated_at=w.updated_at.isoformat()
            )
            for w in workflows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching workflows: {str(e)}")

@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    """Get a specific workflow"""
    workflow = WorkflowService.get_workflow(db, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return WorkflowResponse(
        id=workflow.id,
        name=workflow.name,
        description=workflow.description or "",
        workflow_data=json.loads(workflow.workflow_data),
        is_active=workflow.is_active,
        created_at=workflow.created_at.isoformat(),
        updated_at=workflow.updated_at.isoformat()
    )

@router.put("/{workflow_id}", response_model=WorkflowResponse)
def update_workflow(
    workflow_id: int,
    data: WorkflowUpdate,
    db: Session = Depends(get_db)
):
    """Update a workflow"""
    workflow = WorkflowService.update_workflow(
        db=db,
        workflow_id=workflow_id,
        name=data.name,
        workflow_data=data.workflow_data,
        description=data.description
    )
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return WorkflowResponse(
        id=workflow.id,
        name=workflow.name,
        description=workflow.description or "",
        workflow_data=json.loads(workflow.workflow_data),
        is_active=workflow.is_active,
        created_at=workflow.created_at.isoformat(),
        updated_at=workflow.updated_at.isoformat()
    )

@router.delete("/{workflow_id}")
def delete_workflow(workflow_id: int, db: Session = Depends(get_db)):
    """Delete a workflow"""
    success = WorkflowService.delete_workflow(db, workflow_id)
    if not success:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return {"message": "Workflow deleted successfully"}

@router.post("/{workflow_id}/execute", response_model=ExecutionLogResponse)
def execute_workflow(workflow_id: int, db: Session = Depends(get_db)):
    """Execute a workflow"""
    try:
        execution_log = WorkflowService.execute_workflow(db, workflow_id)
        return ExecutionLogResponse(
            id=execution_log.id,
            workflow_id=execution_log.workflow_id,
            status=execution_log.status,
            started_at=execution_log.started_at.isoformat(),
            completed_at=execution_log.completed_at.isoformat() if execution_log.completed_at else None,
            execution_data=json.loads(execution_log.execution_data) if execution_log.execution_data else None,
            error_message=execution_log.error_message
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing workflow: {str(e)}")

@router.get("/{workflow_id}/executions", response_model=List[ExecutionLogResponse])
def get_workflow_executions(workflow_id: int, db: Session = Depends(get_db)):
    """Get execution logs for a specific workflow"""
    try:
        logs = WorkflowService.get_execution_logs(db, workflow_id)
        return [
            ExecutionLogResponse(
                id=log.id,
                workflow_id=log.workflow_id,
                status=log.status,
                started_at=log.started_at.isoformat(),
                completed_at=log.completed_at.isoformat() if log.completed_at else None,
                execution_data=json.loads(log.execution_data) if log.execution_data else None,
                error_message=log.error_message
            )
            for log in logs
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching execution logs: {str(e)}")
