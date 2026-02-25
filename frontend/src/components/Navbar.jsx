import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X, BookOpen, Sparkles } from 'lucide-react';

const navLinks = [
  { name: 'Home', path: '/' },
  { name: 'Features', path: '/#features' },
  { name: 'How It Works', path: '/#how-it-works' },
  { name: 'Impact', path: '/#impact' },
  { name: 'USSD Demo', path: '/demo' },
  { name: 'Dashboard', path: '/dashboard' },
];

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const isActive = (path) => {
    if (path === '/') return location.pathname === '/';
    return location.pathname.startsWith(path.replace('/#', ''));
  };

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      scrolled
        ? 'bg-white/80 backdrop-blur-xl shadow-lg shadow-black/[0.03] border-b border-gray-200/50'
        : 'bg-transparent'
    }`}>
      <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-10">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 bg-gradient-to-br from-teal to-teal-dark rounded-xl flex items-center justify-center group-hover:shadow-lg group-hover:shadow-teal/25 transition-all duration-300 group-hover:scale-105">
              <BookOpen className="w-5 h-5 text-white" />
            </div>
            <span className="font-heading text-xl font-bold text-gray-900">
              Maktaba<span className="gradient-text">AI</span>
            </span>
          </Link>

          {/* Desktop nav */}
          <div className="hidden lg:flex items-center gap-2">
            {navLinks.map((link) => (
              <Link
                key={link.name}
                to={link.path}
                className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                  isActive(link.path)
                    ? 'text-teal bg-teal/10 shadow-sm'
                    : 'text-gray-500 hover:text-gray-900 hover:bg-gray-100/80'
                }`}
              >
                {link.name}
              </Link>
            ))}
          </div>

          {/* CTA */}
          <div className="hidden lg:flex items-center gap-4">
            <Link
              to="/demo"
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-teal to-teal-dark text-white font-medium text-sm rounded-xl hover:shadow-lg hover:shadow-teal/25 transition-all duration-300 hover:-translate-y-0.5"
            >
              <Sparkles className="w-4 h-4" />
              Try USSD Demo
            </Link>
          </div>

          {/* Mobile toggle */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="lg:hidden p-2.5 rounded-xl text-gray-600 hover:bg-gray-100 transition-colors"
          >
            {isOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <div className="lg:hidden bg-white/95 backdrop-blur-xl border-t border-gray-100 shadow-2xl animate-fade-in-down">
          <div className="px-6 py-5 space-y-1.5">
            {navLinks.map((link) => (
              <Link
                key={link.name}
                to={link.path}
                onClick={() => setIsOpen(false)}
                className={`block px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                  isActive(link.path)
                    ? 'text-teal bg-teal/8 shadow-sm'
                    : 'text-gray-600 hover:text-teal hover:bg-cream'
                }`}
              >
                {link.name}
              </Link>
            ))}
            <Link
              to="/demo"
              onClick={() => setIsOpen(false)}
              className="block mt-4 px-5 py-3 bg-gradient-to-r from-teal to-teal-dark text-white text-center font-medium text-sm rounded-xl hover:shadow-lg transition-all"
            >
              Try USSD Demo
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
}
