import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { motion } from 'framer-motion';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import USSDSimulator from './pages/USSDSimulator';
import BookManagement from './pages/BookManagement';
import UserManagement from './pages/UserManagement';
import Reservations from './pages/Reservations';
import Analytics from './pages/Analytics';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="container mx-auto px-4 py-8"
        >
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/ussd-simulator" element={<USSDSimulator />} />
            <Route path="/books" element={<BookManagement />} />
            <Route path="/users" element={<UserManagement />} />
            <Route path="/reservations" element={<Reservations />} />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </motion.div>
      </div>
    </Router>
  );
}

export default App;
