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

class WorkflowExecuteRequest(BaseModel):
    """Request body for workflow execution with optional runtime parameters"""
    runtime_params: Optional[Dict[str, Any]] = None
    trigger_source: Optional[str] = "manual"
    trigger_metadata: Optional[Dict[str, Any]] = None

class WorkflowExecuteResponse(BaseModel):
    """Detailed workflow execution response"""
    execution_id: int
    workflow_id: int
    workflow_name: str
    status: str
    started_at: str
    completed_at: Optional[str]
    execution_time_seconds: Optional[float]
    nodes_executed: int
    nodes_total: int
    node_results: List[Dict[str, Any]]
    error_message: Optional[str]
    trigger_source: str
    
    class Config:
        from_attributes = True

@router.post("/{workflow_id}/execute", response_model=WorkflowExecuteResponse)
def execute_workflow(
    workflow_id: int,
    request: Optional[WorkflowExecuteRequest] = None,
    db: Session = Depends(get_db)
):
    """
    Execute a workflow with optional runtime parameters
    
    This endpoint can be triggered via API to automate workflow execution.
    
    Parameters:
    - workflow_id: ID of the workflow to execute
    - runtime_params: Optional parameters to pass to all nodes
    - trigger_source: Source of the trigger (api, manual, scheduled, webhook, etc.)
    - trigger_metadata: Additional metadata about the trigger
    
    Returns detailed execution information including:
    - Execution status
    - Results from each node
    - Execution time
    - Any errors that occurred
    """
    try:
        # Extract request data
        runtime_params = request.runtime_params if request else None
        trigger_source = request.trigger_source if request else "manual"
        trigger_metadata = request.trigger_metadata if request else {}
        
        # Execute workflow with enhanced tracking
        execution_log = WorkflowService.execute_workflow(
            db, 
            workflow_id,
            runtime_params=runtime_params,
            trigger_source=trigger_source,
            trigger_metadata=trigger_metadata
        )
        
        # Parse execution data
        execution_data = json.loads(execution_log.execution_data) if execution_log.execution_data else {}
        node_results = execution_data.get("node_results", [])
        
        # Calculate execution time
        execution_time = None
        if execution_log.completed_at and execution_log.started_at:
            delta = execution_log.completed_at - execution_log.started_at
            execution_time = delta.total_seconds()
        
        # Get workflow name
        workflow = WorkflowService.get_workflow(db, workflow_id)
        workflow_name = workflow.name if workflow else "Unknown"
        
        # Count nodes
        nodes_executed = len([r for r in node_results if r.get("success")])
        nodes_total = len(node_results)
        
        return WorkflowExecuteResponse(
            execution_id=execution_log.id,
            workflow_id=execution_log.workflow_id,
            workflow_name=workflow_name,
            status=execution_log.status,
            started_at=execution_log.started_at.isoformat(),
            completed_at=execution_log.completed_at.isoformat() if execution_log.completed_at else None,
            execution_time_seconds=execution_time,
            nodes_executed=nodes_executed,
            nodes_total=nodes_total,
            node_results=node_results,
            error_message=execution_log.error_message,
            trigger_source=trigger_source
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing workflow: {str(e)}")

@router.post("/{workflow_id}/trigger", response_model=WorkflowExecuteResponse)
def trigger_workflow_via_api(
    workflow_id: int,
    request: Optional[WorkflowExecuteRequest] = None,
    db: Session = Depends(get_db)
):
    """
    Trigger workflow execution via API (webhook-style endpoint)
    
    This is an alias for the execute endpoint, designed for external API triggers.
    Use this when you want to trigger workflows from external systems.
    
    Example:
        POST /api/workflows/1/trigger
        {
            "runtime_params": {
                "user_id": "12345",
                "action": "deploy"
            },
            "trigger_source": "github_webhook",
            "trigger_metadata": {
                "commit": "abc123",
                "branch": "main"
            }
        }
    """
    if not request:
        request = WorkflowExecuteRequest()
    
    if not request.trigger_source:
        request.trigger_source = "api"
    
    return execute_workflow(workflow_id, request, db)

@router.get("/executions/all", response_model=List[ExecutionLogResponse])
def get_all_executions(db: Session = Depends(get_db)):
    """Get all execution logs across all workflows"""
    try:
        logs = WorkflowService.get_execution_logs(db)
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