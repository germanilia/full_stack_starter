import React, { useEffect, useState } from 'react';
import { api } from '@/lib/api';

export default function StatusComponent() {
  const [status, setStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        setLoading(true);
        const data = await api.getHealth();
        setStatus(data.status);
      } catch (err) {
        setError('Failed to connect to API');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    checkHealth();
  }, []);

  return (
    <div className="mb-6 p-4 border rounded-md">
      <h2 className="text-lg font-medium mb-2">API Status</h2>
      {loading ? (
        <p>Checking connection...</p>
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : (
        <p className="text-green-500">Backend API is {status}</p>
      )}
    </div>
  );
}