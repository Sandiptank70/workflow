export interface IntegrationType {
  id: number;
  name: string;
  description: string;
  parameters: Parameter[];
  created_at: string;
}

export interface Parameter {
  name: string;
  type: string;
  required: boolean;
  description: string;
}

export interface Integration {
  id: number;
  name: string;
  integration_type_id: number;
  integration_type_name: string;
  is_active: boolean;
  created_at: string;
}

export interface Workflow {
  id: number;
  name: string;
  description: string;
  workflow_data: WorkflowData;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface WorkflowData {
  nodes: WorkflowNode[];
  connections: WorkflowConnection[];
}

export interface WorkflowNode {
  id: string;
  type: string;
  integration_id?: number;
  task?: string;
  params?: Record<string, any>;
  position?: { x: number; y: number };
}

export interface WorkflowConnection {
  from: string;
  to: string;
}

export interface ExecutionLog {
  id: number;
  workflow_id: number;
  status: string;
  started_at: string;
  completed_at?: string;
  execution_data?: any;
  error_message?: string;
}

export interface TestConnectionResult {
  success: boolean;
  message: string;
  data?: any;
}
