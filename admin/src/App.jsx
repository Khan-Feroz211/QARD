import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, NavLink } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import StudentsPage from './pages/StudentsPage';
import BenefitsPage from './pages/BenefitsPage';
import BrandingPage from './pages/BrandingPage';
import AnalyticsPage from './pages/AnalyticsPage';

/**
 * App — root component with routing for the QARD university admin portal.
 */
function AdminLayout({ children }) {
  return (
    <div className="flex min-h-screen bg-gray-100">
      <nav className="w-56 bg-white shadow-md flex flex-col p-4 gap-2">
        <h2 className="text-lg font-bold text-blue-700 mb-4">QARD Admin</h2>
        {[
          { to: '/dashboard', label: 'Dashboard' },
          { to: '/students', label: 'Students' },
          { to: '/benefits', label: 'Benefits' },
          { to: '/branding', label: 'Branding' },
          { to: '/analytics', label: 'Analytics' },
        ].map(({ to, label }) => (
          <NavLink key={to} to={to} className={({ isActive }) => `px-3 py-2 rounded-lg text-sm ${isActive ? 'bg-blue-50 text-blue-700 font-semibold' : 'text-gray-600 hover:bg-gray-50'}`}>
            {label}
          </NavLink>
        ))}
      </nav>
      <main className="flex-1 overflow-auto">{children}</main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<AdminLayout><DashboardPage /></AdminLayout>} />
        <Route path="/students" element={<AdminLayout><StudentsPage /></AdminLayout>} />
        <Route path="/benefits" element={<AdminLayout><BenefitsPage /></AdminLayout>} />
        <Route path="/branding" element={<AdminLayout><BrandingPage /></AdminLayout>} />
        <Route path="/analytics" element={<AdminLayout><AnalyticsPage /></AdminLayout>} />
      </Routes>
    </BrowserRouter>
  );
}
