import React from 'react';
import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom';
import { IntegrationTypesPage } from './pages/IntegrationTypesPage';
import { IntegrationsPage } from './pages/IntegrationsPage';
import { WorkflowsPage } from './pages/WorkflowsPage';
import { ExecutionsPage } from './pages/ExecutionsPage';
import { Workflow, Network, Boxes, History } from 'lucide-react';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center">
                <h1 className="text-xl font-bold text-blue-600">Workflow Automation Platform</h1>
              </div>
              <div className="flex space-x-4">
                <NavLink to="/integration-types" icon={<Boxes className="h-4 w-4" />}>
                  Integration Types
                </NavLink>
                <NavLink to="/integrations" icon={<Network className="h-4 w-4" />}>
                  Integrations
                </NavLink>
                <NavLink to="/workflows" icon={<Workflow className="h-4 w-4" />}>
                  Workflows
                </NavLink>
                <NavLink to="/executions" icon={<History className="h-4 w-4" />}>
                  Executions
                </NavLink>
              </div>
            </div>
          </div>
        </nav>

        <main className="max-w-7xl mx-auto">
          <Routes>
            <Route path="/" element={<Navigate to="/integration-types" replace />} />
            <Route path="/integration-types" element={<IntegrationTypesPage />} />
            <Route path="/integrations" element={<IntegrationsPage />} />
            <Route path="/workflows" element={<WorkflowsPage />} />
            <Route path="/executions" element={<ExecutionsPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

interface NavLinkProps {
  to: string;
  icon: React.ReactNode;
  children: React.ReactNode;
}

const NavLink: React.FC<NavLinkProps> = ({ to, icon, children }) => {
  return (
    <Link
      to={to}
      className={({ isActive }: any) =>
        `flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive
          ? 'bg-blue-100 text-blue-700'
          : 'text-gray-700 hover:bg-gray-100'
        }`
      }
    >
      {icon}
      <span>{children}</span>
    </Link>
  );
};

export default App;