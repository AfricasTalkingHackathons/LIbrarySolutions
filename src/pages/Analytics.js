import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  BookOpen, 
  Phone, 
  Calendar,
  Download,
  Filter,
  Activity
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer 
} from 'recharts';

const Analytics = () => {
  const [timeRange, setTimeRange] = useState('7d');
  const [selectedMetric, setSelectedMetric] = useState('all');

  // Sample data for charts
  const usageData = [
    { date: '2024-01-19', ussdSessions: 245, smsSent: 189, newUsers: 12 },
    { date: '2024-01-20', ussdSessions: 312, smsSent: 234, newUsers: 18 },
    { date: '2024-01-21', ussdSessions: 289, smsSent: 201, newUsers: 15 },
    { date: '2024-01-22', ussdSessions: 367, smsSent: 278, newUsers: 22 },
    { date: '2024-01-23', ussdSessions: 423, smsSent: 312, newUsers: 28 },
    { date: '2024-01-24', ussdSessions: 389, smsSent: 298, newUsers: 19 },
    { date: '2024-01-25', ussdSessions: 456, smsSent: 334, newUsers: 31 }
  ];

  const categoryData = [
    { name: 'Science', value: 35, color: '#3b82f6' },
    { name: 'Mathematics', value: 28, color: '#10b981' },
    { name: 'Language', value: 20, color: '#f59e0b' },
    { name: 'History', value: 10, color: '#8b5cf6' },
    { name: 'Geography', value: 7, color: '#ef4444' }
  ];

  const countyData = [
    { county: 'Nairobi', users: 3421, sessions: 15678 },
    { county: 'Mombasa', users: 2156, sessions: 9834 },
    { county: 'Kisumu', users: 1876, sessions: 7234 },
    { county: 'Nakuru', users: 1543, sessions: 5678 },
    { county: 'Kiambu', users: 1234, sessions: 4567 },
    { county: 'Eldoret', users: 987, sessions: 3456 }
  ];

  const featureUsage = [
    { feature: 'Book Search', usage: 4567, growth: 12.5 },
    { feature: 'Summary Request', usage: 3234, growth: 8.3 },
    { feature: 'Reservations', usage: 2156, growth: 15.7 },
    { feature: 'Revision Materials', usage: 1876, growth: 22.1 },
    { feature: 'Ask Librarian', usage: 1234, growth: 18.9 },
    { feature: 'STEM Guidance', usage: 987, growth: 31.2 }
  ];

  const stats = {
    totalUsers: 12543,
    activeUsers: 8934,
    totalSessions: 45678,
    booksReserved: 2341,
    avgSessionDuration: '4m 32s',
    satisfactionRate: '94.2%'
  };

  const timeRanges = [
    { value: '24h', label: 'Last 24 Hours' },
    { value: '7d', label: 'Last 7 Days' },
    { value: '30d', label: 'Last 30 Days' },
    { value: '90d', label: 'Last 90 Days' }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
          <p className="mt-2 text-gray-600">Track platform usage and performance metrics</p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-2">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="input"
          >
            {timeRanges.map(range => (
              <option key={range.value} value={range.value}>{range.label}</option>
            ))}
          </select>
          <button className="btn btn-outline px-4 py-2">
            <Download className="h-4 w-4 mr-2" />
            Export Report
          </button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <div className="card p-4">
          <div className="flex items-center justify-between mb-2">
            <Users className="h-5 w-5 text-blue-600" />
            <span className="text-xs text-green-600 font-medium">+12.5%</span>
          </div>
          <p className="text-2xl font-bold text-gray-900">{stats.totalUsers.toLocaleString()}</p>
          <p className="text-xs text-gray-600">Total Users</p>
        </div>

        <div className="card p-4">
          <div className="flex items-center justify-between mb-2">
            <Activity className="h-5 w-5 text-green-600" />
            <span className="text-xs text-green-600 font-medium">+8.3%</span>
          </div>
          <p className="text-2xl font-bold text-gray-900">{stats.activeUsers.toLocaleString()}</p>
          <p className="text-xs text-gray-600">Active Users</p>
        </div>

        <div className="card p-4">
          <div className="flex items-center justify-between mb-2">
            <Phone className="h-5 w-5 text-purple-600" />
            <span className="text-xs text-green-600 font-medium">+23.1%</span>
          </div>
          <p className="text-2xl font-bold text-gray-900">{stats.totalSessions.toLocaleString()}</p>
          <p className="text-xs text-gray-600">USSD Sessions</p>
        </div>

        <div className="card p-4">
          <div className="flex items-center justify-between mb-2">
            <BookOpen className="h-5 w-5 text-orange-600" />
            <span className="text-xs text-green-600 font-medium">+15.7%</span>
          </div>
          <p className="text-2xl font-bold text-gray-900">{stats.booksReserved.toLocaleString()}</p>
          <p className="text-xs text-gray-600">Books Reserved</p>
        </div>

        <div className="card p-4">
          <div className="flex items-center justify-between mb-2">
            <Clock className="h-5 w-5 text-indigo-600" />
            <span className="text-xs text-red-600 font-medium">-2.1%</span>
          </div>
          <p className="text-2xl font-bold text-gray-900">{stats.avgSessionDuration}</p>
          <p className="text-xs text-gray-600">Avg Session</p>
        </div>

        <div className="card p-4">
          <div className="flex items-center justify-between mb-2">
            <TrendingUp className="h-5 w-5 text-green-600" />
            <span className="text-xs text-green-600 font-medium">+3.2%</span>
          </div>
          <p className="text-2xl font-bold text-gray-900">{stats.satisfactionRate}</p>
          <p className="text-xs text-gray-600">Satisfaction</p>
        </div>
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Platform Usage Trends</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={usageData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="ussdSessions" stroke="#3b82f6" name="USSD Sessions" />
              <Line type="monotone" dataKey="smsSent" stroke="#10b981" name="SMS Sent" />
              <Line type="monotone" dataKey="newUsers" stroke="#f59e0b" name="New Users" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Book Categories Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Users by County</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={countyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="county" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="users" fill="#3b82f6" name="Users" />
              <Bar dataKey="sessions" fill="#10b981" name="Sessions" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Feature Usage</h3>
          <div className="space-y-3">
            {featureUsage.map((feature, index) => (
              <motion.div
                key={feature.feature}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium text-gray-900">{feature.feature}</span>
                    <span className="text-sm text-gray-600">{feature.usage.toLocaleString()}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${(feature.usage / 5000) * 100}%` }}
                      ></div>
                    </div>
                    <span className={`text-xs font-medium ${
                      feature.growth > 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {feature.growth > 0 ? '+' : ''}{feature.growth}%
                    </span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Activity Table */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity Log</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Time</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">User</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Activity</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Details</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              <tr className="hover:bg-gray-50">
                <td className="px-4 py-2 text-sm text-gray-600">2 mins ago</td>
                <td className="px-4 py-2 text-sm text-gray-900">John Kamau</td>
                <td className="px-4 py-2 text-sm text-gray-600">Book Search</td>
                <td className="px-4 py-2 text-sm text-gray-600">"Introduction to Physics"</td>
                <td className="px-4 py-2">
                  <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">Success</span>
                </td>
              </tr>
              <tr className="hover:bg-gray-50">
                <td className="px-4 py-2 text-sm text-gray-600">5 mins ago</td>
                <td className="px-4 py-2 text-sm text-gray-900">Jane Wanjiru</td>
                <td className="px-4 py-2 text-sm text-gray-600">Summary Request</td>
                <td className="px-4 py-2 text-sm text-gray-600">"Mathematics for Beginners"</td>
                <td className="px-4 py-2">
                  <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">Processing</span>
                </td>
              </tr>
              <tr className="hover:bg-gray-50">
                <td className="px-4 py-2 text-sm text-gray-600">12 mins ago</td>
                <td className="px-4 py-2 text-sm text-gray-900">Michael Ochieng</td>
                <td className="px-4 py-2 text-sm text-gray-600">Reservation</td>
                <td className="px-4 py-2 text-sm text-gray-600">"Chemistry Essentials"</td>
                <td className="px-4 py-2">
                  <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">Confirmed</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
