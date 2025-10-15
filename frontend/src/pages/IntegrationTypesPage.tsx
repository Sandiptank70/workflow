import React, { useState, useEffect } from 'react';
import { Plus, Trash2 } from 'lucide-react';
import { Button } from '@/components/Button';
import { Input } from '@/components/Input';
import { Modal } from '@/components/Modal';
import { integrationTypeService } from '@/services/api';
import type { IntegrationType, Parameter } from '@/types';
import { formatDate } from '@/utils/helpers';

export const IntegrationTypesPage: React.FC = () => {
  const [integrationTypes, setIntegrationTypes] = useState<IntegrationType[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const [formData, setFormData] = useState({
    name: '',
    description: '',
  });
  
  const [parameters, setParameters] = useState<Parameter[]>([
    { name: '', type: 'string', required: true, description: '' },
  ]);

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await integrationTypeService.create({
        name: formData.name,
        description: formData.description,
        parameters: parameters.filter(p => p.name.trim() !== ''),
      });
      
      alert('Integration type created successfully!');
      setIsModalOpen(false);
      resetForm();
      loadIntegrationTypes();
    } catch (error: any) {
      console.error('Error creating integration type:', error);
      alert(error.response?.data?.detail || 'Failed to create integration type');
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({ name: '', description: '' });
    setParameters([{ name: '', type: 'string', required: true, description: '' }]);
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
            <h3 className="text-lg font-semibold mb-2">{type.name}</h3>
            <p className="text-sm text-gray-600 mb-3">{type.description}</p>
            <div className="text-xs text-gray-500 mb-2">
              <strong>Parameters:</strong> {type.parameters.length}
            </div>
            <div className="text-xs text-gray-400">
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
        title="Create Integration Type"
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="e.g., Jira, GitHub, AWS"
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

          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-medium text-gray-700">
                Parameters
              </label>
              <Button type="button" size="sm" onClick={addParameter}>
                <Plus className="h-4 w-4" />
              </Button>
            </div>

            <div className="space-y-3">
              {parameters.map((param, index) => (
                <div key={index} className="border border-gray-200 rounded-md p-3">
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

          <div className="flex justify-end space-x-2 pt-4">
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
              {isLoading ? 'Creating...' : 'Create'}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
