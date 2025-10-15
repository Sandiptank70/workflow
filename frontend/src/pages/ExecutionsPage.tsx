import React from 'react';
import { ExecutionHistory } from '@/components/ExecutionHistory';

export const ExecutionsPage: React.FC = () => {
    return (
        <div className="p-6 space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">Execution History</h1>
                <p className="mt-2 text-gray-600">
                    View all workflow executions with detailed logs and results
                </p>
            </div>

            <ExecutionHistory />
        </div>
    );
};