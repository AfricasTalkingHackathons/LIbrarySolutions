import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import LandingPage from './pages/LandingPage';
import USSDDemo from './pages/USSDDemo';
import DashboardLayout from './pages/DashboardLayout';
import DashboardOverview from './pages/DashboardOverview';
import BooksPage from './pages/BooksPage';
import UsersPage from './pages/UsersPage';
import ReservationsPage from './pages/ReservationsPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/demo" element={<USSDDemo />} />
            <Route path="/dashboard" element={<DashboardLayout />}>
              <Route index element={<DashboardOverview />} />
              <Route path="books" element={<BooksPage />} />
              <Route path="users" element={<UsersPage />} />
              <Route path="reservations" element={<ReservationsPage />} />
            </Route>
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
