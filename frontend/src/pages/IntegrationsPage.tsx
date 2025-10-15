import React, { useState, useEffect } from 'react';
import { Plus, Trash2, CheckCircle, XCircle } from 'lucide-react';
import { Button } from '@/components/Button';
import { Input } from '@/components/Input';
import { Modal } from '@/components/Modal';
import { integrationService, integrationTypeService } from '@/services/api';
import type { Integration, IntegrationType } from '@/types';
import { formatDate } from '@/utils/helpers';

export const IntegrationsPage: React.FC = () => {
  const [integrations, setIntegrations] = useState<Integration[]>([]);
  const [integrationTypes, setIntegrationTypes] = useState<IntegrationType[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [testResult, setTestResult] = useState<any>(null);

  const [formData, setFormData] = useState({
    name: '',
    integration_type_id: '',
    credentials: {} as Record<string, any>,
  });

  const [selectedType, setSelectedType] = useState<IntegrationType | null>(null);

  useEffect(() => {
    loadIntegrations();
    loadIntegrationTypes();
  }, []);

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

  const handleTypeChange = (typeId: string) => {
    setFormData({ ...formData, integration_type_id: typeId, credentials: {} });
    const type = integrationTypes.find(t => t.id === parseInt(typeId));
    setSelectedType(type || null);
    setTestResult(null);
  };

  const handleCredentialChange = (paramName: string, value: any) => {
    setFormData({
      ...formData,
      credentials: {
        ...formData.credentials,
        [paramName]: value,
      },
    });
  };

  const handleTestConnection = async () => {
    if (!formData.integration_type_id) {
      alert('Please select an integration type');
      return;
    }

    setIsLoading(true);
    setTestResult(null);

    try {
      const result = await integrationService.test({
        integration_type_id: parseInt(formData.integration_type_id),
        credentials: formData.credentials,
      });
      setTestResult(result);
    } catch (error: any) {
      console.error('Error testing connection:', error);
      setTestResult({
        success: false,
        message: error.response?.data?.detail || 'Failed to test connection',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!testResult?.success) {
      alert('Please test the connection successfully before creating the integration');
      return;
    }

    setIsLoading(true);

    try {
      await integrationService.create({
        name: formData.name,
        integration_type_id: parseInt(formData.integration_type_id),
        credentials: formData.credentials,
      });

      alert('Integration created successfully!');
      setIsModalOpen(false);
      resetForm();
      loadIntegrations();
    } catch (error: any) {
      console.error('Error creating integration:', error);
      alert(error.response?.data?.detail || 'Failed to create integration');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this integration?')) {
      return;
    }

    try {
      await integrationService.delete(id);
      alert('Integration deleted successfully!');
      loadIntegrations();
    } catch (error) {
      console.error('Error deleting integration:', error);
      alert('Failed to delete integration');
    }
  };

  const resetForm = () => {
    setFormData({ name: '', integration_type_id: '', credentials: {} });
    setSelectedType(null);
    setTestResult(null);
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Integrations</h1>
        <Button onClick={() => setIsModalOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          Create Integration
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {integrations.map((integration) => (
          <div
            key={integration.id}
            className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-lg font-semibold">{integration.name}</h3>
              <button
                onClick={() => handleDelete(integration.id)}
                className="text-red-500 hover:text-red-700"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
            <p className="text-sm text-gray-600 mb-2">
              Type: <span className="font-medium">{integration.integration_type_name}</span>
            </p>
            <div className="flex items-center text-xs text-gray-500 mb-2">
              <span
                className={`inline-flex items-center px-2 py-1 rounded-full ${
                  integration.is_active
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                {integration.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
            <div className="text-xs text-gray-400">
              Created: {formatDate(integration.created_at)}
            </div>
          </div>
        ))}
      </div>

      {integrations.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          No integrations found. Create one to get started!
        </div>
      )}

      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          resetForm();
        }}
        title="Create Integration"
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Integration Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="e.g., My Jira Integration"
            required
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Integration Type <span className="text-red-500">*</span>
            </label>
            <select
              value={formData.integration_type_id}
              onChange={(e) => handleTypeChange(e.target.value)}
              className="w-full h-10 px-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="">Select integration type</option>
              {integrationTypes.map((type) => (
                <option key={type.id} value={type.id}>
                  {type.name}
                </option>
              ))}
            </select>
          </div>

          {selectedType && (
            <div className="space-y-3 border-t pt-4">
              <h4 className="font-medium">Credentials</h4>
              {selectedType.parameters.map((param) => (
                <Input
                  key={param.name}
                  label={param.name}
                  type={param.type === 'password' ? 'password' : 'text'}
                  value={formData.credentials[param.name] || ''}
                  onChange={(e) => handleCredentialChange(param.name, e.target.value)}
                  placeholder={param.description}
                  required={param.required}
                />
              ))}
            </div>
          )}

          {selectedType && (
            <div className="flex justify-between items-center pt-2">
              <Button
                type="button"
                variant="outline"
                onClick={handleTestConnection}
                disabled={isLoading}
              >
                {isLoading ? 'Testing...' : 'Test Connection'}
              </Button>
              {testResult && (
                <div
                  className={`flex items-center text-sm ${
                    testResult.success ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {testResult.success ? (
                    <CheckCircle className="h-4 w-4 mr-1" />
                  ) : (
                    <XCircle className="h-4 w-4 mr-1" />
                  )}
                  {testResult.message}
                </div>
              )}
            </div>
          )}

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
            <Button type="submit" disabled={isLoading || !testResult?.success}>
              {isLoading ? 'Creating...' : 'Create'}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
