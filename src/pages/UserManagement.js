import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Plus, Edit, Trash2, Eye, Filter, Download, Mail, Phone, MapPin, Calendar } from 'lucide-react';

const UserManagement = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCounty, setSelectedCounty] = useState('all');
  const [showAddModal, setShowAddModal] = useState(false);

  const users = [
    {
      id: 1,
      name: 'John Kamau',
      phone: '+254712345678',
      email: 'john.kamau@email.com',
      county: 'Nairobi',
      registrationDate: '2024-01-15',
      lastActive: '2024-01-25',
      totalReservations: 5,
      activeReservations: 2,
      status: 'active'
    },
    {
      id: 2,
      name: 'Jane Wanjiru',
      phone: '+254723456789',
      email: 'jane.wanjiru@email.com',
      county: 'Mombasa',
      registrationDate: '2024-01-10',
      lastActive: '2024-01-24',
      totalReservations: 8,
      activeReservations: 1,
      status: 'active'
    },
    {
      id: 3,
      name: 'Michael Ochieng',
      phone: '+254734567890',
      email: 'michael.o@email.com',
      county: 'Kisumu',
      registrationDate: '2024-01-20',
      lastActive: '2024-01-18',
      totalReservations: 3,
      activeReservations: 0,
      status: 'inactive'
    },
    {
      id: 4,
      name: 'Sarah Achieng',
      phone: '+254745678901',
      email: 'sarah.achieng@email.com',
      county: 'Nakuru',
      registrationDate: '2024-01-12',
      lastActive: '2024-01-25',
      totalReservations: 12,
      activeReservations: 3,
      status: 'active'
    },
    {
      id: 5,
      name: 'David Mutua',
      phone: '+254756789012',
      email: 'david.mutua@email.com',
      county: 'Kiambu',
      registrationDate: '2024-01-18',
      lastActive: '2024-01-22',
      totalReservations: 6,
      activeReservations: 1,
      status: 'active'
    }
  ];

  const counties = ['all', 'Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Kiambu', 'Eldoret', 'Thika'];

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.phone.includes(searchTerm) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCounty = selectedCounty === 'all' || user.county === selectedCounty;
    return matchesSearch && matchesCounty;
  });

  const stats = {
    total: users.length,
    active: users.filter(u => u.status === 'active').length,
    newThisMonth: 3,
    totalReservations: users.reduce((acc, u) => acc + u.totalReservations, 0)
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">User Management</h1>
          <p className="mt-2 text-gray-600">Manage library users and accounts</p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-2">
          <button className="btn btn-outline px-4 py-2">
            <Download className="h-4 w-4 mr-2" />
            Export Users
          </button>
          <button 
            onClick={() => setShowAddModal(true)}
            className="btn btn-primary px-4 py-2"
          >
            <Plus className="h-4 w-4 mr-2" />
            Add User
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Users</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            </div>
            <div className="bg-blue-50 p-2 rounded-lg">
              <div className="w-6 h-6 bg-blue-500 rounded-full"></div>
            </div>
          </div>
        </div>
        
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Active Users</p>
              <p className="text-2xl font-bold text-green-600">{stats.active}</p>
            </div>
            <div className="bg-green-50 p-2 rounded-lg">
              <div className="w-6 h-6 bg-green-500 rounded-full"></div>
            </div>
          </div>
        </div>
        
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">New This Month</p>
              <p className="text-2xl font-bold text-purple-600">{stats.newThisMonth}</p>
            </div>
            <div className="bg-purple-50 p-2 rounded-lg">
              <div className="w-6 h-6 bg-purple-500 rounded-full"></div>
            </div>
          </div>
        </div>
        
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Reservations</p>
              <p className="text-2xl font-bold text-orange-600">{stats.totalReservations}</p>
            </div>
            <div className="bg-orange-50 p-2 rounded-lg">
              <div className="w-6 h-6 bg-orange-500 rounded-full"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="card p-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search by name, phone, or email..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input pl-10"
              />
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Filter className="h-4 w-4 text-gray-400" />
            <select
              value={selectedCounty}
              onChange={(e) => setSelectedCounty(e.target.value)}
              className="input"
            >
              {counties.map(county => (
                <option key={county} value={county}>
                  {county === 'all' ? 'All Counties' : county}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Users Table */}
      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  User Details
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Contact
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Location
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Activity
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredUsers.map((user, index) => (
                <motion.tr
                  key={user.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                  className="hover:bg-gray-50"
                >
                  <td className="px-6 py-4">
                    <div>
                      <div className="text-sm font-medium text-gray-900">{user.name}</div>
                      <div className="text-sm text-gray-500">ID: USR{user.id.toString().padStart(4, '0')}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="space-y-1">
                      <div className="flex items-center text-sm text-gray-600">
                        <Phone className="h-3 w-3 mr-1" />
                        {user.phone}
                      </div>
                      <div className="flex items-center text-sm text-gray-600">
                        <Mail className="h-3 w-3 mr-1" />
                        {user.email}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center text-sm text-gray-600">
                      <MapPin className="h-3 w-3 mr-1" />
                      {user.county}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="space-y-1">
                      <div className="text-sm text-gray-600">
                        <span className="font-medium">{user.totalReservations}</span> total reservations
                      </div>
                      <div className="text-sm text-gray-600">
                        <span className="font-medium">{user.activeReservations}</span> active
                      </div>
                      <div className="text-xs text-gray-400">
                        Last active: {user.lastActive}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      user.status === 'active' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {user.status}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-2">
                      <button className="text-blue-600 hover:text-blue-800">
                        <Eye className="h-4 w-4" />
                      </button>
                      <button className="text-green-600 hover:text-green-800">
                        <Edit className="h-4 w-4" />
                      </button>
                      <button className="text-red-600 hover:text-red-800">
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add User Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto"
          >
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Add New User</h2>
              <button
                onClick={() => setShowAddModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ×
              </button>
            </div>
            
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                  <input type="text" className="input" placeholder="John Kamau" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                  <input type="tel" className="input" placeholder="+254712345678" />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input type="email" className="input" placeholder="john.kamau@email.com" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">County</label>
                  <select className="input">
                    <option>Select county</option>
                    {counties.filter(c => c !== 'all').map(county => (
                      <option key={county} value={county}>{county}</option>
                    ))}
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                <select className="input">
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                </select>
              </div>
            </div>
            
            <div className="flex justify-end space-x-2 mt-6">
              <button
                onClick={() => setShowAddModal(false)}
                className="btn btn-outline px-4 py-2"
              >
                Cancel
              </button>
              <button className="btn btn-primary px-4 py-2">
                Add User
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default UserManagement;
