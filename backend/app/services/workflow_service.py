from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import json
import importlib
from datetime import datetime
from app.models import Workflow, ExecutionLog
from app.services.integration_service import IntegrationService

class WorkflowService:
    """Service for managing workflows and execution"""
    
    @staticmethod
    def create_workflow(
        db: Session,
        name: str,
        workflow_data: Dict[str, Any],
        description: Optional[str] = None
    ) -> Workflow:
        """Create a new workflow"""
        workflow = Workflow(
            name=name,
            description=description,
            workflow_data=json.dumps(workflow_data)
        )
        db.add(workflow)
        db.commit()
        db.refresh(workflow)
        return workflow
    
    @staticmethod
    def get_workflows(db: Session) -> List[Workflow]:
        """Get all workflows"""
        return db.query(Workflow).all()
    
    @staticmethod
    def get_workflow(db: Session, workflow_id: int) -> Optional[Workflow]:
        """Get workflow by ID"""
        return db.query(Workflow).filter(Workflow.id == workflow_id).first()
    
    @staticmethod
    def update_workflow(
        db: Session,
        workflow_id: int,
        name: Optional[str] = None,
        workflow_data: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None
    ) -> Optional[Workflow]:
        """Update an existing workflow"""
        workflow = WorkflowService.get_workflow(db, workflow_id)
        if not workflow:
            return None
        
        if name is not None:
            workflow.name = name
        if description is not None:
            workflow.description = description
        if workflow_data is not None:
            workflow.workflow_data = json.dumps(workflow_data)
        
        db.commit()
        db.refresh(workflow)
        return workflow
    
    @staticmethod
    def delete_workflow(db: Session, workflow_id: int) -> bool:
        """Delete a workflow"""
        workflow = WorkflowService.get_workflow(db, workflow_id)
        if not workflow:
            return False
        
        db.delete(workflow)
        db.commit()
        return True
    
    @staticmethod
    def execute_workflow(db: Session, workflow_id: int) -> ExecutionLog:
        """Execute a workflow and log the results"""
        workflow = WorkflowService.get_workflow(db, workflow_id)
        if not workflow:
            raise ValueError("Workflow not found")
        
        # Create execution log
        execution_log = ExecutionLog(
            workflow_id=workflow_id,
            status="running",
            started_at=datetime.utcnow()
        )
        db.add(execution_log)
        db.commit()
        
        try:
            # Parse workflow data
            workflow_data = json.loads(workflow.workflow_data)
            nodes = workflow_data.get("nodes", [])
            connections = workflow_data.get("connections", [])
            
            # Build execution order based on connections
            execution_order = WorkflowService._build_execution_order(nodes, connections)
            
            # Execute nodes in order
            execution_results = []
            for node_id in execution_order:
                node = next((n for n in nodes if n["id"] == node_id), None)
                if not node:
                    continue
                
                node_result = WorkflowService._execute_node(db, node)
                execution_results.append({
                    "node_id": node_id,
                    "result": node_result
                })
                
                # Stop execution if node failed
                if not node_result.get("success", False):
                    execution_log.status = "failed"
                    execution_log.error_message = node_result.get("message", "Node execution failed")
                    break
            else:
                # All nodes executed successfully
                execution_log.status = "success"
            
            execution_log.completed_at = datetime.utcnow()
            execution_log.execution_data = json.dumps(execution_results)
            db.commit()
            db.refresh(execution_log)
            return execution_log
            
        except Exception as e:
            execution_log.status = "failed"
            execution_log.error_message = str(e)
            execution_log.completed_at = datetime.utcnow()
            db.commit()
            db.refresh(execution_log)
            return execution_log
    
    @staticmethod
    def _build_execution_order(nodes: List[Dict], connections: List[Dict]) -> List[str]:
        """Build execution order based on node connections (topological sort)"""
        # Simple implementation: execute in the order they appear
        # For production, implement proper topological sort
        node_ids = [node["id"] for node in nodes]
        
        if not connections:
            return node_ids
        
        # Build adjacency list
        graph = {node_id: [] for node_id in node_ids}
        in_degree = {node_id: 0 for node_id in node_ids}
        
        for conn in connections:
            from_node = conn.get("from")
            to_node = conn.get("to")
            if from_node in graph and to_node in graph:
                graph[from_node].append(to_node)
                in_degree[to_node] += 1
        
        # Topological sort using Kahn's algorithm
        queue = [node_id for node_id in node_ids if in_degree[node_id] == 0]
        execution_order = []
        
        while queue:
            node_id = queue.pop(0)
            execution_order.append(node_id)
            
            for neighbor in graph[node_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # If not all nodes are included, there's a cycle or disconnected nodes
        if len(execution_order) != len(node_ids):
            # Add remaining nodes
            for node_id in node_ids:
                if node_id not in execution_order:
                    execution_order.append(node_id)
        
        return execution_order
    
    @staticmethod
    def _execute_node(db: Session, node: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow node"""
        try:
            node_type = node.get("type")
            
            if node_type != "integration":
                return {
                    "success": False,
                    "message": f"Unsupported node type: {node_type}"
                }
            
            integration_id = node.get("integration_id")
            task_name = node.get("task")
            params = node.get("params", {})
            
            if not all([integration_id, task_name]):
                return {
                    "success": False,
                    "message": "Missing integration_id or task name"
                }
            
            # Get integration and credentials
            integration = IntegrationService.get_integration(db, integration_id)
            if not integration:
                return {
                    "success": False,
                    "message": f"Integration {integration_id} not found"
                }
            
            credentials = IntegrationService.get_integration_credentials(db, integration_id)
            
            # Get integration type
            integration_type = integration.integration_type
            module_name = integration_type.name.lower()
            
            # Dynamically import and execute task
            module = importlib.import_module(f"app.integrations.{module_name}")
            
            if hasattr(module, task_name):
                task_func = getattr(module, task_name)
                result = task_func(credentials, params)
                return result
            else:
                return {
                    "success": False,
                    "message": f"Task '{task_name}' not found in {module_name}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error executing node: {str(e)}"
            }
    
    @staticmethod
    def get_execution_logs(db: Session, workflow_id: Optional[int] = None) -> List[ExecutionLog]:
        """Get execution logs, optionally filtered by workflow_id"""
        query = db.query(ExecutionLog)
        if workflow_id:
            query = query.filter(ExecutionLog.workflow_id == workflow_id)
        return query.order_by(ExecutionLog.started_at.desc()).all()
