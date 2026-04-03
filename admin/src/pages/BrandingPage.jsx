import React, { useState } from 'react';
import { adminApi } from '../services/api';

/**
 * BrandingPage — update university colors and logo for the student card.
 */
export default function BrandingPage() {
  const [primaryColor, setPrimaryColor] = useState('#1A56DB');
  const [logoUrl, setLogoUrl] = useState('');
  const [message, setMessage] = useState('');

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      await adminApi.put('/admin/branding', null, { params: { primary_color: primaryColor, logo_url: logoUrl } });
      setMessage('Branding updated successfully!');
    } catch {
      setMessage('Failed to update branding.');
    }
  };

  return (
    <div className="p-6 max-w-lg">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">University Branding</h1>
      {message && <p className="mb-4 text-green-600 text-sm">{message}</p>}
      <form onSubmit={handleSave} className="bg-white rounded-xl shadow p-6 space-y-4">
        <div>
          <label className="block text-sm text-gray-600 mb-1">Primary Color</label>
          <div className="flex gap-3 items-center">
            <input type="color" value={primaryColor} onChange={(e) => setPrimaryColor(e.target.value)} className="h-10 w-16 rounded cursor-pointer" />
            <span className="text-sm text-gray-500">{primaryColor}</span>
          </div>
        </div>
        <div>
          <label className="block text-sm text-gray-600 mb-1">Logo URL</label>
          <input className="input w-full" placeholder="https://..." value={logoUrl} onChange={(e) => setLogoUrl(e.target.value)} />
        </div>
        <button type="submit" className="btn-primary w-full">Save Branding</button>
      </form>
    </div>
  );
}
