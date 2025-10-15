import axios from 'axios';
import type {
  IntegrationType,
  Integration,
  Workflow,
  ExecutionLog,
  TestConnectionResult,
} from '@/types';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Integration Types
export const integrationTypeService = {
  getAll: async (): Promise<IntegrationType[]> => {
    const response = await api.get('/integration-types');
    return response.data;
  },

  getById: async (id: number): Promise<IntegrationType> => {
    const response = await api.get(`/integration-types/${id}`);
    return response.data;
  },

  create: async (data: {
    name: string;
    description: string;
    parameters: any[];
  }): Promise<IntegrationType> => {
    const response = await api.post('/integration-types', data);
    return response.data;
  },
};

// Integrations
export const integrationService = {
  getAll: async (): Promise<Integration[]> => {
    const response = await api.get('/integrations');
    return response.data;
  },

  getById: async (id: number): Promise<Integration> => {
    const response = await api.get(`/integrations/${id}`);
    return response.data;
  },

  create: async (data: {
    name: string;
    integration_type_id: number;
    credentials: Record<string, any>;
  }): Promise<Integration> => {
    const response = await api.post('/integrations', data);
    return response.data;
  },

  test: async (data: {
    integration_type_id: number;
    credentials: Record<string, any>;
  }): Promise<TestConnectionResult> => {
    const response = await api.post('/integrations/test', data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/integrations/${id}`);
  },
};

// Workflows
export const workflowService = {
  getAll: async (): Promise<Workflow[]> => {
    const response = await api.get('/workflows');
    return response.data;
  },

  getById: async (id: number): Promise<Workflow> => {
    const response = await api.get(`/workflows/${id}`);
    return response.data;
  },

  create: async (data: {
    name: string;
    description: string;
    workflow_data: any;
  }): Promise<Workflow> => {
    const response = await api.post('/workflows', data);
    return response.data;
  },

  update: async (
    id: number,
    data: {
      name?: string;
      description?: string;
      workflow_data?: any;
    }
  ): Promise<Workflow> => {
    const response = await api.put(`/workflows/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/workflows/${id}`);
  },

  execute: async (id: number): Promise<ExecutionLog> => {
    const response = await api.post(`/workflows/${id}/execute`);
    return response.data;
  },

  getExecutions: async (id: number): Promise<ExecutionLog[]> => {
    const response = await api.get(`/workflows/${id}/executions`);
    return response.data;
  },
};

export default api;
