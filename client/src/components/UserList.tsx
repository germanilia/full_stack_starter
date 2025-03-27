import { useEffect, useState } from 'react';
import { api } from '@/lib/api';

interface User {
  id: number;
  username: string;
  email: string;
  full_name: string | null;
  is_active: boolean;
}

export default function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setLoading(true);
        const data = await api.getUsers();
        setUsers(data);
      } catch (err) {
        setError('Failed to fetch users. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) {
    return <div className="text-center">Loading users...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div className="max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-4">Users</h2>
      <div className="space-y-4">
        {users.map((user) => (
          <div 
            key={user.id}
            className="border p-4 rounded-md shadow-sm hover:shadow-md transition"
          >
            <h3 className="font-bold">{user.full_name || user.username}</h3>
            <p className="text-gray-600">{user.email}</p>
            <p className="text-sm mt-2">
              Status: <span className={user.is_active ? "text-green-500" : "text-red-500"}>
                {user.is_active ? "Active" : "Inactive"}
              </span>
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}