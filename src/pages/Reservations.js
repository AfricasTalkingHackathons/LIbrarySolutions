import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter, Calendar, Clock, CheckCircle, XCircle, AlertCircle, BookOpen, User, Mail, Phone } from 'lucide-react';

const Reservations = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [selectedDate, setSelectedDate] = useState('');

  const reservations = [
    {
      id: 'RES0001',
      user: {
        name: 'John Kamau',
        phone: '+254712345678',
        email: 'john.kamau@email.com'
      },
      book: {
        title: 'Introduction to Physics',
        author: 'John Smith',
        isbn: '978-0-123456-78-9'
      },
      reservationDate: '2024-01-20',
      dueDate: '2024-01-27',
      returnDate: null,
      status: 'active',
      reminderSent: false,
      overdueDays: 0
    },
    {
      id: 'RES0002',
      user: {
        name: 'Jane Wanjiru',
        phone: '+254723456789',
        email: 'jane.wanjiru@email.com'
      },
      book: {
        title: 'Mathematics for Beginners',
        author: 'Jane Doe',
        isbn: '978-0-987654-32-1'
      },
      reservationDate: '2024-01-18',
      dueDate: '2024-01-25',
      returnDate: null,
      status: 'overdue',
      reminderSent: true,
      overdueDays: 2
    },
    {
      id: 'RES0003',
      user: {
        name: 'Michael Ochieng',
        phone: '+254734567890',
        email: 'michael.o@email.com'
      },
      book: {
        title: 'Chemistry Essentials',
        author: 'Robert Johnson',
        isbn: '978-0-555666-77-8'
      },
      reservationDate: '2024-01-15',
      dueDate: '2024-01-22',
      returnDate: '2024-01-21',
      status: 'returned',
      reminderSent: false,
      overdueDays: 0
    },
    {
      id: 'RES0004',
      user: {
        name: 'Sarah Achieng',
        phone: '+254745678901',
        email: 'sarah.achieng@email.com'
      },
      book: {
        title: 'English Literature',
        author: 'Sarah Williams',
        isbn: '978-0-999888-77-6'
      },
      reservationDate: '2024-01-22',
      dueDate: '2024-01-29',
      returnDate: null,
      status: 'active',
      reminderSent: false,
      overdueDays: 0
    },
    {
      id: 'RES0005',
      user: {
        name: 'David Mutua',
        phone: '+254756789012',
        email: 'david.mutua@email.com'
      },
      book: {
        title: 'Biology: Life Sciences',
        author: 'Michael Brown',
        isbn: '978-0-444333-22-1'
      },
      reservationDate: '2024-01-10',
      dueDate: '2024-01-17',
      returnDate: null,
      status: 'overdue',
      reminderSent: true,
      overdueDays: 8
    }
  ];

  const statusOptions = ['all', 'active', 'overdue', 'returned'];

  const filteredReservations = reservations.filter(reservation => {
    const matchesSearch = 
      reservation.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      reservation.user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      reservation.book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      reservation.user.phone.includes(searchTerm);
    
    const matchesStatus = selectedStatus === 'all' || reservation.status === selectedStatus;
    
    return matchesSearch && matchesStatus;
  });

  const stats = {
    total: reservations.length,
    active: reservations.filter(r => r.status === 'active').length,
    overdue: reservations.filter(r => r.status === 'overdue').length,
    returned: reservations.filter(r => r.status === 'returned').length
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-blue-100 text-blue-800';
      case 'overdue':
        return 'bg-red-100 text-red-800';
      case 'returned':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return <Clock className="h-4 w-4" />;
      case 'overdue':
        return <AlertCircle className="h-4 w-4" />;
      case 'returned':
        return <CheckCircle className="h-4 w-4" />;
      default:
        return <Clock className="h-4 w-4" />;
    }
  };

  const handleSendReminder = (reservationId) => {
    console.log('Sending reminder for reservation:', reservationId);
  };

  const handleMarkReturned = (reservationId) => {
    console.log('Marking reservation as returned:', reservationId);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Reservations</h1>
          <p className="mt-2 text-gray-600">Manage book reservations and returns</p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button className="btn btn-primary px-6 py-2">
            <Calendar className="h-4 w-4 mr-2" />
            New Reservation
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Reservations</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            </div>
            <div className="bg-blue-50 p-2 rounded-lg">
              <Calendar className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </div>
        
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Active</p>
              <p className="text-2xl font-bold text-blue-600">{stats.active}</p>
            </div>
            <div className="bg-blue-50 p-2 rounded-lg">
              <Clock className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </div>
        
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Overdue</p>
              <p className="text-2xl font-bold text-red-600">{stats.overdue}</p>
            </div>
            <div className="bg-red-50 p-2 rounded-lg">
              <AlertCircle className="h-6 w-6 text-red-600" />
            </div>
          </div>
        </div>
        
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Returned</p>
              <p className="text-2xl font-bold text-green-600">{stats.returned}</p>
            </div>
            <div className="bg-green-50 p-2 rounded-lg">
              <CheckCircle className="h-6 w-6 text-green-600" />
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
                placeholder="Search by reservation ID, user, book, or phone..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input pl-10"
              />
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Filter className="h-4 w-4 text-gray-400" />
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="input"
            >
              {statusOptions.map(status => (
                <option key={status} value={status}>
                  {status === 'all' ? 'All Status' : status.charAt(0).toUpperCase() + status.slice(1)}
                </option>
              ))}
            </select>
          </div>
          <div className="flex items-center space-x-2">
            <Calendar className="h-4 w-4 text-gray-400" />
            <input
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              className="input"
            />
          </div>
        </div>
      </div>

      {/* Reservations Table */}
      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Reservation
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  User
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Book
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Dates
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
              {filteredReservations.map((reservation, index) => (
                <motion.tr
                  key={reservation.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                  className="hover:bg-gray-50"
                >
                  <td className="px-6 py-4">
                    <div className="text-sm font-medium text-gray-900">{reservation.id}</div>
                    <div className="text-xs text-gray-500">Reserved: {reservation.reservationDate}</div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="space-y-1">
                      <div className="flex items-center text-sm text-gray-900">
                        <User className="h-3 w-3 mr-1" />
                        {reservation.user.name}
                      </div>
                      <div className="flex items-center text-xs text-gray-600">
                        <Phone className="h-3 w-3 mr-1" />
                        {reservation.user.phone}
                      </div>
                      <div className="flex items-center text-xs text-gray-600">
                        <Mail className="h-3 w-3 mr-1" />
                        {reservation.user.email}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="space-y-1">
                      <div className="flex items-center text-sm text-gray-900">
                        <BookOpen className="h-3 w-3 mr-1" />
                        {reservation.book.title}
                      </div>
                      <div className="text-xs text-gray-600">{reservation.book.author}</div>
                      <div className="text-xs text-gray-500">{reservation.book.isbn}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="space-y-1">
                      <div className="text-sm text-gray-600">
                        <span className="font-medium">Due:</span> {reservation.dueDate}
                      </div>
                      {reservation.returnDate && (
                        <div className="text-sm text-green-600">
                          <span className="font-medium">Returned:</span> {reservation.returnDate}
                        </div>
                      )}
                      {reservation.overdueDays > 0 && (
                        <div className="text-xs text-red-600 font-medium">
                          {reservation.overdueDays} days overdue
                        </div>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full flex items-center space-x-1 ${getStatusColor(reservation.status)}`}>
                        {getStatusIcon(reservation.status)}
                        <span>{reservation.status}</span>
                      </span>
                      {reservation.reminderSent && (
                        <span className="text-xs text-gray-500">Reminder sent</span>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-2">
                      {reservation.status === 'active' && (
                        <>
                          <button
                            onClick={() => handleSendReminder(reservation.id)}
                            className="text-blue-600 hover:text-blue-800"
                            title="Send Reminder"
                          >
                            <Mail className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => handleMarkReturned(reservation.id)}
                            className="text-green-600 hover:text-green-800"
                            title="Mark as Returned"
                          >
                            <CheckCircle className="h-4 w-4" />
                          </button>
                        </>
                      )}
                      {reservation.status === 'overdue' && (
                        <button
                          onClick={() => handleSendReminder(reservation.id)}
                          className="text-red-600 hover:text-red-800"
                          title="Send Urgent Reminder"
                        >
                          <AlertCircle className="h-4 w-4" />
                        </button>
                      )}
                    </div>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Reservations;
