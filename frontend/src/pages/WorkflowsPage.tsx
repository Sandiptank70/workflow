import React, { useState, useEffect, useCallback } from 'react';
import ReactFlow, {
  Node,
  Edge,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
  MiniMap,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Plus, Save, Play, Trash2 } from 'lucide-react';
import { Button } from '@/components/Button';
import { Input } from '@/components/Input';
import { Modal } from '@/components/Modal';
import { ExecutionModal } from '@/components/ExecutionModal';
import { workflowService, integrationService, integrationTypeService } from '@/services/api';
import type { Workflow, Integration, IntegrationType } from '@/types';
import { formatDate } from '@/utils/helpers';

export const WorkflowsPage: React.FC = () => {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [integrations, setIntegrations] = useState<Integration[]>([]);
  const [integrationTypes, setIntegrationTypes] = useState<IntegrationType[]>([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState<Workflow | null>(null);
  const [isBuilderOpen, setIsBuilderOpen] = useState(false);
  const [isNodeModalOpen, setIsNodeModalOpen] = useState(false);
  const [isExecutionModalOpen, setIsExecutionModalOpen] = useState(false);
  const [currentExecution, setCurrentExecution] = useState<any>(null);

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  const [workflowName, setWorkflowName] = useState('');
  const [workflowDescription, setWorkflowDescription] = useState('');

  const [nodeFormData, setNodeFormData] = useState({
    integration_id: '',
    task: '',
    params: {} as Record<string, any>,
  });

  const [paramsText, setParamsText] = useState('{}');
  const [availableTasks, setAvailableTasks] = useState<any[]>([]);
  const [selectedTask, setSelectedTask] = useState<any>(null);
  const [showJsonEditor, setShowJsonEditor] = useState(false);

  useEffect(() => {
    loadWorkflows();
    loadIntegrations();
    loadIntegrationTypes();
  }, []);

  const loadWorkflows = async () => {
    try {
      const data = await workflowService.getAll();
      setWorkflows(data);
    } catch (error) {
      console.error('Error loading workflows:', error);
    }
  };

  const loadIntegrations = async () => {
    try {
      const data = await integrationService.getAll();
      setIntegrations(data);
    } catch (error) {
      console.error('Error loading integrations:', error);
    }
  };

  const loadIntegrationTypes = async () => {
    try {
      const data = await integrationTypeService.getAll();
      setIntegrationTypes(data);
    } catch (error) {
      console.error('Error loading integration types:', error);
    }
  };

  // When integration is selected, load its available tasks
  const handleIntegrationChange = (integrationId: string) => {
    setNodeFormData({ ...nodeFormData, integration_id: integrationId, task: '' });
    setSelectedTask(null);
    setParamsText('{}');

    if (integrationId) {
      const integration = integrations.find(i => i.id === parseInt(integrationId));
      if (integration) {
        const integrationType = integrationTypes.find(t => t.id === integration.integration_type_id);
        if (integrationType && integrationType.tasks && integrationType.tasks.length > 0) {
          setAvailableTasks(integrationType.tasks);
        } else {
          setAvailableTasks([]);
        }
      }
    } else {
      setAvailableTasks([]);
    }
  };

  // When task is selected, auto-populate parameter template
  const handleTaskChange = (taskName: string) => {
    setNodeFormData({ ...nodeFormData, task: taskName, params: {} });

    const task = availableTasks.find(t => t.name === taskName);
    setSelectedTask(task);

    if (task && task.parameters && task.parameters.length > 0) {
      // Create parameter template for both JSON and form
      const paramTemplate: any = {};
      task.parameters.forEach((param: any) => {
        if (param.type === 'boolean') {
          paramTemplate[param.name] = false;
        } else if (param.type === 'number') {
          paramTemplate[param.name] = 0;
        } else {
          paramTemplate[param.name] = '';
        }
      });

      // Initialize both JSON text and form params
      setParamsText(JSON.stringify(paramTemplate, null, 2));
      setNodeFormData(prev => ({ ...prev, params: paramTemplate }));
    } else {
      setParamsText('{}');
      setNodeFormData(prev => ({ ...prev, params: {} }));
    }

    // Default to form view if task has parameters
    setShowJsonEditor(false);
  };

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const openBuilder = (workflow?: Workflow) => {
    if (workflow) {
      setSelectedWorkflow(workflow);
      setWorkflowName(workflow.name);
      setWorkflowDescription(workflow.description);

      const loadedNodes: Node[] = workflow.workflow_data.nodes.map((node, index) => ({
        id: node.id,
        type: 'default',
        data: {
          label: `${node.task || 'Node'} (Int: ${node.integration_id})`,
          ...node,
        },
        position: node.position || { x: 100 + index * 200, y: 100 },
      }));

      const loadedEdges: Edge[] = workflow.workflow_data.connections.map((conn) => ({
        id: `e${conn.from}-${conn.to}`,
        source: conn.from,
        target: conn.to,
      }));

      setNodes(loadedNodes);
      setEdges(loadedEdges);
    } else {
      setSelectedWorkflow(null);
      setWorkflowName('');
      setWorkflowDescription('');
      setNodes([]);
      setEdges([]);
    }
    setIsBuilderOpen(true);
  };

  const addNode = () => {
    setIsNodeModalOpen(true);
  };

  const handleNodeSubmit = () => {
    if (!nodeFormData.integration_id || !nodeFormData.task) {
      alert('Please fill in all required fields');
      return;
    }

    // Use params from dynamic form, or parse from JSON if in JSON mode
    let params = {};
    if (showJsonEditor || !selectedTask || selectedTask.parameters.length === 0) {
      // JSON mode or no parameters defined - parse from textarea
      try {
        if (paramsText.trim()) {
          params = JSON.parse(paramsText);
        }
      } catch (error) {
        alert('Invalid JSON format in parameters. Please fix or switch to form view.');
        return;
      }
    } else {
      // Dynamic form mode - use params from nodeFormData
      params = nodeFormData.params;
    }

    const newNode: Node = {
      id: `node-${Date.now()}`,
      type: 'default',
      data: {
        label: `${selectedTask?.display_name || nodeFormData.task} (Int: ${nodeFormData.integration_id})`,
        integration_id: parseInt(nodeFormData.integration_id),
        task: nodeFormData.task,
        params: params,
      },
      position: { x: 250, y: 100 + nodes.length * 100 },
    };

    setNodes((nds) => [...nds, newNode]);
    setIsNodeModalOpen(false);
    setNodeFormData({ integration_id: '', task: '', params: {} });
    setParamsText('{}');
    setAvailableTasks([]);
    setSelectedTask(null);
    setShowJsonEditor(false);
  };

  const saveWorkflow = async () => {
    if (!workflowName.trim()) {
      alert('Please enter a workflow name');
      return;
    }

    const workflowData = {
      nodes: nodes.map((node) => ({
        id: node.id,
        type: 'integration',
        integration_id: node.data.integration_id,
        task: node.data.task,
        params: node.data.params || {},
        position: node.position,
      })),
      connections: edges.map((edge) => ({
        from: edge.source,
        to: edge.target,
      })),
    };

    try {
      if (selectedWorkflow) {
        await workflowService.update(selectedWorkflow.id, {
          name: workflowName,
          description: workflowDescription,
          workflow_data: workflowData,
        });
        alert('Workflow updated successfully!');
      } else {
        await workflowService.create({
          name: workflowName,
          description: workflowDescription,
          workflow_data: workflowData,
        });
        alert('Workflow created successfully!');
      }
      setIsBuilderOpen(false);
      loadWorkflows();
    } catch (error: any) {
      console.error('Error saving workflow:', error);
      alert(error.response?.data?.detail || 'Failed to save workflow');
    }
  };

  const executeWorkflow = async (workflowId: number) => {
    if (!confirm('Are you sure you want to execute this workflow?')) {
      return;
    }

    try {
      const result = await workflowService.execute(workflowId);

      // Show execution details modal
      setCurrentExecution(result);
      setIsExecutionModalOpen(true);

      // Also show summary alert
      if (result.status === 'success') {
        alert(`✅ Workflow executed successfully!\n\nNodes: ${result.nodes_executed}/${result.nodes_total}\nTime: ${result.execution_time_seconds?.toFixed(2)}s`);
      } else {
        alert(`❌ Workflow execution ${result.status}\n\nError: ${result.error_message || 'Unknown error'}`);
      }
    } catch (error: any) {
      console.error('Error executing workflow:', error);
      alert(error.response?.data?.detail || 'Failed to execute workflow');
    }
  };

  const deleteWorkflow = async (workflowId: number) => {
    if (!confirm('Are you sure you want to delete this workflow?')) {
      return;
    }

    try {
      await workflowService.delete(workflowId);
      alert('Workflow deleted successfully!');
      loadWorkflows();
    } catch (error) {
      console.error('Error deleting workflow:', error);
      alert('Failed to delete workflow');
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Workflows</h1>
        <Button onClick={() => openBuilder()}>
          <Plus className="mr-2 h-4 w-4" />
          Create Workflow
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {workflows.map((workflow) => (
          <div
            key={workflow.id}
            className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <h3 className="text-lg font-semibold mb-2">{workflow.name}</h3>
            <p className="text-sm text-gray-600 mb-3">{workflow.description}</p>
            <div className="text-xs text-gray-500 mb-3">
              Nodes: {workflow.workflow_data.nodes.length} | Connections:{' '}
              {workflow.workflow_data.connections.length}
            </div>
            <div className="flex space-x-2">
              <Button size="sm" onClick={() => openBuilder(workflow)}>
                Edit
              </Button>
              <Button
                size="sm"
                variant="secondary"
                onClick={() => executeWorkflow(workflow.id)}
              >
                <Play className="h-4 w-4" />
              </Button>
              <Button
                size="sm"
                variant="danger"
                onClick={() => deleteWorkflow(workflow.id)}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
            <div className="text-xs text-gray-400 mt-2">
              Updated: {formatDate(workflow.updated_at)}
            </div>
          </div>
        ))}
      </div>

      {workflows.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          No workflows found. Create one to get started!
        </div>
      )}

      {isBuilderOpen && (
        <div className="fixed inset-0 z-50 bg-white">
          <div className="h-full flex flex-col">
            <div className="bg-gray-100 p-4 border-b flex justify-between items-center">
              <div className="flex-1 max-w-md">
                <Input
                  placeholder="Workflow Name"
                  value={workflowName}
                  onChange={(e) => setWorkflowName(e.target.value)}
                  className="mb-2"
                />
                <Input
                  placeholder="Description"
                  value={workflowDescription}
                  onChange={(e) => setWorkflowDescription(e.target.value)}
                />
              </div>
              <div className="flex space-x-2">
                <Button onClick={addNode}>
                  <Plus className="mr-2 h-4 w-4" />
                  Add Node
                </Button>
                <Button onClick={saveWorkflow}>
                  <Save className="mr-2 h-4 w-4" />
                  Save
                </Button>
                <Button variant="outline" onClick={() => setIsBuilderOpen(false)}>
                  Close
                </Button>
              </div>
            </div>

            <div className="flex-1">
              <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                fitView
              >
                <Background />
                <Controls />
                <MiniMap />
              </ReactFlow>
            </div>
          </div>
        </div>
      )}

      <Modal
        isOpen={isNodeModalOpen}
        onClose={() => setIsNodeModalOpen(false)}
        title="Add Node"
      >
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Integration <span className="text-red-500">*</span>
            </label>
            <select
              value={nodeFormData.integration_id}
              onChange={(e) => handleIntegrationChange(e.target.value)}
              className="w-full h-10 px-3 border border-gray-300 rounded-md"
              required
            >
              <option value="">Select integration</option>
              {integrations.map((integration) => (
                <option key={integration.id} value={integration.id}>
                  {integration.name} ({integration.integration_type_name})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Task <span className="text-red-500">*</span>
            </label>
            {availableTasks.length > 0 ? (
              <>
                <select
                  value={nodeFormData.task}
                  onChange={(e) => handleTaskChange(e.target.value)}
                  className="w-full h-10 px-3 border border-gray-300 rounded-md"
                  required
                >
                  <option value="">Select task</option>
                  {availableTasks.map((task) => (
                    <option key={task.name} value={task.name}>
                      {task.display_name || task.name}
                    </option>
                  ))}
                </select>
                {selectedTask && selectedTask.description && (
                  <p className="text-xs text-gray-600 mt-1">
                    💡 {selectedTask.description}
                  </p>
                )}
              </>
            ) : (
              <>
                <Input
                  value={nodeFormData.task}
                  onChange={(e) => setNodeFormData({ ...nodeFormData, task: e.target.value })}
                  placeholder="e.g., send_notification, create_issue"
                  required
                />
                <p className="text-xs text-gray-500 mt-1">
                  ⚠️ This integration type has no defined tasks. Enter task name manually.
                </p>
              </>
            )}
          </div>

          {/* Dynamic Parameter Fields */}
          {selectedTask && selectedTask.parameters && selectedTask.parameters.length > 0 ? (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="block text-sm font-medium text-gray-700">
                  Task Parameters
                </label>
                <button
                  type="button"
                  onClick={() => setShowJsonEditor(!showJsonEditor)}
                  className="text-xs text-blue-600 hover:text-blue-700"
                >
                  {showJsonEditor ? '📝 Show Form' : '{ } Show JSON'}
                </button>
              </div>

              {!showJsonEditor ? (
                // Dynamic Form Fields
                <div className="space-y-3 p-4 bg-gray-50 rounded-lg border border-gray-200">
                  {selectedTask.parameters.map((param: any) => (
                    <div key={param.name}>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        {param.description || param.name}
                        {param.required && <span className="text-red-500 ml-1">*</span>}
                        <span className="text-xs text-gray-500 ml-2">({param.type})</span>
                      </label>

                      {param.type === 'boolean' ? (
                        <div className="flex items-center space-x-4">
                          <label className="flex items-center">
                            <input
                              type="radio"
                              name={param.name}
                              checked={nodeFormData.params[param.name] === true}
                              onChange={() => setNodeFormData({
                                ...nodeFormData,
                                params: { ...nodeFormData.params, [param.name]: true }
                              })}
                              className="mr-2"
                            />
                            <span className="text-sm">True</span>
                          </label>
                          <label className="flex items-center">
                            <input
                              type="radio"
                              name={param.name}
                              checked={nodeFormData.params[param.name] === false}
                              onChange={() => setNodeFormData({
                                ...nodeFormData,
                                params: { ...nodeFormData.params, [param.name]: false }
                              })}
                              className="mr-2"
                            />
                            <span className="text-sm">False</span>
                          </label>
                        </div>
                      ) : param.type === 'password' ? (
                        <input
                          type="password"
                          value={nodeFormData.params[param.name] || ''}
                          onChange={(e) => setNodeFormData({
                            ...nodeFormData,
                            params: { ...nodeFormData.params, [param.name]: e.target.value }
                          })}
                          placeholder={`Enter ${param.name}`}
                          required={param.required}
                          className="w-full h-10 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      ) : param.type === 'number' ? (
                        <input
                          type="number"
                          value={nodeFormData.params[param.name] || ''}
                          onChange={(e) => setNodeFormData({
                            ...nodeFormData,
                            params: { ...nodeFormData.params, [param.name]: parseFloat(e.target.value) || 0 }
                          })}
                          placeholder={`Enter ${param.name}`}
                          required={param.required}
                          className="w-full h-10 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      ) : (
                        <input
                          type="text"
                          value={nodeFormData.params[param.name] || ''}
                          onChange={(e) => setNodeFormData({
                            ...nodeFormData,
                            params: { ...nodeFormData.params, [param.name]: e.target.value }
                          })}
                          placeholder={`Enter ${param.name}`}
                          required={param.required}
                          className="w-full h-10 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      )}

                      {param.description && (
                        <p className="text-xs text-gray-500 mt-1">
                          {param.description}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                // JSON Editor (fallback)
                <div>
                  <div className="mb-2 p-2 bg-blue-50 border border-blue-200 rounded text-xs">
                    <div className="font-medium text-blue-900 mb-1">Parameter Schema:</div>
                    {selectedTask.parameters.map((param: any) => (
                      <div key={param.name} className="text-blue-800">
                        • <strong>{param.name}</strong> ({param.type}){param.required && <span className="text-red-600">*</span>}: {param.description}
                      </div>
                    ))}
                  </div>
                  <textarea
                    value={paramsText}
                    onChange={(e) => setParamsText(e.target.value)}
                    className="w-full h-32 px-3 py-2 border border-gray-300 rounded-md font-mono text-sm"
                    placeholder='{"key": "value"}'
                  />
                </div>
              )}
            </div>
          ) : nodeFormData.integration_id && !selectedTask ? (
            // No task selected or no parameters - show JSON editor
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Parameters (JSON) <span className="text-gray-500 text-xs">- Optional</span>
              </label>
              <textarea
                value={paramsText}
                onChange={(e) => setParamsText(e.target.value)}
                className="w-full h-32 px-3 py-2 border border-gray-300 rounded-md font-mono text-sm"
                placeholder='{"key": "value"} or leave as {}'
              />
              <p className="text-xs text-gray-500 mt-1">
                💡 Tip: Leave as <code>{'{}'}</code> if the task doesn't need parameters
              </p>
            </div>
          ) : null}

          <div className="flex justify-end space-x-2">
            <Button
              variant="outline"
              onClick={() => {
                setIsNodeModalOpen(false);
                setNodeFormData({ integration_id: '', task: '', params: {} });
                setParamsText('{}');
                setAvailableTasks([]);
                setSelectedTask(null);
              }}
            >
              Cancel
            </Button>
            <Button onClick={handleNodeSubmit}>Add Node</Button>
          </div>
        </div>
      </Modal>

      {/* Execution Details Modal */}
      <ExecutionModal
        isOpen={isExecutionModalOpen}
        onClose={() => setIsExecutionModalOpen(false)}
        execution={currentExecution}
      />
    </div>
  );
};