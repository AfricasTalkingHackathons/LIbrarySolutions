import { useState } from 'react';
import { Search, Phone, MapPin, Calendar } from 'lucide-react';
import { mockUsers } from '../data/mockData';

export default function UsersPage() {
  const [search, setSearch] = useState('');

  const filtered = mockUsers.filter(
    (user) =>
      user.name.toLowerCase().includes(search.toLowerCase()) ||
      user.phone_number.includes(search) ||
      user.county.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-gray-900 font-heading tracking-tight">Users</h1>
        <p className="text-sm text-gray-400 mt-2">Registered MaktabaAI users across East Africa.</p>
      </div>

      {/* Search */}
      <div className="relative max-w-md">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          type="text"
          placeholder="Search by name, phone, or county..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-10 pr-4 py-3 bg-white border border-gray-200 rounded-xl text-sm focus:outline-none focus:border-teal focus:ring-2 focus:ring-teal/10 transition-all"
        />
      </div>

      {/* Users Table */}
      <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-cream/50">
                <th className="text-left px-5 py-3 font-medium text-gray-500">Name</th>
                <th className="text-left px-5 py-3 font-medium text-gray-500">Phone</th>
                <th className="text-left px-5 py-3 font-medium text-gray-500">Location</th>
                <th className="text-left px-5 py-3 font-medium text-gray-500">Joined</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((user) => (
                <tr key={user.id} className="border-t border-gray-50 hover:bg-cream/30 transition-colors">
                  <td className="px-5 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-teal/10 rounded-full flex items-center justify-center text-teal font-semibold text-sm">
                        {user.name.charAt(0)}
                      </div>
                      <span className="font-medium text-gray-900">{user.name}</span>
                    </div>
                  </td>
                  <td className="px-5 py-4">
                    <div className="flex items-center gap-2 text-gray-600">
                      <Phone className="w-4 h-4 text-gray-400" />
                      {user.phone_number}
                    </div>
                  </td>
                  <td className="px-5 py-4">
                    <div className="flex items-center gap-2 text-gray-600">
                      <MapPin className="w-4 h-4 text-gray-400" />
                      {user.county}
                    </div>
                  </td>
                  <td className="px-5 py-4">
                    <div className="flex items-center gap-2 text-gray-500">
                      <Calendar className="w-4 h-4 text-gray-400" />
                      {user.created_at}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-400">No users found matching your search.</p>
        </div>
      )}
    </div>
  );
}
