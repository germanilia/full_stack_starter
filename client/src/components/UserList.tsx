import { useEffect, useState } from 'react';
import { api } from '@/lib/api';

interface User {
  id: number;
  username: string;
  email: string;
  full_name: string | null;
  is_active: boolean;
  role: string;
  cognito_sub: string | null;
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
    <div className="w-full">
      <h2 className="text-xl font-bold mb-4">Users</h2>
      <div className="space-y-4">
        {users.map((user) => (
          <div
            key={user.id}
            className="border p-4 rounded-md shadow-sm hover:shadow-md transition bg-white"
          >
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h3 className="font-bold">{user.full_name || user.username}</h3>
                <p className="text-gray-600">{user.email}</p>
                <div className="flex items-center gap-4 mt-2">
                  <span className="text-sm">
                    Status: <span className={user.is_active ? "text-green-500" : "text-red-500"}>
                      {user.is_active ? "Active" : "Inactive"}
                    </span>
                  </span>
                  <span className="text-sm">
                    Role: <span className="capitalize font-medium text-blue-600">
                      {user.role}
                    </span>
                  </span>
                </div>
              </div>
              {user.role === 'admin' && (
                <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full">
                  Admin
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}