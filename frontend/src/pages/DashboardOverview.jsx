import { BookOpen, Users, CalendarCheck, MessageSquare, BarChart3, TrendingUp } from 'lucide-react';
import { mockStats, mockReservations, mockBooks, mockUsers } from '../data/mockData';

const statCards = [
  { label: 'Total Users', value: mockStats.totalUsers, icon: Users, color: 'teal', change: '+12%' },
  { label: 'Total Books', value: mockStats.totalBooks, icon: BookOpen, color: 'sage', change: '+3' },
  { label: 'Active Reservations', value: mockStats.activeReservations, icon: CalendarCheck, color: 'teal', change: '+5' },
  { label: 'USSD Sessions', value: mockStats.totalSessions, icon: BarChart3, color: 'sage', change: '+28%' },
  { label: 'SMS Sent', value: mockStats.smsSent.toLocaleString(), icon: MessageSquare, color: 'teal', change: '+156' },
  { label: 'Book Searches', value: mockStats.booksSearched, icon: TrendingUp, color: 'sage', change: '+42%' },
];

export default function DashboardOverview() {
  const recentReservations = mockReservations.slice(0, 5);

  return (
    <div className="space-y-10">
      <div>
        <h1 className="text-3xl font-extrabold text-gray-900 font-heading tracking-tight">Dashboard Overview</h1>
        <p className="text-sm text-gray-400 mt-2">Monitor library activity and user engagement.</p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {statCards.map((stat, idx) => {
          const Icon = stat.icon;
          const bgIcon = stat.color === 'teal' ? 'bg-teal/8' : 'bg-sage/8';
          const textIcon = stat.color === 'teal' ? 'text-teal' : 'text-sage';

          return (
            <div key={idx} className="bg-white p-6 rounded-2xl border border-gray-100 hover:shadow-xl hover:shadow-black/[0.03] transition-all duration-300 hover:-translate-y-0.5">
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 ${bgIcon} rounded-xl flex items-center justify-center`}>
                  <Icon className={`w-5 h-5 ${textIcon}`} />
                </div>
                <span className="text-xs font-semibold text-green-600 bg-green-50 px-2.5 py-1 rounded-full border border-green-100">
                  {stat.change}
                </span>
              </div>
              <p className="text-3xl font-extrabold text-gray-900">{stat.value}</p>
              <p className="text-sm text-gray-400 mt-1">{stat.label}</p>
            </div>
          );
        })}
      </div>

      {/* Recent Reservations */}
      <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden shadow-sm">
        <div className="p-6 border-b border-gray-50">
          <h2 className="font-heading font-bold text-gray-900 text-lg">Recent Reservations</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-cream/50">
                <th className="text-left px-5 py-3 font-medium text-gray-500">User</th>
                <th className="text-left px-5 py-3 font-medium text-gray-500">Book</th>
                <th className="text-left px-5 py-3 font-medium text-gray-500">Reserved</th>
                <th className="text-left px-5 py-3 font-medium text-gray-500">Due Date</th>
                <th className="text-left px-5 py-3 font-medium text-gray-500">Status</th>
              </tr>
            </thead>
            <tbody>
              {recentReservations.map((res) => {
                const user = mockUsers.find((u) => u.id === res.user_id);
                const book = mockBooks.find((b) => b.id === res.book_id);
                return (
                  <tr key={res.id} className="border-t border-gray-50 hover:bg-cream/30 transition-colors">
                    <td className="px-5 py-3 font-medium text-gray-900">{user?.name}</td>
                    <td className="px-5 py-3 text-gray-600">{book?.title}</td>
                    <td className="px-5 py-3 text-gray-500">{res.reserved_at}</td>
                    <td className="px-5 py-3 text-gray-500">{res.due_date}</td>
                    <td className="px-5 py-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        res.returned
                          ? 'bg-green-50 text-green-700'
                          : 'bg-amber-50 text-amber-700'
                      }`}>
                        {res.returned ? 'Returned' : 'Active'}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
