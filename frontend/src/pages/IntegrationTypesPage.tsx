import React, { useState, useEffect } from 'react';
import { Plus, Trash2, Edit, Wrench } from 'lucide-react';
import { Button } from '@/components/Button';
import { Input } from '@/components/Input';
import { Modal } from '@/components/Modal';
import { integrationTypeService } from '@/services/api';
import type { IntegrationType, Parameter } from '@/types';
import { formatDate } from '@/utils/helpers';

interface Task {
  name: string;
  display_name: string;
  description: string;
  parameters: Parameter[];
}

export const IntegrationTypesPage: React.FC = () => {
  const [integrationTypes, setIntegrationTypes] = useState<IntegrationType[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [editingType, setEditingType] = useState<IntegrationType | null>(null);

  const [formData, setFormData] = useState({
    name: '',
    description: '',
  });

  const [parameters, setParameters] = useState<Parameter[]>([
    { name: '', type: 'string', required: true, description: '' },
  ]);

  const [tasks, setTasks] = useState<Task[]>([]);
  const [showTasksSection, setShowTasksSection] = useState(false);

  useEffect(() => {
    loadIntegrationTypes();
  }, []);

  const loadIntegrationTypes = async () => {
    try {
      const data = await integrationTypeService.getAll();
      setIntegrationTypes(data);
    } catch (error) {
      console.error('Error loading integration types:', error);
      alert('Failed to load integration types');
    }
  };

  const handleEdit = (type: IntegrationType) => {
    setEditingType(type);
    setFormData({
      name: type.name,
      description: type.description,
    });
    setParameters(type.parameters.length > 0 ? type.parameters : [{ name: '', type: 'string', required: true, description: '' }]);
    setTasks(type.tasks || []);
    setShowTasksSection((type.tasks || []).length > 0);
    setIsModalOpen(true);
  };

  const handleDelete = async (id: number, name: string) => {
    if (!window.confirm(`Are you sure you want to delete "${name}"? This cannot be undone.`)) {
      return;
    }

    try {
      await integrationTypeService.delete(id);
      alert('Integration type deleted successfully!');
      loadIntegrationTypes();
    } catch (error: any) {
      console.error('Error deleting integration type:', error);
      alert(error.response?.data?.detail || 'Failed to delete integration type');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const data = {
        name: formData.name,
        description: formData.description,
        parameters: parameters.filter(p => p.name.trim() !== ''),
        tasks: tasks.filter(t => t.name.trim() !== ''),
      };

      if (editingType) {
        await integrationTypeService.update(editingType.id, data);
        alert('Integration type updated successfully!');
      } else {
        await integrationTypeService.create(data);
        alert('Integration type created successfully!');
      }

      setIsModalOpen(false);
      resetForm();
      loadIntegrationTypes();
    } catch (error: any) {
      console.error('Error saving integration type:', error);
      alert(error.response?.data?.detail || 'Failed to save integration type');
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setEditingType(null);
    setFormData({ name: '', description: '' });
    setParameters([{ name: '', type: 'string', required: true, description: '' }]);
    setTasks([]);
    setShowTasksSection(false);
  };

  const addParameter = () => {
    setParameters([...parameters, { name: '', type: 'string', required: true, description: '' }]);
  };

  const updateParameter = (index: number, field: keyof Parameter, value: any) => {
    const newParameters = [...parameters];
    newParameters[index] = { ...newParameters[index], [field]: value };
    setParameters(newParameters);
  };

  const removeParameter = (index: number) => {
    setParameters(parameters.filter((_, i) => i !== index));
  };

  const addTask = () => {
    setTasks([...tasks, {
      name: '',
      display_name: '',
      description: '',
      parameters: []
    }]);
  };

  const updateTask = (index: number, field: keyof Task, value: any) => {
    const newTasks = [...tasks];
    newTasks[index] = { ...newTasks[index], [field]: value };
    setTasks(newTasks);
  };

  const removeTask = (index: number) => {
    setTasks(tasks.filter((_, i) => i !== index));
  };

  const addTaskParameter = (taskIndex: number) => {
    const newTasks = [...tasks];
    newTasks[taskIndex].parameters.push({
      name: '',
      type: 'string',
      required: true,
      description: ''
    });
    setTasks(newTasks);
  };

  const updateTaskParameter = (taskIndex: number, paramIndex: number, field: keyof Parameter, value: any) => {
    const newTasks = [...tasks];
    newTasks[taskIndex].parameters[paramIndex] = {
      ...newTasks[taskIndex].parameters[paramIndex],
      [field]: value
    };
    setTasks(newTasks);
  };

  const removeTaskParameter = (taskIndex: number, paramIndex: number) => {
    const newTasks = [...tasks];
    newTasks[taskIndex].parameters = newTasks[taskIndex].parameters.filter((_, i) => i !== paramIndex);
    setTasks(newTasks);
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Integration Types</h1>
        <Button onClick={() => setIsModalOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          Create Integration Type
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {integrationTypes.map((type) => (
          <div
            key={type.id}
            className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between mb-2">
              <h3 className="text-lg font-semibold">{type.name}</h3>
              <div className="flex gap-1">
                <button
                  onClick={() => handleEdit(type)}
                  className="p-1 text-blue-600 hover:bg-blue-50 rounded"
                  title="Edit"
                >
                  <Edit className="h-4 w-4" />
                </button>
                <button
                  onClick={() => handleDelete(type.id, type.name)}
                  className="p-1 text-red-600 hover:bg-red-50 rounded"
                  title="Delete"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
            <p className="text-sm text-gray-600 mb-3">{type.description}</p>
            <div className="space-y-1 text-xs text-gray-500 mb-2">
              <div><strong>Parameters:</strong> {type.parameters.length}</div>
              {type.tasks && type.tasks.length > 0 && (
                <div><strong>Tasks:</strong> {type.tasks.length}</div>
              )}
            </div>
            {type.tasks && type.tasks.length > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-100">
                <div className="text-xs font-medium text-gray-600 mb-2">Available Tasks:</div>
                <div className="space-y-1">
                  {type.tasks.map((task: any, idx: number) => (
                    <div key={idx} className="text-xs text-gray-500 flex items-start gap-1">
                      <Wrench className="h-3 w-3 mt-0.5 flex-shrink-0" />
                      <span>{task.display_name || task.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            <div className="text-xs text-gray-400 mt-3">
              Created: {formatDate(type.created_at)}
            </div>
          </div>
        ))}
      </div>

      {integrationTypes.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          No integration types found. Create one to get started!
        </div>
      )}

      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          resetForm();
        }}
        title={editingType ? "Edit Integration Type" : "Create Integration Type"}
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4 max-h-[70vh] overflow-y-auto px-1">
          <Input
            label="Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="e.g., Teams, Jira, GitHub"
            required
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="w-full h-20 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Description of this integration type"
            />
          </div>

          {/* Parameters Section */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-medium text-gray-700">
                Credentials Parameters
              </label>
              <Button type="button" size="sm" onClick={addParameter}>
                <Plus className="h-4 w-4" />
              </Button>
            </div>

            <div className="space-y-3">
              {parameters.map((param, index) => (
                <div key={index} className="border border-gray-200 rounded-md p-3 bg-gray-50">
                  <div className="grid grid-cols-2 gap-2 mb-2">
                    <Input
                      placeholder="Parameter name"
                      value={param.name}
                      onChange={(e) => updateParameter(index, 'name', e.target.value)}
                      required
                    />
                    <select
                      value={param.type}
                      onChange={(e) => updateParameter(index, 'type', e.target.value)}
                      className="h-10 px-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="string">String</option>
                      <option value="number">Number</option>
                      <option value="boolean">Boolean</option>
                      <option value="password">Password</option>
                    </select>
                  </div>
                  <Input
                    placeholder="Description"
                    value={param.description}
                    onChange={(e) => updateParameter(index, 'description', e.target.value)}
                  />
                  <div className="flex items-center justify-between mt-2">
                    <label className="flex items-center text-sm">
                      <input
                        type="checkbox"
                        checked={param.required}
                        onChange={(e) => updateParameter(index, 'required', e.target.checked)}
                        className="mr-2"
                      />
                      Required
                    </label>
                    {parameters.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeParameter(index)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Tasks Section */}
          <div className="border-t pt-4">
            <div className="flex items-center justify-between mb-3">
              <label className="block text-sm font-medium text-gray-700">
                Available Tasks (Optional)
              </label>
              <Button
                type="button"
                size="sm"
                variant="secondary"
                onClick={() => setShowTasksSection(!showTasksSection)}
              >
                {showTasksSection ? 'Hide Tasks' : 'Add Tasks'}
              </Button>
            </div>

            {showTasksSection && (
              <>
                <p className="text-sm text-gray-500 mb-3">
                  Define tasks that can be performed with this integration type.
                  These will show as human-readable options when building workflows.
                </p>

                <div className="space-y-4">
                  {tasks.map((task, taskIndex) => (
                    <div key={taskIndex} className="border-2 border-blue-200 rounded-md p-4 bg-blue-50">
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="text-sm font-semibold text-blue-900">Task {taskIndex + 1}</h4>
                        <button
                          type="button"
                          onClick={() => removeTask(taskIndex)}
                          className="text-red-500 hover:text-red-700"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>

                      <div className="space-y-2 mb-3">
                        <Input
                          placeholder="Function name (e.g., send_notification)"
                          value={task.name}
                          onChange={(e) => updateTask(taskIndex, 'name', e.target.value)}
                          required={tasks.length > 0}
                        />
                        <Input
                          placeholder="Display name (e.g., Send Notification)"
                          value={task.display_name}
                          onChange={(e) => updateTask(taskIndex, 'display_name', e.target.value)}
                          required={tasks.length > 0}
                        />
                        <textarea
                          placeholder="Task description"
                          value={task.description}
                          onChange={(e) => updateTask(taskIndex, 'description', e.target.value)}
                          className="w-full h-16 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                        />
                      </div>

                      {/* Task Parameters */}
                      <div className="border-t border-blue-200 pt-3">
                        <div className="flex items-center justify-between mb-2">
                          <label className="text-xs font-medium text-gray-700">
                            Task Parameters
                          </label>
                          <button
                            type="button"
                            onClick={() => addTaskParameter(taskIndex)}
                            className="text-xs text-blue-600 hover:text-blue-700"
                          >
                            + Add Parameter
                          </button>
                        </div>

                        {task.parameters.map((param, paramIndex) => (
                          <div key={paramIndex} className="bg-white rounded p-2 mb-2">
                            <div className="grid grid-cols-2 gap-1 mb-1">
                              <input
                                type="text"
                                placeholder="Param name"
                                value={param.name}
                                onChange={(e) => updateTaskParameter(taskIndex, paramIndex, 'name', e.target.value)}
                                className="h-8 px-2 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                              />
                              <select
                                value={param.type}
                                onChange={(e) => updateTaskParameter(taskIndex, paramIndex, 'type', e.target.value)}
                                className="h-8 px-2 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                              >
                                <option value="string">String</option>
                                <option value="number">Number</option>
                                <option value="boolean">Boolean</option>
                              </select>
                            </div>
                            <input
                              type="text"
                              placeholder="Description"
                              value={param.description}
                              onChange={(e) => updateTaskParameter(taskIndex, paramIndex, 'description', e.target.value)}
                              className="w-full h-8 px-2 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 mb-1"
                            />
                            <div className="flex items-center justify-between">
                              <label className="flex items-center text-xs">
                                <input
                                  type="checkbox"
                                  checked={param.required}
                                  onChange={(e) => updateTaskParameter(taskIndex, paramIndex, 'required', e.target.checked)}
                                  className="mr-1"
                                />
                                Required
                              </label>
                              <button
                                type="button"
                                onClick={() => removeTaskParameter(taskIndex, paramIndex)}
                                className="text-red-500 hover:text-red-700"
                              >
                                <Trash2 className="h-3 w-3" />
                              </button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}

                  <Button
                    type="button"
                    variant="outline"
                    onClick={addTask}
                    className="w-full"
                  >
                    <Plus className="h-4 w-4 mr-2" />
                    Add Task
                  </Button>
                </div>
              </>
            )}
          </div>

          <div className="flex justify-end space-x-2 pt-4 border-t">
            <Button
              type="button"
              variant="outline"
              onClick={() => {
                setIsModalOpen(false);
                resetForm();
              }}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? 'Saving...' : (editingType ? 'Update' : 'Create')}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
