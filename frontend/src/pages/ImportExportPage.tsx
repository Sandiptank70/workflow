import React, { useState } from 'react';
import { Button } from '@/components/Button';
import { Download, Upload, FileJson, AlertCircle, CheckCircle2, Database, Workflow, Settings } from 'lucide-react';

export const ImportExportPage: React.FC = () => {
    const [importing, setImporting] = useState(false);
    const [exporting, setExporting] = useState(false);
    const [result, setResult] = useState<{ success: boolean; message: string } | null>(null);

    const exportData = async (type: 'all' | 'integration-types' | 'workflows') => {
        setExporting(true);
        setResult(null);

        try {
            const response = await fetch(`http://localhost:8000/api/import-export/export/${type}`);
            const data = await response.json();

            // Create download link
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${type}-${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            setResult({ success: true, message: `Successfully exported ${type}` });
        } catch (error) {
            setResult({ success: false, message: `Export failed: ${error}` });
        } finally {
            setExporting(false);
        }
    };

    const importData = async (type: 'all' | 'integration-types' | 'workflows', file: File) => {
        setImporting(true);
        setResult(null);

        try {
            const text = await file.text();
            const data = JSON.parse(text);

            const response = await fetch(`http://localhost:8000/api/import-export/import/${type}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (result.success || response.ok) {
                setResult({
                    success: true,
                    message: `Import completed! Imported: ${JSON.stringify(result)}`,
                });
            } else {
                setResult({ success: false, message: `Import failed: ${result.message}` });
            }
        } catch (error) {
            setResult({ success: false, message: `Import failed: ${error}` });
        } finally {
            setImporting(false);
        }
    };

    const handleFileUpload = (type: 'all' | 'integration-types' | 'workflows') => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        input.onchange = (e) => {
            const file = (e.target as HTMLInputElement).files?.[0];
            if (file) {
                importData(type, file);
            }
        };
        input.click();
    };

    return (
        <div className="p-6 max-w-6xl mx-auto">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900">Import / Export</h1>
                <p className="mt-2 text-gray-600">
                    Export your configuration to deploy in other environments, or import existing configurations
                </p>
            </div>

            {result && (
                <div
                    className={`mb-6 p-4 rounded-lg flex items-start gap-3 ${result.success ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
                        }`}
                >
                    {result.success ? (
                        <CheckCircle2 className="h-5 w-5 mt-0.5 flex-shrink-0" />
                    ) : (
                        <AlertCircle className="h-5 w-5 mt-0.5 flex-shrink-0" />
                    )}
                    <div className="flex-1">
                        <p className="font-medium">{result.success ? 'Success' : 'Error'}</p>
                        <p className="text-sm mt-1">{result.message}</p>
                    </div>
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Export All */}
                <div className="bg-white border border-gray-200 rounded-lg p-6">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="p-2 bg-blue-100 rounded-lg">
                            <Database className="h-6 w-6 text-blue-600" />
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-gray-900">Export All</h2>
                            <p className="text-sm text-gray-500">Complete configuration backup</p>
                        </div>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">
                        Export integration types, integrations, and workflows in one file
                    </p>
                    <Button
                        onClick={() => exportData('all')}
                        disabled={exporting}
                        className="w-full"
                    >
                        <Download className="h-4 w-4 mr-2" />
                        Export All Configuration
                    </Button>
                </div>

                {/* Import All */}
                <div className="bg-white border border-gray-200 rounded-lg p-6">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="p-2 bg-green-100 rounded-lg">
                            <Upload className="h-6 w-6 text-green-600" />
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-gray-900">Import All</h2>
                            <p className="text-sm text-gray-500">Restore complete backup</p>
                        </div>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">
                        Import integration types, integrations, and workflows from a JSON file
                    </p>
                    <Button
                        onClick={() => handleFileUpload('all')}
                        disabled={importing}
                        variant="secondary"
                        className="w-full"
                    >
                        <Upload className="h-4 w-4 mr-2" />
                        Import All Configuration
                    </Button>
                </div>

                {/* Export Integration Types */}
                <div className="bg-white border border-gray-200 rounded-lg p-6">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="p-2 bg-purple-100 rounded-lg">
                            <Settings className="h-6 w-6 text-purple-600" />
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-gray-900">Export Integration Types</h2>
                            <p className="text-sm text-gray-500">Types with tasks</p>
                        </div>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">
                        Export only integration type definitions and available tasks
                    </p>
                    <Button
                        onClick={() => exportData('integration-types')}
                        disabled={exporting}
                        className="w-full"
                    >
                        <Download className="h-4 w-4 mr-2" />
                        Export Types
                    </Button>
                </div>

                {/* Import Integration Types */}
                <div className="bg-white border border-gray-200 rounded-lg p-6">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="p-2 bg-purple-100 rounded-lg">
                            <Upload className="h-6 w-6 text-purple-600" />
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-gray-900">Import Integration Types</h2>
                            <p className="text-sm text-gray-500">Add new types</p>
                        </div>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">
                        Import integration types from a JSON file
                    </p>
                    <Button
                        onClick={() => handleFileUpload('integration-types')}
                        disabled={importing}
                        variant="secondary"
                        className="w-full"
                    >
                        <Upload className="h-4 w-4 mr-2" />
                        Import Types
                    </Button>
                </div>

                {/* Export Workflows */}
                <div className="bg-white border border-gray-200 rounded-lg p-6">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="p-2 bg-orange-100 rounded-lg">
                            <Workflow className="h-6 w-6 text-orange-600" />
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-gray-900">Export Workflows</h2>
                            <p className="text-sm text-gray-500">Share workflows</p>
                        </div>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">
                        Export workflow definitions to share with your team
                    </p>
                    <Button
                        onClick={() => exportData('workflows')}
                        disabled={exporting}
                        className="w-full"
                    >
                        <Download className="h-4 w-4 mr-2" />
                        Export Workflows
                    </Button>
                </div>

                {/* Import Workflows */}
                <div className="bg-white border border-gray-200 rounded-lg p-6">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="p-2 bg-orange-100 rounded-lg">
                            <Upload className="h-6 w-6 text-orange-600" />
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-gray-900">Import Workflows</h2>
                            <p className="text-sm text-gray-500">Load workflows</p>
                        </div>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">
                        Import workflow definitions from a JSON file
                    </p>
                    <Button
                        onClick={() => handleFileUpload('workflows')}
                        disabled={importing}
                        variant="secondary"
                        className="w-full"
                    >
                        <Upload className="h-4 w-4 mr-2" />
                        Import Workflows
                    </Button>
                </div>
            </div>

            {/* Information Section */}
            <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
                <h3 className="font-semibold text-blue-900 mb-2">ℹ️ Important Notes</h3>
                <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
                    <li>Credentials are NOT exported for security reasons</li>
                    <li>After importing, manually configure integration credentials</li>
                    <li>Exported files are in JSON format and can be version controlled</li>
                    <li>Use "skip_existing: true" in import files to avoid duplicates</li>
                </ul>
            </div>
        </div>
    );
};