import React, { useEffect, useState } from 'react';
import { adminApi } from '../services/api';

/**
 * DashboardPage — overview of tenant statistics and quick actions.
 */
export default function DashboardPage() {
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    adminApi.get('/admin/analytics').then((res) => setAnalytics(res.data)).catch(() => {});
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Dashboard</h1>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white rounded-xl p-6 shadow">
          <p className="text-sm text-gray-500">Total Students</p>
          <p className="text-3xl font-bold text-blue-700">{analytics?.total_students ?? '—'}</p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow">
          <p className="text-sm text-gray-500">Total Usage Events</p>
          <p className="text-3xl font-bold text-blue-700">{analytics?.total_usage_events ?? '—'}</p>
        </div>
      </div>
    </div>
  );
}
