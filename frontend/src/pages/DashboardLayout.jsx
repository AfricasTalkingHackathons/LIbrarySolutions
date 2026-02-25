import { useState } from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  BookOpen,
  Users,
  CalendarCheck,
  BarChart3,
  Menu,
  X,
  ChevronRight,
} from 'lucide-react';

const sidebarLinks = [
  { name: 'Overview', path: '/dashboard', icon: LayoutDashboard },
  { name: 'Books', path: '/dashboard/books', icon: BookOpen },
  { name: 'Users', path: '/dashboard/users', icon: Users },
  { name: 'Reservations', path: '/dashboard/reservations', icon: CalendarCheck },
];

export default function DashboardLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  return (
    <div className="min-h-screen bg-gradient-to-br from-cream/40 via-white to-cream/30 pt-20">
      {/* Mobile sidebar toggle */}
      <button
        onClick={() => setSidebarOpen(!sidebarOpen)}
        className="lg:hidden fixed top-24 left-5 z-40 p-2.5 bg-white rounded-xl shadow-lg shadow-black/5 border border-gray-100"
      >
        {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
      </button>

      {/* Sidebar */}
      <aside
        className={`fixed top-20 left-0 bottom-0 w-72 bg-white/80 backdrop-blur-xl border-r border-gray-100/80 z-30 transform transition-transform duration-300 lg:translate-x-0 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="p-7">
          <h2 className="text-xs font-bold text-gray-400 uppercase tracking-[0.15em] mb-6">
            Librarian Panel
          </h2>
          <nav className="space-y-1.5">
            {sidebarLinks.map((link) => {
              const Icon = link.icon;
              const isActive = location.pathname === link.path;
              return (
                <Link
                  key={link.name}
                  to={link.path}
                  onClick={() => setSidebarOpen(false)}
                  className={`flex items-center gap-3.5 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 ${
                    isActive
                      ? 'bg-teal/10 text-teal shadow-sm'
                      : 'text-gray-500 hover:bg-cream hover:text-gray-900'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  {link.name}
                  {isActive && <ChevronRight className="w-4 h-4 ml-auto" />}
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="absolute bottom-0 left-0 right-0 p-7">
          <Link
            to="/"
            className="flex items-center gap-2 text-sm text-gray-400 hover:text-teal transition-colors duration-200"
          >
            ← Back to Home
          </Link>
        </div>
      </aside>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/20 backdrop-blur-sm z-20"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main content */}
      <main className="lg:ml-72 p-6 sm:p-8 lg:p-10">
        <Outlet />
      </main>
    </div>
  );
}
