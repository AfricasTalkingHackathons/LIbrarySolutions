import { useState } from 'react';
import { Search, Plus, BookOpen } from 'lucide-react';
import { mockBooks } from '../data/mockData';

export default function BooksPage() {
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('All');

  const categories = ['All', ...new Set(mockBooks.map((b) => b.category))];

  const filtered = mockBooks.filter((book) => {
    const matchSearch =
      book.title.toLowerCase().includes(search.toLowerCase()) ||
      book.author.toLowerCase().includes(search.toLowerCase());
    const matchCategory = categoryFilter === 'All' || book.category === categoryFilter;
    return matchSearch && matchCategory;
  });

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-900 font-heading tracking-tight">Books</h1>
          <p className="text-sm text-gray-400 mt-2">Manage your library's book collection.</p>
        </div>
        <button className="inline-flex items-center gap-2.5 px-5 py-2.5 bg-gradient-to-r from-teal to-teal-dark text-white text-sm font-medium rounded-xl hover:shadow-lg hover:shadow-teal/20 transition-all duration-300 hover:-translate-y-0.5">
          <Plus className="w-4 h-4" />
          Add Book
        </button>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search by title or author..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-white border border-gray-200 rounded-xl text-sm focus:outline-none focus:border-teal focus:ring-2 focus:ring-teal/10 transition-all"
          />
        </div>
        <div className="flex gap-2 flex-wrap">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setCategoryFilter(cat)}
              className={`px-4 py-2.5 text-sm rounded-xl font-medium transition-all duration-200 ${
                categoryFilter === cat
                  ? 'bg-teal text-white'
                  : 'bg-white text-gray-600 border border-gray-200 hover:border-teal/30'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Book Grid */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {filtered.map((book) => (
          <div key={book.id} className="bg-white rounded-2xl border border-gray-100 p-6 hover:shadow-xl hover:shadow-black/[0.03] transition-all duration-300 hover:-translate-y-0.5">
            <div className="flex items-start justify-between mb-4">
              <div className="w-12 h-12 bg-teal/8 rounded-xl flex items-center justify-center">
                <BookOpen className="w-5 h-5 text-teal" />
              </div>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                book.available
                  ? 'bg-green-50 text-green-700'
                  : 'bg-red-50 text-red-600'
              }`}>
                {book.available ? 'Available' : 'Checked Out'}
              </span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">{book.title}</h3>
            <p className="text-sm text-gray-500 mb-1">by {book.author}</p>
            <span className="inline-block px-2 py-0.5 bg-cream text-sage-dark text-xs rounded-md font-medium mb-3">
              {book.category}
            </span>
            <p className="text-sm text-gray-500 leading-relaxed line-clamp-2">{book.summary}</p>
          </div>
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-12">
          <BookOpen className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-400">No books found matching your criteria.</p>
        </div>
      )}
    </div>
  );
}
