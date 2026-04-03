import React, { useEffect, useState } from 'react';
import { adminApi } from '../services/api';

/**
 * BenefitsPage — manage university-specific discount benefits.
 */
export default function BenefitsPage() {
  const [benefits, setBenefits] = useState([]);
  const [form, setForm] = useState({ title: '', partner_name: '', discount_percent: '', category: 'food' });

  useEffect(() => {
    adminApi.get('/benefits').then((res) => setBenefits(res.data)).catch(() => {});
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    const res = await adminApi.post('/admin/benefits', { ...form, discount_percent: Number(form.discount_percent) });
    setBenefits((prev) => [...prev, res.data]);
    setForm({ title: '', partner_name: '', discount_percent: '', category: 'food' });
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Benefits</h1>
      <form onSubmit={handleCreate} className="bg-white p-4 rounded-xl shadow mb-6 grid grid-cols-2 gap-4">
        <input className="input" placeholder="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
        <input className="input" placeholder="Partner Name" value={form.partner_name} onChange={(e) => setForm({ ...form, partner_name: e.target.value })} required />
        <input className="input" type="number" placeholder="Discount %" value={form.discount_percent} onChange={(e) => setForm({ ...form, discount_percent: e.target.value })} required />
        <select className="input" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
          {['food', 'transport', 'books', 'health', 'entertainment'].map((c) => <option key={c}>{c}</option>)}
        </select>
        <button type="submit" className="btn-primary col-span-2">Add Benefit</button>
      </form>
      <div className="grid grid-cols-3 gap-4">
        {benefits.map((b) => (
          <div key={b.id} className="bg-white rounded-xl shadow p-4">
            <h3 className="font-semibold">{b.title}</h3>
            <p className="text-sm text-gray-500">{b.partner_name}</p>
            <p className="text-blue-700 font-bold">{b.discount_percent}% OFF</p>
          </div>
        ))}
      </div>
    </div>
  );
}
