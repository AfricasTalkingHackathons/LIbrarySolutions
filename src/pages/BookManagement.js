import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Plus, Edit, Trash2, Eye, Filter, Download, Upload } from 'lucide-react';

const BookManagement = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [showAddModal, setShowAddModal] = useState(false);

  const books = [
    {
      id: 1,
      title: 'Introduction to Physics',
      author: 'John Smith',
      category: 'Science',
      isbn: '978-0-123456-78-9',
      available: true,
      totalCopies: 5,
      reservedCopies: 2,
      addedDate: '2024-01-15',
      summary: 'A comprehensive introduction to fundamental physics concepts including mechanics, thermodynamics, and electromagnetism.'
    },
    {
      id: 2,
      title: 'Mathematics for Beginners',
      author: 'Jane Doe',
      category: 'Mathematics',
      isbn: '978-0-987654-32-1',
      available: true,
      totalCopies: 8,
      reservedCopies: 1,
      addedDate: '2024-01-20',
      summary: 'Basic mathematical concepts covering algebra, geometry, and statistics for high school students.'
    },
    {
      id: 3,
      title: 'Chemistry Essentials',
      author: 'Robert Johnson',
      category: 'Science',
      isbn: '978-0-555666-77-8',
      available: false,
      totalCopies: 3,
      reservedCopies: 3,
      addedDate: '2024-01-10',
      summary: 'Essential chemistry concepts including atomic structure, chemical reactions, and organic chemistry basics.'
    },
    {
      id: 4,
      title: 'English Literature',
      author: 'Sarah Williams',
      category: 'Language',
      isbn: '978-0-999888-77-6',
      available: true,
      totalCopies: 6,
      reservedCopies: 0,
      addedDate: '2024-01-25',
      summary: 'A collection of classic English literature works with analysis and interpretation guides.'
    },
    {
      id: 5,
      title: 'Biology: Life Sciences',
      author: 'Michael Brown',
      category: 'Science',
      isbn: '978-0-444333-22-1',
      available: true,
      totalCopies: 4,
      reservedCopies: 1,
      addedDate: '2024-01-18',
      summary: 'Comprehensive biology textbook covering cell biology, genetics, evolution, and ecology.'
    }
  ];

  const categories = ['all', 'Science', 'Mathematics', 'Language', 'History', 'Geography'];

  const filteredBooks = books.filter(book => {
    const matchesSearch = book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         book.author.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         book.isbn.includes(searchTerm);
    const matchesCategory = selectedCategory === 'all' || book.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const stats = {
    total: books.length,
    available: books.filter(b => b.available).length,
    reserved: books.reduce((acc, b) => acc + b.reservedCopies, 0),
    categories: [...new Set(books.map(b => b.category))].length
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Book Management</h1>
          <p className="mt-2 text-gray-600">Manage library books and inventory</p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-2">
          <button className="btn btn-outline px-4 py-2">
            <Upload className="h-4 w-4 mr-2" />
            Import
          </button>
          <button className="btn btn-outline px-4 py-2">
            <Download className="h-4 w-4 mr-2" />
            Export
          </button>
          <button 
            onClick={() => setShowAddModal(true)}
            className="btn btn-primary px-4 py-2"
          >
            <Plus className="h-4 w-4 mr-2" />
            Add Book
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Books</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            </div>
            <div className="bg-blue-50 p-2 rounded-lg">
              <div className="w-6 h-6 bg-blue-500 rounded"></div>
            </div>
          </div>
        </div>
        
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Available</p>
              <p className="text-2xl font-bold text-green-600">{stats.available}</p>
            </div>
            <div className="bg-green-50 p-2 rounded-lg">
              <div className="w-6 h-6 bg-green-500 rounded"></div>
            </div>
          </div>
        </div>
        
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Reserved</p>
              <p className="text-2xl font-bold text-orange-600">{stats.reserved}</p>
            </div>
            <div className="bg-orange-50 p-2 rounded-lg">
              <div className="w-6 h-6 bg-orange-500 rounded"></div>
            </div>
          </div>
        </div>
        
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Categories</p>
              <p className="text-2xl font-bold text-purple-600">{stats.categories}</p>
            </div>
            <div className="bg-purple-50 p-2 rounded-lg">
              <div className="w-6 h-6 bg-purple-500 rounded"></div>
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
                placeholder="Search by title, author, or ISBN..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input pl-10"
              />
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Filter className="h-4 w-4 text-gray-400" />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="input"
            >
              {categories.map(category => (
                <option key={category} value={category}>
                  {category === 'all' ? 'All Categories' : category}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Books Table */}
      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Book Details
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Category
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  ISBN
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Availability
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Added Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredBooks.map((book, index) => (
                <motion.tr
                  key={book.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                  className="hover:bg-gray-50"
                >
                  <td className="px-6 py-4">
                    <div>
                      <div className="text-sm font-medium text-gray-900">{book.title}</div>
                      <div className="text-sm text-gray-500">by {book.author}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                      {book.category}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {book.isbn}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-2">
                      <div className={`w-2 h-2 rounded-full ${book.available ? 'bg-green-500' : 'bg-red-500'}`}></div>
                      <span className="text-sm text-gray-600">
                        {book.available ? 'Available' : 'Reserved'}
                      </span>
                      <span className="text-xs text-gray-400">
                        ({book.reservedCopies}/{book.totalCopies})
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {book.addedDate}
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

      {/* Add Book Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto"
          >
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Add New Book</h2>
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
                  <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
                  <input type="text" className="input" placeholder="Book title" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Author</label>
                  <input type="text" className="input" placeholder="Author name" />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">ISBN</label>
                  <input type="text" className="input" placeholder="978-0-123456-78-9" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                  <select className="input">
                    <option>Select category</option>
                    {categories.filter(c => c !== 'all').map(category => (
                      <option key={category} value={category}>{category}</option>
                    ))}
                  </select>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Total Copies</label>
                  <input type="number" className="input" placeholder="5" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Reserved Copies</label>
                  <input type="number" className="input" placeholder="0" />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Summary</label>
                <textarea className="input" rows="4" placeholder="Book summary..."></textarea>
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
                Add Book
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default BookManagement;
