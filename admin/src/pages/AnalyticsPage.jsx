import React, { useEffect, useState } from 'react';
import { adminApi } from '../services/api';

/**
 * AnalyticsPage — usage analytics dashboard for the university admin.
 */
export default function AnalyticsPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    adminApi.get('/admin/analytics').then((res) => setData(res.data)).catch(() => {});
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Analytics</h1>
      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white rounded-xl p-6 shadow">
          <p className="text-sm text-gray-500 mb-1">Registered Students</p>
          <p className="text-4xl font-bold text-blue-700">{data?.total_students ?? '—'}</p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow">
          <p className="text-sm text-gray-500 mb-1">Total Card Usages</p>
          <p className="text-4xl font-bold text-blue-700">{data?.total_usage_events ?? '—'}</p>
        </div>
      </div>
    </div>
  );
}
