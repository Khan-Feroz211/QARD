import React, { useEffect, useState } from 'react';
import { adminApi } from '../services/api';

/**
 * StudentsPage — lists all students registered under the university tenant.
 */
export default function StudentsPage() {
  const [students, setStudents] = useState([]);

  useEffect(() => {
    adminApi.get('/admin/students').then((res) => setStudents(res.data)).catch(() => {});
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Students ({students.length})</h1>
      <div className="bg-white rounded-xl shadow overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-gray-500">
            <tr>
              <th className="px-4 py-3 text-left">Name</th>
              <th className="px-4 py-3 text-left">Email</th>
              <th className="px-4 py-3 text-left">Student ID</th>
              <th className="px-4 py-3 text-left">Plan</th>
              <th className="px-4 py-3 text-left">Verified</th>
            </tr>
          </thead>
          <tbody>
            {students.map((s) => (
              <tr key={s.id} className="border-t">
                <td className="px-4 py-3">{s.full_name}</td>
                <td className="px-4 py-3">{s.email}</td>
                <td className="px-4 py-3">{s.student_id}</td>
                <td className="px-4 py-3 capitalize">{s.plan}</td>
                <td className="px-4 py-3">{s.is_verified ? '✅' : '❌'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
