import React, { useState, useEffect } from 'react';
import { Clock, CheckCircle, XCircle, Eye, RefreshCw, Calendar } from 'lucide-react';
import { Button } from './Button';
import { ExecutionModal } from './ExecutionModal';
import { workflowService } from '@/services/api';

interface ExecutionHistoryProps {
    workflowId?: number;
}

interface ExecutionLog {
    id: number;
    workflow_id: number;
    status: string;
    started_at: string;
    completed_at: string | null;
    execution_data: any;
    error_message: string | null;
}

export const ExecutionHistory: React.FC<ExecutionHistoryProps> = ({ workflowId }) => {
    const [executions, setExecutions] = useState<ExecutionLog[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedExecution, setSelectedExecution] = useState<any>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    useEffect(() => {
        loadExecutions();
    }, [workflowId]);

    const loadExecutions = async () => {
        setLoading(true);
        try {
            const data = workflowId
                ? await workflowService.getExecutions(workflowId)
                : await workflowService.getAllExecutions();
            setExecutions(data);
        } catch (error) {
            console.error('Error loading executions:', error);
        } finally {
            setLoading(false);
        }
    };

    const viewExecutionDetails = (execution: ExecutionLog) => {
        // Transform execution log to match ExecutionModal format
        const executionData = execution.execution_data || {};
        const nodeResults = executionData.node_results || [];
        const metadata = executionData.metadata || {};

        const executionTime = execution.completed_at && execution.started_at
            ? (new Date(execution.completed_at).getTime() - new Date(execution.started_at).getTime()) / 1000
            : null;

        const detailedExecution = {
            execution_id: execution.id,
            workflow_id: execution.workflow_id,
            workflow_name: `Workflow ${execution.workflow_id}`, // You can fetch actual name if needed
            status: execution.status,
            started_at: execution.started_at,
            completed_at: execution.completed_at,
            execution_time_seconds: executionTime,
            nodes_executed: executionData.nodes_executed || nodeResults.length,
            nodes_total: executionData.nodes_total || nodeResults.length,
            node_results: nodeResults,
            error_message: execution.error_message,
            trigger_source: metadata.trigger_source || 'unknown'
        };

        setSelectedExecution(detailedExecution);
        setIsModalOpen(true);
    };

    const getStatusBadge = (status: string) => {
        const badges = {
            success: {
                bg: 'bg-green-100',
                text: 'text-green-800',
                icon: <CheckCircle className="h-4 w-4" />
            },
            failed: {
                bg: 'bg-red-100',
                text: 'text-red-800',
                icon: <XCircle className="h-4 w-4" />
            },
            running: {
                bg: 'bg-blue-100',
                text: 'text-blue-800',
                icon: <RefreshCw className="h-4 w-4 animate-spin" />
            }
        };

        const badge = badges[status as keyof typeof badges] || badges.running;

        return (
            <span className={`inline-flex items-center space-x-1 px-3 py-1 rounded-full text-sm font-medium ${badge.bg} ${badge.text}`}>
                {badge.icon}
                <span className="capitalize">{status}</span>
            </span>
        );
    };

    const formatDuration = (started: string, completed: string | null) => {
        if (!completed) return 'In progress...';
        const start = new Date(started).getTime();
        const end = new Date(completed).getTime();
        const seconds = (end - start) / 1000;
        return `${seconds.toFixed(2)}s`;
    };

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleString();
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center py-12">
                <RefreshCw className="h-8 w-8 animate-spin text-blue-600" />
                <span className="ml-2 text-gray-600">Loading execution history...</span>
            </div>
        );
    }

    if (executions.length === 0) {
        return (
            <div className="text-center py-12">
                <Clock className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No execution history yet</p>
                <p className="text-sm text-gray-500 mt-2">Execute a workflow to see results here</p>
            </div>
        );
    }

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Execution History</h2>
                <Button variant="outline" onClick={loadExecutions}>
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Refresh
                </Button>
            </div>

            <div className="bg-white rounded-lg shadow overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    ID
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Status
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Started At
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Duration
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Nodes
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Trigger
                                </th>
                                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Actions
                                </th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {executions.map((execution) => {
                                const executionData = execution.execution_data || {};
                                const metadata = executionData.metadata || {};
                                const nodeResults = executionData.node_results || [];
                                const nodesExecuted = executionData.nodes_executed || nodeResults.length;
                                const nodesTotal = executionData.nodes_total || nodeResults.length;

                                return (
                                    <tr key={execution.id} className="hover:bg-gray-50">
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                            #{execution.id}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            {getStatusBadge(execution.status)}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                                            <div className="flex items-center space-x-2">
                                                <Calendar className="h-4 w-4 text-gray-400" />
                                                <span>{formatDate(execution.started_at)}</span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                                            <div className="flex items-center space-x-2">
                                                <Clock className="h-4 w-4 text-gray-400" />
                                                <span>{formatDuration(execution.started_at, execution.completed_at)}</span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                                            <span className="font-medium">{nodesExecuted}</span>
                                            <span className="text-gray-400"> / {nodesTotal}</span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                                            <span className="px-2 py-1 bg-gray-100 rounded text-xs font-mono">
                                                {metadata.trigger_source || 'manual'}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={() => viewExecutionDetails(execution)}
                                            >
                                                <Eye className="h-4 w-4 mr-1" />
                                                View Details
                                            </Button>
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Execution Details Modal */}
            <ExecutionModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                execution={selectedExecution}
            />
        </div>
    );
};