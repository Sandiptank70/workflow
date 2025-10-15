import React from 'react';
import { X, CheckCircle, XCircle, Clock, Zap } from 'lucide-react';
import { Button } from './Button';

interface NodeResult {
    node_id: string;
    task: string;
    integration_id: number;
    success: boolean;
    message: string;
    data: Record<string, any>;
    execution_time_seconds: number;
    timestamp: string;
}

interface ExecutionDetails {
    execution_id: number;
    workflow_id: number;
    workflow_name: string;
    status: string;
    started_at: string;
    completed_at: string | null;
    execution_time_seconds: number | null;
    nodes_executed: number;
    nodes_total: number;
    node_results: NodeResult[];
    error_message: string | null;
    trigger_source: string;
}

interface ExecutionModalProps {
    isOpen: boolean;
    onClose: () => void;
    execution: ExecutionDetails | null;
}

export const ExecutionModal: React.FC<ExecutionModalProps> = ({ isOpen, onClose, execution }) => {
    if (!isOpen || !execution) return null;

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'success':
                return 'text-green-600 bg-green-50';
            case 'failed':
                return 'text-red-600 bg-red-50';
            case 'running':
                return 'text-blue-600 bg-blue-50';
            default:
                return 'text-gray-600 bg-gray-50';
        }
    };

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'success':
                return <CheckCircle className="h-5 w-5 text-green-600" />;
            case 'failed':
                return <XCircle className="h-5 w-5 text-red-600" />;
            default:
                return <Clock className="h-5 w-5 text-blue-600" />;
        }
    };

    return (
        <div className="fixed inset-0 z-50 overflow-y-auto">
            <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
                {/* Background overlay */}
                <div
                    className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
                    onClick={onClose}
                />

                {/* Modal panel */}
                <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
                    {/* Header */}
                    <div className="bg-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
                        <div>
                            <h3 className="text-lg font-semibold text-gray-900">
                                Execution Details
                            </h3>
                            <p className="text-sm text-gray-600 mt-1">
                                {execution.workflow_name} • ID: {execution.execution_id}
                            </p>
                        </div>
                        <button
                            onClick={onClose}
                            className="text-gray-400 hover:text-gray-600 transition-colors"
                        >
                            <X className="h-6 w-6" />
                        </button>
                    </div>

                    {/* Content */}
                    <div className="px-6 py-4 max-h-[70vh] overflow-y-auto">
                        {/* Summary Section */}
                        <div className="mb-6">
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                {/* Status */}
                                <div className="bg-gray-50 p-4 rounded-lg">
                                    <div className="text-xs text-gray-600 mb-1">Status</div>
                                    <div className={`flex items-center space-x-2 font-semibold ${getStatusColor(execution.status)}`}>
                                        {getStatusIcon(execution.status)}
                                        <span className="capitalize">{execution.status}</span>
                                    </div>
                                </div>

                                {/* Execution Time */}
                                <div className="bg-gray-50 p-4 rounded-lg">
                                    <div className="text-xs text-gray-600 mb-1">Duration</div>
                                    <div className="flex items-center space-x-2">
                                        <Clock className="h-4 w-4 text-gray-600" />
                                        <span className="font-semibold">
                                            {execution.execution_time_seconds
                                                ? `${execution.execution_time_seconds.toFixed(2)}s`
                                                : 'N/A'}
                                        </span>
                                    </div>
                                </div>

                                {/* Nodes Progress */}
                                <div className="bg-gray-50 p-4 rounded-lg">
                                    <div className="text-xs text-gray-600 mb-1">Nodes</div>
                                    <div className="font-semibold">
                                        {execution.nodes_executed} / {execution.nodes_total}
                                    </div>
                                </div>

                                {/* Trigger Source */}
                                <div className="bg-gray-50 p-4 rounded-lg">
                                    <div className="text-xs text-gray-600 mb-1">Triggered By</div>
                                    <div className="flex items-center space-x-2">
                                        <Zap className="h-4 w-4 text-gray-600" />
                                        <span className="font-semibold text-sm">{execution.trigger_source}</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Timeline */}
                        <div className="mb-6">
                            <div className="flex justify-between text-sm text-gray-600">
                                <span>Started: {new Date(execution.started_at).toLocaleString()}</span>
                                {execution.completed_at && (
                                    <span>Completed: {new Date(execution.completed_at).toLocaleString()}</span>
                                )}
                            </div>
                        </div>

                        {/* Error Message */}
                        {execution.error_message && (
                            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                                <div className="flex items-start space-x-2">
                                    <XCircle className="h-5 w-5 text-red-600 mt-0.5" />
                                    <div>
                                        <div className="font-semibold text-red-900 mb-1">Error</div>
                                        <div className="text-sm text-red-700">{execution.error_message}</div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Node Results */}
                        <div>
                            <h4 className="text-sm font-semibold text-gray-900 mb-3">
                                Node Execution Details
                            </h4>
                            <div className="space-y-3">
                                {execution.node_results.map((node, index) => (
                                    <div
                                        key={node.node_id}
                                        className={`border rounded-lg p-4 ${node.success
                                            ? 'border-green-200 bg-green-50'
                                            : 'border-red-200 bg-red-50'
                                            }`}
                                    >
                                        {/* Node Header */}
                                        <div className="flex justify-between items-start mb-2">
                                            <div className="flex items-center space-x-2">
                                                <div className="flex items-center justify-center w-6 h-6 rounded-full bg-white text-xs font-semibold">
                                                    {index + 1}
                                                </div>
                                                <div>
                                                    <div className="font-semibold text-sm">
                                                        {node.task}
                                                    </div>
                                                    <div className="text-xs text-gray-600">
                                                        Integration ID: {node.integration_id}
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="flex items-center space-x-2">
                                                {node.success ? (
                                                    <CheckCircle className="h-5 w-5 text-green-600" />
                                                ) : (
                                                    <XCircle className="h-5 w-5 text-red-600" />
                                                )}
                                                <span className="text-xs text-gray-600">
                                                    {node.execution_time_seconds.toFixed(2)}s
                                                </span>
                                            </div>
                                        </div>

                                        {/* Node Message */}
                                        <div className="text-sm mb-2">
                                            <span className={node.success ? 'text-green-800' : 'text-red-800'}>
                                                {node.message}
                                            </span>
                                        </div>

                                        {/* Node Data */}
                                        {Object.keys(node.data).length > 0 && (
                                            <details className="mt-2">
                                                <summary className="text-xs text-gray-600 cursor-pointer hover:text-gray-800">
                                                    View Response Data
                                                </summary>
                                                <pre className="mt-2 p-2 bg-white rounded text-xs overflow-x-auto">
                                                    {JSON.stringify(node.data, null, 2)}
                                                </pre>
                                            </details>
                                        )}

                                        {/* Timestamp */}
                                        <div className="text-xs text-gray-500 mt-2">
                                            {new Date(node.timestamp).toLocaleString()}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Footer */}
                    <div className="bg-gray-50 px-6 py-4 border-t border-gray-200 flex justify-end">
                        <Button onClick={onClose}>Close</Button>
                    </div>
                </div>
            </div>
        </div>
    );
};