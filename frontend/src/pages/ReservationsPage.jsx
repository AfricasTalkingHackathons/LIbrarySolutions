import { mockReservations, mockBooks, mockUsers } from '../data/mockData';

export default function ReservationsPage() {
  const enriched = mockReservations.map((r) => ({
    ...r,
    user: mockUsers.find((u) => u.id === r.user_id),
    book: mockBooks.find((b) => b.id === r.book_id),
  }));

  const active = enriched.filter((r) => !r.returned);
  const returned = enriched.filter((r) => r.returned);

  return (
    <div className="space-y-10">
      <div>
        <h1 className="text-3xl font-extrabold text-gray-900 font-heading tracking-tight">Reservations</h1>
        <p className="text-sm text-gray-400 mt-2">Track all book reservations and returns.</p>
      </div>

      {/* Active */}
      <div>
        <h2 className="font-heading font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <span className="w-2 h-2 bg-amber-500 rounded-full" />
          Active Reservations ({active.length})
        </h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {active.map((res) => (
            <div key={res.id} className="bg-white rounded-2xl border border-gray-100 p-6 hover:shadow-xl hover:shadow-black/[0.03] transition-all duration-300 hover:-translate-y-0.5">
              <div className="flex items-center justify-between mb-3">
                <span className="px-2 py-1 bg-amber-50 text-amber-700 text-xs font-medium rounded-full">
                  Active
                </span>
                <span className="text-xs text-gray-400">#{res.id}</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-1">{res.book?.title}</h3>
              <p className="text-sm text-gray-500 mb-3">Reserved by {res.user?.name}</p>
              <div className="space-y-1 text-sm text-gray-500">
                <p>Reserved: <span className="text-gray-700">{res.reserved_at}</span></p>
                <p>Due: <span className="text-gray-700 font-medium">{res.due_date}</span></p>
              </div>
              <button className="mt-4 w-full py-2.5 bg-teal/10 text-teal text-sm font-medium rounded-xl hover:bg-teal/20 transition-all duration-200">
                Mark as Returned
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Returned */}
      <div>
        <h2 className="font-heading font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <span className="w-2 h-2 bg-green-500 rounded-full" />
          Returned ({returned.length})
        </h2>
        <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden shadow-sm">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-cream/50">
                <th className="text-left px-5 py-3 font-medium text-gray-500">Book</th>
                <th className="text-left px-5 py-3 font-medium text-gray-500">User</th>
                <th className="text-left px-5 py-3 font-medium text-gray-500">Reserved</th>
                <th className="text-left px-5 py-3 font-medium text-gray-500">Returned</th>
              </tr>
            </thead>
            <tbody>
              {returned.map((res) => (
                <tr key={res.id} className="border-t border-gray-50">
                  <td className="px-5 py-3 font-medium text-gray-900">{res.book?.title}</td>
                  <td className="px-5 py-3 text-gray-600">{res.user?.name}</td>
                  <td className="px-5 py-3 text-gray-500">{res.reserved_at}</td>
                  <td className="px-5 py-3">
                    <span className="text-green-600 font-medium">✓ Returned</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
